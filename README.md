Jame-ul-Uloom Website
This is a static website built with regular HTML, CSS and JavaScript, just like the original site. The entire website lives in public/, so publish that folder as the site's root. You do not need a build step, an install step, a database or a login, and the website itself does not run server-side code.

GitHub Pages publishing is handled by .github/workflows/deploy-pages.yml. That workflow belongs to the repository; it is not included in or changed by this package.

Two other tasks are handled separately:
- Weekly Bayanath video updates: The GitHub Actions workflow in .github/workflows/update-bayanath.yml runs two small Python scripts in tools/. This updates the video list; it is separate from publishing the website.
- Feedback, Admissions and Careers forms: These can send enquiries to the office through the Cloudflare Worker in serverless/forms-worker/. The service needs to be configured once; see Setting up the form service. Until it is configured, pressing Send opens the visitor's email application with the message prepared. The page says that the email application has been opened; it does not claim that the form was sent. A form shows success only after the service confirms that the message was accepted.
Project layout
public/                    The website; publish this folder as the site root
  index.html               The only homepage
  *.html                   Main pages: About Us, Institutions, Bayanath, Contact, Support Us and others
  <Institution>/*.html     Pages for each institution (ITI, PUGirlsCollege, DegreeGirlsCollege, BCA, NCPUL,
                           EngNurSchoolDEL, EngPrimarySchoolDEL, EngGirlsHighSchool, EngBoysHighSchool,
                           ShobaehifzDel, ShobaeAlimiyathDel)
  ResidentialSchoolBanikuppa/   Residential School site (25 pages, with its own images and styles)
  portal-assets/           Shared CSS, JavaScript, images, documents and videos
  data/                    bayanath-videos.json (video list) and bayanath-speakers.json (speaker exceptions)
  robots.txt, sitemap.xml  Files for search engines
  _headers, _redirects, .htaccess   Security headers and redirects for old addresses (see below)
docs/                      Photo and media maps, plus provenance records
serverless/forms-worker/   Form service for Cloudflare Worker (plain JavaScript, no dependencies)
tools/                     Bayanath updater, static-page refresher, optional host uploader, link checker and tests
.github/workflows/         GitHub Actions workflows, including the weekly Bayanath update
The site contains 115 HTML pages. Most follow the same structure: a header and navigation menu (with a drawer on phones), the page content and a footer. As in the original site, each page contains its own copy of that structure.
Editing the website
- Text, images and links: Edit these directly in the relevant HTML page. Add images to public/portal-assets/images/ and use lowercase file names. Display photographs in full rather than cropping them. The only exception is a decorative, blurred background, where object-fit: cover is allowed. Do not add MP3 audio.
- Navigation menu: Add a new menu item to every page that uses the main site header. The entry usually appears in the desktop menu, the phone drawer and the footer. Search for an existing item such as SupportUs.html to find the relevant locations. The Residential School pages use a separate header.
- Adding a page: Start with a similar existing page. Update its <title>, description, canonical URL, og:url, heading and content. Then add the page to public/sitemap.xml.
- Search metadata: Each page's <head> contains its canonical URL, robots settings, Open Graph metadata and JSON-LD. The site's canonical origin is https://jameululoom.org. The 404 page is the only page marked noindex. The JSON-LD data block uses <script type="application/ld+json">; the security policy allows this data block. Search engines decide what to index, display and cite, so the metadata cannot guarantee a particular result.
- Sitemap, robots and redirects: These files are maintained manually. public/sitemap.xml should list exactly the pages that can be indexed. _redirects and .htaccess should contain the same redirects for old addresses, including the /home rule. Whenever a page moves, add the redirect to both files and confirm that its destination exists.
- Stylesheets and scripts: The shared site design and motion rules are in portal-assets/portal.css. The Residential School uses ResidentialSchoolBanikuppa/assets/css/styles.css and motion.css. Other stylesheets are grouped by page or feature: bayanath.css, scholar.css, slideshow.css, connect.css, support.css, masjid.css and theme-light.css. The main scripts are app.js (menu, drawer, reveal effects and theme toggle), theme-init.js (sets the theme before the first paint), motion.js, slideshow.js, bayanath.js, forms.js, support.js, masjid.js and aurora.js. The Residential School also uses app.js, theme-init.js and motion.js from portal-assets/.
- Themes: The <html> element uses data-theme="light|dark". The selected theme is saved in localStorage under jame-theme. Light mode is the default for first-time visitors, but a saved preference takes priority. The navy-themed pages use dark design tokens, while theme-light.css adapts them for light mode. Change theme colours there instead of hard-coding a dark background in an individual page stylesheet.
- Code style: Use four spaces for indentation, attach the opening brace to selectors (selector{), write functions as function(){, use single quotes and semicolons, and stick to ES5 in scripts that run on every page.
- Public-facing wording: Do not publish internal notes about where content came from, disclaimers about scanned documents or audit notices. Keep dated caveats that help visitors understand the information. Do not silently combine conflicting historical dates or figures; label fees, institution strengths and results with the date given by the source. Make sure each institution is described using its own information, not text belonging to another institution.
Checks to run before publishing
Run these commands from the repository root:
python3 tools/check_site.py                       # Checks links, images, scripts, IDs, redirects, forbidden files and inline code
python3 -I -m unittest discover -s tools/tests -v # Runs page, metadata, security-header, updater and form tests
Python 3.10 or later is sufficient; the GitHub workflow uses Python 3.12. The form service's own tests require Node.js 20 or later and can be run with:
cd serverless/forms-worker && node --test
No packages need to be installed. The Python test suite also runs these Node.js tests when Node is available. If Node is missing, it skips them and reports that. On Windows, the Python command is usually python rather than python3. The .gitattributes file keeps text files on LF line endings.

check_site.py reports a failure if it finds any of the following:
- A broken link, image, script or HTML #id reference.
- A redirect with a missing destination or fragment, or a redirect that chains through another redirect.
- A home.html file at the root of public/.
- A forbidden file inside public/, such as design source files, thumbnail caches, server-configuration backups, archives, keys or server-side scripts.
- An inline <script> body or a style= attribute, which the site's security policy prohibits.
- An image without alt text.
Bayanath page and video updates
- Page content: Bayanath.html includes the speaker profile, video cards, official links, photo slideshow and channel card. The video cards are written into the HTML so search engines can read them. portal-assets/bayanath.js also builds the cards in the browser from data/bayanath-videos.json, allowing the page to display the latest list. Card titles omit the leading emoji and trailing hashtags; the link tooltip keeps the full title. Clicking a card replaces it with the YouTube player.
- Speaker attribution: Each card displays Speaker: <name> with the name linked to the scholar profile. If a video belongs to another speaker, record that in data/bayanath-speakers.json, using {"<11-character video id>": "Other Speaker"} to show the name without a link, or {"<id>": false} to hide the speaker line. Never attribute a video to the scholar when it is known to feature someone else.
- Static markup and structured data: Keep the <!--bayanath:cards--> and <!--bayanath:recent--> markers, along with the bayanath-jsonld data-block ID. tools/refresh_bayanath_static.py updates the marked HTML and structured data from the JSON; the weekly workflow runs this script after an update. Videos without an upload date still appear on the page, but are left out of the structured data.
- Photo slideshow: Every photograph needs descriptive alt text. Use only photographs of the speaker that the owner has permission to publish. Do not use stock photos, images taken from search results or duplicate photographs. Display the photographs in full.
- Aurora background: Animate the CSS gradients using transform and opacity only. aurora.js sets --ax, --ay, --sx and --sy. Do not add a touchmove listener or read layout values on every animation frame. Do not use green on this page, and keep the prefers-reduced-motion rules. Do not use data-count; app.js treats it as a counter.
Support Us and donation information
Donation information appears in SupportUs.html (under About > Support Us in the menu, and in the footer), in the Support Our Mission card on About Us, and in the Donate Now sections at the end of ShobaehifzDel/home.html and ShobaeAlimiyathDel/home.html.

The bank details come from the Trust's appeal flyer supplied by the owner. They appear only on About Us and Support Us; the two Shoba pages link to Support Us and do not display bank details. Never invent, reformat or “tidy up” those details. If they change, update both pages and the data-copy values used by the copy buttons.

There is no payment gateway, QR code, UPI ID, tax claim, fundraising target or statement explaining how donations are used. The building must be described as proposed. The appeal image is portal-assets/support/donation-appeal.png; publish it unchanged, alongside the lighter WebP copy.
Files that must not be published
Keep the following out of the public website:
- Named students' certificates. NCPUL/images/CERT1.jpeg is permanently excluded at the owner's request.
- Anything from the server's private area, including mail, hosting-control files, credentials and cgi-bin contents.
- Old backup copies of the donation flyer.
- The two unidentified portraits and the stock-style picture.
Security and performance
- Security headers: public/_headers is used by Netlify and Cloudflare Pages; public/.htaccess is used by Apache. Keep the values in these files consistent. The Content Security Policy permits only the site's own scripts, styles, fonts, images and media, plus YouTube thumbnails and the YouTube privacy-mode player used on the Bayanath page. It blocks inline code, plugins and framing. The configuration also sets nosniff, a strict referrer policy and HSTS, and disables camera, microphone, location, payment and USB access. The Residential School has a stricter policy in ResidentialSchoolBanikuppa/.htaccess and in its section of _headers; keep those copies in sync. Do not send the same header from two _headers rules.
- Host limitations: GitHub Pages ignores _headers, _redirects and .htaccess. The pages and links still work, but those files do not apply their security headers or redirects there. To use them, publish through a host that supports one of those files.
- No inline code: Do not add inline <script> elements or style= attributes. Do not add unsafe-inline, unsafe-eval or another host to the policy unless there is a clear reason. tools/tests/test_security_headers.py checks the headers.
- Safe DOM updates: Build DOM elements with textContent and createElement. Use innerHTML only for fixed strings; never insert page data into an HTML string. Validate IDs and URLs as shown in bayanath.js. Pages must not write the query string or fragment into the page, or use eval, postMessage or cookies.
- External links and image privacy: External links that open in a new tab need rel="noopener". Photographs of pupils and staff are marked noimageindex. The exception is the official scholar portrait at portal-assets/speaker/mufti-maqsood-imran-rashadi.jpg, which remains eligible for image search. In Apache, .htaccess identifies that exact path with SetEnvIf and omits the header for it; _headers has never covered the speaker folder. Other photos in portal-assets/speaker/ keep the header on Apache. Photograph links inside main open in the dialog.mo-lb viewer, so do not add target="_blank" to them.
- Motion and speed: Animate only transform and opacity. Keep the prefers-reduced-motion rules and the exit behaviour for html.mo-lite. Scripts add the hidden start states (.mo-pre and .mo-group) only below the fold and remove them afterwards, so a script failure does not leave content hidden. Do not use filter: blur() on animated layers, full-screen mix-blend-mode, or backdrop-filter on repeated cards. The header, hero panels, dropdown, drawer and photo viewer may use backdrop-filter; keep the -webkit- prefix and the @supports fallback.
- Jamia Masjid videos and photographs: Videos on the Jamia Masjid page use preload="none", muted, loop, playsinline and data-autoplay. masjid.js plays them only while they are visible, and they must remain silent. Only the first image should load eagerly. The photographs belong to the owner and must remain unchanged. Do not crop, recompress or rename them unless you also update docs/photos-provenance.json and docs/MASJID-MEDIA-MAP.md.
- Apache setup: When Apache is used, Options -Indexes prevents directory listings, and dotfiles, backups, logs and source maps are denied. The headers require mod_headers.
Forms and message delivery
Feedback, Admissions and Careers use ordinary HTML forms. forms.js handles the steps, validation messages and background submission.

A form displays success only when the service returns HTTP 200 with {"ok":true}. If it does not, the visitor's text stays in the form, a brief error appears and a mail link is offered. The form field names, limits, required flags and choices are defined in serverless/forms-worker/src/schema.js. If you change a field, update both the schema and the corresponding page; tools/tests/test_forms_worker.py checks that they match.

When a form's action is a mailto: address and it has data-cx-offline, it does not contact the service. Instead, it opens the visitor's email program with the message prepared and never displays the thank-you panel. Do not add a false or premature success message, and do not invent a service endpoint. The forms do not offer résumé or certificate uploads.

The service in serverless/forms-worker/ accepts POST requests only. It enforces a request-size limit while reading the stream, checks that the request's Origin or Referer is in ALLOWED_ORIGINS, verifies a hidden field and a time trap, and rate-limits requests using a hashed visitor address. It validates every field again, builds the email subject from fixed words and sets Reply-To only after validation. It does not echo submitted data. It reports success only after the mail provider confirms delivery acceptance; otherwise, it responds with HTTP 503.

core.js preserves U+200C, U+200D, U+200E and U+200F, which are needed for Urdu, Persian and Kannada, while removing other control characters. Keep RESEND_API_KEY and RATE_SALT as Cloudflare Worker secrets only. Never put them in wrangler.toml, the repository, a response or a log. Add a test in serverless/forms-worker/test/ whenever you introduce new behaviour.
Setting up the form service
This setup needs accounts that are not included in the repository. The code has been tested, but the service is not live until you create the accounts and deploy it. It has not been tested against the real mail provider or Cloudflare account. The full instructions, curl test and troubleshooting notes are in serverless/forms-worker/README.md.
1. Set up the mail provider. Create an account at Resend, verify jameululoom.org by adding the DNS records Resend provides, and create an API key with sending permission only. In wrangler.toml, MAIL_FROM must use an address on the verified domain.
2. Set up Cloudflare. From serverless/forms-worker/, sign in and create the KV namespace used for rate-limit counters:
   npx wrangler kv namespace create FORMS_KV
   Copy the resulting ID into wrangler.toml. Check ALLOWED_ORIGINS, MAIL_TO and MAIL_FROM, then save the secrets:
   npx wrangler secret put RESEND_API_KEY
   npx wrangler secret put RATE_SALT
   Use a long, random value for RATE_SALT, then deploy the Worker:
   npx wrangler deploy
   The command prints the Worker's URL.
3. Connect the forms to the Worker. In Feedback.html, Admissions.html and Careers.html, set each form's action to the Worker URL and remove enctype="text/plain" and data-cx-offline. Add the Worker's origin (plain https, with no extra path) to connect-src and form-action in _headers and .htaccess, then publish the site.
4. Test delivery. Open Feedback.html on the live site, send a test message and confirm that it arrives. Use npx wrangler tail to view service logs; the logs contain reference numbers and outcomes only.
Limitations: Cloudflare KV rate limits are not atomic, so they help discourage abuse but are not exact counters. The free plan also has daily write limits. The service does not keep a copy of submitted messages, so the office mailbox is the record. Visitors without JavaScript submit directly to the service and see a simple page returned by it.
Hosting on cPanel or another standard web host
The weekly workflow updates files in the repository. If the site is published from that repository through GitHub Pages, Cloudflare Pages or Netlify, the updated version is published automatically. A site hosted on a regular web host does not update automatically, so the latest versions of these three files need to be copied to the host:
- data/bayanath-videos.json
- Bayanath.html
- MuftiMaqsoodImran.html
Choose one of these approaches:
1. Upload from GitHub automatically. After an update, .github/workflows/update-bayanath.yml runs tools/upload_to_host.py, which sends the three files over FTP with TLS. This step is skipped unless the repository secret CPANEL_FTP_HOST is configured. Set it up once:
   - In your hosting control panel, create an FTP account that can access only the website folder. Note the FTP server name, username and password. Use a server name covered by the host's TLS certificate.
   - In the GitHub repository, open Settings → Secrets and variables → Actions and add CPANEL_FTP_HOST, CPANEL_FTP_USER and CPANEL_FTP_PASSWORD. Add CPANEL_FTP_DIR (the site directory as seen by the FTP account, such as /public_html) if the account's home directory is not the website directory. Set CPANEL_FTP_PORT only if the port is not 21.
   - If the host's certificate does not match any usable server name, the optional secret CPANEL_FTP_TLS_VERIFY can be set to off to skip certificate verification. The connection remains encrypted, but the server's identity is no longer verified.
   - Upload the entire public/ folder manually once. Then open the Actions tab and run Update Bayanath videos to test the setup. The log should show uploaded ... for each file. Keep the repository in sync with the live site: a later upload will overwrite any changes made only on the host to one of these three files.
2. Pull and deploy from GitHub. cPanel's Git Version Control can clone the repository. With a .cpanel.yml file, it can copy public/ into the website directory when you select Update from Remote and Deploy HEAD Commit. It does not pull changes by itself, so fully automatic weekly updates need a host cron job to run git pull and the deployment. The repository must be readable by the host, and .cpanel.yml must copy only public/—never .git.
3. Upload manually. After each weekly run, upload the three files listed above, or upload the whole public/ folder.
If you move the domain to GitHub Pages or Cloudflare Pages, none of these cPanel upload steps are needed.
Weekly Bayanath updates with GitHub Actions
The workflow .github/workflows/update-bayanath.yml runs every Saturday at 21:00 India Standard Time. Its cron expression is 30 15 * * 6 in UTC. GitHub may start the scheduled run a few minutes late, and scheduled workflows run only from the repository's default branch.

The workflow reads the official channel (@MuftiMaqsoodImran, channel ID UClF-O3ig9ZKMvbeKB4t9mjQ) from tools/bayanath-config.json. It adds new videos to public/data/bayanath-videos.json, keeps existing entries, removes duplicates and retains the ten newest videos. Then tools/refresh_bayanath_static.py updates the static cards and structured data in Bayanath.html and MuftiMaqsoodImran.html. Both Python scripts use only the standard library.

If a verified Bayanath playlist is available, set playlist_id in the configuration. Otherwise, the updater filters video titles using title_keywords.
- Run it manually: Open the Actions tab, select Update Bayanath videos, and choose Run workflow. Self-tests use a local mock of YouTube; they do not contact YouTube.
- Retries: The update step makes up to three attempts, waiting two minutes and then four minutes between attempts. If all attempts fail, the workflow turns red and leaves the existing committed list unchanged.
- Safety checks: The workflow replaces the file only after building and validating a complete list. If anything fails, the previous list remains in place. Deleted or private videos are removed. The scripts contact only https YouTube and Google addresses, refuse redirects to other hosts and limit response size. The API key is sent only in a request header and is never printed. A commit is made only if the list changes. Keep workflow actions pinned to commit hashes, and preserve the cron schedule, workflow_dispatch and actions: write permissions.
- Publishing the update: A push made with a workflow's own token does not start other workflows. After committing a change, this job therefore starts deploy-pages.yml using gh workflow run. For that to work, deploy-pages.yml must include a workflow_dispatch: trigger. That workflow is not included in this package, so check the repository's version. If dispatch fails, the job prints a warning; the updated data remains committed and deployment must be started manually. The deployment workflow only needs to publish public/; there is no build step.
- Optional API key: The repository secret YOUTUBE_API_KEY (YouTube Data API v3) lets the updater look back through 50 uploads and retrieve exact upload dates. Without it, the updater uses the public RSS feed, which includes the latest 15 uploads.
- Known limits: If branch protection prevents the workflow from pushing to the default branch, the commit step fails. GitHub may also pause scheduled workflows in repositories that have been inactive for a long time; re-enable the workflow in the Actions tab. If all three attempts fail, the next automatic attempt is the following Saturday unless you run the workflow manually.
