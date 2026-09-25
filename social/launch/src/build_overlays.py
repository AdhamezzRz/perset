import base64
b64=base64.b64encode(open('../src/perset-logo-mask.png','rb').read()).decode()
HEAD = """<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,300..700,0..100;1,9..144,300..700,0..100&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
<style>
:root{--linen:#F4EEE4;--ox:#500C02;--blush:#F2A4B6}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;overflow:hidden;background:transparent}
body{font-family:'Jost',sans-serif;position:relative}
.serif{font-family:'Fraunces',serif;font-variation-settings:'SOFT' 60,'opsz' 144}
.eyebrow{font-weight:400;font-size:24px;letter-spacing:.32em;text-transform:uppercase}
.logo{-webkit-mask:url(data:image/png;base64,%s) center/contain no-repeat;mask:url(data:image/png;base64,%s) center/contain no-repeat}
.ticket{position:absolute;left:0;right:0;height:30px;background:var(--blush)}
.ticket.top{top:0;-webkit-mask:radial-gradient(circle at 50%% 100%%, transparent 12px, #000 13px) 0 0/48px 100%% repeat-x}
.ticket.bot{bottom:0;-webkit-mask:radial-gradient(circle at 50%% 0, transparent 12px, #000 13px) 0 0/48px 100%% repeat-x}
/* card */
.card{position:absolute;inset:0;background:var(--ox);color:var(--blush);display:flex;flex-direction:column;align-items:center;justify-content:center}
.card .logo{width:640px;height:348px;background:var(--blush)}
.card .line{font-size:46px;font-weight:300;font-style:italic;margin-top:30px}
.card .line b{font-weight:500;font-style:normal}
.card .eyebrow{position:absolute;left:0;right:0;text-align:center;opacity:.9}
.card .eyebrow.t{top:150px}.card .eyebrow.b{bottom:150px}
.card .big{font-size:120px;font-weight:300;line-height:.95;text-align:center;letter-spacing:-.015em;color:var(--linen)}
.card .big i{font-style:italic;font-weight:400;color:var(--blush)}
.card .small{font-size:30px;font-weight:300;color:var(--linen);opacity:.9;margin-top:40px;text-align:center;line-height:1.4}
.scrim{position:absolute;left:0;right:0;bottom:0;height:900px;background:linear-gradient(to top, rgba(80,12,2,.72) 0%%, rgba(80,12,2,.45) 45%%, rgba(80,12,2,0) 100%%)}
/* lower-third overlay */
.lt{position:absolute;left:80px;right:80px;bottom:300px;color:var(--linen);text-shadow:0 2px 24px rgba(40,10,5,.45)}
.lt .eyebrow{color:var(--blush);margin-bottom:18px;text-shadow:0 2px 18px rgba(40,10,5,.6)}
.lt .h{font-size:132px;line-height:.95;font-weight:300;letter-spacing:-.015em}
.lt .h i{font-style:italic;font-weight:400}
.pill{position:absolute;top:110px;left:80px;background:rgba(80,12,2,.86);color:var(--blush);padding:14px 22px;font-size:22px;letter-spacing:.3em;text-transform:uppercase}
.count{position:absolute;left:80px;right:80px;bottom:260px;color:var(--linen);text-shadow:0 2px 24px rgba(40,10,5,.5)}
.count .row{display:flex;align-items:baseline;gap:26px;padding:12px 0;border-top:2px dashed rgba(244,238,228,.55)}
.count .row:last-of-type{border-bottom:2px dashed rgba(244,238,228,.55)}
.count .n{font-size:66px;font-weight:300;width:70px}
.count .nm{font-size:36px;font-weight:400}
.count .cm{margin-left:auto;font-size:22px;letter-spacing:.2em}
.count .sum{font-size:54px;font-weight:300;margin-top:30px}
.count .sum b{font-weight:500;color:var(--blush)}
</style></head><body>""" % (b64,b64)
TAIL="</body></html>"
pages={}
pages['card_open_r1'] = '<div class="card"><div class="ticket top"></div><div class="ticket bot"></div><div class="eyebrow t">Porcelain tableware · Cairo</div><div class="logo"></div><div class="line serif">Beautiful <b>per piece</b>, perfect <b>per set</b>.</div></div>'
pages['card_end'] = '<div class="card"><div class="ticket top"></div><div class="ticket bot"></div><div class="logo"></div><div class="line serif">Beautiful <b>per piece</b>, perfect <b>per set</b>.</div><div class="eyebrow b">Now open · perset.shop</div></div>'
pages['card_open_r2'] = '<div class="card"><div class="ticket top"></div><div class="ticket bot"></div><div class="eyebrow t">Inside the set</div><div class="big serif">Everything a<br>table of six<br><i>needs.</i></div></div>'
pages['card_open_r3'] = '<div class="card"><div class="ticket top"></div><div class="ticket bot"></div><div class="eyebrow t">The collections</div><div class="big serif">Three stories,<br><i>one table.</i></div></div>'
pages['card_end_r3'] = '<div class="card"><div class="ticket top"></div><div class="ticket bot"></div><div class="logo"></div><div class="small">Each collection is one complete<br>24-piece set for a table of six.</div><div class="eyebrow b">Now open · perset.shop</div></div>'
# reel 1 lower thirds
pages['ov_r1_1'] = '<div class="scrim"></div><div class="pill">No. 01 · Stitches of the Wild</div><div class="lt"><div class="h serif">Beautiful</div></div>'
pages['ov_r1_2'] = '<div class="scrim"></div><div class="pill">No. 02 · A Tale in Beads</div><div class="lt"><div class="h serif"><i>per piece,</i></div></div>'
pages['ov_r1_3'] = '<div class="scrim"></div><div class="pill">No. 03 · Pretty Past</div><div class="lt"><div class="h serif">perfect<br><i>per set.</i></div></div>'
# reel 2
pages['ov_r2_1'] = '<div class="scrim"></div><div class="pill">A Tale in Beads</div><div class="lt"><div class="eyebrow">Service for six</div><div class="h serif">One set.<br><i>Every course.</i></div></div>'
rows=[("6","Dinner plates","27 cm"),("6","Dessert plates","21 cm"),("6","Salad plates","21 cm"),("6","Soup bowls","12 cm")]
pages['ov_r2_2'] = '<div class="scrim"></div><div class="pill">Pretty Past</div><div class="count">'+''.join(f'<div class="row"><div class="n serif">{n}</div><div class="nm">{nm}</div><div class="cm">{cm}</div></div>' for n,nm,cm in rows)+'<div class="sum serif"><b>24</b> pieces, one complete set.</div></div>'
# reel 3
pages['ov_r3_1'] = '<div class="scrim"></div><div class="lt"><div class="eyebrow">No. 01</div><div class="h serif">Stitches<br><i>of the Wild</i></div></div>'
pages['ov_r3_2'] = '<div class="scrim"></div><div class="lt"><div class="eyebrow">No. 02</div><div class="h serif">A Tale<br><i>in Beads</i></div></div>'
pages['ov_r3_3'] = '<div class="scrim"></div><div class="lt"><div class="eyebrow">No. 03</div><div class="h serif">Pretty<br><i>Past</i></div></div>'
for k,v in pages.items(): open(f'{k}.html','w').write(HEAD+v+TAIL)
print(list(pages))
