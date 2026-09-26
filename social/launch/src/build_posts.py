import base64
def b64(p): return base64.b64encode(open(p,'rb').read()).decode()
logo=b64('../src/perset-logo-mask.png')
css=open('fonts_embedded.css').read()
BASE="""<!doctype html><html><head><meta charset="utf-8"><style>
%s
:root{--linen:#F4EEE4;--ox:#500C02;--blush:#F2A4B6;--ink:#2A1A16}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px;overflow:hidden;background:var(--linen)}
body{font-family:'Jost',sans-serif;color:var(--ink);position:relative}
.script{font-family:'Damion',cursive;font-weight:400}
.serif{font-family:'Fraunces',serif;font-variation-settings:'SOFT' 60,'opsz' 144}
.eyebrow{font-weight:400;font-size:19px;letter-spacing:.32em;text-transform:uppercase}
.logo{-webkit-mask:url(data:image/png;base64,%s) center/contain no-repeat;mask:url(data:image/png;base64,%s) center/contain no-repeat;display:block}
.photo{position:absolute;inset:0;background-size:cover;background-position:center}
.grain{position:absolute;inset:0;pointer-events:none;opacity:.06;mix-blend-mode:multiply;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='100%%' height='100%%' filter='url(%%23n)'/></svg>")}
.ticket{position:absolute;left:0;right:0;height:26px;background:var(--blush)}
.ticket.top{top:0;-webkit-mask:radial-gradient(circle at 50%% 100%%, transparent 11px, #000 12px) 0 0/44px 100%% repeat-x}
.ticket.bot{bottom:0;-webkit-mask:radial-gradient(circle at 50%% 0, transparent 11px, #000 12px) 0 0/44px 100%% repeat-x}
/* hand-written annotations */
.note{position:absolute;color:var(--linen);font-family:'Damion',cursive;font-size:64px;line-height:1;text-shadow:0 2px 14px rgba(40,10,5,.55);transform:rotate(-6deg)}
.note.ox{color:var(--ox);text-shadow:0 1px 0 rgba(255,255,255,.35)}
svg.arrow{position:absolute;overflow:visible}
svg.arrow path{fill:none;stroke:var(--linen);stroke-width:5;stroke-linecap:round;stroke-linejoin:round;filter:drop-shadow(0 2px 6px rgba(40,10,5,.55))}
svg.arrow.ox path{stroke:var(--ox);filter:none}
.bar{position:absolute;left:0;right:0;bottom:0;padding:44px 64px 56px;display:flex;justify-content:space-between;align-items:flex-end;color:var(--linen);background:linear-gradient(to top, rgba(80,12,2,.86), rgba(80,12,2,.0))}
.bar .h{font-family:'Damion',cursive;font-size:88px;line-height:.95}
.bar .s{font-size:19px;letter-spacing:.3em;text-transform:uppercase;margin-top:14px;opacity:.9}
.bar .logo{width:150px;height:82px;background:var(--blush)}
%s
</style></head><body>%s<div class="grain"></div></body></html>"""
def page(css_extra, body): return BASE % (css, logo, logo, css_extra, body)
arrow=lambda cls,x,y,w,h,d: f'<svg class="arrow {cls}" style="left:{x}px;top:{y}px" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><path d="{d}"/></svg>'

P={}
# 01 — Wild world with annotations
P['01-wild-same-parasol']=page("""
.photo{background-image:url(data:image/png;base64,%s)}
"""%b64('../worlds/w11.png'), f"""
<div class="photo"></div>
<div class="note" style="left:560px;top:120px">her parasol</div>
{arrow('',540,150,180,110,'M180 10 C 120 20, 70 50, 20 95 M 20 95 l 34 -8 M 20 95 l 6 -34')}
<div class="note" style="left:120px;top:1020px;transform:rotate(-5deg)">his parasol</div>
{arrow('',330,930,150,110,'M10 100 C 40 60, 70 40, 120 20 M 120 20 l -34 2 M 120 20 l -8 32')}
<div class="bar"><div><div class="h">On the plate.<br>On the table.</div><div class="s">Stitches of the Wild · Lunch under bamboo</div></div><div class="logo"></div></div>
""")

# 02 — Beads world (Cairo balcony)
P['02-beads-own-palm']=page("""
.photo{background-image:url(data:image/png;base64,%s)}
"""%b64('../worlds/w21.png'), f"""
<div class="photo"></div>
<div class="note" style="left:640px;top:70px;transform:rotate(5deg)">this palm</div>
{arrow('',760,150,120,120,'M20 10 C 40 50, 70 80, 110 110 M 110 110 l -32 -6 M 110 110 l -2 -32')}
<div class="note" style="left:90px;top:760px;transform:rotate(-7deg)">that palm</div>
{arrow('',330,700,140,90,'M10 80 C 50 50, 90 30, 130 10 M 130 10 l -34 4 M 130 10 l -6 32')}
<div class="bar"><div><div class="h">Breakfast under<br>its own palm.</div><div class="s">A Tale in Beads · Cairo, 8 a.m.</div></div><div class="logo"></div></div>
""")

