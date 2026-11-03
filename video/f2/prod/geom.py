"""Camera and layout geometry of every shot (§3.3), shared by the picture renderer and the type timeline.
All times are in frames (float allowed); all coordinates are screen px at 1080x1920."""
import math

from common import ease, lerp, span

# ---------------------------------------------------------------- S01 hook (f0-f115)
HOOK_ANCHOR = (678.0, 1000.0)
COIN16_SRC = (212.4, 193.1)
COIN16_R = 23.5


def hook_scale(t):
    if t <= 44:
        return lerp(2.43, 2.40, ease('FOCUS', t, 0, 44))
    return lerp(2.40, 2.46, span(t, 44, 115))


def hook_focus_radius(t):
    return 16.0 * (1 - ease('FOCUS', t, 0, 44))


def hook_origin(s):
    return HOOK_ANCHOR[0] - COIN16_SRC[0] * s, HOOK_ANCHOR[1] - COIN16_SRC[1] * s


# ---------------------------------------------------------------- S02 espresso -> slit (f116-f379)
CREMA = (678.0, 1000.0)                    # crema centre (288,140) of the 600x400 print at (390,860)


def coffee_scale(t):
    return lerp(1.0, 1.02, span(t, 116, 259))


def coffee_origin(s):
    return CREMA[0] + (390 - CREMA[0]) * s, CREMA[1] + (860 - CREMA[1]) * s


SLIT_Y0, SLIT_Y1, SLIT_CX, SLIT_W = 693, 1427, 848.0, 284.0
NOSE = (848.0, 827.0)
ROCKET_CROP = (250, 60, 392, 427)


def slit_width(t):
    return SLIT_W * ease('SNAP', t, 260, 287)


def slit_push(t):
    return lerp(1.0, 1.03, span(t, 260, 379))


def rocket_origin(p):
    """Top-left of the FULL rocket image on screen at push p (crop (250,60) sits at (706,693) at p=1)."""
    s = 2.0 * p
    cx = NOSE[0] + (706 - NOSE[0]) * p
    cy = NOSE[1] + (693 - NOSE[1]) * p
    return cx - ROCKET_CROP[0] * s, cy - ROCKET_CROP[1] * s, s


# ---------------------------------------------------------------- S03 tray + router (f380-f643)
TRAY_ORIGIN = (222.0, 700.0)
TRAY_CENTER = (606.0, 1003.0)
ROUTER = [6, 23, 19, 4, 14, 9, 24, 17, 11, 21, 18, 16]    # hop 1..12 coin ids; hop k lands at f488+12(k-1)


def tray_drift(t):
    return lerp(1.0, 1.01, span(t, 380, 643))


def tray_tf(d, base=2.0, origin=TRAY_ORIGIN, center=TRAY_CENTER):
    """Returns (scale, ox, oy) of the coins plate."""
    s = base * d
    ox = center[0] + (origin[0] - center[0]) * d
    oy = center[1] + (origin[1] - center[1]) * d
    return s, ox, oy


def router_lights(t, coins):
    """Key light + afterglow list [(cx_src, cy_src, r_src, k)] in SOURCE px of coins.png (the renderer
    maps them through the plate transform, so lights stay attached to their coins)."""
    C = {c['id']: c for c in coins}
    seq = [16] + ROUTER
    lands = [380] + [488 + 12 * k for k in range(12)]
    lights = []
    # moving key light
    key = None
    for i in range(1, len(seq)):
        a, b = lands[i] - 4, lands[i]
        if t < a:
            break
        if t < b:
            u = ease('HOP', t, a, b)
            p, q = C[seq[i - 1]], C[seq[i]]
            key = (lerp(p['cx'], q['cx'], u), lerp(p['cy'], q['cy'], u), lerp(p['r'], q['r'], u), 1.0)
            break
        key = None
    if key is None:
        idx = 0
        for i in range(len(seq)):
            if t >= lands[i]:
                idx = i
        c = C[seq[idx]]
        key = (c['cx'], c['cy'], c['r'], 1.0)
    lights.append(key)
    # afterglow of every coin the light has left (0.45 -> 0.10 linear over 10 f from the moment it leaves)
    for i in range(1, len(seq)):
        leave = lands[i] - 4
        if leave <= t < leave + 10:
            c = C[seq[i - 1]]
            k = lerp(0.45, 0.10, (t - leave) / 10.0)
            lights.append((c['cx'], c['cy'], c['r'], k))
    return lights


# ---------------------------------------------------------------- S04 Hubble (f644-f859)
HUBBLE_BASE = 1.08
HUBBLE_ORIGIN = (0.0, 544.0)
HUBBLE_ANCHOR_SRC = (727.0, 473.0)
HUBBLE_ANCHOR = (727 * 1.08, 544 + 473 * 1.08)           # (785.16, 1054.84)
BAND = (760, 1330, 72)
STOP = 764


