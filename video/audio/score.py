"""Procedural cinematic score synced to the visual timeline, plus the final mix.

usage: python3 score.py <build_dir>
reads  build/timeline.json, build/vo.wav
writes build/music.wav, build/mix.wav
"""
import sys, json
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt, fftconvolve

B = sys.argv[1]
SR = 48000
tl = json.load(open(f"{B}/timeline.json"))
T = {l["id"]: l for l in tl["lines"]}
OUTRO = 3.4
DUR = tl["duration"] + OUTRO
N = int(DUR * SR) + SR
rng = np.random.default_rng(7)


def word_time(line, word, at="start"):
    text = line["tts"]
    idx = text.find(word)
    if idx < 0:
        return line["start"]
    w = lambda c: 1.6 if c in "，。、？！：,.?!" else (0.6 if c.isascii() and c.isalpha() else 1.0)
    total = sum(w(c) for c in text)
    before = sum(w(c) for c in text[: idx + (len(word) if at == "end" else 0)])
    return line["start"] + (line["end"] - line["start"]) * before / total


# ---- event times (mirrors the shot code) ----------------------------------------------------
cut = {k: T[k]["start"] - 0.28 for k in ["stairs", "title", "disease", "survive"]}
t_boom = word_time(T["hook2"], "两亿") - 0.05
stairs_words = [word_time(T["stairs"], w) for w in ["食物", "力气", "信息"]] + [word_time(T["wisdom"], "智慧")]
t_elec = word_time(T["title"], "像电")
impacts = []
for bid in ["disease", "life", "origin", "dream", "time"]:
    fall = word_time(T["dream"], "正在倒下") - 0.35 if bid == "dream" else T[bid]["start"] + 0.2
    impacts.append(fall + 1.05)
t_rise = word_time(T["dream"], "一个人") - 0.1
t_shatter = word_time(T["time"], "还给") - 0.15
t_open = word_time(T["graduate"], "毕业") - 0.2
t_white = T["dare"]["start"] - 0.25
t_outro = T["dare"]["end"] + 0.9

L = np.zeros(N)
R = np.zeros(N)
SEND = np.zeros((2, N))  # reverb send


def place(sig, start, gain=1.0, pan=0.0, send=0.25):
    i = int(start * SR)
    if i >= N:
        return
    sig = sig[:, : N - i] if sig.ndim == 2 else sig[: N - i]
    a = (pan + 1) * np.pi / 4
    gl, gr = np.cos(a) * gain, np.sin(a) * gain
    if sig.ndim == 2:
        L[i:i + sig.shape[1]] += sig[0] * gain
        R[i:i + sig.shape[1]] += sig[1] * gain
        SEND[0, i:i + sig.shape[1]] += sig[0] * gain * send
        SEND[1, i:i + sig.shape[1]] += sig[1] * gain * send
    else:
        L[i:i + len(sig)] += sig * gl
        R[i:i + len(sig)] += sig * gr
        SEND[0, i:i + len(sig)] += sig * gl * send
        SEND[1, i:i + len(sig)] += sig * gr * send


def lp(x, fc, order=2):
    return sosfilt(butter(order, min(fc, SR / 2 * 0.95) / (SR / 2), "low", output="sos"), x)


def hp(x, fc, order=2):
    return sosfilt(butter(order, fc / (SR / 2), "high", output="sos"), x)


def bp(x, lo, hi):
    return sosfilt(butter(2, [lo / (SR / 2), min(hi, SR / 2 * 0.95) / (SR / 2)], "band", output="sos"), x)


def saw(f, n, detune_cents=0.0, phase=0.0):
    f = f * 2 ** (detune_cents / 1200)
    tt = np.arange(n) / SR
    out = np.zeros(n)
    k = 1
    while k * f < 9000 and k < 60:
        out += np.sin(2 * np.pi * k * f * tt + phase * k) / k
        k += 1
    return out * 0.55


def env(n, a, d_or_none=None, release=0.3, hold=None):
    tt = np.arange(n) / SR
    e = np.minimum(1, tt / max(a, 1e-4))
    if hold is not None:
        e *= np.where(tt > hold, np.exp(-(tt - hold) / release), 1)
    return e


def note(hz):
    return hz


