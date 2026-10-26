/* Form service for the Jame ul uloom website (Feedback, Admissions enquiry, Careers expression of interest).
   Runs as a Cloudflare Worker (see README.md in this folder for the one-time setup). The website itself stays a plain static site
   (GitHub Pages), which cannot run server code; this is the only server-side part.

   Nothing here trusts the browser: every field is validated again, the mail subject is built from fixed words, a visitor's address is
   used only as Reply-To after validation, nothing the visitor typed is echoed back, and "ok" is answered only when the mail provider
   really accepted the message. Secrets (RESEND_API_KEY, RATE_SALT) exist only as Worker secrets; they are never logged or returned. */
import schema from './schema.generated.js';
import { validate, reference, subject, body } from './core.js';

const MAX_BODY = schema.max_body_bytes;
const PLACEHOLDER_SALT = 'change-this-to-a-long-random-text';

function list(value) {
  return String(value || '').split(',').map((x) => x.trim()).filter(Boolean);
}

function allowedOrigins(env) {
  const out = [];
  for (const o of list(env.ALLOWED_ORIGINS)) {
    try {
      const u = new URL(o);
      if (u.protocol === 'https:' || u.hostname === 'localhost' || u.hostname === '127.0.0.1') {
        out.push(u.origin);
      }
    } catch (e) { /* an unusable entry is ignored */ }
  }
  return out;
}

/* Everything the service needs, or the reason it cannot work. The website must never see a success it did not get. */
export function missingConfig(env) {
  const missing = [];
  if (!allowedOrigins(env).length) missing.push('ALLOWED_ORIGINS');
  if (!list(env.MAIL_TO).length) missing.push('MAIL_TO');
  if (!env.MAIL_FROM) missing.push('MAIL_FROM');
  if (!env.RESEND_API_KEY) missing.push('RESEND_API_KEY');
  if (!env.RATE_SALT || env.RATE_SALT === PLACEHOLDER_SALT || String(env.RATE_SALT).length < 16) missing.push('RATE_SALT');
  if (!env.FORMS_KV || typeof env.FORMS_KV.get !== 'function' || typeof env.FORMS_KV.put !== 'function') missing.push('FORMS_KV');
  return missing;
}

function originOf(request) {
  const direct = request.headers.get('Origin');
  const src = direct !== null ? direct : request.headers.get('Referer');
  if (!src) return '';
  try {
    const u = new URL(src);
    return u.origin === 'null' ? '' : u.origin;
  } catch (e) {
    return '';
  }
}

function wantsJson(request) {
  return (request.headers.get('Accept') || '').toLowerCase().includes('application/json');
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

function reply(request, env, status, ok, message, extra = {}, corsOrigin = '') {
  const headers = {
    'Cache-Control': 'no-store',
    'X-Robots-Tag': 'noindex',
    'X-Content-Type-Options': 'nosniff',
  };
  if (corsOrigin) {
    headers['Access-Control-Allow-Origin'] = corsOrigin;
    headers.Vary = 'Origin';
  }
  if (status === 405) headers.Allow = 'POST, OPTIONS';
  if (wantsJson(request)) {
    headers['Content-Type'] = 'application/json; charset=utf-8';
    return new Response(JSON.stringify({ ok, message, ...extra }), { status, headers });
  }
  /* a browser without JavaScript posted the form: a small page of its own (it cannot use the website's stylesheet, which is on another origin) */
  headers['Content-Type'] = 'text/html; charset=utf-8';
  headers['Content-Security-Policy'] = "default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'";
  const title = ok ? 'Thank you' : 'We could not send this';
  const ref = extra.ref ? `<p>Reference: ${escapeHtml(extra.ref)}</p>` : '';
  const back = allowedOrigins(env)[0] || '';
  const link = back ? `<p><a href="${escapeHtml(back)}/index.html">Back to the website</a></p>` : '';
  const page = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex">`
    + `<title>${title} | Jame ul uloom</title><style>body{font:1.05rem/1.6 system-ui,sans-serif;max-width:34rem;margin:3rem auto;padding:0 1rem;color:#14213d}a{color:#14213d}</style></head>`
    + `<body><main><h1>${title}</h1><p>${escapeHtml(message)}</p>${ref}${link}</main></body></html>`;
  return new Response(page, { status, headers });
}

/* Reads the body but never more than `max` bytes, whatever Content-Length claims. Returns null when it is too large. */
async function readLimited(request, max) {
  if (!request.body) return new Uint8Array(0);
  const reader = request.body.getReader();
  const chunks = [];
  let total = 0;
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    total += value.byteLength;
    if (total > max) {
      await reader.cancel();
      return null;
    }
    chunks.push(value);
  }
  const out = new Uint8Array(total);
  let at = 0;
  for (const c of chunks) {
    out.set(c, at);
    at += c.byteLength;
  }
  return out;
}

async function sha256Hex(text) {
  const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return Array.from(new Uint8Array(digest), (b) => b.toString(16).padStart(2, '0')).join('');
}

/* Counters in KV, one per visitor-hour, visitor-day and service-day. Best effort (KV is not atomic), which is plenty against abuse
   of a school contact form. Returns an error message, or '' when the submission may go on. */
