import sys; sys.path.insert(0,'..')
from common import *
A='../assets/'
INK='#F7EEDC'
def slide(photo, loops, notes, arrows, exhibit, extra=''):
    sv=''
    for L in loops:
        cx,cy,rx,ry,seed=L[:5]; rot=L[5] if len(L)>5 else 0
        sv+=f'<path d="{loop_path(cx,cy,rx,ry,seed)}" transform="rotate({rot} {cx} {cy})"/>'
    for (x1,y1,x2,y2,seed,bow) in arrows:
        sv+=f'<path d="{squiggle(x1,y1,x2,y2,seed,bow)}"/><path d="{arrowhead(x2,y2,x1,y1,24,seed)}"/>'
    nt=''.join(f'<div class="abs script note" style="left:{x}px;top:{y}px;font-size:{s}px;transform:rotate({r}deg);width:{w}px;text-align:{al}">{t}</div>' for (x,y,t,s,r,w,al) in notes)
    css=f"""
    .photo{{position:absolute;inset:0;background:url({img(A+photo)}) center/cover}}
    .note{{color:{INK};line-height:1;text-shadow:0 2px 12px rgba(20,8,0,.85),0 0 3px rgba(20,8,0,.7)}}
    svg.pen{{position:absolute;left:0;top:0;overflow:visible;filter:drop-shadow(0 2px 5px rgba(20,8,0,.8))}}
    svg.pen path{{fill:none;stroke:{INK};stroke-width:5.5;stroke-linecap:round;stroke-linejoin:round;opacity:.95}}
    .ex{{position:absolute;right:40px;bottom:36px;color:{INK};font-size:19px;letter-spacing:.3em;text-transform:uppercase;text-shadow:0 2px 10px rgba(20,8,0,.9)}}
    """
    body=f'<div class="photo"></div><svg class="pen" width="1080" height="1350">{sv}</svg>{nt}<div class="ex">{exhibit}</div>{extra}'
    return page(css,body,'',W=1080,H=1350,bgc='#222',fibers=False)
Lbl=lambda: f'''<div class="abs sh" style="left:40px;top:1120px;width:930px;height:170px;transform:rotate(-2deg)"><div style="width:930px;height:170px;background:#FBF8F2;clip-path:{jag(930,170,seed=21,amp=6,step=20)};padding:20px 34px">
 <div class="eyebrow" style="font-size:18px;color:#8a2a1a">per set · a case file</div>
 <div class="script" style="font-size:88px;line-height:1;color:#500C02;margin-top:2px;white-space:nowrap">evidence of a good dinner</div></div></div>
 <div class="abs tape" style="left:70px;top:1100px;width:130px;transform:rotate(-20deg)"></div>
'''
S=[]
S.append(('01-wild', slide('ev_wild.jpg',
  loops=[(400,230,160,200,2),(690,252,95,70,5),(310,930,215,120,8)],
  notes=[(610,60,"someone's<br>lipstick",74,-5,380,'left'),(735,330,'the last crust',58,-4,330,'left'),(560,985,'fork: still<br>on duty',62,-3,330,'left')],
  arrows=[(650,150,545,165,3,26),(790,320,745,280,6,-20),(700,1010,560,960,9,-26)],
  exhibit='exhibit a · stitches of the wild', extra=Lbl())))
S.append(('02-beads', slide('ev_beads.jpg',
  loops=[(858,822,122,94,3,-12),(412,1140,56,72,6,6),(90,706,110,70,9)],
  notes=[(790,612,'flatbread:<br>demolished',60,-4,290,'left'),(235,1210,'honey,<br>everywhere',66,-3,330,'left'),(40,850,'the last fig',58,-3,300,'left')],
  arrows=[(385,1212,412,1192,7,-14),(110,845,100,790,2,-14)],
  exhibit='exhibit b · a tale in beads')))
S.append(('03-past', slide('ev_past.jpg',
  loops=[(270,520,150,180,4),(865,205,150,110,7),(183,775,105,90,2)],
  notes=[(40,262,'candles:<br>spent',68,-5,300,'left'),(520,70,"someone's<br>cardigan",72,-4,420,'left'),(30,915,'half a<br>pomegranate',60,-4,380,'left')],
  arrows=[(190,360,225,420,3,-20),(760,130,800,170,5,18),(190,905,185,865,6,-14)],
  exhibit='exhibit c · pretty past')))
S.append(('04-sink', slide('ev_sink.jpg',
  loops=[(541,488,130,90,3),(980,970,100,95,6)],
  notes=[(60,90,"tomorrow's<br>problem.",120,-4,640,'left'),(640,320,'balanced,<br>somehow',62,4,330,'left'),(560,1105,'hand wash.<br>worth it.',74,-3,460,'left')],
  arrows=[(790,420,690,480,2,20),(800,1100,905,1050,8,-20)],
  exhibit='exhibit d · pretty past')))
# closing card
css="""
.bg{background:#500C02!important}.fibers{opacity:.16}.grain{opacity:.16;mix-blend-mode:screen}.vig{display:none}
#c{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:#F2A4B6}
#c .e{font-size:20px;letter-spacing:.34em;text-transform:uppercase;color:#F2A4B6}
#c .w{font-family:'Damion',cursive;font-size:230px;line-height:.9;color:#F4EEE4;margin-top:14px}
#c .w i{font-style:normal;color:#F2A4B6}
#c .t{font-size:34px;color:#F4EEE4;margin-top:34px;line-height:1.5;opacity:.92}
#c .logo{width:280px;height:152px;background:#F2A4B6;margin-top:56px}
#c .u{font-size:22px;letter-spacing:.34em;text-transform:uppercase;margin-top:26px}
"""
body='<div class="ticket" style="top:0;left:0;right:0;height:30px;background:#F2A4B6;-webkit-mask:radial-gradient(circle at 50% 100%, transparent 12px, #000 13px) 0 0/48px 100% repeat-x"></div><div id="c"><div class="e">case closed</div><div class="w">worth<br><i>it.</i></div><div class="t">Hand washing keeps the colours bright.<br>Every set is 24 pieces. Every table earns its evidence.</div><div class="logo"></div><div class="u">perset.shop</div></div>'
S.append(('05-close', page(css,body,'',W=1080,H=1350,bgc='#500C02')))
for n,h in S: open(n+'.html','w').write(h)
print([n for n,_ in S])
