"""Checks the generated security headers (public/_headers and public/.htaccess).

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


if __name__ == '__main__':
    unittest.main()
