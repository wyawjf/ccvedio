"""Photochemical finishing pass for rendered frames: halation, bloom, grain, chromatic aberration,
vignette, gate weave and flicker. Every parameter can be keyframed over time.

usage:
  python3 f2/film.py <in.mp4> <out.mp4> [--look f2/look.json] [--from S] [--to S]
  python3 f2/film.py --still <in.png> <out.png> --t 12.3 [--look ...]

look.json: {"default": {...params...}, "keys": [{"t": 0, ...overrides...}, {"t": 4.2, ...}]}
Overrides are linearly interpolated between keys; params missing from a key fall back to default.
"""
import json, subprocess, sys
import numpy as np
import cv2

W, H, FPS = 1080, 1920, 30
DEFAULT = dict(
    grain=0.045,        # std of luminance grain (0..1 scale) at mid grey
    grain_size=1.15,    # >1 = coarser grain (noise generated at lower res and upsampled)
    grain_chroma=0.25,  # share of grain that is colored
    halation=0.22,      # strength of red-orange glow around highlights
    hal_thresh=0.72,    # luma above which halation starts
    hal_radius=26,      # px (sigma) of the halation blur
    bloom=0.10,         # neutral soft glow
    bloom_radius=60,
    ca=0.0012,          # radial chromatic aberration (relative scale offset of R/B)
    vignette=0.28,      # darkening at the corners (0..1)
    vig_round=1.0,      # 1 = circular, <1 = follows the frame aspect
    weave=0.35,         # gate weave amplitude in px
    flicker=0.006,      # exposure flicker amplitude
    lift=0.0, gain=1.0, # final black lift / gain
)


def load_look(path):
    if not path:
        return {"default": {}, "keys": []}
    return json.load(open(path))


def params_at(look, t):
    p = dict(DEFAULT)
    p.update(look.get("default", {}))
    keys = sorted(look.get("keys", []), key=lambda k: k["t"])
    if not keys:
        return p
    if t <= keys[0]["t"]:
        p.update({k: v for k, v in keys[0].items() if k != "t"}); return p
    if t >= keys[-1]["t"]:
        p.update({k: v for k, v in keys[-1].items() if k != "t"}); return p
    for a, b in zip(keys, keys[1:]):
        if a["t"] <= t <= b["t"]:
            u = (t - a["t"]) / max(1e-6, b["t"] - a["t"])
            for k in set(a) | set(b):
                if k == "t":
                    continue
                va = a.get(k, p[k]); vb = b.get(k, p[k])
                p[k] = va + (vb - va) * u
            return p
    return p


