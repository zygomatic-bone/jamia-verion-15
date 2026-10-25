#!/usr/bin/env python3
"""Refresh public/data/bayanath-videos.json from the official YouTube channel (standard library only).

Run by .github/workflows/update-bayanath.yml every Friday at 21:00 IST (15:30 UTC), or by hand:
    python3 tools/update_bayanath.py

How it works
  1. Reads tools/bayanath-config.json (channel id, optional Bayanath playlist id, title keywords, limit).
  2. Discovers the channel's recent uploads from ONE of two sources:
       * the YouTube Data API (uploads playlist), when the repository secret YOUTUBE_API_KEY is set. It reaches back
         50 uploads, returns exact publication dates, and states whether a video is public and embeddable;
       * otherwise (or if the API call fails) the channel's public RSS feed, which lists the 15 newest uploads and
         needs no key.
  3. Keeps only eligible videos: every entry of a verified Bayanath playlist (playlist_id), otherwise titles that
     contain a keyword from title_keywords and none from exclude_keywords. Upcoming premieres/live streams are skipped.
  4. Merges with the cached list (older eligible videos are not lost when they scroll out of the feed) and
     de-duplicates on the YouTube video id.
  5. Re-checks every candidate with YouTube's public oEmbed endpoint, so deleted / private / non-embeddable videos are
     dropped, and repairs a title that an earlier run stored truncated ("…"). Entries that still have no publication
     date get it from the video's public watch page when that can be read; nothing is ever guessed.
  6. Sorts newest first, keeps the latest max_videos (exactly ten when at least ten are eligible), validates the result
     and writes it atomically, only if it differs from the cached list.

Safety: ANY failure (network, bad XML/JSON, zero eligible videos, wrong channel, invalid result) exits non-zero
WITHOUT touching the cache, so the website keeps showing the last valid list. Nothing is invented: every field comes
from YouTube. The API key is read from the environment only, sent in a request header and never printed.

Test hooks (environment): YT_FEED_BASE, YT_OEMBED_BASE, YT_CHANNEL_PAGE_BASE, YT_API_BASE, YT_WATCH_BASE replace the
YouTube URLs; BAYANATH_CONFIG and BAYANATH_CACHE replace the config and cache paths. Used by tools/tests/.
"""
import json, os, re, sys, tempfile, urllib.request, urllib.error, urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = Path(os.environ.get('BAYANATH_CONFIG') or ROOT / 'tools' / 'bayanath-config.json')
CACHE = Path(os.environ.get('BAYANATH_CACHE') or ROOT / 'public' / 'data' / 'bayanath-videos.json')
FEED_BASE = os.environ.get('YT_FEED_BASE', 'https://www.youtube.com/feeds/videos.xml')
OEMBED_BASE = os.environ.get('YT_OEMBED_BASE', 'https://www.youtube.com/oembed')
PAGE_BASE = os.environ.get('YT_CHANNEL_PAGE_BASE', 'https://www.youtube.com')
API_BASE = os.environ.get('YT_API_BASE', 'https://www.googleapis.com/youtube/v3')
WATCH_BASE = os.environ.get('YT_WATCH_BASE', 'https://www.youtube.com/watch')
API_KEY = os.environ.get('YOUTUBE_API_KEY', '').strip()
NS = {'a': 'http://www.w3.org/2005/Atom', 'yt': 'http://www.youtube.com/xml/schemas/2015', 'media': 'http://search.yahoo.com/mrss/'}
UA = 'Mozilla/5.0 (compatible; JameUlUloomBayanathBot/2.0; +https://github.com)'
ID_RE = re.compile(r'^[A-Za-z0-9_-]{11}$')
LOG = []


def log(msg):
    print(msg)
    LOG.append(msg)


def summary(status):
    """Append the outcome to the GitHub job summary and expose `changed` as a step output (no-ops outside Actions)."""
    path = os.environ.get('GITHUB_STEP_SUMMARY')
    if path:
        try:
            with open(path, 'a', encoding='utf-8') as f:
                f.write(f'### Bayanath update: {status}\n\n' + '\n'.join(f'- {line}' for line in LOG[-12:]) + '\n')
        except OSError:
            pass


