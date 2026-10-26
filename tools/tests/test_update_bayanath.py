"""Simulation tests for tools/update_bayanath.py.

These tests run the real updater as a subprocess against a LOCAL fake YouTube (feed, oEmbed, channel page, Data API
and watch page). They prove the updater's logic. They do NOT prove that a real YouTube upload is picked up: that can
only be seen in a real workflow run (see the workflow run log in the Actions tab).

Run:  python3 -I -m unittest discover -s tools/tests -v
"""
import json, os, re, subprocess, sys, tempfile, threading, unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'tools' / 'update_bayanath.py'
CHANNEL_ID = 'UClF-O3ig9ZKMvbeKB4t9mjQ'
CONFIG = {'channel_handle': 'MuftiMaqsoodImran', 'channel_id': CHANNEL_ID, 'playlist_id': '',
          'title_keywords': ['bayan', 'bayanat', 'bayanath'], 'exclude_keywords': [], 'max_videos': 10}
SECRET = 'AIzaSy-SECRET-KEY-MUST-NEVER-APPEAR'

# The child processes get a CLEAN environment (so a developer's own YOUTUBE_API_KEY, proxy or PYTHON* settings can never leak into a
# test), but not an EMPTY one. On Windows a child Python started without SYSTEMROOT dies before running a line of code with
# "Fatal Python error: _Py_HashRandomization_Init: failed to get random numbers to initialize Python" (it also cannot open sockets or
# find a temp folder), so the few variables the operating system itself needs are passed through. None of them is a secret.
_OS_VARIABLES = ('PATH', 'SYSTEMROOT', 'WINDIR', 'SYSTEMDRIVE', 'COMSPEC', 'PATHEXT', 'TEMP', 'TMP', 'TMPDIR', 'HOME', 'USERPROFILE',
                 'LANG', 'LC_ALL', 'LD_LIBRARY_PATH')


def child_env(**extra):
    env = {k: os.environ[k] for k in _OS_VARIABLES if k in os.environ}
    env.update(extra)
    return env


def vid(n):
    return 'V' + str(n).zfill(10)  # always 11 characters


def entry(n, day, title=None, ok=True):
    return {'id': vid(n), 'title': title or f'Friday Bayan number {n} #jummabayan', 'published': f'2026-{(day // 28) + 1:02d}-{day % 28 + 1:02d}T10:00:00+00:00', 'ok': ok}


