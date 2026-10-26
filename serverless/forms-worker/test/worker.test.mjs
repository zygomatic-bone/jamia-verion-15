/* Tests of the form service (src/worker.js). Run:  cd serverless/forms-worker && node --test   (no dependencies, no network).
   The mail provider and the counter store are replaced by in-memory fakes, so nothing is ever sent. */
import { test, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert/strict';
import worker, { missingConfig } from '../src/worker.js';
import { clean, validEmail } from '../src/core.js';

const ORIGIN = 'https://site.example';
const KEY = 'resend-key-SECRET-123456';
const SALT = 'a-long-random-salt-for-tests';

const GOOD = {
  feedback: { form: 'feedback', rating: '5', category: 'appreciation', message: 'Thank you for the care shown to my son.', audience: 'parent', name: 'Test Parent', email: 'parent@example.org', opened: '9000' },
  admissions: { form: 'admissions', guardian: 'Test Guardian', phone: '+91 98765 43210', programme: 'pu', level: 'First year', consent: 'on', opened: '9000' },
  careers: { form: 'careers', name: 'Test Candidate', phone: '9876543210', email: 'candidate@example.org', area: 'teaching-school', consent: 'on', opened: '9000' },
};

class FakeKV {
  constructor() { this.map = new Map(); }
  async get(k) { return this.map.has(k) ? this.map.get(k) : null; }
  async put(k, v) { this.map.set(k, v); }
}

let kv; let mails; let mailStatus; let mailThrows; let logs; const realFetch = globalThis.fetch; const realLog = console.log;

function env(over = {}) {
  return {
    ALLOWED_ORIGINS: ORIGIN, MAIL_TO: 'office@example.org', MAIL_FROM: 'website@example.org', RESEND_API_KEY: KEY, RATE_SALT: SALT,
    FORMS_KV: kv, RATE_PER_IP_HOUR: '50', RATE_PER_IP_DAY: '150', RATE_GLOBAL_DAY: '500', ...over,
  };
}

beforeEach(() => {
  kv = new FakeKV(); mails = []; mailStatus = 200; mailThrows = false; logs = [];
  console.log = (...a) => { logs.push(a.join(' ')); };
  globalThis.fetch = async (url, init) => {
    if (mailThrows) throw new Error('network down');
    mails.push({ url: String(url), headers: init.headers, payload: JSON.parse(init.body) });
    return new Response('{}', { status: mailStatus });
  };
});
afterEach(() => { globalThis.fetch = realFetch; console.log = realLog; });

function post(data, { origin = ORIGIN, json = true, ip = '203.0.113.7', raw, headers = {}, e = env(), multipart = false } = {}) {
  let body = raw;
  const h = { ...headers };
  if (body === undefined) {
    if (multipart) {
      body = new FormData();
      for (const [k, v] of Object.entries(data || {})) body.append(k, v);
    } else {
      body = new URLSearchParams(data || {}).toString();
      h['Content-Type'] = 'application/x-www-form-urlencoded';
    }
  } else if (!h['Content-Type']) {
    h['Content-Type'] = 'application/x-www-form-urlencoded';
  }
  if (origin) h.Origin = origin;
  if (json) h.Accept = 'application/json';
  if (ip) h['CF-Connecting-IP'] = ip;
  return worker.fetch(new Request('https://forms.example/submit', { method: 'POST', body, headers: h }), e);
}

test('each form is accepted and mailed once, with a reference and no caching', async () => {
  for (const [name, data] of Object.entries(GOOD)) {
    const r = await post(data);
    assert.equal(r.status, 200, name);
    const j = await r.json();
    assert.equal(j.ok, true);
    assert.match(j.ref, /^JU-[A-Z]{2}-[A-Z2-9]{6}$/);
    assert.equal(r.headers.get('Cache-Control'), 'no-store');
    assert.equal(r.headers.get('Access-Control-Allow-Origin'), ORIGIN);
  }
  assert.equal(mails.length, 3);
  const m = mails[0];
  assert.equal(m.url, 'https://api.resend.com/emails');
  assert.equal(m.headers.Authorization, `Bearer ${KEY}`);
  assert.deepEqual(m.payload.to, ['office@example.org']);
  assert.equal(m.payload.reply_to, 'parent@example.org');
  assert.equal(m.payload.subject, '[Jame ul uloom website] Feedback: 5 of 5, Appreciation');
  assert.ok(mails.some((x) => x.payload.subject === '[Jame ul uloom website] Admissions enquiry: Pre University College for Girls'));
  assert.ok(mails[2].payload.text.includes('Area of interest: Teaching: schools'));
  assert.ok(mails[1].payload.text.includes('The sender agreed to be contacted about this message.'));
});

test('the multipart form posts that the website sends are accepted as well', async () => {
  const r = await post(GOOD.careers, { multipart: true });
  assert.equal(r.status, 200);
  assert.equal(mails.length, 1);
});

test('invalid input is refused field by field and nothing is mailed', async () => {
  let r = await post({ ...GOOD.feedback, rating: '9', category: 'nonsense', message: 'hi', email: 'not-an-email' });
  assert.equal(r.status, 422);
  assert.deepEqual(Object.keys((await r.json()).errors).sort(), ['category', 'email', 'message', 'rating']);
  const noConsent = { ...GOOD.admissions }; delete noConsent.consent;
  r = await post(noConsent);
  assert.equal(r.status, 422);
  assert.ok('consent' in (await r.json()).errors);
  assert.equal((await post({ ...GOOD.careers, phone: 'abc' })).status, 422);
  assert.equal((await post({ ...GOOD.feedback, message: 'x'.repeat(2001) })).status, 422);
  r = await post(null, { raw: new URLSearchParams([...Object.entries(GOOD.feedback), ['name', 'second']]).toString() });
  assert.equal(r.status, 422);   // a repeated field is refused
  assert.ok('name' in (await r.json()).errors);
  const upload = new FormData();
  for (const [k, v] of Object.entries(GOOD.feedback)) upload.append(k, v);
  upload.set('name', new Blob(['x'], { type: 'text/plain' }), 'x.txt');
  r = await worker.fetch(new Request('https://forms.example/s', { method: 'POST', body: upload, headers: { Origin: ORIGIN, Accept: 'application/json' } }), env());
  assert.equal(r.status, 422);   // a file where text is expected
  assert.equal(mails.length, 0);
});

test('a visitor cannot inject mail headers, recipients or subject text', async () => {
  let r = await post({ ...GOOD.feedback, email: 'a@example.org\r\nBcc: victim@example.org' });
  assert.equal(r.status, 422);
  r = await post({ ...GOOD.feedback, name: 'Eve\r\nBcc: victim@example.org', message: 'Line one\r\nBcc: victim@example.org is just text' });
  assert.equal(r.status, 200);
  const p = mails[0].payload;
  assert.deepEqual(Object.keys(p).sort(), ['from', 'reply_to', 'subject', 'text', 'to']);
  assert.equal(p.reply_to, 'parent@example.org');
  assert.deepEqual(p.to, ['office@example.org']);
  assert.equal(p.subject, '[Jame ul uloom website] Feedback: 5 of 5, Appreciation');
  assert.ok(!p.subject.includes('victim') && !p.from.includes('victim'));
  assert.ok(p.text.includes('victim@example.org is just text'));   // inside the body it is only text
});

test('only our own website may post, and only with POST', async () => {
  for (const origin of [null, 'https://evil.example', 'https://site.example.evil.example', 'http://site.example', 'null']) {
    const r = await post(GOOD.feedback, { origin });
    assert.equal(r.status, 403, String(origin));
    assert.equal(r.headers.get('Access-Control-Allow-Origin'), null);
  }
  const g = await worker.fetch(new Request('https://forms.example/submit', { method: 'GET', headers: { Origin: ORIGIN } }), env());
  assert.equal(g.status, 405);
  assert.equal(g.headers.get('Allow'), 'POST, OPTIONS');
  assert.equal(mails.length, 0);
});

test('a browser pre-flight is answered for our site only', async () => {
  const ok = await worker.fetch(new Request('https://forms.example/submit', { method: 'OPTIONS', headers: { Origin: ORIGIN, 'Access-Control-Request-Method': 'POST' } }), env());
  assert.equal(ok.status, 204);
  assert.equal(ok.headers.get('Access-Control-Allow-Origin'), ORIGIN);
  assert.match(ok.headers.get('Access-Control-Allow-Methods'), /POST/);
  assert.equal(ok.headers.get('Access-Control-Allow-Origin') === '*', false);
  const bad = await worker.fetch(new Request('https://forms.example/submit', { method: 'OPTIONS', headers: { Origin: 'https://evil.example' } }), env());
  assert.equal(bad.status, 403);
  assert.equal(bad.headers.get('Access-Control-Allow-Origin'), null);
});

test('robots are refused: hidden field, too-fast submission, unknown form', async () => {
  assert.equal((await post({ ...GOOD.feedback, website: 'http://spam.example' })).status, 400);
  assert.equal((await post({ ...GOOD.feedback, opened: '300' })).status, 400);
  assert.equal((await post({ ...GOOD.feedback, form: 'nothing' })).status, 400);
  assert.equal((await post({ ...GOOD.feedback, form: '__proto__' })).status, 400);
  assert.equal((await post({ ...GOOD.feedback, form: 'constructor' })).status, 400);
  assert.equal(mails.length, 0);
});

test('the rate limit stops a flood, per visitor, and does not store addresses', async () => {
  const e = env({ RATE_PER_IP_HOUR: '2', RATE_PER_IP_DAY: '5' });
  const codes = [];
  for (let i = 0; i < 4; i += 1) codes.push((await post(GOOD.feedback, { e })).status);
  assert.deepEqual(codes, [200, 200, 429, 429]);
  assert.equal(mails.length, 2);
  assert.equal((await post(GOOD.feedback, { e, ip: '198.51.100.9' })).status, 200);   // somebody else is not blocked
  for (const k of kv.map.keys()) {
    assert.ok(!k.includes('203.0.113.7') && !k.includes('198.51.100.9'), k);
  }
});

test('the whole-service daily limit applies too', async () => {
  const e = env({ RATE_GLOBAL_DAY: '1' });
  assert.equal((await post(GOOD.feedback, { e, ip: '192.0.2.1' })).status, 200);
  assert.equal((await post(GOOD.feedback, { e, ip: '192.0.2.2' })).status, 429);
});

test('a body that is too large is refused, whatever its Content-Length says', async () => {
  const big = 'form=feedback&message=' + 'a'.repeat(30000);
  assert.equal((await post(null, { raw: big })).status, 413);
  const stream = new ReadableStream({ start(c) { c.enqueue(new TextEncoder().encode(big)); c.close(); } });
  const lying = new Request('https://forms.example/s', { method: 'POST', body: stream, duplex: 'half', headers: { Origin: ORIGIN, Accept: 'application/json', 'Content-Type': 'application/x-www-form-urlencoded', 'Content-Length': '10' } });
  assert.equal((await worker.fetch(lying, env())).status, 413);
  assert.equal(mails.length, 0);
});

test('a mail provider that does not confirm is never reported to the visitor as success', async () => {
  for (const status of [400, 401, 422, 429, 500, 202]) {
    mailStatus = status;
    const r = await post(GOOD.feedback, { ip: `192.0.2.${status % 200}` });
    assert.equal(r.status, 503, String(status));
    assert.equal((await r.json()).ok, false);
  }
  mailThrows = true;
  const r = await post(GOOD.feedback, { ip: '192.0.2.250' });
  assert.equal(r.status, 503);
  assert.equal((await r.json()).ok, false);
});

test('missing configuration is reported honestly and nothing is attempted', async () => {
  const cases = { ALLOWED_ORIGINS: '', MAIL_TO: '', MAIL_FROM: '', RESEND_API_KEY: '', RATE_SALT: '', FORMS_KV: undefined };
  for (const [name, value] of Object.entries(cases)) {
    const e = env({ [name]: value });
    assert.deepEqual(missingConfig(e), [name]);
    const r = await post(GOOD.feedback, { e });
    assert.equal(r.status, 503, name);
    const j = await r.json();
    assert.equal(j.ok, false);
    assert.ok(!JSON.stringify(j).includes(name));   // no setting names are shown to a visitor
  }
  assert.equal(missingConfig(env({ RATE_SALT: 'change-this-to-a-long-random-text' })).length, 1);   // the placeholder is not a salt
  assert.equal(missingConfig(env({ RATE_SALT: 'short' })).length, 1);
  assert.equal(missingConfig(env({ ALLOWED_ORIGINS: 'http://not-https.example' })).length, 1);
  assert.equal(mails.length, 0);
  assert.equal((await worker.fetch(new Request('https://forms.example/s', { method: 'POST' }), undefined)).status, 503);
});

test('Urdu text and markup are kept as plain text in the mail and never echoed back', async () => {
  const payload = 'شکریہ <script>alert(1)</script> & "quotes"';
  const r = await post({ ...GOOD.feedback, message: payload }, { json: false });
  assert.equal(r.status, 200);
  assert.match(r.headers.get('Content-Type'), /text\/html/);
  assert.match(r.headers.get('Content-Security-Policy'), /default-src 'none'/);
  const page = await r.text();
  assert.ok(!page.includes('<script>') && !page.includes('شکریہ'));
  assert.ok(mails[0].payload.text.includes(payload));
  const bad = await post({ ...GOOD.feedback, rating: '0' }, { json: false });
  assert.equal(bad.status, 422);
  assert.ok((await bad.text()).includes('<h1>We could not send this</h1>'));
});

test('word joiners are kept and hidden direction controls are removed', async () => {
  const persian = 'می‌خواهم';
  const kannada = 'ಕ್‍ಷ';
  const evil = 'abc‮def​ghi\u0007';
  const r = await post({ ...GOOD.feedback, message: `Hello ${persian} ${kannada} ${evil}`, name: persian });
  assert.equal(r.status, 200);
  const text = mails[0].payload.text;
  assert.ok(text.includes(`${persian} ${kannada} abcdefghi`));
  assert.ok(text.includes(`Name: ${persian}`));
  assert.ok(!text.includes('‮') && !text.includes('​') && !text.includes('\u0007'));
});

test('a message of invisible characters only counts as empty', async () => {
  const r = await post({ ...GOOD.feedback, message: '‌‍‎‏‌‍' });
  assert.equal(r.status, 422);
  assert.ok('message' in (await r.json()).errors);
  assert.equal(mails.length, 0);
});

test('invalid UTF-8 is refused instead of being stored as replacement characters', async () => {
  const raw = new Uint8Array([...new TextEncoder().encode('form=feedback&rating=5&category=other&opened=9000&message=hello%20'), ...new TextEncoder().encode('%FF%FEabc')]);
  const r = await post(null, { raw });
  assert.equal(r.status, 422);
  assert.ok('message' in (await r.json()).errors);
});

test('no secret reaches a response, a header or the log, and the log holds no personal data', async () => {
  const everything = [];
  const grab = async (r) => { everything.push(await r.text(), JSON.stringify([...r.headers])); };
  await grab(await post(GOOD.feedback));
  await grab(await post({ ...GOOD.feedback, rating: '9' }));
  await grab(await post(GOOD.feedback, { origin: 'https://evil.example' }));
  mailStatus = 500;
  await grab(await post(GOOD.feedback, { ip: '192.0.2.77' }));
  await grab(await post(GOOD.feedback, { e: env({ RESEND_API_KEY: '' }) }));
  const seen = everything.join('\n') + '\n' + logs.join('\n');
  for (const secret of [KEY, SALT]) assert.ok(!seen.includes(secret), 'a secret leaked');
  for (const personal of ['parent@example.org', 'Test Parent', 'care shown to my son', '203.0.113.7']) assert.ok(!logs.join('\n').includes(personal), `${personal} was logged`);
});

test('the shared validation helpers', () => {
  assert.equal(clean('  a ​ b  ', false), 'a b');
  assert.equal(clean('‌', false), '');
  assert.equal(clean('line1\r\n\r\n\r\n\r\nline2', true), 'line1\n\nline2');
  for (const ok of ['a@b.co', 'first.last+tag@sub.example.org']) assert.equal(validEmail(ok), true, ok);
  for (const bad of ['a@b', '@b.co', 'a b@c.de', 'a@b..co', '.a@b.co', 'a@-b.co', 'a@b.co\n', 'a,b@c.de', 'a@b.c>']) assert.equal(validEmail(bad), false, bad);
});
