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


# =====================================================================================================
# Production additions (used by f2/prod/score.py). Everything above is unchanged. The functions below
# never touch the module RNG: each takes an explicit seed, so a cue renders identically whatever order
# the score calls things in. They compute in float64; instruments return float32 like the rest.
# =====================================================================================================
from scipy.signal import resample_poly  # noqa: E402


def undb(d):
    """dB -> linear amplitude (scalar or array)."""
    return 10.0 ** (np.asarray(d, dtype=np.float64) / 20.0)


def to_db(x, floor=1e-12):
    return 20.0 * np.log10(np.maximum(np.abs(np.asarray(x, dtype=np.float64)), floor))


def rms(x):
    x = np.asarray(x, np.float64)
    return float(np.sqrt(np.mean(x * x))) if x.size else 0.0


def ramp_in(n):
    """Raised-cosine fade-in of n samples, (0, 1]: the first sample is already non-zero."""
    i = np.arange(1, n + 1, dtype=np.float64)
    return np.sin(0.5 * np.pi * i / n) ** 2


def ramp_out(n):
    """Raised-cosine fade-out of n samples, [1, 0): the sample right after it is the first exact zero."""
    i = np.arange(n, dtype=np.float64)
    return np.cos(0.5 * np.pi * i / n) ** 2


def filt(x, kind, f, order=2):
    """float64 Butterworth along the last axis. kind: 'low' | 'high' | 'band' (f = (lo, hi))."""
    x = np.asarray(x, np.float64)
    if kind == 'band':
        sos = butter(order, [max(f[0], 5.0), min(f[1], SR * 0.495)], 'band', fs=SR, output='sos')
    elif kind == 'low':
        sos = butter(order, min(f, SR * 0.495), 'low', fs=SR, output='sos')
    else:
        sos = butter(order, max(f, 5.0), 'high', fs=SR, output='sos')
    return sosfilt(sos, x, axis=-1)


def _rbj(kind, f0, gain_db, q=0.7071):
    A = 10.0 ** (gain_db / 40.0)
    w0 = 2 * np.pi * f0 / SR
    cw, sw = np.cos(w0), np.sin(w0)
    al = sw / (2 * q)
    sa = 2 * np.sqrt(A) * al
    if kind == 'highshelf':
        b = [A * ((A + 1) + (A - 1) * cw + sa), -2 * A * ((A - 1) + (A + 1) * cw), A * ((A + 1) + (A - 1) * cw - sa)]
        a = [(A + 1) - (A - 1) * cw + sa, 2 * ((A - 1) - (A + 1) * cw), (A + 1) - (A - 1) * cw - sa]
    elif kind == 'lowshelf':
        b = [A * ((A + 1) - (A - 1) * cw + sa), 2 * A * ((A - 1) - (A + 1) * cw), A * ((A + 1) - (A - 1) * cw - sa)]
        a = [(A + 1) + (A - 1) * cw + sa, -2 * ((A - 1) + (A + 1) * cw), (A + 1) + (A - 1) * cw - sa]
    else:  # 'peak'
        b = [1 + al * A, -2 * cw, 1 - al * A]
        a = [1 + al / A, -2 * cw, 1 - al / A]
    return np.array([[b[0] / a[0], b[1] / a[0], b[2] / a[0], 1.0, a[1] / a[0], a[2] / a[0]]])


def eq(x, kind, f0, gain_db, q=0.7071):
    """RBJ-cookbook biquad. kind: 'highshelf' | 'lowshelf' | 'peak'."""
    return sosfilt(_rbj(kind, f0, gain_db, q), np.asarray(x, np.float64), axis=-1)


