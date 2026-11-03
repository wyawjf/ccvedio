"""Asset prep for the look-dev of THE LAST ELEMENT (最后一片镜片).

Reads only video/assets/lib/, writes video/f2/concepts/idea/kit/img/.
    python3 -I f2/concepts/idea/kit/prep.py          (from video/)

Everything here is the reference implementation of section 7 of idea.md:
crop boxes are in SOURCE pixels, grades follow section 4.5, the coin "wear" follows section 7.1.
"""
import os
import json
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as ndi
from skimage import filters, segmentation, measure

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.abspath(os.path.join(HERE, '../../../../assets/lib'))
OUT = os.path.join(HERE, 'img')
os.makedirs(OUT, exist_ok=True)


def load(name):
    return np.asarray(Image.open(os.path.join(LIB, name))).astype(np.float32) / 255.0


def save(a, name, mode=None):
    a = np.clip(a, 0, 1)
    Image.fromarray((a * 255 + 0.5).astype(np.uint8), mode).save(os.path.join(OUT, name))


def upscale(a, s, sharpen=0.30):
    """Lanczos upscale + gentle unsharp (radius 1.2 display px). Works on HxW or HxWxC float arrays."""
    h, w = a.shape[:2]
    im = Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8))
    im = im.resize((int(round(w * s)), int(round(h * s))), Image.LANCZOS)
    if sharpen:
        im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=int(sharpen * 100), threshold=1))
    return np.asarray(im).astype(np.float32) / 255.0


# ---------------------------------------------------------------- grade (section 4.5)
def hue_rgb(h):
    """unit-saturation colour for hue in degrees, normalised to zero mean (used as a split-tone direction)."""
    h = (h % 360) / 60.0
    c = np.array([abs(h - 3) - 1, 2 - abs(h - 2), 2 - abs(h - 4)], np.float32)
    c = np.clip(c, 0, 1)
    return c - c.mean()


LUMA = np.array([0.2126, 0.7152, 0.0722], np.float32)


def grade(img, sat=0.82, lift=0.012, gamma=0.95, gain=0.93, sh_hue=210, sh_amt=0.06, hi_hue=36, hi_amt=0.08, knee=0.82):
    x = img.astype(np.float32)
    x = np.clip(gain * (x + lift * (1 - x)), 0, None) ** (1 / gamma)
    L = x @ LUMA
    x = L[..., None] + sat * (x - L[..., None])
    ws = ((1 - L) ** 2)[..., None]
    wh = (L ** 2)[..., None]
    x = x + ws * sh_amt * hue_rgb(sh_hue) + wh * hi_amt * hue_rgb(hi_hue)
    # soft shoulder above the knee
    over = np.clip(x - knee, 0, None)
    x = np.where(x > knee, knee + (1 - knee) * (1 - np.exp(-over / (1 - knee))), x)
    return np.clip(x, 0, 1)


SILVER_LO = np.array([0.050, 0.046, 0.042], np.float32)   # #0D0C0B
SILVER_HI = np.array([0.930, 0.900, 0.850], np.float32)   # #EDE6D9


def silver(L, contrast=0.15, pivot=0.42):
    """warm-silver toning for monochrome plates: S-curve, then per-channel gamma for warm mids."""
    L = np.clip(L, 0, 1)
    s = L + contrast * (L - pivot) * (1 - np.abs(2 * L - 1))
    s = np.clip(s, 0, 1)
    ch = np.stack([s ** 0.97, s ** 1.00, s ** 1.06], -1)
    return SILVER_LO + (SILVER_HI - SILVER_LO) * ch


# ---------------------------------------------------------------- 7.1 coins
coins = load('coins.png')
el = filters.sobel(coins)
markers = np.zeros(coins.shape, int)
markers[coins < 30 / 255] = 1
markers[coins > 150 / 255] = 2
seg = ndi.binary_fill_holes(segmentation.watershed(el, markers) - 1)
lab, _ = ndi.label(seg)
props = [p for p in measure.regionprops(lab) if p.area > 300]
props.sort(key=lambda p: (round(p.centroid[0] / 60), p.centroid[1]))
table = []
for i, p in enumerate(props):
    cy, cx = p.centroid
    y0, x0, y1, x1 = p.bbox
    table.append(dict(id=i, cx=round(cx, 1), cy=round(cy, 1), r=round(float(np.sqrt(p.area / np.pi)), 1),
                      bbox=[int(x0), int(y0), int(x1), int(y1)], label=int(p.label)))
json.dump(table, open(os.path.join(OUT, 'coins.json'), 'w'), indent=1)

HERO = table[15]                      # the facing head, centre (212.4, 193.1), r 23.5
HERO_BOX = (182, 163, 243, 224)       # 61 x 61 source px


