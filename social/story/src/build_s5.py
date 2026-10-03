from common import *
css="""
body{background:#500C02}
.bgl{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 30%,rgba(255,255,255,.07),rgba(0,0,0,0) 60%)}
#h{position:absolute;left:0;right:0;top:300px;text-align:center;color:#F4EEE4;font-family:'Damion',cursive;font-size:220px;line-height:.98}
#h i{font-style:normal;color:#F2A4B6}
#h span{display:block;opacity:0}
#sub{position:absolute;left:0;right:0;top:770px;text-align:center;color:#F2A4B6;font-size:27px;line-height:1.7;opacity:0}
svg#arr{position:absolute;left:400px;top:900px;overflow:visible}
svg#arr path{fill:none;stroke:#F2A4B6;stroke-width:7;stroke-linecap:round;stroke-linejoin:round}
.logo{position:absolute;left:310px;top:1390px;width:460px;height:250px;background:#F2A4B6;opacity:0}
"""
body="""<div class="bgl"></div><div class="ticket top"></div><div class="ticket bot"></div>
<div id="h"><span id="a">Set your</span><span id="b"><i>table.</i></span></div>
<div id="sub" class="eyebrow">Three collections<br>Each a complete set for six</div>
<svg id="arr" width="280" height="260" viewBox="0 0 280 260"><path id="arrp" d="M40 10 C 190 20, 250 90, 170 150 C 130 180, 110 200, 140 236 M140 236 l-30 -14 M140 236 l-4 -34"/></svg>
<div class="logo"></div>"""
js="""
const a=document.getElementById('a'),b=document.getElementById('b'),sub=document.getElementById('sub'),arr=document.getElementById('arrp'),lg=document.querySelector('.logo');
const L=arr.getTotalLength(); arr.style.strokeDasharray=L;
window.setT=function(t){
  const x=ease.out(seg(t,.3,.6)); a.style.opacity=x; a.style.transform='translateY('+((1-x)*50)+'px)';
  const y=ease.out(seg(t,.8,.6)); b.style.opacity=y; b.style.transform='translateY('+((1-y)*50)+'px)';
  sub.style.opacity=ease.out(seg(t,1.5,.6));
  arr.style.strokeDashoffset=L*(1-ease.io(seg(t,2.0,1.0)));
  lg.style.opacity=ease.out(seg(t,2.6,.6));
};
window.setT(0);
"""
open('s5.html','w').write(page(css,body,js,bg='#500C02'))
print('s5 ok')
