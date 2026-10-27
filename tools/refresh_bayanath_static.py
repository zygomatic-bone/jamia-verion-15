#!/usr/bin/env python3
"""Rewrites the plain-HTML copy of the Bayanath video list in the pages from public/data/bayanath-videos.json.

Run by .github/workflows/update-bayanath.yml right after tools/update_bayanath.py has changed the JSON, so that the committed pages
(the video cards, the JSON-LD ItemList and the "latest lectures" list on the scholar's profile page) match the new list. The visitor's
browser still redraws the cards from the same JSON (portal-assets/bayanath.js); the copy in the HTML is what a search engine or any
reader that does not run scripts sees.

It touches only:
  Bayanath.html            <!--bayanath:cards-->...<!--/bayanath:cards-->      the video cards
  Bayanath.html            the ItemList inside <script id="bayanath-jsonld">   (the other JSON-LD entities are left as they are)
  MuftiMaqsoodImran.html   <!--bayanath:recent-->...<!--/bayanath:recent-->    the short list of latest lectures

The speaker of a video is the scholar (name and profile link are read from the Person entity in the page's own JSON-LD) unless
public/data/bayanath-speakers.json says otherwise: {"<video id>": "Other Speaker"} prints that name (not linked) and
{"<video id>": false} prints no speaker; bayanath.js applies the same rules in the browser.
Standard library only. Exit code 0 = done (prints the files changed), 1 = a file or marker is missing.
"""
import json
import re
import sys
from html import escape
from pathlib import Path

PUB = Path(__file__).resolve().parent.parent / 'public'
BAYANATH_FILE = 'Bayanath.html'
PROFILE_FILE = 'MuftiMaqsoodImran.html'
RECENT = 5   # lectures listed on the profile page
ID_RE = re.compile(r'^[A-Za-z0-9_-]{11}$')
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']   # en-IN short names, as toLocaleDateString prints them
TAGS = re.compile(r'(?:\s*#[^\s#]*)+\s*(?:\.{3}|…)?$')
LEAD = re.compile(r'^[^\w"“‘\'(\[]+')
LD = re.compile(r'(?P<open><script type="application/ld\+json" id="bayanath-jsonld">)(?P<body>.*?)(?P<close></script>)', re.S)


def clean_title(t):
    """Same rule as clean() in bayanath.js: no leading emoji, no trailing hashtags; the full title stays in the link's tooltip."""
    t = re.sub(r'\s+', ' ', str(t)).strip()
    return LEAD.sub('', TAGS.sub('', t)).strip() or t


def fmt_date(iso):
    m = re.match(r'(\d{4})-(\d{2})-(\d{2})', iso or '')
    return f'{int(m.group(3))} {MONTHS[int(m.group(2)) - 1]} {m.group(1)}' if m else ''


def load_videos(path):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    vids = [v for v in data.get('videos', []) if isinstance(v, dict) and ID_RE.match(v.get('id', '')) and isinstance(v.get('title'), str) and v['title']]
    vids.sort(key=lambda v: v.get('published') or '', reverse=True)   # newest first, as bayanath.js shows them
    return ([v for v in vids if v.get('published')] + [v for v in vids if not v.get('published')])[:10]


def load_overrides(path):
    p = Path(path)
    d = json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
    return {k: v for k, v in d.items() if ID_RE.match(k)}


def speaker_of(video, overrides, default_name):
    """-> (name or None, is_the_scholar)"""
    if video['id'] in overrides:
        o = overrides[video['id']]
        if o is False or o is None or o == '':
            return None, False
        return str(o), str(o) == default_name
    return default_name, True


def card_lines(v, name, is_scholar, profile_href):
    watch = f'https://www.youtube.com/watch?v={v["id"]}'
    title = clean_title(v['title'])
    tip = f' title="{escape(v["title"], quote=True)}"' if title != v['title'] else ''
    lines = ['<li class="by-card">',
             f'  <a class="by-thumb" href="{watch}" target="_blank" rel="noopener" aria-label="Play: {escape(title, quote=True)}">'
             f'<img alt="Thumbnail for {escape(title, quote=True)}" loading="lazy" decoding="async" width="480" height="360" referrerpolicy="no-referrer" '
             f'src="{escape(v["thumbnail"], quote=True)}"><span class="by-play" aria-hidden="true"></span></a>',
             '  <div class="by-body">',
             f'    <h3><a class="by-title" href="{watch}" target="_blank" rel="noopener"{tip}>{escape(title)}</a></h3>']
    if name:
        who = (f'<a class="by-speaker-name" href="{escape(profile_href, quote=True)}">{escape(name)}</a>' if is_scholar
               else f'<span class="by-speaker-name">{escape(name)}</span>')
        lines.append(f'    <p class="by-speaker"><span class="by-speaker-l">Speaker:</span> {who}</p>')
    if fmt_date(v.get('published')):
        lines.append(f'    <time class="by-date" datetime="{escape(v["published"], quote=True)}">{fmt_date(v["published"])}</time>')
    lines += [f'    <a class="by-yt" href="{watch}" target="_blank" rel="noopener">Watch on YouTube ↗</a>', '  </div>', '</li>']
    return lines


