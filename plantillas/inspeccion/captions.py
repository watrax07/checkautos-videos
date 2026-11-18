# Writes compositions/captions.html from assets/transcript.json (word timings of assets/voz-limpia.wav).
import json, os

ROOT = os.path.join(os.path.dirname(__file__), "..")
VOICE_START = 0.3
LAST = 176  # "carro" — el cierre dice "Confía en Check Autos"

w = json.load(open(os.path.join(ROOT, "assets/transcript.json"), encoding="utf8"))
words = [dict(x) for x in (w if isinstance(w, list) else w["words"])]

import re
T = {w["text"].strip(".,¿?!").lower(): None for w in words}
fixmap = {"baden": "Volkswagen", "golf.": "Gol.", "masía.": "masilla.", "macia,": "masilla,", "cableador.": "cableado.",
          "rallador": "radiador", "tienes": "retenes", "22.000": "22 000", "veintidós": "22", "mil": "mil"}
for w in words:
    k = w["text"].lower()
    if k in fixmap: w["text"] = fixmap[k]
drop = set()

accent = {"desastre", "22", "000", "kilómetros", "estructural", "masillado", "pintura", "pésimo", "2000", "micras", "masilla", "tablero",
          "desmontado", "totalmente", "maletero", "deformado", "ramal", "cortado", "manipulación", "frenos", "cableado", "computadora",
          "abierta", "reparada", "serie", "pertenecía", "armado", "motor", "otro", "reconstruido", "culata", "mal", "refrigerante",
          "agua", "radiador", "adaptado", "camión", "aceite", "retenes", "cigüeñal", "cuidado"}

HIDE = [(1.95, 4.2), (41.8, 51.0)]  # el odómetro y el carro "armado" ya muestran lo que se dice
seq = [dict(words[i], i=i) for i in range(0, LAST + 1) if i not in drop and not any(a <= words[i]["start"] + VOICE_START < b for a, b in HIDE)]
groups, cur = [], []
for x in seq:
    if cur:
        prev = cur[-1]
        gap = x["start"] - prev["end"]
        endp = prev["text"][-1] in ".,?!"
        if len(cur) >= 3 or endp or gap >= 0.15 or (len(cur) >= 2 and len("".join(c["text"] for c in cur)) > 14):
            groups.append(cur); cur = []
    cur.append(x)
if cur:
    groups.append(cur)

r = lambda v: round(v + VOICE_START, 3)
clean = lambda t: t.strip(".,¿?!")
out = []
for gi, g in enumerate(groups):
    s = r(g[0]["start"] - 0.04)
    nxt = r(groups[gi + 1][0]["start"] - 0.04) if gi + 1 < len(groups) else 999
    e = min(nxt, r(g[-1]["end"] + 0.25))
    spans = "".join(
        f'<span class="cw{" acc" if clean(x["text"]).lower().rstrip(",") in accent else ""}" id="cw-{x["i"]}" '
        f'data-s="{r(x["start"])}" data-e="{r(x["end"])}"><span class="cw-t">{clean(x["text"])}</span><span class="cw-u"></span></span> ' for x in g)
    out.append(f'      <div class="cg" id="cg-{gi}" data-s="{s}" data-e="{e}"><span class="cg-b">{spans.strip()}</span></div>')
end = max(float(o.split('data-e="')[1].split('"')[0]) for o in out)

html = f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; background: transparent; }}
    #root .cg {{ position: absolute; left: 0; top: 1190px; width: 1080px; padding: 0 70px; text-align: center;
      opacity: 0; visibility: hidden; overflow: visible; }}
    #root .cg-b {{ display: inline-block; padding: 4px 14px 10px; border-radius: 12px; background: rgba(12,12,12,0.58); }}
    #root .cw {{ position: relative; display: inline-block; margin: 0 12px; font-family: "Montserrat", sans-serif; font-weight: 800; font-size: 68px;
      line-height: 1.15; color: #ffffff; letter-spacing: 0.005em;
      text-shadow: 2px 2px 0 rgba(0,0,0,0.85), -2px 2px 0 rgba(0,0,0,0.85), 2px -2px 0 rgba(0,0,0,0.85), -2px -2px 0 rgba(0,0,0,0.85),
        0 6px 22px rgba(0,0,0,0.75); }}
    #root .cw-u {{ position: absolute; left: 4px; right: 4px; bottom: 2px; height: 7px; border-radius: 4px; background: #ff3b30;
      transform-origin: 0% 50%; box-shadow: 0 2px 8px rgba(0,0,0,0.5); }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
    <div id="cap-layer">
{chr(10).join(out)}
    </div>
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
      document.querySelectorAll("#cap-layer .cg").forEach((grp) => {{
        const s = parseFloat(grp.dataset.s);
        const e = parseFloat(grp.dataset.e);
        tl.set(grp, {{ visibility: "visible" }}, s);
        tl.fromTo(grp, {{ opacity: 0, y: 18, filter: "blur(6px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.16, ease: "power3.out" }}, s);
        grp.querySelectorAll(".cw").forEach((w) => {{
          const ws = parseFloat(w.dataset.s);
          const we = Math.min(parseFloat(w.dataset.e), e - 0.1);
          const u = w.querySelector(".cw-u");
          tl.fromTo(u, {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.14, ease: "power2.out" }}, ws);
          if (w.classList.contains("acc")) tl.fromTo(w, {{ color: "#ffffff" }}, {{ color: "#ffe14d", duration: 0.1 }}, ws);
          tl.to(u, {{ scaleX: 0, transformOrigin: "100% 50%", duration: 0.12, ease: "power2.in" }}, Math.max(we, ws + 0.16));
        }});
        tl.to(grp, {{ opacity: 0, duration: 0.08, ease: "power2.in" }}, e - 0.08);
        tl.set(grp, {{ opacity: 0, visibility: "hidden" }}, e);
      }});
      window.__timelines["captions"] = tl;
    }})();
  </script>
</template>
"""
open(os.path.join(ROOT, "compositions/captions.html"), "w", encoding="utf8", newline="\n").write(html)
print(len(groups), "groups, last ends", end)
