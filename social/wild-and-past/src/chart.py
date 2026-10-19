import numpy as np, json
from PIL import Image, ImageDraw, ImageFont
from scipy.cluster.vq import kmeans2
im=Image.open('../../pack/assets/wild_hi.png').convert('RGBA')
N=64; C=14  # cells across, px per cell
sm=im.resize((N,N),Image.LANCZOS); a=np.array(sm).astype(float)
rgb=a[...,:3]; al=a[...,3]
yy,xx=np.mgrid[0:N,0:N]; inside=((xx-N/2+.5)**2+(yy-N/2+.5)**2)<=(N/2-0.3)**2
pix=rgb[inside]
np.random.seed(2)
cent,lab=kmeans2(pix,9,minit='++',seed=2,iter=30)
L=np.full((N,N),-1); L[inside]=lab
# order clusters by count
cnt=np.bincount(lab,minlength=len(cent)); order=np.argsort(-cnt)
syms=['','×','●','▲','◆','/','○','■','✚','◇']
names={}
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',int(C*0.78)) if __import__('os').path.exists('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf') else ImageFont.load_default()
S=2; W=N*C*S
out=Image.new('RGBA',(W+2,W+2),(0,0,0,0)); d=ImageDraw.Draw(out)
font=ImageFont.truetype(font.path,int(C*S*0.72)) if hasattr(font,'path') else font
symfor={}
for rank,k in enumerate(order): symfor[k]=syms[rank] if rank<len(syms) else '?'
for y in range(N):
    for x in range(N):
        k=L[y,x]
        if k<0: continue
        c=cent[k]; lc=tuple(int(v*0.82+255*0.18) for v in c)
        x0,y0=x*C*S,y*C*S
        d.rectangle([x0,y0,x0+C*S,y0+C*S],fill=lc+(255,))
        s=symfor[k]
        if s:
            lum=0.3*c[0]+0.59*c[1]+0.11*c[2]
            col=(40,25,20,230) if lum>110 else (250,245,235,230)
            d.text((x0+C*S/2,y0+C*S/2+1),s,fill=col,font=font,anchor='mm')
# grid
for i in range(N+1):
    w=3 if i%10==0 else 1; col=(60,40,35,200) if i%10==0 else (90,80,75,110)
    d.line([(i*C*S,0),(i*C*S,W)],fill=col,width=w); d.line([(0,i*C*S),(W,i*C*S)],fill=col,width=w)
out.save('chart.png')
leg=[{'sym':symfor[k],'rgb':[int(v) for v in cent[k]],'n':int(cnt[k])} for k in order]
json.dump(leg,open('legend.json','w')); print(leg)
