#!/usr/bin/env python3
"""Builds JAMIA_PHASE9_RECOVERY_MANIFEST.csv from audit.json (written by phase9_audit.py) and the Phase 8 tree.

Usage: python3 tools/phase9_manifest.py <audit.json> <phase8 public dir> <out.csv>
One row per original file (pages, pictures, PDFs, MP3s, template code, system files) saying what happened to it and why.
"""
import csv, hashlib, json, re, sys
from pathlib import Path

A = json.load(open(sys.argv[1])); P8 = Path(sys.argv[2]); OUT = sys.argv[3]
PUB = Path(__file__).resolve().parent.parent / 'public'
IM = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')
SECTION = {'BCA': 'BCA college', 'DegreeGirlsCollege': 'Degree (B.Com) college', 'EngBoysHighSchool': 'English Boys High School',
           'EngGirlsHighSchool': 'English Girls High School', 'EngNurSchoolDEL': 'English Nursery School', 'EngPrimarySchoolDEL': 'English Higher Primary School',
           'ITI': 'ITI', 'NCPUL': 'MMI-NCPUL Computer Centre', 'PUGirlsCollege': 'PU college for girls', 'ResidentialSchoolBanikuppa': 'Residential School, Banikuppa',
           'ShobaeAlimiyathDel': 'Shoba-e-Alimiyath', 'ShobaehifzDel': 'Shoba-e-Hifz', 'Institutions': 'Institutions page template', 'InstitutionImages': 'Institutions page template',
           'homeimages': 'Main portal', 'images': 'Main portal template', 'masjidimages': 'Jamia Masjid', 'Moulana Maqsood imran Sab Jumma Kutbath': 'Bayanath (sermons)'}
WITHHELD = {
    'NCPUL/images/CERT1.jpeg': 'Permanently excluded by decision of the website owner (Phase 9.2): a diploma certificate issued to a named private student. It must not be published.',
    'ShobaeAlimiyathDel/ShobaeAlimiyathimages/home.jpg': 'Withheld: Darul Quran appeal flyer that prints a bank account number and IFSC code; the English text of the plan is published from the About image instead.'}
TILE = {(170, 80), (180, 100), (188, 188), (125, 125), (200, 100), (119, 91), (109, 85), (125, 104), (170, 170), (94, 119), (36, 36), (50, 35), (47, 60), (257, 49), (159, 44)}
DUP_OF = {'homeimages/Img1.JPG': 'Recognitions page (rec-01, 850x1265)', 'homeimages/testimonials1.jpeg': 'Recognitions page (rec-01, 850x1265)', 'homeimages/Message1.jpeg': 'Chairmen’s Messages (Message 2, 850x1265)'}


def sec(rel):
    return SECTION.get(rel.split('/')[0], 'Main portal' if '/' not in rel else rel.split('/')[0])


