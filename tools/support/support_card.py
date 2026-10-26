"""Renders the "Support Our Mission" card that is added at the end of About Us (AboutUs.html).

The bank details come from tools/support/support-details.json and nowhere else. They are printed ONLY when the file says
"verified": true AND every field is present and well formed; otherwise the card is drawn without any account details and points
to the office instead. Nothing is invented, and there is no payment gateway: the card shows the Trust's published bank details
so that a supporter can transfer from their own bank, and offers copy buttons (support.js)."""
import json
import re
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / 'support-details.json'

TITLE = 'Support Our Mission'
LEDE = ('Your support helps us continue our educational mission and serve our community. '
        'We are grateful for every contribution and every person who stands with us.')
FIELDS = (('account_name', 'Account name'), ('bank', 'Bank'), ('branch', 'Branch'), ('account_type', 'Account type'),
          ('account_number', 'Account number'), ('ifsc', 'IFSC code'))
IFSC = re.compile(r'^[A-Z]{4}0[A-Z0-9]{6}$')
ACCOUNT = re.compile(r'^[0-9]{9,18}$')

ICON = {
    'heart': 'M12 20.5C5 15.6 3 12 3 8.8A4.8 4.8 0 0 1 12 6.3a4.8 4.8 0 0 1 9 2.5c0 3.2-2 6.8-9 11.7Z',
    'copy': 'M9 9h10v11H9ZM5 15V4h10',
    'check': 'M5 12.5l4.5 4.5L19 7.5',
    'bank': 'M3 9.5 12 4l9 5.5M5 10v8M9.5 10v8M14.5 10v8M19 10v8M3 20.5h18',
}


def icon(name, cls='sup-ico'):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="{ICON[name]}"></path></svg>'


def load():
    return json.loads(DATA.read_text(encoding='utf-8'))


def usable(d=None):
    """True only for details the owner marked verified, complete and well formed."""
    d = load() if d is None else d
    if d.get('verified') is not True:
        return False
    if not all(isinstance(d.get(k), str) and d[k].strip() for k, _ in FIELDS):
        return False
    return bool(ACCOUNT.match(d['account_number']) and IFSC.match(d['ifsc']))


def render(office_email, contact_href='Contact.html'):
    d = load()
    head = (f'<div class="sup-head"><p class="sup-eyebrow">{icon("heart", "sup-ico sup-ico-sm")}<span>Stand with us</span></p>'
            f'<h2 id="sup-title">{TITLE}</h2><p class="sup-lede">{escape(LEDE)}</p></div>')
    if usable(d):
        rows = ''.join(
            f'<div class="sup-row sup-row-{k}"><dt>{label}</dt><dd><span class="sup-val" data-copy="{escape(d[k], quote=True)}">{escape(d[k])}</span>'
            f'<button class="sup-copy" type="button" hidden aria-label="Copy {label.lower()}">{icon("copy")}<span>Copy</span></button></dd></div>'
            for k, label in FIELDS)
        body = (f'<div class="sup-body"><h3>{icon("bank", "sup-ico sup-ico-sm")}<span>Bank details</span></h3>'
                f'<dl class="sup-rows">{rows}</dl>'
                f'<div class="sup-actions"><button class="sup-all" type="button" hidden>{icon("copy")}<span>Copy Bank Details</span></button>'
                f'<p class="sup-status" role="status" aria-live="polite"></p></div>'
                f'<p class="sup-note">These are the account details printed on {escape(d["source_label"])}. '
                f'This website does not take online payments. Please confirm the details with the office before you transfer, '
                f'on <a href="{escape(contact_href, quote=True)}">the Contact page</a> or at <a href="mailto:{escape(office_email, quote=True)}">{escape(office_email)}</a>.</p></div>')
    else:
        body = (f'<div class="sup-body"><p class="sup-note">To give or to ask how you can help, please contact the office: '
                f'<a href="{escape(contact_href, quote=True)}">Contact page</a> or <a href="mailto:{escape(office_email, quote=True)}">{escape(office_email)}</a>. '
                f'This website does not take online payments.</p></div>')
    return (f'<section class="sup" id="support" data-support data-no-motion aria-labelledby="sup-title">'
            f'<div class="sup-card"><span class="sup-glow" aria-hidden="true"></span>{head}{body}</div></section>')
