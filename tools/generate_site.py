"""Generator for the Jame Ul Uloom Residential School static website.

Layout of this project
  public/   the deployable website (HTML, assets/, sitemap.xml, robots.txt, _headers ...)
  tools/    this generator + the archived legacy pages it reads (never published)

Run:  pip install -r tools/requirements.txt && python tools/build.py
Optional: SITE_URL=https://your-domain.example python tools/build.py   (used for absolute og:image URLs, sitemap.xml, robots.txt)

All file names are matched case-insensitively against what is really on disk, and every
emitted reference uses the exact on-disk case, so the site also works on case-sensitive hosts.
"""
from pathlib import Path
from bs4 import BeautifulSoup
from html import escape
import json, os, re, struct, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_header import site_header  # the single shared header (also used by generate_portal.py)

TOOLS = Path(__file__).resolve().parent
PROJECT = TOOLS.parent
PUB = PROJECT / 'public'
SRC = TOOLS / 'source-html'
IMG = PUB / 'ResidentialSchoolBanikuppa' / 'assets' / 'images'
OUT = PUB / 'ResidentialSchoolBanikuppa'
BASE_PATH = '/ResidentialSchoolBanikuppa/'
PARENT_HOME = '/'                     # the official root homepage of the whole website
PARENT_INSTITUTIONS = '../Institutions.html'
SCHOOL = 'Jame Ul Uloom Residential School, Banikuppa'
# Production origin (set via the SITE_URL environment variable). Empty by default: og:image stays a relative path
# and sitemap.xml is not written, because the sitemap protocol requires absolute URLs on your real domain.
SITE_URL = os.environ.get('SITE_URL', 'https://jameululoom.org/ResidentialSchoolBanikuppa').rstrip('/')

# ---- case-safe file resolution -------------------------------------------------
IMG_MAP = {p.name.lower(): p.name for p in IMG.iterdir() if p.is_file()}
SRC_MAP = {p.name.lower(): p for p in SRC.glob('*.html')}

def real_img(name):
    """Return the on-disk file name for an image reference of any case, or None."""
    return IMG_MAP.get(Path(str(name).replace('\\', '/')).name.lower())

def image_size(path):
    """(width, height) read from the PNG/GIF/JPEG header using only the standard library."""
    with open(path, 'rb') as f:
        head = f.read(32)
        if head[:8] == b'\x89PNG\r\n\x1a\n':
            return struct.unpack('>II', head[16:24])
        if head[:6] in (b'GIF87a', b'GIF89a'):
            return struct.unpack('<HH', head[6:10])
        if head[:2] == b'\xff\xd8':
            f.seek(2)
            while True:
                b = f.read(1)
                while b and b != b'\xff': b = f.read(1)
                while b == b'\xff': b = f.read(1)
                if not b: break
                m = b[0]
                if m in (0xD8, 0x01) or 0xD0 <= m <= 0xD7: continue
                seg = f.read(2)
                if len(seg) < 2: break
                n = struct.unpack('>H', seg)[0]
                if 0xC0 <= m <= 0xCF and m not in (0xC4, 0xC8, 0xCC):
                    data = f.read(5)
                    h, w = struct.unpack('>HH', data[1:5])
                    return w, h
                f.seek(n - 2, 1)
    raise ValueError('cannot read image size: %s' % path)

def img_meta(name):
    real = real_img(name)
    if not real: return None
    w, h = image_size(IMG / real)
    return real, w, h

def og_url(name):
    return f'{SITE_URL}/assets/images/{real_img(name) or "slide2.jpg"}'.lstrip('/')

SMALL_W = 330  # sources narrower than this are never scaled up (avoids soft/pixelated enlargement)

# Friendly captions carried over unchanged from the supplied gallery (keyed by lower-case file name).
DISPLAY_NAMES = {
 "5.gif": "Sports preview animation", "5.jpg": "About us icon", "activities.jpg": "Activities icon",
 "artsclub.jpg": "Arts Club", "audi1.jpg": "Auditorium — view 1", "audi2.jpg": "Auditorium — view 2",
 "audi3.jpg": "Auditorium — view 3", "audi4.jpg": "Auditorium — view 4",
 "biologylab.jpg": "Biology Lab", "chemistrylab.jpg": "Chemistry Lab", "classroom.jpg": "Classroom",
 "computerlab.jpg": "Computer Lab", "contact.jpg": "Contact icon", "dinninghall.jpg": "Dining hall",
 "dr.fayaz.jpg": "Dr. Fayaz", "facilities.gif": "Facilities preview animation", "facilities.jpg": "Facilities icon",
 "governing.jpeg": "Governing Body", "hostel.gif": "Hostel preview animation", "hostel.jpg": "Hostel",
 "houses.jpg": "School houses", "innerdinninghall.jpg": "Dining hall — inner view",
 "innerdinninghall1.jpg": "Dining hall — inner view 2", "library.jpg": "School library",
 "litraryclub.jpg": "Literary Club", "logo1.png": "School logo", "logon.jpg": "School crest",
 "masjid.jpg": "Campus masjid", "masjid1.jpg": "Campus masjid — view 2", "masjid2.jpg": "Campus masjid — view 3",
 "message9.jpeg": "Principal’s message (scanned letter)", "physicslab.jpg": "Physics Lab",
 "schoolbuilding.jpg": "School building", "scienceclub.jpg": "Science Club",
 "slide1.jpg": "Campus photograph 1", "slide2.jpg": "Campus photograph 2", "slide3.jpg": "Campus photograph 3",
 "slide4.jpg": "Campus photograph 4", "slide5.jpg": "Campus photograph 5", "slide6.jpg": "Campus photograph 6",
 "slide7.jpg": "Campus photograph 7", "sportsclub.jpg": "Sports Club", "sportsevent.jpg": "Sports event",
 "sportsevent1.jpg": "Sports event — view 2", "staff.jpg": "School staff", "trustees.jpg": "Trustees"
}
# Legacy UI graphics, menu icons and animated sidebar GIFs: kept on disk, never shown as photographs.
NON_PHOTO={'5.gif','5.jpg','activities.jpg','contact.jpg','facilities.jpg','facilities.gif','hostel.gif','logo1.png','logon.jpg',
 'fb.png','in.png','twitter.png','youtube.png','menubackimg.png','testimonials.png','labs.png','hostel.png','annualsports.png','chairmansmessage.png'}

