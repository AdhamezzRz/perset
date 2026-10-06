import sys; sys.path.insert(0,'..')
from common import *
dinner=img('../../cutouts/wild_dinner.png'); bowl=img('../../cutouts/wild_soup.png')
S=6.6
def icon(kind,cm):
    d=cm*S
    if kind=='bowl': return f'<img src="{bowl}" style="width:{d}px;height:{d}px;filter:drop-shadow(0 5px 6px rgba(60,35,20,.35))">'
    if kind=='dinner': return f'<img src="{dinner}" style="width:{d}px;height:{d}px;filter:drop-shadow(0 5px 6px rgba(60,35,20,.35))">'
    return f'<div style="width:{d}px;height:{d}px;border:4px dashed #C65A4C;border-radius:50%"></div>'
rows=[('bowl',12,'in the bowl','12 cm','Red lentil soup','lemon, cumin, parsley'),
      ('ghost',21,'on the salad plate','21 cm','Fattoush','sumac, pomegranate, crisp bread'),
      ('dinner',27,'on the dinner plate','27 cm','Mahshi','vine leaves and courgettes, garlic yoghurt'),
      ('ghost',21,'on the dessert plate','21 cm','Om Ali','warm, pistachio, a little cream')]
rhtml=''
for i,(k,cm,where,size,dish,sub) in enumerate(rows):
    rhtml+=f'''<div style="display:flex;align-items:center;gap:34px;height:196px;border-top:2px dashed rgba(80,12,2,.3)">
      <div style="width:190px;display:flex;align-items:center;justify-content:center">{icon(k,cm)}</div>
      <div style="flex:1">
        <div class="eyebrow" style="font-size:17px;color:#8a2a1a;letter-spacing:.26em">{where} · {size}</div>
        <div class="serif" style="font-size:58px;font-style:italic;font-weight:400;color:#500C02;line-height:1.05;margin-top:6px">{dish}</div>
        <div style="font-size:25px;color:#6E5A54;margin-top:6px;font-weight:300">{sub}</div></div></div>'''
W,H=860,1210
poly=jag(W,H,seed=4,amp=5,step=24)
body=f'''
<div class="abs sh" style="left:110px;top:70px;width:{W}px;height:{H}px;transform:rotate(-1deg)">
 <div style="width:{W}px;height:{H}px;background:#FBF8F2;clip-path:{poly};position:relative;padding:50px 64px">
   <div style="position:absolute;inset:22px;border:2px solid rgba(80,12,2,.35)"></div>
   <div style="position:absolute;inset:30px;border:1px solid rgba(80,12,2,.25)"></div>
   <div class="logo" style="width:210px;height:114px;background:#500C02;margin:6px auto 0"></div>
   <div class="eyebrow" style="text-align:center;font-size:18px;color:#6E5A54;margin-top:6px">porcelain tableware · cairo</div>
   <div class="script" style="text-align:center;font-size:104px;line-height:1;color:#500C02;margin-top:6px">a menu for six</div>
   <div style="margin-top:14px">{rhtml}
     <div style="border-top:2px dashed rgba(80,12,2,.3)"></div></div>
   <div class="script" style="text-align:center;font-size:54px;color:#500C02;margin-top:12px">to drink: <span style="color:#d4675b">hibiscus, over ice</span></div>
 </div></div>
<div class="abs script" style="left:36px;top:1215px;font-size:60px;color:#d4675b;transform:rotate(-7deg);width:240px;line-height:.95">set the<br>table first</div>
<svg class="abs hand" style="left:0;top:0;overflow:visible" width="1080" height="1350"><path d="{squiggle(236,1226,330,1190,9,-20)}" style="stroke:#d4675b"/><path d="{arrowhead(330,1190,236,1226,seed=9)}" style="stroke:#d4675b"/></svg>
<div class="abs eyebrow" style="left:0;right:36px;bottom:24px;text-align:right;font-size:16px;color:#6E5A54">perset.shop</div>
'''
open('p2.html','w').write(page('',body,'',W=1080,H=1350,bgc='#E7DAC4'))
