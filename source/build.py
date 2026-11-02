#!/usr/bin/env python3
"""Builds the Lumavu website.

  public/        the site Cloudflare Pages serves (fonts self-hosted, waitlist posts to /api/waitlist)
  ../artifact/   the same pages for a claude.ai preview (Google Fonts, waitlist in preview mode)

Media: drop 16:9 stills into media/raw/<key>.png (or .jpg) and loops into media/raw/<key>.mp4, then run again.
"""
import json, os, re, shutil, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "src"
# In the repo, this file lives in source/ and the site is built one level up, into public/.
IN_REPO = HERE.name == "source"
OUT = Path(os.environ.get("LUMAVU_OUT", HERE.parent if IN_REPO else HERE / "dist" / "Website"))
PUB = OUT / "public"
ART = Path(os.environ.get("LUMAVU_ART", HERE.parent / ".preview" if IN_REPO else HERE / "dist" / "artifact"))
RAW = Path(os.environ.get("LUMAVU_RAW", HERE.parent / "_media" / "raw" if IN_REPO else HERE / "media" / "raw"))
ICON = Path(os.environ.get("LUMAVU_ICON", HERE / "media" / "icon-1024.png"))
FONTS_SRC = HERE / "node_modules"

sys.path.insert(0, str(SRC))
from pages import PAGES  # noqa: E402

# seconds of crossfade from each loop's end back into its start. Motorsport needs none: the camera tracks the car and the
# background pans straight through the seam. Football pans across the pitch, so it gets a quick dissolve that reads like
# a broadcast cutting between cameras.
XFADE = {"news": 0.4, "dunes": 0.5, "leopard": 0.5, "football": 0.4, "salt-road": 0.5}
# full-size width and quality where a loop is shown large; the hero also gets a 1280-wide copy for phones
FULL = {"dunes": (1600, "19"), "salt-road": (1920, "20")}
MEDIUM = {"salt-road"}
# Seedance reframes and regrades its first frame a little, so where a loop fades in over a still that everyone sees first,
# the still is taken from the loop itself (<key>-loop.jpg) and the hand-over is invisible
LOOP_STILL = {"salt-road"}
# loops cut together from several shots, like a trailer. Seedance couldn't bring the walking caravan back to its opening
# frame, so the hero cuts from the walking shot to a wider one. That's a straight cut, which reads as an edit; the wide shot
# drifts back to the walking shot's framing, so the return to the start is the usual short blend (XFADE).
SEQUENCE = {"salt-road": ["salt-road-walk", "salt-road-aerial"]}
SEQ_FADE = 0  # seconds of dissolve between shots; 0 for straight cuts


def probe_duration(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                                capture_output=True, text=True, check=True).stdout.strip())


def sequence(key):
    """Joins a loop's shots into one high-quality intermediate, or returns None until every shot is in media/raw."""
    parts = [RAW / f"{name}.mp4" for name in SEQUENCE[key]]
    if not all(p.exists() for p in parts):
        return None
    out = OUT / ".seq" / f"{key}.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists() and out.stat().st_mtime >= max(p.stat().st_mtime for p in parts):
        return out
    durs = [probe_duration(p) for p in parts]
    args = [a for p in parts for a in ("-i", str(p))]
    graph = ";".join(f"[{i}:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=24,format=yuv420p,"
                     f"setpts=PTS-STARTPTS[s{i}]" for i in range(len(parts)))
    if SEQ_FADE:
        prev, acc = "s0", durs[0]
        for i in range(1, len(parts)):
            graph += f";[{prev}][s{i}]xfade=transition=fade:duration={SEQ_FADE}:offset={acc - SEQ_FADE:.3f}[x{i}]"
            prev, acc = f"x{i}", acc + durs[i] - SEQ_FADE
    else:
        graph += ";" + "".join(f"[s{i}]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=1:a=0[cat]"
        prev = "cat"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args, "-filter_complex", graph, "-map", f"[{prev}]", "-an",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-pix_fmt", "yuv420p", str(out)], check=True)
    return out
KEYS = ["salt-road", "glass-harbour", "northern-quiet", "orbit-nine", "midnight-souk", "ember-coast", "saffron",
        "kingdom-of-glass", "lanterns", "paper-moons", "news", "football", "dunes", "earth", "concert", "kids",
        "farmhouse", "undertow", "leopard", "motorsport"]

GOOGLE_FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
                '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
                '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@400..700'
                '&family=Red+Hat+Mono:wght@500;600&family=Red+Hat+Text:wght@400;500;600&display=swap">')