class Film:
    def __init__(self, w=W, h=H, seed=7):
        self.w, self.h = w, h
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        cx, cy = (w - 1) / 2, (h - 1) / 2
        self.rx = (xx - cx) / (w / 2)
        self.ry = (yy - cy) / (h / 2)
        self.rng = np.random.default_rng(seed)
        self.luma_w = np.array([0.2126, 0.7152, 0.0722], np.float32)
        self._vig = {}
        self._bank = {}
        # tone shoulder as a lookup over 0..2 (1/1024 steps): highlights roll off instead of clipping
        x = np.linspace(0, 2, 2049, dtype=np.float32)
        self.shoulder = np.where(x > 0.85, 0.85 + (1 - np.exp(-(x - 0.85) * 4)) * 0.15, x).astype(np.float32)

    def vignette(self, p):
        key = (round(p["vignette"], 3), round(p["vig_round"], 2))
        if key not in self._vig:
            ry = self.ry * (self.h / self.w) ** (1 - p["vig_round"])
            r2 = self.rx ** 2 + ry ** 2
            v = 1 - p["vignette"] * np.clip(r2 / 2.0, 0, 1) ** 1.35
            self._vig = {key: v[..., None].astype(np.float32)}
        return self._vig[key]

    def ca(self, img, k):
        if k <= 0:
            return img
        h, w = img.shape[:2]
        out = img.copy()
        for ch, s in ((0, 1 + k), (2, 1 - k)):  # RGB order: R scaled out, B scaled in
            M = np.float32([[s, 0, (1 - s) * (w - 1) / 2], [0, s, (1 - s) * (h - 1) / 2]])
            out[..., ch] = cv2.warpAffine(img[..., ch], M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        return out

    def grain_bank(self, size, chroma):
        key = (round(size, 2), round(chroma, 2))
        if key not in self._bank:
            s = max(1.0, size)
            gw, gh = int(self.w / s), int(self.h / s)
            bank = []
            for _ in range(24):
                n = self.rng.standard_normal((gh, gw, 3)).astype(np.float32)
                n = cv2.GaussianBlur(n, (0, 0), 0.55)
                if (gw, gh) != (self.w, self.h):
                    n = cv2.resize(n, (self.w, self.h), interpolation=cv2.INTER_CUBIC)
                n = n[..., :1] * (1 - chroma) + n * chroma
                bank.append(n.astype(np.float32))
            self._bank = {key: bank}
        return self._bank[key]

    def grain(self, p, luma):
        bank = self.grain_bank(p["grain_size"], p["grain_chroma"])
        n = bank[int(self.rng.integers(len(bank)))]
        dy, dx = int(self.rng.integers(self.h)), int(self.rng.integers(self.w))
        n = np.roll(n, (dy, dx), axis=(0, 1))
        if self.rng.random() < 0.5:
            n = n[:, ::-1]
        # film grain is strongest in the mid-tones and quiet in deep shadow / clipped highlight
        resp = (4 * luma * (1 - luma)) ** 0.7 * 0.85 + 0.15
        return n * (p["grain"] * resp[..., None])

    def __call__(self, frame_u8, t):
        p = params_at(self.look, t) if hasattr(self, "look") else dict(DEFAULT)
        img = frame_u8.astype(np.float32) / 255.0
        # gate weave: tiny smooth sub-pixel drift
        if p["weave"] > 0:
            dx = p["weave"] * (np.sin(t * 2.1) * 0.6 + np.sin(t * 5.3 + 1.7) * 0.4)
            dy = p["weave"] * 0.8 * (np.sin(t * 1.7 + 0.4) * 0.6 + np.sin(t * 4.1 + 2.2) * 0.4)
            M = np.float32([[1, 0, dx], [0, 1, dy]])
            img = cv2.warpAffine(img, M, (self.w, self.h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        luma = img @ self.luma_w
        # halation: highlights bleed a warm red-orange into the surroundings
        if p["halation"] > 0:
            hi = np.clip((luma - p["hal_thresh"]) / max(1e-3, 1 - p["hal_thresh"]), 0, 1)
            small = cv2.resize(hi, (self.w // 4, self.h // 4), interpolation=cv2.INTER_AREA)
            small = cv2.GaussianBlur(small, (0, 0), p["hal_radius"] / 4)
            glow = cv2.resize(small, (self.w, self.h), interpolation=cv2.INTER_LINEAR)
            tint = np.array([1.0, 0.36, 0.16], np.float32)
            img = img + glow[..., None] * tint * p["halation"]
        if p["bloom"] > 0:
            small = cv2.resize(img, (self.w // 6, self.h // 6), interpolation=cv2.INTER_AREA)
            small = np.clip(small - 0.55, 0, None)
            small = cv2.GaussianBlur(small, (0, 0), p["bloom_radius"] / 6)
            img = img + cv2.resize(small, (self.w, self.h), interpolation=cv2.INTER_LINEAR) * p["bloom"]
        img = self.ca(img, p["ca"])
        img = img * self.vignette(p)
        if p["flicker"] > 0:
            img = img * (1 + p["flicker"] * (np.sin(t * 23.0) * 0.5 + np.sin(t * 61.0 + 1.3) * 0.5))
        img = img * p["gain"] + p["lift"]
        # soft shoulder so halation never clips harshly
        idx = np.clip(img * 1024, 0, 2048).astype(np.uint16)
        img = self.shoulder[idx]
        luma2 = np.clip(img @ self.luma_w, 0, 1)
        img = img + self.grain(p, luma2)
        return (np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8)


def main():
    a = sys.argv[1:]
    opt = {}
    pos = []
    i = 0
    while i < len(a):
        if a[i].startswith("--"):
            key = a[i][2:]
            if key == "still":
                opt["still"] = True; i += 1; continue
            opt[key] = a[i + 1]; i += 2
        else:
            pos.append(a[i]); i += 1
    look = load_look(opt.get("look"))
    if opt.get("still"):
        src, dst = pos
        im = cv2.cvtColor(cv2.imread(src, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
        f = Film(im.shape[1], im.shape[0]); f.look = look
        out = f(im, float(opt.get("t", 0)))
        cv2.imwrite(dst, cv2.cvtColor(out, cv2.COLOR_RGB2BGR))
        return
    src, dst = pos
    t0 = float(opt.get("from", 0))
    probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                            "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip().split(",")
    w, h = int(probe[0]), int(probe[1])
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "13", "-pix_fmt", "yuv420p", dst],
                           stdin=subprocess.PIPE)
    f = Film(w, h); f.look = look
    n = 0
    size = w * h * 3
    while True:
        buf = dec.stdout.read(size)
        if len(buf) < size:
            break
        fr = np.frombuffer(buf, np.uint8).reshape(h, w, 3)
        enc.stdin.write(f(fr, t0 + n / FPS).tobytes())
        n += 1
        if n % 60 == 0:
            print(f"film: {n} frames", flush=True)
    enc.stdin.close(); enc.wait(); dec.wait()
    print("film done", n, "frames ->", dst)


if __name__ == "__main__":
    main()
