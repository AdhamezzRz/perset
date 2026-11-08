import reel
from reel import *
reel.W,reel.H=1080,1350
d=os.path.abspath('../tw/cap_speed'); os.makedirs(d,exist_ok=True)
# base: clip (5.04s) + 2.4s hold on the last frame, scaled to fill 4:5
run(f'{FF} -v error -y -i vid/k_breakfast_x.mp4 -vf "fps=30,scale=1350:1350,crop=1080:1350,tpad=stop_mode=clone:stop_duration=2.6" -c:v libx264 -crf 15 -pix_fmt yuv420p {d}/base.mp4')
css="""html,body{background:transparent}.bg,.fibers,.vig,.grain{display:none}
#hud{position:absolute;left:50px;top:50px;background:rgba(20,10,6,.72);color:#FBF3E6;border-radius:18px;padding:18px 26px 16px;font-family:'Jost';min-width:420px}
#hud .k{font-size:20px;letter-spacing:.3em;text-transform:uppercase;color:#F2A4B6}
#hud .t{font-family:'Fraunces';font-weight:400;font-size:84px;line-height:1;margin-top:6px;font-variant-numeric:tabular-nums}
#hud .s{font-size:22px;margin-top:6px;color:#e9d9c9}
#pb{position:absolute;left:50px;top:300px;background:#F2A4B6;color:#500C02;font-weight:500;font-size:34px;letter-spacing:.16em;padding:10px 22px;border-radius:12px;transform:rotate(-4deg)}
#end{position:absolute;left:0;right:0;top:1040px;text-align:center;font-family:'Damion';font-size:92px;line-height:1.02;color:#FBF3E6;text-shadow:0 3px 18px rgba(20,8,0,.65)}
#ft{position:absolute;left:0;right:0;top:1285px;text-align:center;font-size:20px;letter-spacing:.3em;text-transform:uppercase;color:#FBF3E6;text-shadow:0 2px 10px rgba(20,8,0,.7)}
"""
body='<div id="hud"><div class="k">breakfast speedrun · any%</div><div class="t" id="tm">00:00.00</div><div class="s" id="sp">cairo · 6 guests · 1 palm</div></div><div id="pb">NEW PERSONAL BEST</div><div id="end">breakfast for six:<br>5 seconds flat.</div><div id="ft">a tale in beads · perset.shop</div>'
js="""window.setT=t=>{const run=Math.min(t,5.04);const s=Math.floor(run),cs=Math.floor((run-s)*100);
document.getElementById('tm').textContent=`00:0${s}.${String(cs).padStart(2,'0')}`;
const k=ease.back(seg(t,5.1,.35));const pb=document.getElementById('pb');pb.style.opacity=seg(t,5.1,.1);pb.style.transform=`rotate(-4deg) scale(${0.6+0.4*k})`;
const e=document.getElementById('end');const ke=ease.out(seg(t,5.5,.6));e.style.opacity=ke;e.style.transform=`translateY(${(1-ke)*30}px)`;document.getElementById('ft').style.opacity=seg(t,5.9,.5);};window.setT(0);"""
open(f'{d}/hud.html','w').write(page(css,body,js,W=1080,H=1350,bgc='transparent',fibers=False))
run(f'cd {d} && VW=1080 VH=1350 {NODE} {SCR}/pack/render.js hud.html fr {FPS} 7.6 png 1')
run(f'{FF} -v error -y -i {d}/base.mp4 -framerate {FPS} -i {d}/fr/f%04d.png -filter_complex "[0:v][1:v]overlay=0:0:shortest=1,noise=alls=5:allf=t,format=yuv420p" -c:v libx264 -crf 18 -preset slow -movflags +faststart {os.path.abspath("../tw/out/beads-post-2-breakfast-speedrun.mp4")}')
