// Pure guard functions for the twin Worker. No network, no secrets, easy to test.

// Input: make hidden-character and look-alike tricks harmless before the model sees them.
const INVISIBLE = /[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F-\u009F­͏؜ᅟᅠ឴឵᠋-᠎​-‏‪-‮⁠-⁯ㅤ︀-️﻿ﾠ\u{E0000}-\u{E007F}\u{1BCA0}-\u{1BCA3}]/gu;

export function cleanInput(raw, max = 400) {
  if (typeof raw !== "string") return "";
  let s = raw.normalize("NFKC").replace(INVISIBLE, "");
  s = s.replace(/[<>]/g, " "); // nobody can fake our delimiter tags
  s = s.replace(/\s+/g, " ").trim();
  return s.slice(0, max);
}

// Encoded payload smuggling: a long run with no spaces is not a human question.
export function looksLikePayload(s) {
  if (/[^\s]{45,}/.test(s)) return true;
  const letters = s.replace(/[\s\p{P}]/gu, "");
  if (letters.length > 60 && /^[A-Za-z0-9+/=]+$/.test(letters)) return true;
  return false;
}

const b64 = (t) => btoa(unescape(encodeURIComponent(t)));
const hex = (t) => [...new TextEncoder().encode(t)].map((b) => b.toString(16).padStart(2, "0")).join("");
const rot13 = (t) => t.replace(/[a-z]/gi, (c) => { const b = c <= "Z" ? 65 : 97; return String.fromCharCode(((c.charCodeAt(0) - b + 13) % 26) + b); });
const squash = (t) => t.normalize("NFKC").toLowerCase().replace(INVISIBLE, "").replace(/[^\p{L}\p{N}]/gu, "");

// Output: did the secret phrase come out in any common disguise?
export function canaryHit(out, canary) {
  if (!canary) return true; // fail closed
  const c = canary.toLowerCase();
  const o = out.normalize("NFKC").toLowerCase().replace(INVISIBLE, "");
  const flat = squash(out);
  const cflat = squash(canary);
  const forms = [cflat, [...cflat].reverse().join(""), squash(rot13(canary)), squash(hex(c)), squash(b64(c)), squash(b64(canary))];
  if (forms.some((f) => f.length >= 6 && flat.includes(f))) return true;
  // partial leaks: any 5-character window of the phrase (plain or reversed), or any word part of it
  for (const form of [cflat, forms[1]]) {
    for (let i = 0; i + 5 <= form.length; i++) if (flat.includes(form.slice(i, i + 5))) return true;
  }
  const words = c.split(/[^a-z0-9]+/).filter((w) => w.length >= 4 && /[a-z]/.test(w));
  if (words.some((w) => o.includes(w) || flat.includes(w))) return true;
  // base64/hex blobs that decode to the phrase
  for (const m of o.match(/[a-z0-9+/=]{12,}/g) || []) {
    try { if (squash(atob(m)).includes(cflat)) return true; } catch { /* not base64 */ }
  }
  return false;
}

// Output: did the instructions leak? Any 28-char window of the rules showing up counts.
export function leaksPrompt(out, instructions) {
  const o = squash(out);
  const src = squash(instructions);
  for (let i = 0; i + 28 <= src.length; i += 7) {
    if (o.includes(src.slice(i, i + 28))) return true;
  }
  return false;
}

export const PRICE = /(?:US\$|HK\$|RMB|CNY|USD|EUR|AED|[$¥€£])\s?\d|\d[\d,.]*\s?(?:USD|RMB|CNY|EUR|AED|dollars?|yuan|元|块|美元|港币|港元)|[零一二两三四五六七八九十百千万]+\s?(?:元|块|美元|港币)/i;
export const PROMISE = /\b(?:i|we)\s+(?:promise|guarantee|commit|will deliver|will certify)\b|\bguaranteed? (?:delivery|price|quality|results?)\b|我(?:保证|承诺|担保)|保证(?:交付|价格|质量)/i;

const SAFE_HOSTS = ["linkedin.com", "github.com", "jasonyou1995.github.io"];
const SAFE_MAIL = ["shengwei.you@gmail.com"];

// Output: nothing clickable, executable or exfiltrating gets through, except our own links.
export function unsafeOutput(out) {
  if (/```|<\s*\/?\s*[a-z][^>]*>|!\[|\]\(|javascript:|data:/i.test(out)) return "markup";
  for (const m of out.match(/(?:https?:\/\/|www\.)[^\s)]+/gi) || []) {
    const host = m.replace(/^https?:\/\//i, "").replace(/^www\./i, "").split(/[/?#]/)[0].toLowerCase();
    if (!SAFE_HOSTS.some((h) => host === h || host.endsWith("." + h))) return "link";
  }
  for (const m of out.match(/[\w.+-]+@[\w-]+(?:\.[\w-]+)+/g) || []) {
    if (!SAFE_MAIL.includes(m.toLowerCase())) return "mail";
  }
  return "";
}

export function vet(out, { canary, instructions }) {
  if (!out || !out.trim()) return { ok: false, why: "empty" };
  if (canaryHit(out, canary)) return { ok: false, why: "canary" };
  if (leaksPrompt(out, instructions)) return { ok: false, why: "prompt" };
  if (PRICE.test(out)) return { ok: false, why: "price" };
  if (PROMISE.test(out)) return { ok: false, why: "promise" };
  const u = unsafeOutput(out);
  if (u) return { ok: false, why: u };
  return { ok: true, why: "" };
}
