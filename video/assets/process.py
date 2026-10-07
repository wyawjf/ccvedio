"""Turn the raw public-domain / CC0 images into comic-print panels (ink-violet-paper duotone,
halftone dots, ink linework) and export the real ECG trace + life-expectancy series as JSON."""
import json, sys
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFilter
from scipy.signal import find_peaks
from skimage import feature, color as skcolor

RAW, OUT = sys.argv[1], sys.argv[2]
INK, VIO, PAPER = np.array([21, 18, 27]), np.array([91, 46, 255]), np.array([244, 240, 232])


def fit(im, w, h, focus=(0.5, 0.5)):
    sw, sh = im.size
    s = max(w / sw, h / sh)
    im = im.resize((int(sw * s + 0.5), int(sh * s + 0.5)), Image.LANCZOS)
    x = int((im.width - w) * focus[0]); y = int((im.height - h) * focus[1])
    return im.crop((x, y, x + w, y + h))


def comic(name, w, h, focus=(0.5, 0.5), mid=0.48, dots=0.32, lines=0.45, invert=False, cell=9):
    im = Image.open(f"{RAW}/{name}").convert("RGB")
    im = fit(im, w, h, focus)
    g = ImageOps.autocontrast(im.convert("L"), cutoff=1)
    if invert:
        g = ImageOps.invert(g)
    L = np.asarray(g).astype(np.float32) / 255.0
    # duotone ramp: ink -> violet -> paper
    a = np.clip(L / mid, 0, 1)[..., None]
    b = np.clip((L - mid) / (1 - mid), 0, 1)[..., None]
    rgb = np.where(L[..., None] < mid, INK * (1 - a) + VIO * a, VIO * (1 - b) + PAPER * b)
    out = Image.fromarray(rgb.astype(np.uint8))
    # halftone screen at 45 degrees in the darker half
    ht = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(ht)
    ang = np.pi / 4
    ca, sa = np.cos(ang), np.sin(ang)
    R = int(np.hypot(w, h))
    for i in range(-R // cell, R // cell + 1):
        for j in range(-R // cell, R // cell + 1):
            u, v = i * cell, j * cell
            x, y = w / 2 + u * ca - v * sa, h / 2 + u * sa + v * ca
            if 0 <= x < w and 0 <= y < h:
                dark = 1 - L[int(y), int(x)]
                r = cell * 0.52 * np.sqrt(max(0, dark - 0.25) / 0.75)
                if r > 0.4:
                    d.ellipse([x - r, y - r, x + r, y + r], fill=255)
    ht = np.asarray(ht).astype(np.float32)[..., None] / 255 * dots
    # ink linework from edges
    edges = feature.canny(np.asarray(g).astype(np.float32) / 255, sigma=2.2).astype(np.float32)
    edges = np.asarray(Image.fromarray((edges * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3))).astype(np.float32)[..., None] / 255 * lines
    o = np.asarray(out).astype(np.float32)
    o = o * (1 - ht) + INK * ht
    o = o * (1 - edges) + INK * edges
    Image.fromarray(o.clip(0, 255).astype(np.uint8)).save(f"{OUT}/{name.split('.')[0]}.png")
    print("panel", name, w, h)


comic("retina.png", 760, 760, mid=0.42, dots=0.3, lines=0.35)
comic("rocket.png", 760, 980, focus=(0.42, 0.5), mid=0.5, dots=0.3, lines=0.4)
comic("astronaut.png", 640, 760, focus=(0.5, 0.2), mid=0.5, dots=0.28, lines=0.4)
comic("grace_hopper.jpg", 560, 680, focus=(0.5, 0.25), mid=0.5, dots=0.3, lines=0.45)
comic("human_mitosis.png", 640, 640, mid=0.38, dots=0.25, lines=0.25)
comic("hubble_deep_field.png", 1080, 1920, mid=0.5, dots=0.18, lines=0.0, cell=8)

# real ECG (MIT-BIH record 208 via scipy.datasets): pick the most regular 5-second window
ecg = np.load(f"{RAW}/ecg.npy"); fs = 360
peaks, _ = find_peaks(ecg, distance=fs * 0.4, prominence=1.0)
best, bi = 1e9, 0
for k in range(len(peaks) - 8):
    rr = np.diff(peaks[k:k + 8])
    if peaks[k + 7] - peaks[k] < 5.5 * fs and rr.std() < best:
        best, bi = rr.std(), k
s0 = peaks[bi] - int(0.3 * fs)
seg = ecg[s0:s0 + 5 * fs]
seg = (seg - np.median(seg)) / (np.abs(seg - np.median(seg)).max())
json.dump({"fs": fs, "start_sample": int(s0), "values": [round(float(v), 4) for v in seg[::2]]}, open(f"{OUT}/ecg.json", "w"))
print("ecg window", s0, "rr std", best)

# global life expectancy at birth (Our World in Data, rounded)
life = [[1900, 32], [1913, 34.1], [1925, 37], [1938, 41], [1950, 46.5], [1960, 50.6], [1970, 56.9], [1980, 61.1],
        [1990, 64.1], [2000, 66.5], [2010, 70.1], [2019, 72.8], [2021, 71.0], [2023, 73.2]]
json.dump(life, open(f"{OUT}/life.json", "w"))
