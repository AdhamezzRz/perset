from reel import *
from plate_tool import paste, cutout
import json
# hi-res canvas: symmetric table at 2x with the real plate at native resolution
k=Image.open('ex/sym_key.png').convert('RGB').resize((2160,3840),Image.LANCZOS)
k=np.array(k)
s=json.load(open('sym_ell.json'))['sym_key']; cx,cy=s[0][0]*2160/1520,s[0][1]*3840/2688; R=s[1][0]/2*2160/1520
k=paste(k,((cx,cy),(2*R,2*R),0.0),'wild',grade=0.35,shade_sigma=0.06)
Image.fromarray(k).save('a/sym_2x.jpg',quality=95)
fx,fy=cx/2160,cy/3840; sx=(cx-0.62*R)/2160
still(k,'seg/st1.mp4',1.6,3.0,3.3,(sx,fy),(sx,fy))
spots=[('gen/g03_awning.png',(0.5,0.14)),('gen/g04_cabana.png',(0.42,0.10)),('gen/g05_karkade.png',(0.42,0.10)),('gen/g06_shirt.png',(0.40,0.30))]
for i,(f,c) in enumerate(spots):
    def fn(fr,t,c=c): return fr
    # punch: 1.9x on the stripe for 0.25s, then ease out to 1.0
    im=np.array(Image.open(f).convert('RGB')).astype(np.float32)
    n=int(1.2*FPS); p=enc(f'seg/st{i+2}.mp4'); ih,iw=im.shape[:2]; base=max(W/iw,H/ih)
    for j in range(n):
        t=j/(n-1); a=min(1,t/0.42); a=1-(1-a)**3
        z=base*(1.9-0.88*a+0.04*t)
        ccx=(c[0]+(0.5-c[0])*a)*iw; ccy=(c[1]+(0.5-c[1])*a)*ih
        hw,hh=W/2/z,H/2/z; ccx=min(max(ccx,hw),iw-hw); ccy=min(max(ccy,hh),ih-hh)
        M=np.float32([[z,0,W/2-z*ccx],[0,z,H/2-z*ccy]])
        fr=cv2.warpAffine(im,M,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
        if j<3: fr=cv2.blur(fr,(1,41-j*12))  # whip blur on the cut
        p.stdin.write(np.clip(fr,0,255).astype(np.uint8).tobytes())
    p.stdin.close(); p.wait()
still(k,'seg/st6.mp4',2.8,3.3,1.0,(sx,fy),(fx,fy))
d='cap_st'
c1=caption('c1',chip('once you see the stripe…',250),d)
c2=caption('c2',chip('…you see it everywhere.',250),d)
c3=caption('c3',chip('so we put it on a plate.',250),d)
labels=['downtown, 4 pm','sahel, august','karkade, zamalek','a tuesday shirt']
L=[caption(f'l{i}',f'<div class="lbl" style="left:70px;top:1680px;transform:rotate(-3deg)">{t}</div>',d) for i,t in enumerate(labels)]
caps=[(c1,0.15,1.6),(c2,1.6,6.4),(c3,6.55,9.2)]+[(L[i],1.6+i*1.2+0.15,1.6+(i+1)*1.2) for i in range(4)]
segs=['seg/st1.mp4']+[f'seg/st{i}.mp4' for i in range(2,6)]+['seg/st6.mp4','seg/end_wild.mp4']
compose([os.path.abspath(s) for s in segs],caps,os.path.abspath('reels/wild-reel-3-same-stripe.mp4'))
