import reel
from reel import *
reel.W,reel.H=1080,1350
W,H=1080,1350
bg=np.array(Image.open('../tw/gen/turntable.png').convert('RGB').crop((200,250,1500,1875)).resize((W,H),Image.LANCZOS)).astype(np.float32)
s=1080/1300; cx,cy=(844-200)*s,(852-250)*s; R=380*s
pl=Image.open(SCR+'/pack/assets/wild_hi.png').convert('RGBA').resize((int(2*R),int(2*R)),Image.LANCZOS)
P=np.array(pl).astype(np.float32); D=P.shape[0]
yy,xx=np.mgrid[0:D,0:D].astype(np.float32)
grad=np.clip(1.0-0.20*((D-xx)/D*0.6+(yy/D)*0.4),0.75,1.0)
tint=np.array([1.0,0.93,0.82],np.float32)
spec=np.exp(-(((xx-D*0.68)/(D*0.16))**2+((yy-D*0.30)/(D*0.07))**2))
# shadow
a0=P[...,3]/255
sh=np.zeros((H,W),np.float32); x0,y0=int(cx-D/2),int(cy-D/2)
sh[y0:y0+D,x0:x0+D]=a0
sh=np.roll(np.roll(cv2.GaussianBlur(sh,(0,0),14),14,0),-10,1)*0.55
base=bg*(1-sh[...,None])
n=int(10.8*FPS); p=enc('../tw/seg/vinyl.mp4')
for i in range(n):
    ang=-360*6*i/n
    M=cv2.getRotationMatrix2D((D/2,D/2),ang,1.0)
    r=cv2.warpAffine(P,M,(D,D),flags=cv2.INTER_LINEAR,borderValue=(0,0,0,0))
    rgb=r[...,:3]*tint*grad[...,None]; rgb=rgb+(255-rgb)*(spec*0.22)[...,None]
    a=(r[...,3:]/255)
    fr=base.copy(); reg=fr[y0:y0+D,x0:x0+D]; fr[y0:y0+D,x0:x0+D]=reg*(1-a)+rgb*a
    p.stdin.write(np.clip(fr,0,255).astype(np.uint8).tobytes())
p.stdin.close(); p.wait()
d='../tw/cap_vinyl'
top=caption('top','<div class="chip" style="top:56px;font-size:30px;padding:12px 24px 14px">now playing · Stitches of the Wild · side A</div>',d)
ly=['♪ two leopards','♪ under two parasols','♪ a dinner for six','♪ on repeat']
L=[caption(f'l{i}',f'<div class="scr" style="top:1110px;font-size:{108}px">{t}</div>',d) for i,t in enumerate(ly)]
caps=[(top,0.0,10.8)]+[(L[i],i*2.7+0.1,i*2.7+2.6) for i in range(4)]
compose([os.path.abspath('../tw/seg/vinyl.mp4')],caps,os.path.abspath('../tw/out/wild-post-3-on-repeat.mp4'))
