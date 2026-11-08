// Cloudflare Pages Function: POST /api/waitlist  { "email": "...", "company": "" }
// Stores each address once in the WAITLIST KV namespace as  email:<address>  ->  { email, joined }.
//
// Hardened 8 Nov 2026:
// - Only the live site's own pages can sign up: the Origin header must be present and be lumavu.app (or www).
//   Preview deployments answer as if it worked but store nothing, so they can't add to the real list.
// - The body is capped at 1 KB and read as text before parsing; the address is length-checked (characters and
//   bytes, since KV keys are limited to 512 bytes) before any pattern runs, and the pattern can't backtrack badly.
// - The honeypot field ("company") is checked here as well as in the page.
// - The answer is the same whether or not the address was already on the list, so the list can't be probed.
// - Storage errors come back as a plain 503 instead of a crash page.
// Abuse volume is handled in front of this by a Cloudflare rate-limiting rule on /api/waitlist.

const LIVE_HOSTS = new Set(["lumavu.app", "www.lumavu.app"]);
const MAX_BODY = 1024;
// local@domain.tld: no spaces, one @, at least one dot in the domain, no empty labels. Linear time.
const EMAIL = /^[^\s@]{1,64}@[^\s@.]+(?:\.[^\s@.]+)+$/;
// Control characters and bidi overrides have no place in an address.
const BAD_CHARS = /[\u0000-\u001f\u007f-\u009f​-‏‪-‮⁦-⁩]/;

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
      "x-content-type-options": "nosniff",
    },
  });

const fail = (status, error) => json({ ok: false, error }, status);
const done = (form) =>
  form
    ? new Response(null, { status: 303, headers: { location: "/#waitlist", "cache-control": "no-store" } })
    : json({ ok: true });

function hostOf(value) {
  try {
    return new URL(value).host;
  } catch {
    return null;
  }
}

export async function onRequestPost({ request, env }) {
  const host = new URL(request.url).host;
  const origin = request.headers.get("origin");
  if (!origin || hostOf(origin) !== host) return fail(403, "Sign up from the Lumavu website");

  const type = (request.headers.get("content-type") || "").toLowerCase();
  const form = type.startsWith("application/x-www-form-urlencoded");
  if (!form && !type.startsWith("application/json")) return fail(415, "Enter your email address and try again");
  const declared = Number(request.headers.get("content-length") || 0);
  if (declared > MAX_BODY) return fail(413, "Enter your email address and try again");

  let text;
  try {
    text = await request.text();
  } catch {
    return fail(400, "Enter your email address and try again");
  }
  if (text.length > MAX_BODY) return fail(413, "Enter your email address and try again");

  let fields;
  try {
    fields = form ? Object.fromEntries(new URLSearchParams(text)) : JSON.parse(text);
  } catch {
    return fail(400, "Enter your email address and try again");
  }
  if (!fields || typeof fields !== "object") return fail(400, "Enter your email address and try again");

  // Filled in only by bots: pretend it worked.
  if (typeof fields.company === "string" && fields.company.trim()) return done(form);

  const email = (typeof fields.email === "string" ? fields.email : "").trim().toLowerCase();
  const bytes = new TextEncoder().encode(email).length;
  if (!email || email.length > 254 || bytes > 254 || BAD_CHARS.test(email) || !EMAIL.test(email)) {
    return fail(400, "That email address doesn't look right. Check it and try again");
  }

  // Preview deployments share the production binding; never write from them.
  if (!LIVE_HOSTS.has(host)) return done(form);
  if (!env.WAITLIST) return fail(503, "The waitlist isn't open yet. Try again soon");

  const key = `email:${email}`;
  try {
    if (!(await env.WAITLIST.get(key))) {
      await env.WAITLIST.put(key, JSON.stringify({ email, joined: new Date().toISOString() }));
    }
  } catch {
    return fail(503, "That didn't go through. Try again in a moment");
  }
  return done(form);
}

export function onRequest() {
  return new Response("Method not allowed", { status: 405, headers: { allow: "POST", "x-content-type-options": "nosniff" } });
}
