from common import *
css="""
#scrim{position:absolute;left:0;right:0;top:0;height:1050px;background:linear-gradient(180deg,rgba(80,12,2,.92) 0%,rgba(80,12,2,.8) 55%,rgba(80,12,2,0) 100%);opacity:0}
#h{position:absolute;left:70px;right:70px;top:270px;color:#F4EEE4;font-family:'Damion',cursive;font-size:190px;line-height:.96;text-shadow:0 4px 28px rgba(30,5,0,.5)}
#h i{font-style:normal;color:#F2A4B6}
#h span{display:block;opacity:0}
#sub{position:absolute;left:74px;top:672px;color:#F2A4B6;font-size:27px;opacity:0;text-shadow:0 2px 14px rgba(30,5,0,.6)}
"""
body="""<div id="scrim"></div><div id="h"><span id="a">Saved you</span><span id="b"><i>a seat.</i></span></div>
<div id="sub" class="eyebrow">Pretty Past · Dinner plate, 27 cm</div>"""
js="""
const sc=document.getElementById('scrim'),a=document.getElementById('a'),b=document.getElementById('b'),sub=document.getElementById('sub');
window.setT=function(t){
  sc.style.opacity=ease.out(seg(t,.2,.7));
  const x=ease.out(seg(t,.5,.6)); a.style.opacity=x; a.style.transform='translateY('+((1-x)*44)+'px)';
  const y=ease.out(seg(t,1.0,.6)); b.style.opacity=y; b.style.transform='translateY('+((1-y)*44)+'px)';
  sub.style.opacity=ease.out(seg(t,1.8,.6));
};
window.setT(0);
"""
open('s4_overlay.html','w').write(page(css,body,js))
print('s4 ok')
