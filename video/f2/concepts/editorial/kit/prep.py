"""PUBLIC DOMAIN (editorial concept) - reference asset prep.

Every number in editorial.md section 7 is implemented here. Sources are read ONLY from
video/assets/lib/. Output: grade plates, masks, the step-and-repeat field, the rocket slit,
contact-sheet thumbnails, paper + blind emboss, and coins.json (centroids, radii, pitches).

    python3 -I f2/concepts/editorial/kit/prep.py  [out_dir]     (default: kit/img)
"""
import json, os, sys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as ndi
from skimage import filters, measure, segmentation

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.normpath(os.path.join(HERE, '../../../../assets/lib'))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'img')
os.makedirs(OUT, exist_ok=True)

NIGHT = np.array([13, 12, 11]) / 255.0       # --night  #0D0C0B
PAPER = np.array([239, 235, 227]) / 255.0    # --paper  #EFEBE3

def load(name, mode=None):
    im = Image.open(os.path.join(LIB, name))
    return im.convert(mode) if mode else im
def f(a): return np.asarray(a, dtype=np.float64) / 255.0
def save(a, name):
    Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8)).save(os.path.join(OUT, name))

# ---------------------------------------------------------------- grades
def cdl(rgb, slope=(0.96, 0.95, 0.92), offset=(0.045, 0.040, 0.035), power=(1.05, 1.04, 1.02), sat=0.82):
    """'Vitrine' ASC-CDL for colour plates (sRGB-encoded values, applied per channel, then Rec.709 saturation)."""
    x = np.clip(rgb * np.array(slope) + np.array(offset), 0, 1) ** np.array(power)
    l = (x * np.array([0.2126, 0.7152, 0.0722])).sum(-1, keepdims=True)
    return np.clip(l + (x - l) * sat, 0, 1)

def selenium(gray, lo=(14, 13, 12), mid=(120, 115, 107), hi=(236, 230, 218)):
    """Toned silver-print ramp for greyscale plates: night -> warm grey -> cream (piecewise linear at 0.5)."""
    lo, mid, hi = (np.array(c) / 255.0 for c in (lo, mid, hi))
    t = np.clip(gray, 0, 1)[..., None]
    return np.where(t < 0.5, lo + (mid - lo) * (t / 0.5), mid + (hi - mid) * ((t - 0.5) / 0.5))

SELENIUM_PAPER = dict(lo=(40, 38, 35), mid=(140, 135, 127), hi=(226, 221, 211))   # grey plates printed on paper

def up(img, s, sharpen=True):
    """Lanczos resample; upscales get a light unsharp mask (r 1.0, 45%, thr 2)."""
    r = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    return r.filter(ImageFilter.UnsharpMask(radius=1.0, percent=45, threshold=2)) if (sharpen and s > 1) else r

def disc_blur(rgb, r, boost=2.2, thr=0.55):
    """Lens blur for the hook's rack focus: linearise (2.2), boost highlights, hard-edged disc kernel, re-encode."""
    lin = np.clip(rgb, 0, 1) ** 2.2
    l = lin.mean(-1, keepdims=True)
    lin = lin * (1 + (boost - 1) * np.clip((l - thr) / (1 - thr), 0, 1))
    if r >= 0.5:
        R = int(np.ceil(r)); y, x = np.mgrid[-R:R + 1, -R:R + 1]
        k = np.clip(r + 0.5 - np.hypot(x, y), 0, 1); k /= k.sum()
        lin = np.dstack([ndi.convolve(lin[..., c], k, mode='nearest') for c in range(3)])
    return np.clip(lin, 0, 1) ** (1 / 2.2)

# ---------------------------------------------------------------- coins: segmentation (the test this image was made for)
coins = np.asarray(load('coins.png', 'L'))
elev = filters.sobel(coins.astype(float))
markers = np.zeros_like(coins, dtype=int); markers[coins < 30] = 1; markers[coins > 150] = 2
seg = ndi.binary_fill_holes(segmentation.watershed(elev, markers) - 1)
lab = measure.label(seg)
props = sorted([p for p in measure.regionprops(lab) if p.area > 300], key=lambda p: (round(p.centroid[0] / 60), p.centroid[1]))
C = [(p.centroid[1], p.centroid[0], float(np.sqrt(p.area / np.pi))) for p in props]   # (cx, cy, r) in source px
SEGM = seg.astype(float)

