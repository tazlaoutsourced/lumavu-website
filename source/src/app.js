(() => {
  "use strict";
  const root = document.documentElement;
  const RM = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (RM) root.classList.add("rm");
  root.classList.add("js");
  const VIDEOS = new Set(window.LUMAVU_VIDEOS || []);
  const MEDIA = "assets/media/";
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => Array.from(el.querySelectorAll(s));
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));

  /* ---------- Device scaling ---------- */
  const fits = $$(".fit[data-w]");
  const fitOne = (el) => {
    const w = +el.dataset.w, k = el.clientWidth / w;
    if (k > 0) el.style.setProperty("--k", k.toFixed(5));
  };
  const ro = new ResizeObserver((entries) => entries.forEach((e) => fitOne(e.target)));
  fits.forEach((el) => { fitOne(el); ro.observe(el); });

  /* ---------- Lazy artwork and video ---------- */
  const setArt = (el) => {
    const key = el.dataset.bg; if (!key) return;
    const small = el.getBoundingClientRect().width < 420 || el.closest(".poster, .cw, .dl-item, .cu-out");
    el.style.backgroundImage = `url(${MEDIA}${key}${small ? "-s" : ""}.jpg)`;
    if (el.dataset.pos) el.style.backgroundPosition = el.dataset.pos;
    delete el.dataset.bg;
  };
  const artIO = new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) { setArt(e.target); artIO.unobserve(e.target); } });
  }, { rootMargin: "1200px 0px" });
  $$("[data-bg]").forEach((el) => artIO.observe(el));

  const vids = $$("video[data-video]");
  vids.forEach((v) => {
    const key = v.dataset.video;
    if (!VIDEOS.has(key) || RM) { v.remove(); return; }
    v.muted = true; v.defaultMuted = true; v.setAttribute("muted", "");
  });
  // the hero loop waits until the rest of the page has loaded, so it never slows the opening
  const settled = new Promise((res) => {
    const go = () => setTimeout(res, 400);
    if (document.readyState === "complete") go(); else addEventListener("load", go, { once: true });
  });
  // choose the file by how wide the 16:9 loop is actually drawn
  const pick = (v) => {
    const fit = v.closest(".fit");
    const k = fit ? (+getComputedStyle(fit).getPropertyValue("--k") || 1) : 1;
    const r = fit ? { width: v.offsetWidth * k, height: v.offsetHeight * k } : v.getBoundingClientRect();
    const t = getComputedStyle(v).transform;
    const scale = fit && t && t !== "none" ? new DOMMatrix(t).a : 1;
    const px = Math.max(r.width, r.height * 16 / 9) * scale * Math.min(devicePixelRatio || 1, 2);
    const size = px <= 640 ? "-s" : px <= 1440 && "m" in v.dataset ? "-m" : "";
    return `${MEDIA}${v.dataset.video}${size}.mp4`;
  };
  const start = (v) => {
    if (!v._vis || v._hold) return;
    if (!v.src) {
      v.src = pick(v);
      v.addEventListener("playing", () => v.classList.add("on"), { once: true });
    }
    v.play().catch(() => {});
  };
  const vidIO = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      const v = e.target;
      v._vis = e.isIntersecting;
      if (!e.isIntersecting) { v.pause(); return; }
      if ("defer" in v.dataset) settled.then(() => start(v)); else start(v);
    });
  }, { rootMargin: "200px 0px" });
  $$("video[data-video]").forEach((v) => vidIO.observe(v));

  /* ---------- Generated posters (the app's own fallback artwork) ---------- */
  $$(".poster.gen").forEach((el) => {
    const t = el.dataset.gen || ""; let h = 0;
    for (const c of t) h = (h * 31 + c.charCodeAt(0)) >>> 0;
    const hue = h % 360;
    el.style.background = `radial-gradient(120% 80% at 20% 0%, hsl(${hue} 55% 34%), transparent 70%), linear-gradient(170deg, hsl(${hue} 45% 22%), hsl(${(hue + 20) % 360} 40% 8%))`;
  });

  /* ---------- Sky: nebula shader + stars ---------- */
  // the nebula is full at the start and the end; in between it dims so each screen's own light leads
  const LEVEL = { violet: 1, night: 0.28, deep: 0.32, dusk: 0.4, ember: 0.42, bright: 0.85 };
  const PALETTES = {
    violet: [[0.30, 0.15, 0.66], [0.17, 0.32, 0.86], [0.86, 0.38, 0.76]],
    night:  [[0.30, 0.15, 0.66], [0.17, 0.32, 0.86], [0.86, 0.38, 0.76]],
    deep:   [[0.11, 0.16, 0.52], [0.12, 0.44, 0.86], [0.50, 0.60, 1.00]],
    dusk:   [[0.44, 0.16, 0.36], [0.78, 0.36, 0.26], [0.95, 0.60, 0.46]],
    ember:  [[0.34, 0.13, 0.46], [0.90, 0.32, 0.22], [1.00, 0.56, 0.42]],
    bright: [[0.36, 0.20, 0.78], [0.30, 0.46, 1.00], [1.00, 0.56, 0.86]],
  };
  const sky = { cur: PALETTES.violet.map((c) => c.slice()), target: PALETTES.violet, k: 1, kT: 1, flash: 0, dirty: true };
  const skySections = $$("[data-sky]");
  const pickSky = () => {
    const mid = (H || innerHeight) / 2;
    for (const s of skySections) {
      const r = s.getBoundingClientRect();
      if (r.top <= mid && r.bottom >= mid) { const key = s.dataset.sky, p = PALETTES[key]; if (p && p !== sky.target) { sky.target = p; sky.dirty = true; } sky.kT = LEVEL[key] ?? 1; return; }
    }
  };

  const neb = $("#nebula");
  let gl = null, prog = null, U = {};
  try { gl = neb.getContext("webgl", { antialias: false, alpha: false, premultipliedAlpha: false, powerPreference: "low-power" }); } catch (e) { gl = null; }
  const VS = "attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}";
  const FS = `precision mediump float;
uniform vec2 r;uniform float t;uniform float s;uniform float fl;uniform float k;uniform vec3 c1;uniform vec3 c2;uniform vec3 c3;
float h(vec2 p){p=fract(p*vec2(123.34,456.21));p+=dot(p,p+45.32);return fract(p.x*p.y);}
float n(vec2 p){vec2 i=floor(p),f=fract(p);vec2 u=f*f*(3.-2.*f);return mix(mix(h(i),h(i+vec2(1.,0.)),u.x),mix(h(i+vec2(0.,1.)),h(i+vec2(1.,1.)),u.x),u.y);}
float fbm(vec2 p){float v=0.,a=.5;mat2 m=mat2(1.6,1.2,-1.2,1.6);for(int i=0;i<5;i++){v+=a*n(p);p=m*p;a*=.5;}return v;}
void main(){
  vec2 uv=(gl_FragCoord.xy-.5*r)/r.y;
  vec2 p=uv*1.35+vec2(.3,-s);
  float tt=t*.018;
  vec2 q=vec2(fbm(p+vec2(0.,tt)),fbm(p+vec2(5.2,1.3)-tt));
  vec2 w=vec2(fbm(p+2.1*q+vec2(1.7,9.2)+tt*.6),fbm(p+2.1*q+vec2(8.3,2.8)));
  float d=fbm(p+1.7*w);
  float band=exp(-pow(uv.x*.62-uv.y*.9+.05,2.)*2.6);
  float neb=smoothstep(.18,.78,d)*(.55+.9*band);
  vec3 col=vec3(.012,.01,.03);
  col=mix(col,c1*.95,smoothstep(.0,.42,neb));
  col=mix(col,c2,smoothstep(.3,.9,neb)*clamp(length(w)*.9,0.,1.));
  col+=c3*pow(smoothstep(.42,.95,d*band+.12),2.)*.6;
  float lanes=smoothstep(.25,.75,fbm(p*1.8-w*1.4+3.));
  col*=.45+.75*lanes;
  col*=k*(1.+fl*1.6);
  col+=c3*fl*.18*band;
  col*=.8+.4*fbm(p*4.3+w*2.);col*=1.18-.32*dot(uv,uv);
  gl_FragColor=vec4(col,1.);
}`;
  const compile = (type, src) => { const sh = gl.createShader(type); gl.shaderSource(sh, src); gl.compileShader(sh); if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(sh)); return sh; };
  if (gl) {
    try {
      prog = gl.createProgram();
      gl.attachShader(prog, compile(gl.VERTEX_SHADER, VS));
      gl.attachShader(prog, compile(gl.FRAGMENT_SHADER, FS));
      gl.linkProgram(prog);
      if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) throw new Error("link");
      gl.useProgram(prog);
      const buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf);
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
      const loc = gl.getAttribLocation(prog, "p"); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
      ["r", "t", "s", "fl", "k", "c1", "c2", "c3"].forEach((k) => (U[k] = gl.getUniformLocation(prog, k)));
    } catch (e) { gl = null; }
  }

  const starC = $("#stars"), sx = starC.getContext("2d"), skyEl = $(".sky");
  let W = 0, H = 0, DPR = 1, stars = [];
  let lastSkyW = 0;
  // On phones innerHeight changes whenever the browser's toolbars slide in or out. The sky is sized to the screen with
  // the toolbars hidden (100lvh), which stays put, so nothing is redrawn or rescaled while someone is scrolling.
  const sizeSky = () => {
    const w = skyEl.clientWidth || innerWidth, h = skyEl.clientHeight || innerHeight, dpr = Math.min(devicePixelRatio || 1, 2);
    if (w === W && h === H && dpr === DPR && stars.length) return;
    const regen = w !== lastSkyW || !stars.length;
    lastSkyW = w;
    W = w; H = h; DPR = dpr;
    starC.width = Math.round(W * DPR); starC.height = Math.round(H * DPR);
    if (gl) { const q = W < 700 ? 0.4 : 0.5; neb.width = Math.round(W * q); neb.height = Math.round(H * q); gl.viewport(0, 0, neb.width, neb.height); }
    if (regen) {
      const count = Math.round((W * Math.max(H, 700)) / 2600);
      let seed = 7; const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
      stars = Array.from({ length: count }, () => ({ x: rnd(), y: rnd(), z: 0.15 + rnd() * 0.85, r: rnd() < 0.015 ? 1.1 + rnd() * 0.6 : 0.35 + rnd() * 0.7, ph: rnd() * 6.28, sp: 0.4 + rnd() * 1.4, tint: rnd() }));
    }
    sky.dirty = true;
  };
  sizeSky();
  addEventListener("resize", sizeSky);

  const drawStars = (time) => {
    sx.setTransform(DPR, 0, 0, DPR, 0, 0);
    sx.clearRect(0, 0, W, H);
    const sc = scrollY;
    for (const s of stars) {
      let y = (s.y * H - sc * 0.12 * s.z) % H; if (y < 0) y += H;
      const x = s.x * W;
      const tw = RM ? 1 : 0.65 + 0.35 * Math.sin(time * 0.001 * s.sp + s.ph);
      const a = (0.25 + 0.75 * s.z) * tw * (0.5 + 0.5 * sky.k);
      if (s.flare) {
        const g = sx.createRadialGradient(x, y, 0, x, y, s.flare * 0.5);
        g.addColorStop(0, `rgba(255,255,255,${0.9 * tw})`); g.addColorStop(1, "rgba(200,190,255,0)");
        sx.fillStyle = g; sx.beginPath(); sx.arc(x, y, s.flare * 0.5, 0, 6.283); sx.fill();
        sx.strokeStyle = `rgba(235,230,255,${0.55 * tw})`; sx.lineWidth = 0.6;
        sx.beginPath(); sx.moveTo(x - s.flare, y); sx.lineTo(x + s.flare, y); sx.moveTo(x, y - s.flare); sx.lineTo(x, y + s.flare); sx.stroke();
        continue;
      }
      sx.fillStyle = s.tint > 0.85 ? `rgba(255,214,236,${a})` : s.tint < 0.15 ? `rgba(196,214,255,${a})` : `rgba(255,255,255,${a})`;
      if (s.r > 1.2) { sx.beginPath(); sx.arc(x, y, s.r, 0, 6.283); sx.fill(); }
      else sx.fillRect(x, y, s.r * 1.4, s.r * 1.4);
    }
  };

  let lastNeb = 0, t0 = performance.now();
  const drawNebula = (now) => {
    if (!gl) return;
    gl.uniform2f(U.r, neb.width, neb.height);
    gl.uniform1f(U.t, RM ? 40 : (now - t0) / 1000 + 40);
    gl.uniform1f(U.s, scrollY / Math.max(1, H) * 0.085);
    gl.uniform1f(U.fl, sky.flash);
    gl.uniform1f(U.k, sky.k);
    gl.uniform3fv(U.c1, sky.cur[0]); gl.uniform3fv(U.c2, sky.cur[1]); gl.uniform3fv(U.c3, sky.cur[2]);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
    if (!neb.classList.contains("on")) neb.classList.add("on");
  };
  const stepPalette = (k) => {
    let moving = false;
    if (Math.abs(sky.kT - sky.k) > 0.002) { sky.k += (sky.kT - sky.k) * k * 1.2; moving = true; } else sky.k = sky.kT;
    for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) {
      const d = sky.target[i][j] - sky.cur[i][j];
      if (Math.abs(d) > 0.002) { sky.cur[i][j] += d * k; moving = true; } else sky.cur[i][j] = sky.target[i][j];
    }
    return moving;
  };

  /* ---------- Header ---------- */
  const top = $("#top");
  const headerFrame = () => { top.classList.toggle("solid", scrollY > 40); };

  /* ---------- Main loop ---------- */
  let ticking = false, frameDue = true;
  const onScroll = () => { frameDue = true; };
  addEventListener("scroll", onScroll, { passive: true });
  addEventListener("resize", () => { frameDue = true; });
  const loop = (now) => {
    if (frameDue) { headerFrame(); pickSky(); frameDue = false; sky.dirty = true; }
    const moving = stepPalette(0.035);
    if (!document.hidden) {
      if (RM) {
        if (sky.dirty || moving) { drawNebula(now); drawStars(now); sky.dirty = false; }
      } else {
        if (now - lastNeb > 33) { drawNebula(now); lastNeb = now; }
        drawStars(now);
      }
    }
    requestAnimationFrame(loop);
  };
  requestAnimationFrame(loop);

  /* ---------- Reveal ---------- */
  const rvIO = new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.remove("pre"); rvIO.unobserve(e.target); } });
  }, { rootMargin: "0px 0px -8% 0px" });
  if (!RM) $$(".rv").forEach((el) => { if (el.getBoundingClientRect().top > innerHeight) { el.classList.add("pre"); rvIO.observe(el); } });

  /* helper: run a loop only while its element is on screen */
  const whileVisible = (el, start, stop) => {
    if (!el) return;
    let on = false;
    new IntersectionObserver((es) => es.forEach((e) => {
      if (e.isIntersecting && !on) { on = true; start(); }
      else if (!e.isIntersecting && on) { on = false; stop && stop(); }
    }), { threshold: 0.25 }).observe(el);
  };

  /* ---------- Add playlist sheet ---------- */
  const FORMS = {
    xtream: { rows: [["Name", "Living Room", 1], ["Server", "http://line.example.tv:8080", 1], ["Username", "livingroom", 1], ["Password", "••••••••••", 1], ["Guide", "From the account", 0]], hint: "Your password goes in the Keychain and is only used to sign in here. If you sync with iCloud, it travels through your own account so your other devices can sign in too." },
    m3u: { rows: [["Name", "World News", 1], ["Link", "https://example.org/playlists/news.m3u", 1], ["Or", "Choose a file…", 0], ["Guide URL", "https://example.org/guide.xml.gz", 1], ["Refresh", "Every day", 0]], hint: "Paste the guide link here too if your provider gave you one. You can also add it later, in the playlist's settings." },
    jellyfin: { rows: [["Name", "Home Server", 1], ["Server", "http://192.168.1.20:8096", 1], ["Username", "home", 1], ["Password", "••••••••", 1], ["Library", "Films and series", 0]], hint: "Sign in once, and your films and series come across with their artwork." },
    emby: { rows: [["Name", "Media Room", 1], ["Server", "https://emby.example.net", 1], ["Username", "family", 1], ["Password", "••••••••", 1], ["Library", "Films and series", 0]], hint: "Works just like Jellyfin. Your library shows up in the sidebar under whatever name you give it." },
  };
  const fieldsEl = $("#fields"), hintEl = $("#sheetHint");
  const showForm = (type) => {
    const f = FORMS[type]; if (!f) return;
    fieldsEl.innerHTML = f.rows.map(([k, v, filled]) => `<div class="field"><label>${k}</label><span class="${filled ? "val" : ""}">${v}</span></div>`).join("");
    hintEl.textContent = f.hint;
    $$(".seg button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.type === type)));
  };
  $$(".seg button").forEach((b) => b.addEventListener("click", () => { showForm(b.dataset.type); segAuto = false; }));
  showForm("xtream");
  let segAuto = true, segTimer = 0;
  whileVisible($("#sheet"), () => {
    if (RM) return;
    const order = ["xtream", "m3u", "jellyfin", "emby"]; let i = 0;
    segTimer = setInterval(() => { if (!segAuto) return clearInterval(segTimer); i = (i + 1) % order.length; showForm(order[i]); }, 3200);
  }, () => clearInterval(segTimer));

  /* ---------- TV guide, on the visitor's own clock ---------- */
  const NOW = new Date();
  const realNow = NOW.getHours() * 60 + NOW.getMinutes();
  const B = Math.floor(realNow / 30) * 30;
  const CH = [
    ["ON", "Orbit News 24", true, [[-120, 60, "News Hour"], [-60, 30, "Business Desk"], [-30, 60, "The World Today"], [30, 60, "The Long Read"], [90, 60, "News Hour"], [150, 60, "Business Desk"]]],
    ["KS", "Kestrel Sport", false, [[-150, 60, "Pre-Match"], [-90, 150, "Matchday Live"], [60, 60, "Extra Time"], [120, 30, "Highlights"], [150, 90, "Classic Matches"]]],
    ["ND", "Northline Docs", true, [[-120, 60, "Ocean Giants"], [-60, 60, "Wild Peaks"], [0, 60, "The Empty Quarter"], [60, 90, "The Last Glaciers"], [150, 60, "Night Skies"]]],
    ["AM", "Apex Motor", false, [[-150, 90, "Qualifying Replay"], [-60, 30, "Grand Prix Build-up"], [-30, 120, "Race Day Live"], [90, 60, "Paddock Talk"], [150, 60, "Onboard"]]],
    ["HM", "Halo Music", false, [[-120, 45, "Studio Sessions"], [-75, 105, "Live at the Bay"], [30, 60, "Strings"], [90, 60, "The Mix"], [150, 60, "Live at the Bay"]]],
    ["SF", "Saffron Food", true, [[-120, 60, "Saffron Hours"], [-60, 60, "Street Food Atlas"], [0, 60, "Kitchen Table"], [60, 90, "Saffron Hours"], [150, 60, "Street Food Atlas"]]],
    ["NK", "Nova Kids", false, [[-120, 30, "Fox and Finch"], [-90, 30, "Paper Forest"], [-60, 30, "Story Time"], [-30, 120, "Little Explorers"], [90, 90, "Fox and Finch"], [180, 30, "Paper Forest"]]],
  ];
  const G0 = B - 90, G1 = B + 180;
  const gChan = $("#gChan"), gTrack = $("#gTrack"), gTicks = $("#gTicks"), nowLine = $("#nowLine"), gTime = $(".g-time");
  const tf = new Intl.DateTimeFormat(undefined, { hour: "numeric", minute: "2-digit" });
  const hhmm = (m) => { const d = new Date(NOW); d.setHours(0, 0, 0, 0); d.setMinutes(m); return tf.format(d); };
  // date chips and the iPad's status bar follow today's date
  (() => {
    const bar = $("#guideBar"); if (!bar) return;
    const day = (n) => { const d = new Date(NOW); d.setDate(d.getDate() + n); return d; };
    const fmt = new Intl.DateTimeFormat(undefined, { weekday: "short", day: "numeric", month: "short" });
    const chips = [`<span class="chip"><svg class="ico"><use href="#i-filter"/></svg>All channels</span>`, `<span class="chip">Yesterday</span>`, `<span class="chip on">Today</span>`, `<span class="chip">Tomorrow</span>`];
    for (let n = 2; n <= 5; n++) chips.push(`<span class="chip">${fmt.format(day(n))}</span>`);
    bar.innerHTML = chips.join("");
    const short = new Intl.DateTimeFormat("en-GB", { weekday: "short", day: "numeric", month: "short" }).format(NOW).replace(",", "");
    $$("[data-today]").forEach((el) => (el.textContent = short));
  })();
  let ppm = 5, gNow = realNow, gW = 0;
  const buildGuide = () => {
    gW = innerWidth;
    ppm = innerWidth < 640 ? 3.4 : 5;
    gTrack.style.width = `${(G1 - G0) * ppm}px`;
    gTicks.innerHTML = "";
    for (let m = G0; m < G1; m += 30) gTicks.insertAdjacentHTML("beforeend", `<span style="left:${(m - G0) * ppm}px">${hhmm(m)}</span>`);
    $$(".g-line", gTrack).forEach((n) => n.remove());
    $$(".g-cell-c", gChan).forEach((n) => n.remove());
    CH.forEach(([code, name, cu, progs]) => {
      gChan.insertAdjacentHTML("beforeend", `<div class="g-cell-c" data-code="${code}"><span class="mono-chip">${code}</span><b>${name}</b></div>`);
      const line = document.createElement("div"); line.className = "g-line";
      progs.forEach(([o, d, title]) => {
        const s = B + o;
        const a = Math.max(s, G0), b = Math.min(s + d, G1); if (b <= a) return;
        const c = document.createElement("div"); c.className = "prog-cell";
        c.dataset.s = s; c.dataset.e = s + d; c.dataset.cu = cu ? "1" : "";
        c.style.left = `${(a - G0) * ppm}px`; c.style.width = `${(b - a) * ppm}px`;
        c.innerHTML = `<small>${hhmm(s)}</small><b>${title}</b>`;
        line.appendChild(c);
      });
      gTrack.appendChild(line);
    });
    paintGuide();
  };
  const paintGuide = () => {
    const viewW = gTime.clientWidth;
    const x = (gNow - G0) * ppm;
    const maxShift = Math.max(0, (G1 - G0) * ppm - viewW);
    const shift = clamp(x - viewW * 0.3, 0, maxShift);
    $$(".prog-cell", gTrack).forEach((c) => {
      const s = +c.dataset.s, e = +c.dataset.e;
      const past = e <= gNow, now = s <= gNow && gNow < e;
      c.classList.toggle("past", past); c.classList.toggle("now", now);
      if (now) c.style.setProperty("--p", `${(((gNow - s) / (e - s)) * 100).toFixed(1)}%`);
      const small = c.querySelector("small");
      const left = parseFloat(c.style.left), w = parseFloat(c.style.width);
      const shown = left + w - Math.max(left, shift);
      small.innerHTML = past && c.dataset.cu && shown > 150 ? `${hhmm(s)} &nbsp;<span class="cu">↺ Catch up</span>` : hhmm(s);
      c.classList.toggle("tiny", shown < 72);
      c.style.paddingLeft = left < shift ? `${Math.min(shift - left, Math.max(0, w - 90)) + 11}px` : "";
    });
    $$("span", gTicks).forEach((t) => { t.style.opacity = parseFloat(t.style.left) - shift < 40 ? "0" : "1"; });
    gTrack.style.transform = `translate3d(${-shift}px,0,0)`;
    nowLine.style.left = `${x - shift}px`;
  };
  buildGuide();
  let gResize = 0; addEventListener("resize", () => { if (innerWidth === gW) return; clearTimeout(gResize); gResize = setTimeout(buildGuide, 150); });
  let gTimer = 0;
  const gTrans = (on) => { const v = on ? "transform 1.1s linear" : "none"; gTrack.style.transition = v; nowLine.style.transition = on ? "left 1.1s linear" : "none"; };
  whileVisible($("#guide"), () => {
    if (RM) return;
    gTrans(true);
    gTimer = setInterval(() => {
      gNow += 1;
      if (gNow > realNow + 75) { gNow = realNow; gTrans(false); paintGuide(); requestAnimationFrame(() => requestAnimationFrame(() => gTrans(true))); return; }
      paintGuide();
    }, 1100);
  }, () => clearInterval(gTimer));
  const flashChannel = (code) => {
    const row = $(`.g-cell-c[data-code="${code}"]`); if (!row) return;
    row.classList.add("hl"); setTimeout(() => row.classList.remove("hl"), 2200);
  };

  /* ---------- Failover ---------- */
  const foP = $("#foPlayer"), foT = $("#foToast"), foRows = $$(".copy-row"), foSteps = $$(".fo-step");
  const setRow = (i, cls, txt) => { const r = foRows[i]; r.className = `copy-row ${cls}`; r.querySelector(".s").textContent = txt; };
  const foState = (n) => {
    foSteps.forEach((s, i) => s.classList.toggle("on", i === n));
    foP.classList.toggle("stall", n === 1);
    const fv = $("video", foP);  // the picture freezes while the copy buffers, then carries on from the next one
    if (fv) { fv._hold = n === 1; if (fv._hold) fv.pause(); else if (fv._vis && fv.src) fv.play().catch(() => {}); }
    foT.classList.toggle("show", n === 2 || n === 3);
    if (n === 0) { setRow(0, "active", "Playing"); setRow(1, "", "Ready"); setRow(2, "", "Ready"); setRow(3, "", "Ready"); }
    if (n === 1) { setRow(0, "active", "Buffering…"); }
    if (n === 2) { setRow(0, "dead", "Stopped"); setRow(1, "active", "Playing"); }
    if (n === 3) { setRow(1, "active", "Playing · remembered"); }
  };
  foState(0);
  let foTimer = 0;
  whileVisible($("#failover"), () => {
    if (RM) { foState(3); return; }
    let n = 0; const dur = [2600, 2400, 3200, 3400];
    const next = () => { foState(n); foTimer = setTimeout(() => { n = (n + 1) % 4; next(); }, dur[n]); };
    next();
  }, () => clearTimeout(foTimer));

  /* ---------- Multiview ---------- */
  const mv = $("#mv"), tiles = $$(".tile", mv), mvWait = $("#mvWait"), mvFrom = $("#mvFrom");
  const hear = (t) => tiles.forEach((x) => x.classList.toggle("audio", x === t));
  tiles.forEach((t) => {
    let last = 0;
    const act = () => {
      const now = Date.now();
      if (now - last < 320) { mv.classList.toggle("one"); tiles.forEach((x) => x.classList.toggle("full", x === t && mv.classList.contains("one"))); }
      else hear(t);
      last = now;
    };
    t.addEventListener("click", act);
    t.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); hear(t); } });
  });
  let mvTimers = [];
  whileVisible(mv, () => {
    mvWait.classList.remove("gone"); mvFrom.classList.remove("show");
    mvTimers.push(setTimeout(() => { mvWait.classList.add("gone"); mvFrom.classList.add("show"); }, RM ? 0 : 3800));
    mvTimers.push(setTimeout(() => mvFrom.classList.remove("show"), RM ? 999999 : 8500));
  }, () => { mvTimers.forEach(clearTimeout); mvTimers = []; });

  /* ---------- Live subtitles ---------- */
  const LINES = {
    en: ["At first light, the dunes start to move.", "The wind lifts sand from every crest,", "a few centimetres at a time.", "Over a century, a whole dune", "can cross the valley floor.", "By evening the heat lifts,", "and the desert comes alive."],
    ar: ["مع أول ضوء، تبدأ الكثبان بالتحرك.", "ترفع الرياح الرمال عن كل قمة،", "بضعة سنتيمترات في كل مرة.", "وعلى مدى قرن، يمكن لكثيب كامل", "أن يعبر أرض الوادي.", "وفي المساء تنحسر الحرارة،", "فتدبّ الحياة في الصحراء."],
    fr: ["Aux premières lueurs, les dunes bougent.", "Le vent soulève le sable de chaque crête,", "quelques centimètres à la fois.", "En un siècle, une dune entière", "peut traverser le fond de la vallée.", "Le soir, la chaleur retombe,", "et le désert s'éveille."],
    es: ["Con la primera luz, las dunas se mueven.", "El viento levanta arena de cada cresta,", "unos centímetros cada vez.", "En un siglo, una duna entera", "puede cruzar el fondo del valle.", "Al anochecer, el calor afloja,", "y el desierto cobra vida."],
    de: ["Im ersten Licht geraten die Dünen in Bewegung.", "Der Wind hebt Sand von jedem Kamm,", "ein paar Zentimeter auf einmal.", "In einem Jahrhundert kann eine ganze Düne", "den Talboden durchqueren.", "Am Abend lässt die Hitze nach,", "und die Wüste erwacht."],
  };
  const LANG_NAMES = { en: "Live subtitles", ar: "Live subtitles · Arabic", fr: "Live subtitles · French", es: "Live subtitles · Spanish", de: "Live subtitles · German" };
  const cap = $("#caption"), capRoll = $("#capRoll"), capOrig = $("#capOrig"), ccLabel = $("#ccLabel"), subsFrame = $("#subsFrame");
  let lang = "en", capTimer = 0, li = 0, wi = 0, lineCount = 0, capOn = false;
  const fitCaption = () => {
    const set = LINES[lang]; const longest = Math.max(...set.map((s) => s.length));
    const boxW = subsFrame.clientWidth * 0.8;
    const per = lang === "ar" ? 0.46 : 0.5;
    const fs = clamp(boxW / (longest * per), 11, lang === "ar" ? 28 : 26);
    $(".cap-lines", cap).style.fontSize = `${fs.toFixed(1)}px`;
  };
  const resetCaption = () => {
    capRoll.innerHTML = ""; capRoll.style.transform = "none"; capOrig.textContent = ""; li = 0; wi = 0; lineCount = 0;
    cap.setAttribute("dir", lang === "ar" ? "rtl" : "ltr");
    capOrig.hidden = lang === "en"; capOrig.setAttribute("dir", "ltr");
    ccLabel.textContent = LANG_NAMES[lang];
    fitCaption();
  };
  const newLine = () => {
    const words = LINES[lang][li].split(" ");
    const div = document.createElement("div"); div.className = "cap-line";
    div.innerHTML = words.map((w) => `<span class="cap-word">${w}</span>`).join(" ");
    capRoll.appendChild(div); lineCount++;
    if (lineCount > 2) capRoll.style.transform = `translateY(${-(lineCount - 2) * 1.35}em)`;
    while (capRoll.children.length > 4) { capRoll.removeChild(capRoll.firstChild); lineCount--; capRoll.style.transition = "none"; capRoll.style.transform = `translateY(${-(lineCount - 2) * 1.35}em)`; void capRoll.offsetWidth; capRoll.style.transition = ""; }
    if (lang !== "en") capOrig.innerHTML = LINES.en[li].split(" ").map((w) => `<span class="cap-word">${w}</span>`).join(" ");
    return div;
  };
  let curLine = null;
  const tick = () => {
    if (!curLine) { curLine = newLine(); wi = 0; }
    const ws = curLine.querySelectorAll(".cap-word");
    const os = capOrig.querySelectorAll(".cap-word");
    if (wi < ws.length) {
      ws[wi].classList.add("in");
      if (os.length) { const upto = Math.round(((wi + 1) / ws.length) * os.length); for (let k = 0; k < upto; k++) os[k].classList.add("in"); }
      wi++; capTimer = setTimeout(tick, 230 + Math.random() * 120);
    } else {
      os.forEach((o) => o.classList.add("in"));
      curLine = null; li = (li + 1) % LINES.en.length;
      if (li === 0) { capTimer = setTimeout(() => { resetCaption(); tick(); }, 2600); }
      else capTimer = setTimeout(tick, li % 2 ? 380 : 900);
    }
  };
  const showStatic = () => {
    resetCaption();
    for (let k = 0; k < 2; k++) { li = k; const d = newLine(); d.querySelectorAll(".cap-word").forEach((w) => w.classList.add("in")); }
    capOrig.querySelectorAll(".cap-word").forEach((w) => w.classList.add("in"));
  };
  const startCaps = () => { clearTimeout(capTimer); curLine = null; resetCaption(); if (RM) showStatic(); else tick(); };
  $$(".langs button").forEach((b) => b.addEventListener("click", () => {
    lang = b.dataset.lang; $$(".langs button").forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
    if (capOn) startCaps(); else showStatic();
  }));
  showStatic();
  let capW = innerWidth; addEventListener("resize", () => { if (innerWidth !== capW) { capW = innerWidth; fitCaption(); } });
  whileVisible(subsFrame, () => { capOn = true; startCaps(); }, () => { capOn = false; clearTimeout(capTimer); });

  /* ---------- Name clean-up ---------- */
  const cuRaw = $("#cuRaw"); let cuTimer = 0;
  whileVisible($("#cleanup"), () => {
    if (RM) { cuRaw.classList.add("clean"); return; }
    cuTimer = setInterval(() => cuRaw.classList.toggle("clean"), 2600);
    setTimeout(() => cuRaw.classList.add("clean"), 900);
  }, () => clearInterval(cuTimer));

  /* ---------- Downloads ---------- */
  const ring = $("#dlRing"), dlS = $("#dlS"); let dlTimer = 0, dlP = 64;
  const paintDl = () => {
    ring.style.strokeDashoffset = (75.4 * (1 - dlP / 100)).toFixed(2);
    dlS.textContent = dlP >= 100 ? "S1 · E5 · 52 min · 1.7 GB" : `S1 · E5 · ${dlP}% · ${(1.7 * dlP / 100).toFixed(1)} of 1.7 GB`;
  };
  whileVisible($("#downloads"), () => {
    if (RM) return;
    dlTimer = setInterval(() => { dlP = dlP >= 100 ? 40 : dlP + 2; paintDl(); }, 420);
  }, () => clearInterval(dlTimer));

  /* ---------- Speed timeline ---------- */
  const tl = $("#timeline");
  const drawTimeline = () => {
    const w = tl.clientWidth; if (!w) return;
    const narrow = w < 560;
    const padL = 0, padR = 8, x0 = padL, x1 = w - padR, max = 400;
    const X = (ms) => x0 + (ms / max) * (x1 - x0);
    const rows = [["Open the whole playlist", 18, "18 ms"], ["Open the whole guide", 16, "16 ms"], ["Search, for each letter you type", 0.7, "0.7 ms"]];
    const rowH = 62, topPad = 46, h = topPad + rows.length * rowH + 30;
    let s = `<svg viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" role="img" aria-label="Lumavu opens a 14,868-channel playlist in 18 milliseconds, its guide in 16 milliseconds, and searches in 0.7 milliseconds per letter, all far quicker than a blink, which takes 100 to 400 milliseconds.">`;
    s += `<rect class="blink" x="${X(100)}" y="${topPad - 10}" width="${X(400) - X(100)}" height="${rows.length * rowH + 4}" rx="6"/>`;
    s += `<text class="blink-l" x="${X(100) + 2}" y="${topPad - 20}">A blink of an eye, 100 to 400 ms</text>`;
    [0, 100, 200, 300, 400].forEach((t) => {
      s += `<line class="grid" x1="${X(t)}" x2="${X(t)}" y1="${topPad - 10}" y2="${topPad + rows.length * rowH - 6}"/>`;
      const anchor = t === 0 ? "start" : t === 400 ? "end" : "middle";
      s += `<text class="tick" x="${X(t)}" y="${h - 6}" text-anchor="${anchor}">${t} ms</text>`;
    });
    s += `<line class="axis" x1="${x0}" x2="${x1}" y1="${topPad + rows.length * rowH - 6}" y2="${topPad + rows.length * rowH - 6}"/>`;
    rows.forEach(([lab, ms, val], i) => {
      const y = topPad + i * rowH + (narrow ? 22 : 24);
      const bw = Math.max(2.5, X(ms) - x0);
      s += `<text class="lab" x="${x0}" y="${y - 10}">${lab}</text>`;
      s += `<rect class="bar${i === 2 ? " e" : ""}" x="${x0}" y="${y}" width="${bw.toFixed(1)}" height="10" rx="3"/>`;
      s += `<text class="val" x="${x0 + bw + 10}" y="${y + 9}">${val}</text>`;
    });
    s += "</svg>";
    tl.innerHTML = s;
  };
  drawTimeline();
  new ResizeObserver(drawTimeline).observe(tl);

  /* ---------- Menu (small screens) ---------- */
  const menu = $("#menu"), menuBtn = $("#menuBtn");
  const setMenu = (open) => {
    menuBtn.setAttribute("aria-expanded", String(open));
    document.body.classList.toggle("menu-open", open);
    if (open) { menu.hidden = false; requestAnimationFrame(() => menu.classList.add("open")); $("a", menu).focus({ preventScroll: true }); }
    else { menu.classList.remove("open"); setTimeout(() => { if (!menu.classList.contains("open")) menu.hidden = true; }, 300); }
  };
  menuBtn.addEventListener("click", () => setMenu(menuBtn.getAttribute("aria-expanded") !== "true"));
  $$("a", menu).forEach((a) => a.addEventListener("click", () => setMenu(false)));
  addEventListener("keydown", (e) => { if (e.key === "Escape" && !menu.hidden) { setMenu(false); menuBtn.focus(); } });
  addEventListener("resize", () => { if (innerWidth > 860 && !menu.hidden) setMenu(false); });

  /* ---------- Ambient light from each screen ---------- */
  const avg = (img, cuts) => {
    const c = document.createElement("canvas"); c.width = 32; c.height = 18;
    const x = c.getContext("2d", { willReadFrequently: true }); x.drawImage(img, 0, 0, 32, 18);
    return cuts.map(([sx, sy, sw, sh]) => {
      const d = x.getImageData(sx, sy, sw, sh).data; let r = 0, g = 0, b = 0, n = 0;
      for (let i = 0; i < d.length; i += 4) { r += d[i]; g += d[i + 1]; b += d[i + 2]; n++; }
      r /= n; g /= n; b /= n;
      // lift the colour a little so it reads as light rather than mud
      const m = Math.max(r, g, b) || 1, k = Math.min(1.9, 205 / m);
      return `rgba(${Math.round(r * k)},${Math.round(g * k)},${Math.round(b * k)},.75)`;
    });
  };
  const QUADS = [[0, 0, 16, 9], [16, 0, 16, 9], [0, 9, 16, 9], [16, 9, 16, 9]];
  const loadImg = (key) => new Promise((res, rej) => { const i = new Image(); i.onload = () => res(i); i.onerror = rej; i.src = `${MEDIA}${key}-s.jpg`; });
  const ambiIO = new IntersectionObserver((entries) => entries.forEach(async (e) => {
    if (!e.isIntersecting) return; ambiIO.unobserve(e.target);
    const el = e.target;
    try {
      if (el.id === "mvAmbi") {
        const keys = ["news", "football", "leopard", "motorsport"];
        const imgs = await Promise.all(keys.map(loadImg));
        imgs.forEach((im, i) => el.style.setProperty(`--a${i + 1}`, avg(im, [[0, 0, 32, 18]])[0]));
      } else {
        const cols = avg(await loadImg(el.dataset.ambi), QUADS);
        cols.forEach((c, i) => el.style.setProperty(`--a${i + 1}`, c));
      }
    } catch (err) { /* keep the default violet light */ }
  }), { rootMargin: "600px 0px" });
  $$(".ambi").forEach((el) => ambiIO.observe(el));

  /* ---------- The films headline tidies itself ---------- */
  const messy = $("#messy");
  if (messy) {
    $$(".tagx", messy).forEach((t) => t.style.setProperty("--mw", `${t.scrollWidth + 2}px`));
    const heights = () => {
      messy.style.transition = "none"; messy.style.height = "";
      const had = messy.classList.contains("clean");
      $$(".tagx", messy).forEach((t) => (t.style.transition = "none"));
      messy.classList.remove("clean"); const hMessy = messy.offsetHeight;
      messy.classList.add("clean"); const hClean = messy.offsetHeight;
      messy.classList.toggle("clean", had);
      void messy.offsetHeight;
      $$(".tagx", messy).forEach((t) => (t.style.transition = ""));
      messy.dataset.h0 = hMessy; messy.dataset.h1 = hClean;
      messy.style.height = `${had ? hClean : hMessy}px`;
      requestAnimationFrame(() => (messy.style.transition = ""));
    };
    heights();
    let mW = innerWidth; addEventListener("resize", () => { if (innerWidth !== mW) { mW = innerWidth; heights(); } });
    document.fonts && document.fonts.ready.then(heights);
    const obs = new MutationObserver(() => { messy.style.height = `${messy.classList.contains("clean") ? messy.dataset.h1 : messy.dataset.h0}px`; });
    obs.observe(messy, { attributes: true, attributeFilter: ["class"] });
    let mt = 0;
    new IntersectionObserver((es) => es.forEach((e) => {
      clearTimeout(mt);
      if (e.isIntersecting) mt = setTimeout(() => messy.classList.add("clean"), RM ? 0 : 900);
      else if (e.boundingClientRect.top > 0) messy.classList.remove("clean");
    }), { threshold: 0.9 }).observe(messy);
  }

  /* ---------- Flight strip ---------- */
  const flight = $(".flight");
  if (flight) new IntersectionObserver((es) => es.forEach((e) => flight.classList.toggle("go", e.isIntersecting)), { threshold: 0.6 }).observe(flight);

  /* ---------- The app icon, tilting like an Apple TV tile ---------- */
  const icon = $("#appIcon"), tilt = $("#appTilt");
  if (icon && !RM) {
    let idle = 0, raf = 0, lastMove = 0, visible = false;
    const set = (rx, ry, gx, gy) => {
      tilt.style.setProperty("--rx", `${rx.toFixed(2)}deg`); tilt.style.setProperty("--ry", `${ry.toFixed(2)}deg`);
      tilt.style.setProperty("--px", `${(-ry * 0.35).toFixed(2)}%`); tilt.style.setProperty("--py", `${(rx * 0.35).toFixed(2)}%`);
      tilt.style.setProperty("--gx", `${gx.toFixed(1)}%`); tilt.style.setProperty("--gy", `${gy.toFixed(1)}%`);
    };
    const zone = $("#launch");
    zone.addEventListener("pointermove", (e) => {
      if (e.pointerType !== "mouse") return;
      const r = icon.getBoundingClientRect();
      const dx = clamp((e.clientX - (r.left + r.width / 2)) / 360, -1, 1), dy = clamp((e.clientY - (r.top + r.height / 2)) / 360, -1, 1);
      icon.classList.add("live"); tilt.style.setProperty("--sc", "1.04");
      set(-dy * 12, dx * 14, 50 + dx * 40, 40 + dy * 40); lastMove = performance.now();
    });
    zone.addEventListener("pointerleave", () => { icon.classList.remove("live"); tilt.style.setProperty("--sc", "1"); set(0, 0, 30, 20); });
    const drift = (t) => {
      if (!visible) return;
      if (t - lastMove > 1800) { const a = t / 2600; set(Math.sin(a) * 5, Math.cos(a * 0.8) * 7, 40 + Math.cos(a) * 25, 30 + Math.sin(a) * 20); }
      raf = requestAnimationFrame(drift);
    };
    new IntersectionObserver((es) => es.forEach((e) => { visible = e.isIntersecting; cancelAnimationFrame(raf); if (visible) { icon.classList.add("live"); raf = requestAnimationFrame(drift); } })).observe(icon);
  }

  /* ---------- Quick switcher (⌘K), as in the app ---------- */
  const pal = $("#palette"), palInput = $("#palInput"), palList = $("#palList");
  const ITEMS = [
    ...[["Live TV and the guide", "#live"], ["When a stream drops", "#failover"], ["Multiview", "#multiview"], ["Live subtitles", "#subtitles"], ["Films and series", "#library"], ["Downloads", "#downloads"], ["Speed", "#speed"], ["Also starring", "#details"], ["Privacy", "#private"], ["Pricing and Lumavu Pro", "#pro"], ["Questions", "#faq"], ["Get the app", "#launch"]]
      .map(([t, h]) => ({ g: "On this page", t, h, icon: "i-list" })),
    ...CH.map(([code, name]) => ({ g: "Channels", t: name, code, h: "#live", sub: "Live" })),
    ...[["The Salt Road", "Film"], ["Orbit Nine", "Film"], ["Glass Harbour", "Film"], ["Paper Moons", "Film"], ["Kingdom of Glass", "Series"], ["The Long Season", "Series"]]
      .map(([t, k]) => ({ g: "Films and series", t, h: "#library", sub: k, icon: k === "Film" ? "i-film" : "i-tv" })),
    ...[["Support", "support.html"], ["Privacy policy", "privacy.html"], ["Terms of use", "terms.html"]].map(([t, h]) => ({ g: "Pages", t, h, icon: "i-info" })),
  ];
  let palSel = 0, palShown = [], palLastFocus = null;
  const match = (q, t) => { q = q.toLowerCase().trim(); if (!q) return true; t = t.toLowerCase(); if (t.includes(q)) return true; let i = 0; for (const ch of t) if (ch === q[i]) i++; return i === q.length; };
  const renderPal = () => {
    const q = palInput.value;
    palShown = ITEMS.filter((it) => match(q, it.t));
    if (!palShown.length) { palList.innerHTML = `<div class="pal-empty">Nothing called “${q.replace(/[<&]/g, "")}” here. Try a channel or a title</div>`; return; }
    palSel = clamp(palSel, 0, palShown.length - 1);
    let html = "", g = "";
    palShown.forEach((it, i) => {
      if (it.g !== g) { g = it.g; html += `<div class="pal-group">${g}</div>`; }
      const lead = it.code ? `<span class="mono-chip">${it.code}</span>` : `<span class="pi"><svg class="ico"><use href="#${it.icon}"/></svg></span>`;
      html += `<div class="pal-item" role="option" id="pi${i}" data-i="${i}" aria-selected="${i === palSel}">${lead}${it.t}${it.sub ? `<small>${it.sub}</small>` : ""}</div>`;
    });
    palList.innerHTML = html;
    palInput.setAttribute("aria-activedescendant", `pi${palSel}`);
    const sel = $(`#pi${palSel}`); if (sel) sel.scrollIntoView({ block: "nearest" });
  };
  const openPal = () => { palLastFocus = document.activeElement; pal.hidden = false; palInput.value = ""; palSel = 0; renderPal(); palInput.focus(); };
  const closePal = () => { pal.hidden = true; if (palLastFocus && palLastFocus.focus) palLastFocus.focus({ preventScroll: true }); };
  const choose = (it) => {
    closePal(); if (!it) return;
    if (!it.h.startsWith("#")) { location.href = it.h; return; }
    const el = $(it.h); if (el) el.scrollIntoView({ behavior: RM ? "auto" : "smooth", block: "start" });
    if (it.code) setTimeout(() => flashChannel(it.code), 700);
  };
  addEventListener("keydown", (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") { e.preventDefault(); pal.hidden ? openPal() : closePal(); return; }
    if (pal.hidden) return;
    if (e.key === "Escape") { e.preventDefault(); closePal(); }
    else if (e.key === "ArrowDown") { e.preventDefault(); palSel = Math.min(palSel + 1, palShown.length - 1); renderPal(); }
    else if (e.key === "ArrowUp") { e.preventDefault(); palSel = Math.max(palSel - 1, 0); renderPal(); }
    else if (e.key === "Enter") { e.preventDefault(); choose(palShown[palSel]); }
    else if (e.key === "Tab") { e.preventDefault(); palInput.focus(); }
  });
  palInput.addEventListener("input", () => { palSel = 0; renderPal(); });
  palList.addEventListener("click", (e) => { const it = e.target.closest(".pal-item"); if (it) choose(palShown[+it.dataset.i]); });
  palList.addEventListener("pointermove", (e) => { const it = e.target.closest(".pal-item"); if (it && +it.dataset.i !== palSel) { palSel = +it.dataset.i; $$(".pal-item", palList).forEach((x) => x.setAttribute("aria-selected", String(x === it))); } });
  $(".pal-scrim", pal).addEventListener("click", closePal);
  $$("[data-palette]").forEach((b) => b.addEventListener("click", openPal));
})();
