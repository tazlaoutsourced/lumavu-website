"""Defocused stand-in stills, matched to each generated image's mood, used until the real Higgsfield stills are in media/raw."""
import numpy as np
from PIL import Image, ImageFilter
from pathlib import Path
OUT = Path(__file__).parent / "media" / "placeholders"; OUT.mkdir(parents=True, exist_ok=True)
W, H = 1600, 900
rng = np.random.default_rng(7)
def hexc(h): h = h.lstrip('#'); return np.array([int(h[i:i+2], 16) for i in (0, 2, 4)], float) / 255
def vgrad(stops):
    y = np.linspace(0, 1, H)[:, None]
    img = np.zeros((H, W, 3))
    pos = [p for p, _ in stops]; cols = [hexc(c) for _, c in stops]
    for ch in range(3):
        img[..., ch] = np.interp(y, pos, [c[ch] for c in cols]).repeat(W, 1)
    return img
def blob(img, cx, cy, rx, ry, col, a):
    yy, xx = np.mgrid[0:H, 0:W]
    d = ((xx - cx * W) / (rx * W)) ** 2 + ((yy - cy * H) / (ry * H)) ** 2
    m = np.exp(-d * 2.2)[..., None] * a
    return img * (1 - m) + hexc(col) * m
def glow(img, cx, cy, r, col, a):
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.sqrt(((xx - cx * W)) ** 2 + ((yy - cy * H)) ** 2) / (r * W)
    return img + hexc(col) * (np.exp(-d * d * 3) * a)[..., None]
def bokeh(img, n, y0, y1, cols, rmin, rmax, a, seed):
    r = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:H, 0:W]
    for _ in range(n):
        cx, cy, rad = r.uniform(0, W), r.uniform(y0 * H, y1 * H), r.uniform(rmin, rmax)
        x0, x1, ya, yb = int(max(0, cx - rad - 2)), int(min(W, cx + rad + 2)), int(max(0, cy - rad - 2)), int(min(H, cy + rad + 2))
        if x1 <= x0 or yb <= ya: continue
        sub = np.sqrt((xx[ya:yb, x0:x1] - cx) ** 2 + (yy[ya:yb, x0:x1] - cy) ** 2)
        m = np.clip((rad - sub) / 2.5, 0, 1) * (0.55 + 0.45 * (sub / rad) ** 3) * a * r.uniform(.5, 1)
        img[ya:yb, x0:x1] += hexc(cols[r.integers(len(cols))]) * m[..., None]
    return img
def ridge(img, base, amp, freq, col, seed, soft=40):
    r = np.random.default_rng(seed)
    x = np.linspace(0, 1, W)
    y = base + sum(amp / (k + 1) * np.sin(2 * np.pi * (freq * (k + 1)) * x + r.uniform(0, 6)) for k in range(3))
    yy = np.arange(H)[:, None] / H
    m = np.clip((yy - y[None, :]) * H / soft + .5, 0, 1)
    return img * (1 - m[..., None]) + hexc(col) * m[..., None]
def finish(img, name, blur=10, vig=.55):
    img = np.clip(img, 0, 1)
    yy, xx = np.mgrid[0:H, 0:W]
    v = 1 - vig * (((xx - W / 2) / (W / 2)) ** 2 * .6 + ((yy - H / 2) / (H / 2)) ** 2 * .5)
    img = img * np.clip(v, 0, 1)[..., None]
    im = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(blur))
    a = np.asarray(im).astype(float) + rng.normal(0, 5, (H, W, 1))
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(OUT / f"{name}.png")

