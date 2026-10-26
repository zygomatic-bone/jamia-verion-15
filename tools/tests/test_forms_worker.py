"""Tests of the replacement for the old PHP form handler: the Cloudflare Worker in serverless/forms-worker/ and its wiring.

  * The Worker's own behaviour is tested in serverless/forms-worker/test/worker.test.mjs with Node's built-in test runner (no dependencies,
    no network: the mail provider and the counter store are faked). This file runs it, and skips (not passes) when Node 20+ is missing.
  * The generated rules file must match tools/connect/forms-schema.json, so a page and the service cannot drift apart.
  * The committed configuration holds no secret.
  * No PHP may come back: no .php file, no PHP endpoint, no PHP command anywhere in the project.

Run:  python3 -I -m unittest discover -s tools/tests -v
"""
import json, re, shutil, subprocess, sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_forms_worker as G          # noqa: E402
from test_update_bayanath import child_env  # noqa: E402

WORKER = ROOT / 'serverless' / 'forms-worker'
NODE = shutil.which('node')


def node_major():
    if not NODE:
        return 0
    try:
        out = subprocess.run([NODE, '--version'], capture_output=True, text=True, timeout=20, env=child_env()).stdout
        return int(re.match(r'v(\d+)', out).group(1))
    except (OSError, subprocess.SubprocessError, AttributeError):
        return 0


class WorkerBehaviour(unittest.TestCase):
    @unittest.skipUnless(node_major() >= 20, 'Node.js 20 or newer is not installed')
    def test_node_test_suite_passes(self):
        p = subprocess.run([NODE, '--test'], cwd=WORKER, capture_output=True, text=True, timeout=180, env=child_env())
        self.assertEqual(p.returncode, 0, p.stdout[-3000:] + p.stderr[-1000:])
        passed = int(re.search(r'^# pass (\d+)', p.stdout, re.M).group(1))
        failed = int(re.search(r'^# fail (\d+)', p.stdout, re.M).group(1))
        skipped = int(re.search(r'^# skipped (\d+)', p.stdout, re.M).group(1))
        self.assertEqual((failed, skipped), (0, 0))
        self.assertGreaterEqual(passed, 18)   # a suite that quietly lost its tests is not a pass


class Wiring(unittest.TestCase):
    def test_generated_rules_match_the_schema(self):
        self.assertEqual((WORKER / 'src' / 'schema.generated.js').read_text(encoding='utf-8'), G.render(),
                         'schema.generated.js is out of date: run python tools/build.py')

    def test_the_schema_is_consistent(self):
        schema = json.loads((ROOT / 'tools' / 'connect' / 'forms-schema.json').read_text(encoding='utf-8'))
        for name, d in schema['forms'].items():
            names = [f['name'] for f in d['fields']]
            self.assertEqual(len(names), len(set(names)), name)
            for f in d['fields']:
                self.assertIn(f['type'], ('text', 'line', 'phone', 'email', 'int', 'choice', 'bool'))
                if f['type'] == 'choice':
                    self.assertIn(f['limit'], schema['choices'], f'{name}.{f["name"]}')
                    values = [v for v, _ in schema['choices'][f['limit']]]
                    self.assertEqual(len(values), len(set(values)))
            self.assertTrue(set(d['min']) <= set(names), name)
        self.assertLess(schema['max_body_bytes'], 100_000)

    def test_committed_configuration_holds_no_secret(self):
        toml = (WORKER / 'wrangler.toml').read_text(encoding='utf-8')
        code = ''.join(p.read_text(encoding='utf-8') for p in (WORKER / 'src').glob('*.js'))
        for text in (toml, code):
            self.assertNotRegex(text, r're_[A-Za-z0-9_]{16,}', 'a mail-provider key')
            self.assertNotRegex(text, r'(?i)(api[_-]?key|secret|salt|token|password)\s*=\s*"[^"]{8,}"', 'a secret value')
        self.assertNotIn('RESEND_API_KEY', toml.split('[vars]')[1].split('[[kv_namespaces]]')[0])   # only ever a secret, never a var
        self.assertNotIn('RATE_SALT =', toml)
        ignored = (WORKER / '.gitignore').read_text(encoding='utf-8').split()
        for name in ('.dev.vars', '.wrangler/', 'node_modules/'):
            self.assertIn(name, ignored)   # Wrangler keeps local secrets in .dev.vars: it must never be committable
        self.assertIn('REPLACE_WITH_THE_ID', toml)   # the placeholder is visible: the setup step cannot be forgotten silently
        self.assertNotIn("Access-Control-Allow-Origin': '*'", code)
        self.assertNotRegex(code, r'\beval\(|new Function\(')

    def test_the_worker_has_no_dependencies(self):
        pkg = json.loads((WORKER / 'package.json').read_text(encoding='utf-8'))
        self.assertFalse(pkg.get('dependencies') or pkg.get('devDependencies'))
        for p in (WORKER / 'src').glob('*.js'):
            for spec in re.findall(r"^import .* from '([^']+)'", p.read_text(encoding='utf-8'), re.M):
                self.assertTrue(spec.startswith('./'), f'{p.name} imports {spec}')


class NoPhp(unittest.TestCase):
    """The site is hosted as static files (GitHub Pages), where PHP cannot run. None may remain."""
    ALLOWED_MENTIONS = {'test_forms_worker.py', 'check_site.py'}   # this file, and the rule that refuses a .php file in public/

    def project_files(self):
        for p in ROOT.rglob('*'):
            rel = p.relative_to(ROOT).parts
            if p.is_file() and '.git' not in rel and '__pycache__' not in rel and 'node_modules' not in rel:
                yield p

    def test_no_php_file_or_old_endpoint_exists(self):
        files = list(self.project_files())
        self.assertGreater(len(files), 100)
        self.assertEqual([str(p.relative_to(ROOT)) for p in files if re.search(r'\.php[0-9]?$', p.name, re.I)], [])
        self.assertFalse((ROOT / 'jame-server').exists())
        self.assertFalse((ROOT / 'public' / 'api').exists())

    def test_no_text_file_mentions_php_or_the_removed_handler(self):
        rx = re.compile(r'(?i)\bphp\b|\.php\b|jame-server|submit\.php|cpanel|JAME_CONFIG|JAME_SERVER')
        offenders = []
        for p in self.project_files():
            if p.suffix.lower() not in ('.md', '.py', '.js', '.mjs', '.json', '.yml', '.yaml', '.toml', '.html', '.css', '.txt', '.xml', '') or p.name in self.ALLOWED_MENTIONS:
                continue
            try:
                text = p.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                continue
            if rx.search(text):
                offenders.append(str(p.relative_to(ROOT)))
        self.assertEqual(offenders, [])

    def test_the_site_check_refuses_a_php_file_in_the_published_folder(self):
        import check_site
        for name in ('api/submit.php', 'x.php', 'x.PHP', 'old.php5'):
            self.assertRegex(name, check_site.FORBIDDEN)
        for name in ('index.html', 'data/bayanath-videos.json', 'portal-assets/forms.js'):
            self.assertNotRegex(name, check_site.FORBIDDEN)


if __name__ == '__main__':
    unittest.main()