FONT_FILES = {
    "red-hat-display.woff2": "@fontsource-variable/red-hat-display/files/red-hat-display-latin-wght-normal.woff2",
    "red-hat-text-400.woff2": "@fontsource/red-hat-text/files/red-hat-text-latin-400-normal.woff2",
    "red-hat-text-500.woff2": "@fontsource/red-hat-text/files/red-hat-text-latin-500-normal.woff2",
    "red-hat-text-600.woff2": "@fontsource/red-hat-text/files/red-hat-text-latin-600-normal.woff2",
    "red-hat-mono-500.woff2": "@fontsource/red-hat-mono/files/red-hat-mono-latin-500-normal.woff2",
    "red-hat-mono-600.woff2": "@fontsource/red-hat-mono/files/red-hat-mono-latin-600-normal.woff2",
}
SELF_FONTS = ('<link rel="preload" href="assets/fonts/red-hat-display.woff2" as="font" type="font/woff2" crossorigin>'
              '<link rel="preload" href="assets/fonts/red-hat-text-400.woff2" as="font" type="font/woff2" crossorigin>'
              "<style>"
              '@font-face{font-family:"Red Hat Display";src:url(assets/fonts/red-hat-display.woff2) format("woff2");font-weight:300 900;font-display:swap}'
              '@font-face{font-family:"Red Hat Text";src:url(assets/fonts/red-hat-text-400.woff2) format("woff2");font-weight:400;font-display:swap}'
              '@font-face{font-family:"Red Hat Text";src:url(assets/fonts/red-hat-text-500.woff2) format("woff2");font-weight:500;font-display:swap}'
              '@font-face{font-family:"Red Hat Text";src:url(assets/fonts/red-hat-text-600.woff2) format("woff2");font-weight:600;font-display:swap}'
              '@font-face{font-family:"Red Hat Mono";src:url(assets/fonts/red-hat-mono-500.woff2) format("woff2");font-weight:500;font-display:swap}'
              '@font-face{font-family:"Red Hat Mono";src:url(assets/fonts/red-hat-mono-600.woff2) format("woff2");font-weight:600;font-display:swap}'
              "</style>")


