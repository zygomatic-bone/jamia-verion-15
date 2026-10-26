"""The Bayanath page around the existing Speaker Profile (tools/speaker/speaker_card.py: channel card, Official Social Media Links card,
Photo Slideshow) and the "Support Our Mission" card on About Us (tools/support/support_card.py).

The brief's first rule: the existing speaker card is not changed. tools/tests/fixtures/speaker-card-original.html is the existing card's
HTML as it was in jameululoom_phase9_4_complete_website_r2.zip, byte for byte. If the owner edits speaker-profile.json on purpose,
regenerate that fixture from speaker.render(); an accidental change fails here.
Run after python3 tools/build.py (the built pages in public/ are checked)."""
import json, re, sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUB = ROOT / 'public'
for sub in ('speaker', 'support', 'connect', ''):
    sys.path.insert(0, str(ROOT / 'tools' / sub) if sub else str(ROOT / 'tools'))
import speaker, speaker_card, support_card   # noqa: E402
from imgutil import image_size   # noqa: E402

FIXTURE = (ROOT / 'tools' / 'tests' / 'fixtures' / 'speaker-card-original.html').read_text(encoding='utf-8')
LINKS = ['https://www.youtube.com/@MuftiMaqsoodImran', 'https://linktr.ee/MuftiMaqsoodImran', 'https://www.facebook.com/MuftiMaqsoodImran',
         'https://www.instagram.com/muftimaqsoodimran', 'https://x.com/maqsoodimran', 'https://chat.whatsapp.com/C2AGE85WofaEseRcOpnddp']


def built(name):
    return (PUB / name).read_text(encoding='utf-8')


class ExistingCardIsUntouched(unittest.TestCase):
    def test_existing_card_html_is_byte_identical_to_the_original(self):
        self.assertEqual(speaker.render(), FIXTURE)

    def test_existing_card_keeps_all_designations_and_content(self):
        html = speaker.render()
        for t in ('Chief Imam &amp; Khateeb', 'Principal', 'Member, Imarat-e-Shariah, Karnataka', 'Convener, Karnataka Moon Sighting Committee'):
            self.assertIn(t, html)
        self.assertEqual(html.count('class="sp-d"'), 6)
        self.assertEqual(html.count('class="sp-pill"'), 8)


class PageLayout(unittest.TestCase):
    """The Bayanath page: a narrow left column that ends with the Linktree card, and a wide right column with the heading, the video grid,
    the full-width slideshow directly under the grid, and the channel card last."""

    @classmethod
    def setUpClass(cls):
        cls.page = built('Bayanath.html')
        m = re.search(r'<div class="bz-side">(.*?)</div><div class="bz-main">', cls.page, re.S)
        cls.side = m.group(1)
        cls.main = cls.page[m.end():]

    def test_the_sidebar_holds_the_profile_then_the_linktree_card_and_nothing_else(self):
        self.assertEqual(self.side, speaker.render() + speaker_card.social())
        self.assertEqual(re.findall(r'<(aside|a|section|div) class="(sp-card|so-card|sc-card|ph)', self.side), [('aside', 'sp-card'), ('a', 'so-card')])
        self.assertNotIn('Watch Lectures on YouTube', self.side)
        self.assertNotIn('Explore All Channels', self.side)
        self.assertNotIn('ph-show', self.side)

    def test_the_main_column_order_is_heading_videos_slideshow_channel(self):
        marks = ['<h1>Bayanath</h1>', 'class="bz-all"', 'data-bayanath', 'class="by-grid"', 'data-slideshow', 'class="sc-card"']
        pos = [self.main.index(m) for m in marks]
        self.assertEqual(pos, sorted(pos))
        self.assertEqual(self.main.count('data-slideshow'), 1)
        self.assertEqual(self.main.count('class="sc-card"'), 1)
        self.assertEqual(self.page.count('class="sc-cta"'), 1)   # no duplicate of the channel card anywhere

    def test_one_h1_and_the_hero_band_keeps_only_the_breadcrumb(self):
        self.assertEqual(self.page.count('<h1>'), 1)
        hero = re.search(r'<section class="page-hero page-hero-slim">(.*?)</section>', self.page, re.S).group(1)
        self.assertIn('class="crumbs"', hero)
        self.assertNotIn('<h1', hero)

    def test_view_all_videos_goes_to_the_channels_video_tab(self):
        self.assertIn('<a class="bz-all" href="https://www.youtube.com/@MuftiMaqsoodImran/videos" target="_blank" rel="noopener noreferrer">', self.page)
        self.assertIn('Latest Bayanath videos from the official YouTube channel, with the speaker’s profile.', self.page)

    def test_the_speakers_name_is_exact_everywhere_it_is_printed(self):
        name = 'Mufti Dr. Mohamed Maqsood Imran Rashadi'
        self.assertGreaterEqual(self.page.count(name), 3)
        for bad in ('Moulana Mufti', 'Maulana Mufti', 'Moulana Dr', 'Mufti Dr Mohamed', 'Mohammed Maqsood'):
            self.assertNotIn(bad, self.page)
        self.assertEqual(speaker_card.load()['name'], name)
        self.assertEqual(speaker.load()['name'], name)

    def test_the_video_data_flow_is_unchanged(self):
        self.assertIn('data-src="data/bayanath-videos.json"', self.page)
        self.assertIn('class="by-grid" aria-busy="true"', self.page)
        self.assertIn('portal-assets/bayanath.js', self.page)
        self.assertIn('portal-assets/aurora.js', self.page)
        js = (ROOT / 'tools' / 'portal-ui' / 'bayanath.js').read_text(encoding='utf-8')
        self.assertIn('fetch(root.dataset.src', js)
        self.assertIn("slice(0, 10)", js)

    def test_the_new_assets_load_in_order_and_ship_and_the_old_ones_are_gone(self):
        for a in ('portal-assets/slideshow.css', 'portal-assets/slideshow.js'):
            self.assertIn(a, self.page)
            self.assertTrue((PUB / a).is_file())
        self.assertLess(self.page.index('portal-assets/bayanath.css'), self.page.index('portal-assets/slideshow.css'))
        self.assertFalse((PUB / 'portal-assets' / 'speakercard.css').exists())
        self.assertFalse((PUB / 'portal-assets' / 'speakercard.js').exists())
        self.assertNotIn('slideshow', built('index.html'))   # nothing leaks onto other pages


