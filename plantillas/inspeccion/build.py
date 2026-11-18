# Video 8 — VW Gol "El desastre del año": metraje anotado a mano + dibujos. Run: python _work/build.py
import os

ROOT = os.path.join(os.path.dirname(__file__), "..")
YEL, RED, CHALK, SLATE, GREEN = "#ffe14d", "#ff3b30", "#f4f1ea", "#1c2321", "#2ecc71"
V0 = 0.3  # la voz entra en 0.3 s

CSS = f"""
    @font-face {{ font-family: "Marker"; src: url("assets/fonts/marker.ttf"); font-weight: 700; }}
    #root {{ position: absolute; inset: 0; overflow: hidden; background: #000; }}
    #root .cam {{ position: absolute; inset: 0; transform-origin: 50% 50%; }}
    #root .cam video, #root .cam img.full {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
    #root .flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; }}
    #root .redf {{ position: absolute; inset: 0; background: {RED}; opacity: 0; mix-blend-mode: multiply; }}
    #root .scrim-top {{ position: absolute; left: 0; top: 0; width: 1080px; height: 700px; background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0)); }}
    #root .slate {{ position: absolute; inset: 0; background: {SLATE}; }}
    #root .ink {{ position: absolute; inset: 0; width: 1080px; height: 1920px; overflow: visible; }}
    #root .hw {{ position: absolute; font-family: "Marker", cursive; font-weight: 700; color: {YEL}; line-height: 1.05;
      text-shadow: 3px 3px 0 rgba(0,0,0,0.85), -2px 2px 0 rgba(0,0,0,0.85), 0 6px 18px rgba(0,0,0,0.6); }}
    #root .hw.r {{ color: {RED}; }}
    #root .hw.w {{ color: {CHALK}; }}
    #root .lbl {{ position: absolute; left: 60px; top: 300px; padding: 10px 26px 14px; background: {RED}; transform: rotate(-3deg);
      font-family: "Marker", cursive; font-weight: 700; font-size: 52px; color: #fff; box-shadow: 6px 8px 0 rgba(0,0,0,0.55); }}
"""

JS = """
      const IR = { immediateRender: false };
      function cut(cam, t, from) { tl.fromTo(cam, { scale: from || 1.12 }, { scale: 1, duration: 0.45, ease: "expo.out" }, t); }
      function flash(sel, t, o) { tl.fromTo(sel, { opacity: o || 0.5 }, { opacity: 0, duration: 0.2, ease: "power2.out", ...IR }, t); }
      // dibuja trazos (path con pathLength=1)
      function draw(sel, t, d, st) { tl.fromTo(sel, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: d || 0.4, stagger: st || 0.08, ease: "power1.inOut" }, t); }
      function pop(sel, t, r) { tl.fromTo(sel, { scale: 0, rotation: (r || 0) - 12, opacity: 0 }, { scale: 1, rotation: r || 0, opacity: 1, duration: 0.32, ease: "back.out(2.4)" }, t); }
      function write(sel, t) { tl.fromTo(sel, { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.35, ease: "power1.out" }, t); }
      function shake(sel, t) { tl.fromTo(sel, { x: 0 }, { keyframes: [{ x: -14, duration: 0.04 }, { x: 12, duration: 0.04 }, { x: -7, duration: 0.04 }, { x: 0, duration: 0.05 }], ...IR }, t); }
"""


def P(d, color=YEL, w=12, cls="dr", extra=""):
    """Trazo a mano (dibujable)."""
    return (f'<path class="{cls}" d="{d}" pathLength="1" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" '
            f'stroke-linejoin="round" stroke-dasharray="1" stroke-dashoffset="1" {extra}/>')


def circle(cx, cy, rx, ry, color=YEL, w=12, cls="dr"):
    """Óvalo dibujado a mano que no cierra perfecto."""
    d = (f"M{cx - rx * 0.2} {cy - ry * 1.02} C{cx + rx * 0.9} {cy - ry * 1.1} {cx + rx * 1.08} {cy + ry * 0.7} {cx + rx * 0.1} {cy + ry * 1.0} "
         f"C{cx - rx * 1.0} {cy + ry * 1.08} {cx - rx * 1.12} {cy - ry * 0.6} {cx - rx * 0.05} {cy - ry * 1.12}")
    return P(d, color, w, cls)


def arrow(x1, y1, x2, y2, color=YEL, w=12, cls="dr"):
    import math
    mx, my = (x1 + x2) / 2 + (y2 - y1) * 0.15, (y1 + y2) / 2 - (x2 - x1) * 0.15
    a = math.atan2(y2 - my, x2 - mx)
    h = 46
    l = (x2 - h * math.cos(a - 0.45), y2 - h * math.sin(a - 0.45))
    r = (x2 - h * math.cos(a + 0.45), y2 - h * math.sin(a + 0.45))
    return (P(f"M{x1} {y1} Q{mx:.0f} {my:.0f} {x2} {y2}", color, w, cls) +
            P(f"M{l[0]:.0f} {l[1]:.0f} L{x2} {y2} L{r[0]:.0f} {r[1]:.0f}", color, w, cls))


