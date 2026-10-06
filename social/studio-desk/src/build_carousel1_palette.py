import sys; sys.path.insert(0,'..')
from common import *
import random, math
A='../assets/'
PAL={
 'wild':[('Parasol Pink','#E38E7B'),('Porcelain','#DED5CA'),('Leopard Gold','#B58A38'),('Bamboo','#756540'),('Thread Umber','#3F3218')],
 'beads':[('Bead Sand','#D0BD98'),('Porcelain','#F9F0F1'),('Zigzag Coral','#E09A88'),('Palm Green','#476D3E'),('Trunk Umber','#4E4832')],
 'past':[('Saffron','#F6BF0F'),('Peacock Blue','#6693BC'),('Rose','#F3736C'),('Peacock Mist','#98BDB6'),('Vintage Cream','#E8D8B0')]}
COLL=[('wild','Stitches of the Wild','No. 01','wild_dinner','raw linen · bamboo · green glass'),
      ('beads','A Tale in Beads','No. 02','beads_dinner','sage linen · brass · fresh figs'),
      ('past','Pretty Past','No. 03','past_dinner','blush napkins · roses · candlelight')]
CUT={k:img(f'../../cutouts/{k}.png') for k in ['wild_dinner','beads_dinner','past_dinner']}
def chip(color,name,hexv,w=470,h=150,rot=0,seed=1,top=0,left=0):
    poly=jag(w,h,seed,amp=5,step=22,edges='rb')
    return f'''<div class="abs sh-s" style="left:{left}px;top:{top}px;width:{w}px;height:{h}px;transform:rotate({rot}deg)">
      <div style="width:{w}px;height:{h}px;background:#FBF8F2;clip-path:{poly};display:flex">
        <div style="width:{h+10}px;height:{h}px;background:{color}"></div>
        <div style="padding:26px 24px;display:flex;flex-direction:column;justify-content:center;gap:4px">
          <div class="script" style="font-size:50px;line-height:1;color:#500C02">{name}</div>
          <div class="eyebrow" style="font-size:19px;color:#6E5A54">{hexv}</div></div></div></div>'''
def slide_collection(key,title,no,cut,pairs,seed):
    rots=[-2.2,1.6,-1.2,2.0,-1.8]; body=''
    for i,(n,h) in enumerate(PAL[key]):
        body+=chip(h,n,h,rot=rots[i],seed=seed+i,top=250+i*168,left=545+(i%2)*14)
    return f'''
    <div class="abs sh" style="left:-330px;top:260px;width:880px;height:880px;transform:rotate({-8+seed}deg)"><img src="{CUT[cut]}" style="width:880px;height:880px"></div>
    <div class="abs eyebrow" style="left:60px;top:70px;font-size:21px;color:#500C02">{no} · {title}</div>
    <div class="abs script" style="left:56px;top:96px;font-size:92px;line-height:1;color:#500C02">the palette</div>
    {body}
    <div class="abs tape" style="left:520px;top:226px;width:150px;transform:rotate(-4deg)"></div>
    <div class="abs script" style="left:60px;right:60px;bottom:96px;font-size:54px;color:#500C02;line-height:1.1;white-space:nowrap">pairs with <span style="color:#8a2a1a">{pairs}</span></div>
    <div class="abs eyebrow" style="left:60px;bottom:50px;font-size:17px;color:#6E5A54">sampled from the plate · swipe →</div>
    '''
slides=[]
# 1 cover: fan deck
chips=[h for k in ('wild','beads','past') for _,h in PAL[k]][:15]
fan=''
N=len(chips); span=84
for i,h in enumerate(chips):
    ang=-span/2+i*span/(N-1)
    fan+=f'''<div class="abs sh-s" style="left:490px;top:690px;width:150px;height:560px;transform-origin:75px 520px;transform:rotate({ang:.1f}deg)">
      <div style="width:150px;height:560px;background:#FBF8F2;border-radius:10px 10px 6px 6px;overflow:hidden">
        <div style="height:380px;background:{h}"></div>
        <div style="padding:10px 12px"><div class="eyebrow" style="font-size:13px;color:#6E5A54;letter-spacing:.16em">{h}</div></div></div></div>'''
cover=f'''
 <div class="abs eyebrow" style="left:64px;top:70px;font-size:21px;color:#500C02">per set · a palette guide</div>
 <div class="abs script" style="left:56px;top:110px;font-size:150px;line-height:.95;color:#500C02">colour,<br>borrowed<br>from <span style="color:#d4675b">porcelain.</span></div>
 <div class="abs" style="left:0;top:0;width:1080px;height:1350px;transform-origin:565px 1210px;transform:translateY(40px) scale(1.16)">{fan}
 <div class="abs" style="left:545px;top:1200px;width:60px;height:60px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#e6c98a,#9b7a34);box-shadow:0 3px 6px rgba(0,0,0,.4)"></div></div>
 <div class="abs eyebrow" style="right:64px;top:80px;font-size:18px;color:#6E5A54;text-align:right;line-height:1.7">3 plates<br>15 colours<br>swipe →</div>
'''
slides.append(('01-cover',cover))
for i,(k,t,no,cut,pairs) in enumerate(COLL):
    slides.append((f'0{i+2}-{k}',slide_collection(k,t,no,cut,pairs,seed=i*7+1)))
# 5 save
three=''.join(f'<div class="abs sh-s" style="left:{120+i*300}px;top:700px;width:240px;height:240px"><img src="{CUT[c]}" style="width:240px;height:240px"></div>' for i,c in enumerate(['wild_dinner','beads_dinner','past_dinner']))
save=f'''
 <div class="abs script" style="left:0;right:0;top:170px;text-align:center;font-size:170px;line-height:.95;color:#500C02">save this<br>for your next<br><span style="color:#d4675b">table.</span></div>
 {three}
 <div class="abs script" style="left:0;right:0;top:985px;text-align:center;font-size:60px;color:#500C02">each collection is a complete 24-piece set</div>
 <div class="abs logo" style="left:380px;top:1085px;width:320px;height:174px;background:#500C02"></div>
 <div class="abs eyebrow" style="left:0;right:0;bottom:46px;text-align:center;font-size:19px;color:#6E5A54">perset.shop</div>
'''
slides.append(('05-save',save))
for name,b in slides:
    open(name+'.html','w').write(page('',b,'',W=1080,H=1350))
print([n for n,_ in slides])
