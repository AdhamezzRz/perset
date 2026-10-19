import json, sys
from plate_tool import *
B={'g01_symtable':[(100,650,1420,1990)],'g10_denim':[(180,370,1580,1760)],'g11_velvet':[(180,370,1580,1760)],
'g12_silk':[(200,430,1520,1780)],'g13_beach':[(250,420,1540,1720)],'g15_peacock':[(220,1520,1400,2390)],
'g16_omali':[(280,0,1250,1100)],'g17_album1':[(0,1280,880,1760),(800,1310,1860,1930)],'g18_album2':[(280,1240,1460,1930)],
'g19_album3':[(320,1140,1870,1930)]}
res={}
for k,bs in B.items():
    im=load(f'gen/{k}.png'); res[k]=[]
    for b in bs:
        e=detect(im,b); res[k].append([list(map(float,e[0])),list(map(float,e[1])),float(e[2])]); print(k,res[k][-1])
    v=im.copy()
    for e in res[k]: cv2.ellipse(v,(tuple(e[0]),tuple(e[1]),e[2]),(0,255,255),6)
    Image.fromarray(cv2.resize(v,None,fx=.2,fy=.2,interpolation=cv2.INTER_AREA)).save(f'chk_{k}.jpg')
json.dump(res,open('ellipses.json','w'),indent=0)