def cross(cx, cy, s, color=RED, w=16, cls="dr"):
    return P(f"M{cx - s} {cy - s * 0.9} L{cx + s * 0.95} {cy + s}", color, w, cls) + P(f"M{cx + s} {cy - s} L{cx - s * 0.9} {cy + s * 0.95}", color, w, cls)


def ink(id_, inner, start=None, dur=None):
    t = f' class="clip" data-start="{start}" data-duration="{dur}"' if start is not None else ""
    return f'<div id="{id_}"{t} style="position:absolute;inset:0"><svg class="ink" viewBox="0 0 1080 1920">{inner}</svg></div>'


def hw(id_, text, x, y, size, kind="", start=None, dur=None, rot=0, w=None):
    t = f' data-start="{start}" data-duration="{dur}"' if start is not None else ""
    ww = f"width:{w}px;" if w else ""
    return (f'<div id="{id_}" class="hw {kind}{" clip" if start is not None else ""}"{t} '
            f'style="left:{x}px;top:{y}px;font-size:{size}px;transform:rotate({rot}deg);{ww}">{text}</div>')


def vid(id_, src, start, dur, ms=0, rate=None):
    r = f' data-playback-rate="{rate}"' if rate else ""
    return f'<video id="{id_}" class="clip" src="assets/media/{src}" data-start="{start}" data-duration="{dur}" data-media-start="{ms}"{r} muted playsinline></video>'


def img(id_, src, start, dur, alt):
    return f'<div class="cam clip" id="{id_}" data-start="{start}" data-duration="{dur}"><img class="full" id="{id_}-i" src="assets/media/{src}" alt="{alt}" /></div>'


def scene(cid, css, body, js):
    html = f"""<template>
  <style>{CSS}{css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
{body}
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});{JS}
{js}
      window.__timelines["{cid}"] = tl;
    }})();
  </script>
</template>
"""
    open(os.path.join(ROOT, "compositions", f"{cid}.html"), "w", encoding="utf-8", newline="\n").write(html)


os.makedirs(os.path.join(ROOT, "compositions"), exist_ok=True)

# ============================================================ gancho 0–5.15
scene("gancho", f"""
    #gc-t {{ position: absolute; left: 0; top: 250px; width: 1080px; text-align: center; }}
    #gc-t1 {{ font-family: "Marker", cursive; font-weight: 700; font-size: 74px; color: {CHALK}; text-shadow: 4px 4px 0 #000; }}
    #gc-t2 {{ margin-top: -6px; font-family: "League Gothic", sans-serif; font-size: 230px; line-height: 0.9; color: {RED};
      text-shadow: 6px 6px 0 #000, 0 10px 40px rgba(0,0,0,0.6); }}
""", f"""
    <div class="cam" id="gc-cam1">{vid("gc-v1", "frente.mp4", 0, 2.06, 0.0, 0.58)}</div>
    <div class="cam" id="gc-cam2">{vid("gc-v2", "tablero-km.mp4", 2.06, 2.14, 0.75, 0.55)}</div>
    <div class="cam" id="gc-cam3">{vid("gc-v3", "lateral.mp4", 4.2, 0.95, 0.3)}</div>
    <div class="scrim-top"></div>
    <div class="clip" id="gc-t" data-start="0" data-duration="2.06"><div id="gc-t1">El desastre</div><div id="gc-t2">DEL AÑO</div></div>
    {ink("gc-k", circle(330, 1168, 135, 72), 2.06, 2.14)}
    {hw("gc-sup", "¿“supuestamente”?", 300, 1340, 66, "", 2.4, 1.8, -4)}
    {hw("gc-q", "??", 860, 1000, 120, "r", 2.7, 1.5, 10)}
    {hw("gc-vw", "Volkswagen Gol", 60, 300, 82, "w", 4.2, 0.95, -3, 960)}
    <div class="flash" id="gc-flash"></div>
""", """
      tl.fromTo("#gc-cam1", { scale: 1.08 }, { scale: 1.0, duration: 2.0, ease: "power1.out" }, 0);
      tl.fromTo("#gc-t2", { scale: 1.25 }, { scale: 1, duration: 0.35, ease: "expo.out" }, 0);
      tl.fromTo("#gc-t1", { opacity: 0.0 }, { opacity: 1, duration: 0.25 }, 0.05);
      shake("#gc-cam1", 0.55);
      cut("#gc-cam2", 2.06, 1.2); flash("#gc-flash", 2.06, 0.5);
      draw("#gc-k .dr", 2.35, 0.5);
      write("#gc-sup", 2.4);
      pop("#gc-q", 2.7, 10);
      cut("#gc-cam3", 4.2, 1.1); flash("#gc-flash", 4.2, 0.4);
      write("#gc-vw", 4.3);
""")

