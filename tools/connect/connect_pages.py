"""Contact, Feedback, Admissions and Careers pages (the "connect" pages).

Every fact on these pages comes from the existing site (the Contact directory, the Admissions pages of each institution and
the 2013-14 school diary) or from the owner's printed flyer and Contact page. Nothing is invented: where a detail is not
published (current fees, dates, vacancies, office hours) the page says so and points to the office.

The pages are plain HTML with real inputs. forms.js (progressive enhancement) adds the step-by-step feedback journey,
the star rating, copy buttons and the fetch() submit to the forms service (serverless/forms-worker/, address in forms-config.json).
Until that address is set a form hands the visitor's answers to their own email program (mailto) and says only that: nothing is ever reported as sent.
Choices, field names and rules come from forms-schema.json, the same file the service validates against
(tools/tests/test_connect.py and test_forms_worker.py check this).
"""
import json
import re
from html import escape
from pathlib import Path
from urllib.parse import urlsplit

HERE = Path(__file__).resolve().parent
SCHEMA = json.loads((HERE / 'forms-schema.json').read_text(encoding='utf-8'))
CONFIG = json.loads((HERE / 'forms-config.json').read_text(encoding='utf-8'))

ADDRESS = 'Jamia Masjid & Muslim Charitable Fund Trust, S.J.P. Road, City Market, Bangalore – 560002'
EMAIL = 'jamiaululoom@gmail.com'
MAPS = 'https://www.google.com/maps/search/?api=1&query=Jamia+Masjid+City+Market+Bangalore+560002'


def _endpoint(value):
    """'' (not set up yet) or a plain https address: no credentials, no query, no fragment."""
    if value == '':
        return ''
    u = urlsplit(value)
    if (not isinstance(value, str) or u.scheme != 'https' or not u.hostname or u.username or u.password or u.query or u.fragment
            or re.search(r'[\s"\'<>]', value)):
        raise SystemExit(f'tools/connect/forms-config.json: endpoint must be empty or a plain https address, got {value!r}')
    return value


ENDPOINT = _endpoint(CONFIG.get('endpoint', ''))
ENDPOINT_ORIGIN = (lambda u: f'{u.scheme}://{u.netloc}' if ENDPOINT else '')(urlsplit(ENDPOINT))
# configured: post to the service. Not configured: a plain mail link for browsers without JavaScript, and a marker the script reads.
FORM_ATTRS = (f'action="{ENDPOINT}" method="post"' if ENDPOINT
              else f'action="mailto:{EMAIL}" method="post" enctype="text/plain" data-cx-offline')

# Numbers exactly as printed on the existing Contact page.
PHONES = [('Administrative Office', ['0822221165', '0822272086']), ('Secretary Saheb (cellar)', ['0822221725']), ('Boys Block', ['0822221726']), ('Jamia Masjid', ['0822239495']), ('Head Mistress', ['0822221156']), ('Maqsood Imran Saheb', ['0822221151']), ('P.U College', ['0826705591', '0826705486']), ('B.C.A', ['0826709915']), ('JUU Computer Section', ['0822221161']), ('M.M.I NCPUL', ['0822221158'])]
MAIN_PHONES = ['0822221151', '0822239495']   # the two numbers printed with the address on the flyer and the Contact page

CHOICES = {name: [tuple(pair) for pair in pairs] for name, pairs in SCHEMA['choices'].items()}   # (value, label), from forms-schema.json

