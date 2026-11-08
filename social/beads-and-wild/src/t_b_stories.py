import sys
from reel import *
PB=img(SCR+'/cutouts/beads_hi.png')
OUT=os.path.abspath('../tw/st'); os.makedirs(OUT,exist_ok=True)
def render(name,css,body,js,dur,bgc='#F2EBDD'):
    d=f'{OUT}/{name}'; os.makedirs(d,exist_ok=True)
    open(f'{d}/p.html','w').write(page(css,body,js,W=1080,H=1920,bgc=bgc))
    run(f'cd "{d}" && VW=1080 VH=1920 {NODE} {SCR}/pack/render.js p.html fr {FPS} {dur} jpeg 0')
    run(f'{FF} -v error -y -framerate {FPS} -i "{d}/fr/f%04d.jpg" -vf "noise=alls=5:allf=t,format=yuv420p" -c:v libx264 -crf 18 -preset slow -movflags +faststart "{os.path.abspath("../tw/out")}/{name}.mp4"')
which=sys.argv[1:] or ['palm','quiz']
if 'palm' in which:
    import random; r=random.Random(3)
    stars=''.join(f'<i class="st" style="left:{r.randint(0,1080)}px;top:{r.randint(0,1920)}px;width:{r.choice([3,4,5,6])}px;height:{r.choice([3,4,5,6])}px" data-p="{r.random()*6.28:.2f}"></i>' for _ in range(90))
    lines=['I see… a long table.','six chairs. one guest is always late.','someone will ask where the plates are from.','you will say: perset.shop']
    lh=''.join(f'<div class="ln" id="ln{i}" data-t="{t}"></div>' for i,t in enumerate(lines))
    css=f"""
.bg{{background:radial-gradient(ellipse at 50% 42%,#5a1a12 0%,#2a0904 70%)!important}}.fibers{{opacity:.12;mix-blend-mode:screen}}.vig{{display:none}}
.st{{position:absolute;border-radius:50%;background:#F7D9A0;box-shadow:0 0 10px #F7D9A0}}
#h{{position:absolute;left:0;right:0;top:140px;text-align:center;font-family:'Damion';font-size:130px;color:#F4D8A8;line-height:1;text-shadow:0 0 30px rgba(244,190,120,.45)}}
#s{{position:absolute;left:0;right:0;top:290px;text-align:center;font-size:30px;letter-spacing:.3em;text-transform:uppercase;color:#F2A4B6}}
#glow{{position:absolute;left:140px;top:420px;width:800px;height:800px;border-radius:50%;background:radial-gradient(circle,rgba(255,210,140,.55),rgba(255,180,120,0) 68%)}}
#pl{{position:absolute;left:200px;top:480px;width:680px;height:680px;background:url({PB}) center/contain no-repeat;filter:drop-shadow(0 0 40px rgba(255,200,140,.5)) drop-shadow(0 30px 40px rgba(0,0,0,.5))}}
#lines{{position:absolute;left:90px;right:90px;top:1260px;text-align:center}}
.ln{{font-family:'Caveat';font-size:64px;line-height:1.15;color:#FBEAD2;min-height:74px}}
.ln:last-child{{color:#F2A4B6}}
#ft{{position:absolute;left:0;right:0;bottom:90px;text-align:center;font-size:22px;letter-spacing:.3em;text-transform:uppercase;color:#F4D8A8}}
"""
    body=f'{stars}<div id="h">palm reading.</div><div id="s">the plate kind</div><div id="glow"></div><div id="pl"></div><div id="lines">{lh}</div><div id="ft">a tale in beads · a set for six</div>'
    js="""const stars=[...document.querySelectorAll('.st')];const L=[...document.querySelectorAll('.ln')];
window.setT=t=>{stars.forEach(s=>{s.style.opacity=0.25+0.75*Math.max(0,Math.sin(t*2+ +s.dataset.p))});
const o=(id,a,dy=24)=>{const e=document.getElementById(id),k=ease.out(seg(t,a,.6));e.style.opacity=k;e.style.transform=`translateY(${(1-k)*dy}px)`};
o('h',.1);o('s',.5);const g=document.getElementById('glow');g.style.opacity=(0.6+0.4*Math.sin(t*2.2))*seg(t,.6,.8);g.style.transform=`scale(${1+0.04*Math.sin(t*2.2)})`;
const p=document.getElementById('pl');p.style.opacity=seg(t,.3,.8);p.style.transform=`rotate(${t*4}deg) scale(${0.92+0.08*ease.out(seg(t,.3,1.2))})`;
L.forEach((e,i)=>{const s=1.8+i*2.3,txt=e.dataset.t;const n=Math.floor(Math.max(0,Math.min(1,(t-s)/1.2))*txt.length);e.textContent=txt.slice(0,n)});
o('ft',10.6,8);};window.setT(0);"""
    render('beads-story-1-palm-reading',css,body,js,12.5,bgc='#2a0904')