def fail(msg):
    print('ERROR:', msg, file=sys.stderr)
    print('The cached list was left untouched.', file=sys.stderr)
    LOG.append(f'ERROR: {msg}')
    summary('FAILED, cached list kept')
    sys.exit(1)


def get(url, timeout=25, headers=None):
    h = {'User-Agent': UA, 'Accept-Language': 'en', 'Cookie': 'CONSENT=YES+1'}
    h.update(headers or {})
    return urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=timeout)


def check_channel(cfg):
    """Soft safety check: the handle page must belong to the configured channel id (skipped if the page can't be read)."""
    try:
        html = get(f"{PAGE_BASE}/@{cfg['channel_handle']}").read().decode('utf-8', 'replace')
    except Exception as e:
        log(f'WARN: could not read the channel page to confirm the channel id ({e}); continuing.')
        return
    if cfg['channel_id'] in html:
        log('Channel id confirmed against the channel page.')
        return
    found = re.findall(r'"(?:channelId|externalId)":"(UC[\w-]{22})"', html)
    if found:
        fail(f"channel_id {cfg['channel_id']} does not match the id on @{cfg['channel_handle']} ({found[0]}). Fix tools/bayanath-config.json.")
    log('WARN: channel id not found on the page; continuing.')


def valid_iso(s):
    try:
        datetime.fromisoformat(s.replace('Z', '+00:00'))
        return True
    except (ValueError, AttributeError):
        return False


# ---- discovery -------------------------------------------------------------------------------------------------
def fetch_feed(cfg):
    q = {'playlist_id': cfg['playlist_id']} if cfg.get('playlist_id') else {'channel_id': cfg['channel_id']}
    url = f"{FEED_BASE}?{urllib.parse.urlencode(q)}"
    try:
        root = ET.fromstring(get(url).read())
    except Exception as e:
        fail(f'could not download or parse the YouTube feed {url}: {e}')
    out = []
    for e in root.findall('a:entry', NS):
        vid = (e.findtext('yt:videoId', default='', namespaces=NS) or '').strip()
        title = (e.findtext('a:title', default='', namespaces=NS) or '').strip()
        pub = (e.findtext('a:published', default='', namespaces=NS) or '').strip()
        thumb = e.find('media:group/media:thumbnail', NS)
        if not (ID_RE.match(vid) and title and valid_iso(pub)):
            continue
        out.append({'id': vid, 'title': title, 'published': pub, 'thumbnail': thumb.get('url') if thumb is not None else f'https://i.ytimg.com/vi/{vid}/hqdefault.jpg'})
    return out


def api_get(path, params):
    url = f"{API_BASE}/{path}?{urllib.parse.urlencode(params)}"
    with get(url, headers={'X-Goog-Api-Key': API_KEY, 'Accept': 'application/json'}) as r:
        return json.loads(r.read().decode('utf-8'))


def fetch_api(cfg):
    """Uploads playlist (or the verified Bayanath playlist) through the Data API. Returns (videos, unavailable_ids)."""
    pid = cfg.get('playlist_id') or 'UU' + cfg['channel_id'][2:]
    ids, token = [], None
    while len(ids) < 50:
        params = {'part': 'contentDetails', 'playlistId': pid, 'maxResults': 50}
        if token:
            params['pageToken'] = token
        page = api_get('playlistItems', params)
        ids += [i['contentDetails']['videoId'] for i in page.get('items', []) if ID_RE.match(i.get('contentDetails', {}).get('videoId', ''))]
        token = page.get('nextPageToken')
        if not token:
            break
    ids = list(dict.fromkeys(ids))[:50]
    if not ids:
        raise ValueError('the uploads playlist returned no videos')
    data = api_get('videos', {'part': 'snippet,status', 'id': ','.join(ids), 'maxResults': 50})
    out, seen = [], set()
    for it in data.get('items', []):
        vid, sn, st = it.get('id', ''), it.get('snippet', {}), it.get('status', {})
        seen.add(vid)
        pub = sn.get('publishedAt', '')
        if not (ID_RE.match(vid) and sn.get('title') and valid_iso(pub)):
            continue
        if st.get('privacyStatus') != 'public' or st.get('embeddable') is False or sn.get('liveBroadcastContent') == 'upcoming':
            continue
        out.append({'id': vid, 'title': sn['title'].strip(), 'published': pub, 'thumbnail': f'https://i.ytimg.com/vi/{vid}/hqdefault.jpg'})
    return out, [i for i in ids if i not in seen]


