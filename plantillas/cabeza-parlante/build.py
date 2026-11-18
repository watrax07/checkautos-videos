# Video 6 — "Mitos vs Realidad" (cabeza parlante). Escribe compositions/*.html e index.html. Run: python _work/build.py
import json, os

ROOT = os.path.join(os.path.dirname(__file__), "..")
RED, GREEN, NAVY, YEL, WHITE = "#e63946", "#16a34a", "#0f172a", "#facc15", "#ffffff"
SEGS = json.load(open(os.path.join(ROOT, "_work/segments.json")))["segments"]
TALK = 42.466
TOTAL = 46.0

BASE = f"""
    #root {{ position: absolute; inset: 0; overflow: hidden; background: transparent; }}
    #root .cam {{ position: absolute; inset: 0; transform-origin: 50% 50%; }}
    #root .cam video {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
    #root .flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; }}
"""
CHECK = '<svg viewBox="0 0 24 24" width="40" height="40"><path d="M4 12.5l5 5L20 6.5" fill="none" stroke="#fff" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CROSS = '<svg viewBox="0 0 24 24" width="40" height="40"><path d="M6 6l12 12M18 6L6 18" fill="none" stroke="#fff" stroke-width="3.6" stroke-linecap="round"/></svg>'


def write(cid, css, body, js):
    html = f"""<template>
  <style>{BASE}{css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
{body}
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
      const IR = {{ immediateRender: false }};
{js}
      window.__timelines["{cid}"] = tl;
    }})();
  </script>
</template>
"""
    open(os.path.join(ROOT, "compositions", f"{cid}.html"), "w", encoding="utf-8", newline="\n").write(html)


os.makedirs(os.path.join(ROOT, "compositions"), exist_ok=True)

# ------------------------------------------------------------ talk: video base con zooms alternos en cada corte
cuts = [round(s["out_a"], 3) for s in SEGS]
zoom = {0.0: 1.0}
punch_js = []
for k, t in enumerate(cuts):
    z = 1.0 if k % 2 == 0 else 1.13
    punch_js.append(f'      tl.set("#tk-cam", {{ scale: {z} }}, {t});')
write("talk", """
    #root { background: #000; }
""", f"""
    <div class="cam" id="tk-cam"><video id="tk-v" class="clip" src="assets/media/talk-edit.mp4" data-start="0" data-duration="{TALK}" muted playsinline></video></div>
""", f"""      tl.set("#tk-cam", {{ transformOrigin: "50% 30%" }}, 0);
{chr(10).join(punch_js)}
""")

# ------------------------------------------------------------ broll: cortes a imágenes reales de Check Autos
BROLL = [("br1", "caja-cambios.mp4", 3.1, 2.45, 0.2, None), ("br2", "motor.mp4", 6.4, 2.15, 3.0, None),
         ("br3", "tablero.mp4", 15.3, 3.75, 4.55, 0.35), ("br4", "caja-cambios.mp4", 23.9, 2.1, 4.4, None),
         ("br5", "motor.mp4", 31.4, 3.1, 0.0, 0.9), ("br6", "colorado.mp4", 38.8, 1.1, 0.6, None),
         ("br7", "sentra.mp4", 39.9, 1.3, 0.5, None)]
b_html, b_js = [], ['      tl.set("#br-flash", { opacity: 0 }, 0);']
for bid, src, st, du, ms, rate in BROLL:
    r = f' data-playback-rate="{rate}"' if rate else ""
    b_html.append(f'    <div class="cam" id="{bid}"><video id="{bid}-v" class="clip" src="assets/broll/{src}" '
                  f'data-start="{st}" data-duration="{du}" data-media-start="{ms}"{r} muted playsinline></video></div>')
    b_js.append(f'      tl.fromTo("#{bid}", {{ scale: 1.14 }}, {{ scale: 1, duration: 0.5, ease: "expo.out" }}, {st});')
    b_js.append(f'      tl.fromTo("#br-flash", {{ opacity: 0.45 }}, {{ opacity: 0, duration: 0.2, ease: "power2.out", ...IR }}, {st});')
