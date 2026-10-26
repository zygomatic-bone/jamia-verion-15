"""Jamia Masjid page: seven photo/video sections built from tools/masjid/photos and tools/masjid/media.

Photographs are the files supplied by the owner (byte for byte); videos are compressed, silent copies of the supplied clips
(see media-info.json). Everything shown about a room is limited to what can be seen in its pictures or what the site already
says about the mosque. Room-to-section assignments are listed in MASJID-MEDIA-MAP.md.
"""
import json, shutil
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
PHOTOS, MEDIA = HERE / 'photos', HERE / 'media'
DEST = 'portal-assets/masjid/'
INFO = json.loads((HERE / 'media-info.json').read_text(encoding='utf-8'))

P = {  # icon paths (24 x 24, stroke)
    'mosque': 'M4 21V11M20 21V11M4 11c0-5 8-8 8-8s8 3 8 8M9 21v-4a3 3 0 0 1 6 0v4M12 3V1.5M2.5 21h19',
    'hall': 'M3 21h18M5 21V9M9 21V9M15 21V9M19 21V9M3 9l9-5 9 5',
    'water': 'M12 3c3 4 5 6.5 5 9.5a5 5 0 0 1-10 0C7 9.5 9 7 12 3ZM4 20c2-1 3-1 5 0s3 1 5 0 3-1 6 0',
    'books': 'M4 4h4v16H4ZM10 4h4v16h-4ZM16.5 5l3.7-1 3 15-3.7 1Z',
    'study': 'M2 9l10-5 10 5-10 5-10-5ZM6 11.5V16c0 1.5 3 3 6 3s6-1.5 6-3v-4.5M22 9v6',
    'class': 'M3 5h18v11H3ZM8 21h8M12 16v5M7 9h6M7 12h10',
    'home': 'M3 11.5 12 4l9 7.5M5.5 10v10h13V10M10 20v-5h4v5',
    'clock': 'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18ZM12 7v5l3 2',
    'doc': 'M6 3h9l4 4v14H6ZM14 3v5h5M9 13h6M9 17h6',
}
def icon(name, cls='mp-ico'):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true"><path d="{P[name]}"></path></svg>'

def _photos(prefix, n, alts):
    return [(f'{prefix}-{i:02d}.jpg' if n > 9 else f'{prefix}-{i}.jpg', alts(i)) for i in range(1, n + 1)]

SECTIONS = [
    dict(id='main-hall', title='Jamia Masjid — Main Hall', icon='mosque',
         facts=['The main prayer hall of Jamia Masjid, in the heart of Bangalore City at City Market. Jame-ul-uloom is housed in the campus of this mosque, one of the biggest in the state.',
                'The hall is carpeted in red, with a gilded mihrab, chandeliers and wooden doors along the side walls.'],
         photos=[(f'main-hall-{i}.jpg', a) for i, a in enumerate([
             'The main prayer hall of Jamia Masjid: a red carpet with white lines, the gilded mihrab on the right and a chandelier overhead',
             'The red-carpeted main hall facing the mihrab, with a large chandelier and wooden doors along the side wall',
             'Wide view of the main hall: red carpet, hanging chandeliers and arched wooden doors along the wall',
             'The main hall seen from the left, with the mihrab and a gilded frame at the far end'], 1)],
         videos=['main-hall-a', 'main-hall-b', 'main-hall-c'], lead=2, vlabel='Main Hall'),
    dict(id='secondary-hall', title='Secondary Hall', icon='hall',
         facts=['A second hall of the mosque with green patterned floor matting, rows of columns and arched wooden doors.'],
         photos=[('secondary-hall-1.jpg', 'The secondary hall with green patterned floor matting, a steel column on the right and red plastic chairs at the side')],
         videos=['secondary-hall-a', 'secondary-hall-b', 'secondary-hall-c'], lead=1, vlabel='Secondary Hall'),
    dict(id='pathway-water-house', title='Pathway and Water House', icon='water',
         facts=['The central pathway of the mosque beneath a high ceiling painted with a blue sky and clouds. A long water channel with fountain jets runs down the middle, between rows of dark seating blocks and columns with gold bands.'],
         photos=[(f'pathway-{i:02d}.jpg', f'The central pathway and water channel beneath the sky-blue ceiling, photograph {n} of 2') for n, i in enumerate((2, 16), 1)],
         videos=['pathway-a', 'pathway-b', 'pathway-c'], lead=2, vlabel='Pathway and Water House'),
    dict(id='advanced-library', title='Advanced Library', icon='books',
         facts=['Reference shelves with books arranged by subject (shelf labels include Engineering Books and Medical Books), reading tables with chairs and computers, and flower arrangements at the shelf ends.'],
         photos=[('adv-library-1.jpg', 'Shelves of books and magazines with flower arrangements, reading tables and black lattice chairs'),
                 ('adv-library-2.jpg', 'The library seen from above: shelves labelled by subject, reading tables with books and desktop computers'),
                 ('adv-library-3.jpg', 'Library shelves of books beside reading tables, with flowers at the end of the shelves'),
                 ('adv-library-4.jpg', 'A wall of bookshelves holding books and magazines, with display shelves and flowers')], videos=[], lead=2),
    dict(id='library', title='Library', icon='books',
         facts=['A library with desks, chairs and open bookshelves, reached through a door with a geometric lattice panel. White arches and a carved lattice window match the rest of the building.'],
         photos=[('study-hall-1.jpg', 'A passage between bookshelves and study desks, seen through an open doorway'),
                 ('study-hall-2.jpg', 'A wood-grain door with a geometric lattice glass panel and a grey floor'),
                 ('study-hall-3.jpg', 'A white room with arches, a long desk, black chairs and a bookshelf'),
                 ('study-hall-4.jpg', 'Study desks with black chairs in a white room with a ceiling fan and arch')], videos=[], lead=2),
    dict(id='large-library', title='Large Library and Classroom Facilities', icon='class',
         facts=['A large hall with long reading desks, black chairs and open wooden shelving, with a carved lattice window and a ceiling fan.'],
         photos=[('large-library-1.jpg', 'A hall with open shelves along the left wall and long desks with black chairs'),
                 ('large-library-2.jpg', 'A long room of open shelves, desks and chairs leading to a door with a lattice panel'),
                 ('large-library-3.jpg', 'Long reading desks and black lattice chairs facing open shelves')], videos=[], lead=2),
    # Added 26 Oct 2026 from two photographs and one video; named by the owner as the study hall of Shoba-e-Hifz.
    dict(id='shoba-e-hifz-study-hall', title='Shoba-e-Hifz Study Hall', icon='study',
         facts=['The study hall of Shoba-e-Hifz: a hall with green pillars, a patterned grey-green carpet and teal curtains, where men and boys in white sit together in rows and small groups, many reading from books.'],
         photos=[('shoba-e-hifz-1.jpg', 'Men in white sitting on a patterned carpet in small groups and reading, in the Shoba-e-Hifz study hall with green pillars and teal curtains along the wall'),
                 ('shoba-e-hifz-2.jpg', 'A wide view of boys and men in white seated on the carpet in rows in the Shoba-e-Hifz study hall, with green pillars, a wall clock and windows behind them')],
         videos=['shoba-e-hifz-a'], lead=2, vlabel='Shoba-e-Hifz Study Hall'),
]

