"""Camera and layout geometry of every shot (§3.3), shared by the picture renderer and the type timeline.
All times are in frames (float allowed); all coordinates are screen px at 1080x1920."""
import math

from common import ease, lerp, span

# ---------------------------------------------------------------- S01 hook (f0-f115)
HOOK_ANCHOR = (678.0, 1000.0)
COIN16_SRC = (212.4, 193.1)
COIN16_R = 23.5


def hook_scale(t):
    if t <= 15:
        return lerp(2.43, 2.42, ease('FADE', t, 0, 15))
    if t <= 44:
        return lerp(2.42, 2.40, ease('ACCEL', t, 15, 44))
    return lerp(2.40, 2.46, span(t, 44, 115))


def hook_focus_radius(t):
    """A first breath with the whirr (f0-f15), then focus accelerates into the clack and lands on f44."""
    if t <= 15:
        return 16.0 - 5.0 * ease('FADE', t, 0, 15)
    return 11.0 * (1 - ease('ACCEL', t, 15, 44))


def hook_origin(s):
    return HOOK_ANCHOR[0] - COIN16_SRC[0] * s, HOOK_ANCHOR[1] - COIN16_SRC[1] * s


# ---------------------------------------------------------------- S02 espresso -> slit (f116-f379)
CREMA = (678.0, 1000.0)                    # crema centre (288,140) of the 600x400 print at (390,860)


def coffee_scale(t):
    return lerp(1.0, 1.02, span(t, 116, 259))


def coffee_origin(s):
    """The drift scales about the right-hung edge (990, 1000): the print stays flush with the slit edge,
    and at s = 1 the crema is still on the coin's centre for the match cut (review CD-12)."""
    return 990.0 + (390 - 990.0) * s, 1000.0 + (860 - 1000.0) * s


SLIT_Y0, SLIT_Y1, SLIT_CX, SLIT_W = 693, 1427, 848.0, 284.0
NOSE = (848.0, 827.0)
ROCKET_CROP = (250, 60, 392, 427)


def slit_width(t):
    return SLIT_W * ease('SNAP', t, 260, 287)


def slit_rows(t):
    """Two beats (review CD-10): the slit first opens only inside the espresso print, then outgrows it."""
    a0, a1 = 1000.0 + (860 - 1000.0) * 1.02, 1000.0 + (1260 - 1000.0) * 1.02     # the print's rows at x1.02
    u = ease('SNAP', t, 300, 318)
    return lerp(a0, float(SLIT_Y0), u), lerp(a1, float(SLIT_Y1), u)


def slit_push(t):
    return lerp(1.0, 1.03, span(t, 260, 379))


def rocket_origin(p):
    """Top-left of the FULL rocket image on screen at push p (crop (250,60) sits at (706,693) at p=1)."""
    s = 2.0 * p
    cx = NOSE[0] + (706 - NOSE[0]) * p
    cy = NOSE[1] + (693 - NOSE[1]) * p
    return cx - ROCKET_CROP[0] * s, cy - ROCKET_CROP[1] * s, s


# ---------------------------------------------------------------- S03 tray + router (f380-f643)
TRAY_ORIGIN = (182.0, 700.0)                             # tray ends at x 950: clear of the feed's icons
TRAY_CENTER = (566.0, 1003.0)
ROUTER = [6, 23, 19, 4, 14, 9, 24, 17, 11, 21, 18, 16]    # hop 1..12 coin ids
# an accelerando on the 75 BPM grid that resolves home (review CD-07): 24,18,12,12,6,6,6,6,12,12,18 frames
LANDS = [488, 512, 530, 542, 554, 560, 566, 572, 578, 590, 602, 620]


def tray_drift(t):
    return lerp(1.0, 1.01, span(t, 380, 643))


def tray_tf(d, base=2.0, origin=TRAY_ORIGIN, center=TRAY_CENTER):
    """Returns (scale, ox, oy) of the coins plate."""
    s = base * d
    ox = center[0] + (origin[0] - center[0]) * d
    oy = center[1] + (origin[1] - center[1]) * d
    return s, ox, oy