# ============================================================ pintura 5.15–13.8
LAYERS = f'''<svg viewBox="0 0 900 520" width="900" height="520" style="position:absolute;left:90px;top:620px">
  <text x="40" y="60" font-family="Marker" font-weight="700" font-size="44" fill="{CHALK}">pintura normal</text>
  <rect id="pi-n" x="40" y="90" width="240" height="56" rx="6" fill="{GREEN}"/>
  <text x="300" y="132" font-family="Marker" font-weight="700" font-size="40" fill="{CHALK}">≈ 120 µm</text>
  <text x="40" y="260" font-family="Marker" font-weight="700" font-size="44" fill="{CHALK}">este carro</text>
  <rect id="pi-b" x="40" y="290" width="820" height="150" rx="8" fill="#b9a88a"/>
  <text x="70" y="390" font-family="Marker" font-weight="700" font-size="60" fill="#3a2f22">MASILLA</text>
  <text id="pi-bt" x="560" y="500" font-family="Marker" font-weight="700" font-size="54" fill="{RED}">+2000 µm</text>
</svg>'''
scene("pintura", f"""
    #pi-gfx {{ position: absolute; inset: 0; }}
    #pi-gk {{ position: absolute; left: 60px; top: 300px; }}
""", f"""
    <div class="cam" id="pi-cam1">{vid("pi-v1", "lateral.mp4", 0, 2.85, 1.2, 0.7)}</div>
    <div class="cam" id="pi-cam2">{vid("pi-v2", "maletero.mp4", 2.85, 2.35, 2.3)}</div>
    {img("pi-cam3", "medidor-2002.jpg", 5.2, 3.45, "Medidor de pintura marcando 2002 micras")}
    <div class="scrim-top"></div>
    <div class="lbl clip" id="pi-l1" data-start="0.1" data-duration="2.75">Estructura: MASILLA</div>
    {ink("pi-s", P("M150 1050 C260 990 330 1110 440 1040 C540 980 600 1100 720 1030 C800 990 860 1080 930 1040", YEL, 14) +
          P("M170 1130 C280 1080 350 1190 460 1120 C560 1060 620 1170 740 1110", YEL, 14), 1.8, 1.05)}
    <div class="lbl clip" id="pi-l2" data-start="2.95" data-duration="2.25">Mala pintura</div>
    {hw("pi-pes", "PÉSIMO", 560, 980, 120, "r", 3.95, 1.25, -6)}
    {ink("pi-c", circle(470, 850, 210, 115, RED, 14) + arrow(880, 540, 640, 740, RED, 12), 5.45, 3.2)}
    {hw("pi-m", "+2000 micras", 470, 330, 86, "r", 5.5, 3.15, -4)}
    <div class="clip" id="pi-gfx" data-start="6.7" data-duration="1.95"><div class="slate"></div>
      {hw("pi-gk", "un montón de masilla", 60, 300, 72, "w")}{LAYERS}</div>
    <div class="flash" id="pi-flash"></div><div class="redf" id="pi-red"></div>
""", """
      cut("#pi-cam1", 0); flash("#pi-flash", 0, 0.5);
      pop("#pi-l1", 0.1, -3);
      draw("#pi-s .dr", 1.85, 0.6, 0.15);
      cut("#pi-cam2", 2.85); flash("#pi-flash", 2.85, 0.4);
      pop("#pi-l2", 2.95, -3);
      pop("#pi-pes", 3.95, -6); shake("#pi-cam2", 3.98);
      cut("#pi-cam3", 5.2, 1.2); flash("#pi-flash", 5.2, 0.5);
      tl.fromTo("#pi-cam3-i", { scale: 1.0 }, { scale: 1.05, duration: 1.6, ease: "power1.inOut", transformOrigin: "44% 44%" }, 5.25);
      draw("#pi-c .dr", 5.45, 0.45, 0.1);
      write("#pi-m", 5.55);
      tl.fromTo("#pi-red", { opacity: 0.35 }, { opacity: 0, duration: 0.35, ...IR }, 5.6);
      tl.fromTo("#pi-gfx", { clipPath: "inset(100% 0% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.4, ease: "power3.inOut" }, 6.7);
      write("#pi-gk", 6.9);
      tl.fromTo("#pi-n", { scaleX: 0 }, { scaleX: 1, duration: 0.35, ease: "power2.out", svgOrigin: "40 118" }, 7.0);
      tl.fromTo("#pi-b", { scaleX: 0 }, { scaleX: 1, duration: 0.7, ease: "power2.out", svgOrigin: "40 365" }, 7.3);
      tl.fromTo("#pi-bt", { opacity: 0 }, { opacity: 1, duration: 0.2 }, 7.9);
""")