def wear(img, mask, cx, cy, r, w):
    """Blend a coin towards a blank token. w=0 original, w=1 blank. Centre (high relief) wears first, rim survives."""
    yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]].astype(np.float32)
    dx, dy = xx - cx, yy - cy
    rho = np.sqrt(dx ** 2 + dy ** 2) / r
    inner = mask * np.clip((0.90 - rho) / 0.08, 0, 1)              # keep the outer 10% (the rim) intact
    mu = img[inner > 0.5].mean()
    shade = 0.07 * (-(dx + dy) / (np.sqrt(2) * r))                    # key light from upper left
    ghost = img - ndi.gaussian_filter(img, 1.5)                        # 12% of the old relief remains
    blank = mu * (1 + shade) + 0.12 * ghost
    wl = np.clip(w * 1.4 - 0.4 * rho, 0, 1) * inner
    return img * (1 - wl) + blank * wl


hero_mask = (lab == HERO['label']).astype(np.float32)
hero_mask = ndi.gaussian_filter(hero_mask, 0.7)
x0, y0, x1, y1 = HERO_BOX
for k, w in enumerate([0, 0.25, 0.5, 0.75, 1.0]):
    wl = wear(coins, hero_mask, HERO['cx'], HERO['cy'], HERO['r'], w)
    crop = wl[y0:y1, x0:x1]
    save(silver(upscale(crop, 6.0, 0.25)), f'coin_hero_w{k}.png')          # 366 x 366 (6x); draw at <= 4.5x for faces

# whole tray, original and fully worn (for the film's S3 end state / carousel alternates)
tray_worn = coins.copy()
for p in table:
    m = ndi.gaussian_filter((lab == p['label']).astype(np.float32), 0.7)
    tray_worn = wear(tray_worn, m, p['cx'], p['cy'], p['r'], 1.0)
save(silver(upscale(coins, 2.0, 0.25)), 'tray.png')
# mid-way through the wear cascade (film S3 at t = 9.6 s): farthest coins first, the hero keeps its face longest
order = sorted(table, key=lambda p: -np.hypot(p['cx'] - HERO['cx'], p['cy'] - HERO['cy']))
tray_mid = coins.copy()
for rank, p in enumerate(order):
    start = 0.11 * rank + (0.3 if p['id'] == HERO['id'] else 0)
    w = float(np.clip((1.6 - start) / 0.6, 0, 1))            # 1.6 s into the cascade
    w = w * w * (3 - 2 * w)
    if w > 0:
        m = ndi.gaussian_filter((lab == p['label']).astype(np.float32), 0.7)
        tray_mid = wear(tray_mid, m, p['cx'], p['cy'], p['r'], w)
save(silver(upscale(tray_mid, 2.0, 0.25)), 'tray_mid.png')
save(silver(upscale(tray_worn, 2.0, 0.25)), 'tray_worn.png')

# ---------------------------------------------------------------- 7.2 espresso (1.5x)
coffee = load('coffee.png')[..., :3]
save(upscale(grade(coffee, sat=0.84, hi_amt=0.07), 1.5, 0.2), 'espresso.png')

# ---------------------------------------------------------------- 7.3 rocket (2.2x for the tele end)
rocket = load('rocket.jpg')[..., :3]
save(upscale(grade(rocket, sat=0.80, sh_amt=0.05, gain=0.95), 2.2, 0.25), 'rocket.png')

# ---------------------------------------------------------------- 7.4 Hubble plates
hub = load('hubble_deep_field.jpg')[..., :3]
HB = (220, 150, 780, 710)            # 560 x 560 source px
hcrop = hub[HB[1]:HB[3], HB[0]:HB[2]]
D = hcrop.shape[0]
yy, xx = np.mgrid[0:D, 0:D]
disc = ndi.gaussian_filter(((xx - D / 2 + .5) ** 2 + (yy - D / 2 + .5) ** 2 <= (D / 2 - 3) ** 2).astype(np.float32), 0.8)
colour = grade(np.clip(hcrop * 1.25, 0, 1), sat=0.86, sh_amt=0.03, hi_amt=0.05, lift=0.0)


def plate(ch):
    return silver(np.clip(hcrop[..., ch] * 1.35 + 0.035, 0, 1)) * disc[..., None] * 0.72


plates = [plate(c) for c in range(3)]


def screen(a, b):
    return 1 - (1 - a) * (1 - b)


