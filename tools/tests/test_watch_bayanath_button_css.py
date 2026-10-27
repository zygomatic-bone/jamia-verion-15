"""Checks of the stylesheet text for the home-page "Watch Bayanath" glass button, and that nothing else is animated by it.
They read the CSS only; the rendered look, the alignment and the animation were checked in a browser (light and dark, desktop, tablet, phone).

Run:  python3 -I -m unittest discover -s tools/tests -p "test_watch_bayanath_button_css.py" -v
"""
import os, re, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUB = Path(os.environ.get('JU_SITE_DIR') or ROOT / 'public')
CSS = (PUB / 'portal-assets/portal.css').read_text(encoding='utf-8')
START = '/* ---- Home hero: "Watch Bayanath" - full-width frosted-glass button'
BLOCK = CSS[CSS.index(START):]
BEFORE = CSS[:CSS.index(START)]
BTN = '.page-home .hero.portal-hero .button-row .hx-btn-ghost'


class Width(unittest.TestCase):
    def test_the_button_spans_the_three_buttons_through_the_row_not_through_a_fixed_width(self):
        self.assertIn('@media (min-width: 40.0625rem) {', BLOCK)
        self.assertIn(BTN.rsplit(' ', 1)[0] + ' { display: grid; grid-template-columns: repeat(3, max-content); justify-content: start; }', BLOCK)
        self.assertIn(BTN + ' { grid-column: 1 / -1; }', BLOCK)
        self.assertNotRegex(BLOCK, r'(?<![-\w])width\s*:')   # no fixed, percentage or calc width anywhere in the block
        for forbidden in (r'\bheight\s*:', r'min-height', r'\bpadding\s*:', r'font-size', r'letter-spacing', r'\bmargin\s*:', r'\bgap\s*:'):
            self.assertNotRegex(BLOCK, forbidden)   # the height, spacing and gap stay with the shared hero-button rules


class Scope(unittest.TestCase):
    def test_every_selector_of_the_block_names_this_button_or_the_home_hero_row(self):
        for sel in re.findall(r'^\s*([^@\s/][^{\n]*?)\s*\{', BLOCK, re.M):
            if re.fullmatch(r'(\d+%)(,\s*\d+%)*', sel):
                continue   # keyframe steps
            self.assertTrue('hx-btn-ghost' in sel or sel == BTN.rsplit(' ', 1)[0], sel)

    def test_no_menu_or_other_button_rule_is_in_the_block(self):
        for name in ('desktop-nav', 'nav-group', 'drop-menu', 'site-header', 'hx-btn-gold', 'hx-points', 'mobile-drawer'):
            self.assertNotIn(name, BLOCK)

    def test_only_two_elements_animate_and_nothing_else_in_the_stylesheet_uses_the_new_keyframes(self):
        self.assertEqual(re.findall(r'@keyframes (ju-[\w-]+)', CSS), ['ju-glass-sweep', 'ju-glass-glow'])
        self.assertEqual(len(re.findall(r'animation: ju-glass', BLOCK)), 2)
        self.assertNotIn('ju-glass', BEFORE)
        self.assertNotIn('ju-glass', (PUB / 'ResidentialSchoolBanikuppa/assets/css/motion.css').read_text(encoding='utf-8'))

    def test_the_older_ghost_button_rules_are_gone_and_the_gold_buttons_keep_theirs(self):
        self.assertNotIn('hx-btn-ghost', BEFORE.replace(START, ''))   # they used to fight the glass rules in dark focus and on touch screens
        self.assertGreaterEqual(BEFORE.count('.hx-btn-gold'), 3)

    def test_the_markup_is_unchanged(self):
        html = (PUB / 'index.html').read_text(encoding='utf-8')
        self.assertIn('<a class="button hx-btn-ghost" href="Bayanath.html"><svg class="btn-icon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9.5"></circle><path d="M10 8.5v7l6-3.5Z"></path></svg>Watch Bayanath</a>', html)


class Look(unittest.TestCase):
    def test_both_themes_have_their_own_glass(self):
        self.assertIn(':root:not([data-theme="dark"]) ' + BTN + ' {', BLOCK)
        self.assertIn(':root[data-theme="dark"] ' + BTN + ' {', BLOCK)
        self.assertIn('color: #071a4d;', BLOCK)   # navy text and icon in light
        self.assertIn('color: #fff;', BLOCK)      # white text in dark
        self.assertRegex(BLOCK, r'border: 1px solid rgba\(214, 177, 99')    # champagne gold
        self.assertRegex(BLOCK, r'border: 1px solid rgba\(230, 192, 106')   # gold on navy

    def test_sweep_and_glow_repeat_stay_behind_the_text_and_use_the_short_ease_out_transition(self):
        self.assertRegex(BLOCK, r'ju-glass-sweep 4\.6s ease-in-out infinite')
        self.assertRegex(BLOCK, r'ju-glass-glow 4s ease-in-out infinite')
        self.assertEqual(len(re.findall(r'z-index: -[12];', BLOCK)), 2)
        self.assertEqual(set(re.findall(r'(\.\d+)s ease-out', BLOCK)), {'.18'})
        self.assertIn('@media (hover: hover) {', BLOCK)
        self.assertIn(BTN + ':active { transform: scale(.985); }', BLOCK)
        self.assertIn(BTN + ':focus-visible { transform: translateY(-1px); }', BLOCK)

    def test_reduced_motion_stops_every_animation_and_movement(self):
        rm = BLOCK[BLOCK.index('@media (prefers-reduced-motion: reduce)'):]
        self.assertEqual(len(re.findall(r'animation: none', rm)), 2)
        self.assertIn('transition: none', rm)
        self.assertIn('transform: none', rm)

    def test_phones_get_no_blur(self):
        ph = BLOCK[BLOCK.index('@media (max-width: 46rem)'):BLOCK.index('@media (prefers-reduced-motion: reduce)')]
        self.assertEqual(len(re.findall(r'(?<!-webkit-)backdrop-filter: none', ph)), 2)


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
