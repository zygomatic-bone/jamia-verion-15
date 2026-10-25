# AGENTS.md

## What this is
The Jame Ul Uloom Residential School (Banikuppa) website: a plain static multi-page site (HTML + one CSS file + one JS file + images) (original legacy notes). There is no framework, package.json or build step.

## Layout
- `*.html` (root) — the 23 published pages. `index.html` is the homepage; `home.html` is the "School overview" subpage (not the homepage).
- `assets/css/styles.css` — all styling, including light/dark theme variables keyed on `html[data-theme]`.
- `assets/js/app.js` — shared behaviour: theme toggle (stored in `localStorage` key `jame-theme`), dropdown/mobile drawer nav, scroll reveal animations, homepage hero slideshow, gallery filters, lightbox, back-to-top.
- `assets/images/` — original school photographs. File names are case-sensitive on many hosts; keep references exact.
- `generate_site.py` / `build.py` — regenerate every root HTML page, `sitemap.xml` and the migration reports from `audit/source-html/`. Hand edits to generated HTML are overwritten by a rebuild; change the generator instead.

## Conventions
- The site content and design come from the client's supplied archive. Do not redesign or rewrite content unless asked.
- The theme is set by an inline script in each page's `<head>` before CSS loads to avoid a flash; keep it when editing pages.
- All asset paths are relative (`assets/...`), so pages work from any folder and via `file://`.
