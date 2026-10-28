# Notes for contributors

This guide is for anyone making changes to the Jame-ul-Uloom website. Most pages are generated from source files, so the key thing is to make edits in the right place and run the checks before publishing. The notes below also cover a few details that need to stay unchanged for the site to work properly.

## Before you start

### Build the site and run the tests

Only the `public/` folder is published. The source files and generators live in `tools/`. After making a change, rebuild the site:

```bash
python3 tools/build.py
```

The build regenerates the site and checks for broken links and missing assets. Fix any errors it reports before moving on.

Please make changes in the source files, not in generated output. The next build replaces generated HTML, `portal.css`, copied scripts, `_headers`, `_redirects`, `.htaccess` and `serverless/forms-worker/src/schema.generated.js`, so edits made directly to those files will be lost.

Run the tests too:

```bash
python3 -I -m unittest discover -s tools/tests
```

Keep the test suite passing. If Node.js 20 or newer is installed, this command also runs the form service's Node tests. If Node is not installed, those tests are skipped; the output will say so.

Use Python 3.10 or newer. Keep the scripts compatible with Python 3.10—for example, avoid backslashes or reusing the same quote type inside an f-string expression, which only works in Python 3.12 and later. When writing generated files, use `write_text(..., encoding='utf-8', newline='\n')` so Windows does not change line endings to CRLF.

A couple of test details are easy to miss:

- Tests that start a child process must use `child_env()` from `test_update_bayanath.py`. Do not pass an environment containing only `PATH`; on Windows, a child Python process also needs `SYSTEMROOT` or it may fail with `_Py_HashRandomization_Init`.
- If a test expects an operation to be refused, use `assertRefused`. Checking only for a non-zero exit code is not enough, because a crash can return one too.

### How the site runs

The site uses plain HTML, CSS and JavaScript and is published on GitHub Pages. Keep `.github/workflows/deploy-pages.yml` in the repository; it is part of the publishing setup and must not be replaced or removed. There is no site framework, database or server-side code running on GitHub Pages.

Two supporting jobs run separately from the published pages:

- The weekly Bayanath video update uses GitHub Actions and `tools/update_bayanath.py`.
- The forms service lives in `serverless/forms-worker/`. It is a Cloudflare Worker written in plain JavaScript, with no dependencies.

The Python files in `tools/` are used while building the site. They do not run as website server code. The form tests also check that server-side script files and the name of the removed form handler are not reintroduced.

### A few rules for every page

The site's Content Security Policy (CSP) blocks inline `<script>` tags and inline `style=` attributes. Keep scripts and styles in their proper files. Do not add `unsafe-inline`, `unsafe-eval` or another host to the policy unless there is a clear need.

Show content photographs in full. Use `object-fit: cover` only for decorative, blurred backgrounds—not for actual photographs. Use lowercase file names, and do not add MP3 audio.

`index.html` is the only homepage. The old root-level `home.html` portal page was removed deliberately, and the generator will reject it if it comes back. The logo, Home links, breadcrumbs and footers should all lead to `index.html`.

When adding code, follow the style already used in the project: four spaces for indentation, CSS selectors written as `selector{`, JavaScript functions written as `function(){`, single quotes and semicolons. Scripts that run on every page must remain compatible with ES5.

## Where to make changes

Most website edits belong in `tools/`, not in the generated HTML files.

- `tools/generate_site.py` builds the Residential School pages.
- `tools/generate_portal.py` builds the main site and institution pages.
- Shared CSS and JavaScript live in `tools/portal-ui/` and are copied to `public/portal-assets/`. The Residential School pages use the shared `app.js`, `theme-init.js`, `motion.js` and `motion.css` as well.
- `tools/site_header.py` is the one place where the site header is defined. Both generators use it; the Residential School passes `home_href='/'`. Do not add a separate school header or top bar.
- Main-site wording is kept in `tools/content_main.py`, `tools/content_more.py` and `tools/content_inst.py`. Change the text there rather than editing the generated page.