b_html.append('    <div class="flash" id="br-flash"></div>')
write("broll", """
    #root .cam video { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }
""", "\n".join(b_html), "\n".join(b_js))

# ------------------------------------------------------------ cards: tarjetas y gráficos generados
BOOK = f'''<svg viewBox="0 0 120 90" width="150" height="112"><path d="M60 16 C45 6 22 6 8 12 V82 C22 76 45 76 60 86 Z" fill="{NAVY}"/>
<path d="M60 16 C75 6 98 6 112 12 V82 C98 76 75 76 60 86 Z" fill="#1e293b"/><g id="cd-page"><path d="M60 16 C72 8 92 8 104 12 V76 C92 72 72 72 60 80 Z" fill="#f1f5f9"/>
<line x1="70" y1="28" x2="96" y2="24" stroke="#94a3b8" stroke-width="3"/><line x1="70" y1="40" x2="96" y2="36" stroke="#94a3b8" stroke-width="3"/><line x1="70" y1="52" x2="90" y2="49" stroke="#94a3b8" stroke-width="3"/></g></svg>'''
MACHINE = f'''<svg viewBox="0 0 300 170" width="250" height="142"><rect x="20" y="20" width="120" height="140" rx="14" fill="{NAVY}"/>
<rect x="36" y="36" width="88" height="44" rx="6" fill="#22d3ee"/><circle cx="56" cy="110" r="10" fill="{YEL}"/><circle cx="90" cy="110" r="10" fill="{GREEN}"/>
<path id="cd-hose1" d="M140 60 C200 60 210 100 280 100" fill="none" stroke="#f59e0b" stroke-width="10" stroke-dasharray="16 12"/>
<path id="cd-hose2" d="M140 120 C200 120 210 140 280 140" fill="none" stroke="#64748b" stroke-width="10" stroke-dasharray="16 12"/></svg>'''
cards_css = f"""
    #root .card {{ position: absolute; left: 70px; width: 940px; top: 1030px; }}
    #root .card-in {{ display: flex; align-items: center; gap: 26px; padding: 22px 30px; border-radius: 28px; background: {WHITE};
      box-shadow: 0 22px 50px rgba(0,0,0,0.35); }}
    #root .badge {{ flex: none; display: flex; align-items: center; gap: 10px; padding: 10px 20px 12px 14px; border-radius: 999px;
      font-family: "Poppins", sans-serif; font-weight: 800; font-size: 34px; color: #fff; letter-spacing: 0.04em; }}
    #root .badge.mito {{ background: {RED}; }}
    #root .badge.real {{ background: {GREEN}; }}
    #root .card-t {{ font-family: "Poppins", sans-serif; font-weight: 700; font-size: 40px; line-height: 1.12; color: {NAVY}; }}
    #root .chips {{ position: absolute; left: 70px; top: 1060px; width: 940px; display: flex; gap: 18px; flex-wrap: wrap; }}
    #root .chip {{ padding: 14px 30px 16px; border-radius: 999px; background: {NAVY}; font-family: "Poppins", sans-serif; font-weight: 800;
      font-size: 42px; color: #fff; box-shadow: 0 14px 30px rgba(0,0,0,0.35); }}
    #root .chip.y {{ background: {YEL}; color: {NAVY}; }}
    #hd {{ position: absolute; left: 0; top: 990px; width: 1080px; display: flex; flex-direction: column; align-items: center; gap: 4px; }}
    #hd-1, #hd-2 {{ display: inline-block; font-family: "Poppins", sans-serif; font-weight: 900; font-size: 92px; line-height: 1; padding: 14px 34px 20px;
      border-radius: 22px; color: #fff; box-shadow: 0 20px 50px rgba(0,0,0,0.4); }}
    #hd-1 {{ background: {RED}; }}
    #hd-2 {{ background: {GREEN}; }}
    #hd-vs {{ display: block; margin: 0; font-family: "Poppins", sans-serif; font-weight: 900; font-size: 44px; color: #fff;
      text-shadow: 0 4px 16px rgba(0,0,0,0.7); }}
    #odo {{ position: absolute; left: 140px; top: 760px; width: 800px; padding: 26px 30px 30px; border-radius: 28px; background: {NAVY};
      box-shadow: 0 24px 60px rgba(0,0,0,0.5); text-align: center; }}
    #odo-l {{ font-family: "Inter", sans-serif; font-weight: 800; font-size: 30px; letter-spacing: 0.18em; color: #94a3b8; }}
    #odo-v {{ margin-top: 8px; font-family: "JetBrains Mono", monospace; font-weight: 700; font-size: 120px; line-height: 1; color: {YEL}; }}
    #odo-v small {{ font-size: 48px; color: #fff; margin-left: 12px; }}
    #odo-s {{ margin-top: 10px; font-family: "Poppins", sans-serif; font-weight: 600; font-size: 34px; color: #e2e8f0; }}
    #tank {{ position: absolute; left: 70px; top: 1010px; width: 940px; height: 175px; border-radius: 28px; background: {WHITE};
      box-shadow: 0 22px 50px rgba(0,0,0,0.35); }}
    #tank-box {{ position: absolute; left: 40px; top: 22px; width: 280px; height: 130px; border: 8px solid {NAVY}; border-radius: 20px; overflow: hidden; }}
    #tank-fl {{ position: absolute; left: 0; bottom: 0; width: 100%; height: 100%; background: #dc2626; transform-origin: 50% 100%; }}
    #tank-t1, #tank-t2 {{ position: absolute; left: 360px; font-family: "Poppins", sans-serif; font-weight: 800; font-size: 50px; }}
    #tank-t1 {{ top: 18px; color: {RED}; }}
    #tank-t2 {{ top: 88px; color: {GREEN}; }}
    #mach {{ position: absolute; left: 70px; top: 1010px; width: 940px; height: 175px; border-radius: 28px; background: {WHITE};
      box-shadow: 0 22px 50px rgba(0,0,0,0.35); display: flex; align-items: center; gap: 24px; padding: 0 30px; }}
    #cu1, #cu2 {{ position: absolute; left: 0; width: 1080px; text-align: center; font-family: "Poppins", sans-serif; font-weight: 900;
      font-size: 96px; line-height: 1; color: #fff; text-shadow: 0 8px 30px rgba(0,0,0,0.7); }}
    #cu1 {{ top: 760px; }}
    #cu2 {{ top: 880px; color: {YEL}; }}
"""


