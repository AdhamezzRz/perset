import json
from plate_tool import *
im=load('gen/g20_nish2.png')
E_=json.load(open('nish_ell.json'))
out=im.copy()
for e in E_:
    ell=(tuple(e[0]),tuple(e[1]),e[2]); (cx,cy),(w,h),_=ell
    yy,xx=np.mgrid[0:im.shape[0],0:im.shape[1]]
    L=lum(im.astype(np.float32))
    rn=np.hypot((xx-cx)/(w/2),(yy-cy)/(h/2))
    keep=((L<95)&(yy>cy+h*0.28)&(rn>0.8)).astype(np.float32)
    keep=ndimage.binary_opening(keep>0,iterations=1).astype(np.float32)
    keep=ndimage.binary_dilation(keep>0,iterations=2).astype(np.float32)
    keep=cv2.GaussianBlur(keep,(0,0),1.2)
    out=paste(out,ell,'salad',grade=0.2,keep=keep,shade_sigma=0.6,shade_pow=0.6,grain=False)
gen=im.astype(np.float32); out=out.astype(np.float32)
m=np.zeros(gen.shape[:2],np.float32)
for e in E_: m=np.maximum(m,ellipse_mask(gen.shape,(tuple(e[0]),tuple(e[1]),e[2]),grow=2))
gb=cv2.GaussianBlur(gen,(0,0),12); Lo=lum(out)[...,None]
o2=(out*0.92+Lo*0.08)*0.86+gb*0.14
res=np.clip(out*(1-m[...,None])+o2*m[...,None],0,255).astype(np.uint8)
Image.fromarray(res).save('ex/g20_nish_salad.png')
Image.fromarray(res).resize((1080,1920),Image.LANCZOS).save('kf/kf_nish_salad.jpg',quality=95)
Image.fromarray(res[650:1900,300:1260]).resize((480,625)).save('nish_salad_view.jpg')
