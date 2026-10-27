"""Checks of the stylesheet text for the header-menu hover animation and the glass "Watch Bayanath" button.
They read the CSS only; the look itself was checked in a browser (light and dark, desktop, tablet and phone).

Run:  python3 -I -m unittest discover -s tools/tests -p "test_button_and_menu_css.py" -v
"""
import os, re, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUB = Path(os.environ.get('JU_SITE_DIR') or ROOT / 'public')
PORTAL = (PUB / 'portal-assets/portal.css').read_text(encoding='utf-8')
RESIDENTIAL = (PUB / 'ResidentialSchoolBanikuppa/assets/css/motion.css').read_text(encoding='utf-8')
MENU_START = '/* ---- Header menu: smooth hover and keyboard-focus response'
BUTTON_START = '/* ---- Home hero: "Watch Bayanath" as a wider, frosted-glass button'


def menu_block(css):
    start = css.index(MENU_START)
    end = css.find(BUTTON_START, start)
    return css[start:end if end != -1 else len(css)]


def button_block(css):
    return css[css.index(BUTTON_START):]


class HeaderMenu(unittest.TestCase):
    def test_every_page_family_gets_the_same_menu_rules(self):
        self.assertEqual(menu_block(PORTAL).strip(), menu_block(RESIDENTIAL).strip())

    def test_timing_is_180ms_ease_out_and_nothing_moves_or_resizes(self):
        block = menu_block(PORTAL)
        durations = set(re.findall(r'(\d*\.?\d+)s ease-out', block))
        self.assertEqual(durations, {'.18'})
        for forbidden in (r'\bwidth\s*:', r'\bheight\s*:', r'\bpadding', r'\bmargin', r'\bfont', r'\bscale\('):
            self.assertNotRegex(block, forbidden)

    def test_hover_is_limited_to_hover_capable_devices_and_motion_can_be_switched_off(self):
        block = menu_block(PORTAL)
        self.assertIn('@media (hover: hover)', block)
        self.assertIn('@media (hover: none)', block)
        self.assertRegex(block, r'@media \(prefers-reduced-motion: reduce\)\{[^@]*transition: none')

    def test_keyboard_focus_gets_the_same_fill(self):
        block = menu_block(PORTAL)
        for sel in ('.desktop-nav > a:focus-visible', '.nav-group > summary:focus-visible', '.drop-menu a:focus-visible'):
            self.assertIn(sel, block)


class WatchBayanathButton(unittest.TestCase):
    def test_only_the_width_is_set_and_the_height_is_left_to_the_shared_hero_button_rule(self):
        block = button_block(PORTAL)
        self.assertIn('width: min(100%, 26rem);', block)
        for forbidden in (r'\bheight\s*:', r'min-height', r'\bpadding\s*:', r'font-size', r'letter-spacing', r'\bmargin\s*:'):
            self.assertNotRegex(block, forbidden)

    def test_both_themes_have_their_own_glass_and_the_selectors_name_only_this_button(self):
        block = button_block(PORTAL)
        self.assertIn(':root:not([data-theme="dark"]) .page-home .hero.portal-hero .button-row a.hx-btn-ghost[href] {', block)
        self.assertIn(':root[data-theme="dark"] .page-home .hero.portal-hero .button-row a.hx-btn-ghost[href] {', block)
        self.assertIn('color: #071a4d;', block)   # navy text and icon in light
        self.assertIn('color: #fff;', block)      # white text in dark
        for line in re.findall(r'^([^@\n{][^{\n]*)\{', block, re.M):
            if line.strip().startswith(('0%', '50%', '66%', '92%', '100%', 'from', 'to')):
                continue
            self.assertIn('hx-btn-ghost', line, line)

    def test_sweep_and_glow_repeat_slowly_stay_behind_the_text_and_stop_for_reduced_motion(self):
        block = button_block(PORTAL)
        self.assertRegex(block, r'ju-glass-sweep 7s ease-in-out infinite')
        self.assertRegex(block, r'ju-glass-glow 4\.8s ease-in-out infinite')
        self.assertEqual(len(re.findall(r'z-index: -[12];', block)), 2)
        self.assertRegex(block, r'@media \(prefers-reduced-motion: reduce\) \{[^@]*animation: none')
        self.assertIn('@media (hover: hover)', block)

    def test_the_markup_is_unchanged(self):
        html = (PUB / 'index.html').read_text(encoding='utf-8')
        self.assertIn('<a class="button hx-btn-ghost" href="Bayanath.html"><svg class="btn-icon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9.5"></circle><path d="M10 8.5v7l6-3.5Z"></path></svg>Watch Bayanath</a>', html)


class LightIsTheDefault(unittest.TestCase):
    def test_first_visit_gets_light_and_only_a_saved_choice_changes_it(self):
        js = (PUB / 'portal-assets/theme-init.js').read_text(encoding='utf-8')
        self.assertIn("var theme = 'light';", js)
        self.assertIn("if (saved === 'dark' || saved === 'light') theme = saved;", js)
        for p in PUB.rglob('*'):
            if p.suffix in ('.css', '.js'):
                self.assertNotIn('prefers-color-scheme', p.read_text(encoding='utf-8', errors='ignore'), str(p))


if __name__ == '__main__':
    unittest.main()