def card(cid, kind, title, start, dur, top=1030, icon=""):
    lab = "MITO" if kind == "mito" else "REALIDAD"
    ic = CROSS if kind == "mito" else CHECK
    return (f'    <div class="card clip" id="{cid}" data-start="{start}" data-duration="{dur}" style="top: {top}px"><div class="card-in">'
            f'<div class="badge {kind}">{ic}{lab}</div><div class="card-t">{title}</div>{icon}</div></div>')


cards_html = f"""
    <div class="clip" id="hd" data-start="0" data-duration="1.33"><span id="hd-1">MITOS</span><span id="hd-vs">vs</span><span id="hd-2">REALIDAD</span></div>
{card("cd-m1", "mito", "A la caja CVT no se le hace mantenimiento", 2.2, 3.35)}
{card("cd-m2", "mito", "No se le cambia el fluido: quedará mal", 5.6, 2.95)}
{card("cd-r1", "real", "Hazle caso al manual del fabricante", 8.75, 2.5, icon=f'<div>{BOOK}</div>')}
    <div class="chips clip" id="cd-ch1" data-start="12.7" data-duration="2.6"><div class="chip y" id="cd-c1">¿Cuándo?</div><div class="chip" id="cd-c2">Fluido</div><div class="chip" id="cd-c3">Filtro</div></div>
    <div class="clip" id="odo" data-start="15.55" data-duration="3.5"><div id="odo-l">CAMBIO DE FLUIDO ENTRE</div>
      <div id="odo-v"><span id="odo-n">80 000</span><small>km</small></div><div id="odo-s" class="clip" data-start="17.0" data-duration="2.05">Según marca y año</div></div>
{card("cd-r2", "real", "Guíate por el manual del fabricante", 19.5, 3.2, icon=f'<div>{BOOK.replace("cd-page", "cd-page2")}</div>')}
{card("cd-m3", "mito", "Abrir un tapón y listo", 24.3, 2.7)}
    <div class="clip" id="tank" data-start="27.1" data-duration="2.1"><div id="tank-box"><div id="tank-fl"></div></div>
      <div id="tank-t1">1 · Drenar</div><div id="tank-t2">2 · Rellenar</div></div>
    <div class="clip" id="mach" data-start="29.2" data-duration="1.6"><div>{MACHINE}</div><div class="card-t">Máquinas que lo hacen bien</div></div>
{card("cd-r3", "real", "Talleres con el equipo adecuado", 32.4, 2.15)}
    <div class="chips clip" id="cd-ch2" data-start="36.2" data-duration="2.55"><div class="chip y" id="cd-c4">¿Dónde lo haces?</div><div class="chip y" id="cd-c5">¿Cuándo?</div></div>
    <div class="clip" id="cu1" data-start="39.25" data-duration="1.9">Cuida tu máquina</div>
    <div class="clip" id="cu2" data-start="40.1" data-duration="1.1">Cuida tu inversión</div>
"""


