from reel import *
# background linen
d='cap_sti'; os.makedirs(d,exist_ok=True)
open(f'{d}/bg.html','w').write(page('','', '',W=1080,H=1920,bgc='#E9D9C6'))
run(f'cd {d} && {NODE} {SCR}/pack/shoot.js 1080 1920 bg.html')
bg=np.array(Image.open(f'{d}/bg.png').convert('RGB')).astype(np.float32)
pl=Image.open(SCR+'/pack/assets/wild_hi.png').convert('RGBA'); D=940
p=np.array(pl.resize((D,D),Image.LANCZOS)).astype(np.float32)
prgb,pa=p[...,:3],p[...,3:]/255
X0,Y0=(1080-D)//2,1000-D//2
# shadow
sh=np.zeros((1920,1080),np.float32); sh[Y0:Y0+D,X0:X0+D]=pa[...,0]
sh=np.roll(np.roll(cv2.GaussianBlur(sh,(0,0),26),26,0),8,1)*0.38+np.roll(cv2.GaussianBlur(sh,(0,0),4),4,0)*0.3
base=bg*(1-sh[...,None])
# blank plate: cream body with real shading and real rim kept
L=0.299*prgb[...,0]+0.587*prgb[...,1]+0.114*prgb[...,2]
shade=cv2.GaussianBlur(L,(0,0),40); shade=shade/np.median(shade[pa[...,0]>0.5])
yy,xx=np.mgrid[0:D,0:D]; r=np.hypot(xx-D/2,yy-D/2)/(D/2)
blank=np.array([243,238,229],np.float32)*(1.0-0.07*r**2-0.05*(yy/D))[...,None]
rim=(r>0.93)[...,None].astype(np.float32); rim=cv2.GaussianBlur(rim,(0,0),1.5)[...,None] if rim.ndim==2 else cv2.GaussianBlur(rim[...,0],(0,0),1.5)[...,None]
blank=blank*(1-rim)+prgb*rim
rng=np.random.default_rng(4)
noise=cv2.resize(rng.random((60,60)).astype(np.float32),(D,D))
order=(yy/D)*0.97+noise*0.03
nd=key_needle=np.array(Image.open('a/needle.png').convert('RGBA'))
# needle sprite: scale so the needle is ~430px, tip at bottom-left in the png
ndl=Image.open('a/needle.png').convert('RGBA'); s=520/ndl.width; ndl=ndl.resize((int(ndl.width*s),int(ndl.height*s)),Image.LANCZOS)
ndl=np.array(ndl).astype(np.float32)
# find tip: left-most opaque pixel
ys,xs=np.where(ndl[...,3]>128); tip=(xs.min(),ys[np.argmin(xs)])
def put(fr,spr,x,y):
    h,w=spr.shape[:2]; x0,y0=int(x),int(y)
    xa,ya=max(0,x0),max(0,y0); xb,yb=min(1080,x0+w),min(1920,y0+h)
    if xb<=xa or yb<=ya: return fr
    sp=spr[ya-y0:yb-y0,xa-x0:xb-x0]; a=sp[...,3:]/255
    # needle shadow
    fr[ya+10:yb+10,xa+6:xb+6]=fr[ya+10:yb+10,xa+6:xb+6]*(1-0.25*a[:max(0,min(yb+10,1920)-(ya+10)),:max(0,min(xb+6,1080)-(xa+6))]) if False else fr[ya+10:yb+10,xa+6:xb+6]
    fr[ya:yb,xa:xb]=fr[ya:yb,xa:xb]*(1-a)+sp[...,:3]*a
    return fr
def frame_at(T,needle=True,glint=None):
    m=(order<T).astype(np.float32)
    m=cv2.GaussianBlur(m,(0,0),0.8)
    band=((order>=T-0.006)&(order<T)).astype(np.float32)
    col=blank*(1-m[...,None])+prgb*m[...,None]
    col=col*(1-0.18*band[...,None])
    if glint is not None:
        g=np.exp(-(((xx+yy)/D-glint)/0.06)**2)*0.55
        col=col+(255-col)*g[...,None]
    fr=base.copy()
    reg=fr[Y0:Y0+D,X0:X0+D]; fr[Y0:Y0+D,X0:X0+D]=reg*(1-pa)+col*pa
    return fr
# s2 reveal
n=int(4.6*FPS); P=enc('seg/sti2.mp4')
for i in range(n):
    t=i/(n-1); T=min(1.02,t*1.05)
    fr=frame_at(T)
    if T<1.0:
        yrow=Y0+T*D; half=np.sqrt(max(0,(D/2)**2-(yrow-Y0-D/2)**2))
        ph=(i*FPS/9.0/FPS*3)%2; ph=ph if ph<1 else 2-ph
        xn=X0+D/2-half*0.92+ph*half*1.84
        bob=6*np.sin(i*2.1)
        fr=put(fr,ndl,xn-tip[0],yrow-tip[1]+bob)
    P.stdin.write(np.clip(fr,0,255).astype(np.uint8).tobytes())
P.stdin.close(); P.wait()
# s3 glint
n=int(2.2*FPS); P=enc('seg/sti3.mp4')
for i in range(n):
    t=i/(n-1); fr=frame_at(2,False,glint=-0.3+2.6*ease(min(1,t/0.7)))
    P.stdin.write(np.clip(fr,0,255).astype(np.uint8).tobytes())
P.stdin.close(); P.wait()
# s1 macro hook on the real plate
hi=np.array(Image.open(SCR+'/pack/assets/wild_hi.png').convert('RGB'))
still(hi,'seg/sti1.mp4',2.2,2.25,2.45,(0.40,0.55),(0.43,0.53))
still('ex/g10_denim.png','seg/sti4.mp4',2.2,1.0,1.07)
c1=caption('c1',chip('zoom in. is this embroidery?',250),d)
c2=caption('c2',chip('40 hours of stitching?',250),d)
c3=caption('c3',chip('nope. it\'s porcelain.',250),d)
c3b=caption('c3b','<div class="scr" style="top:1560px;font-size:96px;color:#500C02;text-shadow:none">tap it. it goes ting.</div>',d)
c4=caption('c4',chip('looks stitched. holds dinner.',250),d)
segs=['seg/sti1.mp4','seg/sti2.mp4','seg/sti3.mp4','seg/sti4.mp4','seg/end_wild.mp4']
compose([os.path.abspath(s) for s in segs],[(c1,0.15,2.2),(c2,2.35,6.8),(c3,6.8,9.0),(c3b,7.3,9.0),(c4,9.1,11.2)],os.path.abspath('reels/wild-reel-1-not-embroidery.mp4'))