# ---- Spelling / typography corrections applied to text carried over from the legacy pages ----
# (literal replacements; school names, people and facts are not changed)
FIXES = [
 ('Endeavor : Jame Masjid & Muslim Charitable Fund Trust a non profit Organization is','Endeavor: Jame Masjid & Muslim Charitable Fund Trust, a non-profit organization, is'),
 ('Over the years It has','Over the years it has'),
 ('educational institutions to create to the needs','educational institutions to cater to the needs'),
 ('affordability .','affordability.'),
 ('yet an other path Breaking venture of the jame masjid and Muslim charitable fund trust to creat world Class excellence and facilities in field of educational and cater','yet another path-breaking venture of the Jame Masjid and Muslim Charitable Fund Trust to create world-class excellence and facilities in the field of education and cater'),
 ('such Parents who','such parents who'),
 ('offering “ quality education and sports facilities at throw away price”','offering “quality education and sports facilities at throwaway price”'),
 ('Avail this opportunity and built the future','Avail this opportunity and build the future'),
 ('beyond the means of a quality .','beyond the means of a quality.'),
 ('The Ambiance : It','The Ambiance: It'),
 ('Bangalore –Mysore four lanes high way','Bangalore–Mysore four-lane highway'),
 ('environment which, makes learning','environment which makes learning'),
 ('an auditorium .','an auditorium.'),
 ('immense plaesure that','immense pleasure that'),
 ('Bannikuppa is out the a new Website.','Banikuppa is out with a new website.'),
 ('I HEAR , I FORGET','I HEAR, I FORGET'),
 ('lessons are complimented by','lessons are complemented by'),
 ('with out hang-ups','without hang-ups'),
 ('in the class room by using state of the art audio','in the classroom by using state-of-the-art audio'),
 ('the main stay of the 21st','the mainstay of the 21st'),
 ('an edge to our student.','an edge to our students.'),
 ('Class rooms','Classrooms'),
 ('CHemistry lab','Chemistry Lab'),
 ('Warden –in chief','Warden-in-chief'),
 ('supervision Of the house masters who planed co-curricular','supervision of the house masters who planned co-curricular'),
 ('Friday are used','Fridays are used'),
 ('poem recitation ,','poem recitation,'),
 ('quiz compititions','quiz competitions'),
 ('and the Successful students','and the successful students'),
 ('good behavior and cent percent. Attendance.','good behavior and cent percent attendance.'),
 ('volley ball','volleyball'),
 ('kabadi and Athletic events','kabaddi and athletic events'),
 ('also Participate in taluk','also participate in taluk'),
 ('Well qualified, dedicated, Attentive, zealous and well behaved.','Well-qualified, dedicated, attentive, zealous and well-behaved.'),
 ('A qualified Doctor and a full time pharmacist','A qualified doctor and a full-time pharmacist'),
 ('Ph:0822221151,0822239495','Ph: 0822221151, 0822239495'),
 ('[email protected]','jamiaululoom@gmail.com'),  # legacy e-mail obfuscation placeholder; same address as the footer
 ('Litrary','Literary'),
 ('Dinning','Dining'),
]
FIX_HITS = {}
def fix_text(t):
    for a,b in FIXES:
        if a in t:
            t=t.replace(a,b); FIX_HITS[a]=FIX_HITS.get(a,0)+1
    return t

def camel(t):
    """'ArtsClub' -> 'Arts Club', 'SportsEvent1' -> 'Sports Event 1' (caption text only, never file names)."""
    if re.search(r'[a-z][A-Z]',t):
        t=re.sub(r'(?<=[a-z])(?=[A-Z])',' ',t); t=re.sub(r'(?<=[A-Za-z])(?=\d)',' ',t)
    return t

PAGE_META={
'index.html':('Home','Boys Residential Higher & Primary School, Banikuppa. Explore the school, campus, learning, activities and facilities.','home.html'),
'home.html':('School Overview','An overview of Jame Ul Uloom Residential School, Banikuppa.','home.html'),
'annual.html':('Auditorium & Annual Day','The school auditorium and Annual Day photographs.','annual.html'),
'careers.html':('Careers','Career enquiries for Jame Ul Uloom Residential School, Banikuppa.','careers.html'),
'classroom.html':('Classrooms','Classroom learning and the school’s approach to teaching.','classroom.html'),
'clubs.html':('Clubs','Student clubs and co-curricular activities.','clubs.html'),
'computerlab.html':('Computer Laboratory','Computer education at Jame Ul Uloom Residential School.','computerlab.html'),
'contact.html':('Contact Us','School contact information and address.','contact.html'),
'hostel.html':('Hostel & Dining','Residential accommodation and dining facilities.','hostel.html'),
'laboratories.html':('Science Laboratories','Chemistry, Physics and Biology laboratory photographs and descriptions.','laboratories.html'),
'library.html':('School Library','The school library and learning resources.','library.html'),
'masjid.html':('Campus Masjid','The campus masjid.','masjid.html'),
'medicalfacility.html':('Medical Facility','Medical care and student health support on campus.','medicalfacility.html'),
'message.html':('Principal’s Message','The Principal’s message to students and parents.','message.html'),
'sports.html':('Co-Curricular Activities & Sports','School houses, co-curricular activities and sports.','sports.html'),
'staff.html':('Staff','Information about the school staff.','staff.html'),
'team.html':('Governing Body','The governing body of the institution.','team.html'),
'trustees.html':('Trustees','The trustees of the institution.','trustees.html'),
}
def theme_boot():
 return '<script src="assets/js/theme-init.js"></script>'

def header(current):
 """The Residential School uses the homepage header unchanged (tools/site_header.py).  The logo and Home item
 point at '/' (the official root homepage) instead of the school's own index.html."""
 return site_header('../',current='ResidentialSchoolBanikuppa/index.html',home_href=PARENT_HOME)

def footer():
 return _footer_html().replace('@@H@@',PARENT_HOME).replace('@@I@@',PARENT_INSTITUTIONS)

