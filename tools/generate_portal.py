"""Generator for the main Jame-ul-Uloom (Jamia Masjid, Bangalore) portal pages and sibling institutional routes.

Writes into public/ (the root of jameululoom.org):
  - 13 root portal HTML pages: index.html (the single official homepage), Institutions.html, Activities.html,
    Services.html, Recognitions.html, ScienceLabs.html, Transport.html, Bayanath.html,
    Contact.html, Careers.html, Admissions.html, Tailoring.html, InsShobaeAlimiyath.html
  - Sibling institutional pages (ITI/, PUGirlsCollege/, DegreeGirlsCollege/, BCA/,
    EngGirlsHighSchool/, EngBoysHighSchool/, NCPUL/) with verified institutional content
  - public/portal-assets/portal.css
Run: python tools/generate_portal.py
"""
from pathlib import Path
import re
import shutil
from html import escape
from urllib.parse import quote
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_header import site_header  # the single shared header (also used by generate_site.py)

PUB = Path(__file__).resolve().parent.parent / 'public'
ASSETS = PUB / 'portal-assets'
ASSETS.mkdir(parents=True, exist_ok=True)

NAME = 'Jame ul uloom, Jamia Masjid, Bangalore'
# UI sources (shared design system, same as the Banikuppa subsite) live in tools/portal-ui/.
UI = Path(__file__).resolve().parent / 'portal-ui'


# Photographs live in the Residential School's asset folder; root pages reference them in place (never copied or renamed).
IMG_REL = 'ResidentialSchoolBanikuppa/assets/images/'
SCHOOL = 'ResidentialSchoolBanikuppa/'

from imgutil import image_size  # PNG / JPEG / GIF header reader
import recovery_assets as RA
import content_main, content_more, content_inst   # Phase 9: restored original content (see tools/content_*.py)
sys.path.insert(0, str(Path(__file__).resolve().parent / 'speaker'))
import speaker   # Phase 9.2: Speaker Profile on Bayanath.html (tools/speaker/)

def fit_media(rp, fn, alt, cls='pf-media', loading='lazy'):
    """Whole photograph (never cropped) over a blurred copy of itself, same pattern as the school site's cards."""
    base = '' if fn.startswith('portal-assets/') else IMG_REL
    w, h = image_size(PUB / base / fn)
    src = escape(f'{rp}{base}{fn}', quote=True)
    return (f'<div class="{cls}"><img class="fit-bg" src="{src}" alt="" aria-hidden="true" loading="lazy" decoding="async">'
            f'<img class="fit" src="{src}" alt="{escape(alt, quote=True)}" width="{w}" height="{h}" loading="{loading}" decoding="async"></div>')

ICON_SCHOOL = '<svg class="btn-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 21h18M5 21V10l7-5 7 5v11M9 21v-6h6v6M12 5V2.5M12 2.5h3"></path></svg>'
ICON_INSTITUTIONS = '<svg class="btn-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 21h18M4 10l8-6 8 6M6 10v8M10 10v8M14 10v8M18 10v8"></path></svg>'

# Photograph for each institution card: an authentic photograph of that institution (Phase 9), shown whole.
def _P(key):
    """Card photograph tuple (file, alt, caption) for a recovered image key."""
    _, dest, alt, cap = RA.IMAGES[key]
    return (RA.R + dest, alt, None)

INST_META = {
    # Every card shows an authentic photograph of that institution from the original site (Phase 9); no "illustrative" substitutes remain.
    'Industrial Training Institute (ITI)': ('Vocational training', 'ITI', _P('iti_campus')),
    'Pre University College for Girls': ('Pre-University', 'PU', _P('pu_school')),
    'Degree College for Girls (B.Com)': ('Degree college', 'B.Com', _P('deg_cls1')),
    'Bachelor of Computer Application (BCA)': ('Degree college', 'BCA', _P('col_comp')),
    'Boys Residential Higher & Primary School, Banikuppa': ('Residential school', '', ('slide5.jpg', 'The school building at the Banikuppa residential campus', None)),
    'English Girls High School': ('High school', 'EGHS', _P('girls_group')),
    'English Boys High School': ('High school', 'EBHS', _P('boys_group')),
    'English Higher Primary School': ('Primary school', 'EHPS', _P('hp_group')),
    'English Nursery School': ('Nursery', 'ENS', _P('nur_group')),
    'MMI-NCPUL Computer Centre': ('Computer training', 'NCPUL', _P('ncpul_lab1')),
    'Tailoring School for Women': ('Vocational training', 'TS', _P('tailoring')),
    'Calligraphy': ('Department', 'CAL', _P('cal_intro')),
    'Shoba-e-Hifz': ('Quranic studies', '', _P('dq_plan')),
    'Shoba-e-Alimiyath': ('Islamic scholarship', 'SA', _P('dq_plan')),
}
# Cards that point at a shared page (no dedicated page exists) say so honestly in the link text.
GENERIC_LINK = {}

def inst_card(n, u, d, rp=''):
    tag, initials, photo = INST_META[n]
    if photo:
        fn, alt, note = photo
        media = fit_media(rp, fn, alt, 'pf-media')
        if note: media += f'<p class="pf-note">{escape(note)}</p>'  # label sits below the photograph, never over it
    else:
        media = f'<div class="pf-media pf-brand" aria-hidden="true"><span class="pf-initials">{escape(initials)}</span><span class="pf-brand-sub">Jame-ul-Uloom</span></div>'
    label = GENERIC_LINK.get(u, 'Explore institution')
    return (f'<li class="pf-card">{media}<div class="pf-body"><p class="pf-tag">{escape(tag)}</p><h3>{escape(n)}</h3><p>{escape(d)}</p>'
            f'<a class="pf-go" href="{rp}{u}">{label} <span aria-hidden="true">→</span></a></div></li>')

