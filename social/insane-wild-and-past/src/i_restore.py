import json
import vtool
from vtool import *
vtool.W,vtool.H=1080,1920
sx,sy=1080/1520,1920/2688
def sc(e): return ((e[0][0]*sx,e[0][1]*sy),(e[1][0]*(sx+sy)/2,e[1][1]*(sx+sy)/2),e[2])
E_=json.load(open('../ins/ell.json'))
for name in ['cat','auction']:
    key=np.array(Image.open(f'kf/kf_{name}.jpg').convert('RGB'))
    P=Plate(key,sc(E_[name]),thr=28)
    w=vtool.writer(f'vid/k_{name}_x.mp4',24)
    for fr in vtool.frames(f'vid/k_{name}.mp4'): w.stdin.write(P.apply(fr).tobytes())
    w.stdin.close(); w.wait(); print('ok',name)
