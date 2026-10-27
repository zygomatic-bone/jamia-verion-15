"""Tests of the form service (the Cloudflare Worker in serverless/forms-worker/) and of the pages that use it.

  * The Worker's own behaviour is tested in serverless/forms-worker/test/worker.test.mjs with Node's built-in test runner (no dependencies,
    no network: the mail provider and the counter store are faked). This file runs it, and skips (not passes) when Node 20+ is missing.
  * The Feedback, Admissions and Careers pages must agree with the rules in serverless/forms-worker/src/schema.js: same form names, same
    field names, same choice values, same limits. A mismatch would make a form that looks fine but is always refused.
  * The committed configuration holds no secret.
  * No PHP may come back: no .php file, no PHP endpoint, no PHP command anywhere in the project.

Run:  python3 -I -m unittest discover -s tools/tests -v
"""
import json, re, shutil, subprocess, sys, unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUB = ROOT / 'public'
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_update_bayanath import child_env  # noqa: E402

WORKER = ROOT / 'serverless' / 'forms-worker'
NODE = shutil.which('node')
EMAIL = 'jamiaululoom@gmail.com'
FILES = (('feedback', 'Feedback.html'), ('admissions', 'Admissions.html'), ('careers', 'Careers.html'))


def load_schema():
    text = (WORKER / 'src' / 'schema.js').read_text(encoding='utf-8')
    body = text[text.index('export default') + len('export default'):].strip().rstrip(';')
    return json.loads(body)


SCHEMA = load_schema()


class FormParser(HTMLParser):
    """Collects the controls of the <form data-cx-form="..."> in a page."""

    def __init__(self, kind):
        super().__init__()
        self.kind, self.inside, self.form, self.controls, self.options, self._select = kind, False, {}, [], {}, None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'form' and a.get('data-cx-form') == self.kind:
            self.inside, self.form = True, a
        elif self.inside and tag in ('input', 'select', 'textarea'):
            self.controls.append((tag, a))
            self._select = a.get('name') if tag == 'select' else None
        elif self.inside and tag == 'option' and self._select:
            self.options.setdefault(self._select, []).append(a.get('value', ''))

    def handle_endtag(self, tag):
        if tag == 'form':
            self.inside = False
        elif tag == 'select':
            self._select = None


def page(name):
    return (PUB / name).read_text(encoding='utf-8')


def parse(kind, file):
    p = FormParser(kind)
    p.feed(page(file))
    return p


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
    def test_the_schema_is_consistent(self):
        schema = SCHEMA
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

    def test_choice_lists_match_the_schema(self):
        for kind, file in FILES:
            p = parse(kind, file)
            for f in SCHEMA['forms'][kind]['fields']:
                if f['type'] != 'choice':
                    continue
                want = [v for v, _ in SCHEMA['choices'][f['limit']]]
                radios = [a['value'] for t, a in p.controls if t == 'input' and a.get('type') == 'radio' and a.get('name') == f['name']]
                got = radios or [v for v in p.options.get(f['name'], []) if v]
                self.assertEqual(got, want, f'{kind}.{f["name"]}')

    def test_every_form_field_is_in_the_schema_and_every_schema_field_is_in_the_form(self):
        for kind, file in FILES:
            p = parse(kind, file)
            names = {a['name'] for _, a in p.controls if a.get('name')} - {'form', 'opened', 'website'}
            self.assertEqual(names, {f['name'] for f in SCHEMA['forms'][kind]['fields']}, kind)
            self.assertTrue(any(a.get('name') == 'website' for _, a in p.controls), 'honeypot field')
            self.assertTrue(any(a.get('name') == 'form' and a.get('value') == kind for _, a in p.controls))
            self.assertEqual(p.form.get('method'), 'post')

    def test_required_attributes_and_length_limits_match_the_schema(self):
        for kind, file in FILES:
            p = parse(kind, file)
            for f in SCHEMA['forms'][kind]['fields']:
                ctl = [a for _, a in p.controls if a.get('name') == f['name']]
                self.assertTrue(ctl, f['name'])
                self.assertEqual('required' in ctl[0], f['required'], f'{kind}.{f["name"]} required')
                if f['type'] in ('line', 'text', 'email', 'phone') and 'maxlength' in ctl[0]:
                    self.assertEqual(int(ctl[0]['maxlength']), f['limit'], f'{kind}.{f["name"]} maxlength')

    def test_forms_post_to_the_configured_service_or_hand_over_to_the_email_program(self):
        for kind, file in FILES:
            p = parse(kind, file)
            action = p.form.get('action', '')
            self.assertNotRegex(action, r'(?i)\.ph' + r'p|^/|^\.|api/', kind)
            if action.startswith('https://'):
                self.assertNotIn('data-cx-offline', p.form)
            else:
                self.assertEqual(action, f'mailto:{EMAIL}', kind)
                self.assertIn('data-cx-offline', p.form)
                self.assertEqual(p.form.get('enctype'), 'text/plain')


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
        rx = re.compile(r'(?i)\bphp\b|\.php\b|jame-server|submit\.php|JAME_CONFIG|JAME_SERVER')
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
