from reel import *
import json
OUT=os.path.abspath('../ins/out'); S=os.path.abspath('../ins/seg')
E_=json.load(open('../ins/ell.json'))
# ---------------- Wild: the cousins
clip('vid/k_cat_x.mp4',f'{S}/cat1.mp4',speed=0.85)
e=E_['cat']; cx,cy=e[0][0]/1520,e[0][1]/2688
still('../ins/gen/cat_x.png',f'{S}/cat2.mp4',2.8,1.0,1.55,(0.5,0.5),(cx,cy-0.03))
d=os.path.abspath('../ins/cap_cat')
c=[caption('c1',chip('a Cairo street cat met our plate.',230),d),
   caption('c2',chip('she checked the leopards.',230),d),
   caption('c3',chip('then she sat down. like family.',230),d),
   caption('c4','<div class="scr" style="top:200px;font-size:150px">cousins.</div><div class="sm" style="top:1720px;font-size:22px">stitches of the wild · a set for six · perset.shop</div>',d)]
compose([f'{S}/cat1.mp4',f'{S}/cat2.mp4'],[(c[0],0.2,2.2),(c[1],2.2,4.2),(c[2],4.2,5.9),(c[3],6.1,8.7)],os.path.abspath(f'{OUT}/wild-reel-3-cousins.mp4'),grain=4)
# ---------------- Past: Lot 24
still('kf/kf_auction.jpg',f'{S}/au1.mp4',2.2,1.0,1.08,(0.5,0.45),(0.5,0.42))
clip('vid/k_auction_x.mp4',f'{S}/au2.mp4')
e=E_['auction']; ax,ay=e[0][0]/1520,e[0][1]/2688
still('../ins/gen/auction_x.png',f'{S}/au3.mp4',2.8,1.0,2.4,(0.5,0.45),(ax,ay))
d=os.path.abspath('../ins/cap_auction')
lt=lambda name,txt,val: caption(name,f'<div style="position:absolute;left:60px;right:60px;top:1500px;background:rgba(20,10,6,.82);border-left:8px solid #F2A4B6;padding:22px 30px;color:#FBF3E6"><div style="font-size:22px;letter-spacing:.3em;text-transform:uppercase;color:#F2A4B6">lot 24 · {txt}</div><div style="font-family:Fraunces;font-size:62px;line-height:1.1;margin-top:6px">{val}</div></div>',d)
c0=caption('c0','<div class="scr" style="top:190px;font-size:140px">Lot 24.</div><div class="sm" style="top:370px;font-size:24px">pretty past dinner plate · cairo · 2026</div>',d)
b=[lt('b1','current bid','2 cousins'),lt('b2','current bid','6 aunties'),lt('b3','current bid','1 mother-in-law'),lt('b4','current bid','Teta. final offer.')]
sold=caption('sold','<div class="scr" style="top:180px;font-size:150px">sold.</div><div style="position:absolute;left:0;right:0;top:390px;text-align:center;font-size:40px;color:#FBF3E6;text-shadow:0 2px 12px rgba(0,0,0,.6)">to whoever hosts on Friday.</div><div class="sm" style="top:1720px;font-size:22px">pretty past · a set for six · perset.shop</div>',d)
caps=[(c0,0.15,2.2),(b[0],2.3,3.5),(b[1],3.5,4.7),(b[2],4.7,5.9),(b[3],5.9,7.2),(sold,7.3,10.0)]
compose([f'{S}/au1.mp4',f'{S}/au2.mp4',f'{S}/au3.mp4'],caps,os.path.abspath(f'{OUT}/past-reel-2-lot-24.mp4'),grain=4)
