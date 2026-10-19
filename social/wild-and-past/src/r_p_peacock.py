from reel import *
clip('vid/k3_peacock_x.mp4','seg/pk1.mp4',speed=0.85)
still('ex/g15_peacock.png','seg/pk2.mp4',2.8,1.9,1.45,(0.20,0.36),(0.48,0.70))
d='cap_pk'
c1=caption('c1',chip('he saw the plate.',250),d)
c2=caption('c2',chip('he has… questions.',250),d)
c3=caption('c3',chip('identity crisis.',250),d)
c4=caption('c4',chip('relax. you\'re still the original.',250),d)
c5=caption('c5','<div class="scr" style="top:1560px;font-size:92px">he only comes in one.<br><span style="font-size:70px">the plate comes in six.</span></div>',d)
segs=['seg/pk1.mp4','seg/pk2.mp4','seg/end_past.mp4']
compose([os.path.abspath(s) for s in segs],[(c1,0.2,2.0),(c2,2.0,3.9),(c3,3.9,5.9),(c4,6.0,8.7),(c5,6.6,8.7)],os.path.abspath('reels/past-reel-3-peacock-has-notes.mp4'))
