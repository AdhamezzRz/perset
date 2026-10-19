from wc import *
W,H=700,1060
tabs=''.join(f'<div class="tab" style="left:{8+i*68}px;{"visibility:hidden;" if i in (2,6) else ""}"><span>perset.shop</span></div>' for i in range(10))
css=f"""
html,body{{background:transparent}}
.bg,.fibers,.vig,.grain{{display:none}}
.p{{position:absolute;left:0;top:0;width:{W}px;height:930px;background:#F8F6F0;padding:34px 40px;color:#141414}}
.h{{font-family:'Fraunces',serif;font-weight:700;font-size:136px;line-height:.86;letter-spacing:-.02em;text-align:center;font-variation-settings:'SOFT' 0,'WONK' 0,'opsz' 144}}
.s{{text-align:center;font-weight:500;letter-spacing:.32em;text-transform:uppercase;font-size:21px;margin-top:14px}}
.ph{{width:620px;height:430px;margin:20px auto 0;background:#fff url({img(SCR+'/pack/assets/wild_hi.png')}) center/400px no-repeat;border:2px solid #141414;filter:saturate(.9) contrast(1.05)}}
.t{{font-size:25px;line-height:1.32;margin-top:18px;text-align:center}}
.t b{{font-weight:500}}
.f{{text-align:center;font-family:'Fraunces',serif;font-weight:700;font-size:40px;margin-top:10px}}
.tab{{position:absolute;top:930px;width:66px;height:130px;background:#F8F6F0;border-left:1px dashed rgba(0,0,0,.35)}}
.tab span{{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%) rotate(-90deg);white-space:nowrap;font-size:16px;font-weight:500;letter-spacing:.06em}}
"""
body=f"""<div class="p"><div class="h">SPOTTED</div><div class="s">two leopards · zamalek</div><div class="ph"></div>
<div class="t">Last seen under two pink parasols at <b>a dinner for six.</b><br>Friendly. Very well dressed.<br>Answers to "dinner's ready".</div>
<div class="f">If found: perset.shop</div><div class="t" style="font-size:19px;margin-top:14px;letter-spacing:.2em;text-transform:uppercase">do not approach before dessert</div></div>{tabs}"""
open('out/poster_flat.html','w').write(page(css,body,'',W=W,H=H,bgc='transparent',fibers=False))
