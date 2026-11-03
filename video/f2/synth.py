"""Small synthesis toolkit for the F2 score: every sound is generated, nothing is sampled.

Signals are float32 numpy arrays at SR. Stereo signals have shape (2, n).
"""
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000
RNG = np.random.default_rng(2026)


def secs(n):
    return int(round(n * SR))


def t_axis(dur):
    return np.arange(secs(dur), dtype=np.float32) / SR


# ---------------------------------------------------------------- envelopes
def env_exp(dur, decay, attack=0.004):
    t = t_axis(dur)
    a = np.clip(t / max(attack, 1e-4), 0, 1)
    return (a * np.exp(-t / decay)).astype(np.float32)


def env_adsr(dur, a=0.01, d=0.1, s=0.7, r=0.3):
    n = secs(dur)
    t = np.arange(n) / SR
    e = np.where(t < a, t / a, np.where(t < a + d, 1 - (1 - s) * (t - a) / d, s))
    rel_start = max(0, dur - r)
    e = np.where(t > rel_start, e * np.clip(1 - (t - rel_start) / max(r, 1e-4), 0, 1), e)
    return e.astype(np.float32)


def fade(sig, fin=0.01, fout=0.05):
    n = sig.shape[-1]
    e = np.ones(n, np.float32)
    a, b = min(n, secs(fin)), min(n, secs(fout))
    if a: e[:a] = np.linspace(0, 1, a) ** 2
    if b: e[-b:] *= np.linspace(1, 0, b) ** 2
    return sig * e


# ---------------------------------------------------------------- filters
def lp(x, f, order=2):
    sos = butter(order, min(f, SR / 2 * 0.99), 'low', fs=SR, output='sos')
    return sosfilt(sos, x, axis=-1).astype(np.float32)


def hp(x, f, order=2):
    sos = butter(order, max(f, 5), 'high', fs=SR, output='sos')
    return sosfilt(sos, x, axis=-1).astype(np.float32)


def bp(x, lo, hi, order=2):
    sos = butter(order, [max(lo, 5), min(hi, SR / 2 * 0.99)], 'band', fs=SR, output='sos')
    return sosfilt(sos, x, axis=-1).astype(np.float32)


def sweep_bp(x, f0, f1, q=6.0, steps=64):
    """Band-pass whose centre glides from f0 to f1 (log), processed in overlapping blocks."""
    n = x.shape[-1]
    out = np.zeros_like(x)
    hop = n // steps + 1
    win = np.hanning(hop * 2).astype(np.float32)
    for i in range(steps + 1):
        a = i * hop
        seg = x[..., max(0, a - hop): a + hop]
        if seg.shape[-1] < 8:
            continue
        fc = f0 * (f1 / f0) ** (i / steps)
        bw = fc / q
        y = bp(seg, fc - bw / 2, fc + bw / 2)
        w = win[: y.shape[-1]] if a - hop >= 0 else win[hop: hop + y.shape[-1]]
        out[..., max(0, a - hop): max(0, a - hop) + y.shape[-1]] += y * w[: y.shape[-1]]
    return out


# ---------------------------------------------------------------- sources
def sine(f, dur, phase=0.0):
    t = t_axis(dur)
    if callable(f):
        ph = 2 * np.pi * np.cumsum(f(t)) / SR
        return np.sin(ph + phase).astype(np.float32)
    return np.sin(2 * np.pi * f * t + phase).astype(np.float32)


def noise(dur, stereo=False):
    n = secs(dur)
    return RNG.standard_normal((2, n) if stereo else n).astype(np.float32)


def pink(dur, stereo=False):
    w = noise(dur, stereo)
    spec = np.fft.rfft(w, axis=-1)
    f = np.fft.rfftfreq(w.shape[-1], 1 / SR)
    f[0] = 1
    spec /= np.sqrt(f)
    p = np.fft.irfft(spec, n=w.shape[-1], axis=-1)
    return (p / (np.abs(p).max() + 1e-9)).astype(np.float32)


def saw_additive(f, dur, partials=24, detune_cents=0.0):
    t = t_axis(dur)
    fd = f * 2 ** (detune_cents / 1200)
    y = np.zeros_like(t)
    for k in range(1, partials + 1):
        if fd * k > SR / 2 * 0.9:
            break
        y += np.sin(2 * np.pi * fd * k * t) / k
    return (y * 0.6).astype(np.float32)


# ---------------------------------------------------------------- instruments
def felt_piano(freq, dur=4.0, vel=0.7, bright=0.5):
    """Soft felt-piano-like tone: slightly inharmonic partials, fast-decaying highs, hammer thump."""
    t = t_axis(dur)
    B = 0.00025  # inharmonicity
    y = np.zeros_like(t)
    for k in range(1, 14):
        fk = freq * k * np.sqrt(1 + B * k * k)
        if fk > 12000:
            break
        amp = (1 / k ** (1.6 - 0.6 * bright)) * (0.9 + 0.2 * RNG.random())
        dec = (2.8 / (1 + 0.45 * (k - 1))) * (220 / max(freq, 60)) ** 0.25
        y += amp * np.sin(2 * np.pi * fk * t + RNG.random() * 6.28) * np.exp(-t / dec)
    # two-stage decay (prompt + aftersound) and a little detuned string pair for chorus
    y2 = np.sin(2 * np.pi * freq * 1.0012 * t) * np.exp(-t / 3.5) * 0.25
    thump = lp(noise(0.05), 900) * env_exp(0.05, 0.012) * 0.25
    y[: thump.size] += thump
    y = (y + y2) * (0.25 + 0.75 * vel)
    y = lp(y, 1800 + 4200 * bright * vel)
    return fade(y.astype(np.float32), 0.002, 0.3)