def classify(a):
    rel, ext, st = a['orig'], a['ext'], a['status']
    if ext == '.mp3': return ('Removed by decision of the website owner', '', 'Phase 9.2: the website owner asked for the MP3 sermons to be removed because the Bayanath videos are now connected from the official YouTube channel. They were published in Phase 9 and are no longer in public/ or in the ZIP; the original backup still holds them.', 'Folder and page section absent from public/')
    if st == 'byte-identical copy': return ('Published, identical', a['dest'], 'Copied unchanged (or served from the shared copy).', 'SHA-256 equal to the published file')
    if st == 're-encoded copy': return ('Published, re-encoded', a['dest'], a['note'], 'Perceptual hash equal within 6/256, same aspect ratio; CMYK conversions viewed by eye')
    if st == 'near-duplicate (other size)': return ('Represented by a larger/smaller copy', a['dest'], a['note'], 'Perceptual hash + same aspect ratio')
    if ext in ('.css', '.js'): return ('Not published: template code', '', 'Code of the old template; replaced by the shared portal CSS/JS.', '')
    if ext == '.db': return ('Not published: system file', '', 'Windows thumbnail cache (Thumbs.db).', '')
    if ext in ('.psd', '.uga'): return ('Not published: design source', '', 'Editing/source file, not web content.', '')
    if '.htaccess' in rel or rel.startswith('.htaccess'): return ('Not published: hosting configuration', '', 'Server configuration is excluded by instruction; new redirects are generated from the page inventory.', '')
    if (a['w'], a['h']) == (857, 1224): return ('Withheld (see unresolved items)', '', WITHHELD['ShobaeAlimiyathDel/ShobaeAlimiyathimages/home.jpg'], 'Viewed')
    if rel in WITHHELD: return ('Withheld (see unresolved items)', '', WITHHELD[rel], 'Viewed')
    if rel in DUP_OF: return ('Lower-resolution duplicate', DUP_OF[rel], 'Same picture as a higher-resolution file that is published.', 'Viewed side by side')
    w, h = a['w'], a['h']
    name = rel.rsplit('/', 1)[-1]
    if (w, h) in TILE or h <= 14 or w <= 60: return ('Not published: menu graphic', '', 'Navigation tile/button/bullet of the old template (replaced by the new navigation).', 'Size and use')
    if re.match(r'slide\d+\.jpg', name, re.I) and (w, h) == (1300, 400): return ('Not published: template banner', '', 'Header slideshow banner (a montage) of the old ITI template.', 'Viewed')
    if (w, h) == (650, 189): return ('Not published: template banner', '', 'Banner used only as a CSS background in the old template.', 'Viewed')
    if rel in ('images/2.PNG', 'images/33.jpg'): return ('Not published: decorative template art', '', 'Phase 9.2 review: an architectural render of a large building, used only as a slide of the removed “Enter Portal” screen (images/style.css). Nothing says which building it is, so it cannot be captioned and is not published.', 'Viewed')
    if rel.startswith('images/') or name in ('Img2.JPG', 'Img3.jpg', 'Img4.JPG', 'Img5.JPG', 'butterfly.gif'):
        return ('Not published: decorative template art', '', 'Title/slide artwork or stock-style picture of the old template; not content of any institution page.', 'Viewed')
    low = name.lower()
    if low == 'cali2.gif': return ('Represented by a larger copy', 'portal-assets/images/calligraphy/calligraphy-2.jpg', 'Phase 9.2: the same artwork as cali2.jpg at 449x295; the larger 624x418 original JPG is now the published picture.', 'Viewed side by side; similarity 0.98')
    if low == 'cali8.gif': return ('Superseded by an undistorted original', 'portal-assets/images/calligraphy/calligraphy-8.jpg', 'Phase 9.2: the GIF is the same artwork stretched sideways (449x295) from the square original cali8.jpg (480x480); the square JPG is now the published picture, so the stretched copy is no longer served.', 'Viewed side by side')
    if low == 'cali1.gif': return ('Represented by a larger copy', 'portal-assets/images/calligraphy/calligraphy-0-emblem.jpg', 'Phase 9.2: same Calligraphy Centre artwork as cali1.jpg (a tighter crop at lower resolution); the larger JPG is published.', 'Viewed side by side')
    if low == 'headmistress.jpg': return ('Represented by a larger copy', 'portal-assets/images/schools/head-mistress.jpg', 'Phase 9.2 review: a 175x116 thumbnail of the already published Head Mistress photograph (same scene, same desk nameplate); never displayed by an original page (dead CSS rule).', 'Viewed; similarity 0.95 on a 24x24 comparison')
    if low == 'principal.jpg':
        big = 'portal-assets/images/colleges/principal-pu.jpg' if rel.startswith('PUGirlsCollege/') else 'portal-assets/images/colleges/principal-degree-bca.jpg'
        return ('Represented by a larger copy', big, 'Phase 9.2 review: a thumbnail of the already published Principal photograph for this college; never displayed by an original page (dead CSS rule).', 'Viewed; similarity 0.97-0.99 on a 24x24 comparison')
    if rel == 'ITI/ITIimages/Classroom1.jpg': return ('Represented by a larger copy', 'portal-assets/images/colleges/classroom-pu-3.jpg', 'Phase 9.2 review: the same classroom photograph as the published PU College classroom picture (whiteboard between two green boards), same size; not published twice.', 'Viewed side by side; similarity 0.97')
    if low in ('chairmen.jpg', 't1.jpg'): return ('Not published: portrait with no identification', '', 'Phase 9.2 review: a small portrait of a man. No original page displays it (only a dead CSS rule or nothing) and nothing printed names him or says what the file shows, so no caption could be written without guessing. Left unpublished.', 'Viewed')
    if low == 'student.jpg': return ('Not published: decorative template art', '', 'Phase 9.2 review: a stock-style portrait of a boy (with a visible grey editing patch) from the old template; not a photograph of any institution. The project forbids stock photographs.', 'Viewed')
    if name.lower() in ('cali1.jpg', 'cali2.jpg', 'cali8.jpg'): return ('Unreferenced variant', '', 'Calligraphy artwork file that no original page displays (the Cali2–8.GIF and Caligraphy1 pictures the pages did display are published).', 'Viewed')
    if name.lower() in ('principal.jpg', 'headmistress.jpg', 'chairmen.jpg', 't1.jpg'):
        return ('Not published: unreferenced portrait', '', 'Small portrait not displayed by any original page (CSS background or unused); the people are not identified in the original.', 'Viewed')
    if re.match(r'(DSC\d+|Classroom1?)\.(jpg)$', name, re.I): return ('Not published: unreferenced photograph', '', 'Real photograph in an institution folder that no original page displays; subject and institution are not stated, so it is listed in the unresolved items instead of being captioned by guess.', 'Viewed')
    return ('Unclassified', '', a['note'], '')


