import sys, os, numpy as np
sys.path.insert(0, '/tmp/claude-0/-home-user-perset/9ff3c93e-59bb-5efc-8bbb-67d4644489c6/scratchpad/pack')
from common import *   # img, page, jag, loop_path, squiggle, arrowhead, BASE_CSS ...
from PIL import Image
from scipy import ndimage
WP = os.path.dirname(os.path.abspath(__file__))
def key(path):
    a=np.asarray(Image.open(path).convert('RGB')).astype(np.float32)
    bg=a[:40,:40].reshape(-1,3).mean(0)
    d=np.linalg.norm(a-bg,axis=2)
    alpha=np.clip((d-60)/(150-60),0,1)
    alpha=ndimage.grey_erosion(alpha,size=(3,3)); alpha=ndimage.gaussian_filter(alpha,0.8)
    interior=alpha>=0.96
    idx=ndimage.distance_transform_edt(~interior,return_distances=False,return_indices=True)
    c=a[idx[0],idx[1]]
    out=Image.fromarray(np.dstack([c,alpha*255]).astype(np.uint8),'RGBA')
    return out.crop(out.getbbox())
def jpg(src, dst, w=None, h=None, box=None, q=92):
    im=Image.open(src).convert('RGB')
    if box: im=im.crop(box)
    if w: im=im.resize((w,h),Image.LANCZOS)
    im.save(dst,quality=q); return dst
def cover_crop(src, dst, W, H, fx=0.5, fy=0.5, q=92):
    im=Image.open(src).convert('RGB'); iw,ih=im.size; s=max(W/iw,H/ih)
    nw,nh=int(round(iw*s)),int(round(ih*s)); im=im.resize((nw,nh),Image.LANCZOS)
    x=int((nw-W)*fx); y=int((nh-H)*fy); im.crop((x,y,x+W,y+H)).save(dst,quality=q); return dst
