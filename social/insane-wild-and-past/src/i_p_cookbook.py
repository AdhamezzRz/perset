from wc import *
import subprocess, cv2
OUT=os.path.abspath('../ins/out'); T=os.path.abspath('../ins/tmp'); os.makedirs(T,exist_ok=True)
bg=np.array(Image.open('../ins/gen/cookbook.png').convert('RGB')).astype(np.float32)
Q=np.float32([(262,726),(1142,544),(1556,1700),(566,2024)])
CW,CH=900,1220
PL=img(SCR+'/cutouts/past_dinner.png')
frame=''.join(f'<div class="fr" style="inset:{i}px;border-width:{w}px"></div>' for i,w in ((70,5),(84,2)))
css=f"""html,body{{width:{CW}px;height:{CH}px;background:transparent}}.bg,.vig,.grain{{display:none}}
.fr{{position:absolute;border-style:solid;border-color:#3b1e0e}}
.c{{position:absolute;left:0;right:0;text-align:center;color:#3b1e0e}}
#pl{{position:absolute;left:210px;top:395px;width:480px;height:480px;border-radius:50%;background:url({PL}) center/contain no-repeat}}
#ring{{position:absolute;left:195px;top:380px;width:500px;height:500px;border-radius:50%;border:3px solid #3b1e0e}}
.orn{{position:absolute;font-family:'Fraunces';font-size:40px;color:#8f1d14}}
"""
ink=f"""{frame}
<div class="c" style="top:150px;font-family:'Jost';font-weight:500;letter-spacing:.42em;font-size:24px">THE</div>
<div class="c" style="top:185px;font-family:'Fraunces';font-weight:700;font-size:96px;line-height:.95;letter-spacing:.02em">PRETTY<br>PAST</div>
<div class="c" style="top:378px;font-family:'Jost';font-weight:500;letter-spacing:.5em;font-size:0">.</div>
<div id="ring"></div><div style="position:absolute;left:96px;top:96px;width:16px;height:16px;background:#8f1d14;transform:rotate(45deg)"></div><div style="position:absolute;left:788px;top:96px;width:16px;height:16px;background:#8f1d14;transform:rotate(45deg)"></div><div style="position:absolute;left:96px;top:1108px;width:16px;height:16px;background:#8f1d14;transform:rotate(45deg)"></div><div style="position:absolute;left:788px;top:1108px;width:16px;height:16px;background:#8f1d14;transform:rotate(45deg)"></div>
<div class="c" style="top:905px;font-family:'Damion';font-size:66px;color:#8f1d14">Cookbook</div>
<div class="c" style="top:995px;font-family:'Fraunces';font-style:italic;font-size:34px">recipes for six, as Teta made them</div>
<div class="c" style="top:1065px;font-family:'Jost';font-weight:500;letter-spacing:.34em;font-size:20px">CAIRO · PER SET · SERVES SIX</div>"""
open(f'{T}/cb_ink.html','w').write(page(css,ink,'',W=CW,H=CH,bgc='transparent',fibers=False))
open(f'{T}/cb_pl.html','w').write(page(css,'<div id="pl"></div>','',W=CW,H=CH,bgc='transparent',fibers=False))
subprocess.run(f'cd {T} && NODE_PATH=$(npm root -g) node {SCR}/wp/out/shootT1.js {CW} {CH} cb_ink.html && NODE_PATH=$(npm root -g) node {SCR}/wp/out/shootT1.js {CW} {CH} cb_pl.html',shell=True,check=True)
M=cv2.getPerspectiveTransform(np.float32([(0,0),(CW,0),(CW,CH),(0,CH)]),Q)
def warp(p):
    a=np.array(Image.open(p).convert('RGBA')).astype(np.float32)
    big=cv2.resize(a,(CW*2,CH*2),interpolation=cv2.INTER_CUBIC)
    M2=M@np.diag([0.5,0.5,1])
    return cv2.warpPerspective(big,M2,(bg.shape[1],bg.shape[0]),flags=cv2.INTER_LINEAR)
ink=warp(f'{T}/cb_ink.png'); pl=warp(f'{T}/cb_pl.png')
L=0.299*bg[...,0]+0.587*bg[...,1]+0.114*bg[...,2]
# ink: multiply, slightly worn by the cloth texture
ia=ink[...,3:]/255*0.9
hp=(L-cv2.GaussianBlur(L,(0,0),3))[...,None]
wear=np.clip(1+hp/40,0.6,1.2)
out=bg*(1-ia)+bg*(ink[...,:3]/255)*ia*wear
# plate: real pixels, lit by the scene (low-frequency light incl. the window dapple), textured very slightly by the cloth
pa=cv2.GaussianBlur(pl[...,3],(0,0),0.8)[...,None]/255
lo=cv2.GaussianBlur(L,(0,0),18); inside=pa[...,0]>0.5
sh=np.clip((lo/np.median(lo[inside]))**0.5,0.8,1.12)
prgb=pl[...,:3]*sh[...,None]*(1+hp/120)
prgb=prgb*np.float32([1.0,0.97,0.9])  # warm room light
out=out*(1-pa)+prgb*pa
out=np.clip(out,0,255).astype(np.uint8)
Image.fromarray(out).resize((1080,1350),Image.LANCZOS).save(f'{OUT}/past-post-2-cookbook.png')