SPLIT = re.compile(r'^<p class="eyebrow">(.*?)</p><h1>(.*?)</h1>(?:<p class="lede">(.*?)</p>)?', re.S)

# ---- Photograph sections on interior pages ----------------------------------------------------------------------------
# PAGE_PHOTOS is the photo-to-page map (also written up in tools/PHOTO-MAP.md). To add or swap a photograph, edit one tuple:
# (file in the Residential School image folder, accurate alt text, caption title, caption detail). Photographs are shown whole
# (never cropped) with the same blurred-backdrop pattern as the rest of the portal. Pages with no authentic photograph are listed
# in tools/PHOTO-MAP.md instead of being given an unrelated picture.
CAMPUS = 'Banikuppa residential campus'
PAGE_PHOTOS = {
    'ScienceLabs.html': ('Laboratory photographs', f'Practical work in the science laboratories of the {CAMPUS}.', [
        ('chemistrylab.jpg', 'A teacher demonstrating an experiment at a chemistry laboratory bench while students look on', 'Chemistry laboratory', CAMPUS),
        ('physicslab.jpg', 'Students and visitors gathered around laboratory tables in the physics laboratory', 'Physics laboratory', CAMPUS),
        ('biologylab.jpg', 'Students, teachers and visitors at the long glass-topped benches of the biology laboratory', 'Biology laboratory', CAMPUS),
    ]),
    'Activities.html': ('Activities in pictures', f'Sports, house competitions and annual-day programmes at the {CAMPUS}.', [
        ('sportsevent.jpg', 'Rows of students in white, blue, red and yellow performing a group exercise drill on the sports ground', 'Group drill on the sports ground', CAMPUS),
        ('sportsevent1.jpg', 'A winning team posing with trophies and certificates beside a student sprinting in an athletics event', 'Sports day winners and athletics', CAMPUS),
        ('houses.jpg', 'Students seated in rows wearing white, red, blue and yellow house colours in front of a school building', 'House competitions', CAMPUS),
        ('audi4.jpg', 'A speaker at the podium during an annual function, and students in traditional costume on a decorated stage', 'Annual day programme', CAMPUS),
    ]),
    'Transport.html': ('Campus facilities in pictures', f'Teaching and residential facilities at the {CAMPUS}.', [
        ('classroom.jpg', 'Students seated at desks in a classroom, writing', 'Classroom', CAMPUS),
        ('library.jpg', 'Students reading at tables in the school library', 'Library', CAMPUS),
        ('computerlab.jpg', 'Rows of computer workstations in the computer laboratory', 'Computer laboratory', CAMPUS),
        ('hostel.jpg', 'The white two-storey hostel building with a lawn in front', 'Hostel building', CAMPUS),
        ('dinninghall.jpg', 'The dining hall building seen across a hedge and lawn', 'Dining hall', CAMPUS),
    ]),
}

def photo_section(filename, rp=''):
    """HTML for the photograph gallery of one interior page ('' when the page has none)."""
    if filename not in PAGE_PHOTOS: return ''
    title, intro, items = PAGE_PHOTOS[filename]
    cards = ''.join(
        f'<li class="pv-item"><figure class="pv-card">{fit_media(rp, fn, alt, "pf-media pv-media")}'
        f'<figcaption><strong>{escape(cap)}</strong><span>{escape(detail)}</span></figcaption></figure></li>'
        for fn, alt, cap, detail in items)
    return (f'<section class="pv-section" aria-labelledby="pv-{filename[:-5].lower()}"><div class="pv-head"><h2 id="pv-{filename[:-5].lower()}">{escape(title)}</h2>'
            f'<p>{escape(intro)}</p></div><ul class="pv-grid">{cards}</ul></section>')

def wordmark(rp, cls='brand brand-text'):
    return f'<a class="{cls}" href="{rp}index.html" aria-label="Jame ul uloom, Jamia Masjid, Bangalore — home">Jame ul uloom<small>Jamia Masjid, Bangalore</small></a>'

def bg_photo(fn, side='right'):
    """Decorative, translucent background photograph (aria-hidden, blurred, masked). Never a content image."""
    return f'<div class="pf-bgphoto pf-bg-{side}" aria-hidden="true"><img src="{IMG_REL}{fn}" alt="" loading="lazy" decoding="async"></div>'

