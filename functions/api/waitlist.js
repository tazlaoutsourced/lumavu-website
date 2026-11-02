// Cloudflare Pages Function: POST /api/waitlist  { "email": "..." }
// Stores each address once in the WAITLIST KV namespace as  email:<address>  ->  { email, joined }.
const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
  });

export async function onRequestPost({ request, env }) {
  // Only accept posts from this site's own pages.
  const origin = request.headers.get("origin");
  if (origin && new URL(origin).host !== new URL(request.url).host) {
    return json({ ok: false, error: "Sign up from the Lumavu website" }, 403);
  }
  let body;
  try {
    body = await request.json();
  } catch {
    return json({ ok: false, error: "Enter your email address and try again" }, 400);
  }
  const email = String(body?.email || "").trim().toLowerCase();
  if (!EMAIL.test(email) || email.length > 254) {
    return json({ ok: false, error: "That email address doesn't look right. Check it and try again" }, 400);
  }
  if (!env.WAITLIST) {
    return json({ ok: false, error: "The waitlist isn't open yet. Try again soon" }, 503);
  }
  const key = `email:${email}`;
  if (await env.WAITLIST.get(key)) return json({ ok: true, already: true });
  await env.WAITLIST.put(key, JSON.stringify({ email, joined: new Date().toISOString() }));
  return json({ ok: true });
}

export function onRequestGet() {
  return new Response("Method not allowed", { status: 405, headers: { allow: "POST" } });
}
