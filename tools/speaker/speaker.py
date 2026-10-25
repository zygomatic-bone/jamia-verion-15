"""Renders the Bayanath page's Speaker Profile (real HTML, no screenshot) from tools/speaker/speaker-profile.json.

The profile data is kept apart from the automatic video feed. Entries with "publish": false are skipped, so a
designation that the Trust does not confirm can be withdrawn by editing one flag and rebuilding.
The "verification" and "check" fields are for the maintainers (see JAMIA_PHASE9_2_SPEAKER_VERIFICATION in the reports);
they are never printed on the page.
"""
import json
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / 'speaker-profile.json'
PHOTO_DIR = HERE / 'photo'
PATTERN = HERE / 'pattern.svg'
ASSET_DIR = 'portal-assets/speaker/'

ICONS = {
    'mosque': 'M4 21V11M20 21V11M4 11c0-5 8-8 8-8s8 3 8 8M9 21v-4a3 3 0 0 1 6 0v4M12 3V1.5M2.5 21h19',
    'college': 'M2 9l10-5 10 5-10 5-10-5ZM6 11.5V16c0 1.5 3 3 6 3s6-1.5 6-3v-4.5M22 9v6',
    'council': 'M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6l8-3ZM9 12l2 2 4-4',
    'moon': 'M20 14.5A8.5 8.5 0 1 1 9.5 4a7 7 0 0 0 10.5 10.5ZM17 3v3M15.5 4.5h3',
    'book': 'M4 5.5C6.5 4.5 9.5 4.5 12 6c2.5-1.5 5.5-1.5 8-.5V19c-2.5-1-5.5-1-8 .5-2.5-1.5-5.5-1.5-8-.5ZM12 6v13.5',
    'star': 'M12 3.5l2.6 5.4 5.9.8-4.3 4.1 1 5.8L12 16.8l-5.2 2.8 1-5.8-4.3-4.1 5.9-.8Z',
    'quran': 'M5 3h11a3 3 0 0 1 3 3v15H8a3 3 0 0 1-3-3ZM5 18a3 3 0 0 1 3-3h11M12 6.5l1 1.8 2 .3-1.5 1.4.4 2-1.9-1-1.9 1 .4-2-1.5-1.4 2-.3Z',
    'scales': 'M12 3v18M7 21h10M5 7h14M5 7l-3 7a3.5 3.5 0 0 0 6 0L5 7ZM19 7l-3 7a3.5 3.5 0 0 0 6 0l-3-7Z',
    'cap': 'M2 9l10-5 10 5-10 5-10-5ZM6 11.5V16c0 1.5 3 3 6 3s6-1.5 6-3v-4.5M22 9v6',
    'mic': 'M12 3a3 3 0 0 0-3 3v6a3 3 0 0 0 6 0V6a3 3 0 0 0-3-3ZM6 11a6 6 0 0 0 12 0M12 17v4M9 21h6',
    'people': 'M9 8a3 3 0 1 0 0-.01M3.5 19c0-3 2.5-5 5.5-5s5.5 2 5.5 5M17 9a2.2 2.2 0 1 0 0-.01M16 14.2c2.7 0 4.5 1.7 4.5 4.3',
    'dialogue': 'M4 5h10a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2H9l-4 3v-3H4a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2ZM18 9h2a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2v3l-3.5-3H12',
    'sprout': 'M12 21v-9M12 12c0-4-3-6-7-6 0 4 3 6 7 6ZM12 15c0-3.5 2.5-5.5 7-5.5 0 3.5-2.5 5.5-7 5.5Z',
}


def icon(name, cls='sp-ico'):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="{ICONS[name]}"></path></svg>'


def load():
    return json.loads(DATA.read_text(encoding='utf-8'))


def photo_size():
    from imgutil import image_size
    return image_size(PHOTO_DIR / load()['photo']['file'])


def render(rp=''):
    d = load()
    w, h = photo_size()
    src = f'{rp}{ASSET_DIR}{d["photo"]["file"]}'
    cards = []
    for x in (x for x in d['designations'] if x.get('publish', True)):
        place = f'<p class="sp-place">{escape(x["place"])}</p>' if x.get('place') else ''
        cards.append(
            f'<li class="sp-d"><div class="sp-d-top"><span class="sp-num" aria-label="Designation {x["n"]}">{x["n"]}</span>{icon(x["icon"])}</div>'
            f'<h3>{escape(x["title"])}</h3>{place}<p>{escape(x["text"])}</p></li>')
    pills = ''.join(f'<li class="sp-pill" tabindex="0">{icon(a["icon"], "sp-ico sp-ico-sm")}<span>{escape(a["label"])}</span></li>' for a in d['areas'])
    return (
        f'<section class="sp" aria-labelledby="sp-name">'
        f'<div class="sp-bg" aria-hidden="true"><span class="sp-orb sp-orb-a"></span><span class="sp-orb sp-orb-b"></span><span class="sp-orb sp-orb-c"></span>'
        f'<span class="sp-pattern"><span></span></span><span class="sp-shine"></span></div>'
        f'<div class="sp-card">'
        f'<div class="sp-photo"><img class="sp-photo-fill" src="{src}" alt="" width="{w}" height="{h}" loading="lazy" decoding="async" aria-hidden="true">'
        f'<figure class="sp-frame"><img src="{src}" alt="{escape(d["photo"]["alt"], quote=True)}" width="{w}" height="{h}" loading="lazy" decoding="async"></figure></div>'
        f'<div class="sp-main"><p class="sp-eyebrow">{escape(d["eyebrow"])}</p><h2 id="sp-name">{escape(d["name"])}</h2>'
        f'<ol class="sp-desig" aria-label="Designations">{"".join(cards)}</ol></div>'
        f'<div class="sp-areas"><hr class="sp-divider"><h3 id="sp-areas-title">{escape(d["areas_title"])}</h3>'
        f'<ul class="sp-pills" aria-labelledby="sp-areas-title">{pills}</ul></div>'
        f'</div></section>')
