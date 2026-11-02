# Lumavu website

A single long page about the app, plus support, privacy and terms pages. Built for Cloudflare Pages, with a small function that keeps the waitlist.

## What's in this folder

- `public/` is the site itself: `index.html` (the home page), `support.html`, `privacy.html`, `terms.html` and `assets/` (fonts, icons, the generated stills and loops).
- `functions/api/waitlist.js` saves waitlist sign-ups to Cloudflare KV, one entry per email address.
- `wrangler.toml` holds the Cloudflare Pages settings.
- `_media/` (not in git) holds the originals described below.
- `source/` holds the parts the pages are built from (`src/`) and `build.py`, which puts them together. Edit there, not in `public/`.
- `_media/raw/` is for the original Higgsfield stills and video loops, named by the keys in `build.py` (for example `salt-road.png`, `news.mp4`). Until a still is there, the build uses a soft, out-of-focus stand-in in the same colours (`source/media/placeholders/`), so the page never shows an empty frame.
- The six loops (the Salt Road hero, news, football, leopard, motorsport, dunes) were made with Seedance 2.5 from those stills. `source/fetch_loops.py` downloads them into `_media/raw/` again if they're ever lost. The build turns each into a full-size MP4 and a 640-wide one for phone-sized tiles, blends the end of each back into its start so it repeats without a jump (motorsport already loops on its own), and the page only plays them while they're on screen. The hero is two shots cut together like a trailer (`salt-road-walk.mp4`, the caravan walking with the camera alongside, then `salt-road-aerial.mp4`, a wider shot that drifts back to the opening framing), because Seedance couldn't bring a walking shot back to its first frame on its own. It waits until the rest of the page has loaded, and its still (`salt-road-loop.jpg`) is taken from the loop's own first frame, because Seedance reframes and regrades slightly; that way the moment the video takes over can't be seen. With reduced motion turned on, the stills stay put instead.

## Putting it live

This repo is connected to the `lumavu-website` project on Cloudflare Pages, which serves lumavu.app. A push to `main` goes live a minute or so later. A push to any other branch gets its own preview address on `lumavu-website.pages.dev` and leaves the live site alone. Pages runs no build: it serves `public/` as committed and turns `functions/` into the waitlist endpoint, with the settings in `wrangler.toml` (including the WAITLIST namespace).

So a change goes: edit `source/`, run `python3 source/build.py` to rebuild `public/`, commit both, push.

The pages give `https://lumavu.app` as their address (the canonical links, the link-preview image and `sitemap.xml`).

## Reading the waitlist

`npx wrangler kv key list --namespace-id <the id> --remote` lists everyone. Each value holds the address and the date they joined. It's also visible in the dashboard under Storage & Databases, then KV, then WAITLIST. The privacy policy promises the list is used once, on launch day, and deleted afterwards.

## Before launch

- The privacy policy, terms and support pages are written from what the app does today (Keychain, on-device subtitles, no analytics). They aren't legal advice, so have someone check them, and add the company's registered name and address if Thinkers & Builders is a limited company.
- The terms assume the law of England and Wales.
- The prices are the ones suggested in the app's README (£2.99 a month, £19.99 a year with 7 days free, £49.99 lifetime).
- Every channel, film, series and image on the site is invented. The stills and loops were generated with Higgsfield for this site.
