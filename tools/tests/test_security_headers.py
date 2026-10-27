"""Checks the security headers (public/_headers and public/.htaccess).

Run:  python3 -I -m unittest discover -s tools/tests -v
"""
import re, unittest
from pathlib import Path

PUB = Path(__file__).resolve().parents[2] / 'public'
REQUIRED = ('X-Content-Type-Options: nosniff', 'X-Frame-Options: DENY', 'Referrer-Policy:', 'Strict-Transport-Security:', 'Cross-Origin-Opener-Policy:')


def site_wide():
    text = (PUB / '_headers').read_text(encoding='utf-8')
    block = re.search(r'^/\*\n((?:[ \t]+.+\n)+)', text, re.M)
    return text, block.group(1)


class Headers(unittest.TestCase):
    def test_every_page_gets_the_security_headers(self):
        text, block = site_wide()
        for line in REQUIRED:
            self.assertIn(line, block)

    def test_policy_allows_no_inline_or_eval_code_and_no_framing(self):
        text, block = site_wide()
        csp = re.search(r'Content-Security-Policy: (.+)', block).group(1)
        for bad in ("'unsafe-inline'", "'unsafe-eval'", ' * ', 'http:'):
            self.assertNotIn(bad, csp)
        for good in ("default-src 'self'", "script-src 'self'", "object-src 'none'", "frame-ancestors 'none'", "base-uri 'self'", "form-action 'self'"):
            self.assertIn(good, csp)
        self.assertIn('frame-src https://www.youtube-nocookie.com;', csp)   # Bayanath player, nothing else

    def test_no_header_is_set_twice_for_the_residential_school(self):
        text, block = site_wide()
        rs = re.search(r'^/ResidentialSchoolBanikuppa/\*\n((?:[ \t]+.+\n)+)', text, re.M).group(1)
        names = lambda b: [l.split(':')[0].strip() for l in b.splitlines()]
        self.assertEqual(names(rs), ['Content-Security-Policy'])   # the stricter extra policy; other headers come once, from /*
        self.assertIn("frame-src 'none'", rs)

    def test_apache_root_file_carries_the_same_headers(self):
        ht = (PUB / '.htaccess').read_text(encoding='utf-8')
        _, block = site_wide()
        for line in block.splitlines():
            name, value = [x.strip() for x in line.split(':', 1)]
            self.assertIn(f'Header always set {name} "{value}"', ht)
        self.assertIn('Options -Indexes', ht)

    def test_published_folder_holds_no_development_files(self):
        bad = [str(p.relative_to(PUB)) for p in PUB.rglob('*') if p.is_file() and re.search(r'\.(py|md|map|log|bak|orig|sql|env|sh|zip|gz|tar)$|~$', p.name)]
        self.assertEqual(bad, [])


PORTRAIT = '/portal-assets/speaker/mufti-maqsood-imran-rashadi.jpg'


def apache_sends_noimageindex(uri):
    """Models the root .htaccess rules (SetEnvIf on the request path, then FilesMatch on the file name with env=!scholar_portrait).
    It is a check of the configuration text, not of a running Apache."""
    ht = (PUB / '.htaccess').read_text(encoding='utf-8')
    env = re.search(r'SetEnvIf Request_URI "([^"]+)" scholar_portrait', ht)
    rule = re.search(r'<FilesMatch "([^"]+)">\s*Header set X-Robots-Tag "noimageindex" env=!scholar_portrait\s*</FilesMatch>', ht)
    assert env and rule, 'the noimageindex rules in .htaccess have an unexpected shape'
    exempt = bool(re.search(env.group(1), uri))
    return bool(re.search(rule.group(1), uri.rsplit('/', 1)[-1])) and not exempt


def static_host_sends_noimageindex(uri):
    """The _headers rules that set X-Robots-Tag, matched the way Netlify and Cloudflare Pages match a trailing *."""
    text = (PUB / '_headers').read_text(encoding='utf-8')
    for path, block in re.findall(r'^(/\S*)\n((?:[ \t]+.+\n)+)', text, re.M):
        if 'X-Robots-Tag: noimageindex' in block and (uri == path or (path.endswith('*') and uri.startswith(path[:-1]))):
            return True
    return False


class PortraitImageIndexing(unittest.TestCase):
    def test_the_official_portrait_exists_and_is_the_picture_the_profile_page_uses(self):
        self.assertTrue((PUB / PORTRAIT.lstrip('/')).is_file())
        profile = (PUB / 'MuftiMaqsoodImran.html').read_text(encoding='utf-8')
        self.assertIn(f'<meta property="og:image" content="https://jameululoom.org{PORTRAIT}">', profile)
        self.assertIn(f'src="{PORTRAIT.lstrip("/")}"', profile)

    def test_apache_lets_the_portrait_be_indexed_and_nothing_else_in_the_speaker_folder(self):
        self.assertFalse(apache_sends_noimageindex(PORTRAIT))
        for uri in ('/portal-assets/speaker/slides/portrait-white-turban.jpg', '/portal-assets/speaker/slides/speaking-at-microphone.png',
                    '/portal-assets/speaker/other/mufti-maqsood-imran-rashadi.jpg', '/portal-assets/speaker/Mufti-Maqsood-Imran-Rashadi.jpg'):
            self.assertTrue(apache_sends_noimageindex(uri), uri)

    def test_apache_still_protects_pupil_and_staff_photographs(self):
        for uri in ('/portal-assets/images/schools/head-mistress.jpg', '/portal-assets/images/colleges/staff-pu.jpeg', '/portal-assets/images/events/activity-2.jpg',
                    '/portal-assets/recognitions/rec-01-k-rahman-khan.jpg', '/portal-assets/masjid/main-hall-a.jpg', '/portal-assets/hero/hero-assembly.jpg',
                    '/ResidentialSchoolBanikuppa/assets/images/staff.jpg'):
            self.assertTrue(apache_sends_noimageindex(uri), uri)
        rs = (PUB / 'ResidentialSchoolBanikuppa' / '.htaccess').read_text(encoding='utf-8')
        self.assertIn('Header set X-Robots-Tag "noimageindex"', rs)   # the Residential School folder keeps its own, unchanged rule
        self.assertNotIn('env=', rs)

    def test_static_hosts_protect_the_photograph_folder_and_never_the_portrait(self):
        self.assertFalse(static_host_sends_noimageindex(PORTRAIT))
        self.assertTrue(static_host_sends_noimageindex('/portal-assets/images/schools/head-mistress.jpg'))

    def test_no_configuration_sets_noindex_for_the_portrait_or_for_pages(self):
        for name in ('.htaccess', '_headers', 'ResidentialSchoolBanikuppa/.htaccess'):
            text = (PUB / name).read_text(encoding='utf-8')
            self.assertNotRegex(text, r'(?i)x-robots-tag[^\n]*\b(noindex|none|noimageindex,\s*noindex)\b')


if __name__ == '__main__':
    unittest.main()
