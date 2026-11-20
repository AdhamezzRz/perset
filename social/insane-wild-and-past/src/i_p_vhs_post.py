"""VHS look on the rendered frames: soft luma, smeared + offset chroma, scanlines, line jitter,
tracking bands at the start and at the 'tape glitch' before the clean 2026 ending."""
from reel import *
import glob
d=os.path.abspath('../ins/vhs'); fs=sorted(glob.glob(f'{d}/fr/f*.jpg'))
rng=np.random.default_rng(7)
def vhs(fr,t,amt,band):
    f=fr.astype(np.float32)
    ycc=cv2.cvtColor(fr,cv2.COLOR_RGB2YCrCb).astype(np.float32)
    Y=ycc[...,0]
    # luma: ~330 lines horizontal resolution
    Ys=cv2.resize(cv2.resize(Y,(420,960),interpolation=cv2.INTER_AREA),(W,H),interpolation=cv2.INTER_CUBIC)
    Y=Y*(1-amt)+Ys*amt
    Y=Y+ (Y-cv2.GaussianBlur(Y,(0,0),3))*0.6*amt   # VCR sharpening halo
    # chroma: very low bandwidth, shifted right
    C=ycc[...,1:]
    Cs=cv2.resize(cv2.resize(C,(90,480),interpolation=cv2.INTER_AREA),(W,H),interpolation=cv2.INTER_LINEAR)
    Cs=np.roll(Cs,int(10*amt),axis=1)
    C=C*(1-amt)+Cs*amt
    C=(C-128)*(1+0.18*amt)+128
    out=cv2.cvtColor(np.clip(np.dstack([Y,C]),0,255).astype(np.uint8),cv2.COLOR_YCrCb2RGB).astype(np.float32)
    # lifted blacks, warm
    out=out*(1-0.08*amt)+np.float32([20,14,18])*amt
    # line jitter
    if amt>0:
        sh=(rng.normal(0,1.2,H)*amt).astype(np.float32)
        if band>0:
            y0=int((1-((t*1.7)%1))*H)
            yy=np.arange(H); w=np.exp(-((yy-y0)/(90))**2)*band
            sh+= (w*rng.normal(0,25,H)).astype(np.float32)
        # head-switching at bottom
        sh[-28:]+=np.linspace(0,30,28)*amt
        mx=np.tile(np.arange(W,dtype=np.float32),(H,1))-sh[:,None]; my=np.tile(np.arange(H,dtype=np.float32)[:,None],(1,W))
        out=cv2.remap(out,mx,my,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
        if band>0:
            n=rng.random((H,W)).astype(np.float32); y0=int((1-((t*1.7)%1))*H)
            m=np.zeros((H,1),np.float32); m[max(0,y0-60):y0+60]=1; m=cv2.GaussianBlur(m,(0,0),20)*band
            out=out*(1-0.6*m[...,None])+ (n[...,None]>0.6)*255*0.6*m[...,None]
        # scanlines + noise
        out[::2]*=1-0.07*amt
        out+=rng.normal(0,5*amt,(H,W,1)).astype(np.float32)
    return np.clip(out,0,255).astype(np.uint8)
p=enc(os.path.abspath('../ins/seg/vhs_full.mp4'))
for i,f in enumerate(fs):
    t=i/FPS
    fr=np.array(Image.open(f).convert('RGB'))
    if t<12.2: amt=1.0
    elif t<12.8: amt=1.0
    else: amt=0.0
    band=max(0,1-t/1.0)*1.0 + (1.0 if 12.2<=t<12.8 else 0) + (0.35 if 6.35<t<6.55 or 10.95<t<11.1 else 0)
    if 12.2<=t<12.8:
        # glitch: roll + freeze stutter
        fr=np.roll(fr,int(rng.integers(-300,300)),axis=0) if rng.random()<0.5 else fr
    o=vhs(fr,t,amt,min(band,1.2))
    if 12.75<t<12.85: o=(o*0.2).astype(np.uint8)
    p.stdin.write(o.tobytes())
p.stdin.close(); p.wait()
run(f'{FF} -v error -y -i "{os.path.abspath("../ins/seg/vhs_full.mp4")}" -vf "noise=alls=3:allf=t,format=yuv420p" -c:v libx264 -crf 18 -preset slow -movflags +faststart "{os.path.abspath("../ins/out/past-reel-1-as-seen-on-tv-1987.mp4")}"')
print('ok')