def _footer_html():
 return '''<footer class="site-footer"><div class="container"><div class="footer-grid"><div class="footer-brand"><img src="assets/images/logo1.png" alt="Jame Ul Uloom" width="675" height="180"><p>Boys Residential Higher &amp; Primary School, Banikuppa. A Jame Masjid &amp; Muslim Charitable Fund Trust institution.</p></div><div><h2>Explore</h2><a href="about.html">About</a><a href="home.html">School overview</a><a href="facilities.html">Facilities</a><a href="activities.html">Activities</a><a href="gallery.html">Gallery</a></div><div><h2>People</h2><a href="team.html">Governing Body</a><a href="trustees.html">Trustees</a><a href="staff.html">Staff</a><a href="message.html">Principal’s Message</a><a href="careers.html">Careers</a></div><div><h2>Contact</h2><a href="tel:0822221151">0822221151</a><a href="tel:0822239495">0822239495</a><a href="mailto:jamiaululoom@gmail.com">jamiaululoom@gmail.com</a><a href="contact.html">S.J.P Road, City Market, Bangalore – 560002</a></div><div><h2>Jame-ul-Uloom</h2><a href="@@H@@">Jame-ul-Uloom home</a><a href="@@I@@">All institutions</a></div></div><div class="footer-bottom"><span>Copyright © <span data-current-year></span> Jame Ul Uloom. All rights reserved.</span><span>Jame Ul Uloom Residential School, Banikuppa. <a href="privacy.html">Privacy &amp; photo use</a></span></div></div></footer><button class="icon-button back-top" type="button" aria-label="Back to top" title="Back to top"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 14 6-6 6 6"></path></svg></button>'''

def lightbox():
 return '''<dialog class="lightbox" id="lightbox" aria-label="Image preview"><div class="lightbox-toolbar"><button class="icon-button" type="button" data-lightbox-close aria-label="Close image preview">×</button></div><div class="lightbox-stage"><button class="lightbox-nav prev" type="button" data-lightbox-prev aria-label="Previous image">‹</button><img data-lightbox-image src="assets/images/slide2.jpg" alt=""><button class="lightbox-nav next" type="button" data-lightbox-next aria-label="Next image">›</button></div><div class="lightbox-caption"><strong data-lightbox-title></strong><span data-lightbox-meta></span></div></dialog>'''

def layout(filename,title,desc,body,og='slide2.jpg',base=False):
 base_tag=f'<base href="{BASE_PATH}">' if base else ''
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">{base_tag}<title>{escape(title)} | {SCHOOL}</title><meta name="description" content="{escape(desc,quote=True)}"><meta property="og:type" content="website"><meta property="og:title" content="{escape(title,quote=True)} | {SCHOOL}"><meta property="og:description" content="{escape(desc,quote=True)}"><meta property="og:image" content="{escape(og_url(og),quote=True)}"><meta name="theme-color" content="#123c2e">{theme_boot()}<link rel="stylesheet" href="assets/css/styles.css"></head><body>{header(filename)}<main id="main">{body}</main>{footer()}{lightbox()}<script src="assets/js/app.js" defer></script></body></html>'''

def img_button(src,alt,title=None):
 m=img_meta(src)
 if not m: return ''
 real,w,h=m
 title=title or alt
 cls='media-frame'+(' is-portrait' if h>w else '')+(' is-small' if w<SMALL_W else '')
 return f'<figure class="legacy-photo reveal"><button class="{cls}" type="button" data-lightbox="assets/images/{escape(real,quote=True)}" data-title="{escape(title,quote=True)}" data-alt="{escape(alt,quote=True)}" data-meta="School photograph"><img src="assets/images/{escape(real,quote=True)}" alt="{escape(alt,quote=True)}" width="{w}" height="{h}" loading="lazy" decoding="async"></button><figcaption>{escape(title)}</figcaption></figure>'

def photo_card(t,d,u,im):
 """Card with the whole photograph visible (never cropped); text sits below the image, not over it."""
 m=img_meta(im)
 media=''
 if m:
  real,w,h=m
  small=' is-small' if w<SMALL_W else ''
  media=f'<div class="card-media"><img class="fit-bg" src="assets/images/{escape(real,quote=True)}" alt="" aria-hidden="true" loading="lazy" decoding="async"><img class="fit{small}" src="assets/images/{escape(real,quote=True)}" alt="{escape(t,quote=True)}" width="{w}" height="{h}" loading="lazy" decoding="async"></div>'
 return f'<article class="card photo-card">{media}<div class="card-content"><h3>{escape(t)}</h3><p>{escape(d)}</p><a class="text-link" href="{u}">Explore <span aria-hidden="true">→</span></a></div></article>'

SKIP_IMAGES={'logo1.png','logon.jpg','5.jpg','activities.jpg','facilities.jpg','contact.jpg','fb.png','in.png','twitter.png','youtube.png'}

def extract_content(filename):
 f=SRC_MAP.get(filename.lower())
 if not f: return [],[]
 soup=BeautifulSoup(f.read_text(encoding='utf-8',errors='ignore'),'html.parser')
 main=soup.select_one('.common_divv_100') or soup.select_one('.middle_boddy_project_page') or soup.body
 if not main: return [],[]
 elements=[]; seen=set()
 # Legacy pages nest <p> inside <h2>/<h4> layout boxes; unwrap them so the text is body copy, not a giant heading.
 for h in main.find_all(['h2','h3','h4','h5','h6']):
  if h.find('p'): h.unwrap()
 # collect body content in document order; image and text content, skip legacy navigation/footer
 for el in main.find_all(['h1','h2','h3','h4','h5','h6','p','li','img','table','blockquote'],recursive=True):
  if el.name=='img':
   orig=el.get('src','').replace('\\','/').split('/')[-1]
   real=real_img(orig)
   if real and (real.lower() in SKIP_IMAGES or real.lower() in NON_PHOTO): continue
   if real and real not in seen:
    seen.add(real); elements.append(('img',real,fix_text(DISPLAY_NAMES.get(real.lower()) or el.get('alt') or camel(re.sub(r'[_-]',' ',Path(orig).stem)))))
  elif el.name=='table':
   rows=[]
   for tr in el.find_all('tr'):
    cells=[' '.join(c.stripped_strings) for c in tr.find_all(['th','td'])]
    if any(cells): rows.append(cells)
   if rows: elements.append(('table',[[fix_text(c) for c in r] for r in rows],''))
  else:
   # avoid descendants of another text element being repeated
   if el.find_parent(['p','li','h1','h2','h3','h4','h5','h6','blockquote']): continue
   text=' '.join(el.stripped_strings)
   text=re.sub(r'\s+',' ',text).strip()
   if not text or len(text)<2: continue
   if text.lower() in {'residential higher & primary school, banikuppa','residential primary & high school, banikuppa','boys residential higher & primary school, banikuppa'}: continue
   if len(text)>4000: text=text[:4000]
   a_tag=el.find('a',href=True)
   if a_tag and re.sub(r'\s+',' ',' '.join(a_tag.stripped_strings)).strip()==text:
    elements.append(('link',text,a_tag['href'].split('/')[-1].lower())); continue
   name=el.name
   if text.startswith('It gives me an immense'): name='blockquote'   # Principal's welcome note
   if name=='p' and text.startswith('The school is conscious about the fact') and filename.lower()=='library.html': continue  # legacy copy-paste of the Computer Lab paragraph
   elements.append(('text',name,fix_text(text)))
 # Capture content images assigned as background-image in the main content.
 for el in main.select('[style*="background"]'):
  style=el.get('style','')
  m=re.search(r'url\([\'"]?([^\)\'"]+)',style,re.I)
  if m:
   orig=m.group(1).replace('\\','/').split('/')[-1]
   real=real_img(orig)
   if real and real not in seen and real.lower() not in SKIP_IMAGES and real.lower() not in NON_PHOTO:
    seen.add(real); elements.append(('img',real,fix_text(DISPLAY_NAMES.get(real.lower()) or camel(re.sub(r'[_-]',' ',Path(orig).stem)))))
 return elements, sorted(seen)

