import sys
from reel import *
PL=img(SCR+'/pack/assets/wild_hi.png')
OUT=os.path.abspath('../tw/st'); os.makedirs(OUT,exist_ok=True)
def render(name,css,body,js,dur,bgc='#F3D9D2'):
    d=f'{OUT}/{name}'; os.makedirs(d,exist_ok=True)
    open(f'{d}/p.html','w').write(page(css,body,js,W=1080,H=1920,bgc=bgc))
    run(f'cd "{d}" && VW=1080 VH=1920 {NODE} {SCR}/pack/render.js p.html fr {FPS} {dur} jpeg 0')
    run(f'{FF} -v error -y -framerate {FPS} -i "{d}/fr/f%04d.jpg" -vf "noise=alls=5:allf=t,format=yuv420p" -c:v libx264 -crf 18 -preset slow -movflags +faststart "{os.path.abspath("../tw/out")}/{name}.mp4"')
parasol='<svg viewBox="0 0 64 64" width="{s}" height="{s}"><path d="M6 30 Q32 2 58 30 Z" fill="#E7877F"/><path d="M6 30 Q12 36 19 30 Q25 36 32 30 Q39 36 45 30 Q52 36 58 30" fill="none" stroke="#C9A227" stroke-width="3"/><line x1="32" y1="30" x2="32" y2="58" stroke="#500C02" stroke-width="3"/><path d="M32 58 q-6 0 -6 -6" fill="none" stroke="#500C02" stroke-width="3"/></svg>'
which=sys.argv[1:] or ['weather','team','wheel']
# ---------------- 1. weather
if 'weather' in which:
    rows=[('12:00','2 parasols','per plate'),('13:00','12 leopards','at the table'),('14:30','90%','chance of seconds'),('16:00','low','UV, thanks to shade')]
    rh=''.join(f'<div class="r" id="r{i}"><div class="tm">{a}</div><div class="ic">{parasol.format(s=54)}</div><div class="v">{b}</div><div class="k">{c}</div></div>' for i,(a,b,c) in enumerate(rows))
    css=f"""
.bg{{background:linear-gradient(180deg,#F6B9B0 0%,#F8D7C4 45%,#F4EEE4 100%)!important}}.fibers{{opacity:.18}}
#loc{{position:absolute;left:0;right:0;top:150px;text-align:center;font-size:34px;letter-spacing:.28em;text-transform:uppercase;color:#500C02}}
#day{{position:absolute;left:0;right:0;top:205px;text-align:center;font-family:'Damion';font-size:96px;color:#500C02}}
#sun{{position:absolute;left:290px;top:360px;width:500px;height:500px;background:url({PL}) center/contain no-repeat;filter:drop-shadow(0 0 60px rgba(255,220,160,.9)) drop-shadow(0 24px 30px rgba(80,12,2,.25))}}
#tmp{{position:absolute;left:0;right:0;top:900px;text-align:center;font-family:'Fraunces';font-weight:300;font-size:190px;line-height:1;color:#500C02}}
#cond{{position:absolute;left:0;right:0;top:1100px;text-align:center;font-size:40px;color:#7a2a1a}}
#card{{position:absolute;left:70px;right:70px;top:1210px;background:rgba(251,248,242,.78);border-radius:34px;padding:26px 36px;box-shadow:0 12px 40px rgba(80,12,2,.12)}}
.r{{display:grid;grid-template-columns:150px 80px 1fr;grid-template-rows:auto auto;align-items:center;padding:14px 0;border-bottom:1px solid rgba(80,12,2,.12)}}
.r:last-child{{border:none}}.tm{{grid-row:1/3;font-size:32px;color:#7a5a48}}.ic{{grid-row:1/3}}.v{{font-size:40px;font-weight:500;color:#500C02}}.k{{font-size:24px;color:#7a5a48}}
#ft{{position:absolute;left:0;right:0;bottom:110px;text-align:center;font-size:22px;letter-spacing:.3em;text-transform:uppercase;color:#7a2a1a}}
"""
    body=f'<div id="loc">cairo · friday</div><div id="day">lunch forecast</div><div id="sun"></div><div id="tmp">100%</div><div id="cond">chance of leopards</div><div id="card">{rh}</div><div id="ft">stitches of the wild · perset.shop</div>'
    js="""window.setT=t=>{const o=(id,a,dy=30)=>{const e=document.getElementById(id),k=ease.out(seg(t,a,.6));e.style.opacity=k;e.style.transform=`translateY(${(1-k)*dy}px)`};
o('loc',.1);o('day',.3);const s=document.getElementById('sun');const k=ease.out(seg(t,.2,1.6));s.style.transform=`translateY(${(1-k)*700}px) rotate(${t*6}deg)`;s.style.opacity=seg(t,.2,.4);
o('tmp',1.4,40);o('cond',1.7);o('card',2.1,60);for(let i=0;i<4;i++)o('r'+i,2.4+i*.35,20);o('ft',3.6,10);};window.setT(0);"""
    render('wild-story-1-lunch-forecast',css,body,js,9.0)