def page(filename, title, body, desc, root_prefix=''):
    rp = root_prefix
    m = SPLIT.match(body)
    eyebrow, h1, lede = (m.group(1), m.group(2), m.group(3)) if m else ('', escape(title), None)
    content = body[m.end():] if m else body
    if filename == 'index.html' and not rp:
        # same heading text, split at the comma so it breaks sensibly when centred
        hero_h1 = h1.replace(', ', ',</span> <span class="hl">', 1) if ', ' in h1 else h1
        hero_h1 = f'<span class="hl">{hero_h1}</span>'
        # Hero ("Modern Overlay"): one authentic campus photograph under a navy gradient, text on the left (styles in extras.css).
        hero = (f'<section class="hero portal-hero"><div class="pf-hero-bg" aria-hidden="true">'
                f'<img class="pf-hbg" src="portal-assets/hero/hero-assembly.jpg" alt="" width="1703" height="923" decoding="async" fetchpriority="high"></div>'
                f'<div class="hero-copy container"><p class="hx-kicker">Knowledge <span aria-hidden="true">·</span> Character <span aria-hidden="true">·</span> Service</p>'
                f'<h1>Jame ul <span class="hx-gold">uloom</span></h1>'
                f'<p class="hx-label">Islamic Educational Institution</p><span class="hx-rule" aria-hidden="true"></span>'
                f'<p class="hero-lede">{lede or ""}</p>'
                f'<div class="button-row"><a class="button hx-btn-gold" href="Institutions.html">Institutions</a>'
                f'<a class="button hx-btn-gold" href="ResidentialSchoolBanikuppa/index.html">Residential School</a>'
                f'<a class="button hx-btn-ghost" href="Bayanath.html"><svg class="btn-icon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9.5"></circle><path d="M10 8.5v7l6-3.5Z"></path></svg>Watch Bayanath</a></div>'
                f'<ul class="hx-points" aria-label="Highlights">'
                f'<li><a href="ShobaeAlimiyathDel/home.html"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5.5C6.5 4.5 9.5 4.5 12 6c2.5-1.5 5.5-1.5 8-.5V19c-2.5-1-5.5-1-8 .5-2.5-1.5-5.5-1.5-8-.5ZM12 6v13.5"></path></svg><span>Islamic<br> Education</span></a></li>'
                f'<li><a href="ResidentialSchoolBanikuppa/index.html"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 21h18M5 21V10l7-5 7 5v11M9 21v-6h6v6M12 5V2.5M12 2.5h3"></path></svg><span>Residential<br> School</span></a></li>'
                f'<li><a href="Services.html"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="9" cy="8" r="3"></circle><path d="M3.5 19c0-3 2.5-5 5.5-5s5.5 2 5.5 5"></path><circle cx="17" cy="9" r="2.2"></circle><path d="M16 14.2c2.7 0 4.5 1.7 4.5 4.3"></path></svg><span>Community<br> Service</span></a></li>'
                f'<li><a href="Activities.html"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3.5l2.6 5.4 5.9.8-4.3 4.1 1 5.8L12 16.8l-5.2 2.8 1-5.8-4.3-4.1 5.9-.8Z"></path></svg><span>Student<br> Activities</span></a></li>'
                f'</ul></div></section>')
        main = hero + INDEX_SECTIONS
    else:
        crumbs = f'<p class="crumbs"><a href="{rp}index.html">Home</a> / {eyebrow}</p>' if eyebrow else ''
        lede_html = f'<p class="lede">{lede}</p>' if lede else ''
        hero_cls, content_cls = COMPACT.get(filename, ('', '')) if not rp else ('', '')
        main = (f'<section class="page-hero {hero_cls}"><div class="container">{crumbs}<h1>{h1}</h1>{lede_html}</div></section>'
                f'<section class="section portal-content {content_cls}"><div class="container">{content}</div></section>')
    footer = (f'<footer class="site-footer"><div class="container"><div class="footer-grid">'
              f'<div class="footer-brand">{wordmark(rp, "brand-text")}<p>Jamia Masjid &amp; Muslim Charitable Fund Trust, S.J.P. Road, City Market, Bangalore – 560002.</p></div>'
              f'<div><h2>Explore</h2><a href="{rp}index.html">Home</a><a href="{rp}Institutions.html">Institutions</a><a href="{rp}Services.html">Services</a><a href="{rp}Activities.html">Activity Calendar</a><a href="{rp}Masjid.html">Jamia Masjid &amp; prayer times</a></div>'
              f'<div><h2>Community</h2><a href="{rp}AboutUs.html">About Us</a><a href="{rp}Message.html">Chairmen’s Messages</a><a href="{rp}Team.html">Governing Body</a><a href="{rp}Recognitions.html">Recognitions</a><a href="{rp}Bayanath.html">Bayanath</a><a href="{rp}Admissions.html">Admissions</a><a href="{rp}Careers.html">Careers</a></div>'
              f'<div><h2>Contact</h2><a href="{rp}Contact.html">Contact directory</a><a href="mailto:jamiaululoom@gmail.com">jamiaululoom@gmail.com</a><a href="{rp}ResidentialSchoolBanikuppa/index.html">Banikuppa school</a></div>'
              f'</div><div class="footer-bottom"><span>© <span data-current-year>2026</span> Jamia Masjid &amp; Muslim Charitable Fund Trust</span><span>Jame-ul-Uloom, Bangalore</span></div></div></footer>')
    extra_js = f'<script src="{rp}portal-assets/bayanath.js" defer></script>' if filename == 'Bayanath.html' and not rp else ''
    extra_css = f'<link rel="stylesheet" href="{rp}portal-assets/bayanath.css">' if filename == 'Bayanath.html' and not rp else ''  # Bayanath layout, speaker card and video-card styles load on this page only
    body_cls = ' class="page-home"' if (filename == 'index.html' and not rp) else (' class="page-bayanath"' if (filename == 'Bayanath.html' and not rp) else '')  # lets the homepage-only dark theme in extras.css find the homepage
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{escape(title)} | {NAME}</title><meta name="description" content="{escape(desc, quote=True)}"><meta name="theme-color" content="#123c2e"><script src="{rp}portal-assets/theme-init.js"></script><link rel="stylesheet" href="{rp}portal-assets/portal.css">{extra_css}</head><body{body_cls}>{site_header(rp, current=(filename if not rp else None))}<main id="main">{main}</main>{footer}<button class="icon-button back-top" type="button" aria-label="Back to top"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"></path></svg></button><script src="{rp}portal-assets/app.js" defer></script>{extra_js}</body></html>"""

# 1. index.html: the single official homepage. This text feeds the hero (eyebrow, heading, lede);
#    the hero buttons and photographs are built in page(), and the sections below the hero are INDEX_SECTIONS.
index_hero = f'''<p class="eyebrow">Jamia Masjid &amp; Muslim Charitable Fund Trust</p><h1>{NAME}</h1><p class="lede">Welcome to Jame-ul-Uloom, housed on the campus of Jamia Masjid, City Market, Bangalore.</p>'''