def recent_lines(videos):
    out = []
    for v in videos[:RECENT]:
        d = fmt_date(v.get('published'))
        date = f' <time datetime="{escape(v["published"], quote=True)}">{d}</time>' if d else ''
        out.append(f'<li><a href="https://www.youtube.com/watch?v={v["id"]}" target="_blank" rel="noopener">{escape(clean_title(v["title"]))}</a>{date}</li>')
    return out


def region(text, name, lines):
    """Replace what lies between <!--bayanath:name--> and <!--/bayanath:name--> (the markers stay), indented like the opening marker."""
    a, b = f'<!--bayanath:{name}-->', f'<!--/bayanath:{name}-->'
    i, j = text.find(a), text.find(b)
    if i < 0 or j < i:
        raise ValueError(f'marker {a} not found')
    indent = text[text.rfind('\n', 0, i) + 1:i]
    body = ''.join(f'\n{indent}{l}' for l in lines)
    return text[:i + len(a)] + body + f'\n{indent}' + text[j:]


def item_list(videos, overrides, graph):
    """ListItem + VideoObject for every video that has an id, a title, a thumbnail and an upload date (a video without a date is
    left out of the data, not given an invented one)."""
    page = next(n for n in graph if 'CollectionPage' in (n['@type'] if isinstance(n['@type'], list) else [n['@type']]))
    person = next(n for n in graph if n['@type'] == 'Person')
    items = []
    for v in videos:
        if not v.get('published') or not v.get('thumbnail'):
            continue
        node = {'@type': 'VideoObject', '@id': f'{page["url"]}#video-{v["id"]}', 'name': clean_title(v['title']), 'thumbnailUrl': v['thumbnail'],
                'uploadDate': v['published'], 'url': f'https://www.youtube.com/watch?v={v["id"]}', 'embedUrl': f'https://www.youtube.com/embed/{v["id"]}',
                'isPartOf': {'@id': page['@id']}}
        if speaker_of(v, overrides, person['name'])[1]:
            node['creator'] = {'@id': person['@id']}
        items.append({'@type': 'ListItem', 'position': len(items) + 1, 'item': node})
    return items


def jsonld(text, videos, overrides):
    m = LD.search(text)
    if not m:
        raise ValueError('bayanath-jsonld script not found')
    indent = text[text.rfind('\n', 0, m.start()) + 1:m.start()]
    data = json.loads(m.group('body'))
    lst = next(n for n in data['@graph'] if n['@type'] == 'ItemList')
    lst['itemListElement'] = item_list(videos, overrides, data['@graph'])
    lst['numberOfItems'] = len(lst['itemListElement'])
    body = json.dumps(data, ensure_ascii=False, indent=2).replace('<', '\\u003c')
    body = '\n'.join(f'{indent}  {l}' for l in body.split('\n'))
    return text[:m.start()] + m.group('open') + '\n' + body + f'\n{indent}' + m.group('close') + text[m.end():]


def person_of(text):
    m = LD.search(text)
    p = next(n for n in json.loads(m.group('body'))['@graph'] if n['@type'] == 'Person')
    return p['name'], p['url'].rsplit('/', 1)[-1]


def refresh_files(pub=PUB):
    """Rewrite the three regions from the current video list; returns the names of the files that changed."""
    pub = Path(pub)
    videos = load_videos(pub / 'data' / 'bayanath-videos.json')
    overrides = load_overrides(pub / 'data' / 'bayanath-speakers.json')
    bayanath = (pub / BAYANATH_FILE).read_text(encoding='utf-8')
    name, profile = person_of(bayanath)
    cards = [l for v in videos for l in card_lines(v, *speaker_of(v, overrides, name), profile)]
    new = jsonld(region(bayanath, 'cards', cards), videos, overrides)
    prof_text = (pub / PROFILE_FILE).read_text(encoding='utf-8')
    prof_new = region(prof_text, 'recent', recent_lines(videos))
    changed = []
    for fname, old, fresh in ((BAYANATH_FILE, bayanath, new), (PROFILE_FILE, prof_text, prof_new)):
        if fresh != old:
            (pub / fname).write_text(fresh, encoding='utf-8', newline='\n')
            changed.append(fname)
    return changed


def main():
    try:
        changed = refresh_files()
    except (OSError, ValueError, KeyError, StopIteration) as e:
        print(f'refresh_bayanath_static: {e}', file=sys.stderr)
        return 1
    print('Updated: ' + ', '.join(changed) if changed else 'The copy of the list in the pages is already up to date.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
