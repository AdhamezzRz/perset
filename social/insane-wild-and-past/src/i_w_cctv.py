from reel import *
from plate_tool import paste
import json, math
OUT=os.path.abspath('../ins/out'); S=os.path.abspath('../ins/seg'); os.makedirs(S,exist_ok=True)
base=np.array(Image.open('../ins/gen/cctv.png').convert('RGB'))
ell=((1310.0,883.0),(334.0,220.0),0.0)
def ir(img):
    g=cv2.cvtColor(img.astype(np.uint8),cv2.COLOR_RGB2GRAY).astype(np.float32)
    g=cv2.GaussianBlur(g,(0,0),0.9); g=(g-g.mean())*0.9+g.mean()*1.05
    return np.clip(g,0,255)
full=ir(paste(base,ell,'wild',grade=0.0,grain=False))
empty=ir(paste(base,ell,'wild_empty',grade=0.0,grain=False))
# paw prints in the flour, from the plate towards the window
def paw(img,x,y,ang,s=1.0):
    o=img.copy()
    c,sn=math.cos(ang),math.sin(ang)
    def P(dx,dy): return (int(x+(dx*c-dy*sn)*s),int(y+(dx*sn+dy*c)*s))
    cv2.ellipse(o,P(0,0),(int(9*s),int(7*s)),math.degrees(ang),0,360,1.0,-1,cv2.LINE_AA)
    for dx,dy in ((-11,-9),(-4,-14),(4,-14),(11,-9)): cv2.circle(o,P(dy*-1 if False else dx,dy),int(3.6*s),1.0,-1,cv2.LINE_AA)
    return o
pts=[]; N=16
for k in range(N):
    u=k/(N-1); x=1140-640*u; y=905-230*u-60*math.sin(u*math.pi)
    nx,ny=-( -230-60*math.pi*math.cos(u*math.pi)), -640  # normal-ish
    side=1 if k%2 else -1
    ang=math.atan2(-230-60*math.pi*math.cos(u*math.pi),-640)+math.pi/2
    pts.append((x+side*14*math.cos(ang),y+side*14*math.sin(ang),ang))
def prints(n):
    m=np.zeros(base.shape[:2],np.float32)
    for (x,y,a) in pts[:n]: m=paw(m,x,y,a,1.15)
    return cv2.GaussianBlur(m,(0,0),1.0)
W_,H_=1080,1920; BH=int(1080*1520/2688); BY=640
rng=np.random.default_rng(5)
def frame_from(src,zoom=1.0,center=(1344,760),t=0,stamp='',pr=None):
    img=src.copy()
    if pr is not None: img=img*(1-0.35*pr)
    h,w=img.shape
    cw,ch=w/zoom,h/zoom; x0=int(np.clip(center[0]-cw/2,0,w-cw)); y0=int(np.clip(center[1]-ch/2,0,h-ch))
    crop=img[y0:int(y0+ch),x0:int(x0+cw)]
    small=cv2.resize(crop,(int(1080/ (1.0 if zoom==1 else 1.6)),int(BH/(1.0 if zoom==1 else 1.6))),interpolation=cv2.INTER_AREA)
    view=cv2.resize(small,(1080,BH),interpolation=cv2.INTER_LINEAR)
    view=view+rng.normal(0,9,view.shape)+rng.normal(0,3)
    view=np.clip(view,0,255).astype(np.uint8)
    v=cv2.cvtColor(view,cv2.COLOR_GRAY2RGB)
    for (txt,pos,sc) in ((stamp,(24,BH-26),0.95),('CAM 03  KITCHEN',(24,46),0.95)):
        cv2.putText(v,txt,pos,cv2.FONT_HERSHEY_SIMPLEX,sc,(0,0,0),5,cv2.LINE_AA); cv2.putText(v,txt,pos,cv2.FONT_HERSHEY_SIMPLEX,sc,(235,235,235),2,cv2.LINE_AA)
    if int(t*2)%2==0: cv2.circle(v,(1030,36),11,(220,30,30),-1,cv2.LINE_AA); cv2.putText(v,'REC',(950,47),cv2.FONT_HERSHEY_SIMPLEX,0.9,(235,235,235),2,cv2.LINE_AA)
    if zoom>1: cv2.putText(v,f'ZOOM x{zoom:.1f}',(860,BH-26),cv2.FONT_HERSHEY_SIMPLEX,0.9,(235,235,235),2,cv2.LINE_AA)
    out=np.zeros((H_,W_,3),np.uint8); out[BY:BY+BH]=v
    return out
segs=[]
def seg(name,dur,fn):
    p=enc(f'{S}/{name}.mp4'); n=int(dur*FPS); last=None
    for i in range(n):
        if i%3==0 or last is None: last=fn(i/FPS)   # 10 fps security-camera stutter
        p.stdin.write(last.tobytes())
    p.stdin.close(); p.wait(); segs.append(f'{S}/{name}.mp4')
def ts(h,m,s): return f'2026-11-21  {h:02d}:{m:02d}:{s:02d}'
seg('c1',3.0,lambda t: frame_from(full,1.0,t=t,stamp=ts(23,58,12+int(t))))
seg('c2',3.2,lambda t: frame_from(empty,1.0+1.6*ease(min(1,t/1.2)),center=(1310,883),t=t,stamp=ts(3,14,7+int(t))))
seg('c3',3.4,lambda t: frame_from(empty,1.0,t=t,stamp=ts(3,14,11+int(t*3)),pr=prints(int(min(N,t/2.6*N)))))
seg('c4',3.4,lambda t: frame_from(full,1.0+1.2*ease(min(1,max(0,t-1.0)/1.2)),center=(1250,860),t=t,stamp=ts(6,58,40+int(t)),pr=prints(N)))
d=os.path.abspath('../ins/cap_cctv')
top=caption('top','<div class="scr" style="top:250px;font-size:104px">we checked the<br>kitchen camera.</div>',d)
c1=caption('c1',chip('11:58 pm. all normal.',1350),d)
c2=caption('c2',chip('3:14 am. wait.',1350),d)
c3=caption('c3',chip('…who left those?',1350),d)
c4=caption('c4',chip('6:58 am. back. acting normal.',1350),d)
end=caption('end','<div class="scr" style="top:1480px;font-size:84px">they always come home<br>for dinner.</div><div class="sm" style="top:1700px;font-size:22px">stitches of the wild · a set for six · perset.shop</div>',d)
caps=[(top,0.1,13.0),(c1,0.2,3.0),(c2,3.1,6.2),(c3,6.3,9.6),(c4,9.7,11.4),(end,11.4,13.0)]
compose(segs,caps,os.path.abspath(f'{OUT}/wild-reel-1-cam-03.mp4'),grain=2)
