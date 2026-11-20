"""Reel assembly helpers: segments from clips/stills, caption PNGs, timeline compose."""
import os, subprocess, json, numpy as np, cv2
from PIL import Image
from wc import page, img, LOGO, SCR, WP

FF = open(SCR + '/ffpath').read().strip()
W, H, FPS = 1080, 1920, 30
NODE = f"NODE_PATH=$(npm root -g) node"


def run(cmd):
    subprocess.run(cmd, shell=True, check=True)


def enc(path):
    return subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                             '-c:v', 'libx264', '-crf', '15', '-preset', 'medium', '-pix_fmt', 'yuv420p', path], stdin=subprocess.PIPE)


def ease(t):
    return t * t * (3 - 2 * t)


def still(src, out, dur, z0=1.0, z1=1.08, c0=(0.5, 0.5), c1=(0.5, 0.5), fn=None, cover=True):
    """Ken Burns on a still. z = zoom relative to cover-fit; c = focus centre (0..1)."""
    im = np.array(Image.open(src).convert('RGB')).astype(np.float32) if isinstance(src, str) else src.astype(np.float32)
    ih, iw = im.shape[:2]
    base = max(W / iw, H / ih) if cover else min(W / iw, H / ih)
    n = int(round(dur * FPS)); p = enc(out)
    for i in range(n):
        t = ease(i / max(1, n - 1))
        z = base * (z0 + (z1 - z0) * t)
        cx = (c0[0] + (c1[0] - c0[0]) * t) * iw; cy = (c0[1] + (c1[1] - c0[1]) * t) * ih
        # keep the frame inside the image
        hw, hh = W / 2 / z, H / 2 / z
        cx = min(max(cx, hw), iw - hw); cy = min(max(cy, hh), ih - hh)
        M = np.float32([[z, 0, W / 2 - z * cx], [0, z, H / 2 - z * cy]])
        fr = cv2.warpAffine(im, M, (W, H), flags=cv2.INTER_LINEAR if z > 1 else cv2.INTER_AREA, borderMode=cv2.BORDER_REFLECT)
        if fn: fr = fn(fr, i / max(1, n - 1))
        p.stdin.write(np.clip(fr, 0, 255).astype(np.uint8).tobytes())
    p.stdin.close(); p.wait()
    return out


def clip(src, out, ss=0, dur=None, speed=1.0, zoom=1.0, c=(0.5, 0.5), zoom_to=None):
    vf = [f"setpts=PTS/{speed}"]
    vf.append(f"fps={FPS}")
    if zoom != 1.0 or zoom_to:
        z0 = zoom; z1 = zoom_to or zoom
        # animated crop zoom via scale+crop expressions
        vf.append(f"scale={int(W*max(z0,z1))}:{int(H*max(z0,z1))}")
        zx = max(z0, z1)
        if z0 == z1:
            vf.append(f"crop={W}:{H}:{int((W*zx-W)*c[0])}:{int((H*zx-H)*c[1])}")
    vf.append(f"scale={W}:{H}")
    d = f"-t {dur}" if dur else ""
    run(f'{FF} -v error -y -ss {ss} -i "{src}" {d} -vf "{",".join(vf)}" -an -c:v libx264 -crf 15 -preset medium -pix_fmt yuv420p "{out}"')
    return out


def cap_css():
    return """
html,body{background:transparent}.bg,.fibers,.vig,.grain{display:none}
.chip{position:absolute;left:50%;transform:translateX(-50%);background:#FBF8F2;color:#1E1410;font-family:'Jost';font-weight:500;
 font-size:46px;line-height:1.18;padding:14px 30px 18px;border-radius:16px;text-align:center;white-space:nowrap;box-shadow:0 6px 18px rgba(0,0,0,.18)}
.chip.dark{background:#500C02;color:#F7EEDC}
.scr{position:absolute;left:0;right:0;text-align:center;font-family:'Damion',cursive;color:#FBF3E6;text-shadow:0 3px 16px rgba(30,10,0,.55),0 0 2px rgba(30,10,0,.4);line-height:1}
.lbl{position:absolute;font-family:'Caveat',cursive;color:#FBF3E6;font-size:58px;text-shadow:0 2px 12px rgba(20,8,0,.7)}
.sm{position:absolute;left:0;right:0;text-align:center;font-family:'Jost';font-weight:500;letter-spacing:.3em;text-transform:uppercase;font-size:22px;color:#FBF3E6;text-shadow:0 2px 10px rgba(20,8,0,.7)}
"""


def caption(name, html, outdir):
    """Render a transparent 1080x1920 caption PNG from body HTML."""
    os.makedirs(outdir, exist_ok=True)
    f = f'{outdir}/{name}.html'
    open(f, 'w').write(page(cap_css(), html, '', W=W, H=H, bgc='transparent', fibers=False))
    run(f'cd "{outdir}" && {NODE} {WP}/out/shootT1.js {W} {H} {name}.html')
    return f'{outdir}/{name}.png'


def chip(text, y, dark=False, size=46):
    return f'<div class="chip{" dark" if dark else ""}" style="top:{y}px;font-size:{size}px">{text}</div>'


def compose(segs, caps, out, xf=None, grain=6, music=None):
    """segs: list of mp4 paths (hard cuts, or xfade list of durations); caps: [(png,t0,t1)]."""
    lst = out + '.txt'
    open(lst, 'w').write(''.join(f"file '{s}'\n" for s in segs))
    tmp = out.replace('.mp4', '_cat.mp4')
    run(f'{FF} -v error -y -f concat -safe 0 -i "{lst}" -c copy "{tmp}"')
    ins = ''.join(f' -loop 1 -t {t1+0.5} -i "{p}"' for p, t0, t1 in caps)
    fc = []
    last = '[0:v]'
    for k, (p, t0, t1) in enumerate(caps):
        fd = 0.22
        fc.append(f'[{k+1}:v]format=rgba,fade=t=in:st={t0}:d={fd}:alpha=1,fade=t=out:st={t1-fd}:d={fd}:alpha=1[c{k}]')
        fc.append(f'{last}[c{k}]overlay=0:0:enable=\'between(t,{t0},{t1})\'[v{k}]')
        last = f'[v{k}]'
    fc.append(f'{last}noise=alls={grain}:allf=t,format=yuv420p[vo]')
    run(f'{FF} -v error -y -i "{tmp}"{ins} -filter_complex "{";".join(fc)}" -map "[vo]" -r {FPS} -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -movflags +faststart "{out}"')
    os.remove(tmp)
    return out


def dur(path):
    o = subprocess.run([FF, '-i', path], capture_output=True, text=True).stderr
    import re
    m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', o)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