class Fake(BaseHTTPRequestHandler):
    state = {}
    seen = []

    def log_message(self, *a):
        pass

    def send(self, code, body, ctype='application/json'):
        b = body.encode() if isinstance(body, str) else body
        self.send_response(code); self.send_header('Content-Type', ctype); self.send_header('Content-Length', str(len(b))); self.end_headers(); self.wfile.write(b)

    def do_GET(self):
        u = urlparse(self.path); q = parse_qs(u.query); st = Fake.state
        Fake.seen.append((u.path, {k: v[0] for k, v in q.items()}, self.headers.get('X-Goog-Api-Key')))
        if u.path == '/redirect-feed':
            self.send_response(302); self.send_header('Location', 'http://example.invalid/feed'); self.send_header('Content-Length', '0'); self.end_headers()
            return
        if u.path == '/feed':
            if st.get('feed_status', 200) != 200:
                return self.send(st['feed_status'], 'nope')
            if 'feed_raw' in st:
                return self.send(200, st['feed_raw'], 'application/xml')
            ents = ''.join(f'<entry><yt:videoId>{e["id"]}</yt:videoId><title>{e["title"]}</title><published>{e["published"]}</published>'
                           f'<media:group><media:thumbnail url="https://i2.ytimg.com/vi/{e["id"]}/hqdefault.jpg"/></media:group></entry>' for e in st.get('feed', []))
            return self.send(200, '<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom" xmlns:yt="http://www.youtube.com/xml/schemas/2015" '
                                  f'xmlns:media="http://search.yahoo.com/mrss/">{ents}</feed>', 'application/xml')
        if u.path == '/oembed':
            v = q['url'][0].split('v=')[1]
            info = st.get('oembed', {}).get(v, 'ok')
            if st.get('oembed_down'):
                return self.send(503, 'down')
            if info == 'ok':
                return self.send(200, json.dumps({'title': st.get('full_titles', {}).get(v, 'x')}))
            return self.send(info, 'gone')
        if u.path.startswith('/@'):
            return self.send(200, f'<html>"channelId":"{st.get("page_channel", CHANNEL_ID)}"</html>', 'text/html')
        if u.path == '/api/playlistItems':
            if st.get('api_status', 200) != 200:
                return self.send(st['api_status'], '{}')
            return self.send(200, json.dumps({'items': [{'contentDetails': {'videoId': e['id']}} for e in st['api']]}))
        if u.path == '/api/videos':
            items = [{'id': e['id'], 'snippet': {'title': e['title'], 'publishedAt': e['published'], 'liveBroadcastContent': e.get('live', 'none')},
                      'status': {'privacyStatus': 'public' if e['ok'] else 'private', 'embeddable': True}} for e in st['api'] if e['id'] in q['id'][0].split(',')]
            return self.send(200, json.dumps({'items': items}))
        if u.path == '/watch':
            d = st.get('watch_dates', {}).get(q['v'][0])
            return self.send(200, f'<meta itemprop="uploadDate" content="{d}">' if d else '<html></html>', 'text/html')
        self.send(404, 'no')


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = ThreadingHTTPServer(('127.0.0.1', 0), Fake)
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()
        cls.base = f'http://127.0.0.1:{cls.srv.server_address[1]}'

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.cache = self.dir / 'bayanath-videos.json'
        self.cfg = self.dir / 'config.json'
        self.cfg.write_text(json.dumps(CONFIG))
        self.out = self.dir / 'output.txt'
        Fake.state = {}; Fake.seen = []

    def tearDown(self):
        self.tmp.cleanup()

    def seed(self, entries):
        vids = [{'id': e['id'], 'title': e['title'], 'published': e['published'], 'thumbnail': f'https://i2.ytimg.com/vi/{e["id"]}/hqdefault.jpg'} for e in entries]
        self.cache.write_text(json.dumps({'channel': {}, 'updated': '2026-01-01T00:00:00Z', 'videos': vids}, ensure_ascii=False, indent=2) + '\n')

    def run_updater(self, key=None, extra=None):
        env = child_env(BAYANATH_CONFIG=str(self.cfg), BAYANATH_CACHE=str(self.cache), GITHUB_OUTPUT=str(self.out),
                        YT_FEED_BASE=self.base + '/feed', YT_OEMBED_BASE=self.base + '/oembed', YT_CHANNEL_PAGE_BASE=self.base,
                        YT_API_BASE=self.base + '/api', YT_WATCH_BASE=self.base + '/watch')
        if key:
            env['YOUTUBE_API_KEY'] = key
        env.update(extra or {})
        p = subprocess.run([sys.executable, '-I', str(SCRIPT)], env=env, capture_output=True, text=True, timeout=120)
        return p

    def assertRefused(self, p, msg=None):
        """The updater really ran and refused: a non-zero exit code alone is also what a child that crashed on start-up returns."""
        self.assertNotEqual(p.returncode, 0, msg)
        self.assertNotIn('Fatal Python error', p.stderr, msg)
        self.assertNotIn('Traceback', p.stderr, msg)
        self.assertIn('ERROR:', p.stderr, msg)
        self.assertIn('The cached list was left untouched.', p.stderr, msg)

    def data(self):
        return json.loads(self.cache.read_text(encoding='utf-8'))

    def ids(self):
        return [v['id'] for v in self.data()['videos']]