def norm(t): return re.sub(r'[^a-z0-9]+',' ',t.lower()).strip()

def quote_html(b):
 m=re.search(r'\s(Mr\. Syed Hussain Sharief.*)$',b)
 if m:
  who=re.sub(r'\s*\(Principal\)',', Principal',m.group(1))
  return '<blockquote class="source-quote">'+escape(b[:m.start()])+'</blockquote><p class="source-attrib">— '+escape(who)+'</p>'
 return '<blockquote class="source-quote">'+escape(b)+'</blockquote>'

def page_body(title,section,lede,elements,source,extra_html=''):
 out=[f'<section class="page-hero"><div class="container reveal"><p class="crumbs"><a href="/">Home</a> / <a href="index.html">Residential School</a> / {escape(section)}</p><p class="eyebrow">{escape(section)}</p><h1>{escape(title)}</h1><p class="lede">{escape(lede)}</p></div></section>']
 text_count=0; images=[]; content=[]
 for kind,a,b in elements:
  if kind=='img': images.append((a,b)); continue
  if kind=='link':
   if b in PAGE_META:
    label='Read the Principal’s message' if b=='message.html' else a
    content.append(f'<p><a class="text-link" href="{escape(b,quote=True)}">{escape(label)} <span aria-hidden="true">→</span></a></p>')
   continue
  if kind=='text':
   tag=a if a in {'h1','h2','h3','h4','h5','h6','blockquote','li'} else 'p'
   if tag=='li': content.append(f'<p class="source-text">{escape(b)}</p>')
   elif tag=='blockquote': content.append(quote_html(b))
   elif tag in {'h1','h2','h3','h4','h5','h6'}:
    if norm(b) in norm(title): continue            # heading only repeats the page title
    content.append(f'<h2>{escape(b)}</h2>' if len(b)<=80 else f'<p>{escape(b)}</p>')
   else: content.append(f'<p>{escape(b)}</p>')
  elif kind=='table':
   rows=a
   content.append('<div class="table-wrap"><table>'+''.join('<tr>'+''.join('<td>'+escape(c)+'</td>' for c in row)+'</tr>' for row in rows)+'</table></div>')
 if content:
  out.append('<section class="section"><div class="container narrow source-copy reveal">'+''.join(content)+'</div></section>')
 if images:
  out.append('<section class="section section-soft"><div class="container"><div class="section-heading"><p class="eyebrow">Photographs</p><h2>School photographs</h2></div><div class="photo-grid'+(' single' if len(images)==1 else '')+' stagger">'+''.join(img_button(src,alt,alt) for src,alt in images)+'</div></div></section>')
 if extra_html: out.append(extra_html)
 return ''.join(out),images