def tv_lowpass(x, fc, block=128, order=2):
    """Butterworth low-pass whose cutoff follows fc (Hz; scalar or one value per sample). Coefficients
    are recomputed every `block` samples and the filter state is carried across (smooth for slow sweeps)."""
    x = np.asarray(x, np.float64)
    n = x.shape[-1]
    fc = np.broadcast_to(np.asarray(fc, np.float64), (n,))
    out = np.empty_like(x)
    zi, cache = None, {}
    for a in range(0, n, block):
        b = min(n, a + block)
        key = round(float(fc[(a + b - 1) // 2]), 1)
        sos = cache.get(key)
        if sos is None:
            sos = cache[key] = butter(order, min(key, SR * 0.495), 'low', fs=SR, output='sos')
        if zi is None:
            zi = np.zeros((sos.shape[0],) + x.shape[:-1] + (2,))
        out[..., a:b], zi = sosfilt(sos, x[..., a:b], axis=-1, zi=zi)
    return out


def pink_noise(n, seed=0, channels=1):
    """Unit-RMS pink (1/f power) noise with DC removed, from its own seed. Shape (n,) or (channels, n)."""
    r = np.random.default_rng(seed)
    spec = np.fft.rfft(r.standard_normal((channels, n)), axis=-1)
    f = np.fft.rfftfreq(n, 1.0 / SR)
    spec[:, 0] = 0.0
    spec[:, 1:] /= np.sqrt(f[1:])
    p = np.fft.irfft(spec, n=n, axis=-1)
    p /= np.sqrt(np.mean(p * p, axis=-1, keepdims=True))
    return p[0] if channels == 1 else p


def true_peak_db(x, os=4):
    """True peak (dBTP) from os-times oversampling with scipy.signal.resample_poly."""
    up = resample_poly(np.atleast_2d(np.asarray(x, np.float64)), os, 1, axis=-1)
    return float(to_db(np.abs(up).max()))


# ---------------------------------------------------------------- struck coin (real small metal disc)
COIN_MODES = ((1.000, 1.00, 0.90), (1.594, 0.62, 0.70), (2.136, 0.48, 0.55),
              (2.653, 0.34, 0.45), (3.156, 0.24, 0.35), (4.060, 0.14, 0.25))  # (ratio, amp, decay s)


def coin_strike(freq, tau=1.0, excite='tick', seed=0, coin=16, dur=None, settle=0.004,
                click_db=-12.0, focus=1.0, beat=1.0):
    """A struck small metal disc after coin_ping's mode table (ratios 1/1.594/2.136/2.653/3.156/4.06,
    decays 0.9/0.7/0.55/0.45/0.35/0.25 s, all x tau, 0.4 % pitch settle). Every mode is a slightly split
    doublet (a real coin is never perfectly round, so each mode beats slowly), and the strike is a short
    excitation convolved with the modal response, so each hit colours the modes a little differently.
      excite: 'tick' 1.5 ms hard-contact noise burst | 'flick' 4 ms finger-nail burst (rounded) |
              'soft' Gaussian mallet (sigma 0.08 ms, no noise): rounded highs, used for glassy pings.
      coin:   seeds the disc's fixed physics (doublet splits, mode damping), shared by every hit of it.
      focus:  >1 concentrates energy in the fundamental (glassier); click_db: contact click re peak.
    Returns mono float32 at unit peak; the excitation starts on sample 0."""
    rng = np.random.default_rng(seed)
    crng = np.random.default_rng(7919 + int(coin))
    taus = np.array([m[2] for m in COIN_MODES]) * tau
    if dur is None:
        dur = 6.0 * taus.max() + 0.03
    n = secs(dur)
    t = np.arange(n) / SR
    warp = np.cumsum(1.0 + settle * np.exp(-t / 0.05)) / SR  # time-warp carrying the pitch settle
    y = np.zeros(n)
    for (r, a0, _), tk in zip(COIN_MODES, taus):
        f = freq * r
        split = crng.uniform(0.0006, 0.0024) * beat
        tpair = tk * crng.uniform(0.88, 1.12, 2)
        if f * (1 + split) > 0.45 * SR:
            continue
        bal = rng.uniform(0.25, 0.75)
        a = a0 ** focus * rng.uniform(0.8, 1.2)
        for s, w, tt in ((-0.5, bal, tpair[0]), (0.5, 1.0 - bal, tpair[1])):
            y += a * w * np.sin(2 * np.pi * f * (1 + s * split) * warp + rng.uniform(0, 2 * np.pi)) * np.exp(-t / tt)
    if excite == 'soft':
        L = 32
        i = np.arange(L) - L / 2
        burst = np.exp(-0.5 * (i / (0.00008 * SR)) ** 2)
    else:
        L = secs(0.004 if excite == 'flick' else 0.0015)
        burst = rng.standard_normal(L) * np.hanning(L + 2)[1:-1]
        if excite == 'flick':
            burst = filt(burst, 'low', 6500)
    burst = burst / np.sqrt(np.sum(burst ** 2))
    y = fftconvolve(y, burst)[:n]
    if click_db is not None and excite != 'soft':
        c = np.zeros(min(n, L + secs(0.003)))
        c[:L] = burst
        c = filt(c, 'high', 2500)
        y[:c.size] += c / (np.abs(c).max() + 1e-12) * np.abs(y).max() * undb(click_db)
    nf = min(n, secs(0.02))
    y[n - nf:] *= ramp_out(nf)
    return (y / (np.abs(y).max() + 1e-12)).astype(np.float32)


# ---------------------------------------------------------------- felt upright piano
_BODY_CACHE = {}


def piano_body(seed=1906):
    """Stereo soundboard + cabinet response of one small upright heard by two close mics. A shared
    (coherent) set of ~140 dense wooden modes 70 Hz - 3.2 kHz (5-25 ms decays) plus two cabinet modes,
    identical in both mics, so the lows stay in phase (mono-safe); each mic adds its own decorrelated
    modal detail above 500 Hz only. Unit energy per channel. Cached: every note of the score goes
    through the same instrument."""
    if seed in _BODY_CACHE:
        return _BODY_CACHE[seed]
    r = np.random.default_rng(seed)
    n = secs(0.12)
    t = np.arange(n) / SR

    def modes(f, a, tau):
        ph = r.uniform(0, 2 * np.pi, f.size)
        x = np.zeros(n)
        for k in range(f.size):
            x += a[k] * np.sin(2 * np.pi * f[k] * t + ph[k]) * np.exp(-t / tau[k])
        return x

    f = np.concatenate([np.sort(r.uniform(70.0, 3200.0, 140)), [104.0, 231.0]])
    a = (f / 400.0) ** -0.2 * r.uniform(0.35, 1.0, f.size)
    a[-2:] = [0.9, 0.7]
    tau = r.uniform(0.005, 0.025, f.size)
    tau[-2:] = [0.028, 0.022]
    common = modes(f, a, tau)
    common /= np.sqrt(np.sum(common ** 2))
    out = np.zeros((2, n))
    for ch in range(2):
        fs_ = np.sort(r.uniform(500.0, 4000.0, 100))
        side = filt(modes(fs_, r.uniform(0.3, 1.0, fs_.size), r.uniform(0.004, 0.018, fs_.size)), 'high', 500.0)
        out[ch] = common + 1.0 * side / np.sqrt(np.sum(side ** 2))
        out[ch] /= np.sqrt(np.sum(out[ch] ** 2))
    _BODY_CACHE[seed] = out
    return out


def felt_upright(freq, dur=5.0, vel=0.6, bright=0.4, decay=1.0, seed=0, body=0.35, mech_db=-21.0):
    """One note of a soft felt upright recorded close (stereo float32, unit peak). Physically informed:
      - 1-3 unison strings (by register), detuned 0.35-0.9 cents, starting in phase -> slow beating;
      - stiff-string partials f_k = k f sqrt((1 + B k^2)/(1 + B)) (fundamental exactly at freq),
        B rising ~1 octave per octave from 1.3e-4 at D2 (an upright's short strings);
      - felt hammer = soft low-pass (corner rises with vel and bright), strike point 1/8.3 of the string,
        weak soundboard radiation of the lowest fundamentals;
      - two-stage decay per partial (prompt sound, then a slower aftersound ~ -15 dB), highs die faster;
      - felt contact grows over 3-10 ms; the action is audible: a low key/hammer thock + a felt puff;
      - everything passes through the same stereo soundboard/cabinet response (piano_body).
    `decay` scales the decay times (1.5 for the long D2)."""
    rng = np.random.default_rng(seed)
    n = secs(dur)
    t = np.arange(n) / SR
    midi = 69 + 12 * np.log2(freq / 440.0)
    B = float(np.clip(1.3e-4 * 2 ** ((midi - 38) / 12.0), 1e-4, 3e-3))
    nstr = 1 if freq < 50 else (2 if freq < 120 else 3)
    sp = rng.uniform(0.35, 0.9)
    offs = {1: [0.0], 2: [-sp / 2, sp / 2],
            3: [-sp, rng.uniform(-0.15, 0.15) * sp, sp * rng.uniform(0.7, 1.0)]}[nstr]
    samp = rng.uniform(0.85, 1.0, nstr)
    fc = (420.0 + 1000.0 * bright) * (0.5 + 0.8 * vel) * (freq / 220.0) ** 0.25
    x0 = 1 / 8.3
    tp1 = 2.1 * (147.0 / freq) ** 0.55 * decay
    y = np.zeros(n)
    for k in range(1, 49):
        fk = k * freq * np.sqrt((1 + B * k * k) / (1 + B))
        if fk > 9000:
            break
        a = abs(np.sin(k * np.pi * x0)) ** 0.8 * k ** -0.5 / (1 + (fk / fc) ** 2) ** 1.25
        a *= (fk / 70.0) ** 2 / (1 + (fk / 70.0) ** 2)
        if a < 2e-4:
            continue
        tp = tp1 / (1 + 0.18 * (k - 1)) / (1 + (fk / 3200.0) ** 1.5)
        ta = tp * rng.uniform(2.8, 3.6)
        w = rng.uniform(0.14, 0.22)
        env = (1 - w) * np.exp(-t / tp) + w * np.exp(-t / ta)
        ph = rng.uniform(-0.3, 0.3)
        part = np.zeros(n)
        for c, sa in zip(offs, samp):
            fs_ = fk * 2 ** ((c + rng.normal(0, 0.04)) / 1200)
            part += sa * np.sin(2 * np.pi * fs_ * t + ph + rng.normal(0, 0.2))
        y += a * env * part / nstr
    na = secs(0.003 + 0.007 * (1 - vel))
    y[:na] *= ramp_in(na)
    pk = np.abs(y).max()
    m = min(n, secs(0.09))
    tm = np.arange(m) / SR
    nz = rng.standard_normal((2, m))
    thock = filt(nz[0], 'band', (35, 240)) * (1 - np.exp(-tm / 0.0015)) * np.exp(-tm / 0.016)
    puff = filt(nz[1], 'band', (450, 2600)) * (1 - np.exp(-tm / 0.0004)) * np.exp(-tm / 0.006)
    lvl = undb(mech_db + 8 * (vel - 0.5)) * pk
    y[:m] += thock / np.abs(thock).max() * lvl + puff / np.abs(puff).max() * lvl * undb(-9)
    bd = piano_body()
    out = np.empty((2, n))
    for ch in range(2):
        out[ch] = 0.85 * y + body * fftconvolve(y, bd[ch])[:n]
    nf = min(n, secs(0.35))
    out[:, n - nf:] *= ramp_out(nf)
    return (out / np.abs(out).max()).astype(np.float32)


# ---------------------------------------------------------------- pad and space
def pad_additive(freqs, dur, attack=0.9, release=0.0, partials=8, cents=3.0, lp_hz=3000.0,
                 width=0.4, seed=0, drift_db=0.7, side=0.3):
    """Additive pad: per note three voices at -cents / 0 / +cents, each 8 harmonics at 1/n^2 with random
    phases and its own slow amplitude drift; voices panned -width / 0 / +width (the shared centre voice
    keeps L/R positively correlated: mono-safe). The detuned side voices sit at `side` x the centre voice,
    so each partial shimmers (about +-4 dB at 0.3) instead of beating down to silence. Raised-cosine attack
    (and optional release), 2-pole low-pass. Stereo float32, unit peak."""
    r = np.random.default_rng(seed)
    n = secs(dur)
    t = np.arange(n) / SR
    st = np.zeros((2, n))
    for f in freqs:
        for c, p, g in ((-cents, -width, side), (0.0, 0.0, 1.0), (cents, width, side)):
            fv = f * 2 ** (c / 1200)
            v = np.zeros(n)
            for k in range(1, partials + 1):
                if fv * k > 0.45 * SR:
                    break
                v += np.sin(2 * np.pi * fv * k * t + r.uniform(0, 2 * np.pi)) / k ** 2
            v *= undb(drift_db * np.sin(2 * np.pi * r.uniform(0.04, 0.11) * t + r.uniform(0, 2 * np.pi)))
            ang = (p + 1) * np.pi / 4
            st[0] += g * v * np.cos(ang)
            st[1] += g * v * np.sin(ang)
    st = filt(st, 'low', lp_hz)
    env = np.ones(n)
    na = secs(attack)
    env[:na] = ramp_in(na)
    nr = secs(release)
    if nr:
        env[n - nr:] *= ramp_out(nr)
    st *= env
    return (st / np.abs(st).max()).astype(np.float32)


def room_ir(rt60=2.2, predelay=0.012, damp=4500.0, seed=12, early=True):
    """Stereo room impulse response: decorrelated noise tails whose decay depends on frequency (below
    400 Hz rt60 x 1.15, mids rt60, above 4 kHz rt60 x 0.5), 2-pole damping at `damp`, a 20 ms diffuse
    build-up, five early reflections at 7/13/19/29/41 ms (-8...-18 dB) after the pre-delay.
    Unit energy per channel, so a return gain of g dB puts the wet g dB under a broadband send."""
    r = np.random.default_rng(seed)
    n = secs(rt60 * 1.15)
    t = np.arange(n) / SR
    pre = secs(predelay)
    ir = np.zeros((2, n + pre))
    for ch in range(2):
        w = r.standard_normal(n)
        lo = filt(w, 'low', 400.0)
        hi = filt(w, 'high', 4000.0)
        mid = w - lo - hi
        tail = (lo * np.exp(-6.9078 * t / (rt60 * 1.15)) + mid * np.exp(-6.9078 * t / rt60)
                + hi * np.exp(-6.9078 * t / (rt60 * 0.5)))
        tail *= 1.0 - np.exp(-t / 0.02)
        if early:
            for dt, g in ((0.007, -8), (0.013, -10), (0.019, -12), (0.029, -14), (0.041, -18)):
                tail[secs(dt + r.uniform(-0.0012, 0.0012))] += r.choice([-1.0, 1.0]) * undb(g) * 30.0
        ir[ch, pre:] = filt(tail, 'low', damp)
    ir /= np.sqrt(np.sum(ir ** 2, axis=1, keepdims=True))
    return ir


def coin_strike_coherent(freq, tau=1.0, excite='tick', seed=0, coin=16, dur=None, settle=0.004,
                         click_db=-12.0, focus=1.0, beat=1.0):
    """coin_strike() with the physically right start for a struck disc: an impulse excites both members of
    each slightly split mode doublet in phase, so every doublet's slow beat starts from its maximum. (coin_strike
    draws the two members' phases independently, so a mode can be born half-cancelled: a router ping's
    fundamental could start 10+ dB down and leave its 1.594 mode to set the pitch.) Same mode table, decays,
    excitations, arguments and return convention as coin_strike: mono float32 at unit peak, excitation on
    sample 0."""
    rng = np.random.default_rng(seed)
    crng = np.random.default_rng(7919 + int(coin))
    taus = np.array([m[2] for m in COIN_MODES]) * tau
    if dur is None:
        dur = 6.0 * taus.max() + 0.03
    n = secs(dur)
    t = np.arange(n) / SR
    warp = np.cumsum(1.0 + settle * np.exp(-t / 0.05)) / SR
    y = np.zeros(n)
    for (r, a0, _), tk in zip(COIN_MODES, taus):
        f = freq * r
        split = crng.uniform(0.0006, 0.0024) * beat
        tpair = tk * crng.uniform(0.88, 1.12, 2)
        if f * (1 + split) > 0.45 * SR:
            continue
        bal = rng.uniform(0.25, 0.75)
        a = a0 ** focus * rng.uniform(0.8, 1.2)
        ph = rng.uniform(0, 2 * np.pi)                       # one phase per mode: both members start together
        for s, w, tt in ((-0.5, bal, tpair[0]), (0.5, 1.0 - bal, tpair[1])):
            y += a * w * np.sin(2 * np.pi * f * (1 + s * split) * warp + ph) * np.exp(-t / tt)
    if excite == 'soft':
        L = 32
        i = np.arange(L) - L / 2
        burst = np.exp(-0.5 * (i / (0.00008 * SR)) ** 2)
    else:
        L = secs(0.004 if excite == 'flick' else 0.0015)
        burst = rng.standard_normal(L) * np.hanning(L + 2)[1:-1]
        if excite == 'flick':
            burst = filt(burst, 'low', 6500)
    burst = burst / np.sqrt(np.sum(burst ** 2))
    y = fftconvolve(y, burst)[:n]
    if click_db is not None and excite != 'soft':
        c = np.zeros(min(n, L + secs(0.003)))
        c[:L] = burst
        c = filt(c, 'high', 2500)
        y[:c.size] += c / (np.abs(c).max() + 1e-12) * np.abs(y).max() * undb(click_db)
    nf = min(n, secs(0.02))
    y[n - nf:] *= ramp_out(nf)
    return (y / (np.abs(y).max() + 1e-12)).astype(np.float32)