class Schedule(unittest.TestCase):
    def test_saturday_2100_ist_cron_and_manual_trigger(self):
        text = (ROOT / '.github' / 'workflows' / 'update-bayanath.yml').read_text(encoding='utf-8')
        self.assertEqual(re.findall(r"^\s*- cron: '([^']+)'", text, re.M), ['30 15 * * 6'])  # 15:30 UTC Saturday == 21:00 IST Saturday
        self.assertIn('workflow_dispatch:', text)
        self.assertRegex(text, r'permissions:\s*\n\s+contents: write[^\n]*\n\s+actions: write')
        self.assertIn('steps.update.outputs.changed', text)
        self.assertIn('${{ secrets.YOUTUBE_API_KEY }}', text)
        self.assertNotIn('AIza', text)  # no key committed

    def test_every_action_is_pinned_to_a_full_commit(self):
        text = (ROOT / '.github' / 'workflows' / 'update-bayanath.yml').read_text(encoding='utf-8')
        uses = re.findall(r'^\s*- uses: (\S+)', text, re.M)
        self.assertEqual(len(uses), 2)
        for u in uses:
            self.assertRegex(u, r'^actions/(checkout|setup-python)@[0-9a-f]{40}$', u)

    def test_the_new_list_is_published_by_starting_the_pages_deployment(self):
        """A push made with GITHUB_TOKEN does not start other workflows, so without this step the JSON would be committed but never deployed."""
        text = (ROOT / '.github' / 'workflows' / 'update-bayanath.yml').read_text(encoding='utf-8')
        self.assertIn('gh workflow run deploy-pages.yml --ref "${GITHUB_REF_NAME}"', text)
        self.assertIn("if: steps.commit.outputs.pushed == 'true'", text)   # only after a real commit and push
        self.assertIn('GH_TOKEN: ${{ github.token }}', text)
        self.assertLess(text.index('git push origin'), text.index('gh workflow run deploy-pages.yml'))
        step = text[text.index('Publish the new list'):]
        self.assertIn('continue-on-error: true', step)   # the data is already committed: a refused dispatch must not hide that

    def test_a_short_outage_is_retried_and_a_lasting_one_fails_the_job(self):
        """Runs the real update step from the workflow in bash with a stand-in for the updater (and for sleep) to prove the retry behaviour."""
        import shutil, subprocess, tempfile
        bash = shutil.which('bash')
        if not bash:
            self.skipTest('bash is not installed')
        text = (ROOT / '.github' / 'workflows' / 'update-bayanath.yml').read_text(encoding='utf-8')
        block = re.search(r'id: update\n(?:.*\n)*?\s+run: \|\n((?:          .*\n|\n)+)', text).group(1)
        script = '\n'.join(line[10:] for line in block.splitlines())
        for fails_first, want_code, want_runs in ((0, 0, 1), (2, 0, 3), (3, 1, 3)):
            with tempfile.TemporaryDirectory() as d:
                d = Path(d)
                (d / 'tools').mkdir()
                (d / 'tools' / 'update_bayanath.py').write_text('x', encoding='utf-8')
                (d / 'bin').mkdir()
                fake = d / 'bin' / 'python3'
                fake.write_text('#!/bin/sh\necho run >> "%s/runs"\nn=$(wc -l < "%s/runs")\n[ "$n" -gt %d ]\n' % (d, d, fails_first), encoding='utf-8')
                nap = d / 'bin' / 'sleep'
                nap.write_text('#!/bin/sh\necho "$1" >> "%s/naps"\n' % d, encoding='utf-8')
                fake.chmod(0o755), nap.chmod(0o755)
                p = subprocess.run([bash, '-c', script], cwd=d, capture_output=True, text=True, env=child_env(PATH=f'{d}/bin:/usr/bin:/bin'), timeout=60)
                self.assertEqual(p.returncode, want_code, p.stdout + p.stderr)
                self.assertEqual(len((d / 'runs').read_text().split()), want_runs)
                if fails_first == 2:
                    self.assertEqual((d / 'naps').read_text().split(), ['120', '240'])   # 2 and 4 minutes
                if fails_first == 3:
                    self.assertIn('::error::', p.stdout)

    def test_the_workflow_does_not_depend_on_anything_but_python(self):
        text = (ROOT / '.github' / 'workflows' / 'update-bayanath.yml').read_text(encoding='utf-8')
        self.assertIn('python3 tools/update_bayanath.py', text)
        self.assertNotRegex(text, r'(?i)\bph' + r'p\b|\bssh\b|\bftp\b|rsync|cpa' + r'nel')   # nothing but Python and the repository

    def test_every_file_agrees_on_saturday_and_none_keeps_an_older_weekday(self):
        """One weekly slot, Saturday 21:00 Asia/Kolkata = GitHub cron `30 15 * * 6` (UTC). An earlier draft used Friday (5); no copy
        of it may survive in the workflow, the docs or the tests."""
        stale = [re.compile(p) for p in (r'30 15 \*' + r' \* 5', r"'weekday'" + r" => 5", r'Friday' + r' 21:00', r'Friday' + r' at 21:00',
                                         r'FRI' + r'_2105', r'next Friday' + r' slot', r'Friday' + r' 21:00')]
        files = [ROOT / 'README.md', ROOT / 'AGENTS.md', ROOT / '.github' / 'workflows' / 'update-bayanath.yml',
                 ROOT / 'tools' / 'update_bayanath.py'] + sorted((ROOT / 'tools' / 'tests').glob('test_*.py'))
        for f in files:
            text = f.read_text(encoding='utf-8')
            for rx in stale:
                self.assertIsNone(rx.search(text), f'{f.name}: stale Friday schedule ({rx.pattern})')
        self.assertIn('Saturday 21:00', (ROOT / 'README.md').read_text(encoding='utf-8'))
        self.assertIn('`30 15 * * 6`', (ROOT / 'README.md').read_text(encoding='utf-8') + (ROOT / 'AGENTS.md').read_text(encoding='utf-8'))

    def test_workflow_is_valid_yaml_when_pyyaml_present(self):
        try:
            import yaml
        except ImportError:
            self.skipTest('PyYAML not installed')
        doc = yaml.safe_load((ROOT / '.github' / 'workflows' / 'update-bayanath.yml').read_text(encoding='utf-8'))
        self.assertEqual(doc[True]['schedule'][0]['cron'], '30 15 * * 6')  # YAML parses the key `on` as boolean True
        self.assertIn('workflow_dispatch', doc[True])


