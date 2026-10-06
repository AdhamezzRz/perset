import base64, random, math, os
HERE=os.path.dirname(os.path.abspath(__file__))
SCR=os.path.dirname(HERE)
def b64(p): return base64.b64encode(open(p,'rb').read()).decode()
def img(p, mime=None):
    m = mime or ('image/png' if p.endswith('.png') else 'image/jpeg')
    return f"data:{m};base64,{b64(p)}"
LOGO=b64(SCR+'/src/perset-logo-mask.png')
FONTS=open(SCR+'/fonts/fonts_embedded.css').read()
JS_HELP="""
const clamp=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
const ease={out:t=>1-Math.pow(1-t,3),io:t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2,back:t=>{const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(t-1,3)+c1*Math.pow(t-1,2)},bounce:t=>{const n=7.5625,d=2.75;if(t<1/d)return n*t*t;if(t<2/d)return n*(t-=1.5/d)*t+.75;if(t<2.5/d)return n*(t-=2.25/d)*t+.9375;return n*(t-=2.625/d)*t+.984375}};
const seg=(t,a,d)=>clamp((t-a)/d);
"""
def jag(w,h,seed=1,amp=5,step=20,edges='trbl'):
    """CSS polygon() with a hand-torn edge on the chosen sides (t,r,b,l)."""
    r=random.Random(seed); pts=[]
    def j(): return r.uniform(0,amp)
    # top edge left->right
    n=max(2,int(w/step))
    for i in range(n+1):
        x=min(w,i*w/n); pts.append((x, j() if 't' in edges else 0))
    n=max(2,int(h/step))
    for i in range(1,n+1):
        y=min(h,i*h/n); pts.append((w-(j() if 'r' in edges else 0), y))
    n=max(2,int(w/step))
    for i in range(1,n+1):
        x=max(0,w-i*w/n); pts.append((x, h-(j() if 'b' in edges else 0)))
    n=max(2,int(h/step))
    for i in range(1,n):
        y=max(0,h-i*h/n); pts.append((j() if 'l' in edges else 0, y))
    return 'polygon('+','.join(f'{x:.1f}px {y:.1f}px' for x,y in pts)+')'
def loop_path(cx,cy,rx,ry,seed=1,turns=1.14):
    """Hand-drawn pencil circle with overshoot and wobble (SVG path d)."""
    r=random.Random(seed); pts=[]; N=60
    a0=r.uniform(-.6,.2)
    for i in range(N+1):
        t=i/N; a=a0+t*turns*2*math.pi
        w=1+0.05*math.sin(a*3+seed)+r.uniform(-.012,.012)
        drift=1+0.10*(t-0.5)  # spiral drift so the ends miss each other
        pts.append((cx+rx*w*drift*math.cos(a), cy+ry*w*drift*math.sin(a)))
    return 'M'+' L'.join(f'{x:.1f} {y:.1f}' for x,y in pts)
def squiggle(x1,y1,x2,y2,seed=1,bow=40):
    r=random.Random(seed); mx,my=(x1+x2)/2,(y1+y2)/2
    nx,ny=-(y2-y1),(x2-x1); L=math.hypot(nx,ny) or 1; nx/=L; ny/=L
    cx,cy=mx+nx*bow+r.uniform(-8,8),my+ny*bow+r.uniform(-8,8)
    return f'M{x1:.1f} {y1:.1f} Q{cx:.1f} {cy:.1f} {x2:.1f} {y2:.1f}'
def arrowhead(x2,y2,x1,y1,size=22,seed=1):
    ang=math.atan2(y2-y1,x2-x1); r=random.Random(seed)
    a1=ang+math.radians(150+r.uniform(-8,8)); a2=ang-math.radians(150+r.uniform(-8,8))
    return f'M{x2+size*math.cos(a1):.1f} {y2+size*math.sin(a1):.1f} L{x2:.1f} {y2:.1f} L{x2+size*math.cos(a2):.1f} {y2+size*math.sin(a2):.1f}'
BASE_CSS="""
:root{--linen:#F2EBDD;--linen-d:#E9DECB;--ox:#500C02;--blush:#F2A4B6;--paper:#FBF8F2;--ink:#2A1A16;--kraft:#D8BF99}
*{box-sizing:border-box;margin:0;padding:0}
html,body{overflow:hidden}
body{font-family:'Jost',sans-serif;position:relative;color:var(--ink)}
.script{font-family:'Damion',cursive;font-weight:400}
.serif{font-family:'Fraunces',serif;font-variation-settings:'SOFT' 50,'opsz' 144}
.eyebrow{font-weight:400;letter-spacing:.3em;text-transform:uppercase}
.logo{-webkit-mask:url(data:image/png;base64,@@LOGO@@) center/contain no-repeat;mask:url(data:image/png;base64,@@LOGO@@) center/contain no-repeat}
.bg{position:absolute;inset:0;background:
   radial-gradient(ellipse at 30% 20%,rgba(255,255,255,.35),rgba(255,255,255,0) 55%),
   var(--bgc,#F2EBDD)}
.fibers{position:absolute;inset:0;pointer-events:none;opacity:.5;mix-blend-mode:multiply;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='600' height='600'><filter id='f'><feTurbulence type='fractalNoise' baseFrequency='0.035 0.9' numOctaves='4' seed='4'/><feColorMatrix values='0 0 0 0 .55  0 0 0 0 .45  0 0 0 0 .32  0 0 0 .55 0'/></filter><rect width='100%' height='100%' filter='url(%23f)'/></svg>")}
.grain{position:absolute;inset:0;pointer-events:none;opacity:.10;mix-blend-mode:multiply;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")}
.vig{position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse at 50% 50%,rgba(0,0,0,0) 60%,rgba(60,30,10,.16) 100%)}
.sh{filter:drop-shadow(0 14px 18px rgba(60,35,20,.30)) drop-shadow(0 2px 3px rgba(60,35,20,.35))}
.sh-s{filter:drop-shadow(0 6px 8px rgba(60,35,20,.28)) drop-shadow(0 1px 2px rgba(60,35,20,.35))}
.tape{position:absolute;height:46px;background:rgba(242,164,182,.80);clip-path:polygon(0 0,100% 0,98% 20%,100% 42%,97% 62%,100% 82%,98% 100%,0 100%,2% 80%,0 60%,3% 40%,0 20%);mix-blend-mode:multiply}
.tape.k{background:rgba(214,190,150,.85)}
.abs{position:absolute}
svg.hand path{fill:none;stroke:var(--ox);stroke-width:4;stroke-linecap:round;stroke-linejoin:round}
""".replace("@@LOGO@@", LOGO)
def page(css, body, js='', W=1080, H=1350, bgc='#F2EBDD', fibers=True):
    fib='<div class="fibers"></div>' if fibers else ''
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{FONTS}\n{BASE_CSS}\n"
            f"html,body{{width:{W}px;height:{H}px}}\n:root{{--bgc:{bgc}}}\n{css}</style></head><body>"
            f"<div class='bg'></div>{fib}{body}<div class='vig'></div><div class='grain'></div>"
            f"<script>{JS_HELP}\n{js}</script></body></html>")
