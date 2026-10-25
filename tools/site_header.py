"""The ONE site header, shared by every generator.

The homepage header (logo, ten-item menu, Facilities/Contact dropdowns, theme toggle, mobile drawer) is defined here
and nowhere else.  generate_portal.py (root + sibling-institution pages) and generate_site.py (Residential School
pages) both call site_header(), so the markup can never drift apart.

    site_header(rp, current=None, home_href=None)

rp         path from the page to the site root: '' for root pages, '../' for pages one folder down.
current    the NAV target to mark aria-current="page" (e.g. 'Bayanath.html').
home_href  override for the logo and the "Home" item.  The Residential School passes '/', so both always land on
           the official root homepage.
"""
from html import escape

IMG_REL = 'ResidentialSchoolBanikuppa/assets/images/'

NAV = [
    ('Home', 'index.html'),
    ('About', [('About Us', 'AboutUs.html'), ('Chairmen’s Messages', 'Message.html'), ('Governing Body', 'Team.html'), ('Trustees', 'Trustees.html'),
               ('Jamia Masjid', 'Masjid.html'), ('Services', 'Services.html'), ('Recognitions', 'Recognitions.html')]),
    ('Institutions', 'Institutions.html'),
    ('Residential School', 'ResidentialSchoolBanikuppa/index.html'),
    ('Activities', 'Activities.html'),
    ('Facilities', [('Transport & Facilities', 'Transport.html'), ('Smart Classrooms', 'Classroom.html'), ('Science Laboratories', 'ScienceLabs.html'),
                    ('Computer Laboratory', 'ComputerLab.html'), ('Library', 'Library.html'), ('Auditorium', 'Auditorium.html'), ('Sports', 'Sports.html'),
                    ('Calligraphy Centre', 'Calligraphy.html'), ('Tailoring School', 'Tailoring.html')]),
    ('Bayanath', 'Bayanath.html'),
    ('Admissions', [('Admissions', 'Admissions.html'), ('Admissions Diary 2013–14', 'AdmissionsDiary.html')]),
    ('Contact', [('Contact directory', 'Contact.html'), ('Careers', 'Careers.html')]),
]

ICON_SUN = '<svg class="sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"></circle><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"></path></svg>'
ICON_MOON = '<svg class="moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 14.3A8.5 8.5 0 0 1 9.7 3.5 8.5 8.5 0 1 0 20.5 14.3Z"></path></svg>'


def _link(u, label, rp, current, home_href):
    href = home_href if (u == 'index.html' and home_href) else f'{rp}{u}'
    cur = ' aria-current="page"' if current == u else ''
    return f'<a href="{href}"{cur}>{escape(label)}</a>'


def nav_html(rp, current=None, home_href=None, drawer=False):
    """Desktop bar and phone drawer share the same NAV list; only the wrapper markup differs."""
    out = []
    for label, target in NAV:
        if isinstance(target, str):
            out.append(_link(target, label, rp, current, home_href))
            continue
        sub = ''.join(_link(u, l, rp, current, home_href) for l, u in target)
        if drawer:
            out.append(f'<details><summary>{escape(label)} <span aria-hidden="true">＋</span></summary><div>{sub}</div></details>')
        else:
            out.append(f'<details class="nav-group"><summary>{escape(label)}</summary><div class="drop-menu">{sub}</div></details>')
    return ''.join(out)


def logo_brand(rp, home_href=None):
    """Header logo: complete crest + wordmark (logo1.png, 675x180) as a plain link to the homepage."""
    return (f'<a class="brand brand-logo" href="{home_href or rp + "index.html"}" aria-label="Jame ul uloom, Jamia Masjid, Bangalore — home">'
            f'<img src="{rp}{IMG_REL}logo1.png" alt="Jame ul uloom — An heritage of excellence" width="675" height="180" decoding="async"></a>')


def site_header(rp, current=None, home_href=None):
    return (f'<a class="skip-link" href="#main">Skip to content</a><header class="site-header"><div class="container nav-shell">{logo_brand(rp, home_href)}'
            f'<nav class="desktop-nav" aria-label="Primary">{nav_html(rp, current, home_href)}</nav>'
            f'<button class="icon-button theme-toggle" type="button" data-theme-toggle aria-label="Switch color theme">{ICON_SUN}{ICON_MOON}</button>'
            f'<button class="icon-button menu-toggle" type="button" data-menu-open aria-label="Open menu"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"></path></svg></button></div></header>'
            f'<dialog class="mobile-drawer" id="mobile-drawer"><div class="drawer-head"><strong>Explore Jame-ul-Uloom</strong><button class="icon-button" type="button" data-menu-close aria-label="Close menu">×</button></div>'
            f'<nav class="drawer-nav" aria-label="Mobile primary">{nav_html(rp, current, home_href, drawer=True)}</nav></dialog>')