# 2. Content shown on the homepage (moved here from the removed portal "home" page)
PRAYERS = [('Fajar', '5:40 AM'), ('Zohar', '1:30 PM'), ('Asar', '5:00 PM'), ('Magrib', '6:35 PM'), ('Isha', '8:15 PM')]
ANNOUNCEMENTS = [
    ('Students Admissions Open', 'Admissions.html'),
    ('Bannikuppa Results', 'ResidentialSchoolBanikuppa/academics.html'),
    ('Jame ul uloom ek tahreek', 'Services.html'),
    ('PU College Results', 'PUGirlsCollege/home.html'),
]
# 3. Institutions.html
INSTS = [
    ('Industrial Training Institute (ITI)', 'ITI/home.html', 'Shikshanagar campus (27th km off the Bangalore–Mysore Highway); Fitter, MRAC & MMV trades.'),
    ('Pre University College for Girls', 'PUGirlsCollege/home.html', 'Pre-University education for girls (Science PCMB and Commerce combinations) at S.J.P. Road, City Market (Ph: 0826705591).'),
    ('Degree College for Girls (B.Com)', 'DegreeGirlsCollege/home.html', 'Bachelor of Commerce programme for women (Ph: 0826709915).'),
    ('Bachelor of Computer Application (BCA)', 'BCA/home.html', 'Bachelor of Computer Application college for girls, “at an arms length from the Jamia Mosque”'),
    ('Boys Residential Higher & Primary School, Banikuppa', 'ResidentialSchoolBanikuppa/index.html', 'Residential campus on the Bangalore–Mysore Highway.'),
    ('English Girls High School', 'EngGirlsHighSchool/home.html', 'High school for girls, started in 1990-91 with 13 girls .'),
    ('English Boys High School', 'EngBoysHighSchool/home.html', 'High school for boys at Ibrahim Ali Shah complex, S.P. Road (Boys Block Ph: 0822221726).'),
    ('English Higher Primary School', 'EngPrimarySchoolDEL/home.html', 'Primary school from 1st to VII standard, three sections in each class.'),
    ('English Nursery School', 'EngNurSchoolDEL/home.html', 'Nursery school; moral education and the learning of Hadiths begin at this stage.'),
    ('MMI-NCPUL Computer Centre', 'NCPUL/home.html', 'One-year computer applications and multilingual DTP course, mainly for girls (Ph: 0822221158).'),
    ('Tailoring School for Women', 'Tailoring.html', 'The Tailoring Department of Jamia Masjid: girls learning the art of tailoring.'),
    ('Calligraphy', 'Calligraphy.html', 'Urdu language and Urdu calligraphy centre run at the Jamia Masjid premises.'),
    ('Shoba-e-Hifz', 'ShobaehifzDel/home.html', 'The Hifz section: Hafiz and Hafiza classes for boys and girls.'),
    ('Shoba-e-Alimiyath', 'ShobaeAlimiyathDel/home.html', 'J.U Darul Quran Arabic College: Arabic studies at the Bannikuppa campus (proposed building).'),
]
institutions = f'''<p class="eyebrow">Jame-ul-Uloom Group of Institutions</p><h1>Institutions</h1><p class="lede">The 14 educational institutions operated by the Jamia Masjid &amp; Muslim Charitable Fund Trust.</p><ul class="pf-grid pf-grid-long pf-stagger">{''.join(inst_card(n, u, d) for n, u, d in INSTS)}</ul>'''+content_more.institutions_extra()
COMPACT = {'Institutions.html': ('page-hero-compact', 'portal-content-tight')}

# 4. Activities.html
CAL_ROWS = [
    ('June', '—', '—', 'School reopens'),
    ('July', 'Lower Primary School<br>Higher Primary School<br>High School', 'Third week<br>Last week<br>Last week', 'Hamd and Nath<br>Qirath / Hamd / Nath<br>Hamd and Nath'),
    ('August', 'Lower Primary School<br>Higher Primary School<br>High School', 'Third week<br>Last week<br>Last week', 'Art &amp; Drawing<br>Needle Work<br>Creative Writing'),
    ('September', 'Lower Primary School<br>Higher Primary School<br>High School', 'Third week<br>Last week<br>Last week', 'Paper Folding<br>Fabric Painting<br>Clay Modelling'),
    ('October', 'Kinder Garden<br>Lower Primary School<br>Higher Primary School<br>High School', 'Second week<br>Third week<br>Last week<br>Last week', 'Recitation<br>Recitation<br>Arabic Quiz<br>Arabic Quiz'),
    ('November', 'Lower Primary School<br>Higher Primary School<br>High School', 'Third week<br>Last week<br>Last week', 'Clay Modeling<br>Science Quiz<br>Science Quiz'),
    ('December', 'Kinder Garden<br>Lower Primary School<br>Higher Primary School<br>High School', 'To be announced', 'Hamd and Nath<br>Literary Competition'),
    ('January', 'Kinder Garden<br>Lower Primary School<br>Higher Primary School<br>Higher Primary Boys School<br>High School Boys<br>High School Girls', 'Second week<br>Third week<br>Third week<br>Last week<br>Last week<br>Last week', 'Fancy Dress<br>Fancy Dress<br>Fancy Dress<br>Mono Acting<br>Mehendi Designs<br>Mehendi Designing'),
]
activities = f'''<p class="eyebrow">Students</p><h1>Extra-Curricular Activities &amp; Activity Calendar</h1>
<div class="prose">
  <p>All-round personality development is a central goal of education at Jame-ul-Uloom. Alongside academics, students participate in quizzes, debates, fancy dress, painting, needlework, clay modelling, and creative writing to cultivate their talents, and represent the institution in inter-school and DHIE competitions.</p>
  <p>Teachers’ Day, Children’s Day, and national festivals such as Independence Day and Republic Day provide further stages for students across all divisions to showcase their abilities.</p>
</div>
{photo_section('Activities.html')}
{content_more.activities_extra()}
<h2>Annual Activity Calendar (June – January)</h2>
<div class="table-wrap"><table class="cal"><thead><tr><th>Month</th><th>School Division</th><th>Schedule Window</th><th>Competition / Event</th></tr></thead><tbody>
{''.join(f'<tr><td><strong>{m}</strong></td><td>{div}</td><td>{day}</td><td>{comp}</td></tr>' for m, div, day, comp in CAL_ROWS)}
</tbody></table></div>
<p>For residential school house competitions and athletics at the Banikuppa campus, see <a href="ResidentialSchoolBanikuppa/sports.html">Banikuppa Co-Curricular Activities &amp; Sports</a>.</p>'''