def venn(W, H, cx, cy, offs, k, bloom=0.0, tri_colour=False, scale=1.0):
    """offs: three (dx, dy) when fully apart; k: 1 apart -> 0 registered. Returns HxWx3 on black."""
    Dd = int(round(D * scale))
    pl = [upscale(p, scale, 0) if scale != 1 else p for p in plates]
    dk = upscale(disc, scale, 0) if scale != 1 else disc
    col = upscale(colour, scale, 0) if scale != 1 else colour
    out = np.zeros((H, W, 3), np.float32)
    masks = []
    for p, (dx, dy) in zip(pl, offs):
        ox, oy = int(round(cx - Dd / 2 + dx * k)), int(round(cy - Dd / 2 + dy * k))
        layer = np.zeros_like(out)
        layer[oy:oy + Dd, ox:ox + Dd] = p
        out = screen(out, layer)
        m = np.zeros((H, W), np.float32)
        m[oy:oy + Dd, ox:ox + Dd] = dk
        masks.append(m)
    if tri_colour:
        tri = masks[0] * masks[1] * masks[2]
        tri = ndi.gaussian_filter(tri, 1.2)
        ox, oy = int(round(cx - Dd / 2)), int(round(cy - Dd / 2))
        cl = np.zeros_like(out)
        cl[oy:oy + Dd, ox:ox + Dd] = col * dk[..., None]
        out = out * (1 - tri[..., None]) + cl * tri[..., None]
    if bloom > 0:
        ox, oy = int(round(cx - Dd / 2)), int(round(cy - Dd / 2))
        cl = np.zeros_like(out)
        cl[oy:oy + Dd, ox:ox + Dd] = col * dk[..., None]
        out = out * (1 - bloom) + cl * bloom
    return np.clip(out, 0, 1)


# film S6 at t=27.4 s (k = 0.45 on the way in), plates drawn at 1.0x; region 1080 x 1160 from y=0
FILM_OFFS = [(-160, -120), (160, -120), (0, 150)]
save(venn(1080, 1160, 540, 700, FILM_OFFS, 0.45), 'venn_film_mid.png')
save(venn(1080, 1160, 540, 700, FILM_OFFS, 0.0, bloom=1.0), 'venn_film_done.png')
# carousel C4: three plates at 0.82x (diameter 460), centre (540, 600), colour only where all three overlap
CA_OFFS = [(-130, -75), (130, -75), (0, 150)]
save(venn(1080, 1100, 540, 600, CA_OFFS, 1.0, tri_colour=True, scale=460 / 560), 'venn_carousel.png')

# ---------------------------------------------------------------- 7.5 handwriting, synthetic depth of field (film S7)
txt = load('text.png')
yy, xx = np.mgrid[0:txt.shape[0], 0:txt.shape[1]].astype(np.float32)
depth = (yy - 64) / 86 + 0.15 * (xx - 224) / 224             # the paper is a tilted plane; 0 = the original focal band


def dof(img, d_f, A, scale=2.45, cap=22.0):
    sig_disp = np.minimum(cap, 9.0 * A * np.abs(depth - d_f))   # blur in DISPLAY px
    sig = sig_disp / scale / 2.0                                 # as a Gaussian sigma in source px
    levels = np.array([0, 0.5, 1, 1.5, 2, 3, 4, 5], np.float32)
    stack = np.stack([img if l == 0 else ndi.gaussian_filter(img, l) for l in levels])
    k = np.clip(np.interp(sig, levels, np.arange(len(levels))), 0, len(levels) - 1.001)
    i0 = np.floor(k).astype(int); f = k - i0
    out = np.take_along_axis(stack, i0[None], 0)[0] * (1 - f) + np.take_along_axis(stack, (i0 + 1)[None], 0)[0] * f
    return out


save(silver(upscale(dof(txt, 0.62, 1.3), 2.45, 0)), 'text_dof.png')      # S7, t = 33.0 s: focus has wandered past the ink
# ---------------------------------------------------------------- 7.6 clock (film S8 insert)
save(silver(upscale(load('clock_motion.png'), 1.5, 0)), 'clock.png')

# ---------------------------------------------------------------- 7.7 retina
ret = load('retina.jpg')[..., :3]
RC, RR = (704, 703), 690                       # mask radius 690 drops the camera's orientation notch at 1:30
yy, xx = np.mgrid[0:ret.shape[0], 0:ret.shape[1]]
rm = ndi.gaussian_filter((((xx - RC[0]) ** 2 + (yy - RC[1]) ** 2) <= RR ** 2).astype(np.float32), 1.5)
rg = grade(ret, sat=0.92, gain=0.92, hi_amt=0.06, sh_amt=0.04) * rm[..., None]
crop = rg[RC[1] - RR:RC[1] + RR, RC[0] - RR:RC[0] + RR]           # 1380 x 1380, fovea ~ (689, 692)
save(crop, 'retina.png')

print('prep done ->', OUT)
print('hero coin', HERO)
