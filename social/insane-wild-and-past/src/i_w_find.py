from reel import *
from plate_tool import paste
import json
OUT=os.path.abspath('../ins/out'); S=os.path.abspath('../ins/seg')
im=np.array(Image.open('../ins/gen/bazaar.png').convert('RGB'))
e=json.load(open('../ins/baz_ell.json')); ell=(tuple(e[0]),tuple(e[1]),e[2])
im=paste(im,ell,'wild',rot=28,grade=0.3,shade_sigma=0.3)
Image.fromarray(im).save('../ins/gen/bazaar_x.png')
ih,iw=im.shape[:2]; cx,cy=e[0][0]/iw,e[0][1]/ih
# 0-6.4: whole table, very slow drift; 6.4-8.4: zoom to the plate with a ring; hold
still(im,f'{S}/f1.mp4',6.4,1.0,1.04,(0.5,0.5),(0.5,0.5))
def ring(fr,t):
    k=min(1,max(0,(t-0.05)/0.25))
    if k>0:
        r=int(305+40*(1-k)); c=(540,960)
        o=fr.copy(); cv2.circle(o,c,r,(251,243,230),9,cv2.LINE_AA); fr=fr*(1-k)+o*k
        dim=np.ones_like(fr); yy,xx=np.mgrid[0:1920,0:1080]; m=(np.hypot(xx-540,yy-960)>r+8)
        fr[m]=fr[m]*(1-0.45*k)
    return fr
still(im,f'{S}/f2.mp4',1.4,1.0,3.6,(0.5,0.5),(cx,cy))
still(im,f'{S}/f3.mp4',2.0,3.6,3.7,(cx,cy),(cx,cy),fn=ring)
d=os.path.abspath('../ins/cap_find')
c0=caption('c0',chip('find the two leopards.',230),d)
c0b=caption('c0b',chip('you have 5 seconds.',330,dark=True,size=40),d)
nums=[caption(f'n{i}',f'<div style="position:absolute;left:0;right:0;top:1560px;text-align:center;font-family:Fraunces;font-weight:300;font-size:220px;color:#FBF3E6;text-shadow:0 4px 30px rgba(0,0,0,.6)">{i}</div>',d) for i in range(5,0,-1)]
c1=caption('c1',chip('found them?',230),d)
c2=caption('c2','<div class="scr" style="top:1430px;font-size:100px">hiding in<br>plain sight.</div><div class="sm" style="top:1660px;font-size:22px">stitches of the wild · perset.shop</div>',d)
caps=[(c0,0.2,6.3),(c0b,0.6,6.3)]+[(nums[i],1.2+i,2.2+i) for i in range(5)]+[(c1,6.4,7.4),(c2,7.6,9.8)]
compose([f'{S}/f1.mp4',f'{S}/f2.mp4',f'{S}/f3.mp4'],caps,os.path.abspath(f'{OUT}/wild-reel-2-find-the-leopards.mp4'),grain=4)