# 5. Services.html, Recognitions.html, ScienceLabs.html, Transport.html
services = content_more.services

recognitions = '''<p class="eyebrow">Institution</p><h1>Awards &amp; Recognition</h1><p class="lede">Recognitions and letters of appreciation received by Jame-ul-Uloom, Jamia Masjid, Bangalore.</p>
''' + content_more.recognitions_intro

sciencelabs = content_more.sciencelabs(photo_section('ScienceLabs.html'))

transport = content_more.transport(photo_section('Transport.html'))

# 6. Contact.html, Careers.html, Admissions.html, Tailoring.html, InsShobaeAlimiyath.html
PHONES = [('Administrative Office', ['0822221165', '0822272086']), ('Secretary Saheb (cellar)', ['0822221725']), ('Boys Block', ['0822221726']), ('Jamia Masjid', ['0822239495']), ('Head Mistress', ['0822221156']), ('Maqsood Imran Saheb', ['0822221151']), ('P.U College', ['0826705591', '0826705486']), ('B.C.A', ['0826709915']), ('JUU Computer Section', ['0822221161']), ('M.M.I NCPUL', ['0822221158'])]
contact = f'''<p class="eyebrow">Contact us</p><h1>Contact Directory</h1><p class="lede">Jamia Masjid &amp; Muslim Charitable Fund Trust, S.J.P. Road, City Market, Bangalore – 560002.</p><h2>Departments &amp; Direct Lines</h2><ul class="card-grid portal-cards">{''.join('<li class="card"><h3>'+escape(d)+'</h3>'+''.join(f'<p><a href="tel:{n}">{n}</a></p>' for n in ns)+'</li>' for d, ns in PHONES)}</ul><h2>Email</h2><p><a href="mailto:jamiaululoom@gmail.com">jamiaululoom@gmail.com</a></p><h2>Boys Residential School, Banikuppa</h2><p>See the <a href="ResidentialSchoolBanikuppa/contact.html">Banikuppa school contact page</a>.</p>'''

careers = '''<p class="eyebrow">Contact us</p><h1>Careers</h1><p class="lede">Welcome to Jame-ul-Uloom Careers — S.J.P. Road, City Market, Bangalore – 560002.</p>
<dl class="facts"><dt>Address</dt><dd>S.J.P. Road, City Market, Bangalore – 560002</dd><dt>Telephone</dt><dd><a href="tel:0822221151">0822221151</a>, <a href="tel:0822239495">0822239495</a></dd><dt>Email</dt><dd><a href="mailto:jamiaululoom@gmail.com?subject=Career%20Enquiry">jamiaululoom@gmail.com</a></dd></dl>
<p>For teaching and administrative positions at the Banikuppa residential campus, see <a href="ResidentialSchoolBanikuppa/careers.html">Banikuppa Residential School Careers</a>.</p>'''

admissions = content_more.admissions

tailoring = content_more.tailoring

# 7. Bayanath.html: latest videos from the official YouTube channel. The cards are drawn in the browser by
#    portal-assets/bayanath.js from public/data/bayanath-videos.json, which tools/update_bayanath.py keeps fresh
#    (scheduled by .github/workflows/update-bayanath.yml).
YT_CHANNEL = 'https://www.youtube.com/@MuftiMaqsoodImran'
bayanath = ('<p class="eyebrow">Presentations</p><h1>Bayanath</h1><p class="lede">Latest Bayanath videos from the official YouTube channel, with the speaker\u2019s profile.</p>'
            + speaker.background()
            + '<div class="bz-grid">'
            + '<div class="bz-side">' + speaker.render() + '</div>'
            + '<div class="bz-main"><div class="bz-head"><p class="eyebrow">Latest videos</p><h2>Latest Bayanath videos</h2><p>The newest ten, with the most recent first.</p></div>'
            + f'<div data-bayanath data-src="data/bayanath-videos.json" data-channel="{YT_CHANNEL}">'
            '<p class="by-status" role="status">Loading the latest Bayanath videos…</p>'
            '<ul class="by-grid" aria-busy="true" aria-label="Latest Bayanath videos"></ul>'
            '<p class="by-meta"></p>'
            f'<p class="by-meta"><a href="{YT_CHANNEL}" target="_blank" rel="noopener">Watch all videos on the official YouTube channel ↗</a></p>'
            f'<noscript><p class="by-status">Please enable JavaScript to see the video list, or <a href="{YT_CHANNEL}" target="_blank" rel="noopener">open the official YouTube channel</a>.</p></noscript></div>'
            '</div></div>')


# 1b. Photographic sections under the hero (index.html only). All copy is taken from existing portal content.
def _inst(name):
    return next(inst_card(n, u, d) for n, u, d in INSTS if n == name)