_P = {
    'pin': 'M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0c0 5.4-6.5 11-6.5 11ZM12 12.2a2.4 2.4 0 1 0 0-4.8 2.4 2.4 0 0 0 0 4.8Z',
    'phone': 'M5 4h3.5l1.8 4.6-2.3 1.5a11 11 0 0 0 5.4 5.4l1.5-2.3L19 15.5V19a1.5 1.5 0 0 1-1.6 1.5A15.5 15.5 0 0 1 3.5 5.6 1.5 1.5 0 0 1 5 4Z',
    'mail': 'M4 6.5h16v11H4ZM4.5 7l7.5 6 7.5-6',
    'copy': 'M9 9h10v11H9ZM5 15V4h10',
    'check': 'M5 12.5l4.5 4.5L19 7.5',
    'arrow': 'M5 12h14M13 6l6 6-6 6',
    'star': 'M12 3.4l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17.4 6.6 20.3l1-6.1-4.4-4.3 6.1-.9Z',
    'heart': 'M12 20.5S4 15.2 4 9.4A4.4 4.4 0 0 1 12 7a4.4 4.4 0 0 1 8 2.4c0 5.8-8 11.1-8 11.1Z',
    'chat': 'M4 5h16v11H9l-5 4Z',
    'book': 'M4 5.5C6.5 4.5 9.5 4.5 12 6c2.5-1.5 5.5-1.5 8-.5V19c-2.5-1-5.5-1-8 .5-2.5-1.5-5.5-1.5-8-.5ZM12 6v13.5',
    'cap': 'M2.5 9.5 12 5l9.5 4.5L12 14ZM6.5 11.7V16c0 1.2 2.5 2.5 5.5 2.5s5.5-1.3 5.5-2.5v-4.3',
    'wrench': 'M14.5 4.5a4.5 4.5 0 0 0-4.2 6.1L4 17l3 3 6.4-6.3a4.5 4.5 0 0 0 6.1-4.2l-3 3-2.5-.5-.5-2.5Z',
    'laptop': 'M5 6h14v9H5ZM2.5 18.5h19',
    'desk': 'M4 8h16v3H4ZM6 11v8M18 11v8M9 14.5h6',
    'home': 'M3 21h18M5 21V10l7-5 7 5v11M9 21v-6h6v6',
    'moon': 'M20.5 14.3A8.5 8.5 0 0 1 9.7 3.5 8.5 8.5 0 1 0 20.5 14.3Z',
    'user': 'M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8ZM4.5 20c0-3.6 3.4-6 7.5-6s7.5 2.4 7.5 6',
    'doc': 'M7 3.5h7l4 4V20.5H7ZM14 3.5V8h4M9.5 12.5h6M9.5 16h6',
    'search': 'M10.5 17a6.5 6.5 0 1 0 0-13 6.5 6.5 0 0 0 0 13ZM15.5 15.5 20 20',
    'compass': 'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18ZM15.5 8.5l-2 5-5 2 2-5Z',
}


def ic(name, cls='cx-ic'):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true"><path d="{_P[name]}"></path></svg>'


def bg():
    """The page's own aurora: four soft bands moved by CSS transform/opacity only (no script)."""
    return '<div class="cx-bg" aria-hidden="true"><span class="cx-au cx-au-a"><i></i></span><span class="cx-au cx-au-b"><i></i></span><span class="cx-au cx-au-c"><i></i></span><span class="cx-au cx-au-d"><i></i></span></div>'


def _head(eyebrow, h1, lede):
    return f'<p class="eyebrow">{eyebrow}</p><h1>{h1}</h1><p class="lede">{lede}</p>'


