# Jame Ul Uloom Residential School — redesigned static website

This project contains a modern, responsive, multi-page redesign built from the supplied website archive.

## Open locally

You can open `index.html` directly in a browser. For best results, use a local static server from this folder:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000`.

## Deploy

Upload the contents of this folder to a static web host (for example, the public directory of your existing hosting provider). Keep the `assets/` folder and the HTML pages in the same relative locations. The site does not require a database or a build step to run.

## Rebuild from the archived pages

The supplied legacy pages are retained under `audit/source-html/`. To regenerate the redesigned pages:

```bash
pip install -r requirements.txt
python build.py
```

## Included features

- 23 linked HTML pages, including the original 18 page routes and five category/gallery landing pages
- Shared responsive navigation and footer
- Light/dark theme toggle with saved preference
- Original image assets retained in `assets/images/`
- Gallery filters and image lightbox
- Hero slideshow, reveal animations and back-to-top control
- Accessible mobile navigation dialog and reduced-motion support
- Migration report and asset inventory

## Migration limitations

This build was generated from the ZIP supplied in the conversation. It does not by itself prove that every item on the live server was captured. `audit/source-html/` preserves the archived source pages, `migration-report.json` records the local inventory, and `MIGRATION-REPORT.md` summarizes what was generated. Compare the result against the live website before claiming complete live-site recovery.

## Before publishing

- Confirm the school's current contact details and institutional content.
- Replace the placeholder domain in `sitemap.xml` with the final production domain.
- Test the website on the actual hosting provider and on mobile devices.