# ---- instruments ---------------------------------------------------------------------------------
def pad(freqs, dur, attack=1.5, release=1.5, cutoff=1400, bright=0.0):
    n = int((dur + release) * SR)
    l = np.zeros(n); r = np.zeros(n)
    for f in freqs:
        l += saw(f, n, -6, rng.random() * 6) + saw(f, n, 4, rng.random() * 6)
        r += saw(f, n, 6, rng.random() * 6) + saw(f, n, -3, rng.random() * 6)
    tt = np.arange(n) / SR
    e = np.minimum(1, tt / attack) * np.where(tt > dur, np.exp(-(tt - dur) / (release / 3)), 1)
    l = lp(l, cutoff + bright) * e; r = lp(r, cutoff + bright) * e
    s = np.stack([l, r]) / (len(freqs) * 2)
    return s


def sub_hit(f0=70, f1=32, dur=3.0, k=7):
    n = int(dur * SR); tt = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-tt * k)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-tt * 1.4) * np.minimum(1, tt / 0.004)


def noise_burst(dur=0.6, fc=900, k=9):
    n = int(dur * SR); tt = np.arange(n) / SR
    return lp(rng.standard_normal(n), fc) * np.exp(-tt * k) * np.minimum(1, tt / 0.002)


def braam(root=36.71, dur=4.0):
    n = int(dur * SR); tt = np.arange(n) / SR
    x = sum(saw(root * m, n, d) for m, d in [(1, -8), (1, 8), (2, -5), (3, 4), (4, -3)])
    out = np.zeros(n); blk = 512
    zi = None
    for i in range(0, n, blk):
        fc = 180 + 2600 * np.exp(-(i / SR) * 2.2) * min(1, (i / SR) / 0.06)
        sos = butter(2, fc / (SR / 2), "low", output="sos")
        seg, zi = sosfilt(sos, x[i:i + blk], zi=zi if zi is not None else np.zeros((sos.shape[0], 2)))
        out[i:i + blk] = seg
    return out * np.exp(-tt * 0.7) * np.minimum(1, tt / 0.03) * 0.5


def riser(dur=2.4):
    n = int(dur * SR); tt = np.arange(n) / SR
    x = rng.standard_normal(n); out = np.zeros(n); blk = 1024; zi = None
    for i in range(0, n, blk):
        fc = 300 * (20 ** (i / n))
        sos = butter(2, [fc / (SR / 2), min(fc * 2.2, 20000) / (SR / 2)], "band", output="sos")
        seg, zi = sosfilt(sos, x[i:i + blk], zi=zi if zi is not None else np.zeros((sos.shape[0], 2)))
        out[i:i + blk] = seg
    return out * (tt / dur) ** 2.5


def tick(hz=3200):
    n = int(0.05 * SR); tt = np.arange(n) / SR
    return bp(rng.standard_normal(n), hz * 0.7, hz * 1.4) * np.exp(-tt * 140) + np.sin(2 * np.pi * hz * tt) * np.exp(-tt * 90) * 0.3


def pluck(f, dur=1.6):
    n = int(dur * SR); tt = np.arange(n) / SR
    x = (np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(4 * np.pi * f * tt) + 0.12 * np.sin(6 * np.pi * f * tt))
    return lp(x * np.exp(-tt * 3.2) * np.minimum(1, tt / 0.003), 3500)


def shimmer(freqs, dur, attack=0.8):
    n = int(dur * SR); tt = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * tt + rng.random() * 6) * (1 + 0.3 * np.sin(2 * np.pi * (4 + i) * tt)) for i, f in enumerate(freqs))
    e = np.minimum(1, tt / attack) * np.minimum(1, (dur - tt) / 0.8)
    return x * e / len(freqs)


def heartbeat():
    n = int(0.5 * SR); tt = np.arange(n) / SR
    beat = lambda d: np.where(tt >= d, np.sin(2 * np.pi * 52 * (tt - d)) * np.exp(-(tt - d) * 16), 0)
    return beat(0) + 0.6 * beat(0.22)


# notes
D2, F2, G2, A2, Bb2, C3 = 73.42, 87.31, 98.0, 110.0, 116.54, 130.81
D3, E3, F3, Fs3, G3, A3, Bb3, C4, D4 = 146.83, 164.81, 174.61, 185.0, 196.0, 220.0, 233.08, 261.63, 293.66
A4, D5, E5, F5, Fs5, A5, D6 = 440.0, 587.33, 659.26, 698.46, 739.99, 880.0, 1174.66