if 'quiz' in which:
    S=660; X0,Y0=210,610; R=S/2*0.961; N=151; ph=-0.07638328
    dots=''.join(f'<circle id="d{m}" cx="{X0+S/2+R*np.cos((-ph+2*np.pi*m)/N):.1f}" cy="{Y0+S/2+R*np.sin((-ph+2*np.pi*m)/N):.1f}" r="7"/>' for m in range(N))
    css=f"""
.bg{{background:#E7F0E2!important}}
#h{{position:absolute;left:0;right:0;top:130px;text-align:center;font-family:'Damion';font-size:112px;line-height:1;color:#500C02}}
#pl{{position:absolute;left:{X0}px;top:{Y0}px;width:{S}px;height:{S}px;background:url({PB}) center/contain no-repeat;filter:drop-shadow(0 26px 30px rgba(40,60,30,.3))}}
svg#dots{{position:absolute;left:0;top:0}} svg#dots circle{{fill:#FFF3E0;opacity:0;filter:drop-shadow(0 0 6px #F2A4B6)}}
.opt{{position:absolute;left:150px;width:780px;height:96px;border-radius:48px;background:#FBF8F2;box-shadow:0 6px 18px rgba(40,60,30,.15);display:flex;align-items:center;padding:0 40px;font-size:40px;color:#2a1a16;font-weight:500}}
.opt b{{display:inline-block;width:64px;color:#C9566B}}
#cnt{{position:absolute;left:0;right:0;top:418px;text-align:center;font-family:'Fraunces';font-weight:300;font-size:120px;color:#500C02;line-height:1;opacity:0}}
#ans{{position:absolute;left:0;right:0;top:1640px;text-align:center;font-family:'Damion';font-size:80px;color:#500C02;line-height:1.05}}
#ft{{position:absolute;left:0;right:0;bottom:56px;text-align:center;font-size:22px;letter-spacing:.3em;text-transform:uppercase;color:#500C02}}
"""
    body=(f'<div id="h">how many beads<br>on the rim?</div><div id="pl"></div><svg id="dots" width="1080" height="1920">{dots}</svg><div id="cnt">0</div>'
          '<div class="opt" id="o0" style="top:1320px"><b>A</b>about 50</div><div class="opt" id="o1" style="top:1430px"><b>B</b>about 100</div><div class="opt" id="o2" style="top:1540px"><b>C</b>150 and up</div>'
          '<div id="ans">on the rim alone.<br><span style="font-size:58px">the palm has its own.</span></div><div id="ft">a tale in beads · perset.shop</div>')
    js=f"""const D=[...document.querySelectorAll('#dots circle')];
window.setT=t=>{{const o=(id,a,dy=24)=>{{const e=document.getElementById(id),k=ease.out(seg(t,a,.5));e.style.opacity=k;e.style.transform=`translateY(${{(1-k)*dy}}px)`}};
o('h',.1);document.getElementById('h').style.top=t>3.6?'110px':'130px';o('pl',.3,40);['o0','o1','o2'].forEach((id,i)=>o(id,.9+i*.2,20));
const u=seg(t,3.6,4.2);const n=Math.floor(Math.pow(u,1.4)*{N});D.forEach((d,i)=>d.style.opacity=i<n?1:0);
const c=document.getElementById('cnt');c.style.opacity=t>3.6?1:0;c.textContent=n>=150?'150+':n;
if(t>8.0){{['o0','o1'].forEach(id=>document.getElementById(id).style.opacity=0.35);const e=document.getElementById('o2');e.style.background='#500C02';e.style.color='#FBF8F2';}}
o('ans',8.4,24);o('ft',8.8,8);
if(t>3.6&&t<8.0){{document.getElementById('ans').style.opacity=0}}
document.getElementById('pl').style.filter=t>3.6?'drop-shadow(0 26px 30px rgba(40,60,30,.3)) brightness(.82)':'drop-shadow(0 26px 30px rgba(40,60,30,.3))';}};window.setT(0);"""
    render('beads-story-2-bead-count',css,body,js,11.5,bgc='#E7F0E2')
