"""Music-only score for the silent (text-driven) cut, synced to build/timeline.json.

usage: python3 score2.py <build_dir>   ->  build/mix.wav
"""
import sys, json
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt, fftconvolve

B = sys.argv[1]
SR = 48000
tl = json.load(open(f"{B}/timeline.json"))
T = {l["id"]: l for l in tl["lines"]}
DUR = tl["duration"] + tl.get("outro", 3.4)
N = int(DUR * SR) + SR
rng = np.random.default_rng(11)
ev = lambda lid, k: T[lid]["start"] + T[lid]["ev"][k]

# ---- event times (mirror the shot code) --------------------------------------------------------
cut_stairs, cut_title, cut_walls, cut_door = (T[k]["start"] - 0.28 for k in ["stairs", "bottleneck", "disease", "survive"])
t_boom = ev("hook2", "两亿") - 0.05
stairs_words = [ev("stairs", w) for w in ["食物", "力气", "信息"]] + [ev("wisdom", "智慧")]
t_genius, t_title, t_elec = T["genius"]["start"], T["title"]["start"], ev("title", "像电")
walls = []
for bid in ["disease", "life", "origin", "dream", "time"]:
    s = T[bid]["start"]
    fall = ev("dream", "正在倒下") - 0.35 if bid == "dream" else s + 0.2
    imp = fall + 1.05
    tb = ev("time", "还给") - 0.1 if bid == "time" else (imp + 2.7 if bid == "dream" else s + 3.9)
    walls.append((s - 0.28, imp, tb))
t_rise = ev("dream", "一个人") - 0.1
t_open = ev("graduate", "毕业") - 0.2
t_white = T["graduate"]["end"] - 0.1
t_q, t_dare = T["question"]["start"], T["dare"]["start"]
t_outro = T["dare"]["end"] + 0.9

L = np.zeros(N); R = np.zeros(N); SEND = np.zeros((2, N))


def place(sig, start, gain=1.0, pan=0.0, send=0.25):
    i = int(start * SR)
    if i >= N or i < 0:
        return
    sig = sig[:, : N - i] if sig.ndim == 2 else sig[: N - i]
    if sig.ndim == 2:
        n = sig.shape[1]
        L[i:i + n] += sig[0] * gain; R[i:i + n] += sig[1] * gain
        SEND[0, i:i + n] += sig[0] * gain * send; SEND[1, i:i + n] += sig[1] * gain * send
    else:
        a = (pan + 1) * np.pi / 4
        n = len(sig)
        L[i:i + n] += sig * np.cos(a) * gain; R[i:i + n] += sig * np.sin(a) * gain
        SEND[0, i:i + n] += sig * np.cos(a) * gain * send; SEND[1, i:i + n] += sig * np.sin(a) * gain * send


def lp(x, fc, o=2): return sosfilt(butter(o, min(fc, SR * 0.47) / (SR / 2), "low", output="sos"), x)
def hp(x, fc, o=2): return sosfilt(butter(o, fc / (SR / 2), "high", output="sos"), x)
def bp(x, lo, hi): return sosfilt(butter(2, [lo / (SR / 2), min(hi, SR * 0.47) / (SR / 2)], "band", output="sos"), x)


def saw(f, n, cents=0.0, ph=0.0):
    f = f * 2 ** (cents / 1200); tt = np.arange(n) / SR; out = np.zeros(n); k = 1
    while k * f < 9000 and k < 60:
        out += np.sin(2 * np.pi * k * f * tt + ph * k) / k; k += 1
    return out * 0.55


def pad(freqs, dur, attack=1.5, release=1.5, cutoff=1400):
    n = int((dur + release) * SR); l = np.zeros(n); r = np.zeros(n)
    for f in freqs:
        l += saw(f, n, -6, rng.random() * 6) + saw(f, n, 4, rng.random() * 6)
        r += saw(f, n, 6, rng.random() * 6) + saw(f, n, -3, rng.random() * 6)
    tt = np.arange(n) / SR
    e = np.minimum(1, tt / attack) * np.where(tt > dur, np.exp(-(tt - dur) / (release / 3)), 1)
    return np.stack([lp(l, cutoff) * e, lp(r, cutoff) * e]) / (len(freqs) * 2)


def sub_hit(f0=70, f1=32, dur=3.0, k=7):
    n = int(dur * SR); tt = np.arange(n) / SR
    ph = 2 * np.pi * np.cumsum(f1 + (f0 - f1) * np.exp(-tt * k)) / SR
    return np.sin(ph) * np.exp(-tt * 1.4) * np.minimum(1, tt / 0.004)


def noise_burst(dur=0.6, fc=900, k=9):
    n = int(dur * SR); tt = np.arange(n) / SR
    return lp(rng.standard_normal(n), fc) * np.exp(-tt * k) * np.minimum(1, tt / 0.002)


