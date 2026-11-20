from wc import *
import subprocess
OUT=os.path.abspath('../ins/out/wild-carousel-case-file'); os.makedirs(OUT,exist_ok=True)
CF=os.path.abspath('../ins/cf')
PHOTO=img(SCR+'/src/wild-2-perset-wild-dinner-plate.jpg'); PL=img(SCR+'/pack/assets/wild_hi.png')
S={k:img(f'{CF}/{k}z.png') for k in ('c1','c2','c3','c4')}
css="""
.bg{background:#2B2420!important}
#desk{position:absolute;inset:0;background:radial-gradient(ellipse at 40% 30%,#4a3d33,#1e1915 80%)}
.sheet{position:absolute;left:70px;top:80px;width:940px;height:1190px;background:#EFE6D2;box-shadow:0 24px 50px rgba(0,0,0,.5);transform:rotate(-.8deg)}
.sheet:before{content:'';position:absolute;inset:0;background:repeating-linear-gradient(0deg,transparent 0 47px,rgba(80,120,160,.12) 47px 48px)}
.ty{font-family:'Courier 10 Pitch','Liberation Mono',monospace;color:#231d18}
.hand{font-family:'Caveat';color:#B3241B}
.hdr{position:absolute;left:60px;right:60px;top:50px;font-size:26px;letter-spacing:.06em;line-height:1.45;border-bottom:2px solid #231d18;padding-bottom:16px}
.hdr b{font-size:44px;letter-spacing:.02em;display:block;margin-top:4px}
.ph{position:absolute;background:#fff;padding:14px 14px 18px;box-shadow:0 10px 24px rgba(0,0,0,.35)}
.ph img{display:block;filter:contrast(1.08)}
.clip{position:absolute;width:44px;height:120px;border:6px solid #9aa0a6;border-radius:22px;border-bottom-color:transparent}
.stamp{position:absolute;font-family:'Courier 10 Pitch',monospace;font-weight:700;color:#B3241B;border:6px solid #B3241B;padding:8px 22px;letter-spacing:.12em;opacity:.85;mix-blend-mode:multiply}
.tape{position:absolute;width:150px;height:46px;background:rgba(240,228,190,.75);box-shadow:0 1px 3px rgba(0,0,0,.2)}
.no{position:absolute;right:60px;bottom:40px;font-size:22px;letter-spacing:.2em}
"""
def shoot(name,body):
    f=f'{OUT}/{name}.html'; open(f,'w').write(page(css,'<div id="desk"></div>'+body,'',W=1080,H=1350,bgc='#2B2420',fibers=False))
    subprocess.run(f'cd {OUT} && NODE_PATH=$(npm root -g) node {SCR}/pack/shoot.js 1080 1350 {name}.html && rm {name}.html',shell=True,check=True)
