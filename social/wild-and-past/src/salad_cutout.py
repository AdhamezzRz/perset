"""Real Pretty Past salad plate from the product photo (lemon in the centre).

1. Flatten the plate ellipse (found with GrabCut) to a circle.
2. Paint out the lemon: fit a smooth quadratic to the clean yellow and fill the centre disc.
3. Relight the lemon's shadow on the white ring from the clean side of the same radius.
usage: python salad_cutout.py photo.png out_dir
"""
import sys, numpy as np, cv2
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
im = np.array(Image.open(src).convert('RGB')).astype(np.float32)

# 1. ellipse -> circle (values from plate_tool.detect on the product photo)
(cx, cy), (a, b), ang = (576.4, 437.7), (800, 828), 84.0
D = 860; r = D / 2
t = np.deg2rad(ang); R = np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])
M = R @ np.diag([a / 2 / r, b / 2 / r]) @ R.T
A = np.hstack([M, (np.array([cx, cy]) - M @ np.array([r, r]))[:, None]]).astype(np.float32)
im = cv2.warpAffine(im, A, (D, D), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP)
H, W = im.shape[:2]
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)

# 2. find the yellow disc edge (blue channel jumps at the coral ring) and refill it
c0 = (430, 453); pts = []
for th in np.linspace(0, 2 * np.pi, 240, endpoint=False):
    prof = np.array([im[int(c0[1] + rr * np.sin(th)), int(c0[0] + rr * np.cos(th))] for rr in np.arange(200, 280, 1.0)])
    d = np.diff(prof[:, 2])
    if np.any(d > 6):
        rr = 200 + int(np.argmax(d > 6)); pts.append((c0[0] + rr * np.cos(th), c0[1] + rr * np.sin(th)))
(ex, ey), (ea, eb), eang = cv2.fitEllipse(np.array(pts, np.float32))
disk = np.zeros((H, W), np.uint8); cv2.ellipse(disk, ((ex, ey), (ea - 5, eb - 5), eang), 1, -1); disk = disk.astype(bool)
lemon = np.zeros((H, W), np.uint8); cv2.ellipse(lemon, ((462, 425), (320, 350), -28), 1, -1); lemon = lemon.astype(bool)
Rc, Gc, Bc = im[..., 0], im[..., 1], im[..., 2]
clean = disk & ~lemon & (Rc > 214) & (Bc < 70) & (Gc > 145)
def basis(x, y): return np.stack([np.ones_like(x), x / W, y / H, (x / W) ** 2, (y / H) ** 2, x * y / (W * H)], 1)
fill = np.zeros_like(im); F = basis(xx.ravel(), yy.ravel())
for c in range(3):
    co, *_ = np.linalg.lstsq(basis(xx[clean], yy[clean]), im[..., c][clean], rcond=None)
    fill[..., c] = (F @ co).reshape(H, W)
s = (im - cv2.GaussianBlur(im, (0, 0), 1.5))[clean].std(0)
fill += np.random.default_rng(1).normal(0, 1, (H, W, 1)).astype(np.float32) * s
m = cv2.GaussianBlur(disk.astype(np.float32), (0, 0), 1.2)[..., None]
im = im * (1 - m) + fill * m

# 3. relight the lower-left sector of the white ring to the per-radius level of the clean side
cx2, cy2 = ex, ey
rad = np.hypot(xx - cx2, yy - cy2); th = np.arctan2(yy - cy2, xx - cx2)
L = 0.299 * im[..., 0] + 0.587 * im[..., 1] + 0.114 * im[..., 2]; Lb = cv2.GaussianBlur(L, (0, 0), 9)
ref = np.zeros_like(L)
for rr in range(236, 341):
    ring = np.abs(rad - rr) < 0.5; up = ring & (th < 0.6) & (th > -2.2)
    if up.sum() > 10: ref[ring] = np.median(Lb[up])
gain = np.ones_like(L); sel = (rad > 236) & (rad < 340) & (th > 1.2) & (th < 3.1)
gain[sel] = np.clip(ref / np.maximum(Lb, 1), 1.0, 1.45)[sel]
gain = cv2.GaussianBlur(gain, (0, 0), 4)
w = np.clip((rad - 236) / 6, 0, 1) * np.clip((340 - rad) / 6, 0, 1)
im = np.clip(im * (1 + (gain - 1) * w)[..., None], 0, 255).astype(np.uint8)

alpha = np.zeros((H, W), np.uint8); cv2.circle(alpha, (W // 2, H // 2), W // 2 - 2, 255, -1, cv2.LINE_AA)
Image.fromarray(np.dstack([im, alpha])).save(f'{out}/salad_cut.png')
