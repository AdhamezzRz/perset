import reel, sys
from reel import *
reel.W,reel.H=1080,1350
W,H=1080,1350
base=np.array(Image.open(SCR+'/src/beads-1-perset-beads-flatlay-hero.jpg').convert('RGB').crop((640,0,1920,1600)).resize((W,H),Image.LANCZOS)).astype(np.float32)
CX,CY=(1179.8-640)*0.84375,781.9*0.84375; RR=509*0.84375
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
which=sys.argv[1:]
if 'marquee' in which:
    N=151; ph=-0.07638328
    th=np.array([(-ph+2*np.pi*m)/N for m in range(N)])
    bx=CX+0.961*RR*np.cos(th); by=CY+0.961*RR*np.sin(th)
    night=base*np.array([0.22,0.25,0.36])
    pool=np.exp(-(((xx-CX)**2+(yy-CY)**2)/(2*(RR*1.05)**2)))[...,None]
    night=night+base*pool*np.array([0.10,0.08,0.08])
    bead=np.zeros((H,W),np.float32)
    n=int(10*FPS); p=enc('../tw/seg/marquee.mp4')
    for i in range(n):
        t=i/FPS
        ph_t=(np.arange(N)/N - t*0.2)%1.0
        b=0.18+sum(np.exp(-(np.minimum(np.abs(ph_t-k/4),1-np.abs(ph_t-k/4))/0.03)**2) for k in range(4))
        b=np.clip(b,0,1)*min(1,t/0.8)
        core=np.zeros((H,W),np.float32)
        for x,y,v in zip(bx,by,b): cv2.circle(core,(int(round(x)),int(round(y))),7,float(v),-1,cv2.LINE_AA)
        halo=cv2.GaussianBlur(core,(0,0),14); core2=cv2.GaussianBlur(core,(0,0),2.5)
        lit=base*core2[...,None]*1.9
        fr=night*(1-core2[...,None])+lit+halo[...,None]*np.array([255,150,140])*2.2
        fr=fr+cv2.GaussianBlur(halo,(0,0),34)[...,None]*np.array([255,140,120])*1.6
        p.stdin.write(np.clip(fr,0,255).astype(np.uint8).tobytes())
    p.stdin.close(); p.wait()
    d='../tw/cap_marquee'
    c1=caption('c1','<div class="scr" style="top:1035px;font-size:100px">the beads come<br>out at night.</div>',d)
    c2=caption('c2','<div class="sm" style="top:1290px;font-size:20px">a tale in beads · a set for six · perset.shop</div>',d)
    compose([os.path.abspath('../tw/seg/marquee.mp4')],[(c1,1.0,10),(c2,1.4,10)],os.path.abspath('../tw/out/beads-post-1-after-dark.mp4'),grain=6)
if 'light' in which:
    fr_=np.array(Image.open('../tw/gen/frond.png').convert('L')).astype(np.float32)/255
    gobo=1-fr_; G=gobo.shape[0]
    keys=[(0,'06:00','breakfast'),(3,'13:00','lunch'),(6,'18:30','golden hour'),(9,'23:00','still on the table')]
    grades=[np.array([0.80,0.78,0.92]),np.array([1.04,1.02,0.98]),np.array([1.10,0.86,0.62]),np.array([0.30,0.30,0.42])]
    n=int(12*FPS); p=enc('../tw/seg/light.mp4')
    for i in range(n):
        t=i/FPS; seg_=min(3,int(t//3)); u=(t-seg_*3)/3
        g0=grades[seg_]; g1=grades[min(3,seg_+1)] if u>0.7 else g0
        k=ease(np.clip((u-0.7)/0.3,0,1)); grade=g0*(1-k)+g1*k
        # sun path: shadow sweeps left->right, length and softness change
        a=t/12
        ang=-60+120*a; sc=1.9-0.7*np.sin(np.pi*a); tx=W*(0.15+0.7*a); ty=H*0.35
        M=cv2.getRotationMatrix2D((G/2,G/2),ang,sc*W/G*1.2); M[0,2]+=tx-G/2; M[1,2]+=ty-G/2
        sh=cv2.warpAffine(gobo,M,(W,H),flags=cv2.INTER_LINEAR)
        soft=6+14*abs(np.cos(np.pi*a)); sh=cv2.GaussianBlur(sh,(0,0),soft)
        strength=0.55*(1 if t<9 else max(0,1-(t-9)/0.8))
        fr=base*(1-strength*sh[...,None])*grade
        if t>8.6:  # lamp at night
            lamp=np.exp(-(((xx-CX)**2+(yy-CY)**2)/(2*(RR*0.95)**2)))[...,None]
            kk=min(1,(t-8.6)/0.8); fr=fr+base*lamp*np.array([0.75,0.55,0.35])*kk
        p.stdin.write(np.clip(fr,0,255).astype(np.uint8).tobytes())
    p.stdin.close(); p.wait()
    d='../tw/cap_light'
    caps=[]
    for j,(t0,clk,lab) in enumerate(keys):
        c=caption(f'k{j}',f'<div style="position:absolute;left:60px;top:60px;font-family:Fraunces;font-weight:300;font-size:120px;line-height:1;color:#FBF3E6;text-shadow:0 3px 14px rgba(20,8,0,.45)">{clk}</div><div class="lbl" style="left:66px;top:190px;font-size:60px">{lab}</div>',d)
        caps.append((c,t0+0.15,t0+3.0 if j<3 else 12))
    c5=caption('c5','<div class="sm" style="top:1290px;font-size:20px">a tale in beads · one palm, all day · perset.shop</div>',d)
    compose([os.path.abspath('../tw/seg/light.mp4')],caps+[(c5,9.4,12)],os.path.abspath('../tw/out/beads-post-3-one-palm-all-day.mp4'),grain=5)
