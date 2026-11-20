from wc import *
import subprocess
OUT=os.path.abspath('../ins/out/past-carousel-lot-24'); os.makedirs(OUT,exist_ok=True)
PH=img(SCR+'/src/past-1-perset-past-dinner-hero.jpg'); PL=img(SCR+'/cutouts/past_dinner.png'); SL=img(SCR+'/salad/salad_cut.png')
css="""
.bg{background:#F4EFE4!important}
.ser{font-family:'Fraunces';color:#1b1714}
.sans{font-family:'Jost';font-weight:500;letter-spacing:.32em;text-transform:uppercase;color:#1b1714}
.rule{position:absolute;left:90px;right:90px;height:0;border-top:1.5px solid #1b1714}
.hd{position:absolute;left:90px;right:90px;top:70px;display:flex;justify-content:space-between;font-size:18px}
.ft{position:absolute;left:90px;right:90px;bottom:62px;display:flex;justify-content:space-between;font-size:16px;color:#6b5f55}
.pl{position:absolute;border-radius:50%;filter:drop-shadow(0 22px 22px rgba(40,25,10,.22)) drop-shadow(0 3px 4px rgba(40,25,10,.2))}
.lot{position:absolute;left:90px;font-size:150px;font-weight:300;line-height:1}
.desc{position:absolute;left:90px;right:90px;font-size:30px;line-height:1.45}
.est{position:absolute;left:90px;right:90px;font-size:20px}
.est b{display:block;font-family:'Fraunces';font-weight:400;letter-spacing:0;text-transform:none;font-size:38px;margin-top:8px;font-style:italic}
"""
def shoot(name,body,n):
    hd=f'<div class="hd sans"><span>The Friday Sale</span><span>Cairo</span></div><div class="rule" style="top:110px"></div>'
    ft=f'<div class="ft sans"><span>Important porcelain for six</span><span>{n} / 5</span></div>'
    f=f'{OUT}/{name}.html'; open(f,'w').write(page(css,hd+body+ft,'',W=1080,H=1350,bgc='#F4EFE4',fibers=True))
    subprocess.run(f'cd {OUT} && NODE_PATH=$(npm root -g) node {SCR}/pack/shoot.js 1080 1350 {name}.html && rm {name}.html',shell=True,check=True)
shoot('slide-1-cover',f"""
<div class="ser" style="position:absolute;left:0;right:0;top:170px;text-align:center;font-size:108px;font-weight:300;line-height:.95">The Friday<br><i>Sale</i></div>
<div class="sans" style="position:absolute;left:0;right:0;top:400px;text-align:center;font-size:20px">Important porcelain for six</div>
<div style="position:absolute;left:190px;top:470px;width:700px;height:700px;background:url({PH}) center/cover;box-shadow:0 20px 40px rgba(40,25,10,.18)"></div>
<div class="ser" style="position:absolute;left:0;right:0;top:1196px;text-align:center;font-size:30px;font-style:italic">Friday, 8 pm. or whenever the food is ready.</div>""",1)
shoot('slide-2-lot-24',f"""
<div class="pl" style="left:240px;top:150px;width:600px;height:600px;background:url({PL}) center/contain no-repeat"></div>
<div class="lot ser" style="top:790px">24</div>
<div class="desc ser" style="left:330px;top:810px;font-size:29px">A <b>Pretty Past</b> dinner plate.<br>Porcelain. Cairo, 2026.<br><span style="color:#6b5f55">Saffron ground, painted with a blue peacock among pink roses, a border of peacock eyes.</span></div>
<div class="rule" style="top:1080px"></div>
<div class="est sans" style="top:1105px">Estimate<b>one invitation to dinner</b></div>""",2)
shoot('slide-3-lot-24a',f"""
<div class="pl" style="left:240px;top:150px;width:600px;height:600px;background:url({SL}) center/contain no-repeat"></div>
<div class="lot ser" style="top:790px">24<span style="font-size:80px">a</span></div>
<div class="desc ser" style="left:380px;top:810px;font-size:29px">The salad plate, en suite.<br><span style="color:#6b5f55">Pink border of coral flowers and peacock eyes, a white ring, a saffron centre. Traditionally arrives first.</span></div>
<div class="rule" style="top:1080px"></div>
<div class="est sans" style="top:1105px">Estimate<b>second helpings</b></div>""",3)
rows=[('Chips','none'),('Cracks','none'),('Peacock','one. very vain.'),('Roses','in bloom. permanently.'),('Glaze','glossy enough to check your lipstick in'),('Previous owners','none yet. it starts with you.'),('Provenance','perset.shop')]
tbl=''.join(f'<div style="display:flex;border-bottom:1px solid rgba(27,23,20,.25);padding:20px 0"><div class="sans" style="width:300px;font-size:18px;padding-top:8px">{k}</div><div class="ser" style="flex:1;font-size:34px;font-style:italic">{v}</div></div>' for k,v in rows)
shoot('slide-4-condition-report',f"""
<div class="ser" style="position:absolute;left:90px;top:160px;font-size:76px;font-weight:300;line-height:1">Condition<br>report <span style="font-size:40px;color:#6b5f55">· lot 24</span></div>
<div style="position:absolute;left:90px;right:90px;top:360px">{tbl}</div>
<div class="pl" style="right:70px;top:1010px;width:230px;height:230px;background:url({PL}) center/contain no-repeat;transform:rotate(-8deg)"></div>""",4)
bids=[('Room','12 aunties'),('Phone','4 cousins'),('Online','1 mother-in-law'),('Absentee','Teta. sent a voice note.')]
bt=''.join(f'<div style="display:flex;border-bottom:1px solid rgba(27,23,20,.25);padding:18px 0"><div class="sans" style="width:300px;font-size:18px;padding-top:8px">{k}</div><div class="ser" style="flex:1;font-size:36px">{v}</div></div>' for k,v in bids)
shoot('slide-5-sold',f"""
<div class="ser" style="position:absolute;left:90px;top:160px;font-size:76px;font-weight:300;line-height:1">Results</div>
<div style="position:absolute;left:90px;right:90px;top:270px">{bt}</div>
<div class="ser" style="position:absolute;left:0;right:0;top:640px;text-align:center;font-size:150px;font-weight:600;color:#8f1d14;letter-spacing:.04em">SOLD</div>
<div class="ser" style="position:absolute;left:0;right:0;top:815px;text-align:center;font-size:44px;font-style:italic">to whoever hosts on Friday.</div>
<div class="pl" style="left:230px;top:905px;width:300px;height:300px;background:url({PL}) center/contain no-repeat"></div>
<div class="pl" style="left:560px;top:935px;width:250px;height:250px;background:url({SL}) center/contain no-repeat"></div>
<div class="sans" style="position:absolute;left:0;right:0;top:1222px;text-align:center;font-size:18px">Pretty Past · 24 pieces for six · perset.shop</div>""",5)
