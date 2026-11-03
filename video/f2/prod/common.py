"""Shared constants and helpers for the F2 production. The spec is f2/DESIGN_BIBLE.md; section numbers
in comments refer to it. Every image value here is float32 sRGB in 0..1 unless a name says `lin`."""
import json
import os

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))          # .../video
LIB = os.path.join(ROOT, 'assets', 'lib')
BUILD = os.path.join(ROOT, 'build', 'f2')
CACHE = os.path.join(BUILD, 'cache')

W, H, FPS = 1080, 1920, 30
NFRAMES = 1772                                          # 59.067 s


def hexrgb(h):
    h = h.lstrip('#')
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32) / 255.0


# §5.1 colour tokens
INK = hexrgb('#0B0A09')
BONE = hexrgb('#ECE6DA')
BONE7 = hexrgb('#BDB5A7')
BONE5 = hexrgb('#8E877B')
SIGNAL = hexrgb('#7A5CFF')
BRAND = hexrgb('#5B2EFF')
PAPER = hexrgb('#F2EEE7')
INKP = hexrgb('#15121B')
GLINT = hexrgb('#F4EEDC')
HAL_TINT = np.array([1.00, 0.42, 0.22], np.float32)
LUMA = np.array([0.2126, 0.7152, 0.0722], np.float32)


# ---------------------------------------------------------------- easing (§6.1)
class Bezier:
    """CSS cubic-bezier(x1, y1, x2, y2): returns y for progress x in 0..1."""

    def __init__(self, x1, y1, x2, y2):
        self.c = (x1, y1, x2, y2)

    @staticmethod
    def _b(t, a, b):
        return 3 * a * (1 - t) ** 2 * t + 3 * b * (1 - t) * t ** 2 + t ** 3

    def __call__(self, x):
        x1, y1, x2, y2 = self.c
        x = min(1.0, max(0.0, float(x)))
        if x in (0.0, 1.0):
            return x
        lo, hi, t = 0.0, 1.0, x
        for _ in range(60):                             # bisection: robust for every curve we use
            v = self._b(t, x1, x2)
            if abs(v - x) < 1e-9:
                break
            if v < x:
                lo = t
            else:
                hi = t
            t = (lo + hi) / 2
        return self._b(t, y1, y2)


EASE = {k: Bezier(*v) for k, v in dict(
    FADE=(.33, 0, .2, 1), SETTLE=(.16, 1, .3, 1), LEAVE=(.7, 0, .84, 0), ROLL=(.2, 0, 0, 1),
    DEVELOP=(.22, .61, .36, 1), FOCUS=(.33, 0, .15, 1), GLINT=(.2, .6, .3, 1), SNAP=(.7, 0, .2, 1),
    HOP=(.5, 0, .2, 1), ACCEL=(.5, 0, 1, 1), RISE=(.25, .1, .25, 1), TRAVEL=(.65, 0, .35, 1),
    DRAW=(.45, 0, .2, 1), REVEAL=(.83, 0, .17, 1), DIVE=(.6, 0, .1, 1), LAMP=(.4, 0, .2, 1),
    SETTLEL=(.22, 1, .36, 1), RAKE=(.45, 0, .55, 1)).items()}
EASE['LINEAR'] = lambda x: min(1.0, max(0.0, float(x)))


def span(t, a, b):
    """Linear progress of time t (frames, may be fractional) through the move a -> b."""
    if b <= a:
        return 1.0 if t >= b else 0.0
    return min(1.0, max(0.0, (t - a) / (b - a)))


def ease(name, t, a, b):
    return EASE[name](span(t, a, b))


def lerp(a, b, u):
    return a + (b - a) * u


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3 - 2 * t)


# ---------------------------------------------------------------- colour
def to_lin(x):
    x = np.asarray(x, np.float32)
    return np.where(x <= 0.04045, x / 12.92, ((np.maximum(x, 0) + 0.055) / 1.055) ** 2.4).astype(np.float32)


def to_srgb(x):
    x = np.maximum(np.asarray(x, np.float32), 0)
    return np.where(x <= 0.0031308, x * 12.92, 1.055 * x ** (1 / 2.4) - 0.055).astype(np.float32)


INK_LIN = to_lin(INK)
PAPER_LIN = to_lin(PAPER)


def luma(rgb):
    return rgb @ LUMA


def curve(x, lift, gain, gamma=1.06, sh=0.82):
    """§7.1 print curve with the soft shoulder above 0.82."""
    y = lift + (gain - lift) * np.clip(x, 0, 1) ** gamma
    k = 1 - np.exp(-1.4)
    s = sh + (1 - np.exp(-(y - sh) / (1 - sh) * 1.4)) * (gain - sh) / k
    return np.where(y > sh, s, y).astype(np.float32)


_SHADOW = np.array([1.04, 1.00, 0.94], np.float32)
_HIGH = np.array([1.02, 1.00, 0.95], np.float32)