def media():
    from PIL import Image, ImageDraw, ImageFilter
    dst = PUB / "assets" / "media"
    dst.mkdir(parents=True, exist_ok=True)
    videos = []
    manifest_p = OUT / ".media-sources.json"
    try:
        manifest = json.loads(manifest_p.read_text())
    except Exception:
        manifest = {}
    PH = HERE / "media" / "placeholders"
    for key in KEYS:
        src = next((RAW / f"{key}{ext}" for ext in (".png", ".jpg", ".jpeg", ".webp") if (RAW / f"{key}{ext}").exists()), None)
        if src is None:
            src = next((PH / f"{key}{ext}" for ext in (".jpg", ".png") if (PH / f"{key}{ext}").exists()), None)
        big, small = dst / f"{key}.jpg", dst / f"{key}-s.jpg"
        if src:
            stamp = f"{src}:{src.stat().st_mtime}"
            if manifest.get(key) != stamp or not big.exists():
                im = Image.open(src).convert("RGB")
                w, h = im.size
                if abs(w / h - 16 / 9) > 0.02:  # centre-crop to 16:9
                    th = round(w * 9 / 16)
                    if th <= h:
                        y = (h - th) // 2; im = im.crop((0, y, w, y + th))
                    else:
                        tw = round(h * 16 / 9); x = (w - tw) // 2; im = im.crop((x, 0, x + tw, h))
                im.resize((1600, 900), Image.LANCZOS).save(big, "JPEG", quality=80, optimize=True, progressive=True)
                im.resize((640, 360), Image.LANCZOS).save(small, "JPEG", quality=78, optimize=True, progressive=True)
                manifest[key] = stamp
        vsrc = sequence(key) if key in SEQUENCE else RAW / f"{key}.mp4"
        if vsrc and vsrc.exists():
            # a full loop for big frames, and a 640-wide one for phone-sized tiles
            tiers = [(dst / f"{key}.mp4", *FULL.get(key, (1280, "22"))), (dst / f"{key}-s.mp4", 640, "23")]
            if key in MEDIUM:
                tiers.append((dst / f"{key}-m.mp4", 1280, "21"))
            for vdst, width, crf in tiers:
                if vdst.exists() and vdst.stat().st_mtime >= vsrc.stat().st_mtime:
                    continue
                vf = f"scale={width}:-2"  # keep Seedance's native 24 fps; padding to 30 would judder
                if key in XFADE:
                    d = XFADE[key]
                    dur = probe_duration(vsrc)
                    graph = (f"[0:v]{vf},split[a][b];[a]trim=start={d},setpts=PTS-STARTPTS[main];[b]trim=0:{d},setpts=PTS-STARTPTS[head];"
                             f"[main][head]xfade=transition=fade:duration={d}:offset={dur - 2 * d:.3f}[v]")
                    args = ["-filter_complex", graph, "-map", "[v]"]
                else:
                    args = ["-vf", vf]
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(vsrc), "-an", *args,
                                "-c:v", "libx264", "-preset", "veryfast", "-crf", crf, "-pix_fmt", "yuv420p",
                                "-movflags", "+faststart", str(vdst)], check=True)
            videos.append(key)
        if key in LOOP_STILL:
            still = dst / f"{key}-loop.jpg"
            full = dst / f"{key}.mp4"
            if full.exists():
                if not still.exists() or still.stat().st_mtime < full.stat().st_mtime:
                    tmp = dst / f".{key}-f0.png"
                    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(full), "-frames:v", "1", str(tmp)], check=True)
                    Image.open(tmp).convert("RGB").resize((1600, 900), Image.LANCZOS).save(still, "JPEG", quality=82, optimize=True, progressive=True)
                    tmp.unlink()
            elif big.exists():
                still.write_bytes(big.read_bytes())
    manifest_p.write_text(json.dumps(manifest, indent=1))
    return videos


def icons():
    from PIL import Image
    dst = PUB / "assets" / "img"
    dst.mkdir(parents=True, exist_ok=True)
    if not ICON.exists():
        return
    im = Image.open(ICON).convert("RGB")
    og = HERE / "media" / "og.jpg"
    if og.exists():
        shutil.copyfile(og, dst / "og.jpg")
    for size, name in ((180, "icon-180.png"), (512, "icon-512.png"), (64, "icon-64.png"), (64, "favicon-64.png")):
        im.resize((size, size), Image.LANCZOS).save(dst / name, optimize=True)


def fonts():
    dst = PUB / "assets" / "fonts"
    dst.mkdir(parents=True, exist_ok=True)
    for name, rel in FONT_FILES.items():
        shutil.copyfile(FONTS_SRC / rel, dst / name)


def webkit(css):
    """Safari before 18 only knows the prefixed backdrop-filter."""
    import re as _re
    css = _re.sub(r"\s*-webkit-backdrop-filter:\s*[^;}]+;?", "", css)
    return _re.sub(r"(?<![-\w])backdrop-filter:\s*([^;}]+)", r"backdrop-filter: \1; -webkit-backdrop-filter: \1", css)


