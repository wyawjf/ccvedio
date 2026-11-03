"""Look-dev plates for RAKING LIGHT (product concept). Reads only video/assets/lib/. Writes kit/img/*.png.
Run:  python3 -I video/f2/concepts/product/kit/prep.py [hero|tray|rocket|hubble|all]
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
from PIL import Image
import cv2
from relight import Plate, to_u8, smoothstep

OUT = os.path.join(HERE, 'img'); os.makedirs(OUT, exist_ok=True)
LIB = '/home/user/ccvedio/video/assets/lib/'

def save(name, arr):
    Image.fromarray(arr).save(os.path.join(OUT, name)); print('wrote', name, arr.shape)

def pool_for(p, k0=1.25, k1=2.15):
    """Light pool centred on the plate centre; radii relative to the coin radius."""
    H, W = p.L.shape
    R = np.sqrt(p.M.sum() / np.pi)
    return (W / 2, H / 2, R * k0, R * k1)

# hero coin #23: helmeted profile, bottom-left of the tray. Watershed bbox (18,233)-(75,288), ~56 px across.
HERO_BOX, HERO_LABEL = (0, 214, 94, 303), 23     # padded crop (94 x 89 src px); neighbours are masked out
which = sys.argv[1] if len(sys.argv) > 1 else 'all'
if which in ('all', 'hero'):
    for sc in (5, 6):
        hero = Plate(HERO_BOX, sc, only_label=HERO_LABEL, felt=True, canvas=(1080, 1000))
        pl = pool_for(hero, 1.35, 3.1) + (1.45,)
        save(f'hero{sc}_hook.png',  to_u8(hero.render(160, 6, 3200, 1.10, pool=pl)))
        save(f'hero{sc}_token.png', to_u8(hero.render(150, 10, 3200, 1.05, pool=pl)))
        save(f'hero{sc}_mid.png',   to_u8(hero.render(115, 34, 4300, 1.00, pool=pool_for(hero, 1.5, 3.3))))
        save(f'hero{sc}_flat.png',  to_u8(hero.render(90, 84, 5600, 1.00, pool=pool_for(hero, 1.9, 3.8))))
        save(f'hero{sc}_eval.png',  to_u8(hero.render(170, 4.5, 3000, 1.18, pool=pl)))
        save(f'hero{sc}_glass.png', to_u8(hero.render(150, 12, 3200, 1.05, pool=pool_for(hero, 1.4, 3.0) + (1.3,))))

def edge_feather(H, W, inset=110):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.minimum(np.minimum(xx, W - 1 - xx), np.minimum(yy, H - 1 - yy))
    return smoothstep(0, inset, d)[..., None]

if which in ('all', 'tray'):
    tray = Plate((0, 0, 384, 303), 3)
    H, W = tray.L.shape
    EF = edge_feather(H, W)
    _save = save
    def save(name, arr, _ef=EF):
        _save(name, (arr.astype(np.float32) * _ef).astype(np.uint8))
    save('tray_flat.png', to_u8(tray.render(90, 84, 5600, 1.0, pool=(W / 2, H / 2, W * 0.30, W * 0.62), ambient=0.0)))
    save('tray_rake.png', to_u8(tray.render(160, 9, 3200, 1.0, pool=(W / 2, H / 2, W * 0.40, W * 0.78))))
    # moving-head spot, day 三 (Wed): coin #20 at src (101,195) -> (303,585)
    save('tray_spot.png', to_u8(tray.render(128, 36, 3200, 1.30, pool=(303, 585, 62, 190), ambient=0.035)))

    save = _save

if which in ('all', 'rocket'):
    r = np.asarray(Image.open(LIB + 'rocket.jpg').convert('RGB')).astype(np.float32) / 255
    x0, y0, x1, y1 = 196, 24, 444, 427
    c = r[y0:y1, x0:x1]
    c = cv2.resize(c, ((x1 - x0) * 2, (y1 - y0) * 2), interpolation=cv2.INTER_CUBIC)
    H = c.shape[0]
    yy = np.linspace(0, 1, H)[:, None, None]
    nd = 2 ** (-1.3 * (1 - smoothstep(0.0, 0.62, yy)))          # graduated ND on the sky
    lum = c @ np.array([0.2126, 0.7152, 0.0722])
    c = lum[..., None] + (c - lum[..., None]) * 0.85
    c = np.clip(c * nd * 1.06 - 0.012, 0, 1)
    save('rocket_plate.png', (c * 255 + 0.5).astype(np.uint8))

if which in ('all', 'hubble'):
    hbl = np.asarray(Image.open(LIB + 'hubble_deep_field.jpg').convert('RGB')).astype(np.float32) / 255
    x0, y0, x1, y1 = 120, 86, 880, 786
    c = cv2.resize(hbl[y0:y1, x0:x1], (888, 818), interpolation=cv2.INTER_CUBIC)
    lum = c @ np.array([0.2126, 0.7152, 0.0722])
    c = lum[..., None] + (c - lum[..., None]) * 0.8
    c = np.clip((c - 0.02) / 0.98, 0, 1)
    save('hubble_plate.png', (c * 255 + 0.5).astype(np.uint8))

# ---- carousel 04: two pools (one 闭源, one 开源) on the dark tray
if which in ('all', 'tray2'):
    tray = Plate((0, 0, 384, 303), 3)
    H, W = tray.L.shape
    a = tray.render(128, 36, 3200, 1.30, pool=(465, 150, 62, 190), ambient=0.035)   # coin at src (155,50)
    b = tray.render(128, 36, 3200, 1.30, pool=(810, 354, 62, 190), ambient=0.035)   # coin at src (270,118)
    out = np.maximum(a, b)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.minimum(np.minimum(xx, W - 1 - xx), np.minimum(yy, H - 1 - yy))
    save('tray_spot2.png', (to_u8(out).astype(np.float32) * smoothstep(0, 110, d)[..., None]).astype(np.uint8))

# ---- the Flattening strip: one light, elevation 5 -> 84 deg, 3000K -> 5600K
if which in ('all', 'strip'):
    hero = Plate(HERO_BOX, 5, only_label=HERO_LABEL, felt=True, canvas=(560, 560))
    steps = [(170, 5, 3000), (160, 12, 3200), (140, 24, 3600), (120, 40, 4300), (100, 62, 5000), (90, 84, 5600)]
    tiles = []
    for az, el, k in steps:
        R = np.sqrt(hero.M.sum() / np.pi)
        pl = (280, 280, R * (1.35 + 0.5 * el / 84), R * (2.6 + 0.8 * el / 84))
        tiles.append(to_u8(hero.render(az, el, k, 1.1 - 0.1 * el / 84, pool=pl)))
    save('flattening_strip.png', np.hstack(tiles))
