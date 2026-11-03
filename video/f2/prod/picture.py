"""Picture layer of the film (§3.3, §6.4, §7): ink ground, photographs, light, hairlines. Type is a separate
layer (type.html); post is film.py. Frame values are float32 sRGB.

    python3 f2/prod/picture.py --frames 0,44,200 --out build/f2/pic_test [--type]
"""
import math
import os
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geom  # noqa: E402
from common import (BONE, EASE, GLINT, H, INK, INK_LIN, W, ease, halation, lerp, load_npy, luma,  # noqa: E402
                    mono, save_png, screen_box, smoothstep, span, to_lin, to_srgb, warp, coins_table, cache_path)

YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)
XX += 0.5
YY += 0.5


def develop(rgb, E, noise, mode='in', hal=None, L=None):
    """§6.4 develop: highlights first (in) or shadows vanish first (out). The threshold is jittered by grain."""
    if L is None:
        L = luma(rgb)
    e = 1 - 1.15 * E if mode == 'in' else -0.15 + 1.15 * E
    a = smoothstep(e - 0.10, e + 0.02, L + noise * 0.12)
    out = INK + (rgb - INK) * a[..., None]
    if mode == 'in' and hal is not None and E < 1:
        out = out + hal * (0.8 * (1 - E)) * (L >= 0.8)[..., None]
    return out.astype(np.float32)


def disc_kernel(r):
    n = int(math.ceil(r)) + 1
    y, x = np.mgrid[-n:n + 1, -n:n + 1].astype(np.float32)
    k = np.clip(r + 0.5 - np.hypot(x, y), 0, 1)
    return (k / k.sum()).astype(np.float32)


def rrect_sd(xx, yy, x0, y0, x1, y1, rad):
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    hx, hy = (x1 - x0) / 2 - rad, (y1 - y0) / 2 - rad
    qx, qy = np.abs(xx - cx) - hx, np.abs(yy - cy) - hy
    return np.hypot(np.maximum(qx, 0), np.maximum(qy, 0)) + np.minimum(np.maximum(qx, qy), 0) - rad


def hairline(img, rect, alpha, radius=0.0, progress=1.0, color=BONE):
    """1 px hairline, DOM convention: border drawn just inside rect (x, y, w, h). Draws on clockwise from
    the top-left corner when progress < 1."""
    if alpha <= 0 or progress <= 0:
        return
    x, y, w, h = rect
    x0, y0, x1, y1 = x + 0.5, y + 0.5, x + w - 0.5, y + h - 0.5
    bx0, by0 = max(0, int(math.floor(x)) - 2), max(0, int(math.floor(y)) - 2)
    bx1, by1 = min(W, int(math.ceil(x + w)) + 2), min(H, int(math.ceil(y + h)) + 2)
    if bx1 <= bx0 or by1 <= by0:
        return
    xx, yy = XX[by0:by1, bx0:bx1], YY[by0:by1, bx0:bx1]
    sd = rrect_sd(xx, yy, x0, y0, x1, y1, radius)
    cov = np.clip(1 - np.abs(sd), 0, 1)
    if progress < 1:
        ww, hh = x1 - x0, y1 - y0
        P = 2 * (ww + hh)
        d = np.stack([np.abs(yy - y0), np.abs(xx - x1), np.abs(yy - y1), np.abs(xx - x0)])
        edge = d.argmin(0)
        arc = np.choose(edge, [xx - x0, ww + (yy - y0), ww + hh + (x1 - xx), 2 * ww + hh + (y1 - yy)])
        cov = cov * np.clip(progress * P - arc + 0.5, 0, 1)
    a = (alpha * cov)[..., None]
    region = img[by0:by1, bx0:bx1]
    img[by0:by1, bx0:bx1] = region * (1 - a) + color * a


