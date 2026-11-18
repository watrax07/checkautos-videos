import soundfile as sf, numpy as np, sys
x, sr = sf.read(sys.argv[1]); x = x if x.ndim==1 else x.mean(1)
for arg in sys.argv[2:]:
    a,b=map(float,arg.split(':'))
    out=[]
    t=a
    while t<b:
        s=x[int(t*sr):int((t+0.02)*sr)]
        out.append("%.2f:%d"%(t,20*np.log10(np.sqrt(np.mean(s**2))+1e-9)))
        t+=0.02
    print(arg,' '.join(out)); print()
