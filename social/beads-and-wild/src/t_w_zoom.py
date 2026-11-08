import reel
from reel import *
from plate_tool import paste, cutout
reel.W,reel.H=1080,1350
W,H=1080,1350
L0=np.array(Image.open('../tw/gen/z1_sat.png').convert('RGB')).astype(np.float32)
L1=np.array(Image.open('../tw/gen/z2_zamalek.png').convert('RGB')).astype(np.float32)
L2=np.array(Image.open('../tw/gen/z3_roof.png').convert('RGB'))
# real plates on the rooftop table, each facing its seat
tc=np.array([908,1150.])
plates=[(908,965),(755,1090),(1065,1077),(835,1262),(1010,1255)]
for (x,y) in plates:
    ang=np.degrees(np.arctan2(tc[0]-x,-(tc[1]-y)))*-1  # rotate so the plate top faces the table centre
    L2=paste(L2,((x,y),(92,92),0.0),'wild',rot=ang,grade=0.25,shade_sigma=0.3,grain=False)
L2=L2.astype(np.float32)
f0,c0=0.11,(0.5*1792,0.47*2240)
f1,anc2,c1=0.22,(0.507*1792,0.513*2240),(964,1035)
# affine L_k px -> L0 px
A1=np.array([[f0,0,c0[0]-f0*896],[0,f0,c0[1]-f0*1120]])
s2=f1*f0
p_anc2_L0=A1@np.array([c1[0],c1[1],1])
A2=np.array([[s2,0,p_anc2_L0[0]-s2*anc2[0]],[0,s2,p_anc2_L0[1]-s2*anc2[1]]])
T=A2@np.array([835,1262,1.])   # target plate in L0 px
PD=92*s2                         # plate diameter in L0 px
k0=W/1792.
Zmax=820/(PD*k0)
HERO=np.array(Image.open(SCR+'/pack/assets/wild_hi.png').convert('RGBA')).astype(np.float32)
hero_ang=np.degrees(np.arctan2(tc[0]-835,-(tc[1]-1262)))*-1
def mip(img,scale):
    # pre-shrink for heavy downscaling
    if scale<0.5:
        f=max(scale*1.5,0.02); return cv2.resize(img,None,fx=f,fy=f,interpolation=cv2.INTER_AREA),f
    return img,1.0
def feather(h,w,edge=0.12):
    y=np.linspace(0,1,h)[:,None]; x=np.linspace(0,1,w)[None,:]
    m=np.clip(np.minimum.reduce([x,1-x])/edge,0,1)*np.clip(np.minimum.reduce([y,1-y])/edge,0,1)
    return (m*m*(3-2*m)).astype(np.float32)
F1=feather(*L1.shape[:2]); F2=feather(*L2.shape[:2])
n=int(9.0*FPS); p=enc('../tw/seg/zoom.mp4')
for i in range(n):
    t=i/FPS; u=min(1,t/6.6); u=u*u*(3-2*u)
    Z=np.exp(np.log(Zmax)*u)
    w=np.clip(np.log(Z)/np.log(Zmax),0,1)
    d0=(T-np.array([896,1120]))*k0
    off=d0*(1-w)**2
    cam=T-off/(Z*k0)
    def M_for(A):  # L_k px -> screen px
        S=np.array([[Z*k0,0,W/2-Z*k0*cam[0]],[0,Z*k0,H/2-Z*k0*cam[1]]])
        return S@np.vstack([A,[0,0,1]])
    fr=np.zeros((H,W,3),np.float32)
    for img,A,Fm in ((L0,np.array([[1,0,0],[0,1,0.]]),None),(L1,A1,F1),(L2,A2,F2)):
        M=M_for(A); sc=M[0,0]
        onscreen=img.shape[1]*sc
        if onscreen<60: continue
        src,f=mip(img,sc); Mf=M.copy(); Mf[:,:2]/=f
        warped=cv2.warpAffine(src,Mf,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
        if Fm is None: fr=warped; continue
        fm,_=mip(Fm,sc) if sc<0.5 else (Fm,1.0)
        a=cv2.warpAffine(fm,Mf,(W,H),flags=cv2.INTER_LINEAR)
        a=a*np.clip((onscreen/W-0.25)/0.45,0,1)
        fr=fr*(1-a[...,None])+warped*a[...,None]
    # sharp hero plate drawn from the real photo once it is big enough
    dia=PD*Z*k0
    if dia>40:
        D=int(dia); pr=cv2.resize(HERO,(D,D),interpolation=cv2.INTER_AREA)
        Mr=cv2.getRotationMatrix2D((D/2,D/2),hero_ang,1.0); pr=cv2.warpAffine(pr,Mr,(D,D),borderValue=(0,0,0,0))
        sx,sy=(T[0]-cam[0])*Z*k0+W/2,(T[1]-cam[1])*Z*k0+H/2
        x0,y0=int(sx-D/2),int(sy-D/2); xa,ya=max(0,x0),max(0,y0); xb,yb=min(W,x0+D),min(H,y0+D)
        if xb>xa and yb>ya:
            al=pr[ya-y0:yb-y0,xa-x0:xb-x0,3:]/255*min(1,(dia-40)/60)
            fr[ya:yb,xa:xb]=fr[ya:yb,xa:xb]*(1-al)+pr[ya-y0:yb-y0,xa-x0:xb-x0,:3]*al
    p.stdin.write(np.clip(fr,0,255).astype(np.uint8).tobytes())
p.stdin.close(); p.wait()
d='../tw/cap_zoom'
c1=caption('c1',chip('somewhere in Cairo…',90),d)
c2=caption('c2',chip('Zamalek.',90),d)
c3=caption('c3',chip('a rooftop. 1:30 pm.',90),d)
c4=caption('c4','<div class="scr" style="top:70px;font-size:96px">two leopards, under<br>two parasols.</div>',d)
c5=caption('c5','<div class="sm" style="top:1275px;font-size:20px">stitches of the wild · a set for six · perset.shop</div>',d)
compose([os.path.abspath('../tw/seg/zoom.mp4')],[(c1,0.15,2.6),(c2,2.6,4.2),(c3,4.2,6.2),(c4,6.6,9.0),(c5,7.0,9.0)],os.path.abspath('../tw/out/wild-post-2-somewhere-in-cairo.mp4'),grain=4)