class Picture:
    def __init__(self):
        n = load_npy
        self.coins = coins_table()
        self.coins_gray, self.coins_matte = n('coins_gray.npy'), n('coins_matte.npy')
        labels = np.load(cache_path('coins_labels.npy'))
        c16 = self.coins[15]
        self.matte16 = cv2.GaussianBlur((labels == c16['label']).astype(np.float32), (0, 0), 0.8)
        self.cells = {k: n(k + '.npy') for k in ('coins_full', 'coffee_rgb', 'rocket_rgb', 'hubble_full', 'retina_full',
                                                 'camera', 'astronaut', 'grace_hopper', 'moon', 'text', 'clock')}
        self.coffee_hal = n('coffee_hal.npy')
        self.rocket_hal = n('rocket_hal.npy')
        self.hub = dict(bg=n('hubble_bg.npy'), fg=n('hubble_fg.npy'), fga=n('hubble_fga.npy'), hal=n('hubble_hal.npy'))
        self.retina_rgb, self.retina_full = n('retina_rgb.npy'), self.cells['retina_full']
        self.paper_alb, self.paper_n = n('paper_albedo.npy'), n('paper_normals.npy')
        d = np.sqrt(((XX - 678) / 460) ** 2 + ((YY - 1000) / 300) ** 2)
        self.hook_vis = (1 - smoothstep(0.45, 1.0, d)).astype(np.float32)
        self._noise_key, self._noise = None, None
        self._paper_rest = None

    # ------------------------------------------------------------ helpers
    def noise(self, f, box):
        k = int(f)
        if self._noise_key != k:
            r = np.random.default_rng(10007 + k)
            small = r.random((int(math.ceil(H / 1.35)), int(math.ceil(W / 1.35))), dtype=np.float32)
            self._noise = cv2.resize(small, (W, H), interpolation=cv2.INTER_LINEAR)
            self._noise_key = k
        x0, y0, x1, y1 = box
        return self._noise[y0:y1, x0:x1] - 0.5

    @staticmethod
    def paste(img, box, rgb, cov):
        x0, y0, x1, y1 = box
        a = cov[..., None]
        img[y0:y1, x0:x1] = img[y0:y1, x0:x1] * (1 - a) + rgb * a

    def coins_dissolve(self, s, ox, oy, lights_src, fill):
        box = screen_box(s, ox, oy, 384, 303)
        g, cov = warp(self.coins_gray, s, ox, oy, box)
        m, _ = warp(self.coins_matte, s, ox, oy, box, sharpen=False)
        x0, y0, x1, y1 = box
        xx, yy = XX[y0:y1, x0:x1], YY[y0:y1, x0:x1]
        L = np.full(g.shape, fill, np.float32)
        for cx, cy, r, k in lights_src:
            sx, sy, sr = ox + cx * s, oy + cy * s, r * s
            d = np.sqrt((xx - sx) ** 2 + (yy - sy) ** 2) / sr
            L = np.maximum(L, fill + (k - fill) * np.exp(-0.5 * (np.maximum(d - 0.85, 0) / 1.035) ** 2))
        g = np.clip(g, 0, 1)
        cloth = np.clip((g - 0.10) / 0.90, 0, 1) ** 1.6 * 0.55
        v = (m * g + (1 - m) * cloth) * L
        return box, mono(v), cov

    # ------------------------------------------------------------ shots
    def s01(self, t, f):
        img = np.empty((H, W, 3), np.float32)
        img[:] = INK
        s = geom.hook_scale(t)
        ox, oy = geom.hook_origin(s)
        c16 = self.coins[15]
        box, rgb, cov = self.coins_dissolve(s, ox, oy, [(c16['cx'], c16['cy'], c16['r'], 1.0)], 0.10)
        x0, y0, x1, y1 = box
        layer = INK + (rgb - INK) * cov[..., None]
        rad = geom.hook_focus_radius(t)
        if rad > 0.25:                                   # §3.3 S01 bokeh: linear light, boosted highlights, disc
            lin = to_lin(layer)
            boost = 1 + 1.2 * smoothstep(0.55, 1.0, luma(layer)) * min(1.0, rad / 6)
            lin = cv2.filter2D(lin * boost[..., None], -1, disc_kernel(rad), borderType=cv2.BORDER_REFLECT)
            layer = to_srgb(np.minimum(lin, 1.0))
        if 44 <= t <= 52:                                # glint across #16, clipped by its matte
            u = EASE['GLINT'](span(t, 44, 52))
            r = c16['r'] * s
            pos = -1.2 * r + 2.4 * r * u
            xx, yy = XX[y0:y1, x0:x1], YY[y0:y1, x0:x1]
            dist = (xx - geom.HOOK_ANCHOR[0]) * 0.5 + (yy - geom.HOOK_ANCHOR[1]) * 0.8660254 - pos
            m16, _ = warp(self.matte16, s, ox, oy, box, sharpen=False)
            band = 0.30 * np.exp(-0.5 * (dist / 6.0) ** 2) * m16
            layer = to_srgb(to_lin(layer) + band[..., None] * to_lin(GLINT))
        vis = self.hook_vis[y0:y1, x0:x1][..., None]
        img[y0:y1, x0:x1] = INK + (layer - INK) * vis
        return img

    def s02(self, t, f):
        img = np.empty((H, W, 3), np.float32)
        img[:] = INK
        w = geom.slit_width(t)
        xl, xr = geom.SLIT_CX - w / 2, geom.SLIT_CX + w / 2
        if t < 314:
            s = geom.coffee_scale(t)
            ox, oy = geom.coffee_origin(s)
            box = screen_box(s, ox, oy, 600, 400)
            rgb, cov = warp(self.cells['coffee_rgb'], s, ox, oy, box)
            L0 = luma(rgb)
            E_in = ease('DEVELOP', t, 116, 149)
            if E_in < 1:
                hal, _ = warp(self.coffee_hal, s, ox, oy, box, sharpen=False)
                rgb = develop(rgb, E_in, self.noise(f, box), 'in', hal, L0)
            expo = lerp(1.0, 0.35, span(t, 244, 256))   # house lights down (linear light)
            if expo < 1:
                rgb = to_srgb(INK_LIN + (to_lin(rgb) - INK_LIN) * expo)
            E_out = ease('DEVELOP', t, 287, 314)
            if E_out > 0:
                rgb = develop(rgb, E_out, self.noise(f, box), 'out', L=L0)
            if w > 0:
                x0, y0, x1, y1 = box
                xs = np.arange(x0, x1, dtype=np.float32)
                colcov = np.clip(np.minimum(xs + 1 - xl, xr - xs), 0, 1)
                ys = np.arange(y0, y1)
                rowin = ((ys >= geom.SLIT_Y0) & (ys < geom.SLIT_Y1)).astype(np.float32)
                cov = cov * (1 - rowin[:, None] * colcov[None, :])
            self.paste(img, box, rgb, cov)
        if t >= 260 and w > 0.01:
            p = geom.slit_push(t)
            ox, oy, s = geom.rocket_origin(p)
            box = (max(0, int(math.floor(xl))), geom.SLIT_Y0, min(W, int(math.ceil(xr))), geom.SLIT_Y1)
            rgb, cov = warp(self.cells['rocket_rgb'], s, ox, oy, box)
            E = ease('DEVELOP', t, 260, 290)
            if E < 1:
                hal, _ = warp(self.rocket_hal, s, ox, oy, box, sharpen=False)
                rgb = develop(rgb, E, self.noise(f, box), 'in', hal)
            xs = np.arange(box[0], box[2], dtype=np.float32)
            colcov = np.clip(np.minimum(xs + 1 - xl, xr - xs), 0, 1)
            self.paste(img, box, rgb, cov * colcov[None, :])
        return img

    def s03(self, t, f):
        img = np.empty((H, W, 3), np.float32)
        img[:] = INK
        s, ox, oy = geom.tray_tf(geom.tray_drift(t))
        box, rgb, cov = self.coins_dissolve(s, ox, oy, geom.router_lights(t, self.coins), 0.10)
        E = ease('DEVELOP', t, 380, 419)
        if E < 1:
            rgb = develop(rgb, E, self.noise(f, box), 'in')
        self.paste(img, box, rgb, cov)
        return img

    def s04(self, t, f):
        img = np.empty((H, W, 3), np.float32)
        img[:] = INK
        y0b, y1b, fe = geom.BAND
        box = (0, y0b, W, y1b)
        kb, kf = geom.hubble_k(t)
        ox, oy, sb = geom.hubble_origin(kb)
        bg, _ = warp(self.hub['bg'], sb, ox, oy, box)
        ox, oy, sf = geom.hubble_origin(kf)
        fg, _ = warp(self.hub['fg'], sf, ox, oy, box)
        fa, _ = warp(self.hub['fga'], sf, ox, oy, box, sharpen=False)
        hal, _ = warp(self.hub['hal'], sf, ox, oy, box, sharpen=False)
        rgb = bg * (1 - fa[..., None]) + fg + hal
        E = ease('DEVELOP', t, 644, 677)
        if E < 1:
            rgb = develop(rgb, E, self.noise(f, box), 'in', hal)
        ys = np.arange(y0b, y1b, dtype=np.float32) + 0.5
        m = np.clip((ys - y0b) / fe, 0, 1) * np.clip((y1b - ys) / fe, 0, 1)
        img[y0b:y1b] = INK + (np.clip(rgb, 0, 1) - INK) * m[:, None, None]
        return img

    def s05(self, t, f):
        img = np.empty((H, W, 3), np.float32)
        img[:] = INK
        size, cx, cy = geom.retina_state(t)
        s = size / geom.RETINA_SRC
        ox, oy = cx - size / 2, cy - size / 2
        box = screen_box(s, ox, oy, geom.RETINA_SRC, geom.RETINA_SRC)
        E = geom.retina_light(t)
        if E < 1:
            rgb, cov = warp(self.retina_rgb, s, ox, oy, box)
            x0, y0, x1, y1 = box
            dcx, dcy, R = ox + geom.RETINA_DISC[0] * s, oy + geom.RETINA_DISC[1] * s, geom.RETINA_DISC[2] * s
            nx, ny = (XX[y0:y1, x0:x1] - dcx) / R, (YY[y0:y1, x0:x1] - dcy) / R
            r2 = nx * nx + ny * ny
            out = r2 > 1
            rr = np.sqrt(np.maximum(r2, 1e-6))
            nx, ny = np.where(out, nx / rr, nx), np.where(out, ny / rr, ny)
            nz = np.sqrt(np.clip(1 - nx * nx - ny * ny, 0, 1))
            # l0 sits behind the disc so f860 opens on a crescent that just holds the optic disc
            l = np.array([-0.80, -0.20, -0.475]) * (1 - E) + np.array([-0.30, -0.20, 0.93]) * E
            l = l / np.linalg.norm(l)
            I = smoothstep(-0.10, 0.30, nx * l[0] + ny * l[1] + nz * l[2] + 0.8 * E)
            rgb = to_srgb(INK_LIN + (to_lin(rgb) - INK_LIN) * I[..., None])
            rgb = np.clip(rgb + halation(rgb, 0.70, 10.0 * size / 748.0, 0.28), 0, 1)
        else:
            rgb, cov = warp(self.retina_full, s, ox, oy, box)
        self.paste(img, box, rgb, cov)
        if 962 <= t < 1108:
            fx0, fy0, fx1, fy1 = geom.RETINA_FRAME
            hairline(img, (fx0, fy0, fx1 - fx0, fy1 - fy0), 0.30 * (1 - ease('LEAVE', t, 1096, 1108)),
                     progress=ease('DRAW', t, 962, 978))
        return img

    def sheet_cells(self, img, t, f, s, tx, ty, fade_out=0.0):
        for cid, name, sw, sh, cs, x, y, start in geom.CELLS:
            if start is not None and t < start:
                continue
            sc = cs * s
            ox, oy = tx + s * x, ty + s * y
            box = screen_box(sc, ox, oy, sw, sh)
            if box[2] - box[0] < 1 or box[3] - box[1] < 1:
                continue
            rgb, cov = warp(self.cells[name], sc, ox, oy, box)
            if start is not None:
                E = ease('DEVELOP', t, start, start + 15)
                if E < 1:
                    rgb = develop(rgb, E, self.noise(f, box), 'in')
            if fade_out > 0:                             # exposure fade in linear light while flying out
                rgb = to_srgb(INK_LIN + (to_lin(rgb) - INK_LIN) * (1 - fade_out))
            self.paste(img, box, rgb, cov)

    def s06(self, t, f):
        img = np.empty((H, W, 3), np.float32)
        img[:] = INK
        s, tx, ty = geom.sheet_tf(t)
        self.sheet_cells(img, t, f, s, tx, ty)
        if t >= 1187:
            x, y, w, h = geom.CELL12
            hairline(img, (tx + s * x, ty + s * y, s * w, s * h), 0.30, progress=ease('DRAW', t, 1187, 1199))
        return img

    def s07(self, t, f):
        img = np.empty((H, W, 3), np.float32)
        img[:] = INK
        s, tx, ty = geom.sheet_tf(t)
        if t < 1416:                                     # the other cells fly out and their exposure falls away
            self.sheet_cells(img, t, f, s, tx, ty, fade_out=ease('LAMP', t, 1390, 1416))
        u = geom.plunge_u(t)
        x, y, w, h = geom.CELL12
        hairline(img, (tx + s * x, ty + s * y, s * w, s * h), lerp(0.30, 0.18, u), radius=6.0 * u)
        return img

    def paper_at(self, t):
        if t >= 1652 and self._paper_rest is not None:
            return self._paper_rest
        az, el = geom.rake(t)
        from prep import plate_shade
        pap = np.minimum(self.paper_alb * plate_shade(self.paper_n, az, el)[..., None], 0.985).astype(np.float32)
        k, ox, oy = geom.paper_tf(t)
        if abs(k - 1) > 1e-6 or abs(ox) > 1e-6 or abs(oy) > 1e-6:
            pap, _ = warp(pap, k, ox, oy, (0, 0, W, H), sharpen=False)
        if t >= 1652:
            self._paper_rest = pap
        return pap

    def s08(self, t, f):
        pap = self.paper_at(t)
        E = geom.lamp(t)
        if E < 1:
            img = to_srgb(INK_LIN + (to_lin(pap) - INK_LIN) * E)
        else:
            img = pap.copy()
        a = 0.18 * (1 - ease('LEAVE', t, 1604, 1616))
        if a > 0:
            hairline(img, geom.plate_rect(t), a, radius=6.0)
        return img

    # ------------------------------------------------------------ frame
    def at(self, t, f):
        shot = geom.shot_of(f)[0]
        return getattr(self, f's0{shot}')(t, f)

    def motion(self, f):
        """Largest on-screen displacement (px) over one frame, for the moves that get motion blur."""
        a, b = f - 0.5, f + 0.5

        def tf_disp(tf):
            s0, x0, y0 = tf(a)
            s1, x1, y1 = tf(b)
            pts = [(0, 0), (W, 0), (0, H), (W, H), (W / 2, H / 2)]
            best = 0.0
            for px, py in pts:                       # screen point at a -> layout point -> screen point at b
                qx, qy = (px - x0) / s0, (py - y0) / s0
                best = max(best, math.hypot(s1 * qx + x1 - px, s1 * qy + y1 - py))
            return best

        if 260 <= f <= 288:
            return abs(geom.slit_width(b) - geom.slit_width(a)) / 2
        if 484 <= f <= 621:
            k0 = geom.router_lights(a, self.coins)[0]
            k1 = geom.router_lights(b, self.coins)[0]
            return math.hypot(k1[0] - k0[0], k1[1] - k0[1]) * 2.0
        if 932 <= f <= 962:
            s0, c0x, c0y = geom.retina_state(a)
            s1, c1x, c1y = geom.retina_state(b)
            return max(math.hypot(c1x + sx * s1 / 2 - c0x - sx * s0 / 2, c1y + sy * s1 / 2 - c0y - sy * s0 / 2)
                       for sx in (-1, 1) for sy in (-1, 1))
        if 1124 <= f <= 1172 or 1388 <= f <= 1428:
            return tf_disp(geom.sheet_tf)
        if 1604 <= f <= 1652:
            return tf_disp(geom.paper_tf)
        return 0.0

    def frame(self, f):
        shot, a, b = geom.shot_of(f)
        v = self.motion(f)
        if v > 8.0:
            # 180 degree shutter in linear light; at least 5 samples (§6.4), more on fast moves so the
            # sub-frame copies stay <= 2.5 px apart and read as one continuous smear, never as ghosts
            n = int(min(41, max(5, math.ceil(0.5 * v / 2.5) + 1)))
            acc = None
            for i in range(n):
                t = min(max(f - 0.25 + 0.5 * i / (n - 1), a), b - 1e-3)
                lin = to_lin(np.clip(self.at(t, f), 0, 1))
                acc = lin if acc is None else acc + lin
            return to_srgb(acc / n)
        return np.clip(self.at(float(f), f), 0, 1)


def main():
    import time
    a = sys.argv[1:]
    frames = [int(x) for x in a[a.index('--frames') + 1].split(',')]
    out = a[a.index('--out') + 1]
    with_type = '--type' in a
    P = Picture()
    if with_type:
        import json
        from PIL import Image
        from common import BUILD
        data = json.load(open(os.path.join(BUILD, 'type_film.json')))
    for f in frames:
        t0 = time.time()
        img = P.frame(f)
        if with_type:
            key = data['states'][data['frames'][f]]['key']
            p = os.path.join(BUILD, 'type', key + '.png')
            if os.path.exists(p):
                tp = np.asarray(Image.open(p).convert('RGBA')).astype(np.float32) / 255.0
                al = tp[..., 3:4]
                img = tp[..., :3] * al + img * (1 - al)
        save_png(os.path.join(out, f'f{f:04d}.png'), img)
        print(f'frame {f}: {time.time() - t0:.2f} s, motion {P.motion(f):.1f}px')


if __name__ == '__main__':
    main()
