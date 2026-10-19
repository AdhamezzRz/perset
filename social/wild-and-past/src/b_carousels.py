from wc import *
os.makedirs('out/cw',exist_ok=True); os.makedirs('out/cp',exist_ok=True)
for k in ['g10_denim','g11_velvet','g12_silk','g13_beach']: jpg(f'ex/{k}.png',f'a/{k}.jpg',1080,1350,q=93)
# ---------- Wild: Leopard is a neutral
cover_css=f"""
.pl{{position:absolute;left:150px;top:560px;width:900px;height:900px;background:url({img(SCR+'/pack/assets/wild_hi.png')}) center/contain no-repeat;transform:rotate(-8deg);filter:drop-shadow(0 30px 36px rgba(80,12,2,.30)) drop-shadow(0 3px 4px rgba(80,12,2,.3))}}
.h{{position:absolute;left:70px;top:110px;font-family:'Fraunces';font-style:italic;font-weight:400;font-size:132px;line-height:.92;color:#500C02;font-variation-settings:'SOFT' 100,'opsz' 144}}
.e{{position:absolute;left:76px;top:70px;font-size:20px;letter-spacing:.32em;text-transform:uppercase;color:#8a2a1a}}
.s{{position:absolute;left:76px;top:430px;font-family:'Caveat';font-size:48px;color:#500C02}}
"""
open('out/cw/01-cover.html','w').write(page(cover_css,'<div class="e">stitches of the wild · a styling note</div><div class="h">Leopard<br>is a neutral.</div><div class="s">here is the proof →</div><div class="pl"></div>','',bgc='#F3C9C9'))
looks=[('a/g10_denim.jpg','01','with denim.','saturday, sunglasses on.'),('a/g12_silk.jpg','02','with silk.','for the slow mornings.'),('a/g13_beach.jpg','03','with sand.','sahel, obviously.'),('a/g11_velvet.jpg','04','with velvet.','for the dinner that runs late.')]
lcss="""
.photo{position:absolute;inset:0;background-size:cover;background-position:center}
.tag{position:absolute;left:56px;bottom:56px;background:#FBF8F2;padding:20px 28px 22px;box-shadow:0 10px 24px rgba(0,0,0,.18)}
.tag .k{font-size:16px;letter-spacing:.32em;text-transform:uppercase;color:#8a2a1a}
.tag .w{font-family:'Fraunces';font-style:italic;font-size:62px;line-height:1;color:#500C02;margin-top:6px;font-variation-settings:'SOFT' 100,'opsz' 144}
.tag .n{font-family:'Caveat';font-size:34px;color:#3a2a22;margin-top:2px}
"""
for i,(p,n,w,s) in enumerate(looks):
    open(f'out/cw/0{i+2}-look-{n}.html','w').write(page(lcss,f'<div class="photo" style="background-image:url({img(p)})"></div><div class="tag"><div class="k">look {n} · leopard</div><div class="w">{w}</div><div class="n">{s}</div></div>','',bgc='#222',fibers=False))