# ============================================================ tablero 13.8–17.2 (3.4)
scene("tablero", "", f"""
    {img("tb-cam", "tablero-desmontado.jpg", 0, 3.4, "Tablero con el tornillo removido")}
    <div class="scrim-top"></div>
    {ink("tb-c", circle(575, 1040, 120, 110, YEL, 14) + arrow(250, 680, 470, 960, YEL, 12), 0.4, 3.0)}
    {hw("tb-t", "Tablero desmontado", 60, 300, 84, "w", 0.25, 3.15, -3)}
    {hw("tb-t2", "¡TOTALMENTE!", 160, 460, 96, "r", 2.05, 1.35, -5)}
    <div class="flash" id="tb-flash"></div>
""", """
      cut("#tb-cam", 0, 1.2); flash("#tb-flash", 0, 0.5);
      tl.to("#tb-cam-i", { scale: 1.06, duration: 3.4, ease: "power1.inOut", transformOrigin: "54% 54%" }, 0);
      write("#tb-t", 0.25);
      draw("#tb-c .dr", 0.6, 0.45, 0.12);
      pop("#tb-t2", 2.05, -5);
""")

# ============================================================ maletero 17.2–23.3 (6.1)
scene("maletero", "", f"""
    <div class="cam" id="ml-cam1">{vid("ml-v1", "maletero.mp4", 0, 3.6, 4.8)}</div>
    <div class="cam" id="ml-cam2">{vid("ml-v2", "maletero.mp4", 3.6, 2.5, 3.0, 0.8)}</div>
    <div class="scrim-top"></div>
    <div class="lbl clip" id="ml-l" data-start="0.1" data-duration="6.0">Maletero</div>
    {hw("ml-m", "lleno de masilla", 80, 420, 80, "", 2.95, 3.15, -4)}
    {ink("ml-a", arrow(280, 640, 470, 860, RED, 14) + circle(560, 990, 270, 150, RED, 14), 4.45, 1.65)}
    {hw("ml-d", "DEFORMADO", 300, 560, 96, "", 4.5, 1.6, -5)}
    <div class="flash" id="ml-flash"></div>
""", """
      cut("#ml-cam1", 0); flash("#ml-flash", 0, 0.5);
      pop("#ml-l", 0.1, -3);
      write("#ml-m", 2.95);
      cut("#ml-cam2", 3.6, 1.1);
      draw("#ml-a .dr", 4.45, 0.4, 0.1);
      pop("#ml-d", 4.6, -5); shake("#ml-cam2", 4.65);
""")

# ============================================================ ramal 23.3–33.2 (9.9)
SCISSORS = P("M0 0 L120 80 M0 80 L120 0", RED, 14) + P("M-30 -14 a22 22 0 1 0 0.1 0", RED, 10) + P("M-30 94 a22 22 0 1 0 0.1 0", RED, 10)
BRAKE = (P("M0 -110 a110 110 0 1 1 -0.1 0", CHALK, 12) + P("M0 -42 a42 42 0 1 1 -0.1 0", CHALK, 10) +
         P("M60 -150 C150 -110 170 -20 140 40", YEL, 14) + cross(0, 0, 130, RED, 18))
scene("ramal", "", f"""
    <div class="cam" id="ra-cam1">{vid("ra-v1", "ramal.mp4", 0, 5.1, 3.4, 0.9)}</div>
    <div class="cam" id="ra-cam2">{vid("ra-v2", "motor.mp4", 5.1, 4.8, 7.6, 0.75)}</div>
    <div class="scrim-top"></div>
    <div class="lbl clip" id="ra-l" data-start="0.1" data-duration="5.0">Escáner: no se pudo</div>
    {ink("ra-sc", f'<g transform="translate(720 860) rotate(-20)">{SCISSORS}</g>' + P("M140 950 L960 820", YEL, 8, "dr"), 3.2, 1.9)}
    {hw("ra-t", "RAMAL CORTADO", 120, 560, 104, "r", 3.4, 1.7, -4)}
    {hw("ra-f", "manipulación en frenos", 60, 300, 70, "w", 5.25, 4.65, -3)}
    {ink("ra-b", f'<g transform="translate(780 640)">{BRAKE}</g>', 5.6, 4.3)}
    {hw("ra-c", "y en todo el cableado", 120, 820, 64, "", 8.2, 1.7, -4)}
    <div class="flash" id="ra-flash"></div>
""", """
      cut("#ra-cam1", 0); flash("#ra-flash", 0, 0.5);
      pop("#ra-l", 0.1, -3);
      draw("#ra-sc .dr", 3.2, 0.3, 0.06);
      pop("#ra-t", 3.4, -4); shake("#ra-cam1", 3.45);
      cut("#ra-cam2", 5.1); flash("#ra-flash", 5.1, 0.4);
      write("#ra-f", 5.25);
      draw("#ra-b .dr", 5.6, 0.45, 0.12);
      write("#ra-c", 8.2);
""")