def router_lights(t, coins):
    """Key light + afterglows [(cx_src, cy_src, r_src, k)] in SOURCE px of coins.png (the renderer maps them
    through the plate transform, so lights stay attached to their coins)."""
    C = {c['id']: c for c in coins}
    seq = [16] + ROUTER
    lands = [380] + LANDS
    travel = [0] + [min(4.0, (lands[i] - lands[i - 1]) / 3) for i in range(1, len(lands))]
    lights = []
    key = None
    for i in range(1, len(seq)):
        a, b = lands[i] - travel[i], lands[i]
        if t < a:
            break
        if t < b:                                      # mid-flight the beam narrows and dims (review MO-05)
            u = ease('HOP', t, a, b)
            g = min(1.0, max(0.0, (b - a - 2) / 2.0))
            sw = math.sin(math.pi * u) * g
            p, q = C[seq[i - 1]], C[seq[i]]
            key = (lerp(p['cx'], q['cx'], u), lerp(p['cy'], q['cy'], u), lerp(p['r'], q['r'], u) * (1 - 0.35 * sw),
                   1.0 - 0.6 * sw)
            break
    if key is None:
        idx = max(i for i in range(len(seq)) if t >= lands[i] or i == 0)
        c = C[seq[idx]]
        key = (c['cx'], c['cy'], c['r'], 1.0)
    lights.append(key)
    for i in range(1, len(seq)):                       # afterglow: 0.45 -> 0.10 over 10 f from leaving
        leave = lands[i] - travel[i]
        if leave <= t < leave + 10:
            c = C[seq[i - 1]]
            lights.append((c['cx'], c['cy'], c['r'], lerp(0.45, 0.10, (t - leave) / 10.0)))
    return lights


# ---------------------------------------------------------------- S04 Hubble (f644-f859)
HUBBLE_BASE = 1.08
HUBBLE_ORIGIN = (0.0, 544.0)
HUBBLE_ANCHOR_SRC = (727.0, 473.0)
HUBBLE_ANCHOR = (727 * 1.08, 544 + 473 * 1.08)           # (785.16, 1054.84)
BAND = (760, 1330, 72)
STOP = 764


def hubble_k(t):
    """The push builds to ~5 px/f at the frame edge so the hard stop reads as the camera dying.
    Max magnification 1.08 * 1.11 = 1.199 (limit 1.20)."""
    u = ease('ACCEL2', min(t, STOP), 644, STOP)
    return lerp(1.0, 1.075, u), lerp(1.0, 1.11, u)         # BG, FG


def hubble_tilt(t):
    """An accelerating tilt on the same curve as the push (FG 50 % faster than BG), so the whole band is
    visibly travelling (~8 px/f) when the camera dies at f764 (review MO-01)."""
    u = ease('ACCEL2', min(t, STOP), 644, STOP)
    return -140.0 * u, -93.0 * u                           # FG, BG


def hubble_origin(k, dy=0.0):
    s = HUBBLE_BASE * k
    return HUBBLE_ANCHOR[0] - HUBBLE_ANCHOR_SRC[0] * s, HUBBLE_ANCHOR[1] - HUBBLE_ANCHOR_SRC[1] * s + dy, s


# ---------------------------------------------------------------- S05 retina (f860-f1123)
RETINA_SRC = 1411
RETINA_DISC = (704.0, 703.0, 695.0)                     # disc centre and radius in source px
RETINA_FRAME = (454, 700, 940, 1186)                      # clear of the feed's like/collect icons


def retina_state(t):
    """(display size, centre x, centre y) of the 1411 px retina image."""
    rise_dy = 36 * (1 - ease('SETTLE', t, 860, 920))
    if t < 920:
        return 748.0, 540.0, 1010.0 + rise_dy
    u = ease('TRAVEL', t, 920, 950)                        # 12 f earlier than §3.3 (review MO-02)
    size = math.exp(lerp(math.log(748.0), math.log(438.0), u))
    return size, lerp(540.0, 697.0, u), lerp(1010.0, 943.0, u)


def retina_light(t):
    return ease('RISE', t, 860, 920)