def make_home():
 elems,_=extract_content('home.html')
 paras=[b for kind,a,b in elems if kind=='text' and a=='p']
 intro=paras[0] if paras else 'Jame-ul-uloom Residential School is an educational institution of Jame Masjid & Muslim Charitable Fund Trust.'
 ambiance=paras[1] if len(paras)>1 else 'A campus designed to support focused learning and residential school life.'
 slides=[f'assets/images/{real_img("slide%d.jpg"%i)}' for i in range(1,8)]
 w,h=image_size(IMG/real_img('slide2.jpg'))
 # Banner is shown in full (never cropped): text above, complete campus photograph below.
 hero=f'''<section class="hero"><div class="hero-backdrop" aria-hidden="true"><img class="is-active" src="{slides[1]}" alt="" decoding="async"><img src="{slides[2]}" alt="" decoding="async" loading="lazy"></div><div class="hero-copy container"><p class="eyebrow">Jame Masjid &amp; Muslim Charitable Fund Trust</p><h1>A heritage of learning.<br><em>A future of possibility.</em></h1><p class="hero-lede">Boys Residential Higher &amp; Primary School, Banikuppa</p><div class="button-row"><a class="button button-primary" href="about.html">Discover the school <span aria-hidden="true">→</span></a><a class="button button-secondary" href="contact.html">Contact the school</a></div></div><div class="hero-banner container"><button class="hero-media" type="button" data-lightbox="{slides[1]}" data-title="Campus photographs" data-alt="Campus photographs" data-meta="School photograph" aria-label="View this campus photograph full screen"><img class="is-active" data-hero-images="{','.join(slides)}" src="{slides[1]}" width="{w}" height="{h}" alt="Campus photographs" decoding="async"><img src="{slides[2]}" width="{w}" height="{h}" alt="" aria-hidden="true" decoding="async" loading="lazy"></button></div><div class="hero-bottom"><span>Residential education</span><span>Campus · Learning · Student life</span></div></section>'''
 welcome=next((b for k,a,b in elems if k=='text' and a=='blockquote'),'')
 welcome_html=(quote_html(welcome)+'<a class="text-link" href="message.html">Read more <span aria-hidden="true">→</span></a>') if welcome else ''
 about=f'''<section class="section"><div class="container split"><div class="reveal"><p class="eyebrow">The institution</p><h2>Education with purpose.</h2><p>{escape(intro)}</p><p>{escape(ambiance)}</p><a class="text-link" href="home.html">Read the school overview <span aria-hidden="true">→</span></a>{welcome_html}</div><div class="mosaic reveal">{img_button('SchoolBuilding.jpg','School building','The school building')}{img_button('slide4.jpg','School campus','Campus photograph')}</div></div></section>'''
 cards=[('Learning spaces','Classrooms, a library, computer education and science laboratories.','classroom.html','Classroom.jpg'),('Residential life','Hostel and dining facilities for students living away from home.','hostel.html','Hostel.jpg'),('Activities & sport','Co-curricular activities, house competitions, clubs and sports.','sports.html','SportsEvent.jpg'),('Campus masjid','Explore the campus masjid.','masjid.html','Masjid.jpg')]
 cardhtml='<div class="card-grid four stagger">'+''.join(photo_card(t,d,u,im) for t,d,u,im in cards)+'</div>'
 features=f'''<section class="section section-soft"><div class="container"><div class="section-heading reveal"><p class="eyebrow">Explore the campus</p><h2>Spaces for learning and growing.</h2><p>Explore the school’s facilities and activities through its pages and photographs.</p></div>{cardhtml}</div></section>'''
 photo_names=['slide1.jpg','slide2.jpg','slide3.jpg','slide4.jpg','slide5.jpg','slide6.jpg','slide7.jpg']
 gallery='<section class="section"><div class="container"><div class="section-heading reveal"><p class="eyebrow">The school in pictures</p><h2>Campus moments.</h2><p>Photographs of the campus and school life.</p></div><div class="featured-strip">'+''.join(img_button(n,'School photograph',Path(n).stem.replace('slide','Campus photograph ')) for n in photo_names[:4])+'</div><p class="center"><a class="button button-primary" href="gallery.html">View all photographs <span aria-hidden="true">→</span></a></p></div></section>'
 gm=img_meta('Governing.jpeg'); gw,gh=gm[1],gm[2]
 trust=f'<section class="section section-dark"><div class="container split"><div class="reveal"><p class="eyebrow">The trust</p><h2>Serving education across generations.</h2><p>Jame Masjid &amp; Muslim Charitable Fund Trust is a non-profit organization with educational institutions serving different sections of society.</p><a class="text-link" href="about.html">About the institution →</a></div><div class="trust-image reveal"><img src="assets/images/{gm[0]}" alt="Governing body of the institution" width="{gw}" height="{gh}" loading="lazy" decoding="async"></div></div></section>'
 contact='<section class="section"><div class="container contact-cta reveal"><div><p class="eyebrow">Get in touch</p><h2>Connect with the school.</h2><p>For contact information, use the details on the contact page.</p></div><a class="button button-primary" href="contact.html">Contact details <span aria-hidden="true">→</span></a></div></section>'
 return hero+about+features+gallery+trust+contact

def generated_overview(title,section,lede,links):
 body=f'<section class="page-hero"><div class="container reveal"><p class="crumbs"><a href="/">Home</a> / <a href="index.html">Residential School</a> / {escape(section)}</p><p class="eyebrow">{escape(section)}</p><h1>{escape(title)}</h1><p class="lede">{escape(lede)}</p></div></section><section class="section"><div class="container"><div class="card-grid stagger">'
 for t,d,u,img in links:
  body+=photo_card(t,d,u,img)
 body+='</div></div></section>'
 return body

def make_gallery():
 files=sorted([p for p in IMG.iterdir() if p.is_file() and p.suffix.lower() in {'.jpg','.jpeg','.png','.gif','.webp'}],key=lambda p:p.name.lower())
 excluded=set(NON_PHOTO)  # icons, GIF sidebar previews and UI graphics are not photographs
 items=[]
 for p in files:
  if p.name.lower() in excluded: continue
  category='campus'
  low=p.name.lower()
  if any(k in low for k in ['lab','classroom','library','computer']): category='learning'
  elif any(k in low for k in ['sports','club','activities','houses']): category='activities'
  elif any(k in low for k in ['hostel','dinning','masjid','audi','facilities','medical']): category='facilities'
  elif any(k in low for k in ['staff','trustee','governing','message']): category='people'
  alt=fix_text(DISPLAY_NAMES.get(low) or re.sub(r'(?<!^)(?=[A-Z])',' ',p.stem).replace('_',' ').strip())
  w,h=image_size(p)
  items.append((p.name,alt,category,w,h))
 filters=[('all','All photographs'),('campus','Campus'),('learning','Learning'),('facilities','Facilities'),('activities','Activities'),('people','People')]
 body='<section class="page-hero"><div class="container reveal"><p class="crumbs"><a href="/">Home</a> / <a href="index.html">Residential School</a> / Gallery</p><p class="eyebrow">Photographs</p><h1>The school in pictures.</h1><p class="lede">A gallery of photographs of the campus and school life.</p></div></section><section class="section"><div class="container"><div class="gallery-filters" role="group" aria-label="Filter photographs">'+''.join(f'<button class="filter-button{" is-active" if i==0 else ""}" type="button" data-gallery-filter="{key}" aria-pressed="{"true" if i==0 else "false"}">{label}</button>' for i,(key,label) in enumerate(filters))+'</div><div class="gallery-grid stagger">'
 for fn,alt,cat,w,h in items:
  small=' class="is-small"' if w<SMALL_W else ''
  body+=f'<figure class="gallery-item" data-category="{cat}"><button type="button" data-lightbox="assets/images/{escape(fn,quote=True)}" data-title="{escape(alt,quote=True)}" data-alt="{escape(alt,quote=True)}" data-meta="School photograph"><img{small} src="assets/images/{escape(fn,quote=True)}" alt="{escape(alt,quote=True)}" width="{w}" height="{h}" loading="lazy" decoding="async"></button><figcaption><strong>{escape(alt)}</strong><span>{escape(cat.title())}</span></figcaption></figure>'
 body+='</div><p class="gallery-note">See our <a href="privacy.html">privacy &amp; photo-use notice</a> if you would like a photograph reviewed or removed.</p></div></section>'
 return body

