from common import *
P={k:b64(f'../assets/{k}.png') for k in ['wild_dinner','beads_dinner','past_dinner']}
css="""
body{background:#500C02}
.bgl{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 38%,rgba(255,255,255,.07),rgba(0,0,0,0) 60%)}
#head{position:absolute;left:0;right:0;top:250px;text-align:center;color:#F2A4B6;font-family:'Damion',cursive;font-size:150px;line-height:1;white-space:nowrap;opacity:0}
.plate{position:absolute;width:330px;height:330px;opacity:0;filter:drop-shadow(0 24px 28px rgba(0,0,0,.5)) drop-shadow(0 3px 4px rgba(0,0,0,.4))}
.plate img{width:100%;height:100%;display:block}
.lab{position:absolute;width:560px;color:#F4EEE4;opacity:0}
.lab .t{font-family:'Damion',cursive;font-size:74px;line-height:1.02}
.lab .t b{font-weight:400;color:#F2A4B6;margin-right:14px}
.lab .s{font-size:22px;letter-spacing:.28em;text-transform:uppercase;color:#F2A4B6;margin-top:14px;line-height:1.5}
.lab.r{text-align:right}
#hint{position:absolute;left:0;right:0;top:1405px;text-align:center;color:#F4EEE4;font-family:'Damion',cursive;font-size:62px;opacity:0}
svg#arr{position:absolute;left:470px;top:1470px;overflow:visible;opacity:1}
svg#arr path{fill:none;stroke:#F2A4B6;stroke-width:6;stroke-linecap:round;stroke-linejoin:round}
"""
body=f"""
<div class="bgl"></div><div class="ticket top"></div><div class="ticket bot"></div>
<div id="head">Pick your plate.</div>
<div class="plate" id="p0" style="left:70px;top:440px"><img src="data:image/png;base64,{P['wild_dinner']}"></div>
<div class="plate" id="p1" style="left:680px;top:740px"><img src="data:image/png;base64,{P['beads_dinner']}"></div>
<div class="plate" id="p2" style="left:70px;top:1040px"><img src="data:image/png;base64,{P['past_dinner']}"></div>
<div class="lab" id="l0" style="left:470px;top:490px"><div class="t"><b>a.</b>Stitches<br>of the Wild</div><div class="s">leopards under<br>a pink parasol</div></div>
<div class="lab r" id="l1" style="left:70px;top:800px;width:570px"><div class="t"><b>b.</b>A Tale<br>in Beads</div><div class="s">a palm, built<br>bead by bead</div></div>
<div class="lab" id="l2" style="left:470px;top:1090px"><div class="t"><b>c.</b>Pretty<br>Past</div><div class="s">a peacock<br>among roses</div></div>
<div id="hint">which one is yours? tell us below</div>

"""
js="""
const head=document.getElementById('head'),hint=document.getElementById('hint');
const pl=[0,1,2].map(i=>document.getElementById('p'+i)),lb=[0,1,2].map(i=>document.getElementById('l'+i));
const T0=[0.7,1.5,2.3],SP=[26,-32,21],BASE=[-8,14,-5];
window.setT=function(t){
  const h=ease.out(seg(t,.2,.6)); head.style.opacity=h; head.style.transform='translateY('+((1-h)*40)+'px)';
  for(let i=0;i<3;i++){
    const s=seg(t,T0[i],.5), e=ease.out(s);
    pl[i].style.opacity=clamp(s*3);
    const drop=1.5-.5*e+(s>0.7&&s<1?0.05*Math.sin((s-.7)/.3*Math.PI):0);
    const rot=BASE[i]+SP[i]*Math.max(0,t-T0[i])+(1-e)*-40;
    pl[i].style.transform='scale('+drop+') rotate('+rot+'deg)';
    const ls=ease.out(seg(t,T0[i]+.45,.5)); lb[i].style.opacity=ls;
    lb[i].style.transform='translateY('+((1-ls)*26)+'px)';
  }
  hint.style.opacity=ease.out(seg(t,3.5,.5));
};
window.setT(0);
"""
open('s3.html','w').write(page(css,body,js,bg='#500C02'))
print('s3 ok')