def page_doc(title, head_extra, body, lang="en-GB"):
    return (f'<!doctype html>\n<html lang="{lang}">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            f"{head_extra}\n</head>\n<body>\n{body}\n</body>\n</html>\n")


def build_index(videos, fonts_html, preview):
    head = (SRC / "head.html").read_text().replace("<!--FONTS-->", fonts_html)
    css = webkit((SRC / "styles.css").read_text())
    body = (SRC / "sprite.html").read_text() + "\n" + (SRC / "body-main.html").read_text()
    js = (SRC / "app.js").read_text()
    cfg = f"<script>window.LUMAVU_VIDEOS={json.dumps(videos)};{'window.LUMAVU_PREVIEW=true;' if preview else ''}</script>"
    inner_head = f"{head}<style>\n{css}\n</style>"
    inner_body = f"{body}\n{cfg}\n<script>\n{js}\n</script>"
    if preview:
        return f"{inner_head}\n{inner_body}\n"
    return page_doc("Lumavu", inner_head, inner_body)


def build_page(fname, title, eyebrow, h1, toc, content, fonts_html):
    css = webkit((SRC / "page.css").read_text())
    toc_html = "".join(f'<a href="#{a}">{t}</a>' for a, t in toc)
    nav = "".join(f'<a href="{f}"{" aria-current=\"page\"" if f == fname else ""}>{n}</a>'
                  for f, n in (("support.html", "Support"), ("privacy.html", "Privacy"), ("terms.html", "Terms")))
    head = (f"<title>{title}</title>\n<meta name=\"description\" content=\"{h1} for Lumavu, the IPTV player for iPhone, iPhone Duo, iPad, Mac and Apple TV.\">\n"
            f'<link rel="canonical" href="https://lumavu.app/{fname[:-5]}">\n'
            f'<meta name="theme-color" content="#07060d">\n<link rel="icon" type="image/png" sizes="64x64" href="assets/img/favicon-64.png">\n'
            f'<link rel="apple-touch-icon" href="assets/img/icon-180.png">\n{fonts_html}\n<style>\n{css}\n</style>')
    body = f"""<div class="glow" aria-hidden="true"></div>
<header class="bar"><div class="wrap"><a class="brand" href="index.html"><svg viewBox="0 0 100 100" aria-hidden="true"><defs><linearGradient id="bg-g" x1=".15" y1=".05" x2=".85" y2="1"><stop offset="0" stop-color="#fdfcff"/><stop offset=".5" stop-color="#e9e3fc"/><stop offset="1" stop-color="#b9a9f0"/></linearGradient></defs><path d="M36.17 18.92 L78.63 43.08 Q90.8 50 78.63 56.92 L36.17 81.08 Q24 88 24 74 L24 26 Q24 12 36.17 18.92 Z" fill="url(#bg-g)" stroke="#8f74e8" stroke-opacity=".35"/></svg>Lumavu</a><nav aria-label="Pages">{nav}</nav></div></header>
<main><div class="wrap doc"><nav class="toc" aria-label="On this page">{toc_html}</nav>
<article><h1>{h1}</h1>
{content}
</article></div></main>
<footer><div class="wrap"><a href="index.html">Lumavu</a><a href="support.html">Support</a><a href="privacy.html">Privacy</a><a href="terms.html">Terms</a><span class="r">Made by <a href="https://thinkersandbuilders.co.uk" target="_blank" rel="noopener">Thinkers &amp; Builders</a></span></div></footer>
<script>
(function(){{var b=document.getElementById('copy'),a=document.getElementById('addr');if(!b||!a)return;
b.addEventListener('click',function(){{var t=a.textContent;var done=function(){{b.textContent='Copied';setTimeout(function(){{b.textContent='Copy'}},1800)}};
var sel=function(){{var r=document.createRange();r.selectNodeContents(a);var s=getSelection();s.removeAllRanges();s.addRange(r);b.textContent='Selected'}};
if(navigator.clipboard&&navigator.clipboard.writeText){{navigator.clipboard.writeText(t).then(done,sel)}}else sel()}})}})();
</script>"""
    return page_doc(title, head, body)


def main():
    PUB.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    fonts()
    icons()
    videos = media()
    (PUB / "index.html").write_text(build_index(videos, SELF_FONTS, preview=False))
    (ART / "index.html").write_text(build_index(videos, GOOGLE_FONTS, preview=True))
    for fname, title, eyebrow, h1, toc, content in PAGES:
        (PUB / fname).write_text(build_page(fname, title, eyebrow, h1, toc, content, SELF_FONTS))
        (ART / fname).write_text(build_page(fname, title, eyebrow, h1, toc, content, GOOGLE_FONTS))
    # Cloudflare extras
    (PUB / "_headers").write_text("""/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: DENY
  Permissions-Policy: camera=(), microphone=(), geolocation=(), interest-cohort=()

/assets/*
  Cache-Control: public, max-age=604800
""")
    (PUB / "robots.txt").write_text("User-agent: *\nAllow: /\n\nSitemap: https://lumavu.app/sitemap.xml\n")
    urls = "".join(f"  <url><loc>https://lumavu.app/{p}</loc></url>\n" for p in ("", "support", "privacy", "terms"))
    (PUB / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    print(json.dumps({"videos": videos, "out": str(OUT), "artifact": str(ART)}))


if __name__ == "__main__":
    main()
