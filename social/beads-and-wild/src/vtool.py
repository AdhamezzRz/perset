"""Per-frame exact-plate restoration for Kling clips shot from a locked camera.

The keyframe we sent to Kling already carries the real plate pixels. For every frame we
re-align the keyframe's plate patch to the frame (phase correlation), detect occluders
(hands, glasses, doors) by difference, match exposure, and paste the real plate back
wherever nothing covers it. Optional mirroring builds perfectly symmetrical shots.
"""
import subprocess, numpy as np, cv2
from PIL import Image

FF = open('/tmp/claude-0/-home-user-perset/9ff3c93e-59bb-5efc-8bbb-67d4644489c6/scratchpad/ffpath').read().strip()
W, H = 1080, 1920


def frames(path):
    p = subprocess.Popen([FF, '-v', 'error', '-i', path, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    while True:
        b = p.stdout.read(W * H * 3)
        if len(b) < W * H * 3:
            break
        yield np.frombuffer(b, np.uint8).reshape(H, W, 3)


def writer(path, fps=24):
    return subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(fps), '-i', '-',
                             '-c:v', 'libx264', '-crf', '14', '-preset', 'slow', '-pix_fmt', 'yuv420p', path], stdin=subprocess.PIPE)


def emask(ell, grow=3):
    (cx, cy), (a, b), ang = ell
    m = np.zeros((H, W), np.uint8)
    cv2.ellipse(m, ((float(cx), float(cy)), (float(a + 2 * grow), float(b + 2 * grow)), float(ang)), 255, -1, cv2.LINE_AA)
    return m.astype(np.float32) / 255


def lum(x):
    return 0.299 * x[..., 0] + 0.587 * x[..., 1] + 0.114 * x[..., 2]


class Plate:
    def __init__(self, key, ell, thr=26, pad=40):
        self.key = key.astype(np.float32)
        self.m = emask(ell)
        ys, xs = np.where(self.m > 0)
        self.box = (max(0, xs.min() - pad), max(0, ys.min() - pad), min(W, xs.max() + pad), min(H, ys.max() + pad))
        self.thr = thr
        self.prev = (0.0, 0.0)

    def apply(self, fr, extra_keep=None, return_occ=False):
        x0, y0, x1, y1 = self.box
        f = fr.astype(np.float32)
        kp = self.key[y0:y1, x0:x1]; fp = f[y0:y1, x0:x1]
        win = cv2.createHanningWindow((x1 - x0, y1 - y0), cv2.CV_32F)
        (dx, dy), resp = cv2.phaseCorrelate(lum(kp), lum(fp), win)
        if resp < 0.08 or abs(dx) > 25 or abs(dy) > 25:
            dx, dy = self.prev
        # smooth the shift
        dx = 0.6 * dx + 0.4 * self.prev[0]; dy = 0.6 * dy + 0.4 * self.prev[1]
        self.prev = (dx, dy)
        M = np.float32([[1, 0, dx], [0, 1, dy]])
        ks = cv2.warpAffine(self.key, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        ms = cv2.warpAffine(self.m, M, (W, H), flags=cv2.INTER_LINEAR)
        # exposure match on clean ring
        d = np.abs(cv2.GaussianBlur(lum(f), (0, 0), 2.5) - cv2.GaussianBlur(lum(ks), (0, 0), 2.5))
        occ = (d > self.thr).astype(np.uint8)
        occ = cv2.morphologyEx(occ, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
        occ = cv2.dilate(occ, np.ones((15, 15), np.uint8))
        occ = cv2.morphologyEx(occ, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
        # ignore speckle occlusions that are tiny
        n, lab, st, _ = cv2.connectedComponentsWithStats(occ * (ms > 0.5).astype(np.uint8))
        keep = np.zeros_like(occ)
        for i in range(1, n):
            if st[i, cv2.CC_STAT_AREA] > 900:
                keep[lab == i] = 1
        occf = cv2.GaussianBlur(keep.astype(np.float32), (0, 0), 3)
        if extra_keep is not None:
            occf = np.maximum(occf, extra_keep)
        clean = (ms > 0.9) & (occf < 0.05)
        if clean.sum() > 500:
            g = np.median(f[clean], 0) / np.maximum(np.median(ks[clean], 0), 1)
            g = np.clip(g, 0.85, 1.15)
            ks = ks * g
        a = (ms * (1 - occf))[..., None]
        out = f * (1 - a) + ks * a
        out = np.clip(out, 0, 255).astype(np.uint8)
        return (out, occf) if return_occ else out


def mirror(fr, axis, side='left'):
    """Make the frame symmetric around x=axis using the chosen half."""
    a = int(round(axis))
    out = fr.copy()
    if side == 'left':
        w = min(a, W - a)
        out[:, a:a + w] = fr[:, a - w:a][:, ::-1]
        if a + w < W:
            out[:, a + w:] = out[:, a + w - 1:a + w]
    else:
        w = min(a, W - a)
        out[:, a - w:a] = fr[:, a:a + w][:, ::-1]
        if a - w > 0:
            out[:, :a - w] = out[:, a - w:a - w + 1]
    return out


def paste_with(fr, plate, occf):
    """Paste plate's key patch (using its last shift) with a given occluder mask, no detection."""
    dx, dy = plate.prev
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    ks = cv2.warpAffine(plate.key, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    ms = cv2.warpAffine(plate.m, M, (W, H), flags=cv2.INTER_LINEAR)
    a = (ms * (1 - occf))[..., None]
    return np.clip(fr.astype(np.float32) * (1 - a) + ks * a, 0, 255).astype(np.uint8)


def mirror2(m, axis, side='left'):
    return mirror(m[..., None].repeat(3, 2), axis, side)[..., 0]