def cgrade(rgb, sat):
    """§7.1 colour 'warm print' grade. Blacks land exactly on INK (the bible's 'lifted to exactly ink')."""
    rgb = np.clip(rgb.astype(np.float32), 0, 1)
    L = luma(rgb)[..., None]
    rgb = np.clip(L + (rgb - L) * sat, 0, 1)
    y = curve(rgb, lift=0.043, gain=0.94)
    w = np.clip(1 - 2 * luma(y), 0, 1)[..., None]
    y = y * (w * _SHADOW + (1 - w) * _HIGH)
    black = curve(np.zeros(3, np.float32), 0.043, 0.94) * _SHADOW      # what pure black became
    s = np.clip(luma(y) / 0.5, 0, 1)[..., None]
    y = y + (INK - black) * (1 - s)
    return np.clip(y, 0, 1).astype(np.float32)


RAMP = np.array([INK, hexrgb('#8C857A'), hexrgb('#EDE6D6')], np.float32)


def mono(v):
    """§7.1 B/W 'selenium print': curve then 3-stop ramp (stop 0 = ink)."""
    g = curve(np.asarray(v, np.float32), lift=0.0, gain=1.0)
    g = np.clip(g, 0, 1)[..., None]
    lo = RAMP[0] + (RAMP[1] - RAMP[0]) * (g / 0.5)
    hi = RAMP[1] + (RAMP[2] - RAMP[1]) * ((g - 0.5) / 0.5)
    return np.where(g < 0.5, lo, hi).astype(np.float32)


def halation(rgb, thr, sigma, strength):
    """§7.1 halation glow layer (additive), sigma in the pixels of `rgb`."""
    L = luma(rgb)
    m = np.clip((L - thr) / (1 - thr), 0, 1).astype(np.float32)
    g = cv2.GaussianBlur(m, (0, 0), sigma)
    return (g[..., None] * HAL_TINT * strength).astype(np.float32)


# ---------------------------------------------------------------- resampling
def unsharp(img, scale):
    """§7.1: upscales > x1.05 get unsharp mask radius 0.8*scale px, 45 %, threshold 2."""
    if scale <= 1.05:
        return img
    b = cv2.GaussianBlur(img, (0, 0), 0.8 * scale)
    d = img - b
    return (img + 0.45 * d * (np.abs(d) > 2 / 255.0)).astype(np.float32)


def warp(src, s, ox, oy, box, sharpen=True):
    """Draw `src` scaled by s with its top-left at screen (ox, oy), sampled for the integer screen box
    (x0, y0, x1, y1). Returns (pixels, coverage) for that box. Downscales go through an area pre-filter,
    upscales through Lanczos + the §7.1 unsharp mask. Coverage is an anti-aliased edge alpha."""
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    sh, sw = src.shape[:2]
    work, ws = src, s
    if s < 0.95:                                         # area pre-filter to (almost) the final size
        nw, nh = max(1, int(round(sw * s))), max(1, int(round(sh * s)))
        work = cv2.resize(src, (nw, nh), interpolation=cv2.INTER_AREA)
        ws = s * sw / nw                                 # residual scale relative to `work` (about 1)
        ws_y = s * sh / nh
    else:
        ws_y = ws
    M = np.float32([[ws, 0, ox - x0], [0, ws_y, oy - y0]])
    interp = cv2.INTER_LANCZOS4 if s >= 0.95 else cv2.INTER_CUBIC
    out = cv2.warpAffine(work, M, (bw, bh), flags=interp, borderMode=cv2.BORDER_REPLICATE)
    ones = np.ones(work.shape[:2], np.float32)
    cov = cv2.warpAffine(ones, M, (bw, bh), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    if sharpen and s > 1.05:
        out = unsharp(out, s)
    if out.ndim == 3:
        out = np.clip(out, 0, 1.5)
    return out.astype(np.float32), np.clip(cov, 0, 1).astype(np.float32)


def screen_box(s, ox, oy, w, h, pad=2):
    """Integer screen box covering a w x h source drawn at scale s, clipped to the frame."""
    x0 = max(0, int(np.floor(ox)) - pad)
    y0 = max(0, int(np.floor(oy)) - pad)
    x1 = min(W, int(np.ceil(ox + w * s)) + pad)
    y1 = min(H, int(np.ceil(oy + h * s)) + pad)
    return x0, y0, x1, y1


# ---------------------------------------------------------------- io
def load_rgb(name):
    from PIL import Image
    return np.asarray(Image.open(os.path.join(LIB, name)).convert('RGB')).astype(np.float32) / 255.0


def load_gray(name):
    from PIL import Image
    return np.asarray(Image.open(os.path.join(LIB, name)).convert('L')).astype(np.float32) / 255.0


def cache_path(name):
    return os.path.join(CACHE, name)


def save_npy(name, arr):
    os.makedirs(CACHE, exist_ok=True)
    np.save(cache_path(name), arr.astype(np.float32) if arr.dtype != np.float32 else arr)


def load_npy(name):
    return np.load(cache_path(name))


def save_png(path, rgb):
    from PIL import Image
    os.makedirs(os.path.dirname(path), exist_ok=True)
    Image.fromarray((np.clip(rgb, 0, 1) * 255 + 0.5).astype(np.uint8)).save(path)


def coins_table():
    return json.load(open(cache_path('coins.json')))