GOVERNING=[('Maqbool Ahmed','President'),('Mohammed Ateeq Ahmed','Secretary'),('Syed Murtuza Husain @ Gufran','Vice President'),('Mohammed Athiulla Khan','Treasurer'),('Syed Noorul Ameen @ Anwer','Joint Secretary'),('Syed Abdul Gafoor','Internal Auditor')]
TRUSTEES=['Abbas Khan','Naveed Ahmed','Syed Sadaqath Peeran','J. Shafiulla','Moin Abdul Kareem','Zaheeruddin Ahmed','Mohammed Saifulla','L. Mohamed Farooq','Zafrulla Khan','Allah Bakash Khan','Ashfaq Ahmed','Allah Bakash','B. Md. Ghouse Qureshi','Syed Hussain','Mir Qamar Hussain','Abdulla Basha','Iqbal Ahmed']
LETTER=['It gives me immense pleasure to express that Jame-ul-uloom Boy’s Residential composite High School Bannikuppe is bringing out the magazine: Faizane Jame-ul-uloom 2010 for the first time',
 'I congratulate imparticular Mr. N. Majeed Basha, assistant master and Mr. Imran S, computer teacher for their day & night efforts to publish this magazine in flying colours in short time. The Staff members and students in grand for the success in their efforts in bringing out the magazine for the year 2010.',
 'School magazine provide a unique opportunity for the students to express their views feelings and experiences in different literary forms. Along with such writing it can also publish information for the benefit of personality development.']

def people_section(heading,note,items):
 lis=''.join('<li><strong>'+escape(n)+'</strong>'+('<span>'+escape(r)+'</span>' if r else '')+'</li>' for n,r in items)
 return f'<section class="section"><div class="container narrow source-copy reveal"><h2>{escape(heading)}</h2><p class="source-note">{escape(note)}</p><ul class="people-list">{lis}</ul></div></section>'

def extra_for(filename):
 if filename=='team.html': return people_section('Governing Body members','Names and designations as shown in the Governing Body image above.',GOVERNING)
 if filename=='trustees.html': return people_section('Trustees','Names as shown in the Trustees image above.',[(n,'') for n in TRUSTEES])
 if filename=='library.html':
  return '<section class="section"><div class="container narrow source-copy reveal"><h2>Computer education</h2><p>The school is conscious about the fact that computer education and information technology is the main stay of the 21st millennium, a powerful tool for not only communication but also access of information and computer knowledge is useful in all aspects of human endeavor, hence the school has introduced computer education right from 1st standard to 10th standard to give an edge to our student.</p></div></section>'
 if filename=='message.html':
  return ('<section class="section"><div class="container narrow source-copy reveal"><h2>Text of the letter</h2><p class="source-note">From the school magazine Faizane Jame-ul-uloom 2010.</p>'
   +''.join(f'<p>{escape(x)}.</p>' if not x.endswith('.') else f'<p>{escape(x)}</p>' for x in LETTER)
   +'<p class="source-attrib">— Syed Hussain Sharief Saheb, Principal, JUBRHS</p>'
   +'</div></section>')
 return ''

def contact_cards(extra=''):
 return '<section class="section section-soft"><div class="container contact-list"><div class="contact-item"><span>Address</span><address>S.J.P Road, City Market, Bangalore – 560002</address></div><div class="contact-item"><span>Phone</span><a href="tel:0822221151">0822221151</a><a href="tel:0822239495">0822239495</a></div><div class="contact-item"><span>Email</span><a href="mailto:jamiaululoom@gmail.com">jamiaululoom@gmail.com</a></div>'+extra+'</div></section>'

def make_clubs(title,section,lede,elements):
 hero=page_body(title,section,lede,[],'clubs.html')[0]
 cards=[]; images=[]; pending=None
 for kind,a,b in elements:
  if kind=='text' and a.startswith('h') and norm(b)!=norm(title): pending=b
  elif kind=='img':
   images.append((a,b)); label=pending or b
   cards.append('<div class="club-card"><h2>'+escape(label)+'</h2>'+re.sub(r'<figcaption>.*?</figcaption>','',img_button(a,label,label))+'</div>'); pending=None
 return hero+'<section class="section"><div class="container"><div class="club-grid stagger">'+''.join(cards)+'</div></div></section>',images

# Generate pages from source content, preserving extracted text and original image assets.
source_pages=[]
for filename,(title,desc,srcfile) in PAGE_META.items():
 if filename in {'index.html','home.html'}: continue
 elements,imgs=extract_content(srcfile)
 section= 'School' if filename in {'careers.html','contact.html'} else ('About' if filename in {'team.html','trustees.html','staff.html','message.html'} else ('Learning' if filename in {'classroom.html','computerlab.html','laboratories.html','library.html'} else ('Activities' if filename in {'annual.html','sports.html','clubs.html'} else 'Campus')))
 if filename=='clubs.html': body,shown=make_clubs(title,section,desc,elements)
 elif filename in {'contact.html','careers.html'}: body,shown=page_body(title,section,desc,[e for e in elements if e[0]!='text'],srcfile)   # details are shown once, as structured cards
 else: body,shown=page_body(title,section,desc,elements,srcfile,extra_for(filename))
 if filename=='contact.html':
  # Contact details as published in the archived source (shown once, as structured cards).
  body+=contact_cards('<div class="contact-item"><span>Campus</span><address>26 km from Bangalore city on the Bangalore–Mysore highway, reachable in 35 to 40 minutes from City Market (as described on the school overview page).</address></div><div class="contact-item"><span>Trust directory</span><a href="../Contact.html">All Jame-ul-Uloom departments and numbers</a></div>')
 if filename=='careers.html': body+=contact_cards()+'<section class="section"><div class="container source-panel"><h2>Career enquiries</h2><p>For career enquiries, use the school email address given on the contact page.</p><a class="button button-primary" href="mailto:jamiaululoom@gmail.com?subject=Careers%20enquiry">Email the school</a></div></section>'
 if filename=='annual.html' and not shown:
  body+='<section class="section"><div class="container photo-grid">'+''.join(img_button(f'audi{i}.jpg',f'Auditorium photograph {i}') for i in range(1,5))+'</div></section>'
 pagehtml=layout(filename,title,desc,body, next((im[0] for im in shown), 'slide2.jpg'))
 (OUT/filename).write_text(pagehtml,encoding='utf-8')
 source_pages.append({'page':filename,'source':srcfile,'title':title,'extracted_images':[i[0] for i in shown],'text_elements':sum(1 for e in elements if e[0]=='text')})

(OUT/'index.html').write_text(layout('index.html','Home','Jame Ul Uloom Residential School, Banikuppa',make_home()),encoding='utf-8')
_home_elems=extract_content('home.html')[0]+[('img',real_img('SchoolBuilding.jpg'),DISPLAY_NAMES['schoolbuilding.jpg'])]
(OUT/'home.html').write_text(layout('home.html','School Overview',PAGE_META['home.html'][1],page_body('School Overview','About',PAGE_META['home.html'][1],_home_elems,'home.html')[0],og='schoolbuilding.jpg'),encoding='utf-8')

