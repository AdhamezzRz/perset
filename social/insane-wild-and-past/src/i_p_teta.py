from reel import *
OUT=os.path.abspath('../ins/out'); d=os.path.abspath('../ins/teta'); os.makedirs(d,exist_ok=True)
hero=img(SCR+'/src/past-1-perset-past-dinner-hero.jpg')
im=Image.open(SCR+'/salad/salad_cut.png').convert('RGBA'); bg=Image.new('RGBA',im.size,(242,214,214,255)); bg.alpha_composite(im); bg.convert('RGB').resize((800,800)).save(f'{d}/salad.jpg',quality=90)
salad=img(f'{d}/salad.jpg')
def wave(n=38,seed=1):
    import random; r=random.Random(seed); return ''.join(f'<i style="height:{r.randint(8,46)}px"></i>' for _ in range(n))
msgs=[ # (t, side, html)
 (0.4,'l',f'<div class="vn" data-a="0.6" data-b="3.2"><div class="pl">▶</div><div class="wv">{wave(38,1)}</div><div class="du">0:14</div></div><div class="tr" data-a="0.8" data-b="3.2">Habibti… I saw the plates. The peacock ones. On the Instagram.</div>'),
 (3.6,'l',f'<img class="ph" src="{hero}">'),
 (4.6,'l','these are ours now?'),
 (5.9,'r','teta it’s a set for six'),
 (7.3,'l','then we invite six.'),
 (8.5,'r','and the salad plates?'),
 (9.6,'l',f'<div class="vn" data-a="9.8" data-b="11.6"><div class="pl">▶</div><div class="wv">{wave(26,2)}</div><div class="du">0:06</div></div><div class="tr" data-a="10.0" data-b="11.6">salad first. then the peacock. like your grandfather liked.</div>'),
 (12.0,'l',f'<img class="ph" src="{salad}">'),
 (13.1,'l','and NOT in the nish.'),
]
bub=''.join(f'<div class="m {s}" data-t="{t}"><div class="b">{h}</div><div class="tm">13:{7+i:02d}</div></div>' for i,(t,s,h) in enumerate(msgs))
css="""
.bg{background:#EFE3D3!important}.fibers{opacity:.25}
#top{position:absolute;left:0;right:0;top:0;height:230px;background:#500C02;color:#FBF3E6;z-index:5}
#sb{position:absolute;left:44px;right:44px;top:22px;display:flex;justify-content:space-between;font-size:30px;font-weight:500}
#who{position:absolute;left:44px;top:100px;display:flex;align-items:center;gap:26px}
#av{width:96px;height:96px;border-radius:50%;background:#F2A4B6;color:#500C02;font-family:'Damion';font-size:64px;display:flex;align-items:center;justify-content:center}
#nm{font-size:44px;font-weight:500;line-height:1.1}#st{font-size:28px;color:#F2C9C0}
#feed{position:absolute;left:0;right:0;top:230px;bottom:150px;overflow:hidden}
#col{position:absolute;left:0;right:0;top:0;padding:30px 40px;display:flex;flex-direction:column;gap:22px}
.m{display:flex;flex-direction:column;max-width:780px;opacity:0}
.m.l{align-self:flex-start}.m.r{align-self:flex-end;align-items:flex-end}
.b{background:#FBF8F2;color:#2a1a16;font-size:44px;line-height:1.25;padding:22px 30px;border-radius:34px;border-top-left-radius:8px;box-shadow:0 3px 10px rgba(80,12,2,.08)}
.m.r .b{background:#F7C9CF;border-top-left-radius:34px;border-top-right-radius:8px}
.tm{font-size:22px;color:#8a6a5a;margin:6px 14px 0}
.ph{display:block;width:620px;height:620px;object-fit:cover;border-radius:22px}
.vn{display:flex;align-items:center;gap:20px;width:640px}
.pl{width:70px;height:70px;border-radius:50%;background:#500C02;color:#FBF3E6;font-size:30px;display:flex;align-items:center;justify-content:center;flex:none}
.wv{display:flex;align-items:center;gap:5px;height:60px;flex:1}.wv i{display:block;width:7px;border-radius:4px;background:#C9A08F}
.du{font-size:26px;color:#8a6a5a}
.tr{font-family:'Caveat';font-size:44px;color:#5a2a1a;margin-top:10px;min-height:20px}
#bar{position:absolute;left:0;right:0;bottom:0;height:150px;background:#FBF8F2;display:flex;align-items:center;padding:0 40px;gap:24px}
#in{flex:1;height:90px;border-radius:45px;background:#EFE3D3;font-size:36px;color:#9a8072;display:flex;align-items:center;padding:0 34px}
#mic{width:90px;height:90px;border-radius:50%;background:#500C02}
#typ{position:absolute;left:40px;bottom:170px;background:#FBF8F2;border-radius:30px;padding:18px 26px;font-size:40px;color:#8a6a5a;opacity:0}
#end{position:absolute;inset:0;background:rgba(80,12,2,.92);display:flex;flex-direction:column;align-items:center;justify-content:center;opacity:0;z-index:10}
#end .a{font-family:'Damion';font-size:150px;color:#FBF3E6;line-height:1}
#end .b2{font-size:34px;letter-spacing:.3em;text-transform:uppercase;color:#F2A4B6;margin-top:30px}
#end .c{width:300px;height:163px;background:#F2A4B6;margin-top:70px}
#end .u{font-size:28px;letter-spacing:.34em;text-transform:uppercase;color:#FBF3E6;margin-top:24px}
"""
body=f"""<div id="top"><div id="sb"><span>13:07</span><span>▮▮▮ 86%</span></div><div id="who"><div id="av">T</div><div><div id="nm">Teta</div><div id="st" id="stt">online</div></div></div></div>
<div id="feed"><div id="col">{bub}</div></div><div id="typ">Teta is typing…</div>
<div id="bar"><div id="in">Message</div><div id="mic"></div></div>
<div id="end"><div class="a">Teta-approved.</div><div class="b2">pretty past · a set for six</div><div class="c logo"></div><div class="u">perset.shop</div></div>"""
js="""const M=[...document.querySelectorAll('.m')];const col=document.getElementById('col');
window.setT=t=>{let shown=[];M.forEach(m=>{const a=+m.dataset.t;const k=ease.out(seg(t,a,.35));m.style.opacity=k;m.style.transform=`translateY(${(1-k)*30}px) scale(${0.96+0.04*k})`;m.style.display=t>=a-0.01?'flex':'none';});
 const h=col.scrollHeight, view=document.getElementById('feed').clientHeight; col.style.transform=`translateY(${Math.min(0,view-h-10)}px)`;
 document.querySelectorAll('.vn').forEach(v=>{const a=+v.dataset.a,b=+v.dataset.b;const u=Math.max(0,Math.min(1,(t-a)/(b-a)));const bars=[...v.querySelectorAll('.wv i')];bars.forEach((x,i)=>x.style.background=(i/bars.length<u)?'#500C02':'#C9A08F');v.querySelector('.pl').textContent=(t>a&&t<b)?'❚❚':'▶';});
 document.querySelectorAll('.tr').forEach(e=>{const a=+e.dataset.a,b=+e.dataset.b;if(!e.dataset.full)e.dataset.full=e.textContent;const f=e.dataset.full;const n=Math.floor(Math.max(0,Math.min(1,(t-a)/(b-a)))*f.length);e.textContent=f.slice(0,n);});
 const ty=document.getElementById('typ');ty.style.opacity=((t>6.5&&t<7.25)||(t>12.5&&t<13.05))?1:0;
 const en=document.getElementById('end');const k=ease.out(seg(t,14.6,.6));en.style.opacity=k;};window.setT(0);"""
open(f'{d}/p.html','w').write(page(css,body,js,W=1080,H=1920,bgc='#EFE3D3'))
run(f'cd "{d}" && VW=1080 VH=1920 {NODE} {SCR}/pack/render.js p.html fr {FPS} 17.5 jpeg 0')
run(f'{FF} -v error -y -framerate {FPS} -i "{d}/fr/f%04d.jpg" -vf "format=yuv420p" -c:v libx264 -crf 18 -preset slow -movflags +faststart "{OUT}/past-reel-3-teta-voice-note.mp4"')
