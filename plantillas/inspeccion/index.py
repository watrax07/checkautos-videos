# Writes index.html (scenes, captions, voice, music, sfx) for video 4.
import os, json

ROOT = os.path.join(os.path.dirname(__file__), "..")
TOTAL = 80.5
SCENES = [("gancho", 0, 5.15), ("pintura", 5.15, 13.8), ("tablero", 13.8, 17.2), ("maletero", 17.2, 23.3), ("ramal", 23.3, 33.2),
          ("computadora", 33.2, 41.9), ("armado", 41.9, 51.2), ("culata", 51.2, 55.3), ("agua", 55.3, 57.9), ("radiador", 57.9, 62.0),
          ("aceite", 62.0, 69.7), ("veredicto", 69.7, 72.1), ("consejo", 72.1, 75.95), ("cierre", 75.95, TOTAL)]
DUR = {"chime": 2.5, "click": 0.37, "click-soft": 0.37, "error": 1.62, "glitch-1": 2.64, "impact-bass-1": 2.12, "impact-bass-2": 2.59,
       "key-press": 0.4, "ping": 1.32, "pop": 0.72, "sparkle": 1.8, "typing": 1.5, "whoosh": 0.57, "whoosh-short": 0.57}
HITS = [7.5, 9.0, 11.0, 15.45, 21.1, 21.7, 27.2, 31.1, 35.85, 40.5, 47.7, 49.95, 54.6, 55.9, 59.2, 64.95]
SFX = [("s-open", "impact-bass-2", -0.5, 0.3), ("s-km", "whoosh", 1.9, 0.2), ("s-q", "pop", 2.6, 0.16), ("s-vw", "whoosh-short", 4.04, 0.16),
       ("s-pin", "whoosh", 4.99, 0.18), ("s-mal", "whoosh-short", 7.84, 0.15), ("s-pes", "impact-bass-1", 9.08, 0.22),
       ("s-meter", "whoosh", 10.19, 0.18), ("s-gfx", "whoosh-short", 11.69, 0.15),
       ("s-tab", "whoosh", 13.64, 0.18), ("s-tot", "impact-bass-1", 15.83, 0.2),
       ("s-mlt", "whoosh", 17.04, 0.18), ("s-def", "impact-bass-1", 21.78, 0.22),
       ("s-ram", "whoosh", 23.14, 0.18), ("s-cut", "glitch-1", 26.24, 0.16), ("s-fren", "whoosh-short", 28.24, 0.15),
       ("s-ecu", "whoosh", 33.04, 0.18), ("s-ecu2", "whoosh-short", 37.49, 0.15), ("s-neq", "error", 39.6, 0.14),
       ("s-arm", "whoosh", 41.74, 0.18), ("s-armado", "impact-bass-2", 43.66, 0.3),
       ("s-cul", "whoosh", 51.04, 0.18), ("s-x", "impact-bass-1", 54.05, 0.2), ("s-agua", "whoosh-short", 55.14, 0.15),
       ("s-rad", "whoosh", 57.74, 0.18), ("s-ace", "whoosh", 61.84, 0.18), ("s-ace2", "whoosh-short", 66.04, 0.12),
       ("s-16", "impact-bass-2", 68.9, 0.3), ("s-cons", "whoosh", 71.94, 0.18), ("s-fin", "sparkle", 76.0, 0.15), ("s-tel", "pop", 76.84, 0.18)]
SFX = [x for x in SFX if x[2] >= 0] + [("s-open", "impact-bass-1", 0.0, 0.25)]
# un trazo de marcador en cada falla del medidor
SFX += [(f"s-h{i}", "key-press", round(t - 0.07, 2), 0.18) for i, t in enumerate(HITS)]

lines = []
for cid, a, b in SCENES:
    lines.append(f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{a}" '
                 f'data-duration="{round(b - a, 3)}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 1"></div>')

lines.append('      <div id="hud" data-composition-id="hud" data-composition-src="compositions/hud.html" data-start="5.15" data-duration="64.55" '
             'data-track-index="3" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 4"></div>')

# pistas de efectos sin solaparse
tracks = {}
sfx_lines = []
for sid, f, t, v in sorted(SFX, key=lambda x: x[2]):
    d = DUR[f]
    tr = next(k for k in range(10, 30) if tracks.get(k, -1) <= t)
    tracks[tr] = t + d
    fade = ' data-fade-out="0.4"' if f in ("whoosh-cinematic", "glitch-2", "glitch-3") else ""
    sfx_lines.append(f'      <audio id="{sid}" src="assets/sfx/{f}.mp3" data-start="{t}" data-duration="{d}" data-track-index="{tr}" data-volume="{v}"{fade}></audio>')

auto = {"version": 1, "lanes": [{"target": "volume", "points": [
    {"t": 0, "v": 0.2}, {"t": 0.2, "v": 0.2}, {"t": 0.45, "v": 0.045}, {"t": 75.9, "v": 0.045}, {"t": 76.4, "v": 0.26}, {"t": TOTAL, "v": 0.02}]}]}
auto_s = json.dumps(auto, separators=(",", ":")).replace('"', "&quot;")

html = f"""<!doctype html>
<html lang="es" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #121212; }}
      body {{ font-family: "Inter", sans-serif; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <!-- Escenas -->
{chr(10).join(lines)}

      <!-- Subtítulos -->
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="75.8" data-track-index="2" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index: 5"></div>

      <!-- Voz limpia (picos saturados reconstruidos; sin los "eh" ni silencios largos) -->
      <audio id="voz" src="assets/voz-limpia.wav" data-start="0.3" data-duration="75.65" data-track-index="3" data-volume="1"></audio>

      <!-- Música: "The Corporate Upbeat" de Soundrider/Dope (Jamendo, CC BY 3.0) -->
      <audio id="musica" src="assets/music/the-corporate-upbeat.mp3" data-start="0" data-duration="{TOTAL}" data-media-start="20.0" data-track-index="4" data-volume="1" data-fade-out="2.5" data-automation="{auto_s}"></audio>

      <!-- Efectos (Pixabay Content License) -->
{chr(10).join(sfx_lines)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
open(os.path.join(ROOT, "index.html"), "w", encoding="utf8", newline="\n").write(html)
print("index written,", len(SFX), "sfx on", len(tracks), "tracks")