# radius -> D-major-pentatonic pitch (largest coin = D5, smallest ~1.5 oct above, quantised)
PENTA = [74, 76, 78, 81, 83, 86, 88, 90, 93, 95, 98]
NAMES = {74: 'D5', 76: 'E5', 78: 'F#5', 81: 'A5', 83: 'B5', 86: 'D6', 88: 'E6', 90: 'F#6', 93: 'A6', 95: 'B6', 98: 'D7'}
rmax, rmin = max(c[2] for c in C), min(c[2] for c in C)
table = []
for i, (cx, cy, r) in enumerate(C):
    m = min(PENTA, key=lambda p: abs(p - (74 + 18 * (rmax - r) / (rmax - rmin))))
    table.append(dict(id=i + 1, cx=round(cx, 1), cy=round(cy, 1), r=round(r, 1), note=NAMES[m], hz=round(440 * 2 ** ((m - 69) / 12), 1)))
json.dump(table, open(os.path.join(OUT, 'coins.json'), 'w'), indent=1)

def _lit(scale, seq, base):
    img = up(Image.fromarray(coins), scale); g = f(img); H, W = g.shape
    m = f(up(Image.fromarray((ndi.gaussian_filter(SEGM, 1.2) * 255).astype(np.uint8)), scale, sharpen=False))
    yy, xx = np.mgrid[0:H, 0:W]
    light = np.full_like(g, base)
    for i, k in seq:                                   # key light: flat over the coin, gaussian falloff (sigma ~1.0 r)
        cx, cy, r = C[i - 1]
        d = np.hypot(xx - cx * scale, yy - cy * scale) / (r * scale)
        key = np.exp(-0.5 * (np.maximum(d - 0.85, 0) / 1.035) ** 2)
        light = np.maximum(light, base + (k - base) * key)
    cloth = np.clip((g - 0.10) / 0.90, 0, 1) ** 1.6 * 0.55     # cloth pulled toward night; coins untouched
    return selenium((m * g + (1 - m) * cloth) * light)

save(_lit(2.4, [(16, 1.0)], 0.10), 'coins_hook_x2.4.png')                       # shots 1-2, cover
save(selenium(f(up(Image.fromarray(coins), 2.0))), 'coins_plate_x2.png')       # house lights up (shot 3 start)
save(_lit(2.0, [(10, .30), (2, 1.0)], 0.10), 'coins_hop_moment_x2.png')       # shot 5 still
save(_lit(2.0, [(24, .22), (22, .36), (11, .55), (21, .78), (18, 1.0)], 0.10), 'coins_hops_multi_x2.png')  # carousel 3
for rr in (16, 8, 3):                                                          # focus-pull reference frames
    save(disc_blur(_lit(2.4, [(16, 1.0)], 0.10), rr), f'coins_hook_blur{rr:02d}.png')

# step-and-repeat: W=766 x H=606, tiles (n, w, h, gutter) = (2,381,301,4) (4,190,150,2) (8,94,74,2) (16,46,36,2)
plate_full = selenium(f(Image.fromarray(coins)))
def field(n, tw, th, g, W=766, H=606):
    canvas = np.ones((H, W, 3)) * NIGHT
    tile = f(Image.fromarray((plate_full * 255).astype(np.uint8)).resize((tw, th), Image.LANCZOS))
    for r in range(n):
        for c in range(n):
            canvas[r * (th + g):r * (th + g) + th, c * (tw + g):c * (tw + g) + tw] = tile
    return canvas
for n, tw, th, g in ((2, 381, 301, 4), (4, 190, 150, 2), (8, 94, 74, 2), (16, 46, 36, 2)):
    save(field(n, tw, th, g), f'coins_field_{n:02d}.png')

# rocket slit: source crop (250,120)-(393,423) = 143 x 303 -> x2.00 = 286 x 606 (tile columns 5-10 of the 16x16 field)
rk = load('rocket.jpg', 'RGB').crop((250, 120, 393, 423))
slit = cdl(f(up(rk, 2.0)))
save(slit, 'rocket_slit_x2.png')
fld = field(16, 46, 36, 2) * 0.42 + NIGHT * 0.58
fld[:, 240:526] = slit[:606, :286]
save(fld, 'field_slit.png')

# retina: keep the fundus camera's black surround; 488 px = x0.346 (frame 536 = 7 columns)
for s in (488, 568):
    save(cdl(f(load('retina.jpg', 'RGB').resize((s, s), Image.LANCZOS)), offset=(0.05, 0.045, 0.04), sat=0.9), f'retina_{s}.png')

# text plate on paper: 9 columns = 696 x 267 (x1.5536)
save(selenium(f(load('text.png', 'L').resize((696, 267), Image.LANCZOS)), **SELENIUM_PAPER), 'text_696.png')

# contact sheet: fit inside 216 x 162 (bottom-left aligned in layout)
SHEET = [('coins.png', 'g'), ('rocket.jpg', 'c'), ('coffee.png', 'c'), ('camera.png', 'g'), ('astronaut.png', 'c'), ('moon.png', 'g'),
         ('text.png', 'g'), ('clock_motion.png', 'g'), ('hubble_deep_field.jpg', 'c'), ('retina.jpg', 'c'), ('grace_hopper.jpg', 'c')]
