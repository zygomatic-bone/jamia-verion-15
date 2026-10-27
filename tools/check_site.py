"""Link and asset checker for the site (public/). Run before publishing:  python3 tools/check_site.py

Checks every local href/src in every HTML file:
  - the target file exists (case-sensitively, like a real web server),
  - a #fragment points at an existing id,
  - nothing links to the removed root portal page (public/home.html),
  - public/home.html itself does not exist.
Routing and publishing checks:
  - every legacy redirect in _redirects (and the matching public/.htaccess rule) points at an existing page and, where it
    has one, an existing #id; no redirect chains or loops, and no redirect source is also a real file,
  - nothing that must never be published is in public/ (design sources, thumbnail databases, server config backups, archives, keys),
  - no inline <script> body and no style="" attribute (the site's Content-Security-Policy forbids both),
  - every <img> has an alt attribute.
Exit code 0 = all good, 1 = problems found (each one is printed).
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

PUB = Path(__file__).resolve().parent.parent / 'public'
EXTERNAL = ('http:', 'https:', 'mailto:', 'tel:', 'data:', 'javascript:', '//')


class Collector(HTMLParser):
    """Collects link targets and element ids from one HTML file."""
    def __init__(self):
        super().__init__()
        self.refs, self.ids = [], set()
        self.inline_script = self.inline_style = self.img_no_alt = 0
        self._in_script = False

    def handle_data(self, data):
        if self._in_script and data.strip(): self.inline_script += 1

    def handle_endtag(self, tag):
        if tag == 'script': self._in_script = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'): self.ids.add(a['id'])
        if tag == 'script' and 'src' not in a and a.get('type') != 'application/ld+json': self._in_script = True
        if a.get('style') is not None: self.inline_style += 1
        if tag == 'img' and 'alt' not in a: self.img_no_alt += 1
        for key in ('href', 'src'):
            if a.get(key): self.refs.append((tag, key, a[key]))
        for item in (a.get('srcset') or '').split(','):
            if item.strip(): self.refs.append((tag, 'srcset', item.strip().split()[0]))


def exists_exact(path):
    """True if the file exists with exactly this capitalisation (Linux web servers are case-sensitive)."""
    if not path.exists(): return False
    cur = PUB
    for part in path.relative_to(PUB).parts:
        if part not in {p.name for p in cur.iterdir()}: return False
        cur = cur / part
    return True


FORBIDDEN = re.compile(r'(^|/)(cgi-bin|\.well-known)(/|$)|\.(psd|uga|db|sql|pem|key|tar|tgz|gz|zip|bak|orig)$|(^|/)(thumbs\.db|\.env|error_log|\.ftpquota|id_rsa)$|\.php[0-9]?$', re.I)   # the site is static: a .php file in public/ is always a mistake


def routing_checks(pages):
    out = []
    # redirects
    rules = {}
    for line in (PUB / '_redirects').read_text(encoding='utf-8').splitlines():
        t = line.split()
        if len(t) >= 3 and t[0].startswith('/') and not line.lstrip().startswith('#'): rules[t[0]] = t[1]
    for src, dst in rules.items():
        if src in ('/home', '/home/', '/home.html'):
            if dst != '/': out.append(f'redirect {src} must go to /')
            continue
        d = urlsplit(dst)
        tgt = PUB / unquote(d.path.lstrip('/'))
        if tgt.is_dir(): tgt = tgt / 'index.html'
        if not exists_exact(tgt): out.append(f'redirect {src} -> {dst}: target missing'); continue
        if d.fragment and tgt in pages and d.fragment not in pages[tgt].ids: out.append(f'redirect {src} -> {dst}: id not found')
        if d.path in rules: out.append(f'redirect {src} -> {dst}: target is itself redirected (chain)')
        if exists_exact(PUB / unquote(src.lstrip('/'))) and src.endswith('.html'): out.append(f'redirect {src}: a real file exists at the source')
    ht = PUB / '.htaccess'
    if ht.exists():
        n = len(re.findall(r'^RewriteRule \^(?!home)', ht.read_text(encoding='utf-8'), re.M))
        if n < len([s for s in rules if s not in ('/home', '/home/', '/home.html')]) - 60:
            out.append(f'public/.htaccess has only {n} rewrite rules; it should mirror _redirects')
    # forbidden files
    for f in PUB.rglob('*'):
        if f.is_file() and FORBIDDEN.search(str(f.relative_to(PUB)).replace('\\', '/')): out.append(f'forbidden file published: {f.relative_to(PUB)}')
    # CSP and accessibility
    for f, c in pages.items():
        rel = f.relative_to(PUB)
        if c.inline_script: out.append(f'{rel}: inline <script> body (CSP)')
        if c.inline_style: out.append(f'{rel}: {c.inline_style} style="" attribute(s) (CSP)')
        if c.img_no_alt: out.append(f'{rel}: {c.img_no_alt} <img> without alt')
    return out


def main():
    problems, pages, links = [], {}, 0
    for f in sorted(PUB.rglob('*.html')):
        c = Collector(); c.feed(f.read_text(encoding='utf-8')); pages[f] = c
    if (PUB / 'home.html').exists():
        problems.append('public/home.html exists: the removed portal page must not return')

    # The Bayanath page shows no cards when this cache is empty. Catch that
    # state before publishing, and ensure every thumbnail is a genuine YouTube URL derived from its video id.
    bayanath_cache = PUB / 'data' / 'bayanath-videos.json'
    try:
        bayanath = json.loads(bayanath_cache.read_text(encoding='utf-8'))
        videos = bayanath.get('videos', [])
        if not videos:
            problems.append('data/bayanath-videos.json has no videos; Bayanath would render no cards')
        if len(videos) > 10:
            problems.append('data/bayanath-videos.json has more than the configured 10 videos')
        for i, video in enumerate(videos, 1):
            vid, thumb = video.get('id', ''), video.get('thumbnail', '')
            if not re.fullmatch(r'[A-Za-z0-9_-]{11}', vid):
                problems.append(f'data/bayanath-videos.json video {i} has an invalid YouTube id')
            if not video.get('title'):
                problems.append(f'data/bayanath-videos.json video {i} has no title')
            if not re.fullmatch(rf'https://(?:i\d?\.ytimg\.com|img\.youtube\.com)/vi/{re.escape(vid)}/[^?#]+(?:[?#].*)?', thumb):
                problems.append(f'data/bayanath-videos.json video {i} thumbnail is not derived from its video id')
    except (OSError, ValueError, TypeError) as exc:
        problems.append(f'data/bayanath-videos.json is missing or invalid: {exc}')
    for f, c in pages.items():
        rel = f.relative_to(PUB)
        for tag, key, ref in c.refs:
            if ref.startswith(EXTERNAL) or ref.startswith('#') and len(ref) == 1: continue
            links += 1
            u = urlsplit(ref)
            target = f if not u.path else (PUB / unquote(u.path.lstrip('/')) if u.path.startswith('/') else (f.parent / unquote(u.path)).resolve())
            if u.path == '' and u.fragment:
                if u.fragment not in c.ids: problems.append(f'{rel}: #{u.fragment} not found on this page')
                continue
            try: target.relative_to(PUB)
            except ValueError: problems.append(f'{rel}: {ref} points outside public/'); continue
            if target.is_dir(): target = target / 'index.html'
            if not exists_exact(target):
                problems.append(f'{rel}: <{tag} {key}="{ref}"> target missing'); continue
            if target == PUB / 'home.html': problems.append(f'{rel}: links to the removed root home.html')
            if u.fragment and target in pages and u.fragment not in pages[target].ids:
                problems.append(f'{rel}: {ref} -> id "{u.fragment}" not found in {target.relative_to(PUB)}')
    problems += routing_checks(pages)
    print(f'Checked {len(pages)} HTML files, {links} local references.')
    for p in problems: print('PROBLEM:', p)
    print('OK: no broken links or assets.' if not problems else f'{len(problems)} problem(s) found.')
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
