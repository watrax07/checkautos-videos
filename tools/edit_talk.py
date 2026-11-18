# Edición de cabeza parlante: mismos cortes para video y audio, alineados a fotograma (30 fps).
# Entrada: _work/voz-clean-full.wav (audio limpio, mismo tiempo que el video fuente) y el video fuente.
# Salida: assets/media/talk-edit.mp4 (video mudo), _work/voz-edit.wav, _work/segments.json
import json, subprocess, sys
import numpy as np, soundfile as sf

SRC = sys.argv[1]
FPS = 30
HEAD, TAIL = 0.80, 47.30                 # desde justo antes de "Mitos" hasta después de "Check Autos"
CUTS = [(34.15, 34.83)]                  # "¿sí?" de muletilla

x, sr = sf.read('_work/voz-clean-full.wav'); x = x if x.ndim == 1 else x.mean(1)
q = lambda t: round(t * FPS) / FPS

# 1) tramos a conservar (fuente)
keep, t = [], HEAD
for a, b in sorted(CUTS):
    if a > t: keep.append([t, a])
    t = max(t, b)
keep.append([t, TAIL])

# 2) acortar silencios largos dentro de cada tramo
hop = int(sr * 0.01)
def silences(a, b):
    seg = x[int(a * sr):int(b * sr)]
    n = len(seg) // hop
    db = np.array([20 * np.log10(np.sqrt(np.mean(seg[i*hop:(i+1)*hop] ** 2)) + 1e-9) for i in range(n)])
    return db
full_db = silences(0, len(x) / sr)
thr = np.percentile(full_db, 8) + 12
pieces = []
for a, b in keep:
    i0, i1 = int(a * 100), int(b * 100)
    on = full_db[i0:i1] > thr
    cur = a; s = None
    for k, v in enumerate(on):
        tk = a + k / 100
        if not v and s is None: s = tk
        if v and s is not None:
            g = tk - s
            if g >= 0.22 and s > a + 0.05:
                new = min(0.22, 0.10 + 0.25 * (g - 0.15))
                ca, cb = s + new / 2, tk - new / 2
                pieces.append([cur, ca]); cur = cb
            s = None
    pieces.append([cur, b])

# 3) alinear a fotograma y descartar trozos diminutos
segs = []
for a, b in pieces:
    a, b = q(a), q(b)
    if b - a >= 3 / FPS:
        segs.append([a, b])

# 4) audio: concatenar con fundidos de 6 ms en cada corte (sin solapar: mismo largo que el video)
fd = int(0.006 * sr)
parts = []
for a, b in segs:
    p = x[int(round(a * sr)):int(round(b * sr))].copy()
    p[:fd] *= np.linspace(0, 1, fd); p[-fd:] *= np.linspace(1, 0, fd)
    parts.append(p)
y = np.concatenate(parts)
sf.write('_work/voz-edit.wav', y, sr, subtype='FLOAT')

# 5) video: trim + concat con los mismos tramos
fc = []
for i, (a, b) in enumerate(segs):
    fc.append(f'[0:v]trim=start_frame={round(a * FPS)}:end_frame={round(b * FPS)},setpts=PTS-STARTPTS[v{i}]')
fc.append(''.join(f'[v{i}]' for i in range(len(segs))) + f'concat=n={len(segs)}:v=1:a=0[cat]')
fc.append('[cat]scale=1080:1920:flags=lanczos,eq=contrast=1.05:saturation=1.08,setsar=1[out]')
open('_work/talk-filter.txt', 'w').write(';\n'.join(fc))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', '_work/talk-cfr.mp4', '-filter_complex_script', '_work/talk-filter.txt',
                '-map', '[out]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', '-r', str(FPS),
                '-g', '15', '-an', '-movflags', '+faststart', 'assets/media/talk-edit.mp4'], check=True)

# 6) mapa fuente -> salida
out, o = [], 0.0
for a, b in segs:
    out.append({'src_a': a, 'src_b': b, 'out_a': round(o, 4)}); o += b - a
json.dump({'segments': out, 'duration': round(o, 4)}, open('_work/segments.json', 'w'), indent=1)
print(f'{len(segs)} tramos, {TAIL - HEAD:.2f} s -> {o:.2f} s (audio {len(y) / sr:.2f} s)')
