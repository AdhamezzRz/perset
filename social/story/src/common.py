import base64
def b64(p): return base64.b64encode(open(p,'rb').read()).decode()
LOGO=b64('../../../assets/perset-logo-mask.png')
FONTS=open('fonts_embedded.css').read()
JS_HELP="""
const clamp=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
const ease={out:t=>1-Math.pow(1-t,3),io:t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2,back:t=>{const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(t-1,3)+c1*Math.pow(t-1,2)}};
const seg=(t,a,d)=>clamp((t-a)/d);
"""
BASE_CSS="""
:root{--linen:#F4EEE4;--ox:#500C02;--blush:#F2A4B6;--paper:#FBF8F2;--ink:#2A1A16}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;overflow:hidden}
body{font-family:'Jost',sans-serif;position:relative}
.script{font-family:'Damion',cursive;font-weight:400}
.eyebrow{font-weight:400;letter-spacing:.34em;text-transform:uppercase}
.logo{-webkit-mask:url(data:image/png;base64,%s) center/contain no-repeat;mask:url(data:image/png;base64,%s) center/contain no-repeat}
.grain{position:absolute;inset:0;pointer-events:none;opacity:.08;mix-blend-mode:multiply;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='100%%' height='100%%' filter='url(%%23n)'/></svg>")}
.ticket{position:absolute;left:0;right:0;height:30px;background:var(--blush)}
.ticket.top{top:0;-webkit-mask:radial-gradient(circle at 50%% 100%%, transparent 12px, #000 13px) 0 0/48px 100%% repeat-x;mask:radial-gradient(circle at 50%% 100%%, transparent 12px, #000 13px) 0 0/48px 100%% repeat-x}
.ticket.bot{bottom:0;-webkit-mask:radial-gradient(circle at 50%% 0, transparent 12px, #000 13px) 0 0/48px 100%% repeat-x;mask:radial-gradient(circle at 50%% 0, transparent 12px, #000 13px) 0 0/48px 100%% repeat-x}
""" % (LOGO, LOGO)
def page(css, body, js, bg='transparent'):
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{FONTS}\n{BASE_CSS}\nhtml,body{{background:{bg}}}\n{css}</style></head><body>{body}<script>{JS_HELP}\n{js}</script></body></html>"
