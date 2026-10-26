"""Renders the three pieces of the Bayanath page that sit around the Speaker Profile (speaker.py, speaker-profile.json):

    channel()    the "On the official channel" card (main column, under the slideshow)
    social()     the "Official Social Media Links" card that opens the Linktree page (sidebar, last)
    slideshow()  the full-width Photo Slideshow (main column, directly under the whole video grid)

All text, links and photographs come from speaker-card.json and tools/speaker/slides/. This module only writes markup; the look is in
tools/portal-ui/bayanath.css and slideshow.css, the behaviour in slideshow.js. Nothing is hidden without JavaScript: the photographs
become a swipeable row, every link is a plain anchor and the "Explore All Channels" panel is a native <details>."""
import json
from html import escape
from pathlib import Path

import speaker

HERE = Path(__file__).resolve().parent
DATA = HERE / 'speaker-card.json'
SLIDE_DIR = HERE / 'slides'
ASSET_DIR = 'portal-assets/speaker/slides/'

# Plain, generic glyphs (not the brands' logos); every one sits beside its text label or inside a link that is named in words.
GLYPHS = {
    'youtube': 'M3 7.5A2.5 2.5 0 0 1 5.5 5h13A2.5 2.5 0 0 1 21 7.5v9a2.5 2.5 0 0 1-2.5 2.5h-13A2.5 2.5 0 0 1 3 16.5ZM10 9.2v5.6L15 12Z',
    'linktree': 'M12 3v18M12 8 6 4M12 8l6-4M12 13 5 9M12 13l7-4M12 18l-4-2M12 18l4-2',
    'facebook': 'M9 8a3 3 0 1 0 0-.01M3.5 19c0-3 2.5-5 5.5-5s5.5 2 5.5 5M17 9a2.2 2.2 0 1 0 0-.01M16 14.2c2.7 0 4.5 1.7 4.5 4.3',
    'instagram': 'M7 4h10a3 3 0 0 1 3 3v10a3 3 0 0 1-3 3H7a3 3 0 0 1-3-3V7a3 3 0 0 1 3-3ZM12 8.5a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7ZM16.8 7.2v.01',
    'x': 'M5 5l14 14M19 5 5 19',
    'threads': 'M16.5 12a4.5 4.5 0 1 0-1.7 3.5c1-.9 1.7-2.2 1.7-3.8V11a4.5 4.5 0 1 0-1.4 3.2',
    'whatsapp': 'M4 20l1.2-4A8 8 0 1 1 8 18.8ZM9.5 9c.5 2.5 2.5 4.5 5 5',
    'play': 'M8 5.5v13l11-6.5Z',
    'pause': 'M8 5v14M16 5v14',
    'prev': 'M15 5l-7 7 7 7',
    'next': 'M9 5l7 7-7 7',
    'arrow': 'M7 17 17 7M9 7h8v8',
    'chevron': 'M9 5l7 7-7 7',
    'plus': 'M12 5v14M5 12h14',
}

REQUIRED_SLIDE_KEYS = ('file', 'alt', 'source', 'rights')


def glyph(name, cls='sc-ico'):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="{GLYPHS[name]}"></path></svg>'


def load():
    d = json.loads(DATA.read_text(encoding='utf-8'))
    # A photograph is only published with a description, a source and the permission to use it. This is the gate that keeps unverified
    # or unlicensed pictures out of the site; a missing file or field stops the build with a plain message.
    for i, s in enumerate(d['slides'], 1):
        for k in REQUIRED_SLIDE_KEYS:
            if not str(s.get(k, '')).strip():
                raise SystemExit(f'speaker-card.json: slide {i} has no "{k}". Every photograph needs a description, a source and its rights.')
        if not (SLIDE_DIR / s['file']).is_file():
            raise SystemExit(f'speaker-card.json: slide {i} points at {s["file"]}, which is not in tools/speaker/slides/.')
    return d


def slide_files():
    return [s['file'] for s in load()['slides']]


def _ext_link(href, cls, label, inner):
    return (f'<a class="{cls}" href="{escape(href, quote=True)}" target="_blank" rel="noopener noreferrer" '
            f'aria-label="{escape(label, quote=True)} (opens in a new tab)">{inner}</a>')


