from reel import *
import math
OUT=os.path.abspath('../ins/out'); d=os.path.abspath('../ins/vhs'); os.makedirs(d,exist_ok=True)
PL=img(SCR+'/cutouts/past_dinner.png'); SL=img(SCR+'/salad/salad_cut.png'); PH=img(SCR+'/src/past-1-perset-past-dinner-hero.jpg')
DUR=16.0
css=f"""
html,body{{width:1080px;height:1920px;overflow:hidden}}.vig,.grain,.fibers{{display:none}}
#blue{{position:absolute;inset:0;background:#1630C8}}
#sun{{position:absolute;left:-600px;top:-200px;width:2280px;height:2280px;border-radius:50%}}
.pl{{position:absolute;width:820px;height:820px;left:130px;top:620px;background:url({PL}) center/contain no-repeat;filter:drop-shadow(14px 18px 0 rgba(40,10,40,.35))}}
#sl{{position:absolute;width:560px;height:560px;background:url({SL}) center/contain no-repeat;filter:drop-shadow(12px 14px 0 rgba(40,10,40,.35))}}
.chrome{{position:absolute;left:0;right:0;text-align:center;font-family:'Fraunces';font-weight:900;font-style:italic;line-height:.9;
 background:linear-gradient(180deg,#ffffff 0%,#bfe6ff 38%,#2a3a8a 50%,#ffcf6a 56%,#fff6d8 100%);-webkit-background-clip:text;color:transparent;
 -webkit-text-stroke:3px #1a0c30;filter:drop-shadow(8px 8px 0 #E8467C) drop-shadow(3px 3px 0 #1a0c30)}}
.blk{{position:absolute;left:0;right:0;text-align:center;font-family:'Inter';font-weight:900;color:#FFF34A;-webkit-text-stroke:4px #1a0c30;
 text-shadow:8px 8px 0 #1a0c30;letter-spacing:-.01em;line-height:.95}}
#new{{position:absolute;left:720px;top:520px;width:300px;height:300px}}
.osd{{position:absolute;font-family:'JetBrains Mono';font-weight:800;color:#fff;font-size:54px;text-shadow:3px 3px 0 rgba(0,0,0,.6)}}
.sm{{position:absolute;left:60px;right:60px;text-align:center;font-family:'Inter';font-weight:600;color:#fff;font-size:28px;text-shadow:2px 2px 0 #1a0c30}}
.tw{{position:absolute;font-size:70px;color:#fff;text-shadow:0 0 18px #fff}}
#clean{{position:absolute;inset:0;background:#F4EFE4}}
#cph{{position:absolute;left:60px;top:430px;width:960px;height:960px;background:url({PH}) center/cover}}
.scr{{position:absolute;left:0;right:0;text-align:center;font-family:'Damion';color:#500C02;line-height:1}}
.cap{{position:absolute;left:0;right:0;text-align:center;font-family:'Jost';font-weight:500;letter-spacing:.3em;text-transform:uppercase;font-size:24px;color:#500C02}}
"""
star=''.join(f'{"L" if i else "M"}{150+(140 if i%2==0 else 100)*math.cos(math.pi*i/12):.1f} {150+(140 if i%2==0 else 100)*math.sin(math.pi*i/12):.1f} ' for i in range(24))+'Z'
body=f"""<div id="blue"></div><div id="sun"></div>
<div class="pl" id="pl"></div><div id="sl"></div>
<svg id="new" viewBox="0 0 300 300"><path d="{star}" fill="#FFF34A" stroke="#1a0c30" stroke-width="6"/><text x="150" y="172" text-anchor="middle" font-family="Inter" font-weight="900" font-size="72" fill="#E8467C" stroke="#1a0c30" stroke-width="3">NEW!</text></svg>
<div class="chrome" id="title" style="top:200px;font-size:190px">PRETTY<br>PAST</div>
<div class="blk" id="k1" style="top:250px;font-size:130px">IT’S A<br>PLATE!</div>
<div class="blk" id="k2" style="top:250px;font-size:130px">IT’S A<br>PEACOCK!</div>
<div class="blk" id="k3" style="top:250px;font-size:150px;color:#7CF2FF">IT’S<br>BOTH!!</div>
<div class="blk" id="k4" style="top:230px;font-size:96px">NOW WITH<br>MATCHING<br>SALAD PLATES!</div>
<div class="blk" id="k5" style="top:1480px;font-size:150px">24 PIECES!</div>
<div class="blk" id="k6" style="top:1640px;font-size:110px;color:#7CF2FF">SERVES SIX!</div>
<div class="sm" id="k7" style="top:1790px">(or one very hungry uncle)</div>
<div id="end" style="position:absolute;inset:0">
 <div class="blk" style="top:300px;font-size:84px;color:#fff">AVAILABLE NOW AT</div>
 <div class="chrome" style="top:420px;font-size:150px">perset.shop</div>
 <div class="blk" style="top:1390px;font-size:96px"><s style="text-decoration-thickness:12px;text-decoration-color:#E8467C">CALL NOW!</s></div>
 <div class="blk" id="click" style="top:1500px;font-size:120px;color:#7CF2FF">CLICK NOW!</div>
 <div class="sm" style="top:1650px;font-size:24px">*the peacock does not actually spin. please do not spin your plates.<br>results at dinner may vary. 24-piece set for six.</div></div>
<div class="tw" id="t1" style="left:150px;top:640px">✦</div><div class="tw" id="t2" style="left:880px;top:1300px">✦</div><div class="tw" id="t3" style="left:900px;top:700px;font-size:50px">✦</div>
<div class="osd" id="play" style="left:70px;top:90px">PLAY ▶</div><div class="osd" id="sp" style="right:70px;top:90px">SP</div>
<div class="osd" id="date" style="left:70px;bottom:60px;font-size:44px">JAN.14 1987<br>PM 8:42</div>
<div id="clean"><div id="cph"></div><div class="scr" style="top:170px;font-size:120px">some things<br>come back.</div>
 <div class="cap" style="top:1450px">pretty past · 2026</div><div class="cap" style="top:1500px;letter-spacing:.2em;font-size:22px;opacity:.75">a 24-piece set for six · perset.shop</div></div>"""