FAC_TILES = [
    ('classroom.jpg', 'Classrooms', 'classroom.html', 'Students in a classroom at the Banikuppa campus'),
    ('computerlab.jpg', 'Computer laboratory', 'computerlab.html', 'Computer laboratory at the Banikuppa campus'),
    ('physicslab.jpg', 'Science laboratories', 'laboratories.html', 'Visitors and students in the science laboratory at the Banikuppa campus'),
    ('library.jpg', 'School library', 'library.html', 'The school library at the Banikuppa campus'),
    ('hostel.jpg', 'Hostel &amp; dining', 'hostel.html', 'The hostel building at the Banikuppa campus'),
    ('audi1.jpg', 'Auditorium &amp; Annual Day', 'annual.html', 'Students seated in the auditorium at the Banikuppa campus'),
]
EXPLORE = [
    ('Services', 'Educational, religious and social welfare services.', 'Services.html'),
    ('Activity Calendar', 'Competitions and events, June to January.', 'Activities.html'),
    ('About Us', 'Vision, history and the Founder Secretary’s essays.', 'AboutUs.html'),
    ('Recognitions', 'Letters of appreciation and recognitions.', 'Recognitions.html'),
    ('Admissions', 'Applications across all 14 institutions.', 'Admissions.html'),
    ('Contact', 'Telephone directory and address.', 'Contact.html'),
]
fac_html = ''.join(
    f'<li class="pf-tile"><a href="{SCHOOL}{u}">{fit_media("", fn, alt, "pf-media")}<span class="pf-cap"><strong>{t}</strong><small>Banikuppa campus</small></span></a></li>'
    for fn, t, u, alt in FAC_TILES)
explore_html = ''.join(f'<li><a class="pf-link" href="{u}"><strong>{t}</strong><span>{d}</span><i aria-hidden="true">→</i></a></li>' for t, d, u in EXPLORE)
SCHOOL_FEATURE = f"""<div class="pf-feature pf-reveal">
  {fit_media("", "slide5.jpg", "The school building at the Banikuppa residential campus", "pf-media pf-feature-media", "lazy")}
  <div class="pf-feature-copy"><p class="eyebrow">Residential school</p><h2>Boys Residential Higher &amp; Primary School, Banikuppa</h2>
  <p>A residential campus 26 km from Bangalore City on the Bangalore–Mysore four-lane highway, reachable in 35–40 minutes from City Market.</p>
  <div class="button-row"><a class="button" href="{SCHOOL}index.html">Explore Residential School <span aria-hidden="true">→</span></a><a class="button button-secondary" href="{SCHOOL}facilities.html">Campus facilities</a></div></div>
</div>"""

EMBLEM = f"""<aside class="pf-emblem pf-reveal" aria-label="Trust at a glance"><img src="{IMG_REL}logon.jpg" alt="Emblem of Jamia Masjid &amp; Muslim Charitable Fund Trust" width="188" height="188" loading="lazy" decoding="async">
  <dl><div><dt>Trust established</dt><dd>1939*</dd></div><div><dt>Institutions</dt><dd>14</dd></div><div><dt>Campus</dt><dd>City Market</dd></div></dl><p class="rc-emblem-note">*Year as given on the Trust’s Institution page; other pages of this website give other years. See <a href="AboutUs.html">About Us</a>.</p></aside>"""
prayer_html = ''.join(f'<li><strong>{n}</strong>{t}</li>' for n, t in PRAYERS)
announcement_html = ''.join(f'<li><a href="{u}">{escape(a)}</a></li>' for a, u in ANNOUNCEMENTS)

INDEX_SECTIONS = f"""
<section class="pf-section">{bg_photo("slide6.jpg","right")}<div class="container pf-intro">
  <div class="pf-reveal"><p class="eyebrow">About Jame-ul-Uloom</p><h2>Center of Knowledge, in the heart of Bangalore</h2>
  <p>Jame-ul-Uloom is an Arabic name meaning <em>“Center of Knowledge”</em>. Housed on the campus of Jamia Mosque—one of the largest mosques in the state, situated in the heart of Bangalore City at City Market—the institution pairs academic education with character building through moral and religious instruction.</p>
  <p>Dedicated to the upliftment of underserved students in the minority community, Jame-ul-Uloom prepares capable, ethical citizens equipped to succeed in a competitive world through a network of 14 constituent educational institutions ranging from nursery and primary schools to degree colleges and technical institutes.</p>
  <p>Operating under the aegis of Jamia Masjid, the institution combines modern secular curricula with religious and moral education in the light of the Holy Quran and Hadith, supported by a dedicated faculty that includes qualified teachers, Hufaz, and Moulvies.</p>
  <p>Every class from L.K.G. through Pre-University (PUC) includes a daily Arabic teaching period on all working days. Each Thursday during the final two periods, a religious congregation (<em>ijtima</em>) is conducted for girl students, and separate after-hours arrangements are provided for adult education under a qualified instructor.</p></div>
  {EMBLEM}
</div></section>
<section class="pf-section pf-tint">{bg_photo("houses.jpg","left")}<div class="container">
  <div class="pf-head pf-reveal"><p class="eyebrow">Our institutions</p><h2>Schools, colleges and training centres</h2><p>A selection from the Trust’s directory of 14 institutions.</p></div>
  <ul class="pf-grid pf-stagger">{_inst('Boys Residential Higher & Primary School, Banikuppa')}{_inst('Pre University College for Girls')}{_inst('Degree College for Girls (B.Com)')}{_inst('Industrial Training Institute (ITI)')}{_inst('MMI-NCPUL Computer Centre')}{_inst('Shoba-e-Hifz')}</ul>
  <p class="pf-more pf-reveal"><a class="button" href="Institutions.html">View all 14 institutions <span aria-hidden="true">→</span></a></p>
</div></section>
<section class="pf-section">{bg_photo("slide3.jpg","right")}<div class="container">
  <div class="pf-head pf-reveal"><p class="eyebrow">Campus and learning facilities</p><h2>Learning at the Banikuppa residential campus</h2><p>Classrooms, laboratories, library, hostel and sports, as photographed at our residential school.</p></div>
  <ul class="pf-tiles pf-stagger">{fac_html}</ul>
  <p class="pf-more pf-reveal"><a class="text-link" href="Transport.html">Transport &amp; campus facilities →</a></p>
</div></section>
<section class="pf-section"><div class="container">{SCHOOL_FEATURE}</div></section>
<section class="pf-section"><div class="container">
  <div class="pf-head pf-reveal" id="masjid"><p class="eyebrow">Jamia Masjid</p><h2>Prayer timings, notices and announcements</h2><p>Jamia Masjid is one of the largest mosques in the state, on S.J.P. Road at City Market. Enquiries: <a href="tel:0822239495">0822239495</a> · <a href="Contact.html">Contact directory</a>.</p></div>
  <ul class="times">{prayer_html}</ul>
  <h3>Announcements &amp; notices</h3>
  <ol class="ann">{announcement_html}</ol>
</div></section>
<section class="pf-section pf-tint"><div class="container">
  <div class="pf-head pf-reveal"><p class="eyebrow">Further exploration</p><h2>Find what you need</h2></div>
  <ul class="pf-links pf-stagger">{explore_html}</ul>
</div></section>
"""