def eligible(v, cfg):
    t = v['title'].lower()
    if any(k.lower() in t for k in cfg.get('exclude_keywords', []) if k):
        return False
    if cfg.get('playlist_id'):
        return True  # a verified Bayanath playlist: everything in it counts
    kws = [k.lower() for k in cfg.get('title_keywords', []) if k]
    return True if not kws else any(k in t for k in kws)


# ---- verification ----------------------------------------------------------------------------------------------
def oembed(video_id):
    """(available, title). available is True/False from oEmbed, or None when it could not be determined."""
    watch = f'https://www.youtube.com/watch?v={video_id}'
    try:
        with get(f"{OEMBED_BASE}?{urllib.parse.urlencode({'url': watch, 'format': 'json'})}", timeout=15) as r:
            if r.status != 200:
                return None, None
            try:
                return True, (json.loads(r.read().decode('utf-8')).get('title') or '').strip()
            except ValueError:
                return True, ''
    except urllib.error.HTTPError as e:
        return (False if e.code in (400, 401, 403, 404) else None), None
    except Exception:
        return None, None


def truncated(title):
    return title.rstrip().endswith(('...', '…'))


def repair_title(old_title, full):
    """Replace a title stored cut off with an ellipsis by YouTube's full title, only when it is the same title."""
    if not full or not truncated(old_title):
        return old_title
    stem = old_title.rstrip().rstrip('.…').rstrip()
    return full if full.startswith(stem) and len(full) >= len(stem) else old_title


def watch_date(video_id):
    """Publication date from the public watch page (schema.org meta tag), or None. Used only to fill a missing date."""
    try:
        html = get(f"{WATCH_BASE}?{urllib.parse.urlencode({'v': video_id})}", timeout=15).read(600000).decode('utf-8', 'replace')
    except Exception:
        return None
    m = re.search(r'itemprop="uploadDate"\s+content="([^"]+)"', html) or re.search(r'itemprop="datePublished"\s+content="([^"]+)"', html) \
        or re.search(r'"publishDate":"([^"]+)"', html)
    if not m or not valid_iso(m.group(1)):
        return None
    d = datetime.fromisoformat(m.group(1).replace('Z', '+00:00'))
    if d.tzinfo is None:  # a bare date such as 2026-08-14 carries no time: keep it as a date at UTC midnight
        d = d.replace(tzinfo=timezone.utc)
    return d.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S+00:00')


def parse_dt(s):
    """A sortable UTC datetime; entries without a public date sort after every dated entry."""
    if not s:
        return datetime.min.replace(tzinfo=timezone.utc)
    return datetime.fromisoformat(s.replace('Z', '+00:00'))


def validate(data, limit):
    """Raise ValueError unless the structure is exactly what the website renders."""
    vids = data.get('videos')
    if not isinstance(vids, list) or not vids:
        raise ValueError('no videos')
    if len(vids) > limit:
        raise ValueError(f'more than {limit} videos')
    ids = [v.get('id') for v in vids]
    if len(set(ids)) != len(ids):
        raise ValueError('duplicate video ids')
    last = None
    for v in vids:
        if not ID_RE.match(v.get('id', '')):
            raise ValueError(f"bad video id {v.get('id')!r}")
        if not isinstance(v.get('title'), str) or not v['title'].strip():
            raise ValueError(f"{v['id']}: empty title")
        if v.get('published') is not None and not valid_iso(v['published']):
            raise ValueError(f"{v['id']}: bad date")
        if not re.fullmatch(rf'https://(?:i\d?\.ytimg\.com|img\.youtube\.com)/vi/{re.escape(v["id"])}/[^?#]+(?:[?#].*)?', v.get('thumbnail', '')):
            raise ValueError(f"{v['id']}: thumbnail is not derived from the video id")
        cur = parse_dt(v.get('published'))
        if last is not None and cur > last:
            raise ValueError('not sorted newest first')
        last = cur
    if json.loads(json.dumps(data, ensure_ascii=False)) != data:
        raise ValueError('not JSON round-trippable')


