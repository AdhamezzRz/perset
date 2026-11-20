from wc import *
import subprocess, random
OUT=os.path.abspath('../ins/out'); T=os.path.abspath('../ins/tmp'); os.makedirs(T,exist_ok=True)
BG=img(os.path.abspath('../ins/gen/notebook.png')); PH=img(SCR+'/src/past-1-perset-past-dinner-hero.jpg')
random.seed(4)
L0=838; P=50.2
def line(i,x,txt,cls='b',size=54,rot=None,extra=''):
    r=rot if rot is not None else random.uniform(-1.2,0.6)
    return f'<div class="{cls}" style="left:{x}px;top:{L0+i*P-size*0.92:.0f}px;font-size:{size}px;transform:rotate({r:.2f}deg);{extra}">{txt}</div>'
L=[line(0,180,"Nour’s gehaz list ♡",size=66,rot=-1.5,extra='text-decoration:underline;text-decoration-thickness:3px;text-underline-offset:8px'),
   line(2,180,'1. fridge (no frost) ✓'),line(3,180,'2. washing machine ✓'),line(4,180,'3. 12 tablecloths (Teta) ✓'),
   line(5,180,'4. the blue pyrex ✓'),line(6,180,'5. a sofa nobody sits on ✓'),line(7,180,'6. glasses for guests ONLY ✓'),
   line(8,180,'<s>7. any dinner set</s>'),
   line(9,180,'7. PRETTY PAST.',cls='r',size=62,rot=-2.4),line(10,215,'the peacock one. 24 pieces.',cls='r',rot=-1.8),
   line(11,215,'<u style="text-decoration-style:double;text-underline-offset:10px">NOT negotiable!!</u>',cls='r',size=62,rot=-2.6),
   line(13,180,'8. a mixer she’ll use once'),line(14,180,'9. more tablecloths'),line(16,180,'10. ...',rot=0)]
R=[line(15,900,'+ the salad plates.',cls='r',rot=-1.5),line(16,940,'the pink ones. all six.',cls='r',rot=-1.2),line(18,1250,'— mama ♡',cls='r',size=60,rot=-3)]
css=f"""html,body{{width:1792px;height:2240px}}.bg{{background:url({BG}) 0 0/1792px 2240px!important}}.vig,.grain{{display:none}}
.b,.r{{position:absolute;font-family:'Caveat';white-space:nowrap;mix-blend-mode:multiply;transform-origin:0 100%}}
.b{{color:#22357c;opacity:.9;font-weight:500}}.r{{color:#B3241B;opacity:.92;font-weight:700}}
s{{text-decoration-color:#22357c;text-decoration-thickness:4px}}
#ph{{position:absolute;left:925px;top:745px;width:600px;padding:20px 20px 64px;background:#FAF7F0;transform:rotate(3.5deg);box-shadow:0 14px 26px rgba(60,40,20,.38),0 2px 4px rgba(0,0,0,.2)}}
#ph div{{width:600px;height:600px;background:url({PH}) center/cover}}
#ph span{{position:absolute;left:0;right:0;bottom:12px;text-align:center;font-family:'Caveat';font-size:40px;color:#22357c}}
.tp{{position:absolute;width:190px;height:58px;background:rgba(244,236,205,.72);box-shadow:0 1px 3px rgba(0,0,0,.18)}}
#light{{position:absolute;inset:0;background:radial-gradient(ellipse at 15% 10%,rgba(255,220,160,.18),transparent 55%);mix-blend-mode:soft-light}}
"""
body=f"""{''.join(L)}{''.join(R)}
<div id="ph"><div></div><span>THIS. ONE.</span></div>
<div class="tp" style="left:1130px;top:715px;transform:rotate(-3deg)"></div>
<svg style="position:absolute;left:0;top:0;mix-blend-mode:multiply" width="1792" height="2240"><path d="M720 1305 C 800 1250, 860 1180, 905 1110" fill="none" stroke="#B3241B" stroke-width="6" stroke-linecap="round" opacity=".9"/><path d="M880 1118 L907 1106 L908 1136" fill="none" stroke="#B3241B" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" opacity=".9"/>
<path d="M120 1278 l14 -26 l14 26 l-30 -16 h32 z" fill="none" stroke="#B3241B" stroke-width="4" opacity=".85"/></svg>
<div id="light"></div>"""
f=f'{T}/gehaz.html'; open(f,'w').write(page(css,body,'',W=1792,H=2240,bgc='#ddd',fibers=False))
subprocess.run(f'cd {T} && NODE_PATH=$(npm root -g) node {SCR}/pack/shoot.js 1792 2240 gehaz.html',shell=True,check=True)
Image.open(f'{T}/gehaz.png').convert('RGB').resize((1080,1350),Image.LANCZOS).save(f'{OUT}/past-post-1-gehaz-list.png')
