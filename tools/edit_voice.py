import soundfile as sf, numpy as np, json
x, sr = sf.read('_work/voz-clean-full.wav'); x = x if x.ndim==1 else x.mean(1)
# referencia para detectar silencios (misma edición que la versión anterior)
import os
ref = None
if os.path.exists('_work/voz-ref-old.wav'):
    ref, _ = sf.read('_work/voz-ref-old.wav'); ref = ref if ref.ndim==1 else ref.mean(1)
# content cuts (source seconds): fillers, repetitions, unclear phrase
cuts = [(0.0,0.55),(25.70,26.20),(49.40,50.20),(72.92,73.31),(82.70,len(x)/sr)]
XF = int(0.015*sr)
keep=[];t=0.0
for a,b in sorted(cuts):
    if a>t: keep.append((t,a))
    t=max(t,b)
if t<len(x)/sr: keep.append((t,len(x)/sr))
def splice(parts):
    out=parts[0].copy()
    for p in parts[1:]:
        n=min(XF,len(out),len(p)); f=np.linspace(0,1,n)
        out[-n:]=out[-n:]*(1-f)+p[:n]*f
        out=np.concatenate([out,p[n:]])
    return out
segmap=[]  # (src_start, src_end) in order
y=splice([x[int(a*sr):int(b*sr)] for a,b in keep]); segmap=keep
yr=splice([ref[int(a*sr):int(b*sr)] for a,b in keep]) if ref is not None else y
# gap compression on edited audio
hop=int(sr*0.01); n=len(y)//hop
db=np.array([20*np.log10(np.sqrt(np.mean(yr[i*hop:(i+1)*hop]**2))+1e-9) for i in range(n)])
floor=np.percentile(db,8); thr=floor+11
on=db>thr
# silence runs
runs=[];s=None
for i,v in enumerate(on):
    if not v and s is None: s=i
    if v and s is not None: runs.append((s,i)); s=None
pad=0.07
pieces=[];last=0
for s,e in runs:
    g=(e-s)/100
    if s==0: continue
    if g<0.22: continue
    new=min(0.32, 0.15+0.3*(g-0.15))
    rm=g-new
    a=s/100+(new/2); b=a+rm
    if a<pad+s/100-0.001: a=s/100+min(pad,new/2)
    pieces.append((last,a)); last=b
pieces.append((last,len(y)/sr))
z=splice([y[int(a*sr):int(b*sr)] for a,b in pieces])
# fade in/out
fi=int(0.02*sr); z[:fi]*=np.linspace(0,1,fi); fo=int(0.25*sr); z[-fo:]*=np.linspace(1,0,fo)
sf.write('_work/voz-edit.wav', z, sr, subtype='PCM_24')
print('src %.2f -> cut %.2f -> final %.2f s, gaps compressed: %d'%(len(x)/sr,len(y)/sr,len(z)/sr,len(pieces)-1))
