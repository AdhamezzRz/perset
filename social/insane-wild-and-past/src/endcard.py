from reel import *
def endcard(name, plate, coll, line, out, bgc='#F2EBDD', ink='#500C02', accent='#C9566B', dur=3.0):
    d=f'{WP}/ec_{name}'; os.makedirs(d,exist_ok=True)
    css=f"""
#pl{{position:absolute;left:220px;top:330px;width:640px;height:640px;background:url({img(plate)}) center/contain no-repeat;filter:drop-shadow(0 26px 30px rgba(60,35,20,.30)) drop-shadow(0 3px 4px rgba(60,35,20,.3))}}
#c{{position:absolute;left:0;right:0;top:1030px;text-align:center;font-family:'Damion';font-size:118px;color:{ink};line-height:1}}
#l{{position:absolute;left:0;right:0;top:1190px;text-align:center;font-family:'Jost';font-weight:500;letter-spacing:.32em;text-transform:uppercase;font-size:24px;color:{accent}}}
#lg{{position:absolute;left:390px;top:1330px;width:300px;height:163px;background:{ink}}}
#u{{position:absolute;left:0;right:0;top:1530px;text-align:center;font-family:'Jost';font-weight:500;letter-spacing:.34em;text-transform:uppercase;font-size:26px;color:{ink}}}
"""
    body=f'<div id="pl"></div><div id="c">{coll}</div><div id="l">{line}</div><div id="lg" class="logo"></div><div id="u">perset.shop</div>'
    js="""
window.setT=t=>{const a=ease.out(seg(t,0,1.1));const pl=document.getElementById('pl');pl.style.transform=`scale(${0.86+0.14*a}) rotate(${-14*(1-a)}deg)`;pl.style.opacity=seg(t,0,.25);
[['c',.45],['l',.75],['lg',1.0],['u',1.15]].forEach(([id,s])=>{const e=document.getElementById(id);const k=ease.out(seg(t,s,.5));e.style.opacity=k;e.style.transform=`translateY(${(1-k)*26}px)`;});};
window.setT(0);"""
    open(f'{d}/ec.html','w').write(page(css,body,js,W=1080,H=1920,bgc=bgc))
    run(f'cd "{d}" && {NODE} {SCR}/pack/render.js ec.html fr {FPS} {dur} jpeg 0')
    run(f'{FF} -v error -y -framerate {FPS} -i "{d}/fr/f%04d.jpg" -c:v libx264 -crf 15 -pix_fmt yuv420p "{out}"')
    return out
if __name__=='__main__':
    os.makedirs('seg',exist_ok=True)
    endcard('wild',SCR+'/pack/assets/wild_hi.png','Stitches of the Wild','a set for six · 24 pieces','seg/end_wild.mp4')
    endcard('past',SCR+'/cutouts/past_dinner.png','Pretty Past','a set for six · 24 pieces','seg/end_past.mp4',accent='#B8860B')
