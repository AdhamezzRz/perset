import json
from vtool import *
sx,sy=1080/1520,1920/2688
def sc(e): return ((e[0][0]*sx,e[0][1]*sy),(e[1][0]*(sx+sy)/2,e[1][1]*(sx+sy)/2),e[2])
old=np.array(Image.open('kf/kf_nish.jpg').convert('RGB')).astype(np.float32)
new=np.array(Image.open('kf/kf_nish_salad.jpg').convert('RGB')).astype(np.float32)
ells=[sc(e) for e in json.load(open('nish_ell.json'))]
masks=[emask(e,grow=5) for e in ells]
rings=[np.clip(emask(e,grow=60)-emask(e,grow=4),0,1) for e in ells]
RING=np.max(rings,0)
boxes=[]
for m in masks:
    ys,xs=np.where(m>0); boxes.append((xs.min()-40,ys.min()-40,xs.max()+40,ys.max()+40))
prev=[(0.,0.)]*4
w=writer('vid/k5_nish_salad.mp4')
for n,fr in enumerate(frames('vid/k5_nish.mp4')):
    f=fr.astype(np.float32)
    R,G,B=f[...,0],f[...,1],f[...,2]
    woodskin=(R>G)&(G>B)&(R-B>45)&(G-B<62)&(G-B>14)&(lum(f)<188)
    d=np.abs(cv2.GaussianBlur(lum(f),(0,0),2)-cv2.GaussianBlur(lum(old),(0,0),2))
    occ=((d>22)&woodskin).astype(np.uint8)
    occ=cv2.morphologyEx(occ,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    k,lab,st,_=cv2.connectedComponentsWithStats(occ)
    keep=np.zeros_like(occ)
    for i in range(1,k):
        if st[i,cv2.CC_STAT_AREA]>2500 and st[i,cv2.CC_STAT_HEIGHT]>150: keep[lab==i]=1
    occ=cv2.morphologyEx(keep,cv2.MORPH_CLOSE,np.ones((15,15),np.uint8)); occ=cv2.dilate(occ,np.ones((5,5),np.uint8))
    occf=cv2.GaussianBlur(occ.astype(np.float32),(0,0),2)
    yel=(R>170)&(G>130)&(B<120)&(R-B>80)
    blu=(B>R+15)&(B>110)
    leak=((yel|blu)&~woodskin&(RING>0.5)).astype(np.uint8)
    leak=cv2.dilate(cv2.morphologyEx(leak,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8)),np.ones((7,7),np.uint8))
    lf=cv2.GaussianBlur(leak.astype(np.float32),(0,0),3)[...,None]
    out=f*(1-lf)+new*lf
    for i,(m,(x0,y0,x1,y1)) in enumerate(zip(masks,boxes)):
        fl=lum(f)[y0:y1,x0:x1]; kl=lum(old)[y0:y1,x0:x1]
        o=occf[y0:y1,x0:x1]; fl=fl*(1-o)+kl*o
        win=cv2.createHanningWindow((x1-x0,y1-y0),cv2.CV_32F)
        (dx,dy),resp=cv2.phaseCorrelate(kl,fl,win)
        if resp<0.1 or abs(dx)>30 or abs(dy)>30: dx,dy=prev[i]
        dx=0.5*dx+0.5*prev[i][0]; dy=0.5*dy+0.5*prev[i][1]; prev[i]=(dx,dy)
        A=np.float32([[1,0,dx],[0,1,dy]])
        ks=cv2.warpAffine(new,A,(W,H),borderMode=cv2.BORDER_REPLICATE); ms=cv2.warpAffine(m,A,(W,H))
        a=(ms*(1-occf))[...,None]; out=out*(1-a)+ks*a
    if n%30==0: print(n,[tuple(round(v,1) for v in p) for p in prev])
    w.stdin.write(np.clip(out,0,255).astype(np.uint8).tobytes())
w.stdin.close(); w.wait(); print('ok')