# Cohesive category landing pages, linked to the original pages.
aboutlinks=[('School overview','The institutional overview and campus introduction.','home.html','SchoolBuilding.jpg'),('Governing Body','The governing body of the institution.','team.html','Governing.jpeg'),('Trustees','The trustees of the institution.','trustees.html','Trustees.jpg'),('Staff','The school staff.','staff.html','Staff.jpg'),('Principal’s Message','The Principal’s message.','message.html','Message9.jpeg')]
(OUT/'about.html').write_text(layout('about.html','About the School','Institutional overview and school leadership pages.',generated_overview('About the school','About','Explore the school overview and the people and trust pages.',aboutlinks)),encoding='utf-8')
academics=[('Classrooms','The school’s classroom teaching approach.','classroom.html','Classroom.jpg'),('Science Laboratories','Chemistry, Physics and Biology laboratories.','laboratories.html','ChemistryLab.jpg'),('Computer Laboratory','Computer education.','computerlab.html','ComputerLab.jpg'),('Library','The school library.','library.html','Library.jpg')]
(OUT/'academics.html').write_text(layout('academics.html','Learning & Academics','Learning spaces and educational facilities.',generated_overview('Learning & academics','Learning','Explore the school’s learning spaces.',academics)),encoding='utf-8')
activities=[('Annual Day & Auditorium','Auditorium photographs from the Annual page.','annual.html','audi4.jpg'),('Sports','Sports and co-curricular activities.','sports.html','SportsEvent.jpg'),('Clubs','Student clubs.','clubs.html','ScienceClub.jpg')]
(OUT/'activities.html').write_text(layout('activities.html','Activities','Sports, clubs, and annual school events.',generated_overview('Activities & student life','Activities','Explore annual events, sports and student clubs.',activities)),encoding='utf-8')
facilities=[('Classrooms','Teaching and learning spaces.','classroom.html','Classroom.jpg'),('Science Laboratories','Science practicals and laboratories.','laboratories.html','BiologyLab.jpg'),('Computer Lab','Computer education.','computerlab.html','ComputerLab.jpg'),('Library','Library facilities.','library.html','Library.jpg'),('Hostel & Dining','Residential facilities and dining.','hostel.html','Hostel.jpg'),('Campus Masjid','The campus masjid.','masjid.html','Masjid.jpg'),('Medical Facility','Medical support on campus.','medicalfacility.html','Dr.Fayaz.jpg')]
(OUT/'facilities.html').write_text(layout('facilities.html','Campus & Facilities','Campus and school facilities.',generated_overview('Campus & facilities','Campus','Explore the school’s facilities.',facilities)),encoding='utf-8')
(OUT/'gallery.html').write_text(layout('gallery.html','Gallery','Photographs from Jame Ul Uloom Residential School, Banikuppa.',make_gallery()),encoding='utf-8')

# ---- Privacy & photo-use notice ------------------------------------------------------------
def make_privacy():
 sections=[
  ('Why photographs appear on this website','This website uses photographs of the campus, classrooms, hostel, activities and the people of Jame Ul Uloom Residential School, Banikuppa, to show visitors what school life is like. Some photographs show pupils, teachers, staff, trustees and members of the governing body.'),
  ('Pupils','Photographs on this site do not carry pupils’ names. We ask that visitors do not copy, edit, redistribute or use photographs of pupils for any purpose other than viewing them on this website.'),
  ('Asking for a photograph to be reviewed or removed','If you appear in a photograph, or you are the parent or guardian of a pupil who does, and you would like it reviewed, replaced or removed, please contact the school using the details below. Please tell us which page the photograph is on. We will review the request promptly and remove the photograph from this website where requested.'),
  ('Information we collect','This website has no forms, accounts, comments, analytics or advertising. It does not ask you for personal information, and it does not set tracking cookies. The only item saved in your browser is your light/dark display preference, which stays on your own device. If you contact the school by telephone or email, the school will use the details you give only to respond to you.'),
  ('Search engines and sharing','We ask search engines not to list the photographs in this website in their image search results. We cannot control copies that other people make or share.'),
 ]
 body='<section class="page-hero"><div class="container reveal"><p class="crumbs"><a href="/">Home</a> / <a href="index.html">Residential School</a> / Privacy</p><p class="eyebrow">Privacy</p><h1>Privacy &amp; photo use</h1><p class="lede">How this website uses photographs of pupils and staff, and how to ask for one to be reviewed or removed.</p></div></section><section class="section"><div class="container narrow source-copy reveal">'
 body+=''.join(f'<h2>{escape(h)}</h2><p>{escape(p)}</p>' for h,p in sections)
 body+='<h2>Contact</h2><p>Jame Ul Uloom Residential School, S.J.P Road, City Market, Bangalore – 560002.</p><p><a class="text-link" href="mailto:jamiaululoom@gmail.com?subject=Photograph%20review%20request">jamiaululoom@gmail.com</a> · <a class="text-link" href="tel:0822221151">0822221151</a> · <a class="text-link" href="tel:0822239495">0822239495</a></p></div></section>'
 return body

(OUT/'privacy.html').write_text(layout('privacy.html','Privacy & Photo Use','How this website uses photographs of pupils and staff, and how to request review or removal of a photograph.',make_privacy()),encoding='utf-8')

# ---- 404 page (served by the host for unknown URLs; <base href="/"> keeps assets working from any path) ----
_nf='<section class="page-hero"><div class="container reveal"><p class="eyebrow">404</p><h1>Page not found</h1><p class="lede">The page you were looking for does not exist or has moved.</p><div class="button-row"><a class="button button-primary" href="index.html">Go to the home page</a><a class="button button-secondary" href="gallery.html">View the gallery</a></div></div></section>'
(OUT/'404.html').write_text(layout('404.html','Page not found','The page you were looking for does not exist.',_nf,base=True),encoding='utf-8')

