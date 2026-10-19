from reel import *
from wc import loop_path
OX,OY=90,550
R=[(490,150,80),(678,212,44),(585,330,78),(770,440,56),(330,700,88),(325,562,28),(130,490,52),(172,275,52),(222,340,30),(405,280,36)]
paths=''.join(f'<path class="lp" id="lp{i}" pathLength="1" d="{loop_path(OX+x,OY+y,r*1.15,r*1.05,i+3)}"/>' for i,(x,y,r) in enumerate(R))
paths+=f'<path class="lp" id="lpk" pathLength="1" d="{loop_path(OX+320,OY+390,150,250,9)}" transform="rotate(-14 {OX+320} {OY+390})"/>'
css=f"""
#pl{{position:absolute;left:{OX}px;top:{OY}px;width:900px;height:900px;background:url({img(SCR+'/cutouts/past_dinner.png')}) center/contain no-repeat;filter:drop-shadow(0 26px 30px rgba(60,35,20,.30)) drop-shadow(0 3px 4px rgba(60,35,20,.3))}}
svg{{position:absolute;left:0;top:0}}
.lp{{fill:none;stroke:#500C02;stroke-width:7;stroke-linecap:round;stroke-dasharray:1;stroke-dashoffset:1}}
.chip{{position:absolute;left:50%;transform:translateX(-50%);background:#FBF8F2;color:#1E1410;font-weight:500;font-size:46px;padding:14px 30px 18px;border-radius:16px;white-space:nowrap;box-shadow:0 6px 18px rgba(0,0,0,.12);text-align:center}}
#n{{position:absolute;left:0;right:0;top:1500px;text-align:center;font-family:'Damion';font-size:230px;color:#500C02;line-height:1}}
#cd{{position:absolute;left:0;right:0;top:1520px;text-align:center;font-family:'Damion';font-size:200px;color:#C9566B;line-height:1}}
#bar{{position:absolute;left:190px;top:1490px;width:700px;height:10px;border-radius:5px;background:rgba(80,12,2,.15)}}
#bar i{{display:block;height:100%;border-radius:5px;background:#500C02;width:100%}}
#pk{{position:absolute;left:0;right:0;top:1500px;text-align:center;font-family:'Damion';font-size:84px;color:#500C02;line-height:1.05}}
#sub{{position:absolute;left:0;right:0;top:360px;text-align:center;font-size:30px;color:#7a5a48;letter-spacing:.04em}}
"""
body=f"""<div id="pl"></div><svg width="1080" height="1920">{paths}</svg>
<div class="chip" id="c1" style="top:250px">how many roses are on this plate?</div>
<div id="sub">count before the line runs out. comment your number.</div>
<div id="bar"><i id="bi"></i></div><div id="cd"></div><div id="n"></div>
<div id="pk">+ 1 peacock<br><span style="font-size:60px">who thinks they're all his.</span></div>
<div class="chip" id="c2" style="top:250px">10 roses. buds count. we checked.</div>
<div class="chip" id="c3" style="top:250px">× 6 plates = 60 roses at one dinner.</div>"""
js="""
const T0=4.3,DT=0.42;
window.setT=t=>{
 const vis=(id,a,b,f=.2)=>{const e=document.getElementById(id);e.style.opacity=Math.min(seg(t,a,f),1-seg(t,b-f,f));};
 vis('c1',0.15,4.3);vis('sub',0.4,4.3);vis('bar',0.4,4.3);
 document.getElementById('bi').style.width=(100*(1-seg(t,0.5,3.6)))+'%';
 const cd=document.getElementById('cd');const k=t<2.7?'':t<3.3?'3':t<3.9?'2':t<4.3?'1':'';cd.textContent=k;
 let c=0;for(let i=0;i<10;i++){const s=T0+i*DT;const p=ease.out(seg(t,s,0.32));document.getElementById('lp'+i).style.strokeDashoffset=1-p;if(t>=s+0.12)c=i+1;}
 const n=document.getElementById('n');n.textContent=c?c:'';n.style.opacity=t<T0?0:(1-seg(t,8.7,0.2));
 n.style.transform=`scale(${1+0.12*Math.max(0,1-((t-T0)%DT)/0.15)})`;
 const pk=ease.out(seg(t,8.9,0.5));document.getElementById('lpk').style.strokeDashoffset=1-pk;
 vis('pk',9.0,12.6);vis('c2',8.8,10.8);vis('c3',10.8,12.6);
 document.querySelectorAll('.lp').forEach(e=>e.style.opacity=1-seg(t,12.4,0.2));
};window.setT(0);"""
d='cap_roses'; os.makedirs(d,exist_ok=True)
open(f'{d}/r.html','w').write(page(css,body,js,W=1080,H=1920,bgc='#F1E4CC'))
run(f'cd {d} && {NODE} {SCR}/pack/render.js r.html fr {FPS} 12.6 jpeg 0')
run(f'{FF} -v error -y -framerate {FPS} -i {d}/fr/f%04d.jpg -c:v libx264 -crf 15 -pix_fmt yuv420p seg/ro1.mp4')
compose([os.path.abspath('seg/ro1.mp4'),os.path.abspath('seg/end_past.mp4')],[],os.path.abspath('reels/past-reel-2-count-the-roses.mp4'))
