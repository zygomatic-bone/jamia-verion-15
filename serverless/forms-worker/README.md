# Form service (Cloudflare Worker)

Receives the Feedback, Admissions enquiry and Careers forms of the website and emails the office. It is the only server-side part of the project: the website itself is static (GitHub Pages) and cannot run server code.

**Status: written and tested, not deployed.** It needs a Cloudflare account and a mail-provider account, which are not part of this repository. Until the steps below are done and the forms point at it, the website's forms only open the visitor's own email program with the message prepared; they never show the thank-you panel. Nothing here has been run against the real mail provider or Cloudflare; the tests use fakes (see "Tests").

## How it works
`POST` from the website, form data. In order: configuration present (otherwise **503**, honest message) → `OPTIONS` pre-flight answered for the website's own origin only → size cap 24 KB read from the stream (**413**) → `Origin` (or `Referer`) must be one of `ALLOWED_ORIGINS` (**403**) → known form name, hidden "website" field empty, not submitted faster than `MIN_FILL_SECONDS` (**400**) → every field validated against `src/schema.js` (**422** with a message per field) → rate limits per hashed visitor address (hour and day) and overall per day (**429**) → one email through the Resend API → **200 `{"ok":true,"ref":"JU-FE-XXXXXX"}` only if Resend answered 200**; anything else is **503** and the website tells the visitor nothing was sent.

The subject is built from fixed words and the chosen options only; a visitor's text appears only in the body; the visitor's address is used as `Reply-To` only after validation; nothing a visitor typed is echoed back; responses are `no-store`. Logs hold form name, reference and outcome only (never personal data, addresses or secrets).

## One-time setup
1. **Resend** (https://resend.com): create an account, add and verify the domain you will send from (DNS records are shown there), create an API key with sending access only. `MAIL_FROM` must be an address on that verified domain.
2. In this folder, with the current Wrangler (`npx wrangler`, Node 20+):
   ```bash
   npx wrangler login
   npx wrangler kv namespace create FORMS_KV      # prints an id: paste it into wrangler.toml
   # edit wrangler.toml [vars]: ALLOWED_ORIGINS (exactly the published addresses), MAIL_TO, MAIL_FROM
   npx wrangler secret put RESEND_API_KEY         # paste the key when asked
   npx wrangler secret put RATE_SALT              # a long random text, 16+ characters
   npx wrangler deploy                            # prints https://jame-forms.<account>.workers.dev
   ```
3. Point the three forms at the service: in `public/Feedback.html`, `public/Admissions.html` and `public/Careers.html` set the form's `action` to the printed address (`https://jame-forms.<account>.workers.dev/submit`) and remove `enctype="text/plain"` and `data-cx-offline`. Add the address's origin to `connect-src` and `form-action` in `public/_headers` and `public/.htaccess`, then deploy the site.
4. Check it from outside (replace the address; the `Origin` must be one of `ALLOWED_ORIGINS`):
   ```bash
   curl -i -X POST https://jame-forms.<account>.workers.dev \
     -H 'Origin: https://jameululoom.org' -H 'Accept: application/json' \
     -d form=feedback -d rating=5 -d category=other -d 'message=Test message from the setup check' -d opened=9000
   ```
   Expect `200` and `{"ok":true,...}`, and an email at `MAIL_TO`. Without the secrets the service answers `503`, which is correct. `npx wrangler tail` shows the log.

## If something is wrong
- Forms on the site show "We could not send your message right now" for every submission: a setting or secret is missing (`wrangler tail` names it, never its value) or `RATE_SALT` is still the placeholder.
- "We could not send your message": the mail provider refused. Check the API key, the verified domain and that `MAIL_FROM` is on it.
- "This form can only be sent from the Jame ul uloom website": the page's address is not in `ALLOWED_ORIGINS` (scheme and host exactly, e.g. `https://www.…` is different from `https://…`).
- Rate limits use KV, which is not atomic: they slow abuse, they are not an exact counter. Each accepted message makes three KV writes; check Cloudflare's current free-plan allowance if you expect many messages.

## Tests
`node --test` in this folder (Node 20+, no packages). The mail provider and KV are replaced by in-memory fakes, so nothing is sent. `tools/tests/test_forms_worker.py` runs the same suite, checks that the pages' form fields match `src/schema.js` and that the committed configuration holds no secret.

`src/schema.js` holds the rules the pages and the service share; change a field in the page and in this file together.
