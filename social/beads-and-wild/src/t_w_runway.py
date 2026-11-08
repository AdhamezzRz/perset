import reel
from reel import *
reel.W,reel.H=1080,1350
W,H=1080,1350
bg=np.array(Image.open('../tw/runway_1080.jpg').convert('RGB')).astype(np.float32)
L=0.299*bg[...,0]+0.587*bg[...,1]+0.114*bg[...,2]
yy,xx=np.mgrid[0:H,0:W]
fg=((L<80)&(yy>980)).astype(np.float32)
fg=cv2.morphologyEx(fg,cv2.MORPH_CLOSE,np.ones((7,7),np.uint8)); fg=cv2.GaussianBlur(fg,(0,0),1.5)[...,None]
PL=np.array(Image.open(SCR+'/pack/assets/wild_hi.png').convert('RGBA')).astype(np.float32)
VX,VY=544,690; FLOOR=1085; DEND=430
rng=np.random.default_rng(7)
# flash sites: audience rows on both sides + photographer pit
sites=[(int(rng.uniform(0,330)),int(rng.uniform(560,1000))) for _ in range(40)]+[(int(rng.uniform(760,1080)),int(rng.uniform(560,1000))) for _ in range(40)]+[(int(rng.uniform(40,1040)),int(rng.uniform(1020,1250))) for _ in range(30)]
n=int(10*FPS); p=enc('../tw/seg/runway.mp4')
gy,gx=np.mgrid[-60:61,-60:61]; blob=np.exp(-(gx**2+gy**2)/(2*14**2)).astype(np.float32)
def flashes(fr,rate):
    k=rng.poisson(rate); glow=0
    for _ in range(k):
        x,y=sites[rng.integers(len(sites))]
        x0,y0=x-60,y-60; xa,ya=max(0,x0),max(0,y0); xb,yb=min(W,x0+121),min(H,y0+121)
        b=blob[ya-y0:yb-y0,xa-x0:xb-x0][...,None]*255
        fr[ya:yb,xa:xb]=fr[ya:yb,xa:xb]+b*(1.6)
        glow+=1
    return fr,glow
for i in range(n):
    t=i/FPS
    if t<6.2:
        u=t/6.2; z=13*(1-u)+1.0*u**0.9; z=max(1.0,13/(1+12*u**1.15)); walk=True
    else:
        z=1.0; walk=False
    dia=DEND/z
    bottom=VY+(FLOOR-VY)/z
    step=t*2*np.pi*1.05
    bob=(abs(np.sin(step))*dia*0.035) if walk else 0
    rot=(2.5*np.sin(step)) if walk else 6*ease(min(1,(t-6.2)/0.6))
    cx=VX+ (4*np.sin(step/2) if walk else 0)
    cy=bottom-dia/2-bob
    fr=bg.copy()
    rate=1.2 if walk else (5.0 if t<8.4 else 1.5)
    # plate
    D=max(4,int(dia))
    pr=cv2.resize(PL,(D,D),interpolation=cv2.INTER_AREA)
    M=cv2.getRotationMatrix2D((D/2,D/2),rot,1.0); pr=cv2.warpAffine(pr,M,(D,D),borderValue=(0,0,0,0))
    rgb=pr[...,:3]*np.array([1.03,0.97,0.88]); a=pr[...,3:]/255
    # reflection on the glossy runway
    ref=pr[::-1]; ra=(ref[...,3:]/255)*np.linspace(0.32,0,D)[:,None,None]
    x0=int(cx-D/2); y0=int(cy-D/2); yr=int(bottom+bob*0)  # reflection starts at floor
    def put(img,al,x,y):
        h,w=img.shape[:2]; xa,ya=max(0,x),max(0,y); xb,yb=min(W,x+w),min(H,y+h)
        if xb<=xa or yb<=ya: return
        fr[ya:yb,xa:xb]=fr[ya:yb,xa:xb]*(1-al[ya-y:yb-y,xa-x:xb-x])+img[ya-y:yb-y,xa-x:xb-x]*al[ya-y:yb-y,xa-x:xb-x]
    put(ref[...,:3]*np.array([1.0,0.95,0.86]),ra,x0,yr)
    put(rgb,a,x0,y0)
    fr,g=flashes(fr,rate)
    if g: fr[y0:y0+D,x0:x0+D]=fr[y0:y0+D,x0:x0+D]*(1+0.06*min(g,3))
    fr=fr*(1-fg)+bg*fg   # photographers stay in front
    p.stdin.write(np.clip(fr,0,255).astype(np.uint8).tobytes())
p.stdin.close(); p.wait()
d='../tw/cap_runway'
c1=caption('c1','<div class="sm" style="top:70px;font-size:24px">cairo fashion week · ss27</div>',d)
c2=caption('c2','<div class="scr" style="top:150px;font-size:120px">the leopards walk.</div>',d)
c3=caption('c3','<div class="sm" style="top:1270px;font-size:20px">stitches of the wild · a set for six · perset.shop</div>',d)
compose([os.path.abspath('../tw/seg/runway.mp4')],[(c1,0.2,10),(c2,6.4,10),(c3,6.8,10)],os.path.abspath('../tw/out/wild-post-1-the-leopards-walk.mp4'),grain=5)