# ============================================================ computadora 33.2–41.9 (8.7)
SER = f'''<svg viewBox="0 0 1080 900" width="1080" height="900" style="position:absolute;left:0;top:420px">
  <rect x="80" y="60" width="400" height="260" rx="18" fill="none" stroke="{CHALK}" stroke-width="8"/>
  <text x="120" y="130" font-family="Marker" font-weight="700" font-size="42" fill="{CHALK}">el carro</text>
  <text x="120" y="230" font-family="JetBrains Mono" font-weight="700" font-size="58" fill="{YEL}">••••••••</text>
  <rect x="600" y="60" width="400" height="260" rx="18" fill="none" stroke="{CHALK}" stroke-width="8"/>
  <text x="640" y="130" font-family="Marker" font-weight="700" font-size="42" fill="{CHALK}">la computadora</text>
  <text x="640" y="230" font-family="JetBrains Mono" font-weight="700" font-size="58" fill="{YEL}">••••••••</text>
  <g id="cp-neq"><line x1="500" y1="170" x2="580" y2="170" stroke="{RED}" stroke-width="14" stroke-linecap="round"/>
  <line x1="500" y1="210" x2="580" y2="210" stroke="{RED}" stroke-width="14" stroke-linecap="round"/>
  <line x1="565" y1="135" x2="515" y2="245" stroke="{RED}" stroke-width="14" stroke-linecap="round"/></g>
</svg>'''
scene("computadora", "", f"""
    <div class="cam" id="cp-cam">{vid("cp-v", "computadora.mp4", 0, 4.45, 0.4, 0.85)}</div>
    <div class="scrim-top"></div>
    <div class="lbl clip" id="cp-l" data-start="0.1" data-duration="4.35">Computadora (ECU)</div>
    {ink("cp-c", circle(560, 900, 330, 260, YEL, 14), 2.3, 2.15)}
    {hw("cp-t", "ABIERTA y reparada", 120, 420, 84, "r", 2.4, 2.05, -4)}
    <div class="clip" id="cp-gfx" data-start="4.45" data-duration="4.25" style="position:absolute;inset:0"><div class="slate"></div>
      {hw("cp-gt", "serie del escáner", 60, 300, 76, "w")}{SER}
      {hw("cp-no", "NO es de este carro", 110, 800, 88, "r")}</div>
    <div class="flash" id="cp-flash"></div>
""", """
      cut("#cp-cam", 0); flash("#cp-flash", 0, 0.5);
      pop("#cp-l", 0.1, -3);
      draw("#cp-c .dr", 2.3, 0.5);
      pop("#cp-t", 2.45, -4);
      tl.fromTo("#cp-gfx", { clipPath: "inset(0% 0% 0% 100%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.4, ease: "power3.inOut" }, 4.45);
      write("#cp-gt", 4.6);
      pop("#cp-neq", 7.0, 0);
      pop("#cp-no", 7.05, -4);
""")

# ============================================================ armado 41.9–51.2 (9.3) — carro "Frankenstein"
CAR = (P("M120 1120 L150 1010 Q180 960 260 950 L380 940 Q450 860 520 820 L760 815 Q830 820 880 900 L940 960 Q990 980 990 1040 L995 1120", CHALK, 10) +
       P("M120 1120 L230 1120 M370 1120 L720 1120 M860 1120 L995 1120", CHALK, 10) +
       P("M300 1120 a70 70 0 1 1 -0.1 0", CHALK, 10) + P("M790 1120 a70 70 0 1 1 -0.1 0", CHALK, 10) +
       P("M420 940 L520 850 L640 846 L640 940 Z M660 846 L760 846 Q810 860 850 935 L660 940 Z", CHALK, 7))
STITCH = lambda x1, y1, x2, y2, n: P(f"M{x1} {y1} L{x2} {y2}", RED, 7) + "".join(
    P(f"M{x1 + (x2 - x1) * k / n - 12} {y1 + (y2 - y1) * k / n - 18} L{x1 + (x2 - x1) * k / n + 12} {y1 + (y2 - y1) * k / n + 18}", RED, 6) for k in range(1, n))
PARTS = [("ar-p1", "computadora de otro carro", 60, 690, 820, 980, 560, 770, 3.85),
         ("ar-p2", "motor de otro carro", 600, 1230, 940, 1040, 780, 1230, 5.85),
         ("ar-p3", "ramal reconstruido", 60, 1230, 330, 1060, 300, 1230, 7.1)]
