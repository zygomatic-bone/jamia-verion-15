#!/usr/bin/env python3
"""Phase 9 audit: compares the ORIGINAL server backup (public_html) with the built site (public/).

Usage: python3 tools/phase9_audit.py <original public_html> [out_dir]
Writes <out_dir>/audit.json (everything the reports are built from). Read-only on both trees.
Matching rules for pictures: identical SHA-256 (byte-identical copy) first; else a 16x16 difference hash
(re-encoded copies, e.g. CMYK->RGB or optimised); else unmatched (reported, never silently dropped).
"""
import hashlib, json, os, re, sys
from pathlib import Path
from PIL import Image

ORIG = Path(sys.argv[1]); OUT = Path(sys.argv[2] if len(sys.argv) > 2 else '.')
PUB = Path(__file__).resolve().parent.parent / 'public'
IMGX = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
SKIP_ORIG = ('cgi-bin', '.well-known')


def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def dhash(p, n=16):
    try:
        im = Image.open(p)
        im.seek(0)
        im = im.convert('L').resize((n + 1, n), Image.LANCZOS)
    except Exception:
        return None
    px = list(im.getdata()); bits = 0
    for r in range(n):
        for c in range(n):
            bits = (bits << 1) | (px[r * (n + 1) + c] > px[r * (n + 1) + c + 1])
    return bits


def walk(root, skip=()):
    for r, d, fs in os.walk(root, followlinks=True):
        d[:] = [x for x in d if x not in skip]
        for f in fs:
            p = Path(r) / f
            yield p, str(p.relative_to(root)).replace(os.sep, '/')


def size(p):
    try:
        with Image.open(p) as im: return im.size
    except Exception: return (0, 0)


# ---- public inventory
pub = {rel: p for p, rel in walk(PUB)}
pub_sha = {}; pub_dh = {}
for rel, p in pub.items():
    pub_sha.setdefault(sha(p), []).append(rel)
    if Path(rel).suffix.lower() in IMGX:
        h = dhash(p)
        if h is not None: pub_dh.setdefault(h, []).append(rel)

# ---- redirects (from _redirects)
redir = {}
for line in (PUB / '_redirects').read_text().splitlines():
    t = line.split()
    if len(t) >= 3 and t[0].startswith('/') and not line.startswith('#'):
        redir[t[0].lstrip('/')] = t[1]

# ---- html references inside public (to find orphan images)
refd = set()
for rel, p in pub.items():
    if rel.endswith(('.html', '.css', '.js', '.xml', '.webmanifest')):
        txt = p.read_text(errors='ignore')
        base = Path(rel).parent
        for m in re.finditer(r'''(?:src|href|content|srcset|poster|url)\s*[=(]\s*["']?([^"')\s>]+\.(?:jpe?g|png|gif|webp|svg|pdf|mp3|ico))''', txt, re.I):
            u = m.group(1).split('?')[0].split('#')[0]
            if u.startswith(('http', '//', 'data:')): continue
            q = os.path.normpath((PUB / base / u) if not u.startswith('/') else (PUB / u.lstrip('/')))
            refd.add(os.path.relpath(q, PUB).replace(os.sep, '/'))
orphans = sorted(r for r in pub if Path(r).suffix.lower() in IMGX | {'.pdf', '.mp3'} and r not in refd)

# ---- original pages
pages = []
for p, rel in sorted(walk(ORIG, SKIP_ORIG)):
    if not rel.endswith('.html'): continue
    if rel in pub: st, dest = 'rebuilt at same URL', rel
    elif rel in redir: st, dest = '301 redirect', redir[rel]
    elif rel == 'home.html': st, dest = 'removed by design (homepage is /)', '/'
    else: st, dest = 'UNMAPPED', ''
    pages.append(dict(orig=rel, status=st, dest=dest))

# ---- original assets
assets = []
for p, rel in sorted(walk(ORIG, SKIP_ORIG)):
    ext = Path(rel).suffix.lower()
    if rel.endswith('.html'): continue
    s = sha(p); w, h = size(p) if ext in IMGX else (0, 0)
    rec = dict(orig=rel, ext=ext, sha=s[:12], bytes=p.stat().st_size, w=w, h=h, status='', dest='', note='')
    if s in pub_sha:
        rec.update(status='byte-identical copy', dest=';'.join(sorted(pub_sha[s])[:3]))
    elif ext in IMGX and (dh := dhash(p)) is not None:
        best = None
        for k, v in pub_dh.items():
            d = bin(k ^ dh).count('1')
            if best is None or d < best[0]: best = (d, v)
        cand = []
        for k, v in pub_dh.items():
            d = bin(k ^ dh).count('1')
            if d <= 10:
                for rel in v:
                    ow, oh = size(pub[rel])
                    if w and h and ow and oh and abs((ow / oh) / (w / h) - 1) <= 0.05: cand.append((d, rel, ow, oh))
        cand.sort()
        if cand and cand[0][0] <= 6 and cand[0][2] * cand[0][3] >= 0.8 * w * h:
            d, rel, ow, oh = cand[0]
            rec.update(status='re-encoded copy', dest=rel, note=f'same picture re-encoded or resized; dhash distance {d}/256; {w}x{h} -> {ow}x{oh}')
        elif cand:
            d, rel, ow, oh = cand[0]
            rec.update(status='near-duplicate (other size)', dest=rel, note=f'same aspect ratio, dhash distance {d}/256; {w}x{h} vs {ow}x{oh}')
        else:
            rec.update(status='not in public', note=f'nearest dhash distance {best[0] if best else "n/a"}')
    else:
        rec.update(status='not in public')
    assets.append(rec)

# original duplicates (same sha under several paths)
by = {}
for a in assets: by.setdefault(a['sha'], []).append(a['orig'])
for a in assets: a['dups'] = len(by[a['sha']])

dup_public = {k[:12]: v for k, v in pub_sha.items() if len(v) > 1 and Path(v[0]).suffix.lower() in IMGX | {'.pdf', '.mp3'}}
bad = [r for r in pub if re.search(r'(cgi-bin|\.psd$|\.uga$|thumbs\.db$|\.env$|\.sql$|\.pem$|id_rsa|passwd|\.ftpquota|error_log|\.tar|\.zip$)', r, re.I)]
json.dump(dict(pages=pages, assets=assets, orphans=orphans, dup_public=dup_public, forbidden=bad,
               pub_files=len(pub), redirects=len(redir)), open(OUT / 'audit.json', 'w'), indent=1)
from collections import Counter
print('pages', Counter(x['status'] for x in pages))
print('assets', Counter((x['ext'] in IMGX and 'img') or x['ext'] for x in assets), Counter(x['status'] for x in assets))
print('orphans in public', len(orphans), 'dup groups in public', len(dup_public), 'forbidden', bad)