ecss="""
#c{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.h{font-family:'Fraunces';font-style:italic;font-size:96px;line-height:1;color:#F4EEE4;font-variation-settings:'SOFT' 100,'opsz' 144}
.s{font-family:'Caveat';font-size:46px;color:#F2A4B6;margin-top:22px}
.e{font-size:20px;letter-spacing:.32em;text-transform:uppercase;color:#F2A4B6;margin-top:70px}
.lg{width:280px;height:152px;background:#F2A4B6;margin-top:26px}
.u{font-size:22px;letter-spacing:.34em;text-transform:uppercase;color:#F4EEE4;margin-top:24px}
.bg{background:#500C02!important}.fibers{opacity:.15}
"""
open('out/cw/06-end.html','w').write(page(ecss,'<div id="c"><div class="h">Goes with<br>everything<br>you own.</div><div class="s">including the friends you invite.</div><div class="e">stitches of the wild · a set for six</div><div class="lg logo"></div><div class="u">perset.shop</div></div>','',bgc='#500C02'))
# ---------- Past: Teta's album
acss=f"""
.bg{{background:#1E1A17!important}}.fibers{{opacity:.35;mix-blend-mode:screen}}
.pg{{position:absolute;inset:0;background:radial-gradient(ellipse at 40% 30%,rgba(255,255,255,.05),rgba(0,0,0,.25))}}
.ph{{position:absolute;background:#F4EEDF;padding:22px 22px 22px;box-shadow:0 14px 26px rgba(0,0,0,.55)}}
.ph div{{width:100%;height:100%;background-size:cover;background-position:center;filter:sepia(.12) contrast(.96)}}
.cn{{position:absolute;width:70px;height:70px;background:#0F0C0A;clip-path:polygon(0 0,100% 0,0 100%)}}
.cap{{position:absolute;font-family:'Caveat';color:#EDE6D6;line-height:1.05}}
"""
def corners(x,y,w,h):
    return (f'<div class="cn" style="left:{x-14}px;top:{y-14}px"></div><div class="cn" style="left:{x+w-56}px;top:{y-14}px;transform:scaleX(-1)"></div>'
            f'<div class="cn" style="left:{x-14}px;top:{y+h-56}px;transform:scaleY(-1)"></div><div class="cn" style="left:{x+w-56}px;top:{y+h-56}px;transform:scale(-1,-1)"></div>')
def photo(src,x,y,w,h,rot):
    return f'<div style="position:absolute;left:0;top:0;width:1080px;height:1350px;transform:rotate({rot}deg);transform-origin:{x+w/2}px {y+h/2}px"><div class="ph" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"><div style="background-image:url({img(src)})"></div></div>{corners(x,y,w,h)}</div>'
for k in ['g17_album1','g18_album2','g19_album3']: jpg(f'ex/{k}.png',f'a/{k}.jpg',1100,1100,q=92)
open('out/cp/01-cover.html','w').write(page(acss,f'<div class="pg"></div>{photo("a/g18_album2.jpg",560,120,420,420,6)}<div class="cap" style="left:90px;top:640px;font-size:84px;width:900px">What if Pretty Past had been at every family lunch since 1978?</div><div class="cap" style="left:94px;top:1120px;font-size:44px;color:#C9A86A">swipe through the album →</div>','',bgc='#1E1A17'))
caps=[('a/g17_album1.jpg','Friday, 1978.','Baba\'s third plate of molokhia.'),('a/g18_album2.jpg','Alexandria, 1979.','Hesham vs. the basbousa.'),('a/g19_album3.jpg','Ramadan, 1982.','ten minutes to maghrib.')]
for i,(p,a,b) in enumerate(caps):
    rot=[-2.5,2,-1.5][i]
    open(f'out/cp/0{i+2}-album-{i+1}.html','w').write(page(acss,f'<div class="pg"></div>{photo(p,110,110,860,860,rot)}<div class="cap" style="left:120px;top:1040px;font-size:76px;transform:rotate(-2deg)">{a}</div><div class="cap" style="left:124px;top:1130px;font-size:58px;color:#D9CDB6;transform:rotate(-2deg)">{b}</div>','',bgc='#1E1A17'))
jpg(SCR+'/src/past-lifestyle.jpg','a/past_life.jpg',1100,1100,q=92)
open('out/cp/05-reveal.html','w').write(page(acss+".lg{position:absolute;left:740px;top:1150px;width:240px;height:130px;background:#EDE6D6}",f'<div class="pg"></div>{photo("a/past_life.jpg",110,90,860,860,1.5)}<div class="cap" style="left:120px;top:1000px;font-size:72px">Made in 2026.</div><div class="cap" style="left:122px;top:1080px;font-size:52px;color:#D9CDB6;width:620px">built for the next forty years of Fridays.</div><div class="cap" style="left:124px;top:1240px;font-family:Jost;font-size:20px;letter-spacing:.32em;text-transform:uppercase;color:#C9A86A">pretty past · perset.shop</div><div class="lg logo"></div>','',bgc='#1E1A17'))