rows = []
# ---- pages
for pg in A['pages']:
    rel = pg['orig']; st = pg['status']; p8 = P8 / rel
    new = PUB / rel
    if st == 'rebuilt at same URL':
        if p8.exists():
            same = hashlib.sha256(p8.read_bytes()).hexdigest() == hashlib.sha256(new.read_bytes()).hexdigest()
            status, action = 'Present', 'Phase 8 page kept unchanged' if same else 'Phase 8 page revised in Phase 9 (content recovered, unsupported text removed or navigation updated)'
        else:
            status, action = 'Present (new in Phase 9)', 'Page did not exist in Phase 8; rebuilt from the original text, photographs and scans'
        dest = rel; ver = 'Link check; 390px and 1280px screenshots; text compared with original'
    elif st == '301 redirect':
        status, dest, action, ver = 'Redirected', pg['dest'], 'Original URL kept alive: 301 to the page that now carries this content (copied-text pages are shown once on the page they describe)', 'check_site.py checks target and #id; redirect rules in _redirects and .htaccess'
    else:
        status, dest, action, ver = 'Removed by design', pg['dest'], 'The root portal page/"Enter Portal" screen must not exist; / is the homepage', 'check_site.py fails if public/home.html exists'
    rows.append(['page', rel, 'html', sec(rel), '', '', '', '', status, dest, action, ver])
# ---- files
for a in A['assets']:
    st, dest, act, ver = classify(a)
    dims = f"{a['w']}x{a['h']}" if a['w'] else ''
    rows.append(['asset', a['orig'], a['ext'].lstrip('.') or 'none', sec(a['orig']), a['bytes'], dims, a['sha'], a['dups'] if a['dups'] > 1 else '', st, dest, act, ver])
for o in A['orphans']:
    rows.append(['public-orphan', '(none: new file)', Path(o).suffix.lstrip('.'), 'Inherited from Phase 8' if o.startswith('ResidentialSchoolBanikuppa/') else 'Phase 9', (PUB / o).stat().st_size, '', '', '', 'In public/ but not referenced by any page', o,
                 'Menu tile / social icon of the old Banikuppa template carried over unchanged from Phase 8; harmless, kept so no Phase 8 file is removed' if o.startswith('ResidentialSchoolBanikuppa/') else 'Unused recovered file: remove or use', 'Listed so it is accounted for'])
# ---- Phase 9.2 additions that do not come from the original server backup
_ph = PUB / 'portal-assets/speaker/mufti-maqsood-imran-rashadi.jpg'
rows.append(['asset', '(owner-supplied attachment) 12f714ee-image.jpg', 'jpg', 'Bayanath (Phase 9.2)', _ph.stat().st_size, '650x399', hashlib.sha256(_ph.read_bytes()).hexdigest()[:12], '', 'Published, identical', 'portal-assets/speaker/mufti-maqsood-imran-rashadi.jpg',
             'Speaker photograph supplied by the website owner for the Bayanath Speaker Profile; copied byte for byte and shown whole (not cropped)', 'SHA-256 equal to the attachment; viewed at 1440, 820 and 390 px'])
_pt = PUB / 'portal-assets/speaker/pattern.svg'
rows.append(['asset', '(created in Phase 9.2)', 'svg', 'Bayanath (Phase 9.2)', _pt.stat().st_size, '120x120', hashlib.sha256(_pt.read_bytes()).hexdigest()[:12], '', 'New file', 'portal-assets/speaker/pattern.svg',
             'Decorative geometric (eight-pointed star) tile for the animated Speaker Profile background; drawn as vector lines, no photograph', 'Viewed in the page'])
hdr = ['record', 'original_path', 'kind', 'institution_or_section', 'bytes', 'dimensions', 'sha256_first12', 'identical_copies_in_original', 'phase9_status', 'phase9_destination', 'action_and_reason', 'verification']
with open(OUT, 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f); w.writerow(hdr); w.writerows(rows)
from collections import Counter
print(len(rows), 'rows'); [print(f'  {n:5d} {k}') for k, n in Counter(r[8] for r in rows).most_common()]
