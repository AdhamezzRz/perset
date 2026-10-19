from wc import *
def stamp(src,val,title,bg,fit='cover',rot=0,x=0,y=0):
    return f'''<div class="st" style="left:{x}px;top:{y}px;transform:rotate({rot}deg)"><div class="in" style="background:{bg}">
<div class="im" style="background-image:url({img(src)});background-size:{fit}"></div>
<div class="v">{val}</div><div class="t">{title}</div><div class="po">per set post · cairo</div></div></div>'''
css=f"""
.table{{position:absolute;inset:0;background:#7B5338;background-image:repeating-linear-gradient(92deg,rgba(0,0,0,.06) 0 3px,rgba(255,255,255,.03) 3px 9px)}}
.env{{position:absolute;left:40px;top:70px;width:1000px;height:1210px;background:#F1E6D0;transform:rotate(-1.5deg);box-shadow:0 24px 40px rgba(20,8,0,.45),0 3px 5px rgba(20,8,0,.4);overflow:hidden}}
.env:before{{content:'';position:absolute;inset:0;border:22px solid transparent;border-image:repeating-linear-gradient(45deg,#B5323A 0 26px,#F1E6D0 26px 40px,#2F4B8A 40px 66px,#F1E6D0 66px 80px) 22}}
.env:after{{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at 30% 20%,rgba(255,255,255,.25),rgba(0,0,0,0) 60%),radial-gradient(ellipse at 90% 100%,rgba(120,80,30,.18),rgba(0,0,0,0) 50%)}}
.st{{position:absolute;width:260px;height:318px;background:#FBF6EA;padding:12px;filter:drop-shadow(0 3px 3px rgba(40,20,5,.35));
 -webkit-mask:radial-gradient(circle at 50% 50%,transparent 6px,#000 6.6px) -10px -10px/20px 20px repeat,linear-gradient(#000,#000) content-box;-webkit-mask-composite:source-over;padding:10px;}}
.st .in{{position:relative;width:100%;height:100%;overflow:hidden;outline:2px solid #FBF6EA;outline-offset:-1px}}
.st .im{{position:absolute;left:10px;right:10px;top:10px;bottom:62px;background-position:center;background-repeat:no-repeat}}
.st .v{{position:absolute;right:12px;top:14px;font-family:'Fraunces';font-weight:700;font-size:30px;color:#500C02;text-shadow:0 0 6px rgba(255,255,255,.8)}}
.st .t{{position:absolute;left:0;right:0;bottom:30px;text-align:center;font-family:'Fraunces';font-style:italic;font-size:24px;color:#2a1a16}}
.st .po{{position:absolute;left:0;right:0;bottom:10px;text-align:center;font-size:11px;letter-spacing:.24em;text-transform:uppercase;color:#6b4a3a}}
.pm{{position:absolute;left:330px;top:300px;width:250px;height:250px;border-radius:50%;border:5px solid rgba(30,30,60,.55);transform:rotate(-12deg)}}
.pm:before{{content:'';position:absolute;inset:16px;border-radius:50%;border:2px solid rgba(30,30,60,.5)}}
.pm span{{position:absolute;left:0;right:0;top:92px;text-align:center;font-weight:500;letter-spacing:.2em;font-size:22px;color:rgba(30,30,60,.6);line-height:1.5}}
.wv{{position:absolute;left:560px;top:330px;width:330px;height:190px;transform:rotate(-12deg)}}
.addr{{position:absolute;left:120px;top:760px;font-family:'Caveat';font-size:62px;line-height:1.08;color:#24346B;transform:rotate(-2deg)}}
.ret{{position:absolute;left:84px;top:88px;font-size:18px;letter-spacing:.24em;text-transform:uppercase;color:#6b4a3a;line-height:1.7}}
.sig{{position:absolute;left:0;right:60px;text-align:right;top:1100px;font-family:'Damion';font-size:66px;color:#500C02;transform:rotate(-3deg)}}
"""
waves=''.join(f'<path d="M0 {20+i*36} q 27 -14 55 0 t 55 0 t 55 0 t 55 0 t 55 0 t 55 0" fill="none" stroke="rgba(30,30,60,.5)" stroke-width="4"/>' for i in range(5))
body=f"""<div class="table"></div><div class="env">
<div class="ret">from: per set<br>perset.shop<br>cairo</div>
{stamp(SCR+'/cutouts/past_dinner.png','24','Pretty Past','#F4C430','92%',3,470,60)}
{stamp('a/st_peacock.png','1','the peacock','#F7E9B0','cover',-2,730,60)}
{stamp('a/st_rose.png','10','the roses','#F7E9B0','cover',-4,470,400)}
{stamp(SCR+'/cutouts/past_soup.png','6','the soup bowl','#F4C430','90%',2,730,400)}
<div class="pm"><span>CAIRO<br>· 2026 ·</span></div><svg class="wv" viewBox="0 0 330 190">{waves}</svg>
<div class="addr">To: the good table<br>whoever's hosting Friday<br>Cairo</div>
<div class="sig">Sent with love, from the past.</div></div>"""
open('out/p_s3_from_the_past.html','w').write(page(css,body,'',W=1080,H=1350,bgc='#7B5338',fibers=False))