def main():
    cfg = json.loads(CONFIG.read_text(encoding='utf-8'))
    limit = int(cfg.get('max_videos', 10))
    cache = json.loads(CACHE.read_text(encoding='utf-8')) if CACHE.exists() else {'videos': []}
    old = [v for v in cache.get('videos', []) if ID_RE.match(v.get('id', ''))]
    old_ids = {v['id'] for v in old}

    check_channel(cfg)
    source, feed, gone = 'rss', None, []
    if API_KEY:
        try:
            feed, gone = fetch_api(cfg)
            source = 'api'
        except Exception as e:  # never print the key: only the exception type and HTTP code
            code = getattr(e, 'code', '')
            log(f'WARN: the YouTube Data API call failed ({type(e).__name__} {code}); falling back to the public RSS feed.')
    if feed is None:
        feed = fetch_feed(cfg)
    if not feed:
        fail('the source contained no usable videos (wrong channel, empty or invalid response)')
    matched = [v for v in feed if eligible(v, cfg)]
    log(f'Source: {source}; entries read: {len(feed)}; eligible Bayanath: {len(matched)}; unrelated excluded: {len(feed) - len(matched)}; cached before: {len(old)}')
    if not matched:
        fail('no entry matched the Bayanath filter. Set "playlist_id" (a verified Bayanath playlist) or adjust "title_keywords" in tools/bayanath-config.json.')

    merged = {v['id']: dict(v) for v in old}
    for v in matched:
        merged[v['id']] = dict(v)  # fresh data wins; the dict key de-duplicates on the video id
    for vid in gone:
        merged.pop(vid, None)  # the API says it is no longer public/listed

    verified = []
    for v in sorted(merged.values(), key=lambda x: parse_dt(x.get('published')), reverse=True):
        ok, full = oembed(v['id'])
        if ok:
            v['title'] = repair_title(v['title'], full)
            if not v.get('published'):
                v['published'] = watch_date(v['id'])
            verified.append(v)
        elif ok is None and v['id'] in old_ids:
            verified.append(v)  # could not check right now: keep what was verified earlier
            log(f"WARN: could not re-check {v['id']}; keeping the earlier entry")
        else:
            log(f"Dropping {v['id']} ({'unavailable/private/deleted/not embeddable' if ok is False else 'could not be verified'}): {v['title']}")
    verified.sort(key=lambda x: parse_dt(x.get('published')), reverse=True)
    verified = verified[:limit]
    if not verified:
        fail('no video could be verified as public on YouTube')

    fields = lambda v: (v['id'], v['title'], v.get('published'), v.get('thumbnail'))
    if [fields(v) for v in verified] == [fields(v) for v in old]:
        log('No change: the cached list is already up to date; nothing written.')
        if os.environ.get('GITHUB_OUTPUT'):
            with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
                f.write('changed=false\n')
        summary('no update needed')
        return
    new_ids = [v['id'] for v in verified if v['id'] not in old_ids]
    data = {
        'channel': {'handle': cfg['channel_handle'], 'id': cfg['channel_id'], 'url': f"https://www.youtube.com/@{cfg['channel_handle']}"},
        'updated': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'videos': [{k: v.get(k) for k in ('id', 'title', 'published', 'thumbnail')} for v in verified],
    }
    try:
        validate(data, limit)
    except ValueError as e:
        fail(f'the result failed validation ({e})')
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=CACHE.parent, suffix='.tmp')
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2); f.write('\n')
    os.replace(tmp, CACHE)
    log(f'Wrote {len(verified)} videos to {CACHE.name}; new: {len(new_ids)}; newest: {verified[0]["title"]}')
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            f.write('changed=true\n')
    summary(f'updated, {len(new_ids)} new video(s)')


if __name__ == '__main__':
    main()