def cin(cid, t):
    return (f'      tl.fromTo("#{cid} .card-in", {{ y: 60, scale: 0.9, opacity: 0 }}, {{ y: 0, scale: 1, opacity: 1, duration: 0.4, ease: "back.out(1.8)" }}, {t});\n'
            f'      tl.fromTo("#{cid} .badge", {{ scale: 0 }}, {{ scale: 1, duration: 0.3, ease: "back.out(2.4)" }}, {t + 0.12});')


cards_js = f"""
      // frame 0: MITOS vs REALIDAD ya en pantalla
      tl.fromTo("#hd-1", {{ x: -40 }}, {{ x: 0, duration: 0.5, ease: "expo.out" }}, 0);
      tl.fromTo("#hd-2", {{ scale: 1 }}, {{ keyframes: [{{ scale: 1.12, duration: 0.12 }}, {{ scale: 1, duration: 0.2 }}] }}, 0.96);
{cin("cd-m1", 2.2)}
{cin("cd-m2", 5.6)}
{cin("cd-r1", 8.75)}
      tl.fromTo("#cd-page", {{ scaleX: 1, svgOrigin: "60 50" }}, {{ scaleX: -1, svgOrigin: "60 50", duration: 0.6, ease: "power2.inOut" }}, 9.9);
      [["#cd-c1", 12.7], ["#cd-c2", 14.25], ["#cd-c3", 14.9]].forEach(([c, t]) => {{
        tl.fromTo(c, {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2.4)" }}, t);
      }});
      tl.fromTo("#odo", {{ y: 80, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.45, ease: "expo.out" }}, 15.55);
      (function () {{
        const o = {{ v: 80000 }}; const n = document.querySelector("#odo-n");
        const f = (v) => Math.round(v / 1000) * 1000;
        tl.fromTo(o, {{ v: 80000 }}, {{ v: 100000, duration: 0.6, ease: "power2.inOut", onUpdate: () => {{ n.textContent = f(o.v).toLocaleString("es-PE").replace(/,/g, " ").replace(/\\./g, " "); }} }}, 16.45);
      }})();
      tl.fromTo("#odo-s", {{ opacity: 0, y: 10 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, 17.0);
{cin("cd-r2", 19.5)}
{cin("cd-m3", 24.3)}
      tl.fromTo("#tank", {{ y: 60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "back.out(1.6)" }}, 27.1);
      tl.fromTo("#tank-fl", {{ scaleY: 1 }}, {{ scaleY: 0.08, duration: 0.7, ease: "power2.inOut" }}, 27.6);
      tl.fromTo("#tank-fl", {{ backgroundColor: "#7f1d1d" }}, {{ backgroundColor: "#dc2626", duration: 0.01, ...IR }}, 28.4);
      tl.to("#tank-fl", {{ scaleY: 0.92, duration: 0.6, ease: "power2.out" }}, 28.55);
      tl.fromTo("#tank-t1", {{ opacity: 0.25 }}, {{ opacity: 1, duration: 0.2 }}, 27.6);
      tl.fromTo("#tank-t2", {{ opacity: 0.25 }}, {{ opacity: 1, duration: 0.2 }}, 28.55);
      tl.fromTo("#mach", {{ y: 60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "back.out(1.6)" }}, 29.2);
      tl.fromTo("#cd-hose1, #cd-hose2", {{ strokeDashoffset: 0 }}, {{ strokeDashoffset: -112, duration: 1.6, ease: "none" }}, 29.2);
{cin("cd-r3", 32.4)}
      [["#cd-c4", 36.2], ["#cd-c5", 37.9]].forEach(([c, t]) => {{
        tl.fromTo(c, {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2.4)" }}, t);
      }});
      tl.fromTo("#cu1", {{ y: 40, opacity: 0, scale: 0.8 }}, {{ y: 0, opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, 39.25);
      tl.fromTo("#cu2", {{ y: 40, opacity: 0, scale: 0.8 }}, {{ y: 0, opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, 40.1);
"""
write("cards", cards_css, cards_html, cards_js)