class ChannelCard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = speaker_card.load()
        cls.html = speaker_card.channel()

    def test_all_six_channel_links_are_exact_and_open_safely(self):
        hrefs = re.findall(r'<a class="sc-(?:cta|soc[^"]*)" href="([^"]+)" target="_blank" rel="([^"]+)"', self.html)
        self.assertEqual([h for h, _ in hrefs], LINKS)
        self.assertTrue(all('noopener' in r for _, r in hrefs))
        self.assertEqual(len(re.findall(r'<a [^>]*href="https?://', self.html)), 6)

    def test_the_youtube_button_is_primary_and_the_other_channels_are_in_an_expandable_panel(self):
        self.assertIn('Watch Lectures on YouTube', self.html)
        self.assertIn('Explore All Channels', self.html)
        self.assertLess(self.html.index('sc-cta'), self.html.index('<details class="sc-more"'))
        self.assertEqual(self.html.count('class="sc-soc '), 5)

    def test_official_wording(self):
        self.assertIn('Discover inspiring lectures, authentic Islamic guidance, and educational talks rooted in the Qur’an and Sunnah.', self.html)
        self.assertIn('Islamic scholar, speaker, author, and educator dedicated to sharing Islamic knowledge with wisdom, knowledge, and compassion.', self.html)
        self.assertIn('Imam &amp; Khateeb of Jamia Masjid Bengaluru City', self.html)
        self.assertIn('Chief Principal of Jamia-ul-Uloom Arabic College, Bengaluru', self.html)


class SocialCard(unittest.TestCase):
    def test_it_links_to_the_official_linktree_page_and_opens_safely(self):
        html = speaker_card.social()
        m = re.match(r'<a class="so-card" href="([^"]+)" target="_blank" rel="([^"]+)">', html)
        self.assertIsNotNone(m)
        # the live official page ends in "Imran"; the shorter "MuftiMaqsoodImra" does not exist (checked when this card was built)
        self.assertEqual(m.group(1), 'https://linktr.ee/MuftiMaqsoodImran')
        self.assertEqual(sorted(m.group(2).split()), ['noopener', 'noreferrer'])
        self.assertEqual(len(re.findall(r'<a ', html)), 1)

    def test_content(self):
        html = speaker_card.social()
        self.assertIn('Official Social Media Links', html)
        self.assertIn('YouTube, Facebook, Instagram, X and Threads.', html)
        self.assertEqual(html.count('class="so-chip"'), 5)
        self.assertIn('opens the official Linktree page in a new tab', html)
        self.assertIn('alt=""', html)   # the small portrait is decorative: the text beside it says everything

    def test_the_portrait_is_a_shipped_owner_supplied_photograph(self):
        d = speaker_card.load()['social_card']
        self.assertTrue((speaker_card.SLIDE_DIR / d['portrait']).is_file())
        self.assertEqual((speaker_card.SLIDE_DIR / d['portrait']).read_bytes(), (PUB / 'portal-assets' / 'speaker' / 'slides' / d['portrait']).read_bytes())

    def test_the_existing_official_links_are_kept(self):
        self.assertIn('https://linktr.ee/MuftiMaqsoodImran', speaker_card.channel())   # still listed under Explore All Channels


