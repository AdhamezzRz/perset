from wc import *
import subprocess
OUT=os.path.abspath('../ins/out')
PL=img(SCR+'/pack/assets/wild_hi.png')
def shoot(name,css,body,bgc):
    f=f'{OUT}/{name}.html'; open(f,'w').write(page(css,body,'',W=1080,H=1350,bgc=bgc,fibers=False))
    subprocess.run(f'cd {OUT} && NODE_PATH=$(npm root -g) node {SCR}/pack/shoot.js 1080 1350 {name}.html',shell=True,check=True)
# ---------- cinema poster
rays=''.join(f'<path d="M540 640 L{540+1400*np.cos(np.radians(a)):.0f} {640+1400*np.sin(np.radians(a)):.0f} L{540+1400*np.cos(np.radians(a+6)):.0f} {640+1400*np.sin(np.radians(a+6)):.0f} Z"/>' for a in range(0,360,12))
css=f"""
.bg{{background:#F1E2C4!important}}
#paper{{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 40%,rgba(255,250,235,.5),rgba(120,80,40,.18) 100%)}}
svg#rays{{position:absolute;left:0;top:0}} svg#rays path{{fill:#E8B04A;opacity:.55}}
#halo{{position:absolute;inset:0;background-image:radial-gradient(circle,rgba(160,40,20,.22) 1.4px,transparent 1.6px);background-size:9px 9px;mix-blend-mode:multiply;-webkit-mask:radial-gradient(circle at 50% 47%,transparent 30%,#000 70%)}}
#pl{{position:absolute;left:215px;top:340px;width:650px;height:650px;background:url({PL}) center/contain no-repeat;filter:drop-shadow(0 18px 0 rgba(120,20,10,.35)) contrast(1.05) saturate(1.05)}}
.top{{position:absolute;left:0;right:0;top:46px;text-align:center;font-weight:500;letter-spacing:.42em;font-size:20px;color:#7a1c10}}
#t1{{position:absolute;left:0;right:0;top:92px;text-align:center;font-family:'Fraunces';font-weight:700;font-style:italic;font-size:124px;line-height:.9;color:#C8261A;-webkit-text-stroke:3px #3a0a05;text-shadow:6px 6px 0 #E8B04A,9px 9px 0 #3a0a05;letter-spacing:-.01em}}
#cast{{position:absolute;left:60px;right:60px;top:1012px;text-align:center;color:#3a0a05}}
#cast .s{{font-size:20px;letter-spacing:.38em;font-weight:500}}
#cast .n{{font-family:'Fraunces';font-weight:700;font-size:44px;line-height:1.05;margin-top:6px}}
#cast .n i{{font-weight:400;font-size:30px}}
#tag{{position:absolute;left:0;right:0;top:1140px;text-align:center;font-family:'Damion';font-size:52px;color:#C8261A}}
#bill{{position:absolute;left:70px;right:70px;top:1215px;text-align:center;font-size:15px;letter-spacing:.14em;color:#5a2a1a;line-height:1.5;border-top:2px solid #3a0a05;padding-top:10px}}
#stamp{{position:absolute;right:52px;top:820px;width:190px;height:190px;border-radius:50%;background:#C8261A;color:#F1E2C4;display:flex;align-items:center;justify-content:center;text-align:center;font-weight:500;font-size:22px;letter-spacing:.12em;line-height:1.2;transform:rotate(-12deg);box-shadow:0 0 0 6px #F1E2C4,0 0 0 9px #C8261A}}
#fold{{position:absolute;inset:0;background:linear-gradient(90deg,transparent 49.6%,rgba(90,50,20,.18) 50%,transparent 50.4%),linear-gradient(0deg,transparent 49.7%,rgba(90,50,20,.14) 50%,transparent 50.3%)}}
#wear{{position:absolute;inset:0;box-shadow:inset 0 0 120px rgba(110,60,20,.45);}}
"""
body=f"""<div id="paper"></div><svg id="rays" width="1080" height="1350">{rays}</svg><div id="halo"></div><div id="pl"></div>
<div class="top">PER SET STUDIOS · CAIRO · PRESENT</div><div id="t1">THE TWO<br>LEOPARDS</div>
<div id="stamp">NOW<br>SHOWING<br>EVERY<br>FRIDAY</div>
<div id="cast"><div class="s">STARRING</div><div class="n">LEFT LEOPARD <i>and</i> RIGHT LEOPARD</div><div class="s" style="margin-top:8px">AND INTRODUCING THE PARASOLS</div></div>
<div id="tag">a story of friendship, shade and dinner for six.</div>
<div id="bill">STITCHES OF THE WILD · A 24-PIECE SET FOR SIX · PORCELAIN · IN COLOUR · ALL AGES · PERSET.SHOP</div><div id="fold"></div><div id="wear"></div>"""
shoot('wild-post-1-the-two-leopards',css,body,'#F1E2C4')
# ---------- dating profile
photo=img(SCR+'/src/wild-2-perset-wild-dinner-plate.jpg')
css=f"""
.bg{{background:linear-gradient(160deg,#F7D6D2,#F2EBDD)!important}}
#card{{position:absolute;left:90px;top:50px;width:900px;height:1120px;background:#FBF8F2;border-radius:40px;overflow:hidden;box-shadow:0 30px 60px rgba(80,12,2,.18)}}
#ph{{height:640px;background:#D9CBBE url({photo}) center/auto 100% no-repeat;position:relative}}
#ph:after{{content:'';position:absolute;left:0;right:0;bottom:0;height:260px;background:linear-gradient(transparent,rgba(30,10,6,.75))}}
#nm{{position:absolute;left:40px;bottom:30px;z-index:2;color:#FBF8F2}}
#nm .a{{font-family:'Fraunces';font-weight:600;font-size:66px;line-height:1}}#nm .b{{font-size:28px;margin-top:8px;opacity:.92}}
#dots{{position:absolute;left:40px;right:40px;top:18px;display:flex;gap:10px;z-index:2}}#dots i{{flex:1;height:6px;border-radius:3px;background:rgba(255,255,255,.45)}}#dots i:first-child{{background:#fff}}
#body{{padding:28px 40px}}
.chips{{display:flex;flex-wrap:wrap;gap:12px}}.chips span{{border:2px solid #E7B9B4;color:#7a2a1a;border-radius:30px;padding:8px 20px;font-size:26px}}
.q{{margin-top:22px}}.q .k{{font-size:22px;letter-spacing:.2em;text-transform:uppercase;color:#C9566B}}.q .v{{font-family:'Fraunces';font-size:40px;line-height:1.15;color:#2a1a16;margin-top:6px}}
#btn{{position:absolute;left:0;right:0;top:1196px;display:flex;justify-content:center;gap:90px}}
#btn div{{width:120px;height:120px;border-radius:50%;background:#FBF8F2;box-shadow:0 12px 26px rgba(80,12,2,.18);display:flex;align-items:center;justify-content:center}}
"""
body=f"""<div id="card"><div id="ph"><div id="dots"><i></i><i></i><i></i><i></i></div><div id="nm"><div class="a">Leo &amp; Leo, 2</div><div class="b">Zamalek · 0 km away · always together</div></div></div>
<div id="body"><div class="chips"><span>dinner parties</span><span>shade</span><span>stripes</span><span>bamboo</span><span>Fridays</span></div>
<div class="q"><div class="k">my love language</div><div class="v">holding the parasol for you.</div></div>
<div class="q"><div class="k">two truths and a lie</div><div class="v">we’re a pair · we’re porcelain · we share one parasol</div></div>
<div class="q"><div class="k">looking for</div><div class="v">a table for six. serious hosts only.</div></div></div></div>
<div id="btn"><div><svg width="50" height="50" viewBox="0 0 50 50"><path d="M12 12 L38 38 M38 12 L12 38" stroke="#8a6a5a" stroke-width="6" stroke-linecap="round"/></svg></div><div><svg width="60" height="56" viewBox="0 0 60 56"><path d="M30 52 C10 36 2 26 2 16 C2 7 9 2 16 2 C22 2 27 6 30 11 C33 6 38 2 44 2 C51 2 58 7 58 16 C58 26 50 36 30 52 Z" fill="#C9566B"/></svg></div></div>"""
shoot('wild-post-2-leo-and-leo',css,body,'#F2EBDD')
