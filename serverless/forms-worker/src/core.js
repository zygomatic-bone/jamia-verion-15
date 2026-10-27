/* Validation and message building for the website forms: pure functions, no network, no secrets.
   The rules come from schema.js; the Feedback, Admissions and Careers pages use the same field names. */

/* Control and invisible "format" characters are removed (NUL, bell, zero-width space, byte-order mark, the bidirectional overrides
   and isolates that can make a name or address read back to front in a mail program ...). Four are KEPT because the languages of this
   community need them: U+200C and U+200D (zero-width non-joiner and joiner: Urdu and Persian word shapes, Kannada and Hindi
   conjuncts) and U+200E and U+200F (left-to-right and right-to-left marks used in mixed English and Urdu lines). */
const STRIP_LINE = /(?![\u200C\u200D\u200E\u200F])\p{C}/gu;
const STRIP_TEXT = /(?![\n\u200C\u200D\u200E\u200F])\p{C}/gu;
const HAS_CONTENT = /[\p{L}\p{N}\p{P}\p{S}]/u;
const LOCAL = /^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+$/;
const DOMAIN_LABEL = /^[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?$/;

export function clean(value, multiline) {
  let s = String(value).replace(/\0/g, '');
  if (s.includes('\uFFFD')) {
    return '';   /* the browser sent bytes that are not valid UTF-8: refuse the field instead of keeping replacement characters */
  }
  s = s.replace(/\r\n/g, '\n').replace(multiline ? STRIP_TEXT : STRIP_LINE, multiline ? '' : ' ');
  s = multiline ? s.replace(/\n{3,}/g, '\n\n') : s.replace(/\s+/gu, ' ');
  s = s.trim();
  return HAS_CONTENT.test(s) ? s : '';   /* text made only of the kept invisible characters is empty text */
}

export function length(s) {
  return Array.from(s).length;   /* characters, not UTF-16 units */
}

export function validEmail(v) {
  if (v.length > 254 || /[\r\n,;<>"\s]/.test(v)) {
    return false;
  }
  const at = v.lastIndexOf('@');
  if (at < 1) {
    return false;
  }
  const local = v.slice(0, at);
  const labels = v.slice(at + 1).split('.');
  return local.length <= 64 && LOCAL.test(local) && !local.startsWith('.') && !local.endsWith('.') && !local.includes('..')
    && labels.length >= 2 && labels.every((l) => DOMAIN_LABEL.test(l));
}

/* Returns { values, errors } for one form. `fd` is a FormData (or anything with getAll). */
export function validate(schema, formName, fd) {
  const def = schema.forms[formName];
  const choices = {};
  for (const [name, pairs] of Object.entries(schema.choices)) {
    choices[name] = new Map(pairs);
  }
  const values = {};
  const errors = {};
  for (const f of def.fields) {
    const all = fd.getAll(f.name);
    if (all.length > 1 || (all.length === 1 && typeof all[0] !== 'string')) {
      errors[f.name] = `${f.label} is not valid.`;   /* repeated fields and file uploads are never accepted */
      values[f.name] = '';
      continue;
    }
    const raw = all.length ? all[0] : '';
    let v = '';
    switch (f.type) {
      case 'bool':
        v = ['1', 'on', 'yes', 'true'].includes(raw.toLowerCase()) ? 'yes' : '';
        break;
      case 'int': {
        const n = /^[0-9]{1,6}$/.test(raw) ? Number(raw) : 0;
        v = n >= 1 && n <= f.limit ? String(n) : '';
        if (raw !== '' && v === '') {
          errors[f.name] = `Please choose a rating from 1 to ${f.limit}.`;
        }
        break;
      }
      case 'choice':
        v = choices[f.limit].has(raw) ? raw : '';
        if (raw !== '' && v === '') {
          errors[f.name] = 'Please choose one of the options.';
        }
        break;
      case 'phone': {
        v = clean(raw, false);
        const digits = v.replace(/\D/g, '');
        if (v !== '' && (!/^[0-9 +()-]{7,20}$/.test(v) || digits.length < 7 || digits.length > 15)) {
          errors[f.name] = 'Please enter a phone number we can call.';
          v = '';
        }
        break;
      }
      case 'email':
        v = clean(raw, false);
        if (v !== '' && (v.length > f.limit || !validEmail(v))) {
          errors[f.name] = 'Please enter a valid email address.';
          v = '';
        }
        break;
      default: {   /* line, text */
        v = clean(raw, f.type === 'text');
        if (length(v) > f.limit) {
          errors[f.name] = `${f.label} is too long (at most ${f.limit} characters).`;
          v = '';
        }
        const min = def.min[f.name] || 0;
        if (v !== '' && length(v) < min) {
          errors[f.name] = `Please write a little more (at least ${min} characters).`;
          v = '';
        }
      }
    }
    if (v === '' && f.required && !errors[f.name]) {
      errors[f.name] = f.type === 'bool' ? 'Please tick the box so that we may contact you.' : `Please fill in: ${f.label}.`;
    }
    values[f.name] = v;
  }
  return { values, errors };
}

const ALPHABET = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';

export function reference(formName) {
  const bytes = new Uint8Array(6);
  let s = '';
  for (let i = 0; i < 6; i += 1) {
    let b;
    do {
      crypto.getRandomValues(bytes.subarray(i, i + 1));
      b = bytes[i];
    } while (b >= 224);   /* 224 = 7 x 32: no modulo bias */
    s += ALPHABET[b % 32];
  }
  return `JU-${formName.slice(0, 2).toUpperCase()}-${s}`;
}

/* The subject is built from fixed words only; a visitor's text never reaches it. */
export function subject(schema, formName, values) {
  const def = schema.forms[formName];
  const label = (list, key) => new Map(schema.choices[list]).get(values[key]);
  let s = `[Jame ul uloom website] ${def.label}`;
  if (formName === 'feedback') {
    s += `: ${values.rating} of 5, ${label('category', 'category')}`;
  } else if (formName === 'admissions') {
    s += `: ${label('programme', 'programme')}`;
  } else {
    s += `: ${label('area', 'area')}`;
  }
  return s;
}

export function body(schema, formName, values, ref, now = new Date()) {
  const def = schema.forms[formName];
  const iso = now.toISOString();
  const lines = [`${def.label} received through the website`, `Reference: ${ref}`, `Received: ${iso.slice(0, 10)} ${iso.slice(11, 16)} UTC`, ''];
  for (const f of def.fields) {
    if (values[f.name] === '' || f.name === 'consent') {
      continue;
    }
    let val = values[f.name];
    if (f.type === 'choice') {
      val = new Map(schema.choices[f.limit]).get(val);
    } else if (f.type === 'int') {
      val = `${val} of ${f.limit} stars`;
    }
    lines.push(`${f.label}: ${f.type === 'text' ? `\n${val}\n` : val}`);
  }
  if (values.consent) {
    lines.push('The sender agreed to be contacted about this message.');
  }
  lines.push('', '--', 'Sent from the website form. Reply to this email to answer the sender (when they gave an address).');
  return lines.join('\n');
}