# ---------------------------------------------------------------- S06/S07 sheet (f1124-f1603)
SHEET_XS = (90, 390, 690)            # third column ends at 945: clear of the feed's action column
SHEET_ROWS = (508, 744, 980, 1216)
S0 = 438.0 / 170.0
S1 = 1160.0 / 255.0                       # plate 12 grows wider than the screen: a band (R2-CD-01)
CELLS = [  # id, cache name, source w, h, scale, sheet x, y, develop start
    (1, 'coins_full', 384, 303, 170 / 303, 90, 508, 1156),
    (2, 'coffee_rgb', 600, 400, 170 / 400, 390, 508, 1140),
    (3, 'rocket_rgb', 640, 427, 170 / 427, 690, 508, 1156),
    (4, 'hubble_full', 1000, 872, 170 / 872, 90, 744, 1146),
    (5, 'retina_full', 1411, 1411, 170 / 1411, 390, 744, None),
    (6, 'camera', 512, 512, 170 / 512, 690, 744, 1146),
    (7, 'astronaut', 512, 512, 170 / 512, 90, 980, 1156),
    (8, 'grace_hopper', 512, 600, 170 / 600, 390, 980, 1140),
    (9, 'moon', 512, 512, 170 / 512, 690, 980, 1156),
    (10, 'text', 258, 172, 170 / 172, 90, 1216, 1179),
    (11, 'clock', 400, 300, 170 / 300, 390, 1216, 1171),
]
CELL12 = (690.0, 1216.0, 255.0, 170.0)
CELL12_C = (690.0 + 127.5, 1216.0 + 85.0)
PLATE12 = (-40.0, 545.3, 1160.0, 773.3)


def sheet_tf(t):
    """screen = s * p + (tx, ty) for sheet-space p."""
    if t < 1172:
        u = ease('REVEAL', t, 1124, 1172)
        s = S0 ** (1 - u)
        w = (S0 - s) / (S0 - 1)
        px, py = lerp(478.0, 390.0, w), lerp(724.0, 744.0, w)
        return s, px - s * 390, py - s * 744
    if t < 1388:                                       # a 2 % lean toward the empty cell (review MO-06)
        d = 1 + 0.02 * span(t, 1172, 1388)
        return d, CELL12_C[0] * (1 - d), CELL12_C[1] * (1 - d)
    s0 = 1.02
    u = ease('DIVE', t, 1388, 1428)
    s = s0 * (S1 / s0) ** u
    p0x, p0y = s0 * 690 + CELL12_C[0] * (1 - s0), s0 * 1216 + CELL12_C[1] * (1 - s0)
    w = (s - s0) / (S1 - s0)
    px, py = lerp(p0x, -40.0, w), lerp(p0y, 545.3, w)
    return s, px - s * 690, py - s * 1216


def plunge_u(t):
    return ease('DIVE', t, 1388, 1428)


# ---------------------------------------------------------------- S08 lamp-up + pull-out (f1604-f1771)
PAPER_REST = (90.0, 540.0, 642.0, 428.0)


def plate_rect(t):
    """Screen rect (x, y, w, h) of the plate during the pull-out."""
    u = ease('SETTLEL', t, 1580, 1628)
    r = 642.0 / 1160.0
    s = r ** u
    k = (1 - s) / (1 - r)
    x, y = lerp(-40.0, 90.0, k), lerp(545.3, 540.0, k)
    return x, y, 1160.0 * s, 773.3 * s


def paper_tf(t):
    """screen = k * (p - (90,540)) + (x, y): paper space is the rest layout."""
    x, y, w, _ = plate_rect(t)
    k = w / 642.0
    return k, x - k * 90.0, y - k * 540.0


def rake(t):
    """The light lowers until the relief peaks on f1604 (the withheld D5), then settles to rest (review MO-03)."""
    if t < 1604:
        u = ease('RAKE', t, 1580, 1604)
        return lerp(215.0, 155.0, u), lerp(38.0, 10.0, u)
    u = ease('SETTLEL', t, 1604, 1628)
    return lerp(155.0, 135.0, u), lerp(10.0, 24.0, u)


def lamp(t):
    """A light table is a switch, not a fade (review CD-08): dark on f1604, on from f1605."""
    return 0.0 if t < 1580.5 else 1.0


# ---------------------------------------------------------------- shots
SHOTS = [(0, 116), (116, 380), (380, 644), (644, 860), (860, 1124), (1124, 1388), (1388, 1580), (1580, 1796)]


def shot_of(f):
    for i, (a, b) in enumerate(SHOTS):
        if a <= f < b:
            return i + 1, a, b
    return 8, 1580, 1796