# ---- Reports (kept in tools/, never published) ---------------------------------------------
all_images=sorted([p for p in IMG.iterdir() if p.is_file() and p.suffix.lower() in {'.jpg','.jpeg','.png','.gif','.webp'}],key=lambda p:p.name.lower())
source_html=sorted(SRC.glob('*.html'))
report={
 'project':SCHOOL,
 'generated_at':'2026-10-17',
 'source_html_pages_archived':len(source_html),
 'source_pages_rendered':len(PAGE_META),
 'additional_landing_pages_generated':['about.html','academics.html','activities.html','facilities.html','gallery.html','privacy.html','404.html'],
 'image_files_in_assets':len(all_images),
 'source_pages':source_pages,
 'asset_inventory':[{'filename':p.name,'bytes':p.stat().st_size,'extension':p.suffix.lower()} for p in all_images],
 'notes':['All original HTML pages remain available in tools/source-html/.','Images referenced in archived page content were mapped when their filenames existed in public/assets/images/ (matched case-insensitively; emitted with the exact on-disk case).','The archive alone does not prove completeness against the live site; compare against the live site before claiming every remote asset has been recovered.','Legacy social icons and some tiny decorative assets remain in assets/images/ but are excluded from the photo gallery.']
}
(TOOLS/'migration-report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
(TOOLS/'MIGRATION-REPORT.md').write_text('# Website migration report\n\n- Archived source HTML pages: **%d**\n- Original image files in assets: **%d**\n- Generated source-based pages: **%d**\n- Additional landing pages: **5** (about, academics, activities, facilities, gallery) plus privacy.html and 404.html\n\n## Important limitations\n\n- The source archive contains 18 original HTML pages. This build generates all 18 as modern pages, plus the landing/gallery/privacy/404 pages.\n- Image references found in the central content areas were mapped where the corresponding file exists in `public/assets/images/`.\n- This report reflects the supplied ZIP, not a live-server crawl. It cannot certify that every image or page on the live website has been captured.\n- Original source pages are retained under `tools/source-html/` for traceability.\n\n## Generated pages\n\n' % (len(source_html),len(all_images),len(PAGE_META)-2) + ''.join(f'- `{f}` — {t}\n' for f,(t,_,_) in PAGE_META.items()) + '- `about.html` — About landing page\n- `academics.html` — Learning landing page\n- `activities.html` — Activities landing page\n- `facilities.html` — Facilities landing page\n- `gallery.html` — Photo gallery\n- `privacy.html` — Privacy & photo-use notice\n- `404.html` — Not-found page\n',encoding='utf-8')

# ---- sitemap.xml (absolute URLs, as the sitemap protocol requires) and robots.txt ----------
urls=sorted(p.name for p in OUT.glob('*.html') if p.name!='404.html')
if SITE_URL:
    (OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{escape(SITE_URL+"/"+("" if u=="index.html" else u))}</loc></url>\n' for u in urls)+'</urlset>\n',encoding='utf-8')
    (OUT/'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n',encoding='utf-8')
else:
    (OUT/'robots.txt').write_text('User-agent: *\nAllow: /\n',encoding='utf-8')
# ---- legacy case-sensitive URLs -> current lowercase files (Apache .htaccess block + Cloudflare/Netlify _redirects) ----
legacy_pages={}; legacy_imgs={}
for f in SRC.glob('*.html'):
 t=f.read_text(encoding='utf-8',errors='ignore')
 for m in re.finditer(r'(?:href|src)="([^"#?]+)"',t):
  n=m.group(1).replace('\\','/')
  if re.fullmatch(r'[A-Za-z0-9_]+\.html',n) and n!=n.lower() and (OUT/n.lower()).exists(): legacy_pages[n]=n.lower()
  mm=re.fullmatch(r'images/([^/]+)',n)
  if mm and real_img(mm.group(1)) and real_img(mm.group(1))!=mm.group(1): legacy_imgs[mm.group(1)]=real_img(mm.group(1))
lp=TOOLS/'legacy-image-names.txt'      # original image names recorded in the audit (CSS background images are not visible in the HTML)
if lp.exists():
 for n in lp.read_text().split():
  if real_img(n) and real_img(n)!=n: legacy_imgs[n]=real_img(n)
# Phase 9: two original pages that only repeated the school overview text (no content of their own) now point at the matching pages.
legacy_pages.update({'DiningHall.html': 'facilities.html', 'co-curricular.html': 'activities.html'})
legacy_pages={k:v for k,v in sorted(legacy_pages.items())}; legacy_imgs={k:v for k,v in sorted(legacy_imgs.items())}
BEGIN,END='# BEGIN legacy-redirects (generated)','# END legacy-redirects'
rules=[BEGIN,'<IfModule mod_rewrite.c>','RewriteEngine On','RewriteBase '+BASE_PATH]
rules+=[f'RewriteRule ^{re.escape(k)}$ {v} [R=301,L]' for k,v in legacy_pages.items()]
rules+=[f'RewriteRule ^images/{re.escape(k)}$ assets/images/{v} [R=301,L]' for k,v in legacy_imgs.items()]
rules+=['</IfModule>',END]
ht=(OUT/'.htaccess').read_text(encoding='utf-8')
if BEGIN in ht: ht=ht[:ht.index(BEGIN)]+'\n'.join(rules)+ht[ht.index(END)+len(END):]
else: ht=ht.rstrip('\n')+'\n\n'+'\n'.join(rules)+'\n'
(OUT/'.htaccess').write_text(ht,encoding='utf-8')
# The old portal/home page was removed. Force (!) the redirect so it applies even if a stale file is ever deployed.
# These rules match only the ROOT paths; /ResidentialSchoolBanikuppa/home.html (the school overview) is a different, valid page.
red=['# Removed portal/home page -> the single official homepage (generated by tools/generate_site.py)',
     '/home        /  301!',
     '/home/       /  301!',
     '/home.html   /  301!',
     '',
     '# Mixed-case URLs of the Banikuppa school site (generated by tools/generate_site.py)']
red+=[f'{BASE_PATH}{k} {BASE_PATH}{v} 301' for k,v in legacy_pages.items()]
red+=[f'{BASE_PATH}images/{k} {BASE_PATH}assets/images/{v} 301' for k,v in legacy_imgs.items()]
(PUB/'_redirects').write_text('\n'.join(red)+'\n',encoding='utf-8')
print('legacy redirects:',len(legacy_pages),'pages,',len(legacy_imgs),'images')
unused=[a for a,_ in FIXES if a not in FIX_HITS]
if unused: print('WARNING unused text fixes:',unused)
print(f'Generated {len(urls)+1} HTML pages; {len(all_images)} image assets; source pages {len(source_html)}; SITE_URL={SITE_URL}')
