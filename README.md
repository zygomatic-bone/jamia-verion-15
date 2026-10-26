# Jame-ul-Uloom Website: Phase 9.4 build (Jamia Masjid photographs and videos, Bayanath aurora, content clean-up)

Static site. **Deploy only `public/`.** Everything under `tools/` is the generator and the evidence tooling.

## What is in `public/` (112 HTML pages, about 64 MB, of which the two large Urdu PDFs are 46 MB)
- **26 root pages.** `index.html` is the only homepage (`/home` and `/home.html` redirect to `/`). Main-portal pages: About Us, Chairmen's Messages, Governing Body, Trustees, Jamia Masjid, Services, Recognitions, Institutions, Colleges (aims, mission and vision), College Regulations, Activities, Facilities pages (Transport, Smart Classrooms, Science Laboratories, Computer Laboratory, Library, Auditorium, Sports, Calligraphy Centre, Tailoring School), Bayanath (speaker profile beside the YouTube video list), Admissions, Admissions Diary 2013-14, Contact, Careers.
- **61 institution pages** in 11 folders: `ITI/`, `PUGirlsCollege/`, `DegreeGirlsCollege/`, `BCA/`, `NCPUL/`, `EngNurSchoolDEL/`, `EngPrimarySchoolDEL/`, `EngGirlsHighSchool/`, `EngBoysHighSchool/`, `ShobaehifzDel/`, `ShobaeAlimiyathDel/`. Pages whose original text was copied unchanged from another institution are shown once, on the page they describe, and the old URL redirects there.
- **25 pages of the Residential School, Banikuppa** (`ResidentialSchoolBanikuppa/`), unchanged from Phase 8 except the Library page (an unsourced description was removed).
- `portal-assets/images/` (photographs and scans, shown whole, never cropped), `portal-assets/documents/` (3 PDFs, unchanged originals).
- Routing: `_redirects` (Cloudflare Pages / Netlify style) and `.htaccess` (Apache) carry the same 94 legacy-URL redirects plus the `/home` rule. Neither contains credentials or server paths.

## Build and check
```bash
python3 tools/build.py          # school site, then root + institution pages, then the checker
python3 tools/check_site.py     # checker on its own
python3 tools/import_recovered_assets.py <original public_html>   # only when the recovered pictures must be re-imported
python3 -I tools/phase9_audit.py <original public_html> <out dir>      # compares the original backup with public/
python3 -I tools/phase9_manifest.py <audit.json> <phase 8 public dir> <out.csv>
```
`check_site.py` fails on: a broken link, image, script or `#id`; a redirect whose target or `#id` is missing, or that chains; any link to or file named `home.html` at the root; forbidden files in `public/` (design sources, thumbnail caches, server config backups, archives, keys); inline `<script>` bodies or `style=` attributes (the CSP forbids them); images without `alt`.

## Where the content comes from
- `tools/content_main.py`, `content_more.py`, `content_inst.py`: the recovered text, written as Python so every page is regenerated. `rc_helpers.py` holds the figure, scan, table and document components.
- `tools/recovery_assets.py` lists every recovered file with its original path, alt text and caption; `import_recovered_assets.py` copies them byte for byte (the eight CMYK JPEGs are converted to RGB so browsers show their colours correctly).
- Historical conflicts (founding year, strengths, land area) are not resolved on the site: each figure appears only where its source states it, labelled with the source and its date. The list of conflicts and withheld items is in the Phase 9 unresolved-items report.

## Not in this package, on purpose
Nothing from the server backup's private area (mail, cPanel files, credentials, `.htaccess` backups, `cgi-bin`). Original images still withheld: a donation flyer that prints a bank account number (three copies). The named student's certificate is permanently excluded by decision of the website owner. Two unidentified portraits and a stock-style picture are unpublished and listed with their reasons in the manifest.

## Phase 9.2 additions
- **Bayanath, weekly automatic update.** `.github/workflows/update-bayanath.yml` runs every Friday at 21:00 IST (cron `30 15 * * 5`, which GitHub reads as UTC) and on manual start (Actions tab, Run workflow). It runs the self-tests, then `tools/update_bayanath.py`, and commits `public/data/bayanath-videos.json` only when the data really changed. On any failure the existing file is kept. Optional secret `YOUTUBE_API_KEY` (YouTube Data API v3) enables the official uploads playlist; without it the channel's public RSS feed (newest 15) is used. Settings: `tools/bayanath-config.json` (channel, keywords, `exclude_keywords`, optional `playlist_id`, `max_videos` = 10).
- **Self-tests.** `python3 -I -m unittest discover -s tools/tests -v` runs 18 tests against a local fake YouTube. They simulate the feeds; they do not contact YouTube.
- **Speaker Profile** (Bayanath page, left column of a 40/60 two-column layout; the video cards are the right column, and on tablets and phones the speaker card comes first with the videos beneath). Data: `tools/speaker/speaker-profile.json`; renderer: `tools/speaker/speaker.py`; photo: `tools/speaker/photo/` (the owner's file, never cropped); pattern: `tools/speaker/pattern.svg`; styles: `tools/portal-ui/bayanath.css` (loaded only on `Bayanath.html`; speaker classes start with `sp-`, video cards with `by-`, layout and background with `bz-`). The page uses the site navy, gold and neutrals only, with no green. The speaker card also has optional `biography` and `languages` lists in the JSON; they are empty because no verified text has been supplied, and an empty list prints nothing. The profile data is separate from the video feed. Each designation carries a `verification` note for the maintainer; those notes are not shown on the page.
- **Published in 9.2:** nine more photographs (three ITI prize-distribution photographs, three classroom photographs, three calligraphy artworks replacing two stretched GIFs), the ITI staff list (owner approved), and the typed-out captions of the staff photographs and the earlier Governing Body poster.
- **MP3 sermons removed** at the owner's request (the Bayanath videos come from YouTube). The Bayanath page now has the latest-videos list and the Speaker Profile only. Do not re-add `portal-assets/audio/` or an MP3 archive section.

## Phase 9.4 additions
- **Jamia Masjid page** (`Masjid.html`, the only Masjid page): six sections built by `tools/masjid/masjid_page.py` from the owner's 37 photographs (`tools/masjid/photos/`, byte-for-byte copies, never cropped) and 9 silent, compressed videos (`tools/masjid/media/`). Where each picture sits is in `tools/masjid/MASJID-MEDIA-MAP.md`; original file names and checksums are in `photos-provenance.json`. Videos start by themselves when they are on screen and pause when they leave it (`portal-ui/masjid.js`); they stay still when the visitor prefers reduced motion or has data saving on. Styles: `portal-ui/masjid.css`.
- **Homepage:** the B.Com card is removed (the Degree College for Girls pages stay under Institutions); the ITI card shows the ITI building photograph.
- **Bayanath "Live Aurora Glow":** near-black navy with four slow CSS-gradient bands (blue, violet, teal, restrained gold; no green), a stronger glass speaker card, a 40/60 layout. No images, canvas or WebGL; still under `prefers-reduced-motion`. The shared blurred orbs are switched off on this page because they sit behind an opaque background and halved the frame rate.
