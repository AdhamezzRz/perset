from wc import *
import json
leg=json.load(open('st/legend.json'))
names=['stripe pink','bone white','shell','leopard gold','bamboo sage','parasol rose','deep olive','ochre spots','spot brown']
names=['bone white','stripe pink','shell','leopard spots','bamboo sage','blush','deep olive','parasol rose','leopard gold']
lg=''.join(f'<div class="li"><span class="sw" style="background:rgb({int(l["rgb"][0]*.82+255*.18)},{int(l["rgb"][1]*.82+255*.18)},{int(l["rgb"][2]*.82+255*.18)})">{l["sym"]}</span>{n}</div>' for l,n in zip(leg,names))
css=f"""
.paper{{position:absolute;left:46px;top:58px;width:720px;height:985px;background:#FCFAF5;transform:rotate(-2.2deg);padding:38px 44px;box-shadow:0 18px 30px rgba(60,35,20,.22),0 2px 4px rgba(60,35,20,.25)}}
.paper:after{{content:'';position:absolute;inset:0;background:linear-gradient(115deg,rgba(255,255,255,0) 40%,rgba(120,90,60,.06) 70%,rgba(255,255,255,0) 90%)}}
.eb{{font-size:15px;letter-spacing:.32em;text-transform:uppercase;color:#8a2a1a}}
.ti{{font-family:'Fraunces',serif;font-size:50px;line-height:1;color:#500C02;margin-top:8px;font-variation-settings:'SOFT' 100,'opsz' 144;font-style:italic}}
.su{{font-family:'Caveat',cursive;font-size:30px;color:#6b4a3a;margin-top:2px}}
.ch{{width:560px;height:560px;margin:18px 0 0 36px;background:url({img('st/chart.png')}) center/contain no-repeat}}
.lg{{display:grid;grid-template-columns:1fr 1fr;gap:6px 22px;margin-top:22px;font-size:17px;color:#3a2a22}}
.li{{display:flex;align-items:center;gap:10px}}
.sw{{width:24px;height:24px;border:1px solid rgba(60,40,30,.35);display:flex;align-items:center;justify-content:center;font-size:14px;color:#2a1a16}}
.ft{{margin-top:18px;font-size:14px;letter-spacing:.18em;text-transform:uppercase;color:#7a6658;border-top:1px solid rgba(80,12,2,.2);padding-top:12px;display:flex;justify-content:space-between}}
.plate{{position:absolute;left:600px;top:812px;width:510px;height:510px;background:url({img(SCR+'/pack/assets/wild_hi.png')}) center/contain no-repeat;filter:drop-shadow(0 22px 26px rgba(60,35,20,.35)) drop-shadow(0 3px 4px rgba(60,35,20,.35))}}
.needle{{position:absolute;left:470px;top:150px;width:560px;height:336px;background:url({img('a/needle.png')}) center/contain no-repeat;transform:rotate(18deg);filter:drop-shadow(0 6px 5px rgba(60,35,20,.28))}}
.note{{position:absolute;font-family:'Caveat',cursive;color:#500C02;line-height:1}}
"""
body=f"""<div class="paper"><div class="eb">pattern nº 01 · cross-stitch</div><div class="ti">Stitches of the Wild</div>
<div class="su">two leopards, two parasols, one bamboo. 64 × 64 stitches.</div>
<div class="ch"></div><div class="lg">{lg}</div>
<div class="ft"><span>difficulty: high · time: about 40 hours</span></div></div>
<div class="needle"></div>
<div class="plate"></div>
<div class="note" style="left:806px;top:520px;font-size:54px;transform:rotate(-6deg);width:250px">or… skip<br>the 40 hours.</div>
<svg class="hand abs" width="1080" height="1350" style="left:0;top:0"><path d="{squiggle(905,640,872,800,3,-30)}"/><path d="{arrowhead(872,800,905,640,22,3)}"/></svg>
<div class="note" style="left:70px;top:1150px;color:#500C02;font-family:Damion;font-size:64px;transform:rotate(-3deg)">Pattern included.<br><span style="font-size:40px;color:#8a2a1a">Needle optional.</span></div>
"""
open('out/w_s2_pattern.html','w').write(page(css,body,'',W=1080,H=1350,bgc='#EBDCCB'))