To add a picture, list its source, destination, alt text and caption in `tools/recovery_assets.py`, then run `import_recovered_assets.py` again. Every picture in that list must be used on a page. The published image folder is `public/portal-assets/images/`; do not bring back the old `recovered/` folder name.

Sometimes the original site repeated information about one institution on another institution's page. Keep that information on the page for the institution it actually describes, then add a redirect through `content_inst.REDIRECTS`. The generator checks that the redirect target and any `#id` fragment exist, and that the old redirect source is no longer a file.

Please take care with historical details. Do not quietly combine dates or figures that conflict, and do not describe one institution using text that originally belonged to another. If a fee, strength or result is tied to a date in the source, keep that date with it.

The public site should not include internal notes about where content came from or how it was recovered, scanned-document disclaimers or audit notices. Keep dated notes only when they help visitors understand the information.

## Material that must stay private

Do not publish certificates belonging to named students. `NCPUL/images/CERT1.jpeg` is permanently excluded at the owner's request. Anything from the server's private area must stay out of the public site too.

Bank details may appear only on the About Us page. They must come from `tools/support/support-details.json`, and they can be displayed only when `verified` is `true`, as authorised in the Speaker Profile brief. The appeal flyer image is marked `WITHHELD` and must not be published. Do not show the bank details anywhere else. The `WITHHELD` entries in `tools/recovery_assets.py` explain which material is being held back and why.

## Security and external links

The main security settings—including CSP, framing restrictions, `nosniff`, referrer policy, HSTS and permissions—are defined in `tools/generate_portal.py` using `CSP`, `CSP_RS` and `SECURITY`. The build writes the settings to `_headers` and `.htaccess`, and `tools/tests/test_security_headers.py` checks them. The Residential School `.htaccess` has its own stricter copy; keep the relevant versions in sync.

Do not define the same header in two `_headers` rules, because some hosts may combine the values. The Residential School block should contain only its additional CSP.

When adding elements to the page with JavaScript, use `textContent` and `createElement`. Use `innerHTML` only for fixed strings—never insert page data into an HTML string. Follow the ID and URL validation used in `bayanath.js`. Any external link that opens with `target="_blank"` must also have `rel="noopener"`.

The Bayanath updater, `tools/update_bayanath.py`, is limited to HTTPS YouTube and Google hosts, along with the loopback test server. It will not follow redirects to other hosts, it limits response sizes, and it never prints or logs the API key. The key is sent only through the `X-Goog-Api-Key` header. Keep GitHub Actions pinned to commit hashes, and run the tests after making changes.

## Bayanath and the Speaker Profile

### Keeping Bayanath videos up to date

`public/Bayanath.html` is generated, and `portal-assets/bayanath.js` builds its video cards from `public/data/bayanath-videos.json`. Do not update the generated page by hand.

The updater is `tools/update_bayanath.py`. Its settings are in `tools/bayanath-config.json`, and `.github/workflows/update-bayanath.yml` runs it every Saturday at 21:00 India time (`30 15 * * 6` in UTC). You can also start the workflow manually.

When the `YOUTUBE_API_KEY` secret is available, the updater reads the channel's uploads playlist through the YouTube Data API. Without that key, it uses the channel's public RSS feed. If an update fails or the list has not changed, the current file is left alone.

The workflow retries up to three times, commits only when the list changes, and then starts `deploy-pages.yml` with `gh workflow run`. That last step is important because a push made with `GITHUB_TOKEN` does not trigger other workflows; without it, the new JSON would not be published. Keep the schedule, pinned action hashes, `workflow_dispatch` and `actions: write`. If a verified Bayanath playlist becomes available, set `playlist_id` in the config. Otherwise, the updater filters titles using `title_keywords`.

### Speaker Profile layout and photographs

The Speaker Profile is assembled from `tools/speaker/speaker_card.py` (`channel()`, `social()` and `slideshow()`), `speaker-card.json` (text, links and slides), and `portal-ui/bayanath.css`, `slideshow.css` and `slideshow.js`.

Please keep the layout in this order:

