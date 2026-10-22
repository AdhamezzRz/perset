from wc import *
jpg('ex/g20_nish_salad.png','a/p_nish.jpg',1080,1350,box=(0,330,1520,2230),q=94)
css=f"""
.photo{{position:absolute;inset:0;background:url({img('a/p_nish.jpg')}) center/cover}}
.note{{position:absolute;font-family:'Caveat',cursive;line-height:1.02;padding:26px 26px 22px;box-shadow:0 10px 16px rgba(20,8,0,.35),0 1px 2px rgba(20,8,0,.4)}}
.old{{left:118px;top:540px;width:330px;background:linear-gradient(170deg,#F3E7C9,#E8D6AE);color:#1F2C5C;font-size:50px;transform:rotate(-4deg)}}
.old:after{{content:'';position:absolute;inset:0;background:radial-gradient(circle at 80% 85%,rgba(140,100,40,.18),rgba(0,0,0,0) 40%),radial-gradient(circle at 15% 10%,rgba(140,100,40,.12),rgba(0,0,0,0) 30%)}}
.new{{left:612px;top:556px;width:316px;height:316px;background:#F7B7C4;color:#3A1010;font-size:49px;transform:rotate(5deg)}}
.tape{{position:absolute;height:40px;width:120px;background:rgba(240,232,210,.78);mix-blend-mode:normal;box-shadow:0 1px 2px rgba(0,0,0,.15)}}
s{{text-decoration-thickness:4px;text-decoration-color:#B0182C}}
"""
body=f"""<div class="photo"></div>
<div class="note old"><b style="font-weight:400;font-size:62px">GUESTS ONLY.</b><br><s>do not touch.</s><br><span style="font-size:44px">— Teta, 1987</span><div class="tape" style="left:100px;top:-18px;transform:rotate(-6deg)"></div></div>
<div class="note new">update:<br>use them on<br>Tuesdays.<br><span style="font-size:44px">— also Teta ♡</span><div class="tape" style="left:110px;top:-20px;transform:rotate(4deg);background:rgba(250,245,235,.6)"></div></div>"""
open('out/p_s1_nish_rules.html','w').write(page(css,body,'',W=1080,H=1350,bgc='#222',fibers=False))
