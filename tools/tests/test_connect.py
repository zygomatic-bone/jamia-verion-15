"""The Contact, Feedback, Admissions and Careers pages must agree with the form service's rules (tools/connect/forms-schema.json, the one
file both the pages and serverless/forms-worker are built from): same form names, same field names, same choice values, same limits.
A mismatch would make a form that looks fine but is always refused."""
import json, re, sys, unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUB = ROOT / 'public'
sys.path.insert(0, str(ROOT / 'tools' / 'connect'))
import connect_pages as C

SCHEMA = json.loads((ROOT / 'tools' / 'connect' / 'forms-schema.json').read_text(encoding='utf-8'))
CONFIG = json.loads((ROOT / 'tools' / 'connect' / 'forms-config.json').read_text(encoding='utf-8'))
FILES = (('feedback', 'Feedback.html'), ('admissions', 'Admissions.html'), ('careers', 'Careers.html'))


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


def parse(kind, file):
    p = FormParser(kind)
    p.feed(page(file))
    return p


def page(name):
    return (PUB / name).read_text(encoding='utf-8')


class Connect(unittest.TestCase):
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
            for name, n in SCHEMA['forms'][kind]['min'].items():
                self.assertLessEqual(n, next(f['limit'] for f in SCHEMA['forms'][kind]['fields'] if f['name'] == name))

    def test_forms_post_to_the_configured_service_or_say_plainly_that_none_is_set_up(self):
        for kind, file in FILES:
            p = parse(kind, file)
            action = p.form.get('action', '')
            html = page(file)
            self.assertNotRegex(action, r'(?i)\.ph' + r'p|^/|^\.|api/', kind)   # no relative endpoint left over from an earlier design
            if CONFIG['endpoint']:
                self.assertEqual(action, CONFIG['endpoint'], kind)
                self.assertNotIn('data-cx-offline', p.form)
            else:
                self.assertEqual(action, f'mailto:{C.EMAIL}', kind)
                self.assertIn('data-cx-offline', p.form)
                self.assertEqual(p.form.get('enctype'), 'text/plain')
                self.assertIn('class="cx-fallback cx-handoff"', html)   # the quiet "your email program should now be open" line, hidden until used

    def test_no_page_shows_a_setup_warning_or_makes_the_site_look_unfinished(self):
        """Visitors must never read about services, accounts or configuration, or that something is not live yet."""
        rx = re.compile(r'(?i)not (yet )?(live|switched on|set up|configured|connected)|(currently|temporarily) unavailable|coming soon|'
                        r'cloudflare|resend|wrangler|\bworker\b|api key|deploy(ed|ment)?\b|backend|serverless|form service|endpoint|todo|lorem ipsum')
        for kind, file in FILES + (('contact', 'Contact.html'),):
            html = re.sub(r'(?s)<(script|style)[^>]*>.*?</\1>', '', page(file))
            text = re.sub(r'<[^>]+>', ' ', html)
            self.assertIsNone(rx.search(text), f'{file}: {rx.search(text) and rx.search(text).group(0)}')

    def test_the_thank_you_panels_say_plainly_that_the_message_was_sent(self):
        for kind, file in FILES:
            self.assertIn('Thank you! Your message has been sent successfully.', page(file), file)

    def test_the_forms_show_a_sending_state_and_the_script_changes_the_button_label(self):
        js = (PUB / 'portal-assets' / 'forms.js').read_text(encoding='utf-8')
        self.assertIn("'Sending\\u2026'", js)
        for _, file in FILES:
            self.assertIn('cx-submit-label', page(file))
        css = (PUB / 'portal-assets' / 'connect.css').read_text(encoding='utf-8')
        self.assertIn('.cx-form.is-busy .cx-spin', css)

    def test_the_endpoint_setting_accepts_only_a_plain_https_address(self):
        self.assertEqual(C._endpoint(''), '')
        self.assertEqual(C._endpoint('https://jame-forms.example.workers.dev/submit'), 'https://jame-forms.example.workers.dev/submit')
        for bad in ('http://forms.example/x', 'javascript:alert(1)', '//forms.example/x', 'forms.example', 'https://u:p@forms.example/x',
                    'https://forms.example/x?a=1', 'https://forms.example/x#f', 'https://forms.example/ x', 'https://forms.example/"x', "https://forms.example/'x",
                    'https://forms.example/<x>', 'https:///x', '/api/submit'):
            with self.assertRaises(SystemExit, msg=bad):
                C._endpoint(bad)

    def test_the_content_security_policy_names_the_service_only_when_one_is_set(self):
        headers = (PUB / '_headers').read_text(encoding='utf-8')
        htaccess = (PUB / '.htaccess').read_text(encoding='utf-8')
        origin = C.ENDPOINT_ORIGIN
        for text in (headers, htaccess):
            if origin:
                self.assertIn(f"connect-src 'self' {origin};", text)
                self.assertIn(f"form-action 'self' {origin};", text)
            else:
                self.assertIn("connect-src 'self';", text)
                self.assertIn("form-action 'self';", text)
            self.assertNotIn('*', re.search(r"connect-src[^;]*;", text).group(0))

    def test_the_requested_wording_is_present(self):
        fb = page('Feedback.html')
        self.assertIn('<h1>Your Voice Matters. Your Thoughts Inspire Us.</h1>', fb)
        self.assertIn('Thank You for Being Part of Our Journey 💙', fb)
        self.assertIn('Your thoughts help us grow, improve, and serve our community better. We truly appreciate you taking the time to share them with us.', fb)
        self.assertIn('Every Great Journey Begins With a First Step.', page('Admissions.html'))
        self.assertIn('Build Your Future. Make a Difference.', page('Careers.html'))

    def test_no_invented_vacancies_and_no_bank_details(self):
        self.assertIn('No specific vacancies are published', page('Careers.html'))
        for f in ('Contact.html', 'Feedback.html', 'Admissions.html', 'Careers.html'):
            t = page(f).lower()
            for word in ('ifsc', 'account number', 'a/c no', 'savings account'):
                self.assertNotIn(word, t, f)

    def test_the_forms_never_claim_to_be_an_application_and_say_what_they_are(self):
        self.assertIn('not an application', page('Admissions.html'))
        self.assertIn('not a job application', page('Careers.html'))

    def test_pages_load_their_own_assets_and_nothing_inline(self):
        for f in ('Contact.html', 'Feedback.html', 'Admissions.html', 'Careers.html'):
            html = page(f)
            self.assertIn('portal-assets/connect.css', html, f)
            self.assertIn('portal-assets/forms.js', html, f)
            self.assertIn('class="page-connect"', html, f)
            self.assertEqual(re.findall(r'<script(?![^>]*\ssrc=)[^>]*>', html), [], f)
            self.assertNotIn(' style=', html, f)
        self.assertNotIn('forms.js', page('Bayanath.html'))

    def test_feedback_is_in_the_menu_and_footer_of_every_root_page(self):
        for f in ('index.html', 'Contact.html', 'Transport.html'):
            self.assertIn('href="Feedback.html"', page(f), f)

    def test_the_phone_numbers_are_exactly_the_published_ones(self):
        printed = {n for _, ns in C.PHONES for n in ns}
        self.assertEqual(len(printed), 12)
        html = page('Contact.html')
        for n in printed:
            self.assertIn(f'href="tel:{n}"', html)
        self.assertIn('mailto:jamiaululoom@gmail.com', html)


if __name__ == '__main__':
    unittest.main()