class Slideshow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = speaker_card.load()
        cls.html = speaker_card.slideshow()

    def test_only_the_listed_photographs_are_used_and_they_ship_unchanged(self):
        srcs = set(re.findall(r'<img [^>]*src="([^"]+)"', self.html))
        files = {s.rsplit('/', 1)[1] for s in srcs}
        self.assertEqual(files, {s['file'] for s in self.d['slides']})
        for f in files:
            self.assertEqual((speaker_card.SLIDE_DIR / f).read_bytes(), (PUB / 'portal-assets' / 'speaker' / 'slides' / f).read_bytes())
        for s in self.d['slides']:   # width/height attributes match the real pictures (no layout shift, no distortion)
            w, h = image_size(speaker_card.SLIDE_DIR / s['file'])
            self.assertIn(f'src="portal-assets/speaker/slides/{s["file"]}" alt="{s["alt"]}" width="{w}" height="{h}"', self.html)

    def test_no_duplicate_photographs(self):
        import hashlib
        digests = [hashlib.sha256((speaker_card.SLIDE_DIR / s['file']).read_bytes()).hexdigest() for s in self.d['slides']]
        self.assertEqual(len(digests), len(set(digests)))
        self.assertEqual(len({s['file'] for s in self.d['slides']}), len(self.d['slides']))

    def test_every_photograph_has_a_description_a_source_and_its_rights(self):
        for s in self.d['slides']:
            for k in speaker_card.REQUIRED_SLIDE_KEYS:
                self.assertTrue(str(s.get(k, '')).strip(), (s['file'], k))

    def test_a_photograph_without_a_source_or_rights_stops_the_build(self):
        import tempfile
        orig = speaker_card.DATA
        try:
            for drop in ('source', 'rights', 'alt'):
                d = json.loads(orig.read_text(encoding='utf-8'))
                del d['slides'][0][drop]
                with tempfile.TemporaryDirectory() as t:
                    p = Path(t) / 'c.json'
                    p.write_text(json.dumps(d), encoding='utf-8')
                    speaker_card.DATA = p
                    with self.assertRaises(SystemExit) as cm:
                        speaker_card.load()
                    self.assertIn(drop, str(cm.exception))
            d = json.loads(orig.read_text(encoding='utf-8'))
            d['slides'][0]['file'] = 'not-there.jpg'
            with tempfile.TemporaryDirectory() as t:
                p = Path(t) / 'c.json'
                p.write_text(json.dumps(d), encoding='utf-8')
                speaker_card.DATA = p
                with self.assertRaises(SystemExit):
                    speaker_card.load()
        finally:
            speaker_card.DATA = orig

    def test_first_photograph_loads_eagerly_and_the_rest_lazily(self):
        n = len(self.d['slides'])
        main = re.findall(r'<img class="ph-img" [^>]*alt="([^"]+)"[^>]*loading="(\w+)"', self.html)
        self.assertEqual(len(main), n)
        self.assertEqual([m[1] for m in main], ['eager'] + ['lazy'] * (n - 1))
        self.assertEqual(len(re.findall(r'class="ph-bg" src="[^"]+" alt=""', self.html)), n)   # backdrop copies are decorative

    def test_accessible_markup(self):
        self.assertIn('role="group" aria-roledescription="carousel"', self.html)
        self.assertEqual(self.html.count('aria-roledescription="slide"'), len(self.d['slides']))
        self.assertIn('aria-label="Previous photograph"', self.html)
        self.assertIn('aria-label="Next photograph"', self.html)
        self.assertIn('aria-label="Pause the slideshow"', self.html)
        self.assertEqual(len(re.findall(r'class="ph-dot[ "]', self.html)), len(self.d['slides']))
        self.assertIn('aria-live="polite"', self.html)
        self.assertIn('tabindex="0"', self.html)
        self.assertEqual(len(re.findall(r'aria-hidden="true" hidden>', self.html)), 2)   # the two redundant side arrows are hidden from assistive technology

    def test_slideshow_pace_is_slow(self):
        self.assertGreaterEqual(self.d['interval_seconds'], 8)
        self.assertLessEqual(self.d['interval_seconds'], 12)

    def test_the_scripts_inject_no_html_and_the_css_uses_no_backdrop_blur(self):
        for name in ('slideshow.js', 'bayanath.js'):
            js = (ROOT / 'tools' / 'portal-ui' / name).read_text(encoding='utf-8')
            for bad in ('innerHTML', 'outerHTML', 'insertAdjacentHTML', 'eval(', 'document.write'):
                self.assertNotIn(bad, js, name)
        css = (ROOT / 'tools' / 'portal-ui' / 'slideshow.css').read_text(encoding='utf-8')
        self.assertNotIn('backdrop-filter', css)
        self.assertIn('prefers-reduced-motion: reduce', css)
        self.assertIn("matchMedia('(prefers-reduced-motion: reduce)')", (ROOT / 'tools' / 'portal-ui' / 'slideshow.js').read_text(encoding='utf-8'))
        self.assertIn('object-fit: contain', css)   # whole photographs, never cropped

    def test_video_ids_and_thumbnails_are_still_validated(self):
        by = (ROOT / 'tools' / 'portal-ui' / 'bayanath.js').read_text(encoding='utf-8')
        self.assertIn(r'/^[A-Za-z0-9_-]{11}$/', by)
        self.assertIn(r"/^https:\/\/(?:i\d?\.ytimg\.com|img\.youtube\.com)\//", by)
        self.assertNotIn('data-count', self.html)   # app.js animates [data-count] elements as counters

    def test_no_video_resources_before_interaction(self):
        page = built('Bayanath.html')
        self.assertNotIn('<iframe', page)
        self.assertNotIn('youtube-nocookie.com/embed', page)
        self.assertNotIn('<video', page)

    def test_no_hotlinked_images_on_the_page(self):
        page = built('Bayanath.html')
        for src in re.findall(r'<img [^>]*src="([^"]+)"', page):
            self.assertFalse(src.startswith(('http:', 'https:', '//')), src)