S = {}
S['salt-road'] = lambda: ridge(ridge(glow(vgrad([(0, '#2b1d45'), (.45, '#a8566a'), (.62, '#f3a85e'), (1, '#f3a85e')]), .72, .56, .22, '#ffd9a0', .9), .66, .05, 1.1, '#9a5a35', 1), .78, .04, 1.7, '#5b331f', 2)
S['glass-harbour'] = lambda: bokeh(ridge(vgrad([(0, '#05070f'), (.5, '#14203a'), (1, '#05080f')]), .6, .03, 3, '#070a14', 3, 6), 70, .2, .65, ['#46d3c9', '#9b6bff', '#e7e9ff'], 6, 26, .55, 1)
S['northern-quiet'] = lambda: ridge(blob(blob(vgrad([(0, '#03060f'), (.7, '#0b1a33'), (1, '#0b1a33')]), .4, .3, .5, .12, '#3cf2a0', .55), .7, .22, .35, .1, '#8d5cff', .4), .68, .05, 1.3, '#a9bfdc', 4, 20)
S['orbit-nine'] = lambda: glow(blob(blob(vgrad([(0, '#05040c'), (1, '#0a0716')]), .7, 1.05, .75, .7, '#b48a6a', .95), .25, .3, .4, .3, '#5a2ea8', .45), .82, .32, .1, '#fff3d8', .8)
S['midnight-souk'] = lambda: bokeh(vgrad([(0, '#0a1430'), (.6, '#2a1a20'), (1, '#140b08')]), 80, .15, .8, ['#ffb347', '#ff8a3d', '#ffd27a'], 8, 34, .6, 4)
S['ember-coast'] = lambda: ridge(glow(vgrad([(0, '#3b1840'), (.42, '#d04b5a'), (.56, '#ff8a42'), (.62, '#2a1530'), (1, '#120a1c')]), .5, .55, .16, '#ffd08a', .9), .62, .06, .8, '#160b18', 5, 10)
S['saffron'] = lambda: glow(blob(vgrad([(0, '#1a0f08'), (1, '#2a1a0e')]), .5, .62, .35, .25, '#e8a33a', .85), .3, .2, .3, '#ffe2b0', .35)
S['kingdom-of-glass'] = lambda: bokeh(blob(vgrad([(0, '#0b1430'), (.5, '#1b3f8a'), (1, '#0a1022')]), .5, .9, .2, .5, '#2a1640', .7), 46, .05, .45, ['#ffd27a', '#fff1c9'], 10, 30, .6, 6)
S['lanterns'] = lambda: bokeh(vgrad([(0, '#1b2d55'), (.55, '#2b3c66'), (.6, '#141c34'), (1, '#0b1124')]), 40, .5, .7, ['#ffb066', '#ffd08a'], 6, 20, .7, 7)
S['paper-moons'] = lambda: bokeh(glow(vgrad([(0, '#2c2560'), (.6, '#7a64b8'), (1, '#f0b38c')]), .66, .28, .14, '#fff3dc', 1.1), 26, .3, .9, ['#ffc27a', '#ffe0a8'], 6, 18, .7, 8)
S['news'] = lambda: blob(blob(vgrad([(0, '#071733'), (.62, '#0d2f66'), (.63, '#162238'), (1, '#0a1222')]), .5, .35, .7, .22, '#3f8cff', .55), .5, .55, .1, .25, '#1a2433', .9)
S['football'] = lambda: bokeh(ridge(vgrad([(0, '#05080f'), (.35, '#1a2230'), (.42, '#123a22')]), .45, .01, 1, '#1f7a3a', 9, 6), 22, .02, .2, ['#ffffff', '#e8f0ff'], 8, 22, .9, 9)
S['dunes'] = lambda: ridge(ridge(vgrad([(0, '#f2d6b6'), (.5, '#f5c9a0'), (1, '#f5c9a0')]), .42, .07, .6, '#c4532a', 10, 12), .7, .05, 1.2, '#2b3566', 11, 30)
S['earth'] = lambda: glow(blob(vgrad([(0, '#020208'), (1, '#04040a')]), .5, 1.25, 1.0, .5, '#0d2b66', 1), .78, .63, .12, '#ffd9a0', .8)
S['concert'] = lambda: bokeh(blob(blob(vgrad([(0, '#0b0618'), (1, '#140a22')]), .3, .2, .2, .9, '#7a3cff', .55), .7, .2, .2, .9, '#ffb24a', .45), 30, .75, 1, ['#ffe0b0', '#c8a8ff'], 10, 30, .5, 12)
S['kids'] = lambda: bokeh(vgrad([(0, '#ffd59e'), (.5, '#9fd88a'), (1, '#4c9a5a')]), 40, 0, 1, ['#ff8a4c', '#ffd34c', '#7cc6ff'], 20, 60, .45, 13)
S['farmhouse'] = lambda: glow(blob(vgrad([(0, '#2a1e16'), (1, '#140d08')]), .7, .35, .25, .3, '#9fb3c8', .6), .35, .45, .25, '#e8a65a', .7)
S['undertow'] = lambda: glow(vgrad([(0, '#0c3a5c'), (.5, '#06223a'), (1, '#020c18')]), .45, .55, .2, '#7fe6ff', .55)
S['leopard'] = lambda: ridge(blob(vgrad([(0, '#3b5675'), (.6, '#c99a8a'), (1, '#6a6670')]), .6, .55, .2, .15, '#e8c3a8', .6), .62, .05, 1.4, '#3a3a44', 14, 18)
S['motorsport'] = lambda: bokeh(blob(vgrad([(0, '#160c28'), (.5, '#2a1a3a'), (1, '#0b0810')]), .5, .62, .5, .08, '#ff3b30', .5), 30, .1, .5, ['#ffffff', '#ffd8a0'], 6, 20, .7, 15)
for k, f in S.items():
    finish(f(), k)
    print(k)