def braam(root=36.71, dur=4.0):
    n = int(dur * SR); tt = np.arange(n) / SR
    x = sum(saw(root * m, n, d) for m, d in [(1, -8), (1, 8), (2, -5), (3, 4), (4, -3)])
    out = np.zeros(n); blk = 512; zi = None
    for i in range(0, n, blk):
        fc = 180 + 2600 * np.exp(-(i / SR) * 2.2) * min(1, (i / SR) / 0.06)
        sos = butter(2, fc / (SR / 2), "low", output="sos")
        seg, zi = sosfilt(sos, x[i:i + blk], zi=zi if zi is not None else np.zeros((sos.shape[0], 2)))
        out[i:i + blk] = seg
    return out * np.exp(-tt * 0.7) * np.minimum(1, tt / 0.03) * 0.5


def sweep(dur=2.4, f0=300, ratio=20, curve=2.5, rev=False):
    n = int(dur * SR); tt = np.arange(n) / SR; x = rng.standard_normal(n); out = np.zeros(n); blk = 1024; zi = None
    for i in range(0, n, blk):
        fc = f0 * (ratio ** (i / n))
        sos = butter(2, [fc / (SR / 2), min(fc * 2.2, 20000) / (SR / 2)], "band", output="sos")
        seg, zi = sosfilt(sos, x[i:i + blk], zi=zi if zi is not None else np.zeros((sos.shape[0], 2)))
        out[i:i + blk] = seg
    e = (tt / dur) ** curve
    return out * (e[::-1] if rev else e)


def whoosh(dur=0.55):
    n = int(dur * SR); tt = np.arange(n) / SR
    return sweep(dur, 400, 12, 1.0) * np.sin(np.pi * tt / dur) ** 1.5 * 1.6


def tick(hz=3200):
    n = int(0.05 * SR); tt = np.arange(n) / SR
    return bp(rng.standard_normal(n), hz * 0.7, hz * 1.4) * np.exp(-tt * 140) + np.sin(2 * np.pi * hz * tt) * np.exp(-tt * 90) * 0.3


def pluck(f, dur=1.4):
    n = int(dur * SR); tt = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(4 * np.pi * f * tt) + 0.12 * np.sin(6 * np.pi * f * tt)
    return lp(x * np.exp(-tt * 3.2) * np.minimum(1, tt / 0.003), 3500)


def bell(f, dur=3.0):
    n = int(dur * SR); tt = np.arange(n) / SR
    x = sum(a * np.sin(2 * np.pi * f * m * tt) * np.exp(-tt * d) for m, a, d in [(1, 1, 1.2), (2.76, 0.5, 2.0), (5.4, 0.25, 3.5), (8.9, 0.12, 5)])
    return x * np.minimum(1, tt / 0.002)


def shimmer(freqs, dur, attack=0.8):
    n = int(dur * SR); tt = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * tt + rng.random() * 6) * (1 + 0.3 * np.sin(2 * np.pi * (4 + i) * tt)) for i, f in enumerate(freqs))
    return x * np.minimum(1, tt / attack) * np.minimum(1, np.maximum(0, (dur - tt)) / 0.8) / len(freqs)


def kick():
    n = int(0.45 * SR); tt = np.arange(n) / SR
    ph = 2 * np.pi * np.cumsum(45 + 110 * np.exp(-tt * 30)) / SR
    return np.sin(ph) * np.exp(-tt * 9) + lp(rng.standard_normal(n), 2500) * np.exp(-tt * 80) * 0.15


def stereo(x): return np.stack([x, x])


D2, F2, G2, A2, Bb2, C3 = 73.42, 87.31, 98.0, 110.0, 116.54, 130.81
D3, E3, F3, Fs3, G3, A3, Bb3, C4, D4, E4, F4, A4 = 146.83, 164.81, 174.61, 185.0, 196.0, 220.0, 233.08, 261.63, 293.66, 329.63, 349.23, 440.0
D5, E5, F5, Fs5, A5, D6 = 587.33, 659.26, 698.46, 739.99, 880.0, 1174.66
beat = 60 / 96

# ---- 1. cold open --------------------------------------------------------------------------------------
place(pad([D2, A2, D3], t_boom + 0.3, attack=2.5, release=1.0, cutoff=480), 0.0, 0.6)
tk = 0.6
while tk < t_boom - 0.12:
    odd = int(tk / beat * 2) % 2
    place(tick(3000 if odd else 2300), tk, 0.12, pan=0.35 if odd else -0.35, send=0.15)
    tk += beat / 2 * (1 - 0.55 * min(1, max(0, (tk - 2.5) / (t_boom - 2.5))))