- **Sidebar:** profile first, Official Social Media Links (Linktree) card last.
- **Main area:** heading and View All Videos link, two-column video grid, full-width slideshow directly below the grid, then the channel card.

`test_speaker_card.py` checks the order. Use the speaker's full name exactly as written here everywhere: **Mufti Dr. Mohamed Maqsood Imran Rashadi**. The correct Linktree address is `https://linktr.ee/MuftiMaqsoodImran`; the shorter address ending in `...Imra` does not exist.

Every photo in `tools/speaker/slides/` needs `alt`, `source` and `rights` entries in `speaker-card.json`. The build stops if any are missing. Use only photographs of the speaker that the owner has the right to publish—no stock photos, hotlinked images, search-result images or duplicates. Display each photograph in full with `object-fit: contain`.

The legacy card, `speaker.py`, `speaker-profile.json` and the `sp-` rules in `bayanath.css` must remain byte-for-byte unchanged because a test pins the HTML. Keep official links exactly as supplied, including `rel="noopener noreferrer"`. Do not add `backdrop-filter` here. Keep the reduced-motion rules, avoid `data-count` (the shared `app.js` turns it into a counter), and use generic symbols instead of brand logos.

### Support Our Mission and speaker details

The Support Our Mission section on the About Us page is maintained in `tools/support/`. Never invent or tidy up bank details, and do not add a payment gateway, UPI details or claims about donations. If an account changes, update it only in `support-details.json`.

For the Speaker Profile, edit `tools/speaker/speaker-profile.json`, not the generated HTML. The six designation titles and eight area labels must keep the exact wording supplied by the owner. Do not make up biography details, credentials, affiliations or languages. Leave `biography` and `languages` empty until the owner provides verified text, and do not display the internal `verification` notes. Show the photograph in full.

The Bayanath stylesheet is scoped under `body.page-bayanath`. Do not use green on this page. Where `backdrop-filter` is already used, keep the `-webkit-` prefix and the `@supports` fallback. Animated layers must keep `pointer-events: none` and use transforms only. Keep the `prefers-reduced-motion` rules too.

### Aurora background

The Aurora background moves CSS gradients using `transform` and `opacity` only. `portal-ui/aurora.js` sets `--ax`, `--ay`, `--sx` and `--sy` on `.bz-bg`; the `.bz-au` markup comes from `tools/speaker/speaker.py`.

Do not add a `touchmove` listener or read layout values on every animation frame. The shared `.ambient` orbs are hidden on this page and should stay hidden.

## Jamia Masjid page

Make Jamia Masjid changes in `tools/masjid/masjid_page.py`, where the sections, alt text and order are set. Do not edit the generated `Masjid.html` directly.

The photographs belong to the owner and must be copied unchanged. Do not crop, recompress or rename them unless you also update `photos-provenance.json` and `MASJID-MEDIA-MAP.md`. The current assignment of pictures to the Advanced Library, Library and Large Library sections was inferred from the images; update it in the source file if the owner corrects it.

The Pathway and Water House section should include two photographs and all its videos. The Library section uses `#library`; do not bring back the old study-hall name.

Videos must use `preload="none"`, `muted`, `loop`, `playsinline` and `data-autoplay`. `portal-ui/masjid.js` plays them only while they are visible. Keep videos silent, and preserve the reduced-motion and data-saving options. Load the first photograph eagerly and lazy-load the rest.

The homepage must not have a B.Com card. The ITI card must use `iti/campus.jpg`, which shows the ITI building.

## Motion, accessibility and speed

Make animation changes in `portal-ui/motion.css` and `portal-ui/motion.js`, not in their generated copies under `public/`.

The `.mo-pre` and `.mo-group` hidden start states are added by script only to content below the fold, then removed after the content is revealed. Keep that behaviour: if JavaScript is disabled or fails, page content must still be visible. Animate `transform` and `opacity` only, and preserve both `prefers-reduced-motion` and the `html.mo-lite` exits for slower devices.