def hubble_k(t):
    u = ease('ACCEL', min(t, STOP), 644, STOP)
    return lerp(1.0, 1.06, u), lerp(1.0, 1.09, u)          # BG, FG


def hubble_origin(k):
    s = HUBBLE_BASE * k
    return HUBBLE_ANCHOR[0] - HUBBLE_ANCHOR_SRC[0] * s, HUBBLE_ANCHOR[1] - HUBBLE_ANCHOR_SRC[1] * s, s


# ---------------------------------------------------------------- S05 retina (f860-f1123)
RETINA_SRC = 1411
RETINA_DISC = (704.0, 703.0, 695.0)                     # disc centre and radius in source px
RETINA_FRAME = (504, 700, 990, 1186)


def retina_state(t):
    """(display size, centre x, centre y) of the 1411 px retina image."""
    rise_dy = 36 * (1 - ease('SETTLE', t, 860, 920))
    if t < 932:
        return 748.0, 540.0, 1010.0 + rise_dy
    u = ease('TRAVEL', t, 932, 962)
    size = math.exp(lerp(math.log(748.0), math.log(438.0), u))
    return size, lerp(540.0, 747.0, u), lerp(1010.0, 943.0, u)


def retina_light(t):
    return ease('RISE', t, 860, 920)


# ---------------------------------------------------------------- S06/S07 sheet (f1124-f1603)
SHEET_XS = (90, 405, 720)
SHEET_ROWS = (508, 744, 980, 1216)
S0 = 438.0 / 170.0
S1 = 996.0 / 255.0
CELLS = [  # id, cache name, source w, h, scale, sheet x, y, develop start
    (1, 'coins_full', 384, 303, 170 / 303, 90, 508, 1154),
    (2, 'coffee_rgb', 600, 400, 170 / 400, 405, 508, 1157),
    (3, 'rocket_rgb', 640, 427, 170 / 427, 720, 508, 1160),
    (4, 'hubble_full', 1000, 872, 170 / 872, 90, 744, 1163),
    (5, 'retina_full', 1411, 1411, 170 / 1411, 405, 744, None),
    (6, 'camera', 512, 512, 170 / 512, 720, 744, 1169),
    (7, 'astronaut', 512, 512, 170 / 512, 90, 980, 1172),
    (8, 'grace_hopper', 512, 600, 170 / 600, 405, 980, 1175),
    (9, 'moon', 512, 512, 170 / 512, 720, 980, 1178),
    (10, 'text', 273, 172, 170 / 172, 90, 1216, 1181),
    (11, 'clock', 400, 300, 170 / 300, 405, 1216, 1184),
]
CELL12 = (720.0, 1216.0, 255.0, 170.0)
PLATE12 = (42.0, 600.0, 996.0, 664.0)


def sheet_tf(t):
    """screen = s * p + (tx, ty) for sheet-space p."""
    if t < 1172:
        u = ease('REVEAL', t, 1124, 1172)
        s = S0 ** (1 - u)
        w = (S0 - s) / (S0 - 1)
        px, py = lerp(528.0, 405.0, w), lerp(724.0, 744.0, w)
        return s, px - s * 405, py - s * 744
    if t < 1388:
        return 1.0, 0.0, 0.0
    u = ease('DIVE', t, 1388, 1428)
    s = S1 ** u
    w = (s - 1) / (S1 - 1)
    px, py = lerp(720.0, 42.0, w), lerp(1216.0, 600.0, w)
    return s, px - s * 720, py - s * 1216


def plunge_u(t):
    return ease('DIVE', t, 1388, 1428)


# ---------------------------------------------------------------- S08 lamp-up + pull-out (f1604-f1771)
PAPER_REST = (90.0, 540.0, 642.0, 428.0)


def plate_rect(t):
    """Screen rect (x, y, w, h) of the plate during the pull-out."""
    u = ease('SETTLEL', t, 1604, 1652)
    r = 642.0 / 996.0
    s = r ** u
    k = (1 - s) / (1 - r)
    x, y = lerp(42.0, 90.0, k), lerp(600.0, 540.0, k)
    return x, y, 996.0 * s, 664.0 * s


def paper_tf(t):
    """screen = k * (p - (90,540)) + (x, y): paper space is the rest layout."""
    x, y, w, _ = plate_rect(t)
    k = w / 642.0
    return k, x - k * 90.0, y - k * 540.0


def rake(t):
    u = ease('RAKE', t, 1604, 1652)
    return lerp(215.0, 135.0, u), lerp(8.0, 24.0, u)


def lamp(t):
    return ease('LAMP', t, 1604, 1628)


# ---------------------------------------------------------------- shots
SHOTS = [(0, 116), (116, 380), (380, 644), (644, 860), (860, 1124), (1124, 1388), (1388, 1604), (1604, 1772)]


def shot_of(f):
    for i, (a, b) in enumerate(SHOTS):
        if a <= f < b:
            return i + 1, a, b
    return 8, 1604, 1772