def _img(fn, alt, cls, lazy=True, w=None, h=None):
    from imgutil import image_size
    w, h = image_size(PHOTOS / fn)
    ori = 'is-portrait' if h > w else 'is-landscape'
    return (f'<a class="mp-ph {ori}" href="{DEST}{fn}" aria-label="Open full-size photograph: {escape(alt, quote=True)}">'
            f'<img src="{DEST}{fn}" alt="{escape(alt, quote=True)}" width="{w}" height="{h}" loading="{"lazy" if lazy else "eager"}" decoding="async"></a>')

def _video(name, label, n):
    d = INFO[name]; ori = 'is-portrait' if d['h'] > d['w'] else 'is-landscape'
    sec = d['seconds']
    return (f'<figure class="mp-vid {ori}"><video muted loop playsinline preload="none" controls data-poster="{DEST}{name}.jpg" width="{d["w"]}" height="{d["h"]}" '
            f'data-autoplay aria-label="{escape(label)} walkthrough video {n}, {int(sec)} seconds, no sound">'
            f'<source src="{DEST}{name}.mp4" type="video/mp4"></video>'
            f'<figcaption>{escape(label)} · video {n}</figcaption></figure>')

def sections():
    out = []
    for s in SECTIONS:
        photos = dict(s['photos'])
        names = [f for f, _ in s['photos']]
        lead = names[:s['lead']]; rest = names[s['lead']:]
        ph = lambda fns, lazy=True: ''.join(_img(f, photos[f], '', lazy) for f in fns)
        # only the very first picture of the page loads at once; everything else waits until it is near the screen
        first = s['id'] == 'main-hall'
        body = '<div class="mp-lead">' + ''.join(_img(f, photos[f], '', lazy=not (first and i == 0)) for i, f in enumerate(lead)) + '</div>'
        body += (f'<header class="mp-head"><span class="mp-badge">{icon(s["icon"])}</span><div><h2 id="{s["id"]}-h">{escape(s["title"])}</h2>'
                 + ''.join(f'<p>{escape(t)}</p>' for t in s['facts']) + '</div></header>')
        if s['videos']:
            body += '<div class="mp-videos">' + ''.join(_video(v, s['vlabel'], i) for i, v in enumerate(s['videos'], 1)) + '</div>'
        if rest:
            n = len(rest)
            if len(names) > 8:
                shown, more = rest[:5], rest[5:]
                body += f'<div class="mp-gallery">{ph(shown)}</div>'
                body += (f'<details class="mp-more"><summary>Show all {len(names)} photographs</summary><div class="mp-gallery">{ph(more)}</div></details>')
            else:
                body += f'<div class="mp-gallery">{ph(rest)}</div>'
        out.append(f'<section class="mp-sec" id="{s["id"]}" aria-labelledby="{s["id"]}-h">{body}</section>')
    return ''.join(out)

def topbar():
    chips = [('prayer-times', 'Prayer times', 'clock')] + [(s['id'], s['title'].replace('Jamia Masjid — ', ''), s['icon']) for s in SECTIONS] + [('documents', 'Historical documents', 'doc')]
    return ('<div class="mp-top"><a class="mp-home" href="index.html" aria-label="Back to the Jame-ul-Uloom homepage">' + icon('home') + '<span>Home</span></a>'
            '<nav class="mp-chips" aria-label="Jamia Masjid sections">' + ''.join(f'<a href="#{i}">{icon(ic, "mp-ico mp-ico-sm")}<span>{escape(t)}</span></a>' for i, t, ic in chips) + '</nav></div>')

def copy_assets(assets):
    d = assets / 'masjid'; d.mkdir(exist_ok=True)
    keep = set()
    for f in PHOTOS.glob('*.jpg'): shutil.copyfile(f, d / f.name); keep.add(f.name)
    for v in INFO:
        for ext in ('mp4', 'jpg'): shutil.copyfile(MEDIA / f'{v}.{ext}', d / f'{v}.{ext}'); keep.add(f'{v}.{ext}')
    for f in d.iterdir():
        if f.name not in keep: f.unlink()