js="""
const $=id=>document.getElementById(id);
const vis=(id,a,b)=>{const e=$(id);const on=T>=a&&T<b;e.style.display=on?'block':'none';return on};
let T=0;
const BGS=[[1.0,'#E8467C','#FFB23A'],[4.0,'#E8467C','#FFF34A'],[4.8,'#2CB5A0','#7CF2FF'],[5.6,'#6B2D7A','#FFB23A'],[6.4,'#FFB23A','#E8467C'],[8.8,'#2C4FD8','#7CF2FF'],[11.0,'#E8467C','#6B2D7A']];
window.setT=t=>{T=t;
 vis('blue',0,1.0);
 let c=BGS[0];for(const b of BGS) if(t>=b[0]) c=b;
 const s=$('sun'); s.style.display=t>=1.0&&t<12.8?'block':'none';
 s.style.background=`repeating-conic-gradient(from ${t*18}deg,${c[1]} 0deg 10deg,${c[2]} 10deg 20deg)`;
 // plate: keyframed centre (cx,cy) and scale, eased between phases
 const K=[[0,540,1030,1],[6.4,290,1100,.6],[8.8,290,1000,.6],[11.0,540,960,.78]];
 let cx=540,cy=1030,k=1;
 for(let i=1;i<K.length;i++){const e=ease.io(seg(t,K[i][0],.55));cx+=(K[i][1]-cx)*e;cy+=(K[i][2]-cy)*e;k+=(K[i][3]-k)*e;}
 const p=$('pl'); p.style.display=t>=1.0&&t<12.8?'block':'none';
 const pin=ease.back(seg(t,1.0,.6));
 p.style.transform=`translate(${cx-540}px,${cy-1030}px) scale(${k*pin}) rotate(${t*95}deg)`;
 const sl=$('sl'); sl.style.display=t>=6.4&&t<11.0?'block':'none';
 const si=ease.out(seg(t,6.6,.6)); const sy=850-100*ease.io(seg(t,8.8,.55));
 sl.style.width=sl.style.height='500px'; sl.style.left=(1200-(1200-556)*si)+'px'; sl.style.top=sy+'px'; sl.style.transform=`rotate(${-t*80}deg)`;
 const ti=$('title'); vis('title',1.4,4.0); ti.style.transform=`scale(${0.2+0.8*ease.back(seg(t,1.4,.45))}) rotate(${-4+2*Math.sin(t*6)}deg)`;
 const nw=$('new'); nw.style.display=t>=2.2&&t<4.0?'block':'none'; nw.style.transform=`scale(${ease.back(seg(t,2.2,.35))*(1+0.06*Math.sin(t*14))}) rotate(${t*30}deg)`;
 [['k1',4.0,4.8],['k2',4.8,5.6],['k3',5.6,6.4],['k4',6.6,8.8]].forEach(([id,a,b])=>{if(vis(id,a,b)) $(id).style.transform=`scale(${0.6+0.4*ease.back(seg(t,a,.25))})`});
 [['k5',8.9,11.0],['k6',9.6,11.0],['k7',10.2,11.0]].forEach(([id,a,b])=>{if(vis(id,a,b)) $(id).style.transform=`scale(${0.5+0.5*ease.back(seg(t,a,.3))})`});
 vis('end',11.0,12.8); $('click').style.opacity=(Math.floor(t*4)%2)?1:.55;
 ['t1','t2','t3'].forEach((id,i)=>{const e=$(id);e.style.display=t>=1.2&&t<11?'block':'none';e.style.transform=`scale(${Math.max(0,Math.sin(t*5+i*2))}) rotate(${t*90}deg)`});
 const osd=t<12.8; $('play').style.display=osd&&t<2.5?'block':'none'; $('sp').style.display=osd?'block':'none'; $('date').style.display=osd?'block':'none';
 const cl=$('clean'); cl.style.display=t>=12.8?'block':'none'; $('cph').style.transform=`scale(${1+0.04*seg(t,12.8,3.2)})`;
};window.setT(0);"""
open(f'{d}/p.html','w').write(page(css,body,js,W=1080,H=1920,bgc='#000',fibers=False))
run(f'cd "{d}" && VW=1080 VH=1920 {NODE} {SCR}/pack/render.js p.html fr {FPS} {DUR} jpeg 0')
print('rendered')
