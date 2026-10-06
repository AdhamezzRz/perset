import sys; sys.path.insert(0,'..')
from common import *
import math
S=17  # px per cm
cx,cy=350,790
dinner=img('../../cutouts/wild_dinner.png'); bowl=img('../../cutouts/wild_soup.png')
def circ(d,x,y,extra=''): return f'left:{x-d/2}px;top:{y-d/2}px;width:{d}px;height:{d}px;{extra}'
# cutlery (outline drawings)
fork='''<svg class="abs hand" style="left:{x}px;top:{y}px" width="46" height="{h}" viewBox="0 0 46 {h}"><g style="stroke:#500C02;stroke-width:3.5;fill:rgba(255,255,255,.35);stroke-linejoin:round;stroke-linecap:round">
 <path d="M8 4 V70 Q8 92 23 96 Q38 92 38 70 V4 M18 4 V66 M28 4 V66"/><path d="M19 96 L19 {h2} Q19 {h3} 23 {h3} Q27 {h3} 27 {h2} L27 96" /></g></svg>'''
def forksvg(x,y,h=340): return fork.format(x=x,y=y,h=h,h2=h-14,h3=h-4)
knife=lambda x,y,h=390:f'''<svg class="abs hand" style="left:{x}px;top:{y}px" width="40" height="{h}" viewBox="0 0 40 {h}"><g style="stroke:#500C02;stroke-width:3.5;fill:rgba(255,255,255,.35);stroke-linejoin:round;stroke-linecap:round"><path d="M10 4 Q36 18 34 120 L34 190 L10 190 Z"/><path d="M12 190 L12 {h-14} Q12 {h-4} 22 {h-4} Q32 {h-4} 32 {h-14} L32 190"/></g></svg>'''
spoon=lambda x,y,h=320:f'''<svg class="abs hand" style="left:{x}px;top:{y}px" width="44" height="{h}" viewBox="0 0 44 {h}"><g style="stroke:#500C02;stroke-width:3.5;fill:rgba(255,255,255,.35);stroke-linejoin:round;stroke-linecap:round"><ellipse cx="22" cy="52" rx="19" ry="48"/><path d="M16 98 L16 {h-14} Q16 {h-4} 22 {h-4} Q28 {h-4} 28 {h-14} L28 98"/></g></svg>'''
# ruler
ticks=''; 
for i in range(0,61):
    x=30+i*S; hh=34 if i%5==0 else (22 if i%1==0 else 14)
    ticks+=f'<line x1="{x}" y1="1262" x2="{x}" y2="{1262+hh}" stroke="#2A1A16" stroke-width="{2.2 if i%5==0 else 1.4}"/>'
    if i%5==0: ticks+=f'<text x="{x+4}" y="1312" font-family="Jost" font-size="19" fill="#2A1A16" letter-spacing="1">{i}</text>'
ruler=f'<div class="abs" style="left:14px;top:1250px;width:1052px;height:74px;background:#E9CF98;opacity:.92;border-radius:3px;box-shadow:0 3px 8px rgba(60,35,20,.3)"></div><svg class="abs" style="left:0;top:0" width="1080" height="1350">{ticks}</svg><div class="abs eyebrow" style="left:640px;top:1214px;font-size:17px;color:#6E5A54;width:400px;text-align:right">ruler · true scale</div>'
def lbl(x,y,text,size=46,align='left',w=420,color='#500C02',rot=0):
    return f'<div class="abs script" style="left:{x}px;top:{y}px;width:{w}px;text-align:{align};font-size:{size}px;line-height:1.02;color:{color};transform:rotate({rot}deg)">{text}</div>'
def ln(x1,y1,x2,y2,seed,bow=24,head=True):
    d=squiggle(x1,y1,x2,y2,seed,bow)
    h=arrowhead(x2,y2,x1,y1,seed=seed) if head else ''
    return f'<svg class="abs hand" style="left:0;top:0;overflow:visible" width="1080" height="1350"><path d="{d}"/><path d="{h}"/></svg>'
a=math.radians
dp=lambda d,deg:(cx+d/2*math.cos(a(deg)),cy+d/2*math.sin(a(deg)))
x1,y1=dp(27*S,135); x2,y2=dp(21*S,95); x3,y3=dp(12*S,-140)
body=f'''
<div class="abs" style="inset:26px;border:3px dashed rgba(80,12,2,.35);border-radius:6px"></div>
<div class="abs script" style="left:62px;top:62px;font-size:104px;line-height:.96;color:#500C02">a place setting,<br><span style="color:#d4675b">to scale.</span></div>
<div class="abs eyebrow" style="left:66px;top:290px;font-size:19px;color:#6E5A54;line-height:1.7">27 · 21 · 21 · 12 cm<br>one place, drawn at true size</div>
<!-- dessert ghost -->
<div class="abs" style="{circ(21*S,850,300,'border:5px dashed #C65A4C;border-radius:50%;opacity:.9')}"></div>
{lbl(690,495,'21 cm dessert plate,<br>for later',44,'center',320)}
<!-- the stack -->
<div class="abs sh" style="{circ(27*S,cx,cy)}"><img src="{dinner}" style="width:100%;height:100%"></div>
<div class="abs" style="{circ(21*S,cx,cy,'border:5px dashed #C65A4C;border-radius:50%;background:rgba(251,248,242,.22)')}"></div>
<div class="abs sh" style="{circ(12*S,cx,cy)}"><img src="{bowl}" style="width:100%;height:100%"></div>
{forksvg(62,cy-170)}{knife(618,cy-195)}{spoon(676,cy-160)}
<!-- glass -->
<div class="abs" style="{circ(7*S,860,880,'border:4px solid #500C02;border-radius:50%;background:rgba(255,255,255,.35)')}"></div>
<div class="abs" style="{circ(5*S,860,880,'border:2.5px solid rgba(80,12,2,.55);border-radius:50%')}"></div>
{lbl(790,950,'7 cm glass',38,'center',150)}
<!-- callouts -->
{lbl(48,1065,'27 cm<br>dinner plate',48,'left',260)}
{ln(190,1068,x1-4,y1+8,3,bow=-30)}
{lbl(320,1080,'21 cm salad plate,<br>stacked on top',46,'left',360)}
{ln(430,1074,x2,y2,5,bow=30)}
{lbl(52,470,'12 cm<br>soup bowl',46,'left',240)}
{ln(190,565,x3,y3,7,bow=-30)}
{lbl(690,1060,'× 6 places<br><span style="color:#d4675b">= 24 pieces</span>',56,'center',360,rot=-4)}
{ruler}
'''
open('p1.html','w').write(page('',body,'',W=1080,H=1350,bgc='#EBDFCB'))
print('ok')
