"""HTML helpers for the Phase 9 recovered content (images, scans, documents, audio, tables, notes).

Everything returns an HTML string. `rp` is the path from the page to the site root ('' for root pages, '../' for pages one
folder down), exactly as in generate_portal.py. Images are always shown whole (never cropped) at their own proportions.
Dimensions are read from the files so the browser can reserve space (no layout shift).
"""
from html import escape
from pathlib import Path

from imgutil import image_size
import recovery_assets as RA

PUB = Path(__file__).resolve().parent.parent / 'public'


def _src(rp, key):
    """(public-relative path, alt, caption) for a recovered image key, or for an existing Phase 8 photograph."""
    if key in RA.IMAGES:
        _, dest, alt, cap = RA.IMAGES[key]
        return RA.R + dest, alt, cap
    if key in RA.EXISTING:
        return RA.EXISTING[key]
    raise KeyError(key)


def esc(s):
    return escape(s, quote=True)


def img_tag(rp, key, alt=None, loading='lazy'):
    rel, a, _ = _src(rp, key)
    w, h = image_size(PUB / rel)
    return f'<img src="{rp}{esc(rel)}" alt="{esc(alt if alt is not None else a)}" width="{w}" height="{h}" loading="{loading}" decoding="async">'


def fig(rp, key, caption=None, alt=None, detail=None, link=True, loading='lazy'):
    """One captioned photograph. The picture opens the full-size file in a new tab."""
    rel, a, cap = _src(rp, key)
    cap = cap if caption is None else caption
    tag = img_tag(rp, key, alt, loading)
    if link:
        tag = f'<a href="{rp}{esc(rel)}" target="_blank" rel="noopener" aria-label="Open the full-size photograph: {esc(cap or a)}">{tag}</a>'
    inner = ''
    if cap: inner += f'<strong>{escape(cap)}</strong>'
    if detail: inner += escape(detail)
    return f'<figure class="rc-fig">{tag}' + (f'<figcaption>{inner}</figcaption>' if inner else '') + '</figure>'


def gallery(rp, keys, cls='', captions=None):
    """Responsive grid of whole photographs. keys: list of image keys; captions: optional {key: caption}."""
    captions = captions or {}
    items = ''.join(f'<li>{fig(rp, k, caption=captions.get(k))}</li>' for k in keys)
    return f'<ul class="rc-gallery {cls}">{items}</ul>'


def single(rp, key, big=False, caption=None, detail=None, extra_cls=''):
    cls = 'rc-single' + (' rc-big' if big else '') + (f' {extra_cls}' if extra_cls else '')
    return f'<div class="{cls}">{fig(rp, key, caption=caption, detail=detail)}</div>'


def logo(rp, key):
    """Institution logo banner (original Institutions/*Logo.jpg)."""
    rel, a, cap = _src(rp, key)
    w, h = image_size(PUB / rel)
    return f'<div class="rc-logo"><img src="{rp}{esc(rel)}" alt="{esc(a)}" width="{w}" height="{h}" decoding="async"></div>'


def scan(rp, key, caption=None):
    """A tall scanned page: whole, with a link to the full-size file."""
    rel, a, cap = _src(rp, key)
    cap = cap if caption is None else caption
    return (f'<figure class="rc-scan"><a href="{rp}{esc(rel)}" target="_blank" rel="noopener" aria-label="Open the full-size scan: {esc(cap)}">{img_tag(rp, key)}</a>'
            f'<figcaption>{escape(cap)} · <a href="{rp}{esc(rel)}" target="_blank" rel="noopener">Open full size ↗</a></figcaption></figure>')


def split(text_html, media_html, flip=False):
    """Text column next to a photograph (stacks on phones)."""
    return f'<div class="rc-split{" rc-flip" if flip else ""}"><div class="rc-text">{text_html}</div>{media_html}</div>'


def p(*paras):
    return ''.join(f'<p>{x}</p>' for x in paras)


def quote(*paras, sign=None, role=None):
    """Verbatim text typed from an original page or letter."""
    body = ''.join(f'<p>{x}</p>' for x in paras)
    s = ''
    if sign:
        s = f'<p class="rc-sign">{sign}' + (f'<small>{role}</small>' if role else '') + '</p>'
    return f'<div class="rc-text"><blockquote>{body}{s}</blockquote></div>'


def dated(text):
    return f'<p class="rc-dated">{text}</p>'


def note(text):
    return f'<p class="rc-note">{text}</p>'


def sources(text):
    return f'<p class="rc-sources">{text}</p>'


def table(headers, rows, caption=None, cls=''):
    """Responsive table: on a phone each row becomes labelled lines (data-label)."""
    th = ''.join(f'<th scope="col">{h}</th>' for h in headers)
    body = ''.join('<tr>' + ''.join(f'<td data-label="{esc(headers[i]) if i < len(headers) else ""}">{c}</td>' for i, c in enumerate(r)) + '</tr>' for r in rows)
    cap = f'<caption>{caption}</caption>' if caption else ''
    return f'<div class="rc-table-wrap"><table class="rc-table {cls}">{cap}<thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'


def people(items):
    """items: [(name, role)]"""
    return '<ul class="rc-people">' + ''.join(f'<li><strong>{n}</strong><span>{r}</span></li>' for n, r in items) + '</ul>'


def vision(items):
    return '<ol class="rc-vision">' + ''.join(f'<li><span>{i}</span></li>' for i in items) + '</ol>'


def doc_card(rp, key, extra=None):
    """PDF card with size and a link; the file is the unchanged original."""
    _, dest, title, desc = RA.DOCUMENTS[key]
    size = (PUB / RA.DOC / dest).stat().st_size / 1_048_576
    href = f'{rp}{RA.DOC}{dest}'
    more = f'<p>{extra}</p>' if extra else ''
    return (f'<li class="rc-doc"><p class="rc-meta">PDF · {size:.1f} MB</p><h3>{escape(title)}</h3><p>{escape(desc)}</p>{more}'
            f'<div class="button-row"><a class="button" href="{href}" target="_blank" rel="noopener">Open PDF</a>'
            f'<a class="button button-quiet" href="{href}" download>Download</a></div></li>')


def doc_list(rp, keys):
    return '<ul class="rc-docs">' + ''.join(doc_card(rp, k) for k in keys) + '</ul>'



def phone(n):
    return f'<a href="tel:{n}">{n}</a>'