# Awards & Recognition photographs: rendered ONLY from genuine files listed in tools/recognitions.json
# ([{"file": "name.jpg", "caption": "...", "alt": "..."}], images in public/portal-assets/recognitions/). Absent file = no gallery.
import json
_rec = Path(__file__).resolve().parent / 'recognitions.json'
if _rec.exists():
    _items = []
    for it in json.loads(_rec.read_text(encoding='utf-8')):
        fp = ASSETS / 'recognitions' / it['file']
        if not fp.exists(): continue
        w, h = image_size(fp)
        src = f'portal-assets/recognitions/{escape(it["file"], quote=True)}'
        alt = escape(it.get('alt') or it.get('caption') or '', quote=True)
        role = f'<span class="rg-role">{escape(it["role"])}</span>' if it.get('role') else ''
        date = f'<span class="rg-date">{escape(it["date"])}</span>' if it.get('date') else ''
        _items.append(
            f'<li class="rg-item"><figure class="rg-card">'
            f'<a class="rg-photo" href="{src}" target="_blank" rel="noopener" aria-label="Open full-size image: {escape(it.get("caption") or "", quote=True)}">'
            f'<img src="{src}" alt="{alt}" width="{w}" height="{h}" loading="lazy" decoding="async"></a>'
            f'<figcaption><strong class="rg-name">{escape(it.get("caption") or "")}</strong>{role}'
            f'<span class="rg-more">{date}<a class="rg-open" href="{src}" target="_blank" rel="noopener">View full size <span aria-hidden="true">↗</span></a></span></figcaption>'
            f'</figure></li>')
    if _items:
        recognitions += ('<section class="rg-panel" aria-labelledby="rg-title"><div class="rg-head"><p class="rg-eyebrow">Gallery</p>'
                         '<h2 id="rg-title">Letters of Appreciation</h2>'
                         '<p>Messages of goodwill and appreciation received from public figures and educationists, most dated early February 2011. Hover, focus or tap a card for details.</p></div>'
                         '<ul class="rg-grid">' + ''.join(_items) + '</ul></section>')

PAGES = [
    ('index.html', 'Welcome', index_hero, 'Jame-ul-Uloom, Jamia Masjid, Bangalore — overview, prayer timings, announcements and institutions.'),
    ('Institutions.html', 'Institutions', institutions, 'All 14 educational institutions of the Jamia Masjid & Muslim Charitable Fund Trust.'),
    ('Activities.html', 'Extra-Curricular Activities & Calendar', activities, 'Extra-curricular competitions and annual activity calendar from June to January.'),
    ('Services.html', 'Services', services, 'Educational and community services of Jame-ul-Uloom in English and Urdu.'),
    ('Recognitions.html', 'Awards & Recognition', recognitions, 'Awards, recognitions, and institutional achievements of Jame-ul-Uloom.'),
    ('ScienceLabs.html', 'Science Laboratories', sciencelabs, 'Science laboratories at Jame-ul-Uloom PU College for Girls and High Schools.'),
    ('Transport.html', 'Transport & Facilities', transport, 'Transport and campus facilities across the Jame-ul-Uloom Group of Institutions.'),
    ('Bayanath.html', 'Bayanath', bayanath, 'Latest Bayanath videos from the official YouTube channel, and the speaker profile.'),
    ('Contact.html', 'Contact', contact, 'Central departmental telephone directory and address for Jame-ul-Uloom.'),
    ('Careers.html', 'Careers', careers, 'Career enquiries at Jame-ul-Uloom, Jamia Masjid, Bangalore.'),
    ('Admissions.html', 'Admissions', admissions, 'Admissions information across the 14 institutions of Jame-ul-Uloom.'),
    ('Tailoring.html', 'Tailoring School for Women', tailoring, 'Jame-ul-Uloom Tailoring School for Women at Jamia Masjid, Bangalore.'),
]
PAGES += [(fn, t, b, d) for fn, (t, b, d) in {**content_main.ROOT, **content_more.ROOT_MORE}.items()]


for fn, t, b, d in PAGES:
    (PUB / fn).write_text(page(fn, t, b, d), encoding='utf-8')

# The old portal page (public/home.html) was removed on purpose. index.html is the only homepage.
# Delete any leftover copy from an older build, and refuse to continue if a page named home.html is ever added to PAGES.
assert 'home.html' not in [fn for fn, *_ in PAGES], 'public/home.html is the removed portal page; do not recreate it'
(PUB / 'home.html').unlink(missing_ok=True)