parts_html = ""
parts_js = ""
for pid, txt, tx, ty, ax, ay, bx, by, t in PARTS:
    parts_html += hw(pid, txt, tx, ty, 58, "", t, 9.3 - t, -3, 470)
    parts_html += ink(pid + "a", arrow(bx, by, ax, ay, YEL, 9), t, 9.3 - t)
    parts_js += f'      write("#{pid}", {t}); draw("#{pid}a .dr", {t + 0.1}, 0.35, 0.08);\n'
scene("armado", f"""
    #ar-t {{ position: absolute; left: 0; top: 390px; width: 1080px; text-align: center; font-family: "League Gothic", sans-serif;
      font-size: 150px; line-height: 0.92; color: {CHALK}; }}
    #ar-t b {{ color: {RED}; font-weight: 400; }}
""", f"""
    <div class="slate"></div>
    {hw("ar-k", "en pocas palabras…", 60, 300, 58, "w", 0.0, 9.3, -2)}
    <div class="clip" id="ar-t" data-start="0.3" data-duration="9.0">ESTE CARRO ESTABA<br /><b>TOTALMENTE ARMADO</b></div>
    {ink("ar-car", CAR + STITCH(430, 950, 470, 1120, 5) + STITCH(700, 820, 720, 1120, 7) + STITCH(150, 1040, 990, 1040, 14), 1.1, 8.2)}
    {parts_html}
    <div class="flash" id="ar-flash"></div>
""", f"""
      flash("#ar-flash", 0, 0.5);
      write("#ar-k", 0.05);
      tl.fromTo("#ar-t", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "expo.out" }}, 0.3);
      tl.fromTo("#ar-t b", {{ scale: 1.4 }}, {{ scale: 1, duration: 0.25, ease: "power4.in" }}, 2.55);
      draw("#ar-car .dr", 1.1, 0.5, 0.05);
{parts_js}""")

# ============================================================ culata 51.2–55.3 (4.1)
scene("culata", "", f"""
    <div class="cam" id="cu-cam">{vid("cu-v", "culata.mp4", 0, 4.1, 1.2, 0.8)}</div>
    <div class="scrim-top"></div>
    <div class="lbl clip" id="cu-l" data-start="0.1" data-duration="4.0">Culata reparada</div>
    {ink("cu-c", circle(560, 960, 330, 200, YEL, 14), 0.6, 3.5)}
    {hw("cu-t", "…y MUY MAL reparada", 70, 420, 82, "r", 2.6, 1.5, -4)}
    {ink("cu-x", cross(540, 960, 170), 2.7, 1.4)}
    <div class="flash" id="cu-flash"></div>
""", """
      cut("#cu-cam", 0); flash("#cu-flash", 0, 0.5);
      pop("#cu-l", 0.1, -3);
      draw("#cu-c .dr", 0.6, 0.5);
      write("#cu-t", 2.6);
      draw("#cu-x .dr", 2.75, 0.25, 0.1); shake("#cu-cam", 2.9);
""")

# ============================================================ agua 55.3–57.9 (2.6)
DROP = P("M0 -120 C40 -50 90 0 90 50 a90 90 0 1 1 -180 0 C-90 0 -40 -50 0 -120 Z", "#5ec8ff", 12)
scene("agua", "", f"""
    <div class="cam" id="ag-cam">{vid("ag-v", "refrigerante.mp4", 0, 2.6, 0.4, 0.9)}</div>
    <div class="scrim-top"></div>
    {hw("ag-t1", "sin refrigerante", 60, 300, 80, "w", 0.05, 2.55, -3)}
    {ink("ag-d", f'<g transform="translate(860 560)">{DROP}</g>', 1.15, 1.45)}
    {hw("ag-t2", "PURA AGUA", 140, 1010, 120, "", 1.4, 1.2, -5)}
    <div class="flash" id="ag-flash"></div>
""", """
      cut("#ag-cam", 0); flash("#ag-flash", 0, 0.5);
      write("#ag-t1", 0.05);
      draw("#ag-d .dr", 1.15, 0.5);
      pop("#ag-t2", 1.4, -5);
""")

# ============================================================ radiador 57.9–62.0 (4.1)
TRUCK = (P("M0 0 L260 0 L260 140 L0 140 Z", CHALK, 10) + P("M260 40 L360 40 L410 100 L410 140 L260 140", CHALK, 10) +
         P("M80 140 a34 34 0 1 1 -0.1 0", CHALK, 9) + P("M340 140 a34 34 0 1 1 -0.1 0", CHALK, 9))
