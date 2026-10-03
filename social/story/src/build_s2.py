from common import *
bgimg=b64('../../launch/worlds/w21.jpg')
rows=[
 ('ln c','logo'),
]
css="""
body{background:#2a0a04}
#bg{position:absolute;inset:-120px;background:url(data:image/jpeg;base64,%s) center/cover no-repeat;filter:blur(20px) brightness(.55) saturate(1.1)}
#bgs{position:absolute;inset:0;background:linear-gradient(180deg,rgba(40,8,2,.55),rgba(40,8,2,.15) 40%%,rgba(40,8,2,.55))}
#paper{position:absolute;left:130px;top:195px;width:820px;padding:64px 64px 70px;background:var(--paper);color:var(--ink);
  box-shadow:0 30px 60px rgba(0,0,0,.45);transform-origin:50%% 0}
#paper:after{content:'';position:absolute;left:0;right:0;bottom:-21px;height:22px;background:conic-gradient(from 135deg at 50%% 0,var(--paper) 90deg,transparent 0) 0 0/36px 22px repeat-x}
.ln{opacity:0;clip-path:inset(0 100%% 0 0)}
.c{text-align:center}
.logo{width:300px;height:163px;background:var(--ox);margin:0 auto}
.tag{font-size:24px;letter-spacing:.3em;text-transform:uppercase;color:#6E5A54;margin-top:8px}
.rule{border-top:3px dashed rgba(80,12,2,.4);margin:20px 0 16px}
.row{display:flex;align-items:baseline;gap:12px;font-size:36px;letter-spacing:.06em;text-transform:uppercase;font-weight:400;padding:7px 0;font-variant-numeric:tabular-nums}
.row .d{flex:1;border-bottom:3px dotted rgba(42,26,22,.45);transform:translateY(-6px)}
.row.sub{font-size:31px;padding:4px 0 4px 34px;color:#4a3630;font-weight:300}
.row.tot{font-size:44px;font-weight:500;padding-top:12px}
.row.tot .v{font-family:'Damion',cursive;text-transform:none;font-size:70px;letter-spacing:0;color:var(--ox);font-weight:400}
.thanks{font-family:'Damion',cursive;font-size:82px;line-height:1.02;text-align:center;color:var(--ox);margin-top:18px}
.bar{display:flex;gap:4px;justify-content:center;margin-top:26px;height:96px}
.bar i{display:block;background:var(--ink);height:100%%}
.url{text-align:center;font-size:23px;letter-spacing:.34em;text-transform:uppercase;margin-top:12px;color:#6E5A54}
#zone{height:230px;position:relative}
#stamp{position:absolute;left:50%%;top:60%%;padding:10px 30px;border:8px double #7a1a0c;color:#7a1a0c;font-size:92px;font-weight:500;letter-spacing:.08em;text-transform:uppercase;white-space:nowrap;
  transform:translate(-50%%,-50%%) rotate(-9deg) scale(2.6);opacity:0;mix-blend-mode:multiply;border-radius:10px;background:rgba(122,26,12,.04)}
""" % bgimg
bars=''.join(f'<i style="width:{w}px"></i>' for w in [4,2,6,3,2,5,2,8,3,2,4,6,2,3,5,2,7,3,2,4,2,6,3,5,2,4,8,2,3,6,2,4,3,5,2,7,3,2,5,4])
body=f"""
<div id="bg"></div><div id="bgs"></div>
<div id="paper">
 <div class="ln c" data-i="0"><div class="logo logo"></div></div>
 <div class="ln c tag" data-i="1">Porcelain tableware · Cairo</div>
 <div class="ln rule" data-i="2"></div>
 <div class="ln row" data-i="3"><span>Table for</span><span class="d"></span><span>6</span></div>
 <div class="ln row" data-i="4"><span>1 × Complete set</span><span class="d"></span><span>24 pcs</span></div>
 <div class="ln row sub" data-i="5"><span>6 dinner plates</span><span class="d"></span><span>27 cm</span></div>
 <div class="ln row sub" data-i="6"><span>6 dessert plates</span><span class="d"></span><span>21 cm</span></div>
 <div class="ln row sub" data-i="7"><span>6 salad plates</span><span class="d"></span><span>21 cm</span></div>
 <div class="ln row sub" data-i="8"><span>6 soup bowls</span><span class="d"></span><span>12 cm</span></div>
 <div class="ln rule" data-i="9"></div>
 <div class="ln row" data-i="10"><span>Packing</span><span class="d"></span><span>double-boxed</span></div>
 <div class="ln row" data-i="11"><span>Delivery</span><span class="d"></span><span>across Egypt</span></div>
 <div class="ln rule" data-i="12"></div>
 <div class="ln row tot" data-i="13"><span>Total</span><span class="d"></span><span class="v">one good table</span></div>
 <div class="ln thanks" data-i="14">thank you for<br>setting your table</div>
 <div id="zone"><div id="stamp" class="eyebrow">Open now</div></div>
 <div class="ln url" data-i="15">perset.shop</div>
</div>
"""
js="""
const paper=document.getElementById('paper'),bg=document.getElementById('bg'),stamp=document.getElementById('stamp');
const lines=[...document.querySelectorAll('.ln')];
const T0=1.1, STEP=0.2;
window.setT=function(t){
  const p=ease.out(seg(t,.15,.9));
  paper.style.transform='translateY('+((1-p)*1700)+'px) rotate('+(-1.4*p)+'deg)';
  bg.style.transform='scale('+(1.0+0.07*t/8)+')';
  lines.forEach((el,i)=>{
    const s=seg(t,T0+i*STEP,.16);
    el.style.opacity=s>0?1:0; el.style.clipPath='inset(0 '+((1-s)*100)+'% 0 0)';
  });
  const k=seg(t,6.6,.14);
  stamp.style.opacity=k>0?(0.9):0;
  const sc=2.6-1.6*ease.out(k);
  const sh=(t>6.74&&t<6.9)?Math.sin((t-6.74)*120)*5:0;
  stamp.style.transform='translate(calc(-50% + '+sh+'px),calc(-50% + '+sh+'px)) rotate(-9deg) scale('+sc+')';
};
window.setT(0);
"""
open('s2.html','w').write(page(css,body,js,bg='#2a0a04'))
print('s2 ok')
