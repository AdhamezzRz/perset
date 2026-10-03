from common import *
css="""
#shutter{position:absolute;left:0;top:0;width:1080px;height:1920px;will-change:transform;
  background:repeating-linear-gradient(180deg,#7a2314 0,#7a2314 2px,#5c1306 2px,#500C02 22px,#470a02 50px,#2b0400 53px,#2b0400 56px);
  box-shadow:0 40px 70px rgba(0,0,0,.5)}
#shutter .sheen{position:absolute;inset:0;background:linear-gradient(90deg,rgba(0,0,0,.28),rgba(255,255,255,.05) 18%,rgba(255,255,255,0) 50%,rgba(0,0,0,.12) 100%)}
#shutter .rail{position:absolute;left:0;right:0;bottom:0;height:64px;background:linear-gradient(180deg,#f7b6c5,#F2A4B6 40%,#d98a9d);box-shadow:0 -6px 14px rgba(0,0,0,.35)}
#shutter .rail:after{content:'';position:absolute;left:50%;top:18px;width:160px;height:26px;margin-left:-80px;border-radius:14px;background:#3a0a03;box-shadow:inset 0 3px 6px rgba(0,0,0,.7)}
#shutter .logo{position:absolute;left:190px;top:560px;width:700px;height:380px;background:#F2A4B6}
#shutter .eb{position:absolute;left:0;right:0;top:960px;text-align:center;color:#F2A4B6;font-size:30px;opacity:.9}
#shutter .note{position:absolute;left:230px;top:1130px;width:620px;padding:42px 40px 46px;background:#FBF8F2;color:#500C02;transform:rotate(-3deg);box-shadow:0 14px 30px rgba(0,0,0,.4);text-align:center}
#shutter .note .s{font-family:'Damion',cursive;font-size:70px;line-height:1.02}
#shutter .note .tape{position:absolute;top:-20px;width:150px;height:46px;background:rgba(242,164,182,.82)}
#shutter .note .tape.l{left:-34px;transform:rotate(-28deg)} #shutter .note .tape.r{right:-34px;transform:rotate(28deg)}
#hous{position:absolute;left:0;right:0;top:0;height:140px;background:linear-gradient(180deg,rgba(24,4,0,.85),rgba(24,4,0,0));opacity:0}
#scrim{position:absolute;left:0;right:0;bottom:0;height:1100px;background:linear-gradient(0deg,rgba(80,12,2,.86) 0%,rgba(80,12,2,.5) 45%,rgba(80,12,2,0) 100%);opacity:0}
#h1{position:absolute;left:0;right:0;top:1180px;text-align:center;color:#F4EEE4;font-family:'Damion',cursive;font-size:230px;line-height:1;text-shadow:0 4px 30px rgba(30,5,0,.55);opacity:0}
#h1 i{font-style:normal;color:#F2A4B6}
#url{position:absolute;left:0;right:0;top:1445px;text-align:center;color:#F4EEE4;font-size:32px;opacity:0;text-shadow:0 2px 16px rgba(30,5,0,.6)}
"""
body="""
<div id="hous"></div><div id="scrim"></div>
<div id="h1">We&#8217;re <i>open.</i></div><div id="url" class="eyebrow">perset.shop</div>
<div id="shutter"><div class="sheen"></div><div class="logo logo"></div><div class="eb eyebrow">Opening day</div>
 <div class="note"><div class="tape l"></div><div class="tape r"></div><div class="s">back in a minute,<br>setting the table</div></div>
 <div class="rail"></div></div>
"""
js="""
const sh=document.getElementById('shutter'),hous=document.getElementById('hous'),scrim=document.getElementById('scrim'),h1=document.getElementById('h1'),url=document.getElementById('url');
window.setT=function(t){
  let y=0,x=0;
  if(t>.3&&t<.6) x=4*Math.sin(t*80)*(1-(t-.3)/.3);
  if(t>=.6&&t<.85) y=26*Math.sin((t-.6)/.25*Math.PI);
  if(t>=.85) y=-(1920+120)*ease.io(seg(t,.85,1.7));
  sh.style.transform='translate('+x+'px,'+y+'px)';
  hous.style.opacity=clamp(ease.io(seg(t,.85,1.7))*4);
  scrim.style.opacity=ease.out(seg(t,2.6,.9));
  const a=ease.out(seg(t,2.8,.7)); h1.style.opacity=a; h1.style.transform='translateY('+((1-a)*50)+'px) scale('+(0.96+0.04*a)+')';
  const b=ease.out(seg(t,3.6,.6)); url.style.opacity=b;
};
window.setT(0);
"""
open('s1_overlay.html','w').write(page(css,body,js))
print('s1 ok')