def _tel(n, cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<a{c} href="tel:{n}">{n}</a>'


# ---------------------------------------------------------------- form building blocks

def _hidden(form):
    return (f'<input type="hidden" name="form" value="{form}"><input type="hidden" name="opened" value="" data-cx-opened>'
            '<div class="cx-hp" aria-hidden="true"><label>Leave this empty<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>')


def _field(form, name, label, kind='text', req=False, ac='', maxlen=None, hint='', rows=5, mode=''):
    fid = f'{form}-{name}'
    desc = f'{fid}-e' + (f' {fid}-h' if hint else '')
    star = '<span class="cx-req" aria-hidden="true"> *</span>' if req else ''
    attrs = f' name="{name}" id="{fid}" placeholder=" " aria-describedby="{desc}"' + (' required' if req else '') + (f' autocomplete="{ac}"' if ac else '') + (f' maxlength="{maxlen}"' if maxlen else '') + (f' inputmode="{mode}"' if mode else '')
    if kind == 'textarea':
        ctl = f'<textarea{attrs} rows="{rows}"></textarea>'
    else:
        ctl = f'<input type="{kind}"{attrs}>'
    h = f'<p class="cx-hint" id="{fid}-h">{hint}</p>' if hint else ''
    return f'<div class="cx-field">{ctl}<label for="{fid}">{label}{star}</label><span class="cx-glow" aria-hidden="true"></span>{h}<p class="cx-err" id="{fid}-e" hidden></p></div>'


def _select(form, name, label, kind, req=False, blank='Choose one'):
    fid = f'{form}-{name}'
    opts = f'<option value="">{blank}</option>' + ''.join(f'<option value="{v}">{escape(t)}</option>' for v, t in CHOICES[kind])
    star = '<span class="cx-req" aria-hidden="true"> *</span>' if req else ''
    return (f'<div class="cx-field cx-select"><label for="{fid}">{label}{star}</label><select name="{name}" id="{fid}" aria-describedby="{fid}-e"{" required" if req else ""}>{opts}</select>'
            f'<span class="cx-glow" aria-hidden="true"></span><p class="cx-err" id="{fid}-e" hidden></p></div>')


def _chips(form, name, legend, kind, req=False, hint=''):
    star = '<span class="cx-req" aria-hidden="true"> *</span>' if req else ''
    chips = ''.join(f'<label class="cx-chip"><input type="radio" name="{name}" value="{v}"{" required" if req and i == 0 else ""}><span>{escape(t)}</span></label>' for i, (v, t) in enumerate(CHOICES[kind]))
    h = f'<p class="cx-hint">{hint}</p>' if hint else ''
    return f'<fieldset class="cx-chips" data-chips="{name}"><legend>{legend}{star}</legend>{h}<div class="cx-chip-row">{chips}</div><p class="cx-err" id="{form}-{name}-e" hidden></p></fieldset>'


def _consent(form, text):
    return (f'<div class="cx-check-wrap"><label class="cx-check"><input type="checkbox" name="consent" value="1" required aria-describedby="{form}-consent-e"><span class="cx-box" aria-hidden="true">{ic("check")}</span><span class="cx-check-text">{text}</span></label>'
            f'<p class="cx-err" id="{form}-consent-e" hidden></p></div>')


def _submit(label):
    return f'<button class="button cx-submit" type="submit"><span class="cx-submit-label">{label}</span><span class="cx-spin" aria-hidden="true"></span></button>'


def _form_tail(form, mail_subject):
    return (f'<div class="cx-banner" role="alert" hidden></div>'
            f'<p class="cx-fallback" hidden>If the form will not send, you can write to <a href="mailto:{EMAIL}?subject={mail_subject}">{EMAIL}</a> or call <a href="tel:{MAIN_PHONES[0]}">{MAIN_PHONES[0]}</a>.</p>'
            f'<p class="cx-fallback cx-handoff" role="status" hidden>Your email program should now be open with your message ready. Please press Send there to complete it. '
            f'If nothing opened, write to <a href="mailto:{EMAIL}?subject={mail_subject}">{EMAIL}</a> or call <a href="tel:{MAIN_PHONES[0]}">{MAIN_PHONES[0]}</a>.</p>')


# ---------------------------------------------------------------- Contact

def contact():
    def dept(d, ns):
        return (f'<li class="cx-card cx-dept" data-dept="{escape(d.lower())} {" ".join(ns)}"><h3>{escape(d)}</h3>'
                + ''.join(f'<p>{ic("phone")}{_tel(n)}</p>' for n in ns) + '</li>')
    paths = [
        ('chat', 'Share your thoughts', 'Tell us what we do well and where we can do better.', 'Feedback.html', 'Give feedback'),
        ('cap', 'Ask about admissions', 'Programmes, documents and a simple enquiry form.', 'Admissions.html', 'Begin an enquiry'),
        ('user', 'Join our team', 'Teaching, technical, Islamic studies and office roles.', 'Careers.html', 'See careers'),
        ('mail', 'Write to the office', 'Any other question: a short email is the quickest way.', f'mailto:{EMAIL}?subject=General%20enquiry', 'Send an email'),
    ]
    return (_head('Contact us', 'We’d love to hear from you', 'Visit, call or write. Whichever way you reach us, your message goes to the office of the Jamia Masjid &amp; Muslim Charitable Fund Trust.')
            + bg()
            + '<section class="cx-section" aria-labelledby="cx-reach"><h2 id="cx-reach" class="cx-sr">Ways to reach us</h2><div class="cx-grid cx-three">'
            + f'<article class="cx-card cx-glass cx-tilt"><span class="cx-badge">{ic("pin")}</span><h3>Visit us</h3><address>Jamia Masjid &amp; Muslim Charitable Fund Trust<br>S.J.P. Road, City Market<br>Bangalore – 560002</address>'
              f'<div class="cx-actions"><a class="button" href="{MAPS}" target="_blank" rel="noopener">{ic("compass")}Get directions<span class="cx-sr"> (opens Google Maps in a new tab)</span></a>'
              f'<button class="button button-secondary cx-copy" type="button" data-cx-copy="{escape(ADDRESS, quote=True)}" data-cx-what="Address" hidden>{ic("copy")}Copy address</button></div></article>'
            + f'<article class="cx-card cx-glass cx-tilt"><span class="cx-badge">{ic("phone")}</span><h3>Call us</h3><p class="cx-big">{_tel(MAIN_PHONES[0])}</p><p class="cx-big">{_tel(MAIN_PHONES[1])}</p>'
              f'<p class="cx-note">Tap a number to call. Direct lines for every department are listed below.</p><div class="cx-actions"><a class="button button-secondary" href="#cx-dir">{ic("search")}Find a department</a></div></article>'
            + f'<article class="cx-card cx-glass cx-tilt"><span class="cx-badge">{ic("mail")}</span><h3>Write to us</h3><p class="cx-big cx-email"><a href="mailto:{EMAIL}">{EMAIL}</a></p>'
              f'<p class="cx-note">We read every message that reaches this address.</p><div class="cx-actions"><a class="button" href="mailto:{EMAIL}">{ic("mail")}Send an email</a>'
              f'<button class="button button-secondary cx-copy" type="button" data-cx-copy="{EMAIL}" data-cx-what="Email address" hidden>{ic("copy")}Copy email</button></div></article>'
            + '</div></section>'
            + '<section class="cx-section" aria-labelledby="cx-help"><div class="cx-head"><p class="eyebrow">How can we help?</p><h2 id="cx-help">Choose where you’d like to begin</h2></div><ul class="cx-grid cx-four cx-paths">'
            + ''.join(f'<li><a class="cx-card cx-path" href="{h}"><span class="cx-badge cx-badge-sm">{ic(i)}</span><h3>{t}</h3><p>{d}</p><span class="cx-go">{b}{ic("arrow")}</span></a></li>' for i, t, d, h, b in paths)
            + '</ul></section>'
            + '<section class="cx-section" id="cx-dir" aria-labelledby="cx-dirh"><div class="cx-head"><p class="eyebrow">Telephone directory</p><h2 id="cx-dirh">Departments &amp; direct lines</h2>'
              '<p>Numbers are shown exactly as the institution prints them.</p></div>'
              f'<div class="cx-search" hidden><label class="cx-sr" for="cx-q">Search departments</label>{ic("search")}<input id="cx-q" type="search" placeholder="Search a department or number" autocomplete="off" data-cx-filter="#cx-depts"></div>'
              '<p class="cx-count" role="status" aria-live="polite" hidden></p>'
            + f'<ul class="cx-grid cx-depts" id="cx-depts">{"".join(dept(d, ns) for d, ns in PHONES)}</ul></section>'
            + '<section class="cx-section" aria-labelledby="cx-find"><div class="cx-find cx-glass"><div class="cx-find-art" aria-hidden="true"><span class="cx-ring cx-r1"></span><span class="cx-ring cx-r2"></span><span class="cx-ring cx-r3"></span>'
              f'<span class="cx-pin">{ic("pin")}</span></div><div class="cx-find-text"><p class="eyebrow">Find us</p><h2 id="cx-find">In the heart of Bangalore</h2>'
              '<p>Jame ul uloom is in the campus of Jamia Masjid on S.J.P. Road, beside City Market.</p>'
              '<p>Our Boys Residential School is on the Bangalore–Mysore highway, 26 km from the city. It can be reached in 35 to 40 minutes from City Market, as described on the school’s own pages.</p>'
              f'<div class="cx-actions"><a class="button" href="{MAPS}" target="_blank" rel="noopener">{ic("compass")}Open in Google Maps<span class="cx-sr"> (new tab)</span></a>'
              '<a class="button button-secondary" href="ResidentialSchoolBanikuppa/index.html">Visit the Residential School</a></div></div></div></section>'
            + '<p class="cx-toast" role="status" aria-live="polite"></p>')


# ---------------------------------------------------------------- Feedback

def feedback():
    steps = ['Rating', 'Topic', 'Thoughts', 'About you']
    prog = '<ol class="cx-progress" aria-label="Progress" hidden>' + ''.join(f'<li><span class="cx-dot" aria-hidden="true">{i + 1}</span><span class="cx-dot-l">{s}</span></li>' for i, s in enumerate(steps)) + '</ol>'
    stars = ''.join(f'<input type="radio" name="rating" id="fb-r{i}" value="{i}"{" required" if i == 1 else ""}><label for="fb-r{i}" class="cx-star" data-v="{i}"><span class="cx-sr">{i} out of 5</span>{ic("star", "cx-star-ic")}</label>' for i in range(1, 6))
    face = ('<svg class="cx-face" viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="21"></circle><circle class="cx-eye" cx="17" cy="20" r="2"></circle><circle class="cx-eye" cx="31" cy="20" r="2"></circle>'
            '<path class="cx-mouth" d="M15 30 Q24 30 33 30"></path></svg>')
    form = (f'<form class="cx-form cx-glass" id="cx-feedback-form" data-cx-form="feedback" data-no-motion {FORM_ATTRS} novalidate aria-labelledby="fb-title">'
            + _hidden('feedback')
            + '<div class="cx-form-head"><h2 id="fb-title">Share your feedback</h2><p>It takes about a minute. Only the first three questions are needed.</p></div>' + prog
            + '<fieldset class="cx-step" data-step="0"><legend>How has your experience with us been?</legend>'
              f'<div class="cx-rate"><div class="cx-stars" role="radiogroup" aria-label="Rating">{stars}</div><div class="cx-rate-out" aria-live="polite">{face}<span class="cx-rate-word" data-cx-word>Tap a star to rate</span></div></div>'
              '<p class="cx-err" id="feedback-rating-e" hidden></p></fieldset>'
            + '<fieldset class="cx-step" data-step="1"><legend>What would you like to talk about?</legend>'
            + _chips('feedback', 'category', 'Choose a topic', 'category', True) + _select('feedback', 'about', 'Which part of Jame ul uloom? (optional)', 'about', False, 'Choose one, or leave blank') + '</fieldset>'
            + '<fieldset class="cx-step" data-step="2"><legend>Tell us in your own words</legend>'
            + _field('feedback', 'message', 'Your thoughts', 'textarea', True, maxlen=2000, rows=6, hint='What did you enjoy? What could be better? There is no wrong answer.')
            + '<p class="cx-counter" aria-hidden="true"><span data-cx-count>0</span> / 2000</p></fieldset>'
            + '<fieldset class="cx-step" data-step="3"><legend>Who is sharing? <span class="cx-opt">(optional)</span></legend>'
            + _chips('feedback', 'audience', 'I am a…', 'audience', False)
            + '<div class="cx-two">' + _field('feedback', 'name', 'Your name', 'text', False, 'name', 80) + _field('feedback', 'email', 'Email, only if you would like a reply', 'email', False, 'email', 120) + '</div>'
              '<p class="cx-privacy">Your answers go to the office of the institution and are used only to read and respond to your feedback. We do not sell or share them.</p></fieldset>'
            + '<div class="cx-nav"><button class="button button-secondary cx-back" type="button" hidden>Back</button><button class="button cx-next" type="button" hidden>Continue' + ic('arrow') + '</button>' + _submit('Send my feedback').replace('class="button cx-submit"', 'class="button cx-submit cx-final"') + '</div>'
            + _form_tail('feedback', 'Feedback') + '</form>')
    success = ('<div class="cx-success cx-glass" data-cx-success="feedback" data-no-motion hidden tabindex="-1"><svg class="cx-seal" viewBox="0 0 96 96" aria-hidden="true"><circle class="cx-seal-ring" cx="48" cy="48" r="42"></circle><path class="cx-seal-heart" d="M48 70S27 56 27 41a11.5 11.5 0 0 1 21-6.5A11.5 11.5 0 0 1 69 41C69 56 48 70 48 70Z"></path></svg>'
               '<h2 data-cx-focus>Thank You for Being Part of Our Journey 💙</h2><p class="cx-sent">Thank you! Your message has been sent successfully.</p>'
               '<p class="cx-quote"><em>Your thoughts help us grow, improve, and serve our community better. We truly appreciate you taking the time to share them with us.</em></p>'
               '<p class="cx-ref-line" hidden>Reference <strong data-cx-ref></strong></p><div class="cx-actions"><a class="button" href="index.html">Back to the homepage</a><button class="button button-secondary cx-again" type="button">Share another thought</button></div></div>')
    side = ('<aside class="cx-side cx-glass"><p class="eyebrow">Why it matters</p><h2>A message from all of us</h2>'
            '<p>Students, parents, alumni, visitors and neighbours: you are all part of the Jame ul uloom family. Tell us what has made you proud, what could be better and what you hope we will do next.</p>'
            f'<ul class="cx-bullets"><li>{ic("heart")}<span>Appreciation helps our teachers and staff know their work is seen.</span></li><li>{ic("book")}<span>Suggestions help us improve classrooms, facilities and services.</span></li>'
            f'<li>{ic("mail")}<span>Add your email only if you would like a reply.</span></li></ul>'
            f'<p class="cx-note">Prefer to talk? Call <a href="tel:{MAIN_PHONES[0]}">{MAIN_PHONES[0]}</a> or see the <a href="Contact.html">contact page</a>.</p></aside>')
    return (_head('Feedback', 'Your Voice Matters. Your Thoughts Inspire Us.', 'Students, parents, alumni, visitors and our wider community: we would love to hear about your experience with Jame ul uloom.')
            + bg() + f'<div class="cx-fb">{side}<div class="cx-fb-main">{form}{success}</div></div>')


# ---------------------------------------------------------------- Admissions

def admissions():
    journey = [
        ('Choose', 'Pick the institution and the class or course. Each one has its own page with what the institution has published.'),
        ('Ask', 'Send the short enquiry below or call the office. Seats, dates and current fees are confirmed by the office, not on this website.'),
        ('Gather', 'Prepare the documents on the checklist. Colleges ask for attested or photocopies; originals are shown at admission.'),
        ('Apply', 'Colleges: fill the prescribed form in your own handwriting and hand it to the office during working hours before the last date. Schools: admission depends on seats in the class.'),
        ('Verify', 'The office checks the documents. Admissions to the Pre University College are provisional until approved by the P.U.C. board.'),
    ]
    steps = ''.join(f'<li class="cx-step-card"><span class="cx-num" aria-hidden="true">{i + 1}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(journey))
    panels = [
        ('schools', 'cap', 'Nursery, primary &amp; high school', 'English-medium school for girls and boys, attached to Jamia Masjid.',
         ['Open to both girls and boys; admission is made on the basis of seats in the particular class.', 'A birth certificate from the Corporation’s Chief Registrar of Births, with the child’s name entered, is required for pre-primary and above.',
          'A transfer certificate from the previous school, countersigned by the B.E.O. of the Education Department (children from other states: countersigned by the D.D.P.I. of that state or district).', 'Fees once paid are not refunded on any account.'],
         'AdmissionsDiary.html', 'Read the Admissions Diary 2013–14'),
        ('pu', 'book', 'Pre University College for Girls', 'A two-year pre-university course.',
         ['Open to candidates who have passed the Karnataka S.S.L.C. examination or an examination the board recognises as equivalent.', 'Part 1 languages: English (compulsory) and one of Urdu, Hindi or Kannada. Part 2: Physics, Chemistry, Maths, Biology; or Economics, Business Studies, Accountancy, Computer Science.',
          'The college page lists the fee structure it published. Please confirm the current fees with the office.'],
         'PUGirlsCollege/Admissions.html', 'See the PU College admissions page'),
        ('degree', 'desk', 'Degree College (B.Com) &amp; BCA', 'Degree courses for girls.',
         ['The prescribed application form is filled in your own handwriting and submitted to the office during working hours before the last date.', 'Attested or photocopies of the documents on the checklist must accompany the form.',
          'For fees and eligibility, please ask the college office (BCA office: 0826709915).'],
         'DegreeGirlsCollege/Admissions.html', 'See the Degree College page'),
        ('ncpul', 'laptop', 'MMI-NCPUL Computer Centre', 'A computer course of 1000 hours, from July to June.',
         ['Intake is 60 students a year, in two batches of 30. Each batch studies three hours a day: one and a half hours of theory and one and a half of practicals.', 'Modules cover information technology, business systems and web application development.'],
         'NCPUL/Admissions.html', 'See the course and fee details'),
        ('iti', 'wrench', 'Industrial Training Institute', 'NCVT trades of two years.',
         ['Trades: Fitter, MRAC (Mechanic Refrigeration &amp; Air Conditioning) and MMV (Mechanic Motor Vehicle), each of two years.', 'Eligibility: S.S.L.C. Seating capacity is 42 in each trade.', 'For admission dates and seats, please contact the institute office.'],
         'ITI/Admissions.html', 'See the ITI admissions page'),
    ]
    acc = ''.join(
        f'<details class="cx-acc cx-card"{" open" if i == 0 else ""}><summary><span class="cx-badge cx-badge-sm">{ic(icn)}</span><span class="cx-acc-t"><strong>{t}</strong><small>{s}</small></span><span class="cx-chev" aria-hidden="true">{ic("arrow")}</span></summary>'
        f'<div class="cx-acc-body"><ul class="cx-list">{"".join(f"<li>{x}</li>" for x in pts)}</ul><a class="cx-go" href="{href}">{lab}{ic("arrow")}</a></div></details>'
        for i, (k, icn, t, s, pts, href, lab) in enumerate(panels))

    def checklist(key, title, items):
        li = ''.join(f'<li><label class="cx-check"><input type="checkbox" data-cx-tick><span class="cx-box" aria-hidden="true">{ic("check")}</span><span class="cx-check-text">{x}</span></label></li>' for x in items)
        return (f'<div class="cx-card cx-glass cx-checklist" data-cx-list><h3>{title}</h3><div class="cx-meter" hidden><span class="cx-meter-bar"><i></i></span><span class="cx-meter-t" role="status" aria-live="polite"></span></div><ul>{li}</ul></div>')
    docs = ('<div class="cx-grid cx-two-col">'
            + checklist('c', 'Pre University, Degree &amp; BCA', ['Statement of marks of the qualifying examination', 'Transfer certificate from the institution last attended', 'Latest caste certificate (only for SC/ST/BC/BT students)', 'Migration certificate, if applicable', 'Six passport-size photographs and two stamp-size photographs'])
            + checklist('s', 'Nursery, primary &amp; high school', ['Birth certificate from the Corporation’s Chief Registrar of Births, with the child’s name', 'Transfer certificate countersigned by the B.E.O. (D.D.P.I. for other states), where the child has studied elsewhere'])
            + '</div><p class="cx-note">This checklist is only for your own use; nothing you tick is sent anywhere. Furnishing false documents or wrong information is a criminal offence, as the colleges state in their rules.</p>')
    form = (f'<form class="cx-form cx-glass" id="cx-admissions-form" data-cx-form="admissions" data-no-motion {FORM_ATTRS} novalidate aria-labelledby="ad-title">'
            + _hidden('admissions')
            + '<div class="cx-form-head"><h2 id="ad-title">Send an admissions enquiry</h2><p>This is an enquiry, not an application. The office will contact you to explain the next steps.</p></div>'
            + _chips('admissions', 'programme', 'Which programme are you asking about?', 'programme', True)
            + '<div class="cx-two">' + _field('admissions', 'level', 'Class or year you are asking about', 'text', False, '', 60) + _field('admissions', 'student', 'Student’s name', 'text', False, '', 80) + '</div>'
            + '<div class="cx-two">' + _field('admissions', 'guardian', 'Parent or guardian name', 'text', True, 'name', 80) + _field('admissions', 'phone', 'Phone number', 'tel', True, 'tel', 20, mode='tel') + '</div>'
            + _field('admissions', 'email', 'Email (optional)', 'email', False, 'email', 120)
            + _field('admissions', 'message', 'Anything you would like us to know (optional)', 'textarea', False, maxlen=1000, rows=4)
            + _consent('admissions', 'I agree that the office may contact me about this enquiry. My details are used for that purpose only.')
            + _submit('Send my enquiry') + _form_tail('admissions', 'Admissions%20enquiry') + '</form>')
    success = ('<div class="cx-success cx-glass" data-cx-success="admissions" data-no-motion hidden tabindex="-1"><svg class="cx-seal" viewBox="0 0 96 96" aria-hidden="true"><circle class="cx-seal-ring" cx="48" cy="48" r="42"></circle><path class="cx-seal-tick" d="M30 49l12 12 25-27"></path></svg>'
               '<h2 data-cx-focus>Thank you. Your enquiry has reached us.</h2><p class="cx-sent">Thank you! Your message has been sent successfully.</p><p class="cx-quote">The office will contact you on the number you gave. Please remember that this was an enquiry; it is not an application or a reserved seat.</p>'
               '<p class="cx-ref-line" hidden>Reference <strong data-cx-ref></strong></p><div class="cx-actions"><a class="button" href="index.html">Back to the homepage</a></div></div>')
    return (_head('Admissions', 'Every Great Journey Begins With a First Step.', 'Learn how admission works at each institution, see what to bring, and send us a simple enquiry. We are glad you are here.')
            + bg()
            + '<section class="cx-section" aria-labelledby="ad-j"><div class="cx-head"><p class="eyebrow">The journey</p><h2 id="ad-j">Five steps from curiosity to classroom</h2></div>'
              f'<ol class="cx-journey cx-grid">{steps}</ol></section>'
            + '<section class="cx-section" aria-labelledby="ad-p"><div class="cx-head"><p class="eyebrow">Programmes</p><h2 id="ad-p">What each institution publishes</h2>'
              '<p>Open a programme to see its published eligibility and requirements. Dates and current fees change from year to year, so please confirm them with the office.</p></div>'
              f'<div class="cx-accs">{acc}</div></section>'
            + f'<section class="cx-section" aria-labelledby="ad-d"><div class="cx-head"><p class="eyebrow">Documents</p><h2 id="ad-d">Gather what you need</h2></div>{docs}</section>'
            + f'<section class="cx-section cx-enquire" id="enquire" aria-labelledby="ad-title"><div class="cx-form-wrap">{form}{success}</div>'
              f'<aside class="cx-aside cx-glass"><p class="eyebrow">Prefer to talk?</p><h2>Call or visit the office</h2><p>S.J.P. Road, City Market, Bangalore – 560002</p><p class="cx-big">{_tel(MAIN_PHONES[0])}</p><p class="cx-big">{_tel(MAIN_PHONES[1])}</p>'
              f'<p class="cx-note">Each department’s direct line is on the <a href="Contact.html#cx-dir">contact page</a>.</p><a class="cx-go" href="Institutions.html">Browse all institutions{ic("arrow")}</a></aside></section>')


# ---------------------------------------------------------------- Careers

def careers():
    roles = [
        ('teaching-school', 'cap', 'Teaching: schools', 'Nursery, primary and high school classrooms.'),
        ('teaching-college', 'book', 'Teaching: colleges', 'Pre University, Degree and BCA colleges for girls.'),
        ('islamic', 'moon', 'Islamic studies &amp; Hifz', 'Shoba-e-Hifz, Shoba-e-Alimiyath and religious instruction.'),
        ('technical', 'wrench', 'Technical training', 'Instructors for the ITI trades.'),
        ('computer', 'laptop', 'Computer education', 'MMI-NCPUL and the computer laboratories.'),
        ('admin', 'desk', 'Administration &amp; office', 'Supporting the institutions behind the scenes.'),
        ('residential', 'home', 'Residential campus', 'Boys Residential School, Banikuppa.'),
        ('other', 'heart', 'Another way to contribute', 'Tell us how your skills could help.'),
    ]
    cards = ''.join(f'<li><button class="cx-card cx-role" type="button" data-cx-area="{v}"><span class="cx-badge cx-badge-sm">{ic(i)}</span><h3>{t}</h3><p>{d}</p><span class="cx-go">Express interest{ic("arrow")}</span></button></li>' for v, i, t, d in roles)
    form = (f'<form class="cx-form cx-glass" id="cx-careers-form" data-cx-form="careers" data-no-motion {FORM_ATTRS} novalidate aria-labelledby="cr-title">'
            + _hidden('careers')
            + '<div class="cx-form-head"><h2 id="cr-title">Tell us about yourself</h2><p>This is an expression of interest, not a job application. Please do not send certificates or identity numbers.</p></div>'
            + '<div class="cx-two">' + _field('careers', 'name', 'Your name', 'text', True, 'name', 80) + _select('careers', 'area', 'Area of interest', 'area', True) + '</div>'
            + '<div class="cx-two">' + _field('careers', 'phone', 'Phone number', 'tel', True, 'tel', 20, mode='tel') + _field('careers', 'email', 'Email', 'email', True, 'email', 120) + '</div>'
            + '<div class="cx-two">' + _field('careers', 'qualification', 'Qualification (optional)', 'text', False, '', 120) + _select('careers', 'experience', 'Experience (optional)', 'experience', False, 'Choose one, or leave blank') + '</div>'
            + _field('careers', 'message', 'A few words about you (optional)', 'textarea', False, maxlen=1500, rows=5, hint='Subjects you teach, skills you bring, or why you would like to be part of Jame ul uloom.')
            + _consent('careers', 'I agree that the office may contact me about opportunities. My details are used for that purpose only.')
            + _submit('Send my interest') + _form_tail('careers', 'Career%20enquiry') + '</form>')
    success = ('<div class="cx-success cx-glass" data-cx-success="careers" data-no-motion hidden tabindex="-1"><svg class="cx-seal" viewBox="0 0 96 96" aria-hidden="true"><circle class="cx-seal-ring" cx="48" cy="48" r="42"></circle><path class="cx-seal-tick" d="M30 49l12 12 25-27"></path></svg>'
               '<h2 data-cx-focus>Thank you for your interest.</h2><p class="cx-sent">Thank you! Your message has been sent successfully.</p><p class="cx-quote">Your details have reached the office. We cannot promise a reply to every enquiry, but we will get in touch if a suitable opportunity arises.</p>'
               '<p class="cx-ref-line" hidden>Reference <strong data-cx-ref></strong></p><div class="cx-actions"><a class="button" href="index.html">Back to the homepage</a></div></div>')
    why = [('heart', 'Work with purpose', 'The institution’s aim is the upliftment of the community and the building of character, alongside formal education.'),
           ('book', 'A place that has grown', 'Started in 1983-84 with two pupils in the basement of the masjid, the schools now teach around 3,500 pupils, according to the 2013–14 school diary.'),
           ('user', 'Many ways to serve', 'From classrooms and workshops to computer labs, the residential campus and the office, there are different ways to contribute.')]
    return (_head('Careers', 'Build Your Future. Make a Difference.', 'Jame ul uloom is a community institution that began with two pupils in the basement of the masjid and has grown into a family of schools and colleges. If you would like to help it grow further, we would like to hear from you.')
            + bg()
            + '<section class="cx-section" aria-labelledby="cr-why"><div class="cx-head"><p class="eyebrow">Why join us</p><h2 id="cr-why">Education that shapes character</h2></div><ul class="cx-grid cx-three cx-why">'
            + ''.join(f'<li class="cx-card cx-glass"><span class="cx-badge">{ic(i)}</span><h3>{t}</h3><p>{d}</p></li>' for i, t, d in why) + '</ul></section>'
            + '<section class="cx-section" aria-labelledby="cr-open"><div class="cx-status cx-glass" role="note"><span class="cx-pulse" aria-hidden="true"></span><div><h2 id="cr-open">Current openings</h2>'
              '<p>No specific vacancies are published on this website at the moment. We will not invent any. Tell us where you could contribute and the office will keep your details in mind.</p></div></div>'
              f'<div class="cx-head"><p class="eyebrow">Where you could contribute</p><h2>Choose an area</h2><p>Select a card to fill in your area of interest below.</p></div><ul class="cx-grid cx-four cx-roles">{cards}</ul></section>'
            + f'<section class="cx-section cx-enquire" id="interest" aria-labelledby="cr-title"><div class="cx-form-wrap">{form}{success}</div>'
              '<aside class="cx-aside cx-glass"><p class="eyebrow">What happens next</p><h2>Simple and respectful</h2>'
              f'<ol class="cx-mini"><li>Your details go to the office by email.</li><li>If a suitable opportunity arises, the office contacts you.</li><li>We do not ask for a résumé or certificates here.</li></ol>'
              f'<p class="cx-note">Residential campus roles: see <a href="ResidentialSchoolBanikuppa/careers.html">Banikuppa careers</a>. You can also write to <a href="mailto:{EMAIL}?subject=Career%20enquiry">{EMAIL}</a>.</p></aside></section>')
