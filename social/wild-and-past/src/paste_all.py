import json, sys
from plate_tool import *
E_=json.load(open('ellipses.json'))
cfg={'g01_symtable':'wild','g10_denim':'wild','g11_velvet':'wild','g12_silk':'wild','g13_beach':'wild',
'g15_peacock':'past','g16_omali':'past','g17_album1':'past','g18_album2':'past','g19_album3':'past'}
only=sys.argv[1:]
for k,name in cfg.items():
    if only and k not in only: continue
    im=load(f'gen/{k}.png')
    for e in E_[k]:
        ell=(tuple(e[0]),tuple(e[1]),e[2])
        grade=0.75 if 'album' in k else 0.45
        im=paste(im,ell,name,grade=grade)
    Image.fromarray(im).save(f'ex/{k}.png')
    print('ok',k)
