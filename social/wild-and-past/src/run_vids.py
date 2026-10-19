import json, sys
from vtool import *
sx,sy=1080/1520,1920/2688
def sc(e): return ((e[0][0]*sx,e[0][1]*sy),(e[1][0]*(sx+sy)/2,e[1][1]*(sx+sy)/2),e[2])
which=sys.argv[1:]
if 'sym' in which:
    key=np.array(Image.open('kf/kf_sym.jpg').convert('RGB'))
    s=json.load(open('sym_ell.json'))['sym_key']; ell=sc(s); axis=ell[0][0]
    for name,side in (('k1_fork','left'),):
        P=Plate(key,ell,thr=30); w=writer(f'vid/{name}_x.mp4')
        for fr in frames(f'vid/{name}.mp4'):
            r,occ=P.apply(fr,return_occ=True)
            m=mirror(r,axis,side); om=mirror2(occ,axis,side)
            w.stdin.write(paste_with(m,P,om).tobytes())
        w.stdin.close(); w.wait(); print('done',name)
if 'peacock' in which:
    key=np.array(Image.open('kf/kf_peacock.jpg').convert('RGB'))
    e=json.load(open('ellipses.json'))['g15_peacock'][0]; ell=sc(e)
    P=Plate(key,ell,thr=30); w=writer('vid/k3_peacock_x.mp4')
    for fr in frames('vid/k3_peacock.mp4'): w.stdin.write(P.apply(fr).tobytes())
    w.stdin.close(); w.wait(); print('done peacock')
if 'nish' in which:
    key=np.array(Image.open('kf/kf_nish.jpg').convert('RGB'))
    Ps=[Plate(key,sc(e),thr=24,pad=30) for e in json.load(open('nish_ell.json'))]
    w=writer('vid/k5_nish_x.mp4')
    for fr in frames('vid/k5_nish.mp4'):
        for P in Ps: fr=P.apply(fr)
        w.stdin.write(fr.tobytes())
    w.stdin.close(); w.wait(); print('done nish')