# 1 cover: folder
shoot('slide-1-cover',f"""
<div style="position:absolute;left:80px;top:150px;width:920px;height:1080px;background:#D6B47A;border-radius:6px 6px 10px 10px;box-shadow:0 30px 60px rgba(0,0,0,.55);transform:rotate(1.2deg)">
 <div style="position:absolute;left:0;top:-54px;width:330px;height:70px;background:#D6B47A;border-radius:14px 14px 0 0"></div>
 <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 30% 20%,rgba(255,240,200,.35),transparent 60%),repeating-linear-gradient(90deg,rgba(120,80,30,.05) 0 2px,transparent 2px 7px)"></div>
 <div class="ty" style="position:absolute;left:60px;top:60px;width:520px;background:#F3EAD6;padding:22px 26px;font-size:26px;line-height:1.55;box-shadow:0 2px 4px rgba(0,0,0,.2)">
  CASE FILE No. 24/26<br>SUBJECT: <b>2 LEOPARDS</b> (porcelain)<br>LAST SEEN: on a dinner plate,<br>&nbsp;&nbsp;Cairo kitchen, CAM 03<br>FILED: 21 NOV, 07:02 am</div>
 <div class="ph" style="left:520px;top:330px;transform:rotate(6deg)"><div style="width:330px;height:330px;background:#D9CBBE url({PHOTO}) center/auto 100%"></div><div class="hand" style="font-size:38px;text-align:center;margin-top:6px;color:#231d18">the suspects</div></div>
 <div class="clip" style="left:690px;top:290px;transform:rotate(6deg)"></div>
 <div class="stamp" style="left:60px;top:470px;font-size:78px;transform:rotate(-9deg)">MISSING</div>
 <div class="hand" style="position:absolute;left:70px;top:640px;font-size:60px;line-height:1.05;transform:rotate(-3deg)">3 hours.<br>no witnesses.<br>16 paw prints.</div>
 <div class="ty" style="position:absolute;left:60px;bottom:50px;font-size:22px;letter-spacing:.14em">STITCHES OF THE WILD · EVIDENCE ENCLOSED · SWIPE →</div>
</div>""")
def exhibit(name,letter,ts,still,typed,hand,extra='',stamp=''):
    shoot(name,f"""<div class="sheet"><div class="hdr ty">EXHIBIT {letter} · CAM 03 KITCHEN<b>{ts}</b></div>
 <div class="ph" style="left:44px;top:250px;transform:rotate(1.4deg)"><img src="{still}" width="820" height="464">{extra}</div>
 <div class="tape" style="left:390px;top:226px;transform:rotate(-4deg)"></div>
 <div class="ty" style="position:absolute;left:60px;right:60px;top:790px;font-size:30px;line-height:1.6">{typed}</div>
 <div class="hand" style="position:absolute;left:60px;right:60px;top:1000px;font-size:60px;line-height:1.05;transform:rotate(-2deg)">{hand}</div>
 {stamp}<div class="no ty">{letter} / D</div></div>""")
exhibit('slide-2-exhibit-a','A','23:58:13',S['c1'],'Plate on counter. Both leopards present.<br>Parasols: up. Bamboo: still.<br>Behaviour: suspiciously calm.','“we’re just sitting here.”')
ring='<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border:6px solid #B3241B;border-radius:50%;transform:rotate(-6deg)"></div>'
exhibit('slide-3-exhibit-b','B','03:14:07',S['c2'],'Plate on counter. Stripes present.<br>Leopards: <u>not present</u>.<br>Parasols: also gone. (they took them.)','where do 2 leopards go at 3 am?',
        extra=ring.format(x=250,y=166,w=300,h=210))
exhibit('slide-4-exhibit-c','C','03:15:44',S['c3'],'16 prints in the flour, plate to window.<br>Size: small. Gait: elegant.<br>Material: suspected porcelain.','they went out for a walk.<br>in matching outfits.',
        extra=ring.format(x=136,y=140,w=420,h=210))
exhibit('slide-5-exhibit-d','D','06:58:41',S['c4'],'Both leopards back on plate.<br>Positions: exactly the same as before.<br>Statement: "we never left."','acting normal. too normal.',
        stamp='<div class="stamp" style="right:150px;top:1070px;font-size:30px;transform:rotate(6deg)">FLOUR ON THE PAWS</div>')
# 6 verdict
shoot('slide-6-verdict',f"""<div class="sheet" style="transform:rotate(.6deg)">
 <div class="hdr ty">VERDICT · CASE No. 24/26<b>CASE CLOSED.</b></div>
 <div style="position:absolute;left:190px;top:215px;width:560px;height:560px;background:url({PL}) center/contain no-repeat;filter:drop-shadow(0 14px 18px rgba(0,0,0,.3))"></div>
 <div class="stamp" style="left:560px;top:800px;font-size:36px;transform:rotate(-8deg)">RETURNED<br>FOR DINNER</div>
 <div class="ty" style="position:absolute;left:60px;right:60px;top:940px;font-size:30px;line-height:1.6">Finding: the leopards always come home<br>in time to be served on.<br>Sentence: dinner for six, every Friday.</div>
 <div class="ty" style="position:absolute;left:60px;right:60px;bottom:52px;font-size:21px;letter-spacing:.1em;border-top:2px solid #231d18;padding-top:14px">STITCHES OF THE WILD · 24 PIECES FOR SIX · PERSET.SHOP</div></div>""")