scene("radiador", "", f"""
    <div class="cam" id="rd-cam">{vid("rd-v", "radiador.mp4", 0, 4.1, 3.6, 0.85)}</div>
    <div class="scrim-top"></div>
    <div class="lbl clip" id="rd-l" data-start="0.1" data-duration="4.0">Radiador adaptado</div>
    {ink("rd-tk", f'<g transform="translate(560 470)">{TRUCK}</g>', 1.5, 2.6)}
    {hw("rd-t", "celdas de un CAMIÓN", 120, 1040, 82, "r", 2.2, 1.9, -4)}
    <div class="flash" id="rd-flash"></div>
""", """
      cut("#rd-cam", 0); flash("#rd-flash", 0, 0.5);
      pop("#rd-l", 0.1, -3);
      draw("#rd-tk .dr", 1.5, 0.4, 0.08);
      write("#rd-t", 2.2);
""")

# ============================================================ aceite 62.0–69.7 (7.7)
drops = "".join(f'<g class="od" id="ac-o{i}"><path d="M0 0 C14 22 22 34 22 46 a22 22 0 1 1 -44 0 C-22 34 -14 22 0 0 Z" fill="#2a1d0a" stroke="{YEL}" stroke-width="6"/></g>' for i in range(5))
scene("aceite", f"""
    #ac-drops {{ position: absolute; inset: 0; }}
""", f"""
    <div class="cam" id="ac-cam1">{vid("ac-v1", "aceite.mp4", 0, 4.2, 0.0, 0.8)}</div>
    <div class="cam" id="ac-cam2">{vid("ac-v2", "aceite.mp4", 4.2, 3.5, 3.6, 0.7)}</div>
    <div class="scrim-top"></div>
    {hw("ac-t0", "de verdad, el desastre", 60, 300, 72, "w", 0.0, 2.3, -3)}
    <div class="lbl clip" id="ac-l" data-start="2.35" data-duration="5.35">Fuga de aceite</div>
    <div class="clip" id="ac-drops" data-start="2.5" data-duration="5.2"><svg class="ink" viewBox="0 0 1080 1920">{drops}</svg></div>
    {hw("ac-t", "retenes de cigüeñal", 120, 1040, 80, "", 5.1, 2.6, -4)}
    <div class="flash" id="ac-flash"></div>
""", """
      cut("#ac-cam1", 0); flash("#ac-flash", 0, 0.5);
      write("#ac-t0", 0.0);
      pop("#ac-l", 2.35, -3);
      [[260, 2.5], [520, 2.9], [780, 3.3], [400, 3.9], [660, 4.4]].forEach(([x, t], i) => {
        tl.fromTo("#ac-o" + i, { x: x, y: 520, scale: 0.4, opacity: 0 }, { x: x, y: 520, scale: 1, opacity: 1, duration: 0.25, ease: "back.out(2)" }, t);
        tl.to("#ac-o" + i, { y: 1000, duration: 1.0, ease: "power2.in" }, t + 0.35);
        tl.to("#ac-o" + i, { opacity: 0, scaleX: 2.2, scaleY: 0.3, duration: 0.2 }, t + 1.45);
      });
      cut("#ac-cam2", 4.2, 1.08);
      write("#ac-t", 5.1);
""")

# ============================================================ veredicto 69.7–72.1 (2.4)
scene("veredicto", f"""
    #ve-n {{ position: absolute; left: 0; top: 300px; width: 1080px; text-align: center; font-family: "League Gothic", sans-serif;
      font-size: 330px; line-height: 0.85; color: {RED}; }}
    #ve-s {{ position: absolute; left: 0; top: 590px; width: 1080px; text-align: center; font-family: "League Gothic", sans-serif;
      font-size: 120px; color: {CHALK}; letter-spacing: 0.04em; }}
    #ve-km {{ position: absolute; left: 0; top: 960px; width: 1080px; text-align: center; font-family: "Marker", cursive; font-weight: 700;
      font-size: 84px; color: {YEL}; }}
""", f"""
    <div class="slate"></div>
    {hw("ve-p", "PÉSIMO", 330, 230, 76, "w", 0.0, 2.4, -6)}
    <div class="clip" id="ve-n" data-start="0.0" data-duration="2.4">16</div>
    <div class="clip" id="ve-s" data-start="0.0" data-duration="2.4">FALLAS GRAVES</div>
    <div class="clip" id="ve-km" data-start="0.65" data-duration="1.75">…¿y solo 22 000 km?</div>
    {ink("ve-u", P("M220 1070 C400 1100 700 1050 880 1080", RED, 12), 0.9, 1.5)}
    <div class="flash" id="ve-flash"></div>
""", """
      flash("#ve-flash", 0, 0.6);
      tl.fromTo("#ve-n", { scale: 1.8, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.22, ease: "power4.in" }, 0.0);
      tl.fromTo("#ve-s", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, ease: "expo.out" }, 0.15);
      write("#ve-km", 0.65);
      draw("#ve-u .dr", 0.95, 0.35);
""")

