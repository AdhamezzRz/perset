from reel import *
bg=np.array(Image.open('../tw/gen/desert.png').convert('RGB').resize((1080,1920),Image.LANCZOS)).astype(np.float32)
L=bg.mean(2); col=L.mean(1)
# horizon: strongest vertical brightness drop between sky and sand
d=np.diff(cv2.GaussianBlur(col.reshape(-1,1),(1,15),4).ravel()); HZ=int(np.argmax(np.abs(d[600:1800]))+600); print('horizon',HZ)
PL=np.array(Image.open(SCR+'/cutouts/beads_hi.png').convert('RGBA')).astype(np.float32)
sky=bg[HZ-260:HZ-60].reshape(-1,3).mean(0)
n=int(6.6*FPS); p=enc('../tw/seg/mirage.mp4')
yy=np.arange(1920,dtype=np.float32)
for i in range(n):
    t=i/FPS; u=ease(min(1,t/6.4))
    dia=int(150+390*u); A=9*(1-u)+0.6; haze=0.55*(1-u)
    fr=bg.copy()
    pr=cv2.resize(PL,(dia,dia),interpolation=cv2.INTER_AREA)
    rgb=pr[...,:3]*(1-haze)+sky*haze; a=pr[...,3:]/255*(0.75+0.25*u)
    x0=540-dia//2; y0=HZ-dia+int(dia*0.02)
    layer=np.zeros_like(fr); al=np.zeros(fr.shape[:2]+(1,),np.float32)
    layer[y0:y0+dia,x0:x0+dia]=rgb; al[y0:y0+dia,x0:x0+dia]=a
    # mirage reflection under the horizon
    rh=int(dia*0.55); ref=rgb[::-1][:rh]; ra=a[::-1][:rh]*np.linspace(0.45,0,rh)[:,None,None]
    layer[HZ:HZ+rh,x0:x0+dia]=layer[HZ:HZ+rh,x0:x0+dia]*(1-ra)+(ref*0.6+sky*0.4)*ra; al[HZ:HZ+rh,x0:x0+dia]=np.maximum(al[HZ:HZ+rh,x0:x0+dia],ra)
    fr=fr*(1-al)+layer*al
    # heat shimmer: row-wise horizontal displacement near the horizon
    band=np.exp(-((yy-HZ)/(220+dia*0.6))**2)
    dx=A*band*(np.sin(yy*0.11+t*7.0)+0.5*np.sin(yy*0.037-t*4.3))
    mx=(np.arange(1080,dtype=np.float32)[None,:]+dx[:,None]).astype(np.float32); my=np.repeat(yy[:,None],1080,1).astype(np.float32)
    fr=cv2.remap(fr,mx,my,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
    p.stdin.write(np.clip(fr,0,255).astype(np.uint8).tobytes())
p.stdin.close(); p.wait()
real=np.array(Image.open(SCR+'/src/beads-2-perset-beads-setting.jpg').convert('RGB').crop((560,0,1910,2400))).astype(np.float32)
still(real,'../tw/seg/mirage2.mp4',3.6,1.0,1.07,(0.5,0.45),(0.5,0.45))
d='../tw/cap_mirage'
c1=caption('c1',chip('41°C. somewhere outside Cairo.',240),d)
c2=caption('c2',chip('you are not seeing things.',240),d)
c3=caption('c3',chip('that is a palm.',240),d)
c4=caption('c4','<div class="scr" style="top:150px;font-size:112px;color:#500C02;text-shadow:none">an oasis<br>for your table.</div>',d)
c5=caption('c5','<div class="sm" style="top:400px;font-size:22px;color:#500C02;text-shadow:none">a tale in beads · perset.shop</div>',d)
compose([os.path.abspath('../tw/seg/mirage.mp4'),os.path.abspath('../tw/seg/mirage2.mp4')],[(c1,0.3,2.3),(c2,2.3,4.4),(c3,4.4,6.5),(c4,6.8,10.2),(c5,7.2,10.2)],os.path.abspath('../tw/out/beads-story-3-mirage.mp4'),grain=5)
