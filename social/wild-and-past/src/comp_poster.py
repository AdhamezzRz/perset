import numpy as np, cv2
from PIL import Image
rng=np.random.default_rng(5)
wall=np.array(Image.open('gen/g07_wall.png').convert('RGB')).astype(np.float32)
H,W=wall.shape[:2]
P=np.array(Image.open('out/poster_flat.png').convert('RGBA')).astype(np.float32)
ph,pw=P.shape[:2]
# paper wrinkles: low freq noise + two creases (folded in four)
n=cv2.resize(rng.normal(0,1,(12,8)).astype(np.float32),(pw,ph),interpolation=cv2.INTER_CUBIC)
n2=cv2.GaussianBlur(rng.normal(0,1,(ph,pw)).astype(np.float32),(0,0),25)
sh=1+0.025*n+0.6*n2
yy,xx=np.mgrid[0:ph,0:pw].astype(np.float32)
for (pos,axis,s) in ((pw*0.5,'x',1),(ph*0.44,'y',1)):
    d=(xx-pos) if axis=='x' else (yy-pos)
    sh+= -0.05*np.exp(-(d/5)**2)+0.03*np.exp(-((d-10)/14)**2)
P[...,:3]*=sh[...,None]
# target quad (slight perspective, slight rotation)
cx,cy=900,1010; h=1180; w=h*pw/ph
src=np.float32([[0,0],[pw,0],[pw,ph],[0,ph]])
dst=np.float32([[cx-w/2+6,cy-h/2+4],[cx+w/2+2,cy-h/2-10],[cx+w/2-4,cy+h/2-2],[cx-w/2-2,cy+h/2+10]])
M=cv2.getPerspectiveTransform(src,dst)
Wp=cv2.warpPerspective(P,M,(W,H),flags=cv2.INTER_AREA,borderValue=(0,0,0,0))
a=Wp[...,3:4]/255
# lighting from wall
L=0.299*wall[...,0]+0.587*wall[...,1]+0.114*wall[...,2]
Lb=cv2.GaussianBlur(L,(0,0),6)
ref=np.median(Lb[400:1700,400:1400])
light=np.clip(Lb/ref,0.35,1.15)[...,None]
tint=cv2.GaussianBlur(wall,(0,0),40)/np.maximum(cv2.GaussianBlur(L,(0,0),40)[...,None],1)
rgb=Wp[...,:3]*light*(0.9+0.1*tint)*0.97
# soft contact shadow
sa=cv2.GaussianBlur(Wp[...,3],(0,0),7)/255
sa=np.roll(np.roll(sa,6,0),4,1)
base=wall*(1-0.22*sa[...,None])
out=base*(1-a)+rgb*a
# tape strips
def tape(x,y,ang,lw=150,lh=46):
    global out
    m=np.zeros((H,W),np.float32); box=cv2.boxPoints(((x,y),(lw,lh),ang)); cv2.fillPoly(m,[box.astype(np.int32)],1.0)
    m=cv2.GaussianBlur(m,(0,0),1.2)[...,None]
    col=np.array([236,228,206],np.float32)
    out=out*(1-0.42*m)+(out*0.6+col*0.4*light)*0.42*m*1.0+out*0.0
tape(dst[0][0]+30,dst[0][1]+12,-38); tape(dst[1][0]-30,dst[1][1]+14,40); tape(dst[3][0]+40,dst[3][1]-160,30,120,40); tape(dst[2][0]-40,dst[2][1]-160,-30,120,40)
# grain
hp=wall-cv2.GaussianBlur(wall,(0,0),1.5); s=hp.std()
g=rng.normal(0,s*0.9,(H,W)).astype(np.float32)
out=out+g[...,None]*a
out=np.clip(out,0,255).astype(np.uint8)
im=Image.fromarray(out).crop((250,230,1530,1830)).resize((1080,1350),Image.LANCZOS)
im.save('out/w_s1_spotted.jpg',quality=94)
im.resize((540,675)).save('spot_small.jpg')