# ---- arrangement ----------------------------------------------------------------------------------
# 1. cold open: dark drone + ticking that accelerates into the boom
place(pad([D2, A2, D3], t_boom + 0.2, attack=2.5, release=1.2, cutoff=500), 0.0, 0.55)
tk = 0.95
while tk < t_boom - 0.15:
    place(tick(3000 if int(tk * 2) % 2 else 2400), tk, 0.11, pan=0.3 if int(tk * 2) % 2 else -0.3, send=0.15)
    gap = 0.5 - 0.32 * min(1, max(0, (tk - 4.5) / (t_boom - 4.5)))
    tk += gap
place(riser(2.6), t_boom - 2.6, 0.28, send=0.4)
# 2. the boom
place(sub_hit(80, 30, 4.5, 6), t_boom, 0.95, send=0.2)
place(noise_burst(1.2, 1400, 4), t_boom, 0.35, send=0.6)
place(braam(36.71, 4.5), t_boom, 0.6, pan=-0.15, send=0.5)
place(braam(36.71 * 1.5, 4.5), t_boom + 0.01, 0.35, pan=0.15, send=0.5)
place(pad([D2, A2, D3, F3, A3], cut["stairs"] - t_boom + 0.3, attack=0.6, release=0.6, cutoff=1800), t_boom, 0.45)

# 3. stairs: rising arpeggio, one step per word
arp = [D3, F3, A3, D4, F3, A3, D4, E5 / 2, A3, D4, F5 / 2, A4]
bt = 0.24
for i in range(int((cut["title"] - cut["stairs"]) / bt)):
    tt = cut["stairs"] + i * bt
    level = sum(tt > w for w in stairs_words[:3])
    f = arp[(i + level * 2) % len(arp)] * (2 if level >= 2 and i % 2 else 1)
    place(pluck(f, 1.4), tt, 0.10 + 0.03 * level, pan=np.sin(i * 1.3) * 0.5, send=0.45)
for w in stairs_words[:3]:
    place(sub_hit(60, 38, 1.2, 9), w, 0.35, send=0.2)
place(pad([D3, F3, A3, C4], cut["title"] - cut["stairs"], attack=1.2, release=0.8, cutoff=2200), cut["stairs"], 0.32)
# ignite on "智慧"
place(riser(1.2), stairs_words[3] - 1.2, 0.22, send=0.5)
place(sub_hit(90, 34, 3.0, 6), stairs_words[3], 0.8, send=0.3)
place(np.stack([shimmer([D5, A5, D6], 3.5, 0.2)] * 2), stairs_words[3], 0.18, send=0.8)

# 4. title: electric shimmer and a broad chord
place(pad([Bb2, F3, Bb3, D4], cut["disease"] - cut["title"] + 0.5, attack=0.4, release=1.0, cutoff=2600), cut["title"], 0.42)
place(np.stack([shimmer([F5, Bb3 * 4, D6], cut["disease"] - cut["title"], 0.3)] * 2), cut["title"], 0.12, send=0.7)
for i in range(14):
    place(tick(5000 + 400 * (i % 5)), t_elec - 0.3 + i * 0.09, 0.05, pan=np.sin(i) * 0.8, send=0.5)

# 5. walls: chord per wall, heartbeat underneath, a heavy impact on each landing
chords = [[D2, A2, D3, F3], [Bb2, F3, Bb3, D4], [F2, C3, F3, A3], [C3, G3, C4, E3 * 2], [G2, D3, G3, Bb3]]
starts = [cut["disease"]] + [T[k]["start"] - 0.28 for k in ["life", "origin", "dream", "time"]] + [cut["survive"]]
for i, ch in enumerate(chords):
    place(pad(ch, starts[i + 1] - starts[i] + 0.2, attack=0.5, release=0.8, cutoff=1300 + 350 * i), starts[i], 0.36 + 0.03 * i)
hb = cut["disease"] + 0.2
while hb < cut["survive"] - 0.4:
    place(heartbeat(), hb, 0.32, send=0.1)
    hb += 0.82
for i, t_imp in enumerate(impacts):
    place(sub_hit(75, 28, 3.0, 7), t_imp, 0.9, send=0.25)
    place(noise_burst(0.9, 700, 6), t_imp, 0.4, send=0.5)
    place(braam(36.71 * [1, 0.8909, 1.335, 1.189, 0.749][i], 2.6), t_imp + 0.005, 0.3, send=0.5)
