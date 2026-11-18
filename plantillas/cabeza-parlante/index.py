# Writes index.html (scenes, captions, voice, music, sfx) for video 4.
import os, json

ROOT = os.path.join(os.path.dirname(__file__), "..")
TOTAL = 46.0
LAYERS = [("talk", 0, 42.466, 1, "graphics"), ("broll", 0, 42.466, 2, "graphics"), ("cards", 0, 41.2, 3, "graphics"),
          ("cierre", 41.2, TOTAL, 6, "graphics")]
DUR = {"chime": 2.5, "click": 0.37, "click-soft": 0.37, "error": 1.62, "impact-bass-1": 2.12, "ping": 1.32, "pop": 0.72, "sparkle": 1.8,
       "whoosh": 0.57, "whoosh-short": 0.57}
SFX = [
    ("s-open", "whoosh", 0.0, 0.2), ("s-real0", "pop", 0.85, 0.2),
    ("s-m1", "error", 1.47, 0.12), ("s-br1", "whoosh", 2.94, 0.2), ("s-m2", "error", 4.87, 0.12), ("s-br2", "whoosh-short", 6.24, 0.18),
    ("s-r1", "chime", 8.34, 0.18), ("s-page", "whoosh-short", 9.74, 0.12),
    ("s-c1", "pop", 12.59, 0.16), ("s-c2", "pop", 14.14, 0.16), ("s-c3", "pop", 14.79, 0.16),
    ("s-br3", "whoosh", 15.14, 0.2), ("s-odo", "pop", 15.44, 0.18), ("s-100", "ping", 16.73, 0.15),
    ("s-r2", "chime", 19.09, 0.15), ("s-br4", "whoosh-short", 23.74, 0.18), ("s-m3", "error", 23.57, 0.12),
    ("s-tank", "pop", 26.99, 0.18), ("s-drain", "whoosh-short", 27.44, 0.12), ("s-fill", "whoosh-short", 28.39, 0.12),
    ("s-mach", "pop", 29.09, 0.18), ("s-br5", "whoosh", 31.24, 0.2), ("s-r3", "chime", 31.99, 0.15),
    ("s-c4", "pop", 36.09, 0.16), ("s-c5", "pop", 37.79, 0.16),
    ("s-br6", "whoosh", 38.64, 0.2), ("s-cu1", "pop", 39.14, 0.18), ("s-br7", "whoosh-short", 39.74, 0.15), ("s-cu2", "pop", 40.09, 0.18),
    ("s-fin", "whoosh", 41.04, 0.2), ("s-logo", "sparkle", 41.23, 0.18), ("s-tel", "pop", 42.19, 0.2),
]

lines = []
for cid, a, b, z, kind in LAYERS:
    lines.append(f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{a}" '
                 f'data-duration="{round(b - a, 3)}" data-track-index="{z}" data-track-kind="{kind}" data-width="1080" data-height="1920" style="z-index: {z}"></div>')

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
    {"t": 0, "v": 0.05}, {"t": 42.0, "v": 0.05}, {"t": 42.6, "v": 0.26}, {"t": TOTAL, "v": 0.02}]}]}
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
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="41.3" data-track-index="5" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index: 5"></div>

      <!-- Voz (sale del mismo video, cortada igual que talk-edit.mp4; picos saturados reconstruidos) -->
      <audio id="voz" src="assets/voz-limpia.wav" data-start="0" data-duration="42.5" data-track-index="7" data-volume="1"></audio>

      <!-- Música: "The Corporate Upbeat" de Soundrider/Dope (Jamendo, CC BY 3.0) -->
      <audio id="musica" src="assets/music/the-corporate-upbeat.mp3" data-start="0" data-duration="{TOTAL}" data-media-start="44.31" data-track-index="8" data-volume="1" data-fade-out="2.5" data-automation="{auto_s}"></audio>

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