place(sweep(2.6), t_boom - 2.6, 0.3, send=0.4)
place(sub_hit(80, 30, 4.5, 6), t_boom, 1.0, send=0.2)
place(noise_burst(1.4, 1600, 3.5), t_boom, 0.4, send=0.6)
place(braam(36.71, 5.0), t_boom, 0.7, pan=-0.15, send=0.5)
place(braam(55.0, 5.0), t_boom + 0.01, 0.4, pan=0.15, send=0.5)
place(pad([D2, A2, D3, F3, A3], cut_stairs - t_boom + 0.3, attack=0.5, release=0.8, cutoff=1900), t_boom, 0.5)
for i, f in enumerate([D5, A4, F5]):
    place(bell(f, 3.5), T["nobel"]["start"] + i * 0.12, 0.13, pan=[-0.4, 0.4, 0][i], send=0.7)
place(sub_hit(60, 34, 2.0, 8), T["nobel"]["start"], 0.5, send=0.3)
place(sub_hit(70, 30, 2.5, 7), ev("trailer", "这只是"), 0.7, send=0.3)
place(braam(36.71, 2.5), ev("trailer", "这只是"), 0.35, send=0.5)
place(sweep(1.4), cut_stairs - 1.4, 0.22, send=0.5)

# ---- 2. stairs: rising arpeggio, a hit per step ----------------------------------------------------
arp = [D3, F3, A3, D4, F3, A3, D4, E4, A3, D4, F4, A4]
bt = beat / 2
for i in range(int((cut_title - cut_stairs) / bt)):
    tt = cut_stairs + i * bt
    level = sum(tt > w for w in stairs_words[:3])
    f = arp[(i + level * 2) % len(arp)] * (2 if level >= 2 and i % 2 else 1)
    place(pluck(f), tt, 0.11 + 0.03 * level, pan=np.sin(i * 1.3) * 0.5, send=0.45)
    if i % 2 == 0:
        place(kick(), tt, 0.25 + 0.08 * level, send=0.05)
for w in stairs_words[:3]:
    place(sub_hit(60, 38, 1.2, 9), w, 0.4, send=0.2)
place(pad([D3, F3, A3, C4], cut_title - cut_stairs, attack=1.0, release=0.8, cutoff=2200), cut_stairs, 0.35)
place(sweep(1.2), stairs_words[3] - 1.2, 0.25, send=0.5)
place(sub_hit(90, 34, 3.0, 6), stairs_words[3], 0.9, send=0.3)
place(braam(36.71, 3.0), stairs_words[3], 0.4, send=0.5)
place(stereo(shimmer([D5, A5, D6], 3.0, 0.2)), stairs_words[3], 0.2, send=0.8)

# ---- 3. bottleneck (tense) -> genius (opens up) -> title ------------------------------------------------
place(pad([Bb2, F3, Bb3], t_genius - cut_title, attack=0.6, release=0.4, cutoff=700), cut_title, 0.45)
tt = cut_title + 0.2
while tt < t_genius - 0.1:
    place(kick(), tt, 0.32, send=0.05)
    place(tick(1800), tt + beat / 2, 0.08, send=0.2)
    tt += beat
place(sub_hit(70, 34, 2.0, 7), T["bottleneck"]["start"] + 0.3, 0.6, send=0.3)
place(sweep(1.0), t_genius - 1.0, 0.2, send=0.5)
place(sub_hit(80, 34, 2.5, 6), t_genius, 0.7, send=0.3)
place(pad([Bb2, F3, Bb3, D4, F4], cut_walls - t_genius + 0.4, attack=0.3, release=0.8, cutoff=3000), t_genius, 0.42)
for i in range(int((cut_walls - t_genius) / (beat / 2))):
    place(pluck([Bb3, D4, F4, Bb3 * 2, F4, D4][i % 6] * 2, 1.0), t_genius + i * beat / 2, 0.09, pan=np.sin(i) * 0.6, send=0.5)
place(stereo(shimmer([F5, Bb3 * 4, D6], cut_walls - t_title, 0.3)), t_title, 0.14, send=0.7)
place(sub_hit(90, 30, 3.0, 6), t_title, 0.8, send=0.3)
for i in range(16):
    place(tick(5000 + 400 * (i % 5)), t_elec - 0.2 + i * 0.07, 0.06, pan=np.sin(i) * 0.8, send=0.5)