# ------------------------------------------------------------ cierre
write("cierre", f"""
    #root {{ background: {NAVY}; }}
    #ci-bg {{ position: absolute; inset: 0; background: radial-gradient(circle at 50% 30%, #1e3a8a 0%, {NAVY} 70%); }}
    #ci-plate {{ position: absolute; left: 215px; top: 330px; width: 650px; height: 460px; border-radius: 28px; background: #f9f9f9;
      display: flex; align-items: center; justify-content: center; box-shadow: 0 30px 70px rgba(0,0,0,0.5); }}
    #ci-plate img {{ width: 580px; height: auto; display: block; }}
    #ci-t {{ position: absolute; left: 0; top: 850px; width: 1080px; text-align: center; font-family: "Poppins", sans-serif; font-weight: 900;
      font-size: 72px; color: #fff; }}
    #ci-s {{ position: absolute; left: 0; top: 945px; width: 1080px; text-align: center; font-family: "Poppins", sans-serif; font-weight: 600;
      font-size: 38px; color: #cbd5e1; }}
    #ci-tel {{ position: absolute; left: 140px; top: 1040px; width: 800px; height: 160px; border-radius: 999px; background: {GREEN};
      display: flex; align-items: center; justify-content: center; gap: 24px; box-shadow: 0 20px 50px rgba(22,163,74,0.35); }}
    #ci-tel-n {{ font-family: "Poppins", sans-serif; font-weight: 900; font-size: 92px; line-height: 1; color: #fff; }}
""", f"""
    <div id="ci-bg"></div>
    <div class="clip" id="ci-plate" data-start="0" data-duration="4.8"><img src="assets/brand/logo.png" alt="Check Autos" /></div>
    <div class="clip" id="ci-t" data-start="0.35" data-duration="4.45">Somos Check Autos</div>
    <div class="clip" id="ci-s" data-start="0.6" data-duration="4.2">Revisión técnica vehicular</div>
    <div class="clip" id="ci-tel" data-start="1.1" data-duration="3.7">
      <svg viewBox="0 0 24 24" width="62" height="62"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z" fill="#fff"/></svg>
      <div id="ci-tel-n">959 365 374</div>
    </div>
""", """
      tl.fromTo("#ci-bg", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0);
      tl.fromTo("#ci-plate", { scale: 0.6, opacity: 0, rotation: -6 }, { scale: 1, opacity: 1, rotation: 0, duration: 0.55, ease: "back.out(1.6)" }, 0.05);
      tl.fromTo("#ci-t", { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "expo.out" }, 0.35);
      tl.fromTo("#ci-s", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0.6);
      tl.fromTo("#ci-tel", { scale: 0.7, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.45, ease: "back.out(1.8)" }, 1.1);
""")
print("compositions written; cuts at", cuts)