def fm_bell(freq, dur=3.0, ratio=3.5, index=2.2, decay=1.2):
    t = t_axis(dur)
    ienv = np.exp(-t / (decay * 0.35))
    mod = np.sin(2 * np.pi * freq * ratio * t) * index * ienv
    y = np.sin(2 * np.pi * freq * t + mod) * np.exp(-t / decay)
    return fade(y.astype(np.float32), 0.001, 0.2)


def coin_ping(freq=2400, dur=1.6):
    """Metallic disc: inharmonic modes of a free plate, quick pitch settle, bright transient."""
    t = t_axis(dur)
    modes = [(1.0, 1.0, 0.9), (1.594, 0.6, 0.7), (2.136, 0.45, 0.55), (2.653, 0.32, 0.45), (3.156, 0.22, 0.35), (4.06, 0.12, 0.25)]
    y = np.zeros_like(t)
    drift = 1 + 0.004 * np.exp(-t / 0.05)
    for r, a, d in modes:
        y += a * np.sin(2 * np.pi * freq * r * np.cumsum(drift) / SR + RNG.random() * 6.28) * np.exp(-t / d)
    click = hp(noise(0.01), 3000) * env_exp(0.01, 0.0015) * 0.6
    y[: click.size] += click
    return fade(y.astype(np.float32) * 0.5, 0.0005, 0.2)


def sub_hit(dur=2.2, f0=58, f1=32, decay=0.7):
    t = t_axis(dur)
    f = f1 + (f0 - f1) * np.exp(-t / 0.12)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / decay)
    y = np.tanh(y * 1.6) / np.tanh(1.6)
    return fade(y.astype(np.float32), 0.003, 0.3)


def whoosh(dur=1.4, f0=300, f1=4000, peak=0.65, stereo=True):
    x = pink(dur, stereo)
    y = sweep_bp(x, f0, f1, q=3.0)
    t = t_axis(dur)
    e = np.where(t < dur * peak, (t / (dur * peak)) ** 2.2, np.exp(-(t - dur * peak) / (dur * 0.12)))
    return (y * e.astype(np.float32)).astype(np.float32)


def tick(f=4200, dur=0.03, level=0.5):
    y = hp(noise(dur), f) * env_exp(dur, 0.004)
    return (y * level).astype(np.float32)


def drone(freq, dur, voices=5, spread_cents=9, cutoff=900, lfo=0.07):
    t = t_axis(dur)
    L = np.zeros_like(t); R = np.zeros_like(t)
    for v in range(voices):
        c = (v - (voices - 1) / 2) * spread_cents / max(1, (voices - 1) / 2)
        s = saw_additive(freq, dur, partials=18, detune_cents=c)
        pan = (v / max(1, voices - 1)) * 2 - 1
        L += s * np.cos((pan + 1) * np.pi / 4); R += s * np.sin((pan + 1) * np.pi / 4)
    st = np.stack([L, R]) / voices
    st = lp(st, cutoff)
    st *= (1 + 0.25 * np.sin(2 * np.pi * lfo * t))[None, :]
    return st.astype(np.float32)


# ---------------------------------------------------------------- space
def reverb_ir(dur=3.2, predelay=0.02, damp=4500, seed=3):
    r = np.random.default_rng(seed)
    n = secs(dur)
    t = np.arange(n) / SR
    ir = r.standard_normal((2, n)).astype(np.float32) * np.exp(-t / (dur / 6.9))[None, :]
    ir = lp(ir, damp)
    ir[:, : secs(predelay)] = 0
    return ir / np.abs(ir).max()


def convolve(x, ir):
    if x.ndim == 1:
        x = np.stack([x, x])
    out = np.stack([fftconvolve(x[c], ir[c])[: x.shape[1]] for c in range(2)])
    return out.astype(np.float32)


def pan(x, p=0.0):
    a = (p + 1) * np.pi / 4
    return np.stack([x * np.cos(a), x * np.sin(a)]).astype(np.float32)


class Mix:
    def __init__(self, dur):
        self.n = secs(dur) + SR
        self.dry = np.zeros((2, self.n), np.float32)
        self.send = np.zeros((2, self.n), np.float32)

    def add(self, sig, at, gain=1.0, p=0.0, send=0.2):
        if sig.ndim == 1:
            sig = pan(sig, p)
        i = secs(at)
        if i >= self.n:
            return
        m = min(sig.shape[1], self.n - i)
        if i < 0:
            sig = sig[:, -i:]; m = min(sig.shape[1], self.n); i = 0
        self.dry[:, i:i + m] += sig[:, :m] * gain
        self.send[:, i:i + m] += sig[:, :m] * gain * send

    def render(self, ir=None, wet=1.0):
        out = self.dry.copy()
        if ir is not None:
            out += convolve(self.send, ir)[:, : self.n] * wet
        out = np.tanh(out * 1.1) / 1.1  # gentle glue
        return out
