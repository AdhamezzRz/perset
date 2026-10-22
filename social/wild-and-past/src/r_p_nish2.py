from reel import *
still('ex/g20_nish_salad.png','seg/ns1.mp4',3.0,1.0,1.12,(0.5,0.45),(0.5,0.42))
still('ex/g20_nish_salad.png','seg/ns2.mp4',2.2,2.3,2.5,(0.70,0.318),(0.70,0.322))
clip('vid/k5_nish_salad.mp4','seg/ns3.mp4')
clip('vid/k6_tuesday_x.mp4','seg/ns4.mp4')
d='cap_nish'
c1=caption('c1',chip('every egyptian home has a nish.',250),d)
c2=caption('c2',chip('the good plates live here.',250),d)
c2b=caption('c2b',chip('look. don\'t touch. guests only.',360,dark=True,size=40),d)
c3=caption('c3',chip('this is your sign. open it.',250),d)
c4=caption('c4',chip('Pretty Past was made for a tuesday.',250),d)
c5=caption('c5','<div class="scr" style="top:1560px;font-size:110px">#FreeThePlates</div>',d)
segs=['seg/ns1.mp4','seg/ns2.mp4','seg/ns3.mp4','seg/ns4.mp4','seg/end_past_salad.mp4']
compose([os.path.abspath(s) for s in segs],[(c1,0.2,3.0),(c2,3.0,5.2),(c2b,3.9,5.2),(c3,5.35,10.2),(c4,10.35,15.25),(c5,12.6,15.25)],os.path.abspath('reels/past-reel-1-el-nish.mp4'))
