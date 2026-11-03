"""RAKING LIGHT / 侧光 — reference relight model for coins.png (product concept, look-dev).

Reads ONLY video/assets/lib/coins.png. Everything here is the exact math the film shader must reproduce.

Model (per pixel, source photo treated as a shallow relief lit by one light):
  A  = low-pass of the photo (patina / albedo)                    sigma = 5 src px
  h  = G(L, 0.9 px) - G(L, 4.5 px)  (+ coin body dome)            relief, src-px units
  r  = 1 + clamp(cot(el), 0, 9) * k * (-grad(h) . l_xy)            relief contrast grows with cot(elevation)
  base = A + (L - A) * mix(0.35, 1, smoothstep(80deg, 30deg, el))   baked photo shading fades as the light goes frontal
  sh = height-field shadow toward the light (soft)
  out = (base * r * (0.30 + 0.70 sh) * metal * Lcolor + spec) * spot  + cloth
"""
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
from skimage import filters, segmentation
import cv2

LIB = '/home/user/ccvedio/video/assets/lib/'


def smoothstep(a, b, x):
    t = np.clip((np.asarray(x, np.float32) - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def kelvin_rgb(k):
    """Approximate blackbody tint, normalised so max channel = 1 (only 2700..6500 K used)."""
    table = {2700: (1.0, 0.82, 0.63), 3200: (1.0, 0.885, 0.745), 4300: (1.0, 0.94, 0.87),
             5600: (0.93, 0.96, 1.0), 6500: (0.88, 0.93, 1.0)}
    ks = sorted(table)
    k = min(max(k, ks[0]), ks[-1])
    for a, b in zip(ks, ks[1:]):
        if a <= k <= b:
            u = (k - a) / (b - a)
            return np.array([table[a][i] * (1 - u) + table[b][i] * u for i in range(3)], np.float32)
    return np.array(table[ks[-1]], np.float32)


def coin_labels():
    """Watershed segmentation (classic skimage recipe) -> label map, 24 coins."""
    im = np.asarray(Image.open(LIB + 'coins.png')).astype(np.float32) / 255
    elev = filters.sobel(im)
    markers = np.zeros(im.shape, int)
    markers[im < 0.25] = 1
    markers[im > 0.55] = 2
    seg = segmentation.watershed(elev, markers) - 1
    seg = ndi.binary_fill_holes(seg)
    lab, n = ndi.label(seg)
    sizes = ndi.sum(np.ones_like(lab), lab, range(n + 1))
    lab[np.isin(lab, np.where(sizes < 300)[0])] = 0
    return im, lab


class Plate:
    def __init__(self, box, scale, only_label=None, felt=False, seed=3, canvas=None):
        im, lab = coin_labels()
        x0, y0, x1, y1 = box
        self.box, self.s = box, scale
        crop = im[y0:y1, x0:x1]
        W, H = (x1 - x0) * scale, (y1 - y0) * scale
        self.L = np.clip(cv2.resize(crop, (W, H), interpolation=cv2.INTER_CUBIC), 0, 1)
        m = (lab[y0:y1, x0:x1] == only_label) if only_label else (lab[y0:y1, x0:x1] > 0)
        M = cv2.resize(m.astype(np.float32), (W, H), interpolation=cv2.INTER_LINEAR)
        if canvas:                                   # embed the crop, centred, in a larger synthetic-felt canvas
            CW, CH = canvas
            Lc = np.full((CH, CW), 0.055, np.float32); Mc = np.zeros((CH, CW), np.float32)
            ox, oy = (CW - W) // 2, (CH - H) // 2
            Lc[oy:oy + H, ox:ox + W] = self.L; Mc[oy:oy + H, ox:ox + W] = M
            self.L, M = Lc, Mc
        M = cv2.GaussianBlur(M, (0, 0), scale * 0.7)
        self.M = smoothstep(0.35, 0.65, M)
        s = scale
        self.A = cv2.GaussianBlur(self.L, (0, 0), 5 * s)
        band = cv2.GaussianBlur(self.L, (0, 0), 0.9 * s) - cv2.GaussianBlur(self.L, (0, 0), 4.5 * s)
        dist = ndi.distance_transform_edt(self.M > 0.5) / s
        body = 0.22 * smoothstep(0, 2.2, dist)
        self.h = cv2.GaussianBlur((body + 0.55 * band) * self.M, (0, 0), 0.6 * s)
        gy, gx = np.gradient(self.h)
        self.gx, self.gy = gx * s, gy * s          # slope per source px
        # background cloth: the photo's own dark ground (tray shots) or synthetic black felt (isolated hero)
        bg = cv2.GaussianBlur(self.L, (0, 0), 1.2 * s)
        if felt:
            bg = np.full_like(self.L, 0.055)
        self.cloth = np.clip(bg * (1 - self.M), 0, 1)
        # felt microtexture (display-res): fibres only show under low light, exactly like real felt
        rng = np.random.default_rng(seed)
        n = rng.standard_normal(self.L.shape).astype(np.float32)
        n = cv2.GaussianBlur(n, (0, 0), 0.8) * 0.6 + cv2.GaussianBlur(n, (0, 0), 2.2) * 1.4
        fy, fx = np.gradient(n)
        self.fgx, self.fgy = fx * 0.35, fy * 0.35

    def render(self, az, el, kelvin=3200, intensity=1.0, pool=None, ambient=0.0, k_relief=2.2, flat_keep=0.35):
        """az: direction the light COMES FROM, degrees, 0 = from screen right, 90 = from screen top (counter-clockwise).
        el: elevation above the table, degrees.  pool: (cx, cy, r_inner, r_outer) in output px or None."""
        a, e = np.radians(az), np.radians(max(el, 2.0))
        lx, ly = np.cos(a), -np.sin(a)                 # screen y grows downward
        facing = -(self.gx * lx + self.gy * ly)       # >0 where the surface tilts toward the light
        r = np.clip(1 + min(1 / np.tan(e), 9) * k_relief * facing, 0, 3.0)
        # soft height-field shadows (only matter below ~40 deg)
        sh = np.ones_like(self.h)
        if el < 40:
            tanel = np.tan(e)
            Hh = self.h * self.s * 6.0
            for step in range(2, int(10 * self.s), 2):
                shf = ndi.shift(Hh, (-step * ly, -step * lx), order=1, mode='nearest')
                sh = np.minimum(sh, np.clip(1 - (shf - Hh - step * tanel) * 0.8, 0, 1))
        k = flat_keep + (1 - flat_keep) * smoothstep(80, 30, el)
        base = self.A + (self.L - self.A) * k
        # Blinn-Phong glint on the relief
        nz = 1.0 / np.sqrt(1 + self.gx ** 2 + self.gy ** 2)
        nx, ny = -self.gx * nz, -self.gy * nz
        l = np.array([np.cos(e) * lx, np.cos(e) * ly, np.sin(e)])
        hv = l + np.array([0, 0, 1.0]); hv /= np.linalg.norm(hv)
        ndh = np.clip(nx * hv[0] + ny * hv[1] + nz * hv[2], 0, 1)
        spec = (ndh ** 90) * 1.1 * sh * smoothstep(0.35, 0.8, self.L) * smoothstep(70, 20, el)
        # a frontal light is a broad soft source: lower contrast, lower peak
        expo = intensity * (0.92 - 0.16 * smoothstep(30, 85, el))
        tint = kelvin_rgb(kelvin)
        metal = np.array([1.0, 0.96, 0.905], np.float32)
        coin = (base * r * (0.30 + 0.70 * sh))[..., None] * metal * tint + (spec[..., None] * tint * 1.0)
        ffacing = -(self.fgx * lx + self.fgy * ly)
        fr = np.clip(1 + min(1 / np.tan(e), 9) * 0.9 * ffacing, 0.2, 2.2)
        cloth = ((0.42 * self.cloth + 0.012) * fr)[..., None] * np.array([0.95, 0.93, 0.9]) * tint * (0.55 + 0.45 * smoothstep(60, 10, el))
        out = coin * self.M[..., None] + cloth * (1 - self.M[..., None])
        out = out * expo
        if pool is not None:
            cx, cy, r0, r1 = pool[:4]
            stretch = pool[4] if len(pool) > 4 else 1.0
            yy, xx = np.mgrid[0:out.shape[0], 0:out.shape[1]].astype(np.float32)
            u = (xx - cx) * lx + (yy - cy) * ly            # along the light direction
            v = -(xx - cx) * ly + (yy - cy) * lx
            d = np.sqrt((u / stretch) ** 2 + v ** 2)
            p = smoothstep(r1, r0, d)
            out = out * (ambient + (1 - ambient) * p[..., None])
        return np.clip(out, 0, None)


def to_u8(x, gamma=1.0):
    x = x / (1 + 0.12 * x)                      # gentle shoulder
    return (np.clip(x, 0, 1) ** (1 / gamma) * 255 + 0.5).astype(np.uint8)