class Updater(Base):
    def test_new_eligible_video_is_detected_and_unrelated_is_excluded(self):
        old = [entry(i, 20 - i) for i in range(1, 11)]
        self.seed(old)
        new = entry(11, 25)
        unrelated = entry(12, 26, title='Cooking class: biryani at home')
        Fake.state['feed'] = [unrelated, new] + old[:5]
        p = self.run_updater()
        self.assertEqual(p.returncode, 0, p.stderr)
        ids = self.ids()
        self.assertEqual(ids[0], new['id'])
        self.assertNotIn(unrelated['id'], ids)
        self.assertEqual(len(ids), 10)
        self.assertNotIn(old[-1]['id'], ids)  # the oldest fell out of the displayed ten
        self.assertIn('changed=true', self.out.read_text(encoding='utf-8'))
        self.assertTrue(any(f'channel_id' in q and q['channel_id'] == CHANNEL_ID for path, q, _ in Fake.seen if path == '/feed'))

    def test_duplicates_and_ordering(self):
        e = [entry(1, 10), entry(2, 12), entry(3, 11)]
        Fake.state['feed'] = [e[0], e[1], e[2], e[1], e[0]]  # duplicates in the feed
        self.cache.parent.mkdir(exist_ok=True)
        p = self.run_updater()
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(self.ids(), [e[1]['id'], e[2]['id'], e[0]['id']])  # newest first, no duplicates

    def test_fewer_than_ten_keeps_only_real_entries(self):
        Fake.state['feed'] = [entry(1, 3), entry(2, 4)]
        self.assertEqual(self.run_updater().returncode, 0)
        self.assertEqual(len(self.ids()), 2)

    def test_exactly_ten_when_more_available(self):
        Fake.state['feed'] = [entry(i, i) for i in range(1, 16)]
        self.assertEqual(self.run_updater().returncode, 0)
        self.assertEqual(len(self.ids()), 10)
        self.assertEqual(self.ids()[0], vid(15))

    def test_unchanged_feed_writes_nothing_and_reports_no_change(self):
        e = [entry(i, i) for i in range(1, 6)]
        Fake.state['feed'] = list(e)
        self.assertEqual(self.run_updater().returncode, 0)
        before, mtime = self.cache.read_bytes(), self.cache.stat().st_mtime_ns
        self.out.write_text('')
        p = self.run_updater()
        self.assertEqual(p.returncode, 0)
        self.assertEqual(before, self.cache.read_bytes())
        self.assertEqual(mtime, self.cache.stat().st_mtime_ns)
        self.assertIn('changed=false', self.out.read_text(encoding='utf-8'))
        self.assertIn('No change', p.stdout)

    def test_source_failure_keeps_valid_data(self):
        e = [entry(i, i) for i in range(1, 6)]
        self.seed(e)
        before = self.cache.read_bytes()
        Fake.state['feed_status'] = 500
        p = self.run_updater()
        self.assertRefused(p)
        self.assertEqual(before, self.cache.read_bytes())

    def test_invalid_responses_cannot_overwrite_the_feed(self):
        self.seed([entry(i, i) for i in range(1, 6)])
        before = self.cache.read_bytes()
        for raw in ('<html>not xml', '<feed xmlns="http://www.w3.org/2005/Atom"></feed>',
                    '<feed xmlns="http://www.w3.org/2005/Atom" xmlns:yt="http://www.youtube.com/xml/schemas/2015"><entry><yt:videoId>bad id!</yt:videoId><title>Bayan</title><published>x</published></entry></feed>'):
            Fake.state['feed_raw'] = raw
            p = self.run_updater()
            self.assertRefused(p, raw)
            self.assertEqual(before, self.cache.read_bytes(), raw)

    def test_only_unrelated_videos_is_a_failure_not_an_empty_list(self):
        self.seed([entry(1, 1)])
        before = self.cache.read_bytes()
        Fake.state['feed'] = [entry(2, 5, title='Cricket highlights')]
        self.assertRefused(self.run_updater())
        self.assertEqual(before, self.cache.read_bytes())

    def test_wrong_channel_is_refused(self):
        self.seed([entry(1, 1)])
        before = self.cache.read_bytes()
        Fake.state['page_channel'] = 'UCzzzzzzzzzzzzzzzzzzzzzz'
        Fake.state['feed'] = [entry(2, 5)]
        self.assertRefused(self.run_updater())
        self.assertEqual(before, self.cache.read_bytes())

    def test_deleted_private_video_is_dropped_and_oembed_outage_keeps_old_entries(self):
        e = [entry(i, i) for i in range(1, 5)]
        self.seed(e)
        Fake.state['feed'] = list(e)
        Fake.state['oembed'] = {e[3]['id']: 404}
        self.assertEqual(self.run_updater().returncode, 0)
        self.assertNotIn(e[3]['id'], self.ids())
        Fake.state['oembed'] = {}; Fake.state['oembed_down'] = True
        before = self.cache.read_bytes()
        self.assertEqual(self.run_updater().returncode, 0)  # cannot verify -> keep earlier entries
        self.assertEqual(before, self.cache.read_bytes())

    def test_truncated_title_is_repaired_and_missing_date_filled(self):
        a = entry(1, 20); b = entry(2, 5)
        self.seed([a, {**b, 'title': 'Friday Bayan number 2 #jumma...', 'published': None}])
        Fake.state['feed'] = [a]
        Fake.state['full_titles'] = {b['id']: 'Friday Bayan number 2 #jummabayan #full'}
        Fake.state['watch_dates'] = {b['id']: '2026-07-03'}
        self.assertEqual(self.run_updater().returncode, 0)
        v = {x['id']: x for x in self.data()['videos']}[b['id']]
        self.assertEqual(v['title'], 'Friday Bayan number 2 #jummabayan #full')
        self.assertEqual(v['published'], '2026-07-03T00:00:00+00:00')

    def test_a_missing_date_is_never_invented(self):
        a = entry(1, 20)
        self.seed([a, {**entry(2, 5), 'published': None}])
        Fake.state['feed'] = [a]
        self.assertEqual(self.run_updater().returncode, 0)
        self.assertIsNone({x['id']: x for x in self.data()['videos']}[vid(2)]['published'])

    def test_result_is_valid_json_that_the_site_check_accepts(self):
        Fake.state['feed'] = [entry(i, i) for i in range(1, 12)]
        self.assertEqual(self.run_updater().returncode, 0)
        d = json.loads(self.cache.read_text(encoding='utf-8'))
        self.assertEqual(set(d), {'channel', 'updated', 'videos'})  # schema unchanged
        for v in d['videos']:
            self.assertEqual(set(v), {'id', 'title', 'published', 'thumbnail'})
            self.assertRegex(v['id'], r'^[A-Za-z0-9_-]{11}$')
        self.assertEqual(len({v['id'] for v in d['videos']}), len(d['videos']))