def channel():
    """The compact channel card: the channel's own description, what it carries, and the official links."""
    d = load()
    p = d['primary']
    roles = ''.join(f'<li class="sc-role">{speaker.icon(r["icon"], "sc-ico")}<span>{escape(r["text"])}</span></li>' for r in d['roles'])
    tags = ''.join(f'<li class="sc-tag">{speaker.icon(c["icon"], "sc-ico sc-ico-sm")}<span>{escape(c["text"])}</span></li>' for c in d['categories'])
    tiles = ''.join(
        '<li>' + _ext_link(l['url'], f'sc-soc sc-soc-{l["key"]}', l['label'],
                           f'<span class="sc-soc-ic">{glyph(l["key"])}</span>'
                           f'<span class="sc-soc-tx"><b>{escape(l["label"])}</b><small>{escape(l["sub"])}</small></span>{glyph("arrow", "sc-ico sc-ico-go")}') + '</li>'
        for l in d['links'])
    cta = _ext_link(p['url'], 'sc-cta', p['label'],
                    f'<span class="sc-cta-ic">{glyph("youtube")}</span><span class="sc-cta-tx">{escape(p["label"])}</span>{glyph("arrow", "sc-ico sc-ico-go")}')
    return (
        '<section class="sc-card" aria-labelledby="sc-title"><div class="sc-info">'
        f'<p class="sc-eyebrow">{escape(d["eyebrow"])}</p>'
        f'<h2 id="sc-title" class="sr-only">{escape(d["eyebrow"])}: {escape(d["name"])}</h2>'
        f'<ul class="sc-roles" aria-label="Roles">{roles}</ul>'
        f'<p class="sc-intro">{escape(d["intro"])}</p>'
        f'<p class="sc-bio">{escape(d["biography"])}</p>'
        f'<div class="sc-cats"><h3 id="sc-cats-t">{escape(d["categories_title"])}</h3><ul class="sc-tags" aria-labelledby="sc-cats-t">{tags}</ul></div>'
        f'<p class="sc-source">{escape(d["source_note"])}</p></div>'
        f'<div class="sc-links">{cta}'
        f'<details class="sc-more"><summary><span>{escape(d["more_label"])}</span>{glyph("plus", "sc-ico sc-ico-plus")}</summary>'
        f'<ul class="sc-soc-list">{tiles}</ul></details></div>'
        '</section>')


def social():
    """The Official Social Media Links card: one link to the speaker's Linktree page, with a small portrait and generic symbols."""
    d = load()['social_card']
    from imgutil import image_size
    w, h = image_size(SLIDE_DIR / d['portrait'])
    icons = ''.join(f'<span class="so-chip">{glyph(k, "so-ico")}</span>' for k in d['icons'])
    return (
        f'<a class="so-card" href="{escape(d["url"], quote=True)}" target="_blank" rel="noopener noreferrer">'
        f'<img class="so-photo" src="{ASSET_DIR}{d["portrait"]}" alt="" width="{w}" height="{h}" loading="lazy" decoding="async">'
        f'<span class="so-text"><b class="so-title">{escape(d["heading"])}</b>'
        f'<small class="so-sub">{escape(d["text"])}</small>'
        f'<span class="so-icons" aria-hidden="true">{icons}</span></span>'
        f'{glyph("chevron", "so-go")}'
        '<span class="sr-only">(opens the official Linktree page in a new tab)</span></a>')


def _slides(d):
    from imgutil import image_size
    out, dots = [], []
    n = len(d['slides'])
    for i, s in enumerate(d['slides']):
        w, h = image_size(SLIDE_DIR / s['file'])
        src = f'{ASSET_DIR}{s["file"]}'
        first = i == 0
        out.append(
            f'<figure class="ph-slide{" is-active" if first else ""}" role="group" aria-roledescription="slide" aria-label="{i + 1} of {n}">'
            f'<img class="ph-bg" src="{src}" alt="" width="{w}" height="{h}" loading="lazy" decoding="async" aria-hidden="true">'
            f'<img class="ph-img" src="{src}" alt="{escape(s["alt"], quote=True)}" width="{w}" height="{h}" loading="{"eager" if first else "lazy"}" decoding="async">'
            f'<span class="ph-miss">This photograph could not be loaded.</span>'
            f'</figure>')
        # (a backslash inside an f-string expression is a SyntaxError before Python 3.12, so the attribute is built outside it)
        current = ' aria-current="true"' if first else ''
        dots.append(f'<button class="ph-dot{" is-active" if first else ""}" type="button" aria-label="Show photograph {i + 1} of {n}"{current}><i></i></button>')
    return ''.join(out), ''.join(dots)


def slideshow():
    d = load()
    slides, dots = _slides(d)
    return (
        f'<section class="ph" data-slideshow data-interval="{int(d["interval_seconds"])}" data-no-motion aria-labelledby="ph-title">'
        f'<div class="ph-head"><h2 id="ph-title">{escape(d["slideshow_title"])}</h2>'
        f'<div class="ph-arrows" hidden>'
        f'<button class="ph-arrow ph-prev" type="button" aria-label="Previous photograph">{glyph("prev")}</button>'
        f'<button class="ph-arrow ph-next" type="button" aria-label="Next photograph">{glyph("next")}</button></div></div>'
        f'<div class="ph-show" role="group" aria-roledescription="carousel" aria-label="Photographs of {escape(d["name"], quote=True)} and his programmes" tabindex="0">'
        f'<div class="ph-stage">{slides}</div>'
        f'<button class="ph-side ph-side-prev" type="button" tabindex="-1" aria-hidden="true" hidden>{glyph("prev")}</button>'
        f'<button class="ph-side ph-side-next" type="button" tabindex="-1" aria-hidden="true" hidden>{glyph("next")}</button>'
        f'<p class="ph-live" role="status" aria-live="polite"></p></div>'
        f'<div class="ph-bar" hidden><div class="ph-dots" role="group" aria-label="Choose a photograph">{dots}</div>'
        f'<button class="ph-pp" type="button" aria-pressed="false" aria-label="Pause the slideshow">'
        f'<span class="ph-pp-pause">{glyph("pause")}</span><span class="ph-pp-play">{glyph("play")}</span></button></div>'
        '</section>')