# ---- 4. the five walls: driving pulse, chord per wall, impacts ---------------------------------------
chords = [[D2, A2, D3, F3], [Bb2, F3, Bb3, D4], [F2, C3, F3, A3], [C3, G3, C4, E4], [G2, D3, G3, Bb3]]
roots = [36.71, 29.14, 43.65, 32.70, 49.0]
for i, (cut, imp, tb) in enumerate(walls):
    nxt = walls[i + 1][0] if i + 1 < len(walls) else cut_door
    place(whoosh(0.5), cut - 0.45, 0.35, send=0.3)
    place(pad(chords[i], nxt - cut + 0.2, attack=0.4, release=0.8, cutoff=1300 + 380 * i), cut, 0.38 + 0.03 * i)
    place(sweep(0.9, 500, 10), imp - 0.9, 0.18, send=0.4)
    place(sub_hit(78, 28, 3.0, 7), imp, 1.0, send=0.25)
    place(noise_burst(1.0, 800, 5), imp, 0.45, send=0.5)
    place(braam(roots[i], 2.8), imp + 0.005, 0.38, send=0.5)
    place(bell([D5, F5, A5, E5, G3 * 4][i], 2.5), tb, 0.12, pan=0.3, send=0.7)
    tt = imp + beat
    while tt < nxt - 0.2:
        place(kick(), tt, 0.22 + 0.04 * i, send=0.05)
        place(tick(2600), tt + beat / 2, 0.05 + 0.01 * i, pan=-0.3, send=0.2)
        tt += beat
place(stereo(shimmer([G3 * 4, D5, Bb3 * 4], 2.4, 0.5)), t_rise, 0.14, send=0.7)
for i in range(22):
    place(tick(2600 + 500 * (i % 4)), walls[4][2] + i * 0.045 + rng.random() * 0.03, 0.07, pan=rng.uniform(-0.9, 0.9), send=0.6)

# ---- 5. door: sparse, then a major swell when it opens ----------------------------------------------
place(whoosh(0.6), cut_door - 0.5, 0.35, send=0.3)
place(pad([D2, A2, D3, F3, A3], t_open - cut_door, attack=1.6, release=0.4, cutoff=900), cut_door, 0.45)
place(sweep(2.4), t_open - 2.4, 0.28, send=0.5)
place(sub_hit(70, 30, 4.0, 5), t_open, 0.85, send=0.35)
place(pad([D2, A2, D3, Fs3, A3, D4, Fs3 * 2], t_white - t_open + 0.1, attack=0.25, release=0.25, cutoff=3200), t_open, 0.6)
place(stereo(shimmer([D5, Fs5, A5, D6], t_white - t_open + 0.2, 0.5)), t_open, 0.18, send=0.8)
# hard cut at the white flash, then deep space
ci = int(t_white * SR); fl = int(0.1 * SR)
fade = np.ones(N); fade[ci:ci + fl] = np.linspace(1, 0, fl); fade[ci + fl:] = 0
L *= fade; R *= fade; SEND *= fade
place(pad([D2, A2, E3, Fs3, A3], DUR - t_white, attack=1.4, release=2.0, cutoff=1100), t_white + 0.1, 0.32)
place(stereo(shimmer([A4, E5, Fs5], t_dare - t_q + 0.5, 1.0)), t_q, 0.08, send=0.9)
place(sub_hit(65, 30, 5.0, 4), t_dare, 0.95, send=0.5)
place(braam(36.71, 4.0), t_dare, 0.35, send=0.6)
place(stereo(shimmer([D5, A5, D6], DUR - t_dare, 0.05)), t_dare, 0.12, send=0.9)
for i, f in enumerate([D5, Fs5, A5]):
    place(bell(f, 3.0), t_outro + i * 0.18, 0.1, pan=[-0.4, 0, 0.4][i], send=0.8)

# ---- reverb, master ------------------------------------------------------------------------------------
ir_n = int(3.8 * SR); it = np.arange(ir_n) / SR
ir = np.stack([lp(rng.standard_normal(ir_n), 6000) * np.exp(-it * 1.9) for _ in range(2)])
ir[:, : int(0.012 * SR)] *= np.linspace(0, 1, int(0.012 * SR))
wet = np.stack([fftconvolve(SEND[c], ir[c])[:N] for c in range(2)]) * 0.09
mix = hp(np.stack([L, R]) + wet, 28)
n_out = int(DUR * SR)
mix = mix[:, :n_out]
tail = int(1.2 * SR); mix[:, -tail:] *= np.linspace(1, 0, tail) ** 1.5
thr = 0.55; over = np.abs(mix) > thr
mix[over] = np.sign(mix[over]) * (thr + (1 - thr) * np.tanh((np.abs(mix[over]) - thr) / (1 - thr)))
mix = mix / np.abs(mix).max() * 0.95
sf.write(f"{B}/mix.wav", mix.T, SR)
print(f"duration {DUR:.2f}s boom {t_boom:.2f} impacts {[round(w[1], 2) for w in walls]} open {t_open:.2f} white {t_white:.2f}")
