from wc import *
jpg('ex/g16_omali.png','a/p_omali.jpg',1080,1350,q=94)
css=f"""
.photo{{position:absolute;inset:0;background:url({img('a/p_omali.jpg')}) center/cover}}
.card{{position:absolute;left:520px;top:860px;width:500px;height:340px;transform:rotate(-7deg);background:#FBF7EE;filter:sepia(.22) brightness(.94) contrast(.98);
 background-image:repeating-linear-gradient(180deg,rgba(0,0,0,0) 0,rgba(0,0,0,0) 37px,rgba(70,110,170,.35) 37px,rgba(70,110,170,.35) 38px);background-position:0 60px;
 box-shadow:0 14px 18px rgba(40,20,5,.35),0 2px 3px rgba(40,20,5,.35);padding:12px 26px;font-family:'Caveat',cursive;color:#3B3A55;font-size:31px;line-height:38px}}
.card:before{{content:'';position:absolute;left:0;right:0;top:56px;height:2px;background:rgba(200,60,70,.45)}}
.card h{{display:block;font-size:46px;line-height:46px;color:#500C02;margin-bottom:8px}}
.ring{{position:absolute;left:330px;top:240px;width:120px;height:120px;border-radius:50%;border:7px solid rgba(120,70,30,.18);filter:blur(1px)}}
"""
body="""<div class="photo"></div><div class="card"><h>Teta's Om Ali</h>
3 croissants (don't tell anyone)<br>milk, cream, a little sugar<br>nuts, coconut, raisins<br>bake till golden. serve in the good bowls.<br><span style="color:#500C02">update: the good plates too. — T.</span><div class="ring"></div></div>"""
open('out/p_s2_teta_om_ali.html','w').write(page(css,body,'',W=1080,H=1350,bgc='#222',fibers=False))
