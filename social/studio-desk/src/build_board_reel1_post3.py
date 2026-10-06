import sys; sys.path.insert(0,'..')
from common import *
A='../assets/'
leo=img(A+'macro_leopards.jpg'); palm=img(A+'macro_palm.jpg'); pea=img(A+'macro_peacock.jpg')
CH=['#E38E7B','#B58A38','#476D3E','#6693BC','#F6BF0F']
polyS=jag(540,340,seed=11,amp=7,step=20,edges='tb')
fan=''.join(f'''<div class="abs chip" id="chip{i}" style="left:200px;top:990px;width:120px;height:300px;transform-origin:60px 280px;transform:rotate(0deg)"><div class="sh-s" style="width:120px;height:300px;background:#FBF8F2;border-radius:8px 8px 5px 5px;overflow:hidden"><div style="height:222px;background:{c}"></div><div class="eyebrow" style="font-size:12px;letter-spacing:.14em;padding:10px 10px;color:#6E5A54">{c}</div></div></div>''' for i,c in enumerate(CH))
body=f'''
<div class="abs script" id="title" style="left:66px;top:118px;font-size:120px;line-height:.95;color:#500C02;white-space:nowrap">the moodboard</div>
<div class="abs eyebrow" id="sub" style="left:72px;top:246px;font-size:20px;color:#6E5A54">for your next table</div>

<div class="abs it" id="e1" style="left:60px;top:330px;width:420px;height:520px;--rot:-5deg">
  <div class="sh" style="width:420px;height:520px"><div style="width:420px;height:520px;background:#FDFBF6;padding:24px"><div style="width:372px;height:372px;background:url({leo}) center/cover"></div>
   <div class="script" style="font-size:62px;color:#500C02;text-align:center;margin-top:20px;line-height:1">stitches</div></div></div>
  <div class="tape tp" id="t1" style="left:150px;top:-22px;width:130px;transform:rotate(-3deg)"></div></div>

<div class="abs it" id="e2" style="left:500px;top:345px;width:540px;height:340px;--rot:3deg">
  <div class="sh" style="width:540px;height:340px"><div style="width:540px;height:340px;background:url({palm}) 50% 45%/cover;clip-path:{polyS}"></div></div>
  <div class="tape tp" id="t2" style="left:-30px;top:20px;width:120px;transform:rotate(-38deg)"></div>
  <div class="tape tp" id="t2b" style="right:-34px;bottom:22px;width:120px;transform:rotate(-38deg)"></div></div>

<div class="abs tp" id="t3" style="left:470px;top:668px;width:560px;height:50px;transform:rotate(-2deg);background:rgba(242,164,182,.9);mix-blend-mode:multiply;clip-path:polygon(0 0,100% 0,99% 30%,100% 55%,99% 80%,100% 100%,0 100%,1% 75%,0 50%,1% 25%)"><div class="eyebrow" style="font-size:16px;color:#500C02;line-height:50px;text-align:center;letter-spacing:.3em">porcelain · made in cairo</div></div>

<div class="abs it" id="e4" style="left:600px;top:800px;width:412px;height:412px;--rot:0deg">
  <div class="sh" style="width:412px;height:412px;border-radius:50%;background:#FDFBF6;padding:16px"><div style="width:380px;height:380px;border-radius:50%;background:url({pea}) center/cover"></div></div>
  <div class="tape tp" id="t4" style="left:140px;top:-20px;width:130px;transform:rotate(6deg)"></div></div>

{fan}
<div class="abs" style="left:176px;top:1260px;width:48px;height:48px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#e6c98a,#9b7a34);box-shadow:0 3px 6px rgba(0,0,0,.4)" id="rivet"></div>

<div class="abs it" id="e6" style="left:405px;top:1235px;width:236px;height:360px;--rot:9deg;transform-origin:118px 30px">
  <svg class="abs hand" style="left:60px;top:-120px;overflow:visible" width="120" height="150"><path d="M118 -10 C 90 40, 20 60, 58 148" style="stroke:#8a6a3a;stroke-width:3"/></svg>
  <div class="sh" style="width:236px;height:360px"><div style="width:236px;height:360px;background:#D8BF99;clip-path:polygon(24% 0,76% 0,100% 12%,100% 100%,0 100%,0 12%);position:relative">
    <div style="position:absolute;left:98px;top:30px;width:40px;height:40px;border-radius:50%;background:#EBDFCB;box-shadow:inset 0 2px 4px rgba(0,0,0,.35)"></div>
    <div class="script" style="position:absolute;left:0;right:0;top:120px;text-align:center;font-size:76px;line-height:.95;color:#500C02">set<br>of 24</div>
    <div class="eyebrow" style="position:absolute;left:0;right:0;top:296px;text-align:center;font-size:17px;color:#500C02;letter-spacing:.22em">6 · 6 · 6 · 6</div></div></div></div>

<div class="abs script wr" id="n1" style="left:84px;top:868px;font-size:60px;color:#8a2a1a;transform:rotate(-4deg)">look closer.</div>
<div class="abs script wr" id="n2" style="left:505px;top:722px;font-size:60px;color:#8a2a1a;transform:rotate(-2deg)">beaded.</div>
<div class="abs script wr" id="n3" style="left:660px;top:1232px;font-size:60px;color:#8a2a1a;transform:rotate(3deg)">brushstrokes.</div>
<div class="abs script wr" id="n4" style="left:700px;top:1330px;font-size:76px;color:#d4675b;transform:rotate(-4deg);line-height:.95;width:380px">a table<br>for six</div>
<svg class="abs hand wr" id="a4" style="left:0;top:0;overflow:visible" width="1080" height="1920"><path d="{squiggle(695,1362,650,1318,4,-18)}" style="stroke:#d4675b"/><path d="{arrowhead(650,1318,695,1362,seed=4)}" style="stroke:#d4675b"/></svg>

<div class="abs logo" id="lg" style="left:715px;top:1462px;width:290px;height:158px;background:#500C02"></div>

<div class="abs script" id="cta" style="left:70px;top:1690px;font-size:92px;line-height:1;color:#500C02">save it for later <span style="color:#d4675b">→</span></div>
<div class="abs eyebrow" id="url" style="left:76px;top:1815px;font-size:20px;color:#6E5A54">perset.shop</div>
'''
js="""
const STATIC=%STATIC%;
const el=id=>document.getElementById(id);
const items=[['e1',.9],['e2',1.7],['e4',3.2],['e6',5.6]];
const tapes=[['t1',1.45],['t2',2.25],['t2b',2.35],['t3',2.7],['t4',3.75]];
const notes=[['n1',6.5],['n2',7.0],['n3',7.5],['n4',8.0],['a4',8.5]];
const rots={e1:-5,e2:3,e4:0,e6:9};
window.setT=function(t){
  if(STATIC){t=99;}
  const ti=ease.out(seg(t,.15,.7)); el('title').style.opacity=ti; el('title').style.transform='translateY('+((1-ti)*30)+'px)';
  el('sub').style.opacity=ease.out(seg(t,.7,.5));
  items.forEach(([id,t0])=>{
    const p=seg(t,t0,id==='e6'?.1:.55); const e=el(id);
    if(id==='e6'){ // swing in on its string
      const dt=Math.max(0,t-t0); e.style.opacity=t>=t0?1:0;
      const r=9+(t>=t0?30*Math.exp(-3.6*dt)*Math.cos(8*dt):40);
      e.style.transform='rotate('+r+'deg)'; return;}
    const q=ease.out(p); const back=1-q;
    e.style.opacity=p>0?1:0;
    e.style.transform='translateY('+(-1500*back)+'px) rotate('+(rots[id]+(rots[id]>=0?22:-22)*back)+'deg) scale('+(1+0.05*Math.sin(p*Math.PI))+')';
  });
  tapes.forEach(([id,t0])=>{const e=el(id); const p=ease.out(seg(t,t0,.25)); e.style.opacity=p>0?1:0; e.style.clipPath=e.style.clipPath; e.style.transformOrigin='left center'; const base=e.style.transform.replace(/ scaleX\\([^)]*\\)/,''); e.style.transform=base+' scaleX('+(0.15+0.85*p)+')';});
  // chips fan
  const angs=[-26,-13,0,13,26];
  for(let i=0;i<5;i++){const p=ease.out(seg(t,4.1+i*.18,.5)); el('chip'+i).style.transform='rotate('+(angs[i]*p)+'deg)'; el('chip'+i).style.opacity=seg(t,4.1+i*.18,.1);}
  el('rivet').style.opacity=seg(t,4.0,.2);
  notes.forEach(([id,t0])=>{const e=el(id); const p=ease.io(seg(t,t0,.6)); e.style.clipPath='inset(-20px '+((1-p)*100)+'%% -20px -20px)'; e.style.opacity=p>0?1:0;});
  el('lg').style.opacity=ease.out(seg(t,8.9,.5));
  el('cta').style.opacity=ease.out(seg(t,9.4,.5)); el('url').style.opacity=ease.out(seg(t,9.9,.5));
  if(STATIC){el('title').style.opacity=0;el('sub').style.opacity=0;el('cta').style.opacity=0;el('url').style.opacity=0;}
};
window.setT(0);
"""
# initial hidden state css
css="""
.it,.chip,#rivet,.wr,#lg,#cta,#url,#title,#sub{opacity:0}
.tape.tp,#t3{opacity:0}
"""
for name,static in (('board',False),('board_static',True)):
    open(name+'.html','w').write(page(css,body,js.replace('%STATIC%','true' if static else 'false').replace('%%','%'),W=1080,H=1920,bgc='#EDE2CE'))
print('ok')