# 8. Sibling institutional sections (content: tools/content_inst.py).  Each page is wrapped in the same eyebrow / h1 / subnav / prose
#    structure as before; headings get ids so that legacy URLs can redirect to a section (e.g. Facilities.html#library).
SIBLINGS = content_inst.SIBLINGS

def slug(text):
    t = re.sub(r'<[^>]+>', '', text)
    t = re.sub(r'&[a-z]+;', ' ', t)
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')

def add_heading_ids(html):
    seen = set(re.findall(r'id="([^"]+)"', html))
    def sub(m):
        tag, text = m.group(1), m.group(2)
        i = slug(text)
        if not i or i in seen: return m.group(0)
        seen.add(i)
        return f'<{tag} id="{i}">{text}</{tag}>'
    return re.sub(r'<(h[23])>(.*?)</\1>', sub, html, flags=re.S)

sib_count = 0
for folder, meta in SIBLINGS.items():
    sub_dir = PUB / folder
    sub_dir.mkdir(parents=True, exist_ok=True)
    subnav = '<div class="subnav">' + ''.join(f'<a href="{escape(u, quote=True)}">{escape(lbl)}</a>' for lbl, u in meta['nav']) + '</div>'
    for fn, (pg_title, pg_html) in meta['pages'].items():
        body = f'<p class="eyebrow">{escape(meta["name"])}</p><h1>{escape(pg_title)}</h1>{subnav}<div class="prose rc-prose rc-wideprose">{add_heading_ids(pg_html)}</div>'
        (sub_dir / fn).write_text(page(fn, pg_title, body, f'{pg_title} — {NAME}', root_prefix='../'), encoding='utf-8')
        sib_count += 1
# Files left by an earlier build that are no longer part of a section (Phase 8 pages with invented text, or pages now merged) are removed
for folder, meta in SIBLINGS.items():
    for f in (PUB / folder).glob('*.html'):
        if f.name not in meta['pages']: f.unlink()
# Phase 8 files that carried invented text are replaced by redirects (and must not linger from an earlier build)
for rel in content_inst.REMOVE:
    (PUB / rel).unlink(missing_ok=True)

# Legacy URLs of the original site -> current pages. Netlify/Cloudflare `_redirects` and an Apache root `.htaccess` carry the same rules.
REDIRECTS = dict(content_inst.REDIRECTS)
REDIRECTS.update({'Caligraphy.html': 'Calligraphy.html'})
for old, new in REDIRECTS.items():
    target = new.split('#')[0]
    assert (PUB / target).exists(), f'redirect {old} -> {new}: target page missing'
    assert not ((PUB / old).exists()), f'redirect source {old} still exists as a file'
RB, RE = '# BEGIN phase9-redirects (generated by tools/generate_portal.py)', '# END phase9-redirects'
lines = [RB] + [f'/{o} /{n} 301' for o, n in sorted(REDIRECTS.items())] + [RE]
red = (PUB / '_redirects').read_text(encoding='utf-8')
if RB in red: red = red[:red.index(RB)] + red[red.index(RE) + len(RE) + 1:]
(PUB / '_redirects').write_text(red.rstrip('\n') + '\n\n' + '\n'.join(lines) + '\n', encoding='utf-8')
ht = ['# Root routing for jameululoom.org (generated by tools/generate_portal.py). Security headers and the Residential School rules live in',
      '# ResidentialSchoolBanikuppa/.htaccess; this file only carries the legacy-URL redirects of the earlier site address.',
      'Options -Indexes', '',
      '<IfModule mod_headers.c>', '  # Ask search engines not to list photographs of pupils and staff in image search (same policy as the Residential School)',
      '  <FilesMatch "\\.(jpe?g|png|gif|webp)$">', '    Header set X-Robots-Tag "noimageindex"', '  </FilesMatch>', '</IfModule>', '',
      '<IfModule mod_rewrite.c>', 'RewriteEngine On', 'RewriteBase /', 'RewriteRule ^home(\\.html)?/?$ / [R=301,L]']
for o, n in sorted(REDIRECTS.items()):
    dest = n.split('#')
    ht.append(f'RewriteRule ^{re.escape(o).replace("&", "&")}$ /{dest[0]}' + (f'#{dest[1]}' if len(dest) > 1 else '') + ' [R=301,L,NE]')
ht += ['</IfModule>', '']
(PUB / '.htaccess').write_text('\n'.join(ht), encoding='utf-8')

hdr = re.split(r'\n\s*# Privacy', (PUB / '_headers').read_text(encoding='utf-8'))[0]   # drop any earlier generated block, then write it again
HB = '# Privacy: keep photographs of pupils and staff out of image search (generated by tools/generate_portal.py)'
(PUB / '_headers').write_text(hdr.rstrip('\n') + f'\n\n{HB}\n/portal-assets/images/*\n  X-Robots-Tag: noimageindex\n', encoding='utf-8')

(ASSETS / 'portal.css').write_text(''.join((UI / f).read_text(encoding='utf-8') for f in ('base.css', 'extras.css', 'recovered.css')), encoding='utf-8')
for _f in ('app.js', 'theme-init.js', 'bayanath.js', 'bayanath.css'):
    shutil.copyfile(UI / _f, ASSETS / _f)
(ASSETS / 'speaker').mkdir(exist_ok=True)
shutil.copyfile(speaker.PHOTO_DIR / speaker.load()['photo']['file'], ASSETS / 'speaker' / speaker.load()['photo']['file'])  # the owner-supplied photograph, byte for byte
shutil.copyfile(speaker.PATTERN, ASSETS / 'speaker' / 'pattern.svg')
print(f'Generated {len(PAGES)} root portal pages and {sib_count} sibling institutional pages; {len(REDIRECTS)} legacy redirects')