For performance, avoid `filter: blur()` on animated layers, full-screen `mix-blend-mode` layers and `backdrop-filter` on repeated cards. Section 9 of `motion.css` lists the restrictions. Keep `backdrop-filter` only on the header, hero panels, dropdown, drawer and photograph viewer. Background orbs are disabled on screens up to `38rem` wide; do not turn them back on without testing on a phone.

Photograph links inside `main` open in the `dialog.mo-lb` viewer. Do not add `target="_blank"` to those links. Also check long scroll-reveal lists on phones: `portal-ui/app.js` should reveal an item taller than the screen as soon as any part of it becomes visible.

## Forms and contact pages

Feedback, Contact, Admissions and Careers pages are managed in `tools/connect/connect_pages.py` (text and markup), `portal-ui/connect.css` (styles scoped under `body.page-connect`) and `portal-ui/forms.js` (ES5 form behaviour). The pages are registered in `generate_portal.py` through `CONNECT_PAGES`.

Do not invent vacancies, fees, dates, opening hours or coordinates. Keep the phone numbers exactly as printed on the owner's Contact page unless the owner confirms a correction.

### Form fields and validation

`tools/connect/forms-schema.json` is the single source for form field names, types, limits, required flags, choices and the maximum body size. `connect_pages.py` builds the page markup from this file. `tools/generate_forms_worker.py`, which runs as part of `tools/build.py`, creates `serverless/forms-worker/src/schema.generated.js` from the same schema, and the Worker checks every submission against it.

To change a field or choice, update the schema and run `python3 tools/build.py`. The `test_connect.py` and `test_forms_worker.py` tests catch mismatches between the pages and the Worker.

### What visitors see before the form service is set up

The form service address is stored as `endpoint` in `tools/connect/forms-config.json`. While it is empty, the forms act as mail links marked `data-cx-offline`. Do not add a notice on the site saying the forms are being configured or are not live.

When a visitor presses Send, `forms.js` does not contact a server. It opens the visitor's email program with the message prepared and shows the hand-off message (`.cx-handoff`) only. It must not show the thank-you panel. Never tell visitors a message was sent unless it actually was.

Once an endpoint is configured, it must be a plain HTTPS address. The forms can then submit to it, and the CSP should allow only that origin in `connect-src` and `form-action`. Do not invent an endpoint or add extra origins. Show success only when the service returns HTTP 200 with `{"ok":true}`.

### Form service safeguards

In `serverless/forms-worker/src/core.js`, keep the U+200C, U+200D, U+200E and U+200F characters. Urdu, Persian and Kannada text can rely on these joiners and direction marks. Remove other control or invisible characters, but do not strip the entire `\p{C}` category, as that would remove characters these languages need.

The checks in `serverless/forms-worker/src/worker.js` are there to protect the service. It accepts POST requests and answers OPTIONS requests only for the site's own origin. It reads the request-size limit from the stream, checks that Origin or Referer is an HTTPS origin listed in `ALLOWED_ORIGINS`, and uses a honeypot, a time trap and KV rate limits. The visitor address is hashed for rate limiting; the raw address is not stored.

The Worker validates every field, removes disallowed control characters, builds the email subject from fixed words and sets Reply-To only after validation. It does not echo submitted data back to visitors and uses `no-store`. If the mail provider returns anything other than HTTP 200, the Worker must return a failure (503), never success.

Keep `RESEND_API_KEY` and `RATE_SALT` as Worker secrets. Never put them in `wrangler.toml`, the repository, a response or a log, and do not log personal data. Do not add file uploads unless file type, size and contents are validated.

Run the form tests with `node --test` from `serverless/forms-worker/`; they also run through `test_forms_worker.py` when Node is available. Add a test for every new behaviour, and make sure the test would fail if that behaviour were removed.

### Phone numbers still need confirmation

The numbers on the Contact page begin with `082…` (for example, `0822221151`), while the printed flyer uses eight-digit local numbers such as `22221151`. Bengaluru's STD code is 080, so the full number may be `08022221151`. Until the owner confirms it, leave the numbers exactly as they appear on the Contact page.