class Api(Base):
    def test_api_mode_uses_uploads_playlist_header_key_and_never_prints_it(self):
        api = [entry(i, i) for i in range(1, 13)]
        api[0]['ok'] = False  # private
        Fake.state['api'] = api
        p = self.run_updater(key=SECRET)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertNotIn(SECRET, p.stdout + p.stderr + self.cache.read_text(encoding='utf-8'))
        pl = [q for path, q, k in Fake.seen if path == '/api/playlistItems']
        self.assertEqual(pl[0]['playlistId'], 'UU' + CHANNEL_ID[2:])
        self.assertTrue(all(k == SECRET for path, q, k in Fake.seen if path.startswith('/api/')))
        self.assertFalse(any(SECRET in json.dumps(q) for path, q, k in Fake.seen))  # key is a header, not in the URL
        self.assertNotIn(vid(1), self.ids())
        self.assertEqual(len(self.ids()), 10)

    def test_api_failure_falls_back_to_rss(self):
        Fake.state['api'] = []
        Fake.state['api_status'] = 403
        Fake.state['feed'] = [entry(1, 3)]
        p = self.run_updater(key=SECRET)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertNotIn(SECRET, p.stdout + p.stderr)
        self.assertEqual(self.ids(), [vid(1)])
        self.assertIn('falling back', p.stdout)

    def test_upcoming_premiere_is_not_listed(self):
        up = entry(2, 9); up['live'] = 'upcoming'
        Fake.state['api'] = [entry(1, 3), up]
        self.assertEqual(self.run_updater(key=SECRET).returncode, 0)
        self.assertEqual(self.ids(), [vid(1)])


class Safety(Base):
    def test_a_redirect_off_the_trusted_hosts_is_refused_and_the_list_kept(self):
        self.seed([entry(1, 3)])
        before = self.cache.read_text(encoding='utf-8')
        p = self.run_updater(key=SECRET, extra={'YT_FEED_BASE': self.base + '/redirect-feed'})
        self.assertRefused(p)
        self.assertIn('refusing a redirect', p.stderr)
        self.assertEqual(self.cache.read_text(encoding='utf-8'), before)
        self.assertNotIn(SECRET, p.stdout + p.stderr)

    def test_only_https_youtube_hosts_or_the_local_test_server_may_be_fetched(self):
        self.seed([entry(1, 3)])
        before = self.cache.read_text(encoding='utf-8')
        for bad in ('file:///etc/passwd', 'ftp://example.com/feed', 'https://example.com/feed', 'http://www.youtube.com/feeds/videos.xml'):
            p = self.run_updater(extra={'YT_FEED_BASE': bad})
            self.assertRefused(p, bad)
            self.assertIn('refusing to fetch', p.stderr, bad)
            self.assertEqual(self.cache.read_text(encoding='utf-8'), before, bad)


if __name__ == '__main__':
    unittest.main()