class SupportCard(unittest.TestCase):
    def test_about_us_keeps_its_whole_body_and_gains_the_support_section_after_it(self):
        import content_main
        old = content_main.ROOT['AboutUs.html'][1]
        page = built('AboutUs.html')
        inner = old.split('</p>', 2)[-1]   # past the eyebrow, title and lede that the page template re-wraps
        self.assertIn(inner, page)
        self.assertLess(page.index(inner), page.index('id="support"'))
        self.assertEqual(page.count('Support Our Mission'), 1)
        self.assertIn('Your support helps us continue our educational mission and serve our community. We are grateful for every contribution and every person who stands with us.', page)

    def test_the_verified_details_are_published_on_about_us_only(self):
        d = support_card.load()
        self.assertTrue(support_card.usable(d))
        page = built('AboutUs.html')
        for k, _ in support_card.FIELDS:
            self.assertIn(d[k].replace('&', '&amp;'), page)
        for p in PUB.glob('**/*.html'):
            if p.name != 'AboutUs.html':
                self.assertNotIn(d['account_number'], p.read_text(encoding='utf-8'), p.name)

    def test_formats(self):
        d = support_card.load()
        self.assertRegex(d['account_number'], r'^[0-9]{9,18}$')
        self.assertRegex(d['ifsc'], r'^[A-Z]{4}0[A-Z0-9]{6}$')
        self.assertEqual(d['ifsc'][:4], 'CNRB')   # Canara Bank's code

    def test_details_are_withheld_unless_verified_complete_and_well_formed(self):
        good = support_card.load()
        self.assertTrue(support_card.usable(good))
        for change in ({'verified': False}, {'verified': 'yes'}, {'account_number': ''}, {'ifsc': 'cnrb0000410'}, {'account_number': '12AB'}, {'bank': '  '}):
            d = dict(good); d.update(change)
            self.assertFalse(support_card.usable(d), change)
        d = dict(good); del d['branch']
        self.assertFalse(support_card.usable(d))

    def test_a_withdrawn_card_shows_no_numbers_and_no_placeholders(self):
        orig = support_card.load
        try:
            support_card.load = lambda: dict(orig(), verified=False)
            html = support_card.render('jamiaululoom@gmail.com')
        finally:
            support_card.load = orig
        self.assertIn('Support Our Mission', html)
        self.assertNotRegex(html, r'\d{9}')
        self.assertNotIn('sup-copy', html)
        self.assertNotIn('IFSC', html)
        self.assertIn('mailto:jamiaululoom@gmail.com', html)

    def test_no_payment_gateway_form_or_external_script(self):
        html = support_card.render('jamiaululoom@gmail.com')
        for bad in ('<form', '<input', '<script', 'razorpay', 'paypal', 'upi://', 'Pay now', 'Donate now'):
            self.assertNotIn(bad, html)
        self.assertIn('does not take online payments', html)

    def test_the_support_assets_load_on_about_us_only(self):
        self.assertIn('portal-assets/support.css', built('AboutUs.html'))
        self.assertNotIn('support.css', built('Contact.html'))
        for a in ('support.css', 'support.js'):
            self.assertTrue((PUB / 'portal-assets' / a).is_file())

    def test_the_withheld_flyer_image_stays_out_of_the_site(self):
        self.assertFalse(list(PUB.glob('**/home.jpg')), 'the appeal flyer image itself is not published')


if __name__ == '__main__':
    unittest.main()
