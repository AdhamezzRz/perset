from reel import *
os.makedirs('seg',exist_ok=True); os.makedirs('reels',exist_ok=True)
# s1 balcony, mirrored
b=np.array(Image.open('gen/g02_balcony.png').convert('RGB')); a=b.shape[1]//2
b[:,a:]=b[:,:a][:,::-1][:, :b.shape[1]-a]
still(b,'seg/sym1.mp4',2.6,1.0,1.10,(0.5,0.5),(0.5,0.47))
clip('vid/k1_fork_x.mp4','seg/sym2.mp4',ss=0.8,dur=3.4)
clip('vid/k2_glass_x.mp4','seg/sym3.mp4')
key=np.array(Image.open('kf/kf_sym.jpg').convert('RGB'))
cx,cy=537.2/1080,947.2/1920
def line(fr,t):
    k=min(1,t/0.55); y0=int(1920*0.16); y1=int(y0+(1920*0.84-y0)*k)
    o=fr.copy()
    for y in range(y0,y1,26): cv2.line(o,(540,y),(540,min(y+14,y1)),(251,243,230),4,cv2.LINE_AA)
    return fr*0.25+o*0.75
still(key,'seg/sym4.mp4',2.8,1.12,1.38,(cx,cy),(cx,cy),fn=line)
d='cap_sym'
c1=caption('c1',chip('a perfectly symmetrical lunch',250),d)
c2=caption('c2',chip('two hands. one fork.',250),d)
c3=caption('c3',chip('cheers, in stereo.',250),d)
c4=caption('c4',chip('even the leopards agree.',250),d)
segs=['seg/sym1.mp4','seg/sym2.mp4','seg/sym3.mp4','seg/sym4.mp4','seg/end_wild.mp4']
compose([os.path.abspath(s) for s in segs],[(c1,0.25,2.5),(c2,2.75,5.9),(c3,7.3,10.95),(c4,11.2,13.75)],os.path.abspath('reels/wild-reel-2-symmetrical-lunch.mp4'))
