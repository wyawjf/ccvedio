"""Step 1 (Appendix B): graded full-resolution plates, the coin matte and table, Hubble FG/BG layers,
paper albedo and plate-mark normals. Reads only assets/lib/, writes build/f2/cache/.

    python3 f2/prod/prep.py
"""
import json
import os
import sys

import cv2
import numpy as np
from scipy import ndimage as ndi

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (CACHE, INK, PAPER, W, H, cgrade, halation, load_gray, load_rgb, luma, mono,  # noqa: E402
                    save_npy, save_png, smoothstep)

QA = os.path.join(CACHE, 'qa')

# Appendix A: pitch mapping, D minor pentatonic
PENT = {0: 'C', 2: 'D', 5: 'F', 7: 'G', 9: 'A'}


def midi_name(m):
    return f"{PENT[m % 12]}{m // 12 - 1}"


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def coins():
    from skimage import filters, measure, segmentation
    g = load_gray('coins.png')                              # 303 x 384
    u8 = (g * 255 + 0.5).astype(np.uint8)
    elev = filters.sobel(u8.astype(float))
    markers = np.zeros_like(u8, dtype=int)
    markers[u8 < 30] = 1
    markers[u8 > 150] = 2
    seg = ndi.binary_fill_holes(segmentation.watershed(elev, markers) - 1)
    lab = measure.label(seg)
    props = sorted([p for p in measure.regionprops(lab) if p.area > 300],
                   key=lambda p: (round(p.centroid[0] / 60), p.centroid[1]))
    assert len(props) == 24, len(props)
    rs = [np.sqrt(p.area / np.pi) for p in props]
    rmax, rmin = max(rs), min(rs)
    allowed = [m for m in range(60, 100) if m % 12 in PENT]
    table = []
    for i, p in enumerate(props, 1):
        cy, cx = p.centroid
        r = np.sqrt(p.area / np.pi)
        target = 74 + 18 * (rmax - r) / (rmax - rmin)
        m = min(allowed, key=lambda a: (abs(a - target), a))
        table.append(dict(id=i, cx=round(float(cx), 1), cy=round(float(cy), 1), r=round(float(r), 1),
                          label=int(lab[int(cy), int(cx)]), note=midi_name(m), hz=round(hz(m), 2)))
    # the bible's Appendix A values (checked, not trusted)
    ref = {16: (212.4, 193.1, 23.5, 'D6'), 18: (347.0, 186.7, 31.6, 'D5'), 6: (334.7, 43.5, 28.8, 'F5'),
           9: (153.5, 127.2, 18.5, 'G6')}
    for k, (cx, cy, r, note) in ref.items():
        c = table[k - 1]
        assert abs(c['cx'] - cx) < 0.11 and abs(c['cy'] - cy) < 0.11 and abs(c['r'] - r) < 0.11, (k, c)
        assert c['note'] == note, (k, c['note'], note)
    matte = cv2.GaussianBlur(seg.astype(np.float32), (0, 0), 0.8)
    labels = lab.astype(np.int32)
    json.dump(table, open(os.path.join(CACHE, 'coins.json'), 'w'), indent=1)
    save_npy('coins_gray.npy', g)
    save_npy('coins_matte.npy', matte)
    np.save(os.path.join(CACHE, 'coins_labels.npy'), labels)
    save_npy('coins_full.npy', mono(g))                    # house lights up (sheet cell 01, C1)
    save_png(os.path.join(QA, 'coins_full.png'), mono(g))
    print('coins: 24 segmented, #16', table[15])


def coffee():
    a = cgrade(load_rgb('coffee.png'), 0.84)
    hal = halation(a, 0.80, 10.0, 0.22)                     # hero scale x1.00
    save_npy('coffee_rgb.npy', np.clip(a + hal, 0, 1))
    save_npy('coffee_hal.npy', hal)
    save_png(os.path.join(QA, 'coffee.png'), a + hal)


