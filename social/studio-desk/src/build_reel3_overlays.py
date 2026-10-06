import sys; sys.path.insert(0,'..')
from common import *
def ov(name, word, sub, x, y, align='left', w=900, fs=190):
    css=f"""
    html,body{{background:transparent}} .bg,.fibers,.grain,.vig{{display:none}}
    #t{{position:absolute;left:{x}px;top:{y}px;width:{w}px;text-align:{align};color:#500C02;text-shadow:0 0 22px rgba(255,250,240,.55)}}
    #t .w{{font-family:'Damion',cursive;font-size:{fs}px;line-height:1}}
    #t .s{{font-size:25px;letter-spacing:.3em;text-transform:uppercase;margin-top:6px;margin-left:6px;opacity:.95}}
    """
    body=f'<div id="t"><div class="w">{word}</div><div class="s">{sub}</div></div>'
    open(name+'.html','w').write(page(css,body,'',W=1080,H=1920,bgc='transparent',fibers=False))
ov('o1','honey.','A Tale in Beads · 27 cm',60,1440,'right',960,170)
ov('o2','olive oil.','Pretty Past · 12 cm bowl',70,118,'left',620,118)
ov('o3','sumac.','Stitches of the Wild · 27 cm',70,112,'left',620,128)
# end card
css="""
.bg{background:#500C02!important}.fibers{opacity:.18}.grain{opacity:.14;mix-blend-mode:screen}.vig{display:none}
#c{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#F2A4B6;text-align:center}
#c .logo{width:640px;height:348px;background:#F2A4B6}
#c .l{font-family:'Damion',cursive;font-size:84px;line-height:1.05;color:#F4EEE4;margin-top:30px}
#c .u{font-size:26px;letter-spacing:.34em;text-transform:uppercase;margin-top:34px}
"""
open('card.html','w').write(page(css,'<div id="c"><div class="logo"></div><div class="l">on the plate,<br>on the table.</div><div class="u">perset.shop</div></div>','',W=1080,H=1920,bgc='#500C02',fibers=True))