place(np.stack([shimmer([G3 * 4, D5, Bb3 * 4], 2.4, 0.5)] * 2), t_rise, 0.12, send=0.7)
for i in range(18):
    place(tick(2600 + 500 * (i % 4)), t_shatter + i * 0.05 + rng.random() * 0.03, 0.07, pan=rng.uniform(-0.9, 0.9), send=0.6)

# 6. door: long swell into a major chord when the door opens
place(pad([D2, A2, D3, F3, A3], t_open - cut["survive"], attack=2.0, release=0.4, cutoff=900), cut["survive"], 0.4)
place(riser(2.2), t_open - 2.2, 0.25, send=0.5)
place(sub_hit(70, 30, 4.0, 5), t_open, 0.75, send=0.35)
place(pad([D2, A2, D3, Fs3, A3, D4, Fs3 * 2], t_white - t_open + 0.1, attack=0.25, release=0.25, cutoff=2600, bright=800), t_open, 0.55)
place(np.stack([shimmer([D5, Fs5, A5, D6], t_white - t_open + 0.2, 0.6)] * 2), t_open, 0.16, send=0.8)
# hard cut to silence at the white-out, then one last hit under "你敢不敢想"
cut_i = int(t_white * SR)
fade = np.ones(N); fade[cut_i:cut_i + int(0.12 * SR)] = np.linspace(1, 0, int(0.12 * SR)); fade[cut_i + int(0.12 * SR):] = 0
L *= fade; R *= fade; SEND *= fade
place(sub_hit(65, 30, 5.0, 4), T["dare"]["start"] - 0.02, 0.85, send=0.5)
place(np.stack([shimmer([D5, A5], 6.0, 0.05)] * 2), T["dare"]["start"], 0.1, send=0.9)
place(pad([D3, Fs3, A3, D4], DUR - t_outro + 0.5, attack=1.2, release=2.0, cutoff=1500), t_outro - 0.4, 0.3)

# ---- reverb ----------------------------------------------------------------------------------------
ir_n = int(3.8 * SR); it = np.arange(ir_n) / SR
ir = np.stack([lp(rng.standard_normal(ir_n), 6000) * np.exp(-it * 1.9) for _ in range(2)])
ir[:, : int(0.012 * SR)] *= np.linspace(0, 1, int(0.012 * SR))
wet = np.stack([fftconvolve(SEND[c], ir[c])[:N] for c in range(2)]) * 0.09
music = np.stack([L, R]) + wet
music = hp(music, 28)
music = np.tanh(music * 1.1) / 1.1  # gentle glue

# ---- mix with voice-over, ducking the music under speech ----------------------------------------------
vo, sr = sf.read(f"{B}/vo.wav", dtype="float64")
assert sr == SR
vo = np.pad(vo, (0, N - len(vo)))[:N]
vo = hp(vo, 70)
env_vo = np.convolve(np.abs(vo), np.ones(int(0.05 * SR)) / int(0.05 * SR), "same")
duck = 1 - 0.35 * np.clip(env_vo / 0.06, 0, 1)
duck = np.convolve(duck, np.ones(int(0.12 * SR)) / int(0.12 * SR), "same")
n_out = int(DUR * SR)
music = music[:, :n_out]
vo = vo[:n_out]
speech = env_vo[:n_out] > 0.02
rms = lambda a: np.sqrt(np.mean(a ** 2) + 1e-12)
# music sits ~10 dB under the voice while it speaks; hits are allowed to poke above via the limiter
g = rms(vo[speech]) / rms(music[:, speech]) * 10 ** (-8 / 20)
mix = music * duck[:n_out] * g + vo
# soft-knee limiter on peaks only
thr = 0.6
over = np.abs(mix) > thr
mix[over] = np.sign(mix[over]) * (thr + (1 - thr) * np.tanh((np.abs(mix[over]) - thr) / (1 - thr)))
mix = mix / np.abs(mix).max() * 0.95
sf.write(f"{B}/music.wav", (music / np.abs(music).max() * 0.9).T, SR)
sf.write(f"{B}/mix.wav", mix.T, SR)
print(f"duration {DUR:.2f}s  boom {t_boom:.2f}  impacts {[round(x, 2) for x in impacts]}  open {t_open:.2f}  white {t_white:.2f}")
