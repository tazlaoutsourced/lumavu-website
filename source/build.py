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
<header class="bar"><div class="wrap"><a class="brand" href="index.html" aria-label="Lumavu home"><svg viewBox="0 0 100 100" aria-hidden="true"><defs><linearGradient id="bg-g" x1=".15" y1=".05" x2=".85" y2="1"><stop offset="0" stop-color="#fdfcff"/><stop offset=".5" stop-color="#e9e3fc"/><stop offset="1" stop-color="#b9a9f0"/></linearGradient></defs><path d="M36.17 18.92 L78.63 43.08 Q90.8 50 78.63 56.92 L36.17 81.08 Q24 88 24 74 L24 26 Q24 12 36.17 18.92 Z" fill="url(#bg-g)" stroke="#8f74e8" stroke-opacity=".35"/></svg><svg class="wm" viewBox="0 0 3366.3 693.0" aria-hidden="true"><path d="M0 656L0 24C0 9.1 9.1 0 24 0L76 0C90.9 0 100 9.1 100 24L100 656C100 670.9 90.9 680 76 680L24 680C9.1 680 0 670.9 0 656ZM208 203.1L208 468.7C208 592.6 308.4 693 432.3 693C556.1 693 656.6 592.6 656.6 468.7L656.6 203.1C656.6 188.2 647.4 179.1 632.6 179.1L580.6 179.1C565.7 179.1 556.6 188.2 556.6 203.1L556.6 473.7C556.6 542.4 500.9 598 432.3 598C363.6 598 308 542.4 308 473.7L308 203.1C308 188.2 298.9 179.1 284 179.1L232 179.1C217.1 179.1 208 188.2 208 203.1ZM788.5 680L840.5 680C855.4 680 864.5 670.9 864.5 656L864.5 392.2C864.5 369.6 870 348.9 881 330C892 311.1 906.8 295.9 925.4 284.3C943.9 272.8 964.3 267.1 986.5 267.1C1009.1 267.1 1029.6 272.5 1048.2 283.4C1066.8 294.3 1081.5 309.2 1092.5 328C1103.4 346.8 1108.9 368.2 1108.9 392.2L1108.9 656C1108.9 670.9 1118 680 1132.9 680L1184.9 680C1199.7 680 1208.9 670.9 1208.9 656L1208.9 392.2C1208.9 368.2 1214.4 346.8 1225.4 328C1236.4 309.2 1251.1 294.3 1269.5 283.4C1288 272.5 1308.5 267.1 1331 267.1C1353.6 267.1 1374.1 272.8 1392.5 284.3C1410.9 295.9 1425.5 311.1 1436.5 330C1447.5 348.9 1453 369.6 1453 392.2L1453 656C1453 670.9 1462.2 680 1477 680L1529 680C1543.9 680 1553 670.9 1553 656L1553 366.8C1553 329.7 1544 296 1526 265.6C1508 235.3 1483.8 211.1 1453.4 193C1423 175 1389.3 166 1352.3 166C1316.4 166 1283.5 174.6 1253.7 191.9C1223.9 209.1 1200.1 232.1 1182.5 260.8C1164.9 232.1 1141.1 209.1 1111 191.9C1081 174.6 1047.9 166 1011.9 166C982.1 166 954.5 172.2 929 184.6C903.5 196.9 882 213.7 864.5 234.9L864.5 204C864.5 189.1 855.4 180 840.5 180L788.5 180C773.7 180 764.5 189.1 764.5 204L764.5 656C764.5 670.9 773.7 680 788.5 680ZM2081.9 205.3L2084.7 256.4C2066.4 229.8 2043.1 208.1 2014.9 191.3C1986.8 174.4 1954.3 166 1917.5 166C1881.7 166 1848.2 172.7 1817 186.2C1785.7 199.6 1758.2 218.2 1734.5 242C1710.8 265.8 1692.3 293.5 1679 324.9C1665.7 356.3 1659 389.9 1659 425.8C1659 462.7 1665.9 497.3 1679.6 529.5C1693.4 561.7 1712.5 590 1736.9 614.5C1761.4 639.1 1789.7 658.3 1821.9 672.2C1854.1 686.1 1888.6 693 1925.5 693C1960.3 693 1990.4 684.9 2015.8 668.7C2041.2 652.5 2061.3 631.3 2076.2 605L2079.1 657.3C2079.9 671.4 2089 680 2103.1 680L2156.5 680C2171.4 680 2180.5 670.9 2180.5 656L2180.5 204C2180.5 189.1 2171.4 180 2156.5 180L2105.9 180C2090.2 180 2081.1 189.6 2081.9 205.3ZM1923.1 596.5C1894 596.5 1867.2 589.1 1842.7 574.3C1818.1 559.4 1798.5 539.4 1783.7 514.2C1768.9 489 1761.5 461 1761.5 430C1761.5 399.2 1768.7 371.2 1783.1 345.9C1797.5 320.6 1817 300.5 1841.5 285.6C1866.1 270.7 1893.3 263.2 1923.1 263.2C1952.9 263.2 1979.1 270.6 2001.5 285.4C2023.9 300.3 2041.4 320.3 2053.9 345.5C2066.4 370.7 2072.6 398.8 2072.6 430C2072.6 460.5 2066.4 488.5 2054 513.8C2041.6 539 2024.2 559.2 2001.8 574.1C1979.4 589 1953.1 596.5 1923.1 596.5ZM2283.8 179.1L2335.9 179.1C2345.1 179.1 2353.2 184 2357.3 192.2L2520.6 512.1C2538.3 546.7 2559.9 546.7 2577.6 512.1L2740.9 192.2C2745.1 184 2753.2 179.1 2762.3 179.1L2814.5 179.1C2840 179.1 2848 192.7 2835.3 214.9L2604.9 620.5C2567.7 686 2530.5 686 2493.3 620.5L2262.9 214.9C2250.3 192.7 2258.2 179.1 2283.8 179.1ZM2917.7 203.1L2917.7 468.7C2917.7 592.6 3018.1 693 3142 693C3265.8 693 3366.3 592.6 3366.3 468.7L3366.3 203.1C3366.3 188.2 3357.1 179.1 3342.3 179.1L3290.3 179.1C3275.4 179.1 3266.3 188.2 3266.3 203.1L3266.3 473.7C3266.3 542.4 3210.6 598 3142 598C3073.3 598 3017.7 542.4 3017.7 473.7L3017.7 203.1C3017.7 188.2 3008.6 179.1 2993.7 179.1L2941.7 179.1C2926.8 179.1 2917.7 188.2 2917.7 203.1Z"/></svg></a><nav aria-label="Pages">{nav}</nav></div></header>
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
