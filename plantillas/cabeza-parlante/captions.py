# Subtítulos del video 6 desde la transcripción original proyectada sobre los cortes (_work/mapwords.py).
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from mapwords import mapped

ROOT = os.path.join(os.path.dirname(__file__), "..")
LAST = 145  # "inversión." — el cierre dice "Somos Check Autos"
words = [w for w in mapped() if 3 <= w["i"] <= LAST]  # "Mitos contra realidad" ya está en el título
fix = {12: "CVT,"}
drop = {13, 131}
for w in words:
    if w["i"] in fix: w["text"] = fix[w["i"]]
cvt = next(w for w in words if w["i"] == 12); nxt = next(w for w in words if w["i"] == 13); cvt["end"] = nxt["end"]
words = [w for w in words if w["i"] not in drop]

accent = {"mitos", "realidad", "cvt", "mantenimiento", "fluido", "mal", "manual", "fabricante", "fluidos", "filtro", "80", "100",
          "marca", "año", "tapón", "drenar", "rellenar", "máquinas", "talleres", "equipos", "cuidado", "momento", "máquina", "inversión"}
groups, cur = [], []
for x in words:
    if cur:
        prev = cur[-1]
        if len(cur) >= 3 or prev["text"][-1] in ".,?!" or x["start"] - prev["end"] >= 0.15 or len("".join(c["text"] for c in cur)) > 14:
            groups.append(cur); cur = []
    cur.append(x)
groups.append(cur)
clean = lambda t: t.strip(".,¿?!")
out = []
for gi, g in enumerate(groups):
    s = round(max(0.05, g[0]["start"] - 0.03), 3)
    nx = round(groups[gi + 1][0]["start"] - 0.03, 3) if gi + 1 < len(groups) else 999
    e = round(min(nx, g[-1]["end"] + 0.25), 3)
    spans = " ".join(f'<span class="cw{" acc" if clean(x["text"]).lower() in accent else ""}" data-s="{x["start"]}" data-e="{x["end"]}">{clean(x["text"])}</span>' for x in g)
    out.append(f'      <div class="cg" id="cg-{gi}" data-s="{s}" data-e="{e}">{spans}</div>')
html = f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; background: transparent; }}
    #root .cg {{ position: absolute; left: 0; top: 1195px; width: 1080px; padding: 0 70px; text-align: center; opacity: 0; visibility: hidden; }}
    #root .cw {{ display: inline-block; margin: 0 10px; font-family: "Nunito", sans-serif; font-weight: 900; font-size: 72px; line-height: 1.1;
      color: #ffffff; text-shadow: 4px 4px 0 #0f172a, -4px 4px 0 #0f172a, 4px -4px 0 #0f172a, -4px -4px 0 #0f172a, 0 4px 0 #0f172a,
      0 -4px 0 #0f172a, 4px 0 0 #0f172a, -4px 0 0 #0f172a, 0 10px 24px rgba(0,0,0,0.6); }}
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
        const s = parseFloat(grp.dataset.s), e = parseFloat(grp.dataset.e);
        tl.set(grp, {{ visibility: "visible" }}, s);
        tl.fromTo(grp, {{ opacity: 0, y: 16, scale: 0.92 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.14, ease: "back.out(2.2)" }}, s);
        grp.querySelectorAll(".cw").forEach((w) => {{
          const ws = parseFloat(w.dataset.s), we = Math.min(parseFloat(w.dataset.e), e - 0.1);
          const acc = w.classList.contains("acc");
          tl.fromTo(w, {{ color: "#ffffff", scale: 1 }}, {{ color: acc ? "#facc15" : "#e2f2ff", scale: acc ? 1.1 : 1.03, duration: 0.08, ease: "power2.out" }}, ws);
          tl.to(w, {{ color: acc ? "#facc15" : "#ffffff", scale: 1, duration: 0.1, ease: "power2.in" }}, Math.max(we, ws + 0.12));
        }});
        tl.to(grp, {{ opacity: 0, duration: 0.08 }}, e - 0.08);
        tl.set(grp, {{ opacity: 0, visibility: "hidden" }}, e);
      }});
      window.__timelines["captions"] = tl;
    }})();
  </script>
</template>
"""
open(os.path.join(ROOT, "compositions/captions.html"), "w", encoding="utf8", newline="\n").write(html)
print(len(groups), "groups; last ends", max(g[-1]["end"] for g in groups))
