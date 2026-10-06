import sys; sys.path.insert(0,'..')
from common import *
plate=img('../assets/wild_hi.png')
# plate drawn at 940px diameter, centred at (540, 830) at zoom 1.
D=900; PX,PY=540,935
# focus points in plate-relative coords (0..1) -- measured on the cutout
FOC=[
 ('01','the parasols','pink and gold, threaded',(0.285,0.285),2.9, 'left'),
 ('02','the leopards','a stitched-look coat, dot by dot',(0.34,0.58),2.9,'right'),
 ('03','the bamboo','five stalks in forest green',(0.52,0.46),2.7,'left'),
 ('04','the stripe','coral and white, edge to edge',(0.14,0.45),2.4,'right'),
 ('05','the border','a rim of tiny stitches',(0.14,0.80),3.2,'left'),
]
cards=''.join(f'''<div class="card" id="c{i}"><div class="no">{n}</div><div class="nm script">{t}</div><div class="sb">{s}</div></div>''' for i,(n,t,s,_,_,_) in enumerate(FOC))
focjs=str([[f[3][0],f[3][1],f[4]] for f in FOC])
css="""
#world{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:0 0}
#plate{position:absolute;filter:drop-shadow(0 26px 30px rgba(60,35,20,.4)) drop-shadow(0 3px 5px rgba(60,35,20,.4))}
#plate img{width:100%;height:100%;display:block}
#ring{position:absolute;left:540px;top:760px;width:420px;height:420px;margin:-210px 0 0 -210px;opacity:0}
#ring circle{fill:none;stroke:#500C02;stroke-width:5;stroke-linecap:round;stroke-dasharray:8 14}
#title{position:absolute;left:0;right:0;top:130px;text-align:center;color:#500C02}
#title .a{font-family:'Damion',cursive;font-size:150px;line-height:.95}
#title .b{font-size:23px;letter-spacing:.34em;text-transform:uppercase;margin-top:14px;color:#6E5A54}
.card{position:absolute;left:70px;right:70px;top:1290px;opacity:0;background:#FBF8F2;padding:30px 40px 34px;box-shadow:0 14px 26px rgba(60,35,20,.3)}
.card .no{font-size:22px;letter-spacing:.3em;color:#8a2a1a}
.card .nm{font-size:92px;line-height:1.02;color:#500C02;margin-top:4px}
.card .sb{font-size:28px;color:#6E5A54;margin-top:2px}
#tape{position:absolute;left:470px;top:1398px;width:140px;opacity:0}
#end{position:absolute;left:0;right:0;top:1490px;text-align:center;opacity:0;color:#500C02}
#end .l{font-family:'Damion',cursive;font-size:84px}
#end .u{font-size:22px;letter-spacing:.34em;text-transform:uppercase;margin-top:6px;color:#6E5A54}
#eb{position:absolute;left:0;right:0;top:1560px;text-align:center;color:#6E5A54;opacity:0;font-size:21px;letter-spacing:.3em;text-transform:uppercase}
"""
body=f'''
<div id="world"><div id="plate" style="left:{PX-D/2}px;top:{PY-D/2}px;width:{D}px;height:{D}px"><img src="{plate}"></div></div>
<div id="title"><div class="a">anatomy of<br>a plate</div><div class="b">stitches of the wild · 27 cm</div></div>
<svg id="ring" viewBox="0 0 420 420"><circle cx="210" cy="210" r="196"/></svg>
{cards}<div class="tape" id="tape"></div>
<div id="eb">swipe through the set →</div>
<div id="end"><div class="l">five details, one plate.</div><div class="u">perset.shop</div></div>
'''
js=f"""
const FOC={focjs}, D={D}, PX={PX}, PY={PY};
const world=document.getElementById('world'), ring=document.getElementById('ring'), title=document.getElementById('title'), tape=document.getElementById('tape'), end=document.getElementById('end');
const cards=[...document.querySelectorAll('.card')];
const T=[[1.6,3.4],[3.4,5.2],[5.2,7.0],[7.0,8.8],[8.8,10.6]];
function view(t){{
  // returns scale and focus point in world px
  let s=1,fx=PX,fy=PY;
  for(let i=0;i<5;i++){{
    const [a,b]=T[i]; const f=FOC[i]; const tx=PX-D/2+f[0]*D, ty=PY-D/2+f[1]*D;
    const inn=ease.io(seg(t,a-.45,.9)), out=ease.io(seg(t,b-.45,.9));
    if(t>=a-.45 && t<b+.5){{
      const w=inn*(1-(i<4?0:0)); 
      const prevS=s, prevX=fx, prevY=fy;
      const k=inn; s=prevS+(f[2]-prevS)*k; fx=prevX+(tx-prevX)*k; fy=prevY+(ty-prevY)*k;
    }}
  }}
  // pull back at the end
  const back=ease.io(seg(t,10.4,1.1)); s=s+(1-s)*back; fx=fx+(PX-fx)*back; fy=fy+(PY-fy)*back;
  return [s,fx,fy];
}}
window.setT=function(t){{
  const [s,fx,fy]=view(t);
  // keep the focus point at screen centre-top area (540, 760)
  const cxs=540, cys=(s>1.05?760:935);
  const tx=cxs-s*fx, ty=cys-s*fy;
  world.style.transform='translate('+tx+'px,'+ty+'px) scale('+s+')';
  // subtle plate rotation drift at start
  const intro=ease.out(seg(t,0,1.2));
  document.getElementById('plate').style.transform='rotate('+((1-intro)*-14)+'deg) scale('+(0.88+0.12*intro)+')';
  document.getElementById('plate').style.opacity=clamp(t/.5);
  title.style.opacity=ease.out(seg(t,.3,.7))*(1-ease.out(seg(t,1.5,.5)));
  title.style.transform='translateY('+((1-ease.out(seg(t,.3,.7)))*30)+'px)';
  // ring
  let ro=0; for(let i=0;i<5;i++){{const [a,b]=T[i]; ro=Math.max(ro, seg(t,a,.35)*(1-seg(t,b-.3,.3)));}}
  ring.style.opacity=ro; ring.style.transform='scale('+(1.12-0.12*ro)+') rotate('+(t*14)+'deg)';
  ring.style.top=(760)+'px';
  // cards
  for(let i=0;i<5;i++){{const [a,b]=T[i]; const p=ease.out(seg(t,a+.1,.45))*(1-ease.out(seg(t,b-.25,.25)));
    cards[i].style.opacity=p; cards[i].style.transform='translateY('+((1-p)*40)+'px) rotate('+(i%2?1.2:-1.2)+'deg)';}}
  tape.style.opacity=0;
  end.style.opacity=ease.out(seg(t,10.9,.6)); document.getElementById('eb').style.opacity=0;
}};
window.setT(0);
"""
open('r2.html','w').write(page(css,body,js,W=1080,H=1920,bgc='#EDE2CE'))
print('ok')