# ============================================================ consejo 72.1–75.95 (3.85)
scene("consejo", "", f"""
    <div class="cam" id="cs-cam">{vid("cs-v", "lateral.mp4", 0, 3.85, 0.0, 0.84)}</div>
    <div class="scrim-top"></div>
    {hw("cs-t", "Tengan <span style='color:#ffe14d'>MUCHO</span> cuidado al comprar un carro", 60, 300, 72, "w", 0.1, 3.75, -3, 960)}
    <div class="flash" id="cs-flash"></div>
""", """
      cut("#cs-cam", 0); flash("#cs-flash", 0, 0.5);
      write("#cs-t", 0.1);
""")

# ============================================================ cierre 75.95–80.5 (4.55)
scene("cierre", f"""
    #root {{ background: {SLATE}; }}
    #ci-plate {{ position: absolute; left: 240px; top: 330px; width: 600px; height: 420px; border-radius: 20px; background: #f9f9f9;
      display: flex; align-items: center; justify-content: center; transform: rotate(-2deg); box-shadow: 10px 14px 0 rgba(0,0,0,0.5); }}
    #ci-plate img {{ width: 540px; height: auto; }}
    #ci-tel {{ position: absolute; left: 150px; top: 1010px; width: 780px; height: 150px; border-radius: 18px; background: {RED};
      display: flex; align-items: center; justify-content: center; gap: 22px; font-family: "League Gothic", sans-serif; font-size: 112px;
      color: #fff; letter-spacing: 0.03em; box-shadow: 8px 10px 0 rgba(0,0,0,0.5); }}
""", f"""
    <div class="clip" id="ci-plate" data-start="0.05" data-duration="4.5"><img src="assets/brand/logo.png" alt="Check Autos" /></div>
    {hw("ci-t", "Confía en Check Autos", 150, 820, 78, "w", 0.3, 4.25, -2)}
    {ink("ci-u", P("M180 930 C420 960 700 915 930 945", YEL, 12), 0.7, 3.85)}
    <div class="clip" id="ci-tel" data-start="1.0" data-duration="3.55">
      <svg viewBox="0 0 24 24" width="66" height="66"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z" fill="#fff"/></svg>
      <span>959 365 374</span></div>
""", """
      pop("#ci-plate", 0.05, -2);
      write("#ci-t", 0.3);
      draw("#ci-u .dr", 0.75, 0.35);
      pop("#ci-tel", 1.0, 0);
""")

# ============================================================ medidor de desastre (HUD) 5.15–69.7
HITS = [7.5, 9.0, 11.0, 15.45, 21.1, 21.7, 27.2, 31.1, 35.85, 40.5, 47.7, 49.95, 54.6, 55.9, 59.2, 64.95]
HUD_START = 5.15
segs = "".join(f'<div class="hs" id="hs{i}"></div>' for i in range(len(HITS)))
hjs = "\n".join(
    f'      tl.fromTo("#hs{i}", {{ backgroundColor: "rgba(255,255,255,0.18)", scaleY: 1 }}, {{ backgroundColor: "#ff3b30", scaleY: 1.6, duration: 0.12, ease: "power2.out" }}, {t - HUD_START:.2f});\n'
    f'      tl.to("#hs{i}", {{ scaleY: 1, duration: 0.2 }}, {t - HUD_START + 0.12:.2f});\n'
    f'      tl.set("#hd-n", {{ textContent: "{i + 1}" }}, {t - HUD_START:.2f});\n'
    f'      tl.fromTo("#hd-n", {{ scale: 1.6 }}, {{ scale: 1, duration: 0.25, ease: "back.out(2)", ...IR }}, {t - HUD_START:.2f});'
    for i, t in enumerate(HITS))
scene("hud", f"""
    #root {{ background: transparent; }}
    #hd {{ position: absolute; left: 60px; top: 178px; width: 960px; height: 96px; padding: 10px 18px; border-radius: 14px;
      background: rgba(0,0,0,0.62); display: flex; align-items: center; gap: 18px; }}
    #hd-l {{ flex: none; font-family: "Marker", cursive; font-weight: 700; font-size: 30px; color: {CHALK}; line-height: 1; width: 170px; }}
    #hd-bar {{ flex: 1; display: flex; gap: 6px; height: 30px; }}
    #root .hs {{ flex: 1; border-radius: 4px; background: rgba(255,255,255,0.18); }}
    #hd-n {{ flex: none; width: 90px; text-align: center; font-family: "League Gothic", sans-serif; font-size: 76px; color: {RED}; line-height: 1; }}
""", f"""
    <div id="hd"><div id="hd-l">nivel de desastre</div><div id="hd-bar">{segs}</div><div id="hd-n">0</div></div>
""", f"""
      tl.fromTo("#hd", {{ y: -40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "expo.out" }}, 0.05);
{hjs}
      tl.to("#hd", {{ opacity: 0, duration: 0.25 }}, {69.7 - HUD_START - 0.25:.2f});
""")
print("scenes written")