async function rateLimited(request, env) {
  const rate = {
    hour: Number(env.RATE_PER_IP_HOUR) || 5,
    day: Number(env.RATE_PER_IP_DAY) || 15,
    all: Number(env.RATE_GLOBAL_DAY) || 300,
  };
  const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
  const who = (await sha256Hex(`${ip}|${env.RATE_SALT}`)).slice(0, 32);
  const sec = Math.floor(Date.now() / 1000);
  const hourKey = `ip:${who}:h:${Math.floor(sec / 3600)}`;
  const dayKey = `ip:${who}:d:${Math.floor(sec / 86400)}`;
  const allKey = `all:d:${Math.floor(sec / 86400)}`;
  const counters = [[hourKey, rate.hour, 3700], [dayKey, rate.day, 90000], [allKey, rate.all, 90000]];
  const current = [];
  for (const [key, max] of counters) {
    const n = Number(await env.FORMS_KV.get(key)) || 0;
    if (n >= max) {
      return 'Too many messages have been sent just now. Please wait a little and try again, or call the office.';
    }
    current.push(n);
  }
  await Promise.all(counters.map(([key, , ttl], i) => env.FORMS_KV.put(key, String(current[i] + 1), { expirationTtl: ttl })));
  return '';
}

async function sendMail(env, subjectLine, text, replyTo) {
  const payload = { from: `Jame ul uloom website <${env.MAIL_FROM}>`, to: list(env.MAIL_TO), subject: subjectLine, text };
  if (replyTo) payload.reply_to = replyTo;
  try {
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(10000),
    });
    return r.status === 200;
  } catch (e) {
    return false;
  }
}

export default {
  async fetch(request, env) {
    const missing = missingConfig(env || {});
    if (missing.length) {
      console.log(`forms: not configured (${missing.join(', ')})`);   /* names only, never values */
      return reply(request, env || {}, 503, false, 'We could not send your message right now. Please try again a little later, or call or email the office.');
    }
    const origin = originOf(request);
    const okOrigin = allowedOrigins(env).includes(origin);
    const cors = okOrigin ? origin : '';

    if (request.method === 'OPTIONS') {
      if (!okOrigin) return new Response(null, { status: 403 });
      return new Response(null, {
        status: 204,
        headers: {
          'Access-Control-Allow-Origin': origin, Vary: 'Origin', 'Access-Control-Allow-Methods': 'POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Accept, Content-Type', 'Access-Control-Max-Age': '600', 'Cache-Control': 'no-store',
        },
      });
    }
    if (request.method !== 'POST') {
      return reply(request, env, 405, false, 'This address only accepts the website forms.', {}, cors);
    }
    if (Number(request.headers.get('Content-Length') || 0) > MAX_BODY) {
      return reply(request, env, 413, false, 'That message is too large. Please shorten it and try again.', {}, cors);
    }
    if (!okOrigin) {
      console.log('forms: rejected: origin');
      return reply(request, env, 403, false, 'This form can only be sent from the Jame ul uloom website.');
    }
    const bytes = await readLimited(request, MAX_BODY);
    if (bytes === null) {
      return reply(request, env, 413, false, 'That message is too large. Please shorten it and try again.', {}, cors);
    }
    let fd;
    try {
      fd = await new Response(bytes, { headers: { 'Content-Type': request.headers.get('Content-Type') || '' } }).formData();
    } catch (e) {
      return reply(request, env, 400, false, 'This form is not recognised.', {}, cors);
    }
    const formName = String(fd.get('form') || '');
    if (!Object.prototype.hasOwnProperty.call(schema.forms, formName)) {
      return reply(request, env, 400, false, 'This form is not recognised.', {}, cors);
    }
    if (String(fd.get('website') || '').trim() !== '') {   /* hidden field that only robots fill in */
      console.log(`forms: rejected: honeypot (${formName})`);
      return reply(request, env, 400, false, 'This message could not be accepted.', {}, cors);
    }
    const opened = Number.parseInt(String(fd.get('opened') || '0'), 10) || 0;   /* milliseconds since the page was opened, measured in the browser */
    const minFill = (Number(env.MIN_FILL_SECONDS) || 2) * 1000;
    if (opened > 0 && opened < minFill) {
      console.log(`forms: rejected: too fast (${formName})`);
      return reply(request, env, 400, false, 'That was very quick. Please take a moment to check your message and send it again.', {}, cors);
    }
    const { values, errors } = validate(schema, formName, fd);
    if (Object.keys(errors).length) {
      return reply(request, env, 422, false, 'Please check the highlighted fields.', { errors }, cors);
    }
    const limited = await rateLimited(request, env);
    if (limited) {
      console.log(`forms: rejected: rate limit (${formName})`);
      return reply(request, env, 429, false, limited, {}, cors);
    }
    const ref = reference(formName);
    const mailed = await sendMail(env, subject(schema, formName, values), body(schema, formName, values, ref), values.email || '');
    console.log(`forms: ${mailed ? 'sent' : 'MAIL FAILED'} ${formName} ${ref}`);   /* reference only: no personal data in the log */
    if (!mailed) {
      return reply(request, env, 503, false, 'We could not send your message just now. Please try again in a few minutes, or call or email the office directly.', {}, cors);
    }
    return reply(request, env, 200, true, 'Your message has reached the Jame ul uloom office.', { ref }, cors);
  },
};