# 03 — Pretty Past (roses painted and picked)
P['03-past-painted-picked']=page("""
.photo{background-image:url(data:image/png;base64,%s)}
"""%b64('../worlds/w32.png'), f"""
<div class="photo"></div>
<div class="note" style="left:70px;top:520px;transform:rotate(-8deg)">picked</div>
{arrow('',210,590,120,90,'M10 10 C 40 40, 70 60, 110 80 M 110 80 l -30 -10 M 110 80 l -4 -30')}
<div class="note" style="left:640px;top:1010px;transform:rotate(-5deg)">painted</div>
{arrow('',590,1000,110,80,'M100 60 C 70 40, 45 25, 10 10 M 10 10 l 30 2 M 10 10 l 6 28')}
<div class="bar"><div><div class="h">Roses, painted<br>and picked.</div><div class="s">Pretty Past · Golden hour</div></div><div class="logo"></div></div>
""")

# 04 — humour: dusk dinner
P['04-guests-six']=page("""
.photo{background-image:url(data:image/png;base64,%s)}
.stack{position:absolute;left:64px;right:64px;top:110px;color:var(--linen);text-shadow:0 2px 18px rgba(40,10,5,.6)}
.stack .row{display:flex;justify-content:space-between;align-items:baseline;border-bottom:2px dashed rgba(244,238,228,.55);padding:14px 0}
.stack .k{font-size:22px;letter-spacing:.3em;text-transform:uppercase}
.stack .v{font-family:'Damion',cursive;font-size:84px;line-height:1}
"""%b64('../worlds/w31.png'), f"""
<div class="photo"></div>
<div class="stack">
  <div class="row"><span class="k">Guests</span><span class="v">six</span></div>
  <div class="row"><span class="k">Pieces</span><span class="v">twenty-four</span></div>
  <div class="row"><span class="k">Reasons to host</span><span class="v">unlimited</span></div>
</div>
<div class="bar"><div><div class="h">Perfect per set.</div><div class="s">Pretty Past · The dinner that runs late</div></div><div class="logo"></div></div>
""")

# 05 — Which table are you? triptych of worlds
P['05-which-table']=page("""
body{background:var(--ox)}
.tri{position:absolute;left:40px;right:40px;top:200px;height:900px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px}
.col{position:relative;overflow:hidden}
.col .im{position:absolute;inset:0;background-size:cover;background-position:center}
.c1 .im{background-image:url(data:image/png;base64,%s);background-position:55%% 50%%}
.c2 .im{background-image:url(data:image/png;base64,%s);background-position:45%% 50%%}
.c3 .im{background-image:url(data:image/png;base64,%s);background-position:50%% 50%%}
.col .lab{position:absolute;left:0;right:0;bottom:0;padding:120px 18px 22px;background:linear-gradient(to top, rgba(80,12,2,.9), rgba(80,12,2,0));color:var(--linen)}
.col .lab .a{font-family:'Damion',cursive;font-size:40px;color:var(--blush);line-height:1}
.col .lab .b{font-family:'Damion',cursive;font-size:52px;line-height:1;margin-top:8px}
.head{position:absolute;left:40px;right:40px;top:80px;color:var(--linen);display:flex;justify-content:space-between;align-items:baseline}
.head .h{font-family:'Damion',cursive;font-size:84px;line-height:1;color:var(--blush)}
.foot{position:absolute;left:40px;right:40px;bottom:96px;color:var(--linen);display:flex;justify-content:space-between;align-items:center}
.foot .t{font-size:24px;font-weight:300}
.foot .t b{font-family:'Damion',cursive;font-weight:400;font-size:44px;color:var(--blush);margin-left:10px}
.foot .logo{width:150px;height:82px;background:var(--blush)}
"""%(b64('../worlds/w12.png'),b64('../worlds/w22.png'),b64('../worlds/w31.png')), """
<div class="ticket top"></div><div class="ticket bot"></div>
<div class="head"><div class="h">Which table are you?</div></div>
<div class="tri">
  <div class="col c1"><div class="im"></div><div class="lab"><div class="a">a.</div><div class="b">The long lunch</div></div></div>
  <div class="col c2"><div class="im"></div><div class="lab"><div class="a">b.</div><div class="b">The slow<br>Saturday</div></div></div>
  <div class="col c3"><div class="im"></div><div class="lab"><div class="a">c.</div><div class="b">The dinner<br>that runs late</div></div></div>
</div>
<div class="foot"><div class="t">Tell us in the comments <b>a, b or c</b></div><div class="logo"></div></div>
""")

# 06 — manifesto type: per piece / per set / per table / per Sunday
P['06-per-everything']=page("""
body{background:var(--ox)}
.list{position:absolute;left:0;right:0;top:230px;text-align:center;color:var(--linen);display:grid;gap:0}
.list .l{font-family:'Damion',cursive;font-size:150px;line-height:1.02}
.list .l i{font-style:normal;color:var(--blush)}
.list .l.dim{opacity:.55;font-size:120px}
.foot{position:absolute;left:0;right:0;bottom:130px;text-align:center;color:var(--blush)}
.foot .logo{width:260px;height:141px;background:var(--blush);margin:0 auto 20px}
""", """
<div class="ticket top"></div><div class="ticket bot"></div>
<div class="list">
  <div class="l"><i>per</i> piece.</div>
  <div class="l"><i>per</i> set.</div>
  <div class="l"><i>per</i> table.</div>
  <div class="l"><i>per</i> Sunday.</div>
  <div class="l dim"><i>per</i> Cairo.</div>
</div>
<div class="foot"><div class="logo"></div><div class="eyebrow">Porcelain tableware · Now open · perset.shop</div></div>
""")

for k,v in P.items(): open(k+'.html','w').write(v)
print(list(P))
