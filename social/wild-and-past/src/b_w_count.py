from wc import *
jpg('ex/g01_symtable.png','a/w_count.jpg',1080,1350,box=(0,376,1520,2276),q=94)
INK='#FBF3E6'
loops=[(387,800,120,95,3,-8),(707,515,70,62,5,0),(556,640,46,155,7,0)]
arrows=[(250,1150,330,905,4,-30),(870,215,750,445,6,30),(700,1180,590,830,8,25)]
sv=''.join(f'<path d="{loop_path(cx,cy,rx,ry,s)}" transform="rotate({r} {cx} {cy})"/>' for cx,cy,rx,ry,s,r in loops)
sv+=''.join(f'<path d="{squiggle(x1,y1,x2,y2,s,b)}"/><path d="{arrowhead(x2,y2,x1,y1,24,s)}"/>' for x1,y1,x2,y2,s,b in arrows)
css=f"""
.photo{{position:absolute;inset:0;background:url({img('a/w_count.jpg')}) center/cover}}
svg.pen{{position:absolute;left:0;top:0;filter:drop-shadow(0 2px 5px rgba(20,8,0,.6))}}
svg.pen path{{fill:none;stroke:{INK};stroke-width:5.5;stroke-linecap:round;stroke-linejoin:round}}
.n{{position:absolute;font-family:'Caveat',cursive;font-weight:400;color:{INK};line-height:.95;-webkit-text-stroke:1.2px #FBF3E6;text-shadow:0 2px 12px rgba(20,8,0,.75)}}
.h{{position:absolute;left:60px;top:60px;font-family:'Damion';font-size:84px;color:{INK};text-shadow:0 3px 16px rgba(20,8,0,.7);line-height:1}}
"""
body=f"""<div class="photo"></div><svg class="pen" width="1080" height="1350">{sv}</svg>
<div class="h">A set for six<br>comes with:</div>
<div class="n" style="left:770px;top:110px;font-size:62px;transform:rotate(4deg)">12 parasols</div>
<div class="n" style="left:70px;top:1160px;font-size:66px;transform:rotate(-4deg)">12 leopards</div>
<div class="n" style="left:610px;top:1170px;font-size:58px;transform:rotate(3deg)">6 bamboo groves</div>
<div class="n" style="left:0;right:0;text-align:center;top:1262px;font-size:48px">and 0 arguments about shade.</div>"""
open('out/w_s3_set_comes_with.html','w').write(page(css,body,'',W=1080,H=1350,bgc='#222',fibers=False))