def rocket():
    src = load_rgb('rocket.jpg')                            # 427 x 640
    L = src.mean(-1)
    gy, gx = np.gradient(ndi.gaussian_filter(L, 1.0))
    g = np.hypot(gx, gy)
    mask = (g < 0.012).astype(np.float32)
    mask[330:] = 0
    mask = ndi.gaussian_filter(mask, 2)[..., None]
    blur = np.stack([ndi.gaussian_filter(src[..., c], 1.4) for c in range(3)], -1)
    deb = src * (1 - mask) + blur * mask                    # §7.2 deblock the dusk sky first
    a = cgrade(deb, 0.74)
    hal = halation(a, 0.78, 10.0 / 2.0, 0.22)               # hero scale x2.00 in the slit
    save_npy('rocket_rgb.npy', np.clip(a + hal, 0, 1))
    save_npy('rocket_hal.npy', hal)
    save_png(os.path.join(QA, 'rocket.png'), a + hal)


def hubble():
    a = cgrade(load_rgb('hubble_deep_field.jpg'), 0.86)      # 872 x 1000
    s = 1.08
    hal = halation(a, 0.62, 10.0 / s, 0.22)
    L = luma(a)
    fg = (cv2.GaussianBlur(L, (0, 0), 2.0 / s) > 0.30).astype(np.uint8)
    k = int(round(3 / s)) * 2 + 1
    fg = cv2.dilate(fg, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
    fga = cv2.GaussianBlur(fg.astype(np.float32), (0, 0), 2.0 / s)
    u8 = (np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8)
    med = cv2.medianBlur(u8, 15).astype(np.float32) / 255.0
    bg = a * (1 - fga[..., None]) + med * fga[..., None]     # BG: bright galaxies median-filled
    fg_pre = a * fga[..., None]                              # FG premultiplied by its alpha
    save_npy('hubble_bg.npy', bg)
    save_npy('hubble_fg.npy', fg_pre)
    save_npy('hubble_fga.npy', fga)
    save_npy('hubble_hal.npy', hal)                          # glow travels with the FG layer
    save_npy('hubble_full.npy', np.clip(a + hal, 0, 1))     # flat version for the contact sheet
    save_png(os.path.join(QA, 'hubble_bg.png'), bg)
    save_png(os.path.join(QA, 'hubble_fg.png'), fg_pre + hal)
    print('hubble: FG coverage', round(float(fga.mean()), 4))


def retina():
    a = cgrade(load_rgb('retina.jpg'), 0.86)                # 1411 x 1411
    hal = halation(a, 0.70, 10.0 / 0.5301, 0.28)            # hero scale x0.5301 (748 px)
    save_npy('retina_rgb.npy', a)                            # terminator is applied before halation
    save_npy('retina_hal.npy', hal)
    save_npy('retina_full.npy', np.clip(a + hal, 0, 1))     # fully lit print (S05 after the rise, sheet)
    save_png(os.path.join(QA, 'retina.png'), a + hal)


def sheet_only():
    save_npy('camera.npy', mono(load_gray('camera.png')))
    save_npy('astronaut.npy', cgrade(load_rgb('astronaut.png'), 0.82))
    save_npy('grace_hopper.npy', cgrade(load_rgb('grace_hopper.jpg'), 0.82))
    save_npy('moon.npy', mono(load_gray('moon.png')))
    save_npy('text.npy', mono(load_gray('text.png')[0:172, 87:360]))   # the only cropped thumbnail
    save_npy('clock.npy', mono(load_gray('clock_motion.png')))


# ---------------------------------------------------------------- paper + plate mark (§7.3)
def rrect_sd(xx, yy, x0, y0, x1, y1, rad):
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    hx, hy = (x1 - x0) / 2 - rad, (y1 - y0) / 2 - rad
    qx, qy = np.abs(xx - cx) - hx, np.abs(yy - cy) - hy
    return np.hypot(np.maximum(qx, 0), np.maximum(qy, 0)) + np.minimum(np.maximum(qx, qy), 0) - rad


def paper_and_mark(w, h, rect, seed, depth=0.8):
    """Returns (albedo HxWx3, normals HxWx3). Shade later with plate_shade(normals, az, el)."""
    r = np.random.default_rng(seed)
    low = ndi.gaussian_filter(r.standard_normal((h, w)).astype(np.float32), 48)
    low /= low.std()
    f = r.standard_normal((h, w)).astype(np.float32)
    fib = 0.7 * ndi.gaussian_filter(f, (0.7, 2.2)) + 0.3 * ndi.gaussian_filter(f, (2.2, 0.7))
    fib /= fib.std()
    albedo = PAPER[None, None, :] * (1 + 0.008 * low + 0.0025 * fib)[..., None]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    sd = rrect_sd(xx + 0.5, yy + 0.5, *rect, 9.0)
    t = smoothstep(0.0, 1.0, 0.5 - sd / 14.0)
    hgt = -depth * t + 0.22 * depth * np.exp(-((sd - 8.4) / 12.6) ** 2) * (sd > 0)
    hgt = ndi.gaussian_filter(hgt.astype(np.float32), 4.0)
    hgt += 0.006 * fib * (1 - 0.65 * t)
    gy, gx = np.gradient(hgt)
    n = np.dstack([-gx, -gy, np.ones_like(hgt)]).astype(np.float32)
    n /= np.linalg.norm(n, axis=2, keepdims=True)
    wipe = ndi.gaussian_filter(r.standard_normal((h, w)).astype(np.float32), (30, 90))
    wipe /= wipe.std()
    albedo *= (1 - 0.018 * (1 + 0.35 * wipe) * t)[..., None] * (np.array([1.0, 0.995, 0.985], np.float32)[None, None, :] ** t[..., None])
    return albedo.astype(np.float32), n


def plate_shade(n, az, el):
    th, e = np.radians(az), np.radians(el)
    L = np.array([np.cos(th) * np.cos(e), -np.sin(th) * np.cos(e), np.sin(e)], np.float32)
    return np.clip((n @ L) / L[2], 0.70, 1.25).astype(np.float32)


def measure_mark(img, rect):
    x0, y0, x1, y1 = rect
    Lm = luma(img)
    base = np.median(Lm[y0 - 120:y0 - 40, x0 + 40:x1 - 40])
    top = Lm[y0 - 6:y0 + 16, x0 + 60:x1 - 60].min(axis=0).mean() / base - 1
    left = Lm[y0 + 60:y1 - 60, x0 - 6:x0 + 16].min(axis=1).mean() / base - 1
    bot = Lm[y1 - 16:y1 + 6, x0 + 60:x1 - 60].max(axis=0).mean() / base - 1
    right = Lm[y0 + 60:y1 - 60, x1 - 16:x1 + 6].max(axis=1).mean() / base - 1
    inside = np.median(Lm[y0 + 60:y1 - 60, x0 + 60:x1 - 60]) / base - 1
    return dict(top=round(float(top) * 100, 1), left=round(float(left) * 100, 1), bottom=round(float(bot) * 100, 1),
                right=round(float(right) * 100, 1), inside=round(float(inside) * 100, 1))


def paper(depth):
    rect = (90, 540, 732, 968)                              # S08 rest rect (paper space = screen at rest)
    alb, n = paper_and_mark(W, H, rect, seed=7, depth=depth)
    save_npy('paper_albedo.npy', alb)
    save_npy('paper_normals.npy', n)
    rest = np.minimum(alb * plate_shade(n, 135, 24)[..., None], 0.985)
    m = measure_mark(rest, rect)
    save_png(os.path.join(QA, 'paper_rest.png'), rest)
    print('plate mark at rest (target top/left -13..-17, bottom/right +4..+7, inside -2..-4 %):', m)
    return m


if __name__ == '__main__':
    os.makedirs(QA, exist_ok=True)
    only = sys.argv[1:]
    steps = dict(coins=coins, coffee=coffee, rocket=rocket, hubble=hubble, retina=retina, sheet=sheet_only,
                 paper=lambda: paper(float(os.environ.get('EMBOSS_DEPTH', '0.9'))))
    for k, fn in steps.items():
        if not only or k in only:
            fn()
    print('prep done ->', CACHE)