# ---------------- 2. team left / team right
if 'team' in which:
    L=['orders dessert first','claims the parasol at 7 am','"on my way" (still home)']
    R=['arrives exactly on time','brings flowers, every time','finishes your fattoush']
    li=''.join(f'<li id="l{i}">{x}</li>' for i,x in enumerate(L)); ri=''.join(f'<li id="q{i}">{x}</li>' for i,x in enumerate(R))
    css=f"""
.bg{{background:#F2EBDD!important}}
#h{{position:absolute;left:0;right:0;top:150px;text-align:center;font-family:'Damion';font-size:104px;line-height:1;color:#500C02}}
#s{{position:absolute;left:0;right:0;top:390px;text-align:center;font-size:30px;letter-spacing:.06em;color:#7a2a1a}}
.half{{position:absolute;left:140px;top:470px;width:800px;height:800px;background:url({PL}) center/contain no-repeat;filter:drop-shadow(0 26px 30px rgba(60,35,20,.28))}}
#hl{{clip-path:inset(0 50% 0 0)}}#hr{{clip-path:inset(0 0 0 50%)}}
.team{{position:absolute;top:1290px;width:470px;font-size:34px;line-height:1.25;color:#2a1a16}}
.team h3{{font-family:'Damion';font-weight:400;font-size:76px;color:#500C02;margin-bottom:10px}}
.team ul{{list-style:none;padding:0;margin:0}}.team li{{padding:8px 0;border-bottom:1px dashed rgba(80,12,2,.25)}}
#tl{{left:56px}}#tr{{right:56px;text-align:right}}
#v{{position:absolute;left:0;right:0;bottom:120px;text-align:center;font-size:24px;letter-spacing:.3em;text-transform:uppercase;color:#7a2a1a}}
"""
    body=f'<div id="h">team left or<br>team right?</div><div id="s">same plate. very different leopards.</div><div class="half" id="hl"></div><div class="half" id="hr"></div><div class="team" id="tl"><h3>team left</h3><ul>{li}</ul></div><div class="team" id="tr"><h3>team right</h3><ul>{ri}</ul></div><div id="v">vote below · stitches of the wild</div>'
    js="""window.setT=t=>{const o=(id,a,dy=24)=>{const e=document.getElementById(id),k=ease.out(seg(t,a,.5));e.style.opacity=k;e.style.transform=`translateY(${(1-k)*dy}px)`};
o('h',.1);o('s',.5);const sp=ease.io(seg(t,1.2,.9))*(1-ease.io(seg(t,8.0,.8)));
document.getElementById('hl').style.transform=`translateX(${-90*sp}px) rotate(${-4*sp}deg)`;document.getElementById('hr').style.transform=`translateX(${90*sp}px) rotate(${4*sp}deg)`;
o('tl',1.9);o('tr',2.1);for(let i=0;i<3;i++){o('l'+i,2.4+i*.45,12);o('q'+i,2.6+i*.45,12);}o('v',4.2,10);};window.setT(0);"""
    render('wild-story-2-team-left-or-right',css,body,js,9.6)
# ---------------- 3. wheel
if 'wheel' in which:
    labels=['you','mama','your best friend','whoever has the balcony','the leopards','whoever has the plates']
    N=len(labels); win=5
    lab=''.join(f'<div class="lb" style="transform:rotate({i*360/N}deg) translateY(-470px)"><span>{x}</span></div>' for i,x in enumerate(labels))
    css=f"""
.bg{{background:radial-gradient(ellipse at 50% 45%,#F7C7C0,#E9A0A3 70%)!important}}
#h{{position:absolute;left:0;right:0;top:150px;text-align:center;font-family:'Damion';font-size:110px;line-height:1;color:#500C02}}
#wheel{{position:absolute;left:540px;top:1000px;width:0;height:0}}#rot{{position:absolute;left:0;top:0}}
#pl{{position:absolute;left:-380px;top:-380px;width:760px;height:760px;background:url({PL}) center/contain no-repeat;filter:drop-shadow(0 26px 30px rgba(80,12,2,.35))}}
.lb{{position:absolute;left:0;top:0;width:0;height:0}}
.lb span{{position:absolute;transform:translate(-50%,-50%);white-space:nowrap;font-size:30px;font-weight:500;color:#500C02;background:#FBF8F2;padding:8px 18px;border-radius:30px;box-shadow:0 4px 12px rgba(80,12,2,.15)}}
#ptr{{position:absolute;left:510px;top:430px;width:60px;height:80px}}
#res{{position:absolute;left:0;right:0;top:1580px;text-align:center;font-family:'Damion';font-size:92px;color:#500C02;line-height:1}}
#sub{{position:absolute;left:0;right:0;top:1690px;text-align:center;font-size:30px;color:#7a2a1a}}
#ft{{position:absolute;left:0;right:0;bottom:90px;text-align:center;font-size:22px;letter-spacing:.3em;text-transform:uppercase;color:#500C02}}
"""
    body=f'<div id="h">who hosts<br>this friday?</div><div id="wheel"><div id="rot">{lab}</div><div id="pl"></div></div><svg id="ptr" viewBox="0 0 60 80"><path d="M30 78 L6 12 Q30 -6 54 12 Z" fill="#500C02"/><circle cx="30" cy="22" r="8" fill="#F2A4B6"/></svg><div id="res">whoever has the plates.</div><div id="sub">(that could be you. perset.shop)</div><div id="ft">stitches of the wild · a set for six</div>'
    final=360*5+ (360-win*360/N)   # land label `win` under the pointer
    js=f"""window.setT=t=>{{const o=(id,a,dy=24)=>{{const e=document.getElementById(id),k=ease.out(seg(t,a,.5));e.style.opacity=k;e.style.transform=`translateY(${{(1-k)*dy}}px)`}};
o('h',.1);const u=seg(t,.8,5.2);const k=1-Math.pow(1-u,3.2);const ang={final}*k;
document.getElementById('rot').style.transform=`rotate(${{ang}}deg)`;document.getElementById('pl').style.transform=`rotate(${{1800*k}}deg)`;
const tick=Math.abs(Math.sin(ang*Math.PI/({360/N})))  ;document.getElementById('ptr').style.transform=`rotate(${{(1-u)*tick*-14}}deg)`;
o('res',6.2,30);o('sub',6.7,16);o('ft',7.0,8);}};window.setT(0);"""
    render('wild-story-3-who-hosts-friday',css,body,js,10.0)
