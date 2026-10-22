"""Replace a generated plate with the real plate photo (exact pixels), matched to the scene.

detect(img, box) -> ellipse ((cx,cy),(MA,ma),angle) via GrabCut inside an approximate box.
paste(img, ell, cutout, ...) -> new image with the real cutout warped onto the ellipse,
    lit by the generated plate's low-frequency shading and graded to the scene.
"""
import numpy as np, cv2
from PIL import Image
from scipy import ndimage

SCR = '/tmp/claude-0/-home-user-perset/9ff3c93e-59bb-5efc-8bbb-67d4644489c6/scratchpad'
CUT = {'wild': SCR + '/pack/assets/wild_hi.png', 'past': SCR + '/cutouts/past_dinner.png',
       'wild_bowl': SCR + '/cutouts/wild_soup.png', 'past_bowl': SCR + '/cutouts/past_soup.png', 'salad': SCR + '/salad/salad_cut.png'}


def load(p):
    return np.array(Image.open(p).convert('RGB'))


def cutout(name):
    im = np.array(Image.open(CUT[name]).convert('RGBA')).astype(np.float32)
    a = im[..., 3]
    ys, xs = np.where(a > 128)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    return im[y0:y1, x0:x1]


def detect(img, box, iters=6):
    """box = (x0,y0,x1,y1) loosely around the plate."""
    mask = np.zeros(img.shape[:2], np.uint8)
    x0, y0, x1, y1 = box
    rect = (x0, y0, x1 - x0, y1 - y0)
    bg = np.zeros((1, 65), np.float64); fg = np.zeros((1, 65), np.float64)
    # work at reduced scale for speed
    s = 0.5
    sm = cv2.resize(img, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
    m = np.zeros(sm.shape[:2], np.uint8)
    r = tuple(int(v * s) for v in rect)
    cv2.grabCut(cv2.cvtColor(sm, cv2.COLOR_RGB2BGR), m, r, bg, fg, iters, cv2.GC_INIT_WITH_RECT)
    fgm = ((m == 1) | (m == 3)).astype(np.uint8)
    fgm = ndimage.binary_opening(fgm, iterations=2)
    fgm = ndimage.binary_fill_holes(fgm).astype(np.uint8)
    lab, n = ndimage.label(fgm)
    if n == 0:
        raise RuntimeError('nothing found')
    sizes = ndimage.sum(fgm, lab, range(1, n + 1))
    big = (lab == (np.argmax(sizes) + 1)).astype(np.uint8)
    cs, _ = cv2.findContours(big, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c = max(cs, key=cv2.contourArea)
    hull = cv2.convexHull(c)
    (cx, cy), (MA, ma), ang = cv2.fitEllipse(hull)
    return ((cx / s, cy / s), (MA / s, ma / s), ang)


def ellipse_mask(shape, ell, grow=0):
    (cx, cy), (MA, ma), ang = ell
    m = np.zeros(shape[:2], np.uint8)
    cv2.ellipse(m, ((cx, cy), (MA + 2 * grow, ma + 2 * grow), ang), 255, -1, cv2.LINE_AA)
    return m.astype(np.float32) / 255


def warp_cutout(cut, ell, shape, rot=0.0, scale=1.0):
    """Affine-map the circular cutout onto the ellipse. rot = in-plane design rotation (deg)."""
    (cx, cy), (MA, ma), ang = ell
    h, w = cut.shape[:2]
    # cutout centre/radius
    c0 = np.array([w / 2, h / 2]); r0 = w / 2
    # compose: rotate design by rot, scale to (MA/2, ma/2) along ellipse axes rotated by ang
    th = np.deg2rad(rot); a = np.deg2rad(ang)
    R1 = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    S = np.diag([MA / 2 / r0 * scale, ma / 2 / r0 * scale])
    Ra = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
    # fitEllipse width axis is along angle 'ang'; but we want the design upright for near-circular
    # plates seen at an angle (major axis horizontal). Use Ra @ S @ Ra^-1 so content is not rotated.
    M = Ra @ S @ Ra.T @ R1
    t = np.array([cx, cy]) - M @ c0
    A = np.hstack([M, t[:, None]]).astype(np.float32)
    out = cv2.warpAffine(cut, A, (shape[1], shape[0]), flags=cv2.INTER_LANCZOS4,
                         borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    return out


def lum(x):
    return 0.299 * x[..., 0] + 0.587 * x[..., 1] + 0.114 * x[..., 2]


def paste(img, ell, name, rot=0.0, scale=1.0, shade_sigma=0.05, shade_pow=0.9,
          grade=0.6, grain=True, feather=1.2, keep=None, extra_shade=None):
    """keep: optional float mask (H,W) of pixels to keep from the generated image (occluders)."""
    img = img.astype(np.float32)
    cut = cutout(name)
    wc = warp_cutout(cut, ell, img.shape, rot, scale)
    rgb, a = wc[..., :3], wc[..., 3] / 255
    a = cv2.GaussianBlur(a, (0, 0), feather)
    inside = a > 0.5
    R = (ell[1][0] + ell[1][1]) / 4
    sig = max(2, shade_sigma * R)
    # shading: ratio of low-passed luminance (generated / real)
    lg = cv2.GaussianBlur(lum(img) * a, (0, 0), sig) / (cv2.GaussianBlur(a, (0, 0), sig) + 1e-4)
    lr = cv2.GaussianBlur(lum(rgb) * a, (0, 0), sig) / (cv2.GaussianBlur(a, (0, 0), sig) + 1e-4)
    ratio = np.clip(lg / (lr + 1e-3), 0.25, 1.6)
    ratio = ratio / np.median(ratio[inside])  # global exposure handled by grade
    ratio = ratio ** shade_pow
    if extra_shade is not None:
        ratio = ratio * extra_shade
    out = rgb * ratio[..., None]
    # colour grade toward the generated plate statistics (Reinhard, partial)
    for ch in range(3):
        g = img[..., ch][inside]; r = out[..., ch][inside]
        mg, sg = g.mean(), g.std() + 1e-3; mr, sr = r.mean(), r.std() + 1e-3
        k = (sg / sr) ** 0.5
        adj = (out[..., ch] - mr) * k + mg
        out[..., ch] = out[..., ch] * (1 - grade) + adj * grade
    if grain:
        hp = img - cv2.GaussianBlur(img, (0, 0), 1.5)
        n = hp[inside].std()
        rng = np.random.default_rng(3)
        g = rng.normal(0, n * 0.8, img.shape[:2]).astype(np.float32)
        g = cv2.GaussianBlur(g, (0, 0), 0.6)
        out = out + g[..., None]
    if keep is not None:
        a = a * (1 - keep)
    res = img * (1 - a[..., None]) + out * a[..., None]
    return np.clip(res, 0, 255).astype(np.uint8)


def show_ellipse(img, ell, path, scale=0.35):
    v = img.copy()
    cv2.ellipse(v, (tuple(map(float, ell[0])), tuple(map(float, ell[1])), float(ell[2])), (0, 255, 255), 6)
    v = cv2.resize(v, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    Image.fromarray(v).save(path, quality=85)
