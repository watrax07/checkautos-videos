import soundfile as sf, numpy as np, json, sys
x, sr = sf.read(sys.argv[1]); 
if x.ndim>1: x=x.mean(1)
hop=int(sr*0.01); n=len(x)//hop
rms=np.array([np.sqrt(np.mean(x[i*hop:(i+1)*hop]**2)) for i in range(n)])
db=20*np.log10(rms+1e-9)
floor=np.percentile(db,10); print("floor dB %.1f  p50 %.1f p90 %.1f"%(floor,np.percentile(db,50),np.percentile(db,90)))
thr=floor+12
on=db>thr
# segments with min gap merge 0.08
segs=[];s=None
for i,v in enumerate(on):
    if v and s is None: s=i
    if not v and s is not None: segs.append([s,i]); s=None
if s is not None: segs.append([s,n])
m=[]
for a,b in segs:
    if m and a-m[-1][1]<8: m[-1][1]=b
    else: m.append([a,b])
m=[[a/100,b/100] for a,b in m if b-a>=4]
w=json.load(open(sys.argv[2],encoding='utf8'))
for a,b in m:
    ws=[x['text'] for x in w if x['start']<b and x['end']>a]
    print("%6.2f-%6.2f (%.2f) %s"%(a,b,b-a,' '.join(ws)))
