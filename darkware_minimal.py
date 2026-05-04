"""DarkWare Engine — Minimal. Zero dependencies."""
import math

M = 0.9317

class R:
    def __init__(s, seed):
        s.a = seed & 0xFFFFFFFF
    def n(s):
        s.a = (s.a + 0x6D2B79F5) & 0xFFFFFFFF
        t = (s.a ^ (s.a >> 15)) & 0xFFFFFFFF
        t = (t * (1 | s.a)) & 0xFFFFFFFF
        t = (t + ((t ^ (t >> 7)) * (61 | t) & 0xFFFFFFFF)) & 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296.0

class BC:
    def __init__(s, L, seed=42):
        s.L=L; s.N=L*L; s.r=R(seed); s.s=[1]*s.N; s.nb=[]
        for i in range(s.N):
            ro,co=i//L,i%L; nb=[]
            for dr in(-1,0,1):
                for dc in(-1,0,1):
                    if dr==0 and dc==0: continue
                    nb.append(((ro+dr)%L)*L+((co+dc)%L))
            s.nb.append(nb)
    def eq(s, sw=15):
        for _ in range(sw):
            for i in range(s.N):
                o=s.s[i]; n=[-1,0,1][int(s.r.n()*3)]
                if n==o: continue
                dE=2.0*((1-n*n)-(1-o*o))
                for j in s.nb[i]: dE-=(n-o)*s.s[j]
                if dE<=0 or s.r.n()<math.exp(-dE/2.70): s.s[i]=n
    def clone(s):
        c=BC(s.L,int(s.r.n()*1e9)); c.s=list(s.s); c.nb=s.nb; return c

def encode(vals, zone):
    t=[]; nv=max(len(vals),1)
    for vi,v in enumerate(vals):
        f=M*(0.5+v*3); ph=vi*6.283/nv; pf=max(1,zone//nv)
        for i in range(pf):
            w=math.sin(6.283*f*i/pf+ph)
            t.append(1 if w>0.33 else(-1 if w<-0.33 else 0))
    return t[:zone]

def classify(features, classes, L=10, seeds=(42,137,256,500,777)):
    zone=L*L//5; labels=list(classes.keys())
    vals=list(classes.values()); nf=len(vals[0])
    mn=[min(v[i] for v in vals) for i in range(nf)]
    mx=[max(v[i] for v in vals) for i in range(nf)]
    norm=lambda v:[(v[i]-mn[i])/max(mx[i]-mn[i],1e-10) for i in range(nf)]
    cent={l:[] for l in labels}
    for sd in seeds:
        lat=BC(L,sd); lat.eq()
        gnd=[lat.s[i] for i in range(zone)]
        for l in labels:
            c=lat.clone(); tr=encode(norm(classes[l]),zone)
            for i in range(min(len(tr),zone)): c.s[i]=tr[i]
            cent[l].append([c.s[i]-gnd[i] for i in range(zone)])
    cm={l:[sum(s[i] for s in cent[l])/len(cent[l]) for i in range(zone)] for l in labels}
    cs={l:[(sum((s[i]-cm[l][i])**2 for s in cent[l])/len(cent[l]))**0.5+.001 for i in range(zone)] for l in labels}
    nv=norm(features); tr=encode(nv,zone); scores={}
    for sd in seeds:
        lat=BC(L,sd); lat.eq()
        gnd=[lat.s[i] for i in range(zone)]
        c=lat.clone()
        for i in range(min(len(tr),zone)): c.s[i]=tr[i]
        sig=[c.s[i]-gnd[i] for i in range(zone)]
        for l in labels:
            d=sum(((sig[i]-cm[l][i])/cs[l][i])**2 for i in range(zone))**0.5
            scores[l]=scores.get(l,0)+1/(1+d)
    best=max(scores,key=scores.get); total=sum(scores.values())
    return best, int(scores[best]/total*100)

# ═══ TEST ═══
if __name__=='__main__':
    classes={
        'Normal':[0.12,0.34,2.8,3.1,120],
        'Misalign':[0.45,0.89,1.9,4.2,60],
        'Imbalance':[0.67,1.23,1.8,3.0,45],
        'BearFault':[0.23,0.95,4.1,8.5,340],
        'Looseness':[0.34,0.78,2.3,5.7,90],
    }
    for name,feats in classes.items():
        cls,conf=classify(feats,classes)
        print(f"  {name:>12s} -> {cls:>12s} {conf}% {'OK' if cls==name else 'MISS'}")
    # Noisy test
    cls,conf=classify([0.13,0.32,2.9,3.0,118],classes)
    print(f"  {'Noisy norm':>12s} -> {cls:>12s} {conf}%")
    # Iris
    iris={'Setosa':[0.22,0.63,0.07,0.04],'Versicolor':[0.57,0.47,0.56,0.42],'Virginica':[0.64,0.45,0.79,0.70]}
    for name,feats in iris.items():
        cls,conf=classify(feats,iris)
        print(f"  {name:>12s} -> {cls:>12s} {conf}% {'OK' if cls==name else 'MISS'}")
