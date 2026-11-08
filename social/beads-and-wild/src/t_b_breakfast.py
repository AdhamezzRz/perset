import vtool
from vtool import *
vtool.W=vtool.H=1080
key=np.array(Image.open('kf/kf_breakfast.jpg').convert('RGB'))
ell=((540.5,527.8),(686,693),34.6)
P=Plate(key,ell,thr=30)
w=vtool.writer('vid/k_breakfast_x.mp4',24)
for fr in vtool.frames('vid/k_breakfast_1080.mp4'): w.stdin.write(P.apply(fr).tobytes())
w.stdin.close(); w.wait(); print('ok')