for name, kind in SHEET:
    im = load(name, 'L' if kind == 'g' else 'RGB')
    s = min(216 / im.width, 162 / im.height)
    t = f(im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS))
    save(selenium(t) if kind == 'g' else cdl(t), 'th_' + name.split('.')[0] + '.png')

# paper + blind emboss
def paper(W, H, seed=7):
    r = np.random.default_rng(seed)
    low = ndi.gaussian_filter(r.standard_normal((H, W)), 48); low /= low.std()
    fib = r.standard_normal((H, W))
    fib = ndi.gaussian_filter(fib, (0.6, 5.0)) * 0.6 + ndi.gaussian_filter(fib, (5.0, 0.6)) * 0.4; fib /= fib.std()
    return np.clip(PAPER * (1 + 0.008 * low + 0.0035 * fib)[..., None], 0, 1), fib

def emboss(W, H, rect, theta_deg=135, elev_deg=24, depth=1.0, bevel=7.0, seed=7, cap=0.97):
    """Debossed rectangle (signed-distance height field, smoothstep bevel), Lambert relit by a raking light.
    theta: light azimuth (deg, 0 = from screen-right, CCW); elev: light elevation. Highlights capped at `cap`."""
    base, fib = paper(W, H, seed)
    x0, y0, x1, y1 = rect
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    dx = np.maximum(np.maximum(x0 - xx, xx - x1), 0); dy = np.maximum(np.maximum(y0 - yy, yy - y1), 0)
    inside = np.minimum(np.minimum(xx - x0, x1 - xx), np.minimum(yy - y0, y1 - yy))
    sd = np.where((dx > 0) | (dy > 0), np.hypot(dx, dy), -inside)
    t = np.clip(0.5 - sd / bevel, 0, 1); t = t * t * (3 - 2 * t)
    h = -depth * t + 0.0025 * fib * (1 - 0.6 * t)
    gy, gx = np.gradient(ndi.gaussian_filter(h, 0.8))
    n = np.dstack([-gx * 2.2, -gy * 2.2, np.ones_like(h)]); n /= np.linalg.norm(n, axis=2, keepdims=True)
    th, el = np.radians(theta_deg), np.radians(elev_deg)
    L = np.array([np.cos(th) * np.cos(el), -np.sin(th) * np.cos(el), np.sin(el)])
    return np.minimum(base * np.clip((n @ L) / L[2], 0.86, 1.06)[..., None], cap)

save(paper(1080, 1920)[0], 'paper_1080x1920.png')
save(paper(1080, 1440, seed=9)[0], 'paper_1080x1440.png')
save(emboss(1080, 1920, (72, 672, 768, 1194)), 'emboss_film_plate12.png')       # 9 columns x 522
save(emboss(1080, 1440, (72, 548, 688, 1010), seed=9), 'emboss_car_plate12.png')  # 8 columns x 462
rake = [emboss(520, 400, (60, 50, 460, 350), theta_deg=t, elev_deg=e) for t, e in ((215, 10), (135, 18), (55, 30))]
save(np.hstack(rake), 'rake_sweep_test.png')                                    # start / mid / end of the 1.6 s sweep

# index thumbnails (96 x 72) for 'our reading'
def thumb(arr, name, w=96, h=72):
    im = Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8))
    s = max(w / im.width, h / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - w) // 2, (im.height - h) // 2
    im.crop((l, t, l + w, t + h)).save(os.path.join(OUT, name))
thumb(field(16, 46, 36, 2), 'idx_field.png')
thumb(emboss(400, 300, (40, 30, 360, 270), theta_deg=135, elev_deg=14, depth=1.6, bevel=5.0, seed=3), 'idx_emboss.png')
thumb(f(load('retina.jpg', 'RGB').resize((300, 300), Image.LANCZOS)), 'idx_retina.png')

# coin 16 matted with its own segmentation mask, x2, RGBA (closing move: coin -> brand dot)
cx, cy, r = C[15]; R = int(r + 4); box = (int(cx - R), int(cy - R), int(cx + R), int(cy + R))
rgb = (selenium(f(up(Image.fromarray(coins).crop(box), 2.0))) * 255).astype(np.uint8)
alpha = np.asarray(up(Image.fromarray((ndi.gaussian_filter((lab == lab[int(cy), int(cx)]).astype(float), 0.8) * 255).astype(np.uint8)).crop(box), 2.0, sharpen=False))
Image.fromarray(np.dstack([rgb, alpha]), 'RGBA').save(os.path.join(OUT, 'coin16_matte_x2.png'))
print(f'ok: {len(C)} coins -> {OUT}')
