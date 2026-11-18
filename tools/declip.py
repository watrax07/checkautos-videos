# Reconstruye picos recortados con interpolación cúbica (spline) entre muestras no recortadas.
import soundfile as sf, numpy as np, sys
from scipy.interpolate import CubicSpline
x, sr = sf.read(sys.argv[1]); x = x.astype(np.float64)
thr = 0.95
clip = np.abs(x) >= thr
y = x.copy()
i, n, fixed = 0, len(x), 0
while i < n:
    if clip[i]:
        j = i
        while j < n and clip[j]: j += 1
        a, b = max(0, i - 6), min(n, j + 6)
        keep = np.r_[a:i, j:b]
        if len(keep) >= 4:
            cs = CubicSpline(keep, x[keep])
            seg = cs(np.arange(i, j))
            s = np.sign(x[i:j])
            seg = s * np.clip(np.abs(seg), np.abs(x[i:j]), 1.6)   # nunca por debajo del recorte ni por encima de 1.6
            y[i:j] = seg; fixed += 1
        i = j
    else:
        i += 1
sf.write(sys.argv[2], y, sr, subtype='FLOAT')
print('runs fixed', fixed, 'new peak', np.abs(y).max().round(3))
