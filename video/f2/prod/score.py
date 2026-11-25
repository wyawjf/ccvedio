#!/usr/bin/env python3
"""第十二张 · THE TWELFTH PLATE — the score (DESIGN_BIBLE §8 + §11, re-timed by f2/prod/CUES_v2.md; QA §10 "Sound").

    cd /home/user/ccvedio/video && python3 -I f2/prod/score.py

Synthesizes every instrument of §8.1 (nothing sampled), places every cue of the §8.2 cue sheet AS RE-TIMED BY
f2/prod/CUES_v2.md (the picture was re-timed after the design review, §11; wherever the two differ CUES_v2 wins,
and the router landings are imported from geom.LANDS) so that each cue starts on sample round(f * 1600), mixes
and masters per §8.3, then measures the written file and reports:

    build/f2/score.wav            48 kHz / 24-bit PCM stereo, exactly 1796 * 1600 = 2,873,600 samples
    build/f2/score_cues.json      every placed event: {frame, sample, cue, gain_dbfs, pan}
    build/f2/score_report.json    LUFS, true peak, zero window, D5 at f1604, f1187 absence, correlation, sample lock,
                                  and 'review_acceptance': every acceptance test of the independent review
    build/f2/score_spec.png       spectrogram of the whole score
    build/f2/score_hook_spec.png  0-4 s zoom (the coin settles at f44)

Level convention (review fix 11). Every level in this file and in score_cues.json is a MIX-BUS level, as §8.1/§8.2
give them: RMS where the bible says RMS (ROOM, WHIRR, DRONE, SLIT, PAD, and the BLOOMs, levelled like their sibling
noise sweep the SLIT, review fix 6), sample peak otherwise. The cue sheet as written integrates to about -28 LUFS, so
§8.2 and §8.3 (-16 LUFS) cannot both hold at one scale: the master is ONE uniform gain (about +12 dB, reported as
master_gain_db) and nothing else. No limiter acts: render() moves the hook group (flick, whirr, rattle, CLACK and
their room, in the cue sheet's own balance) as one so the CLACK lands at CLACK_DBTP (-1.40 dBTP) and levels the plunge
SUB to SUB_DBTP just under it; every other peak of the film sits below both. score_report.json shows
limiter_clusters == [] and file_equals_gain_times_mix_bus. DESIGN_BIBLE §8.3 should carry this convention; this
script may not edit the bible. Where a review fix had to differ from its prescription to pass the review's own
acceptance test, score_report.json 'review_fixes' says what was measured and what was changed.

The hard stop (§1 move 2): every event that starts before f764 is cut at sample 1,222,400 (2 ms de-click fade
ending there), the pre-stop reverb returns are cut the same way and never resume, and nothing post-stop starts
before f776. The master is a per-sample gain, so the zeros stay exact. Deterministic: every sound has a fixed seed.
"""
import json
import os
import sys
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
F2 = os.path.dirname(HERE)
ROOT = os.path.dirname(F2)
for _p in (F2, HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np  # noqa: E402
import pyloudnorm as pyln  # noqa: E402
import soundfile as sf  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402
from scipy.ndimage import maximum_filter1d  # noqa: E402
from scipy.signal import butter, fftconvolve, lfilter, resample_poly, sosfilt, welch  # noqa: E402

import synth as S  # noqa: E402
from synth import (SR, secs, undb, to_db, ramp_in, ramp_out, filt, eq, tv_lowpass, pink_noise,  # noqa: E402
                   coin_strike, coin_strike_coherent, felt_upright, pad_additive, room_ir)
from geom import LANDS, CELLS, RETINA_FRAME, sheet_tf  # noqa: E402  (the picture's own timing, §11)

OUT = os.path.join(ROOT, 'build', 'f2')
FPS, SPF, NF = 30, 1600, 1796                # one beat added after review (DESIGN_BIBLE §11)
N = NF * SPF                                  # 2,873,600 samples = 59.8667 s
S764, S776 = 764 * SPF, 776 * SPF             # exact zeros on [1,222,400, 1,241,600)
DECLICK = secs(0.002)                         # 96 samples
T_CLACK = 44 / FPS                            # 1.4667 s, the hook
LUFS_TARGET, TP_CEIL = -16.0, -1.25           # §8.3 (-1.0 dBTP spec; 0.25 dB margin)
RET_MUSIC, RET_COIN = -14.0 + 10.46, -18.0 + 10.46   # returns for a 0.3 send: wet -14 dB (piano) / -18 dB (coin)

# ---------------------------------------------------------------- the picture's timing (f2/prod/CUES_v2.md)
assert len(LANDS) == 12
F_SLIT2 = 300                                  # a second, lighter SLIT swell (the slit outgrows the print f300-f318)
F_DRAW = (950, 966)                            # the retina frame draws (E-DRAW)
F_STAMPS = (968, 992, 1016)                    # 身份 / 记录 / 权限
SHEET = (                                      # arrival order, as chords: (frame, ((cell, Hz, name), ...))
    (1136, ((5, 349.23, 'F4'),)),
    (1140, ((2, 440.00, 'A4'), (8, 523.25, 'C5'))),
    (1146, ((4, 233.08, 'Bb3'), (6, 523.25, 'C5'))),
    (1156, ((1, 293.66, 'D4'), (3, 659.26, 'E5'), (7, 349.23, 'F4'), (9, 783.99, 'G5'))),
    (1171, ((11, 392.00, 'G4'),)),
    (1179, ((10, 261.63, 'C4'),)))
F_NO_NOTE = 1187                               # the withheld 12th (unchanged)
F_DRONE_OUT = (1568, 1580)                     # DRONE fades out over 12 f
F_RELAY, F_LIGHT = 1580, 1581                  # the click one frame before the light; HUM + PAD from the light
F_D5 = 1604                                    # the raking light's relief peaks: the withheld 12th note
F_TING = 1700                                  # account mark (B69)
F_HOLD = (1712, 1795)                          # complete card: everything but the room fades to the room

# ---------------------------------------------------------------- mix decisions (independent review, fixes 1-11)
CLACK_DBTP = -1.40          # 1/11: the hook group moves as one so the CLACK is the file's peak at -1.40 dBTP (no limiter)
FLICK_DAMP = 0.15           # 1: the table's contact damping of the flick's ring from f2, exp(-(t - t2)/0.15)
SUB_DBTP = CLACK_DBTP - 0.1   # 1/11: the plunge SUB lands with the CLACK (render() levels it); nothing else reaches them
CLACK_RING_DB = -4.0        # 1: the CLACK's D7 tau x1.5 ring re its bursts (was -16; the review's -8 left the CLACK quieter than the flick)
CLACK_THUMP = (2.0, 0.030)  # 1: the 120 Hz table sine for its full 40 ms, dB re the bursts and decay (s): the table takes the weight
FLICK_LP = 5000.0           # 7: flick low-passed at 5 kHz, 4th order
HOOK_LP = 7500.0            # 7: rattle and CLACK end in a 4th-order low-pass at 7.5 kHz (no 9 kHz shelf)
WHIRR_LP = (7000.0, 8)      # 7: the whirr (most of the hook's energy) ends in an 8th-order low-pass at 7 kHz
WHIRR_DB = -30.0            # §8.1: WHIRR -30 dBFS RMS
WHIRR_TAIL = 0.25           # s: the whirr's body ends at f15 and releases over 0.25 s into the rattle (its AM is at the
#                             rattle's own 9 Hz there), so the rolling hands over to the wobble without an 11 dB step
RATTLE_BED_DB = (-54.0, -44.0)   # 5: rattle bed RMS, its pulses driven by the ticks' own times; every tick >= 6 dB over it (3-7 kHz)
PING_FOCUS, PING_BEAT = 3.0, 0.2   # 9: soft mallet, tau x0.6, beat 0.2, doublets struck in phase, focus 3 (2.0 left 7 dB)
PING_DENSE_DB = -2.0        # CUES_v2 accelerando: a call landing 6 f after the last is played 2 dB lighter (the rings pile up)
SLIT_CREST_DB = 8.0         # SLIT noise: spikes above 8 dB over its local RMS are soft-saturated (inaudible on noise)
SLIT2_DB = -6.0             # CUES_v2: the f300 swell sits about 6 dB under the f260 one
DRONE_DIP = (1187, 1188, 1205, 1211)            # f1187: down in 1 f, at -6 dB for 18 f (to f1205), back by f1211
DRONE_NOTCHES = ((183.55, -15.0), (367.10, -15.0), (734.20, -15.0), (256.97, -10.0), (513.94, -10.0))  # 10: (Hz, dB), Q 12
SUB_LAYER = dict(swell=-12.0, plunge=-3.0)      # 8: saturated harmonic layer re the sub's peak (dB)
SUB_SERIES = (0.7, 0.5, 1.5)    # 8: layer = 2nd-10th harmonics of the glide: 2nd/3rd weight, k^-slope, tanh drive
BLOOM_TRIM = {116: 0.0, 380: 0.0, 644: 0.0, 1124: 0.0}   # 6: dB over the cue sheet's -34 / -36 dBFS RMS (loudest 100 ms)
SHEET_DB = (-30.0, -28.7, -27.3, -26.0, -27.0, -28.0)   # 3: one note, dBFS peak, per arrival (was -24 -> -20): -30 -> -26
#                             into the four-note chord, then the last two cells arrive softer and the 12th is withheld
CHORD_LAW = 7.5             # 3: a k-note chord's notes sit CHORD_LAW * log10(k) dB under a single note
PAD_DMAJ_DB = -27.0         # 2: PAD D major add9 dBFS RMS (§8.1 -24: the ending was the film's loudest passage, D5 under it)
PAD_E5_DB = -10.0           # 2: the add9 E5 re one chord tone of the S08 pad (review -8: its line still topped the D5's by f1644)
PAD_RIDE = (1598, 1606, 1614, 1652, -4.0)       # 2: one move: down f1598-f1606, held, back up f1614-f1652 (dB)
D5_DB, D5_DECAY, D5_SEED = -17.0, 2.4, 16280    # the withheld note: -17 dBFS (§8.2 -18), rings (decay x2.4); this take's
#                                                 three unison strings do not beat down to a null while exposed


def smp(frame):
    """Frame -> first sample of that frame (§8.2: sample = round(f * 1600))."""
    return int(round(frame * SPF))


# ---------------------------------------------------------------- easing (§6.1) and small helpers
def bezier(x1, y1, x2, y2):
    """CSS cubic-bezier as a vectorised function of progress u in 0..1."""
    def f(u):
        u = np.clip(np.asarray(u, np.float64), 0.0, 1.0)
        lo, hi = np.zeros_like(u), np.ones_like(u)
        for _ in range(48):
            s = 0.5 * (lo + hi)
            xs = 3 * (1 - s) ** 2 * s * x1 + 3 * (1 - s) * s ** 2 * x2 + s ** 3
            lo, hi = np.where(xs < u, s, lo), np.where(xs < u, hi, s)
        s = 0.5 * (lo + hi)
        return 3 * (1 - s) ** 2 * s * y1 + 3 * (1 - s) * s ** 2 * y2 + s ** 3
    return f


E_SNAP, E_DRAW = bezier(.7, 0, .2, 1), bezier(.45, 0, .2, 1)


def pan_mono(x, p):
    a = (np.asarray(p, np.float64) + 1) * np.pi / 4
    x = np.asarray(x, np.float64)
    return np.stack([x * np.cos(a), x * np.sin(a)])


def balance(st, p):
    """Equal-power balance for a stereo source (unity at p = 0)."""
    a = (p + 1) * np.pi / 4
    return np.asarray(st, np.float64) * np.array([[np.cos(a)], [np.sin(a)]]) * np.sqrt(2)


def peak(x):
    return float(np.abs(x).max())


def at_peak(x, db):
    return np.asarray(x, np.float64) * (undb(db) / peak(x))


def power(x):
    x = np.asarray(x, np.float64)
    return (x * x).mean(axis=0) if x.ndim == 2 else x * x


def st_rms_max(x, win=0.05):
    """Max short-term RMS (per-channel mean power, `win` s windows)."""
    h = secs(win)
    c = np.concatenate([[0.0], np.cumsum(power(x))])
    return float(np.sqrt(((c[h:] - c[:-h]) / h).max()))


def at_strms(x, db, win=0.05):
    return np.asarray(x, np.float64) * (undb(db) / st_rms_max(x, win))


def rms_of(x, a=None, b=None):
    return float(np.sqrt(power(np.asarray(x)[..., a:b]).mean()))


def moving_mean(x, h):
    """Centred moving average over h samples (cumulative sums; the window shrinks at the edges)."""
    x = np.asarray(x, np.float64)
    c = np.concatenate([[0.0], np.cumsum(x)])
    i = np.arange(x.size)
    lo, hi = np.clip(i - h // 2, 0, x.size), np.clip(i - h // 2 + h, 0, x.size)
    return (c[hi] - c[lo]) / (hi - lo)


def pitch_pan(freq):
    """A close pair on an upright, player's side: bass a little left, treble a little right."""
    midi = 69 + 12 * np.log2(freq / 440.0)
    return float(np.clip((midi - 60) / 30 * 0.35, -0.3, 0.3))


def x_pan(x):
    """§8.3 screen-x pan law: pan = (x - 540) / 540 * 0.6."""
    return (x - 540.0) / 540.0 * 0.6


def cell_pan(cell, frame):
    """A sheet note sits where its cell is on screen when it develops (geom.sheet_tf at that frame): the ripple
    spreads out from the eye in the stereo image as it does in the picture. (x - 540)/540 * 0.45, clipped."""
    cid, _, sw, sh, cs, x, y, _ = [c for c in CELLS if c[0] == cell][0]
    s, tx, ty = sheet_tf(frame)
    cx = tx + s * (x + 0.5 * sw * cs)
    return float(np.clip((cx - 540.0) / 540.0 * 0.45, -0.45, 0.45))


# ---------------------------------------------------------------- the mixer
class Score:
    """Stems on one frame-locked timeline. Events starting before f764 belong to segment A and are cut at
    f764; events from f776 on are segment B. Reverb sends are kept per segment, so the pre-stop tails can
    be cut and never come back."""

    def __init__(self):
        self.stems = {}
        self.send = {(b, s): np.zeros((2, N)) for b in ('music', 'coin', 'hook') for s in 'AB'}
        self.cues = []
        self.refs = []              # (frame, cue, first 200 ms of the placed event (mono), tag): placement check
        self.kept = {}              # tag -> (first sample, placed stereo signal): per-cue measurements
        self.onsets = []            # (frame, cue, first sample, offset of its first non-zero sample)

    def stem(self, name):
        if name not in self.stems:
            self.stems[name] = np.zeros((2, N))
        return self.stems[name]

    def log(self, frame, cue, gain_dbfs, pan=0.0):
        self.cues.append(dict(frame=int(frame), sample=smp(frame), cue=cue,
                              gain_dbfs=None if gain_dbfs is None else round(float(gain_dbfs), 2),
                              pan=round(float(pan), 3)))

    def place(self, stem, x, frame, cue, gain_dbfs, pan=0.0, send=None, log=True, free=False, tag=None):
        """x: stereo signal already at its mix-bus level. Its sample 0 lands on sample round(frame * 1600)."""
        s0 = smp(frame)
        if not free:
            assert not (S764 <= s0 < S776), f'{cue}: nothing may start inside the hard stop'
        x = np.asarray(x, np.float64)
        end = min(N, s0 + x.shape[1])
        x = x[:, :end - s0].copy()
        seg = 'A' if s0 < S764 else 'B'
        if seg == 'A' and not free and end >= S764:         # reaches the hard stop: cut there, never resumes
            cut = S764 - s0
            a = max(0, cut - DECLICK)
            x[:, a:cut] *= ramp_out(DECLICK)[DECLICK - (cut - a):]
            x[:, cut:] = 0.0
        self.stem(stem)[:, s0:end] += x
        for bus, amt in (send or {}).items():
            self.send[(bus, seg)][:, s0:end] += x * amt
        if tag is not None:
            self.kept[tag] = (s0, x)
        if log:
            self.log(frame, cue, gain_dbfs, pan)
            if not free:
                self.refs.append((int(frame), cue, 0.5 * (x[0, :secs(0.2)] + x[1, :secs(0.2)]), tag))
                nz = np.flatnonzero(np.any(x != 0, axis=0))
                self.onsets.append((int(frame), cue, s0, int(nz[0]) if nz.size else None))

    def reverb_returns(self):
        """The hook (f1-f53) has its own send into the same 1.0 s coin room, so render() can level it (dry + wet)."""
        irs = {'music': room_ir(2.2, 0.012, 4500.0, seed=22), 'coin': room_ir(1.0, 0.012, 4500.0, seed=10)}
        irs['hook'] = irs['coin']
        gains = {'music': undb(RET_MUSIC), 'coin': undb(RET_COIN), 'hook': undb(RET_COIN)}
        out = {}
        for bus in ('music', 'coin', 'hook'):
            ret = np.zeros((2, N))
            for seg in 'AB':
                snd = filt(self.send[(bus, seg)], 'high', 120.0)
                if not np.any(snd):
                    continue
                w = np.stack([fftconvolve(snd[c], irs[bus][c])[:N] for c in range(2)])
                if seg == 'A':
                    w[:, S764 - DECLICK:S764] *= ramp_out(DECLICK)
                    w[:, S764:] = 0.0
                else:
                    w[:, :S776] = 0.0
                ret += w
            out[bus] = ret * gains[bus]
        return out


# ---------------------------------------------------------------- instruments built on synth.py (§8.1)
def room_bed():
    """ROOM: pink noise BP 60 Hz-6 kHz, two noises at 0.7 correlation, -46 dBFS RMS, +-1.5 dB wander at
    0.05 Hz. Level automation per §8.2: f0 fade-in 0.25 s; cut at f764; back at f776 at -50 (2 ms fade);
    -52 inside the plate (f1428); back to -46 once the light table is on (f1581, over the pull-out to f1628);
    ends at f1796."""
    a, b = pink_noise(N, seed=11, channels=2)
    st = filt(np.stack([a, 0.7 * a + np.sqrt(1 - 0.49) * b]), 'band', (60.0, 6000.0))
    st /= np.sqrt((st * st).mean(axis=1, keepdims=True))
    t = np.arange(N) / SR
    k = [(0, -46.0), (S764, -46.0), (S776, -50.0), (smp(1428), -50.0), (smp(1428) + secs(0.03), -52.0),
         (smp(F_LIGHT), -52.0), (smp(1628), -46.0), (N, -46.0)]
    lvl = np.interp(np.arange(N), [p for p, _ in k], [v for _, v in k])
    g = undb(lvl + 1.5 * np.sin(2 * np.pi * 0.05 * t + 0.9))
    n0 = secs(0.25)
    g[:n0] *= ramp_in(n0)
    g[S764 - DECLICK:S764] *= ramp_out(DECLICK)
    g[S764:S776] = 0.0
    g[S776:S776 + DECLICK] *= ramp_in(DECLICK)
    ne = secs(0.02)
    g[N - ne:] *= ramp_out(ne)
    return st * g


def spin_rate(t):
    """Rotation / contact rate of the settling coin (Hz) at film time t: the WHIRR spins down 14 -> 9 Hz
    over f2-f15, then the RATTLE follows Euler's disk, Omega = 9 Hz * ((T - 0.5)/(T - t))^(1/3), capped
    at 32 Hz, T = the clack (f44)."""
    t = np.asarray(t, np.float64)
    whirr = 14.0 * (9.0 / 14.0) ** np.clip((t - 2 / FPS) / (13 / FPS), 0, 1)
    om = np.minimum(32.0, 9.0 * ((T_CLACK - 0.5) / np.maximum(T_CLACK - t, 1e-6)) ** (1 / 3))
    return np.where(t < 0.5, whirr, om)


def coin_flick():
    """f1: the coin is flicked into a spin (D7, 4 ms finger-nail excitation, -14 dBFS strike). From f2 it spins
    on its rim on the table, and the table contact damps the ring, exp(-(t - t2)/0.15) (25 dB down by f15), so the
    flick never out-rings the hook: the CLACK's own D7 ring is the one left hanging at f44 (review fix 1). While it
    rings it is swept by the rotating radiation pattern (gentle AM at the spin rate). 4th-order low-pass at
    5 kHz (fix 7): the 1 / 1.594 modes stay, the upper modes soften."""
    y = coin_strike(2349.3, tau=1.0, excite='flick', seed=101, coin=16, click_db=-10.0).astype(np.float64)
    t = 1 / FPS + np.arange(y.size) / SR
    ph = 2 * np.pi * np.cumsum(spin_rate(np.minimum(t, T_CLACK))) / SR
    depth = 0.28 * np.clip((t - 2 / FPS) / 0.02, 0, 1)
    y *= 1 - depth * (0.5 - 0.5 * np.cos(ph))
    y *= np.exp(-np.maximum(t - 2 / FPS, 0.0) / FLICK_DAMP)
    y = filt(y, 'low', FLICK_LP, order=4)
    land = int(round((T_CLACK - 1 / FPS) * SR))
    y[land - secs(0.006):land] *= ramp_out(secs(0.006))
    y[land:] = 0.0
    return y


def whirr():
    """f2-f15: rolling rim on the table. BP noise 4-8 kHz (4th order) coloured by the coin's own modes, AM at the
    spin rate 14 -> 9 Hz, a faint table rumble at the same rate, 8th-order low-pass at 7 kHz (fix 7: the band's upper
    skirt was most of the hook's energy above 8 kHz; a 4th-order 7.5 kHz low-pass still left it at -21 dB); -30 dBFS RMS.
    Its body ends at f15; it releases over WHIRR_TAIL s into the rattle."""
    n = smp(15) - smp(2) + secs(WHIRR_TAIL)
    r = np.random.default_rng(202)
    t = 2 / FPS + np.arange(n) / SR
    ph = 2 * np.pi * np.cumsum(spin_rate(np.minimum(t, 0.5 - 1e-6))) / SR
    am = 0.35 + 0.65 * (0.5 + 0.5 * np.cos(ph)) ** 1.5
    hiss = filt(r.standard_normal(n), 'band', (4000.0, 8000.0), order=4)
    ring = coin_strike(2349.3, tau=0.08, excite='tick', seed=203, coin=16, click_db=None)
    metal = filt(fftconvolve(r.standard_normal(n), ring)[:n], 'band', (3000.0, 8000.0), order=4)
    rumble = filt(r.standard_normal(n), 'band', (120.0, 400.0)) * (0.5 + 0.5 * np.cos(ph)) ** 4
    y = (hiss / S.rms(hiss) * 0.75 + metal / S.rms(metal) * 0.45 + rumble / S.rms(rumble) * 0.1) * am
    y = filt(y, 'low', WHIRR_LP[0], order=WHIRR_LP[1])
    na = secs(0.025)
    y[:na] *= ramp_in(na)
    nr = secs(WHIRR_TAIL)
    y[n - nr:] *= ramp_out(nr)
    return y


def rattle_ticks(seed=151):
    """Tick times (s) of the Euler-disk rattle (review fix 5). The contact rate is the bible's
    Omega(t) = 9 Hz * ((T - 0.5)/(T - t))^(1/3), capped at 32 Hz, T = the clack (f44); tick k sits where the
    integrated rate Phi(t) = int_0.5^t Omega dt reaches k cycles (so every interval is one true period), then
    moves by a uniform +-3 % of the local period. Phi(T) = 12.7 cycles: 13 ticks, the 13th about 22 ms before the
    clack. Tick 0 is exactly f15 (the cue's sample-locked start). Returns (times, ideal times)."""
    r = np.random.default_rng(seed)
    t = 0.5 + np.arange(smp(44) - smp(15) + 1) / SR
    w = spin_rate(t)
    phi = np.concatenate([[0.0], np.cumsum(0.5 * (w[1:] + w[:-1])) / SR])
    k = np.arange(int(np.floor(phi[-1])) + 1)
    base = np.interp(k, phi, t)
    times = base + r.uniform(-0.03, 0.03, k.size) / spin_rate(base)
    times[0] = 0.5
    return times, base


def env_3_7k(x):
    """3-7 kHz amplitude envelope (4th-order BP, rectified, 2 ms mean)."""
    b = filt(x, 'band', (3000.0, 7000.0), order=4)
    return np.convolve(np.abs(b), np.ones(secs(0.002)) / secs(0.002), 'same')


def rattle():
    """f15-f44: Euler's-disk tick train (rattle_ticks: integrated Omega(t), +-3 % jitter), each tick =
    1.5 ms noise BP 3-7 kHz (4th order, -18 dB) + COIN D7 tau x0.1 (-28 dB) + 180 Hz 'table' sine 8 ms
    (-26 dB); ticks -24 -> -18 dBFS; late ticks chatter (a micro-bounce). Under them a rolling bed (BP 2.5-7 kHz,
    4th order, -54 -> -44 dBFS RMS) whose pulses are driven by the same tick times (each contact sets the rim
    rolling again: no flam), the glue of the buzz, carrying the 32 Hz cap on after the last tick. 4th-order
    low-pass at 7.5 kHz. Returns (mono, tick times in s, stats: ideal times and the 3-7 kHz tick-over-bed margin)."""
    n = smp(44) - smp(15)
    r = np.random.default_rng(150)
    times, ideal = rattle_ticks()
    ticks = np.zeros(n)
    m = secs(0.012)
    tm = np.arange(secs(0.008)) / SR
    table = np.sin(2 * np.pi * 180.0 * tm) * (1 - np.exp(-tm / 0.0005)) * np.exp(-tm / 0.0025)
    table[-secs(0.002):] *= ramp_out(secs(0.002))
    table /= peak(table)
    for i, tt in enumerate(times):
        u = (tt - 0.5) / (T_CLACK - 0.5)
        L = secs(0.0015)
        burst = np.zeros(m)
        burst[:L] = r.standard_normal(L) * np.hanning(L + 2)[1:-1]
        burst = filt(burst, 'band', (3000.0, 7000.0), order=4)
        burst /= peak(burst)
        ring = coin_strike(2349.3, tau=0.1, excite='tick', seed=300 + i, coin=16, click_db=None).astype(np.float64)
        tick = np.zeros(ring.size)
        tick[:m] += undb(-18) * burst
        tick += undb(-28) * ring
        tick[:table.size] += undb(-26) * table
        if r.random() < 0.1 + 0.5 * u:                         # chatter as the wobble tightens
            j = secs(r.uniform(0.0015, 0.004))
            tick[j:j + m] += undb(-18 - r.uniform(8, 12)) * burst
        tick *= undb(-24 + 6 * u) / peak(tick)
        i0 = int(round((tt - 0.5) * SR))
        k = min(n - i0, tick.size)
        ticks[i0:i0 + k] += tick[:k]
    t = 0.5 + np.arange(n) / SR
    tk = np.concatenate([times, times[-1] + np.arange(1, 4) / 32.0])     # after the last tick: the 32 Hz cap
    cyc = np.interp(t, tk, np.arange(tk.size, dtype=np.float64))
    fr_ = cyc - np.floor(cyc)                                            # 0 on every tick
    swell = (1 - np.exp(-fr_ / 0.04)) * np.exp(-fr_ / 0.3) / 0.663      # each contact sets the rim rolling again
    u = (t - 0.5) / (T_CLACK - 0.5)
    bed = filt(r.standard_normal(n), 'band', (2500.0, 7000.0), order=4) * (0.2 + 0.8 * swell)
    lo, hi = RATTLE_BED_DB
    bed *= undb(lo + (hi - lo) * u) / S.rms(bed)
    na = secs(0.04)
    bed[:na] *= ramp_in(na)
    # 3-7 kHz: each tick's pulse vs the bed's strongest moment around it (half an interval either side)
    et, eb = env_3_7k(ticks), env_3_7k(bed)
    margins = []
    for k_, tt in enumerate(times):
        i0 = int(round((tt - 0.5) * SR))
        half = int(0.5 * SR / float(spin_rate(tt)))
        margins.append(float(to_db(et[i0:i0 + secs(0.008)].max()) - to_db(eb[max(0, i0 - half):i0 + half].max())))
    y = filt(ticks + bed, 'low', HOOK_LP, order=4)
    nr = secs(0.003)
    y[n - nr:] *= ramp_out(nr)                                # the coin lands: the rolling stops
    return y, times, dict(ideal=ideal, tick_over_bed_db=margins)


def clack():
    """f44: the coin lands flat (review fix 1). 3 ticks within 12 ms (bounces, BP 2-8 kHz 4th order) + 120 Hz table
    sine for its full 40 ms, 2 dB over the bursts with a 30 ms decay (the table takes the weight) + COIN D7 tau x1.5 at
    -4 dB (its ring is the tail heard f44-f53, the glint's sound), 4th-order low-pass at 7.5 kHz. Unit peak. (The review's
    0 dB / 25 ms / -8 dB left the CLACK's 50 ms RMS 1.2 dB over the flick's ring and its loudness under it.)"""
    r = np.random.default_rng(440)
    n = secs(5.0)
    y = np.zeros(n)
    L = secs(0.0015)
    for dt, g in ((0.0, 1.0), (0.0052, 0.5), (0.0110, 0.28)):
        burst = np.zeros(secs(0.01))
        burst[:L] = r.standard_normal(L) * np.hanning(L + 2)[1:-1]
        burst = filt(burst, 'band', (2000.0, 8000.0), order=4)
        i0 = secs(dt)
        y[i0:i0 + burst.size] += g * burst / peak(burst)
    tm = np.arange(secs(0.04)) / SR
    thump = np.sin(2 * np.pi * 120.0 * tm) * (1 - np.exp(-tm / 0.001)) * np.exp(-tm / CLACK_THUMP[1])
    thump[-secs(0.008):] *= ramp_out(secs(0.008))
    y[:thump.size] += undb(CLACK_THUMP[0]) * thump / peak(thump)
    ring = coin_strike(2349.3, tau=1.5, excite='tick', seed=441, coin=16, click_db=None).astype(np.float64)
    k = min(n, ring.size)
    y[:k] += undb(CLACK_RING_DB) * ring[:k]
    y = filt(y, 'low', HOOK_LP, order=4)
    y[n - secs(1.0):] *= ramp_out(secs(1.0))          # the ring dies away (about -32 dB by 5 s), never truncated
    return y / peak(y)


def drone_voices(dur, cutoff_curve=None, notches=True):
    """DRONE: synth.drone() voices on D1 36.71, D2 73.42 (+ a copy at +0.15 Hz) and A2 110.00, LFO 0.07 Hz
    +-2 dB. No unison detune: drone() starts its voices in phase, so detuned unisons would beat at full depth;
    coherent voices keep the bed steady and mono-stable. The movement is the bible's own: the +0.15 Hz D2 copy,
    the LFO, and the slow just-vs-tempered beats (A2 against D1's 3rd partial, 0.13 Hz). Low-pass 900 Hz,
    automatable. Each voice starts at a different point of its cycle (D2 = 2 x D1 exactly: coinciding saw edges
    would add 2.3 dB of crest factor). Review fix 10: the saws' 5th-harmonic family (F#3 183.55 / F#4 367.10 /
    F#5 734.20 Hz: a major third under everything) is notched -15 dB and the 7th harmonics (256.97 / 513.94 Hz: a
    flat C) -10 dB, Q 12, on both drone segments: the drone stays an open D-A fifth, the film's first F# stays the
    lamp-up PAD's, and nothing rubs against the F3/F4 and C5 felt notes."""
    v = {}
    n = secs(dur)
    for name, f, w, off in (('D1', 36.71, 0.6, 0), ('D2', 73.42, 1.0, 170), ('D2b', 73.57, 0.35, 245), ('A2', 110.0, 0.5, 380)):
        x = S.drone(f, dur + 0.01, voices=2, spread_cents=0, cutoff=23000, lfo=0.07).astype(np.float64)[:, off:off + n] * w
        fc = np.full(n, 900.0) if cutoff_curve is None else cutoff_curve(np.arange(n) / SR)
        x = filt(tv_lowpass(x, fc), 'high', 25.0)
        if notches:
            for f0, g in DRONE_NOTCHES:
                x = eq(x, 'peak', f0, g, 12.0)
        v[name] = x
    return v


def bloom(dur, level_db, seed, reverse=False):
    """BLOOM: whoosh(dur, 250 -> 1600 Hz, peak 0.6) on pink noise; reversed for the pull-back. Review fix 6: its
    level is the RMS of its loudest 100 ms (at_strms), like its sibling noise sweep the SLIT; as a sample peak
    (-34 dBFS peak is about -45 dBFS RMS) it sat under the drone and was masked in every band."""
    S.RNG = np.random.default_rng(seed)               # legacy noise() draws from the module RNG
    w = S.whoosh(dur, 250, 1600, peak=0.6, stereo=True).astype(np.float64)
    if reverse:
        w = w[:, ::-1].copy()
        w[:, :secs(0.03)] *= ramp_in(secs(0.03))
    else:
        w[:, -secs(0.08):] *= ramp_out(secs(0.08))
    return at_strms(filt(w, 'high', 120.0), level_db, 0.1)


def tame_crest(x, crest_db, win=0.05):
    """Soft-saturate a noise cue's rare waveform spikes above crest_db over its own local RMS (per channel,
    50 ms): y = c tanh(x / c), c = local RMS x crest. Gaussian noise throws an occasional 4-5 sigma spike that is
    no part of the sound but sets its true peak; this keeps the master a pure gain. Inaudible on noise."""
    x = np.asarray(x, np.float64)
    r = np.sqrt(np.stack([moving_mean(ch * ch, secs(win)) for ch in np.atleast_2d(x)])).reshape(x.shape) + 1e-12
    c = r * undb(crest_db)
    return c * np.tanh(x / c)


def slit(dur, f0, f1, level_db, seed):
    """SLIT: band-pass noise sweeping f0 -> f1 over the slit's move (`dur` s), envelope = the slit's opening
    speed (derivative of E-SNAP), level = RMS of its loudest 100 ms, placed at the slit (x 848). f260: 300 ->
    1800 Hz over 0.9 s at -28 dBFS (§8.1); f300 (CUES_v2): the slit outgrows the print, a lighter second swell,
    600 -> 2400 Hz over 0.6 s, about 6 dB under."""
    n = secs(dur)
    p = pink_noise(n, seed=seed, channels=2)
    x = np.stack([p[0], 0.6 * p[0] + 0.8 * p[1]]).astype(np.float32)
    y = S.sweep_bp(x, f0, f1, q=2.5, steps=48).astype(np.float64)
    u = np.arange(n) / n
    v = np.gradient(E_SNAP(u))
    y *= (v / v.max()) ** 0.8
    y = tame_crest(y, SLIT_CREST_DB)
    return at_strms(balance(y, x_pan(848)), level_db, 0.1)


def sine_pair(f, n, detune, rng, second=0.5):
    t = np.arange(n) / SR
    a = np.sin(2 * np.pi * f * t + rng.uniform(0, 2 * np.pi))
    b = second * np.sin(2 * np.pi * (f + detune) * t + rng.uniform(0, 2 * np.pi))
    return a, b


def shimmer_s02():
    """SHIMMER (f272): sines A6 1760 + E7 2637.02, 3 s Gaussian envelope, -44 dBFS; each a slowly beating
    pair, placed over the rocket slit (right of centre)."""
    n = secs(3.0)
    r = np.random.default_rng(272)
    t = np.arange(n) / SR
    env = np.exp(-0.5 * ((t - 1.5) / 0.5) ** 2)
    env = np.clip((env - env[0]) / (1 - env[0]), 0, 1)
    a1, a2 = sine_pair(1760.0, n, 0.35, r)
    e1, e2 = sine_pair(2637.02, n, 0.43, r)
    st = pan_mono(a1, 0.12) + pan_mono(a2, 0.38) + 0.6 * (pan_mono(e1, 0.22) + pan_mono(e2, 0.46))
    return at_peak(st * env, -44.0)


def push_curve(n, lo, hi):
    """The S04 push (§8.2): lo -> hi dB, exponential to the stop, over n samples ending at f764."""
    u = np.arange(n) / n
    return lo + (hi - lo) * (np.exp(3 * u) - 1) / (np.exp(3) - 1)


def shimmer_s04():
    """SHIMMER (f644 -> f764): sines D5 587.33 + A5 880, -36 -> -28 dBFS peak, exponential to the stop (review
    fix 4). Each sine has a slow partner (0.2 x, +0.25 / +0.31 Hz) panned apart, all in phase on f764, so the
    shimmer moves in the stereo image but its level is the ramp itself (50 ms peak envelope held to the ramp)."""
    n = S764 - smp(644)
    r = np.random.default_rng(644)
    t = (np.arange(n) - n) / SR                       # 0 on f764: every pair is in phase there
    st = np.zeros((2, n))
    for f, det, g, p1, p2 in ((587.33, 0.25, 1.0, 0.08, 0.32), (880.0, 0.31, 0.8, 0.18, 0.42)):
        ph = r.uniform(0, 2 * np.pi)
        st += g * (pan_mono(np.sin(2 * np.pi * f * t + ph), p1) + 0.2 * pan_mono(np.sin(2 * np.pi * (f + det) * t + ph), p2))
    env = moving_mean(maximum_filter1d(np.abs(st).max(axis=0), secs(0.05), mode='nearest'), secs(0.1))
    st *= undb(push_curve(n, -36.0, -28.0)) / env
    na = secs(0.6)
    st[:, :na] *= ramp_in(na)
    return st


def sub_layer(phi, env, seed):
    """Small-speaker layer of a sub (review fix 8): harmonics of the sub's own phase, so the layer follows the glide:
    the 2nd and 3rd (the review's layer) continued through the 10th as a saturated tone continues its series
    (amplitudes k^-0.5, the 2nd/3rd at 0.7 of that), softly saturated (tanh, level-dependent: it cleans up as the hit
    decays), high-passed at 90 Hz (the boom itself stays the sub's), low-passed at 1.2 kHz (warm, never a buzz). The
    4th-10th are what a phone plays (nothing below about 200 Hz); the ear hears the glide's pitch from their spacing.
    A 2nd/3rd-only layer at -10 dB measured 6.8 LU UNDER the riser through a 200 Hz high-pass. Unit peak."""
    w23, slope, drive = SUB_SERIES
    r = np.random.default_rng(seed)
    h = sum((w23 if k < 4 else 1.0) * k ** -slope * np.sin(k * phi + r.uniform(0, 2 * np.pi)) for k in range(2, 11))
    h = np.tanh(drive * env * h / np.abs(h).max()) / np.tanh(drive)
    h = filt(filt(h, 'high', 90.0, order=2), 'low', 1200.0, order=2)
    na = secs(0.004)
    h[:na] *= ramp_in(na)
    return h / peak(h)


def sub_swell():
    """SUB swell (f860): 32 -> 45 Hz over 2 s, rising 0.6 s then decaying, soft-saturated, plus its small-speaker
    layer (sub_layer, SUB_LAYER['swell'] re its peak: a soft rising hum on a phone, felt below that on full range);
    -20 dBFS peak (well under the plunge SUB)."""
    n = secs(3.0)
    t = np.arange(n) / SR
    f = 32.0 * (45.0 / 32.0) ** np.clip(t / 2.0, 0, 1)
    env = np.where(t < 0.6, np.sin(0.5 * np.pi * t / 0.6) ** 2, np.exp(-(t - 0.6) / 0.8))
    phi = 2 * np.pi * np.cumsum(f) / SR
    y = np.tanh(1.4 * np.sin(phi) * env) / np.tanh(1.4)
    y = y + undb(SUB_LAYER['swell']) * peak(y) * sub_layer(phi, env, 861)
    y[-secs(0.3):] *= ramp_out(secs(0.3))
    return y


def sub_plunge():
    """SUB (f1428): synth.sub_hit(52 -> 32 Hz, decay 0.45 s) plus its small-speaker layer (sub_layer on the same
    glide and envelope, SUB_LAYER['plunge'] re the sub's peak), so the landing is heard on a phone and felt on
    full range. Unit peak; placed at -14 dBFS peak."""
    sh = S.sub_hit(dur=2.2, f0=52, f1=32, decay=0.45).astype(np.float64)
    t = np.arange(sh.size) / SR
    phi = 2 * np.pi * np.cumsum(32.0 + 20.0 * np.exp(-t / 0.12)) / SR      # sub_hit's own phase
    y = sh + undb(SUB_LAYER['plunge']) * peak(sh) * sub_layer(phi, np.exp(-t / 0.45), 1429)
    y[-secs(0.3):] *= ramp_out(secs(0.3))
    return y / peak(y)


def draw_whisper():
    """DRAW (f950-f966, CUES_v2): BP noise 3-7 kHz with a paper-grain flutter, envelope = the hairline's draw speed
    (derivative of E-DRAW), panned with the pen as it runs clockwise round the retina frame (§11: (454,700)-(940,
    1186)); -40 dBFS."""
    n = smp(F_DRAW[1]) - smp(F_DRAW[0])
    r = np.random.default_rng(962)
    u = np.arange(n) / n
    s = E_DRAW(u)
    v = np.gradient(s)
    v /= v.max()
    x0, _, x1, _ = RETINA_FRAME
    side = float(x1 - x0)
    p = s * 4 * side                                    # pen position along the perimeter (px)
    x = np.select([p < side, p < 2 * side, p < 3 * side], [x0 + p, x1 + 0 * p, x1 - (p - 2 * side)], x0 + 0 * p)
    grain = 1 + 0.6 * filt(r.standard_normal(n), 'low', 60.0) / 0.05
    y = filt(r.standard_normal(n), 'band', (3000.0, 7000.0)) * v * np.clip(grain, 0.2, 2.5)
    return at_peak(pan_mono(y, x_pan(x)), -40.0)


def stamp(seed):
    """STAMP: modal click f0 900 Hz, ratios 1 / 2.76 / 5.40, decays 40 / 20 / 10 ms + 140 Hz knock 30 ms."""
    r = np.random.default_rng(seed)
    n = secs(0.15)
    t = np.arange(n) / SR
    f0 = 900.0 * (1 + r.uniform(-0.025, 0.025))
    modal = sum(a * np.sin(2 * np.pi * f0 * k * t + r.uniform(0, 2 * np.pi)) * np.exp(-t / d)
                for k, d, a in ((1.0, 0.040, 1.0), (2.76, 0.020, 0.6), (5.40, 0.010, 0.35)))
    hit = filt(r.standard_normal(48) * np.hanning(50)[1:-1], 'low', 7000.0)
    modal = fftconvolve(modal, hit)[:n]
    knock = np.sin(2 * np.pi * 140.0 * t) * (1 - np.exp(-t / 0.0008)) * np.exp(-t / 0.009)
    knock[secs(0.03):] = 0.0
    knock[secs(0.025):secs(0.03)] *= ramp_out(secs(0.005))
    paper = filt(r.standard_normal(n), 'band', (1200.0, 5000.0)) * np.exp(-t / 0.003)
    y = modal / peak(modal) + 0.8 * knock / peak(knock) + 0.25 * paper / peak(paper)
    y[n - secs(0.03):] *= ramp_out(secs(0.03))
    return y


def riser():
    """RISER (f1388 -> f1428): pink noise, low-pass 300 -> 3000 Hz (exponential) over 1.333 s,
    -30 -> -22 dBFS, hard cut (1 ms) on f1428 where the SUB lands. No reverb send: nothing outlives the cut."""
    n = smp(1428) - smp(1388)
    p = pink_noise(n, seed=1388, channels=2)
    x = np.stack([p[0], 0.5 * p[0] + np.sqrt(0.75) * p[1]])
    t = np.arange(n) / SR
    y = tv_lowpass(x, 300.0 * 10 ** (t / (n / SR)), block=64)
    e = np.sqrt(np.convolve(power(y), np.ones(secs(0.03)) / secs(0.03), 'same')) + 1e-9
    y *= undb(8.0 * t / (n / SR)) / e                   # level rises 8 dB, the -30 -> -22 dBFS peak ramp
    y *= undb(-22.0) / peak(y[:, n - secs(0.1):])
    y[:, :secs(0.05)] *= ramp_in(secs(0.05))
    y[:, n - secs(0.001):] *= ramp_out(secs(0.001))
    return y


def relay():
    """RELAY (f1580, one frame before the light): two clicks 18 ms apart (1.2 ms noise BP 2-5 kHz, a small
    armature ring) + 80 Hz thump 25 ms: the light table's switch."""
    r = np.random.default_rng(1604)
    n = secs(0.12)
    t = np.arange(n) / SR
    y = np.zeros(n)
    L = secs(0.0012)
    for dt, g in ((0.0, 1.0), (0.018, 0.7)):
        c = np.zeros(secs(0.02))
        c[:L] = r.standard_normal(L) * np.hanning(L + 2)[1:-1]
        c = filt(c, 'band', (2000.0, 5000.0))
        tc = np.arange(c.size) / SR
        c = c / peak(c) + 0.3 * (np.sin(2 * np.pi * 3150 * tc) * np.exp(-tc / 0.004)
                                 + 0.6 * np.sin(2 * np.pi * 4730 * tc) * np.exp(-tc / 0.003))
        i0 = secs(dt)
        y[i0:i0 + c.size] += g * c
    th = np.sin(2 * np.pi * 80.0 * t) * (1 - np.exp(-t / 0.001)) * np.exp(-t / 0.008)
    th[secs(0.025):] = 0.0
    th[secs(0.02):secs(0.025)] *= ramp_out(secs(0.005))
    return y / peak(y) + 0.7 * th / peak(th)


def hum(dur):
    """HUM: light-table ballast, 100 / 200 / 300 Hz at -46 / -52 / -58 dBFS (plus a trace of 400 Hz at -68 for the
    ballast's buzz), 0.5 Hz +-1 dB wobble (absolute mix-bus levels). The table is a switch (CUES_v2): no fade-in,
    only a 3 ms de-click and a tiny inrush (+3 dB at the switch, settling with a 60 ms time constant)."""
    n = secs(dur)
    t = np.arange(n) / SR
    r = np.random.default_rng(100)
    y = sum(undb(d) * np.sin(2 * np.pi * f * t + r.uniform(0, 2 * np.pi))
            for f, d in ((100.0, -46.0), (200.0, -52.0), (300.0, -58.0), (400.0, -68.0)))
    y *= undb(1.0 * np.sin(2 * np.pi * 0.5 * t))
    y *= 1 + (undb(3.0) - 1) * np.exp(-t / 0.06)
    y[:secs(0.003)] *= ramp_in(secs(0.003))
    return np.stack([y, y])


def pad_ride(sample):
    """PAD_RIDE = (f_down_start, f_down_end, f_up_start, f_up_end, dB): one move under the withheld note (review
    fix 2): raised-cosine down, held, raised-cosine back to 0 dB. Returns dB per absolute sample."""
    a, b, c, d, g = PAD_RIDE
    s = np.asarray(sample, np.float64)
    down = np.clip((s - smp(a)) / (smp(b) - smp(a)), 0, 1)
    up = np.clip((s - smp(c)) / (smp(d) - smp(c)), 0, 1)
    return g * (0.5 - 0.5 * np.cos(np.pi * down)) * (0.5 + 0.5 * np.cos(np.pi * up))


# ---------------------------------------------------------------- the cue sheet (§8.2 as re-timed by CUES_v2.md)
PINGS = [  # §3.3 S03 router table, hop 1..12: (coin, Hz, note, screen x of the coin -> pan)
    (6, 698.46, 'F5', 891.4), (23, 1046.50, 'C6', 823.2), (19, 783.99, 'G5', 313.8), (4, 1174.66, 'D6', 652.4),
    (14, 1396.91, 'F6', 425.4), (9, 1567.98, 'G6', 529.0), (24, 1396.91, 'F6', 938.4), (17, 1174.66, 'D6', 769.0),
    (11, 1046.50, 'C6', 763.2), (21, 783.99, 'G5', 566.6), (18, 587.33, 'D5', 916.0), (16, 1174.66, 'D6', 646.8)]


def compose():
    sc = Score()

    # f0 ROOM (whole film, its own automation; exact zeros f764-f775 and a 2 ms return at f776)
    room = room_bed()
    sc.place('room', room, 0, 'ROOM in (fade 0.25 s), pink BP 60 Hz-6 kHz, L/R corr 0.7', -46.0, 0.0, free=True)
    sc.refs.append((776, 'ROOM back (2 ms fade)', 0.5 * (room[0, S776:S776 + secs(0.2)] + room[1, S776:S776 + secs(0.2)]), None))

    # S01 hook: the coin settles (pan = coin #16 at x 678 -> +0.15). The hook keeps the cue sheet's internal balance
    # (flick -14 peak, whirr -30 RMS, ticks -24 -> -18, CLACK -10 dBFS peak); render() then moves the whole group
    # (dry + its room) so the CLACK is the delivered file's loudest peak.
    hp = x_pan(678.0)
    sc.place('hook', at_peak(pan_mono(coin_flick(), hp), -14.0), 1, 'COIN flick D7 2349.3 Hz (4 ms excitation, table-damped from f2)', -14.0, hp,
             {'hook': 0.3}, tag='flick')
    sc.place('hook', at_strms(pan_mono(whirr(), hp), WHIRR_DB, 0.35), 2, 'WHIRR f2-f15, BP 4-8 kHz, AM 14 -> 9 Hz', WHIRR_DB, hp, {'hook': 0.15},
             tag='whirr')
    rt, rattle_times, rstats = rattle()
    rt_st = pan_mono(rt, hp)
    rt_st *= undb(-18.0) / peak(rt_st[:, int(round((rattle_times[-1] - 0.5) * SR)):])  # last tick at -18 dBFS
    sc.place('hook', rt_st, 15, f'RATTLE f15-f44, {len(rattle_times)} ticks, Euler disk 9 -> 32 Hz (integrated), -24 -> -18 dBFS', -18.0, hp,
             {'hook': 0.15}, tag='rattle')
    sc.place('hook', at_peak(pan_mono(clack(), hp), -10.0), 44, f'CLACK (3 ticks / 12 ms + 120 Hz 40 ms at {CLACK_THUMP[0]:+g} dB + COIN D7 tau x1.5 at {CLACK_RING_DB:g} dB)', -10.0, hp,
             {'hook': 0.3}, tag='clack')

    # DRONE segment A: f53 -> cut at f764 (LP 900 -> 500 at f244, back at f380; push from f644)
    a0 = smp(53)
    durA = (S764 - a0) / SR

    def lp_curve_a(t):
        ft = a0 / SR + t
        c = np.full(t.shape, np.log(900.0))
        u1 = np.clip((ft - smp(244) / SR) / 0.4, 0, 1)
        u2 = np.clip((ft - smp(380) / SR) / 0.3, 0, 1)
        c = c + (np.log(500.0) - np.log(900.0)) * (0.5 - 0.5 * np.cos(np.pi * u1))
        c = c + (np.log(900.0) - np.log(500.0)) * (0.5 - 0.5 * np.cos(np.pi * u2))
        return np.exp(c)
    dv = drone_voices(durA, lp_curve_a)
    dA = sum(dv.values())
    dA *= undb(-30.0) / rms_of(dA, smp(150) - a0, smp(640) - a0)
    gA = np.ones(dA.shape[1])
    nf = secs(1.5)
    gA[:nf] = ramp_in(nf)
    # the push f644 -> f764 (review fix 4): the drone's own smoothed 300 ms RMS is steered onto the cue sheet's ramp,
    # -30 -> -24 dBFS RMS, exponential to the stop. It starts wherever the LFO / D2-copy beat has the drone at f644
    # (no step) and joins the ramp by f692 (0.4 of the push); left alone, those slow beats sat in a trough on f764.
    p0 = smp(644) - a0
    env = np.sqrt(moving_mean(power(dA), secs(0.3)))
    e0 = float(to_db(env[p0]))
    nP = dA.shape[1] - p0
    uP = np.arange(nP) / nP
    target = push_curve(nP, -30.0, -24.0) + (e0 + 30.0) * np.clip(1 - uP / 0.4, 0, 1) ** 2
    gA[p0:] *= undb(target) / env[p0:]
    sc.place('drone', dA * gA, 53, 'DRONE in (1.5 s fade): D1 36.71 + D2 73.42 (+0.15 Hz copy) + A2 110, LP 900 Hz, LFO 0.07 Hz', -30.0, 0.0, {'music': 0.05},
             tag='droneA')
    sc.log(244, 'DRONE low-pass 900 -> 500 Hz over 0.4 s', -30.0)
    sc.log(380, 'DRONE low-pass back to 900 Hz', -30.0)
    sc.log(644, f'DRONE push {e0:.1f} -> -30 -> -24 dBFS RMS (300 ms), exponential to f764', -24.0)

    def felt(frame, freq, level, vel=0.5, dur=5.0, decay=1.0, pan=None, name=None, seed=None, tag=None):
        p = pitch_pan(freq) if pan is None else pan
        y = balance(felt_upright(freq, dur, vel, 0.4, decay, seed=seed if seed is not None else frame * 7 + 1), p)
        sc.place('felt', at_peak(y, level), frame, name or f'FELT {freq:.2f} Hz vel {vel:.2f}', level, p, {'music': 0.3}, tag=tag)

    felt(54, 146.83, -22.0, 0.50, name='FELT D3 146.83, vel 0.50')

    # S02
    lv = -34.0 + BLOOM_TRIM[116]
    sc.place('fx', bloom(0.9, lv, 116), 116, 'BLOOM whoosh 0.9 s 250 -> 1600 Hz (RMS, loudest 100 ms)', lv, 0.0, {'music': 0.15}, tag='bloom116')
    felt(116, 220.00, -22.0, 0.50, name='FELT A3 220.00, vel 0.50')
    sc.place('fx', slit(0.9, 300.0, 1800.0, -28.0, 260), 260, 'SLIT BP noise 300 -> 1800 Hz / 0.9 s (E-SNAP speed, f260-f287)', -28.0, x_pan(848),
             {'music': 0.15}, tag='slit260')
    felt(260, 329.63, -22.0, 0.55, name='FELT E4 329.63, vel 0.55')
    sc.place('fx', shimmer_s02(), 272, 'SHIMMER A6 1760 + E7 2637.02, 3 s Gaussian', -44.0, 0.28, {'music': 0.4})
    sc.place('fx', slit((smp(318) - smp(F_SLIT2)) / SR, 600.0, 2400.0, -28.0 + SLIT2_DB, 300), F_SLIT2,
             'SLIT second swell: the slit outgrows the print (f300-f318), 600 -> 2400 Hz / 0.6 s, 6 dB lighter', -28.0 + SLIT2_DB, x_pan(848),
             {'music': 0.15}, tag='slit300')

    # S03: coin #16 returns, then the router pings at the picture's landings (geom.LANDS, an accelerando)
    y = coin_strike(1174.66, tau=1.0, excite='tick', seed=380, coin=16, click_db=-14.0)
    p16 = x_pan(646.8)
    sc.place('coins', at_peak(pan_mono(y, p16), -24.0), 380, 'COIN D6 1174.66 (#16, its own pitch)', -24.0, p16, {'coin': 0.3})
    lv = -36.0 + BLOOM_TRIM[380]
    sc.place('fx', bloom(0.9, lv, 380), 380, 'BLOOM whoosh 0.9 s (RMS, loudest 100 ms)', lv, 0.0, {'music': 0.15}, tag='bloom380')
    for k, ((coin, f, nm, x), fr) in enumerate(zip(PINGS, LANDS)):
        lvl = (-20.0 if k == 11 else -22.0) + (PING_DENSE_DB if k and fr - LANDS[k - 1] <= 6 else 0.0)
        # review fix 9: coin_strike(f, tau=0.6, excite='soft', focus=2.0, beat=0.2), its doublets struck in phase
        # (coin_strike_coherent: a struck disc excites both members of a split mode together; with independent
        # phases a ping's fundamental could be born half-cancelled and leave the 1.594 mode to set the pitch)
        y = coin_strike_coherent(f, tau=0.6, excite='soft', seed=fr, coin=coin, focus=PING_FOCUS, beat=PING_BEAT, click_db=None)
        sc.place('coins', at_peak(pan_mono(y, x_pan(x)), lvl), fr,
                 f'PING hop {k + 1}: {nm} {f:.2f} Hz, coin #{coin:02d} (tau x0.6, soft mallet, focus {PING_FOCUS:g})', lvl, x_pan(x), {'coin': 0.35},
                 tag=f'ping{k + 1}')

    # S04: push, swell, hard stop
    lv = -34.0 + BLOOM_TRIM[644]
    sc.place('fx', bloom(0.9, lv, 644), 644, 'BLOOM whoosh 0.9 s (RMS, loudest 100 ms)', lv, 0.0, {'music': 0.15}, tag='bloom644')
    felt(644, 174.61, -22.0, 0.50, name='FELT F3 174.61, vel 0.50')
    sc.place('fx', shimmer_s04(), 644, 'SHIMMER D5 587.33 + A5 880, -36 -> -28 dBFS peak (exponential to f764)', -36.0, 0.25, {'music': 0.3},
             tag='shimmer644')
    sc.log(764, 'HARD STOP: every track incl. reverb tails to digital zero, f764-f775', None)
    sc.log(776, 'ROOM back at -50 dBFS (2 ms fade)', -50.0)
    felt(777, 73.42, -20.0, 0.60, dur=6.0, decay=1.5, name='FELT D2 73.42, vel 0.60, decay x1.5')

    # S05: the eye
    sc.place('fx', at_peak(pan_mono(sub_swell(), 0.0), -20.0), 860,
             f'SUB swell 32 -> 45 Hz over 2 s (+ saturated harmonic layer 2nd-10th, {SUB_LAYER["swell"]:g} dB)', -20.0, 0.0, tag='swell')
    durB = (smp(1164) - smp(860)) / SR
    pb = pad_additive([116.54, 174.61, 293.66], durB, attack=0.9, release=2.0, seed=860).astype(np.float64)
    pb *= undb(-30.0) / rms_of(pb, secs(1.2), pb.shape[1] - secs(2.2))
    sc.place('pad', pb, 860, 'PAD Bb: Bb2 116.54 / F3 174.61 / D4 293.66 (8 partials 1/n^2, +-3 cents x3, LP 3 kHz)', -30.0, 0.0, {'music': 0.2},
             tag='pad_bb')
    sc.place('fx', draw_whisper(), F_DRAW[0], f'DRAW whisper f{F_DRAW[0]}-f{F_DRAW[1]} (E-DRAW speed, pen-following pan)', -40.0,
             x_pan(0.5 * (RETINA_FRAME[0] + RETINA_FRAME[2])))
    for fr in F_STAMPS:
        sc.place('fx', at_peak(pan_mono(stamp(fr), -0.35), -26.0), fr, 'STAMP modal 900 Hz + 140 Hz knock', -26.0, -0.35, {'coin': 0.25})

    # S06: the contact sheet
    lv = -34.0 + BLOOM_TRIM[1124]
    sc.place('fx', bloom(1.6, lv, 1124, reverse=True), 1124, 'reverse BLOOM (space opening), ends f1172 (RMS, loudest 100 ms)', lv, 0.0,
             {'music': 0.15}, tag='bloom1124')
    b0 = smp(1124)
    durD = (smp(F_DRONE_OUT[1]) - b0) / SR
    dv = drone_voices(durD)
    full = sum(dv.values())
    gn = undb(-30.0) / rms_of(full, smp(1210) - b0, smp(1420) - b0)
    d1n = undb(-34.0) / rms_of(dv['D1'], smp(1210) - b0, smp(1420) - b0)
    nB = full.shape[1]
    tB = np.arange(nB)
    k0 = smp(1428) - b0
    xf = np.clip((tB - (k0 - secs(0.02))) / secs(0.02), 0, 1)
    xf = 0.5 - 0.5 * np.cos(np.pi * xf)
    dB = (full - dv['D1']) * gn * (1 - xf) + dv['D1'] * (gn * (1 - xf) + d1n * xf)
    g = np.ones(nB)
    g[:secs(1.5)] = ramp_in(secs(1.5))
    # the dip: down in 2 f from f1187 and held at -6 dB for the cue sheet's 18 f (to f1205), back by f1211: the floor
    # drops out exactly where the 12th note would have sounded and stays out while cell 12 develops
    dip = np.interp(tB, [smp(f) - b0 for f in DRONE_DIP], [0.0, -6.0, -6.0, 0.0])
    g *= undb(dip)
    g[smp(F_DRONE_OUT[0]) - b0:] *= ramp_out(smp(F_DRONE_OUT[1]) - smp(F_DRONE_OUT[0]))
    sc.place('drone', dB * g, 1124, 'DRONE returns with the pull-back (1.5 s fade), -30 dBFS RMS', -30.0, 0.0, {'music': 0.05}, tag='droneB')
    # The sheet develops as a ripple from the eye (CUES_v2): the notes arrive in that order, as chords. One note
    # rises -30 -> -26 dBFS peak into the four-note chord (review fix 3: 6 dB under the cue sheet's -24 -> -20), then the
    # last two cells arrive softer (-27, -28) and the 12th is withheld; a k-note chord's notes sit CHORD_LAW*log10(k) dB
    # under that (the chord at f1156: 4.5 dB per note), so a chord is a little fuller than one note but never louder
    # than the CLACK, and the cascade is not the film's loudest passage. Softer hands for the chords (velocity), each
    # note panned where its cell is on screen.
    for i, (fr, notes) in enumerate(SHEET):
        k = len(notes)
        base = SHEET_DB[i] - CHORD_LAW * np.log10(k)
        vel = {1: 0.52, 2: 0.48, 4: 0.45}[k]
        for j, (cell, f, nm) in enumerate(notes):
            lvl = base + (1.0 if (k == 4 and nm == 'G5') else 0.0)        # the chord's top voice leads a little
            felt(fr, f, lvl, vel, dur=4.0, pan=cell_pan(cell, fr), name=f'FELT sheet cell {cell:02d}: {nm} {f:.2f} Hz',
                 seed=fr * 7 + 1 + 13 * j, tag=f'cell{cell}')
    sc.log(F_NO_NOTE, 'NO NOTE (the 12th, D5, is withheld); DRONE dips -6 dB for 18 f (f1187-f1205, back by f1211)', -36.0)

    # S07: the plunge
    sc.place('fx', riser(), 1388, 'RISER pink noise LP 300 -> 3000 Hz, -30 -> -22 dBFS, hard cut f1428', -22.0, 0.0, tag='riser')
    sc.place('sub', at_peak(pan_mono(sub_plunge(), 0.0), -14.0), 1428,
             f'SUB sub_hit 52 -> 32 Hz, decay 0.45 s (+ saturated harmonic layer 2nd-10th, {SUB_LAYER["plunge"]:g} dB)', -14.0, 0.0, tag='plunge')
    sc.log(1428, 'ROOM -52 dBFS; DRONE reduced to D1 at -34 dBFS RMS', -34.0)
    pa, pe = pitch_pan(220.0), pitch_pan(329.63)
    dy = balance(felt_upright(220.0, 5.0, 0.45, 0.4, seed=1444), pa) + balance(felt_upright(329.63, 5.0, 0.45, 0.4, seed=1445), pe)
    sc.place('felt', at_peak(dy, -24.0), 1444, 'FELT dyad A3 220.00 + E4 329.63', -24.0, 0.5 * (pa + pe), {'music': 0.3})
    sc.log(F_DRONE_OUT[0], f'DRONE fades out over 12 f (f{F_DRONE_OUT[0]}-f{F_DRONE_OUT[1]})', None)

    # S08: the light table is a switch (dark f1580, lit f1581)
    sc.place('fx', at_peak(pan_mono(relay(), 0.0), -28.0), F_RELAY, 'RELAY two clicks 18 ms apart + 80 Hz thump (one frame before the light)',
             -28.0, 0.0, {'coin': 0.2}, tag='relay')
    sc.place('fx', hum((N - smp(F_LIGHT)) / SR), F_LIGHT, 'HUM 100/200/300 Hz at -46/-52/-58, switched on (3 ms, +3 dB inrush)', -46.0, 0.0,
             tag='hum')
    # PAD D major add9. Its E5 (the add9) sits a whole tone over the D5, inside one critical band, so it is voiced
    # PAD_E5_DB under the chord tones; and the pad gives way for the withheld note with one ride (PAD_RIDE), so the
    # D5 is the thing heard at f1604 rather than a note under a louder chord (review fix 2).
    pdur = (N - smp(F_LIGHT)) / SR
    pm = pad_additive([146.83, 220.00, 369.99], pdur, attack=0.8, seed=1604).astype(np.float64)
    pe = pad_additive([659.26], pdur, attack=0.8, seed=1605).astype(np.float64)
    w0, w1 = secs(1.2), secs(3.5)
    pe *= undb(PAD_E5_DB) * (rms_of(pm, w0, w1) / np.sqrt(3)) / rms_of(pe, w0, w1)
    pd = pm + pe
    pd *= undb(PAD_DMAJ_DB) / rms_of(pd, w0, w1)
    pd *= undb(pad_ride(np.arange(pd.shape[1]) + smp(F_LIGHT)))
    sc.place('pad', pd, F_LIGHT, f'PAD D major add9: D3 / A3 / F#4 + E5 at {PAD_E5_DB:g} dB (the first F#), {PAD_DMAJ_DB:g} dBFS RMS, 0.8 s attack',
             PAD_DMAJ_DB, 0.0, {'music': 0.2}, tag='pad_dmaj')
    r0, r1, r2, r3, rg = PAD_RIDE
    sc.log(r0, f'PAD ride {rg:g} dB: down f{r0}-f{r1}, held, back to 0 dB f{r2}-f{r3} (one move under the D5)', PAD_DMAJ_DB + rg)
    sc.log(F_LIGHT, 'ROOM back to -46 dBFS once the table is lit (f1581-f1628)', -46.0)
    felt(F_D5, 587.33, D5_DB, 0.75, dur=6.0, decay=D5_DECAY, name='FELT D5 587.33, vel 0.75: the withheld 12th note', seed=D5_SEED, tag='d5')
    y = coin_strike(2349.3, tau=0.8, excite='tick', seed=1700, coin=16, click_db=-16.0)
    sc.place('coins', at_peak(pan_mono(y, hp), -30.0), F_TING, 'COIN ting D7 2349.3, tau x0.8 (frame-0 callback)', -30.0, hp, {'coin': 0.3},
             tag='ting')
    sc.log(F_HOLD[0], f'PAD + HUM (+ all music and reverb) fade to ROOM, f{F_HOLD[0]}-f{F_HOLD[1]}', None)
    sc.log(NF, 'ROOM ends (end of file)', None)
    sc.cues.sort(key=lambda c: (c['frame'], c['cue']))
    return sc, rattle_times, rstats


# ---------------------------------------------------------------- mix + master (§8.3)
def tp_limit(y, ceil_db):
    """True-peak 'clip-gain' limiter that behaves like a fader ride: finds the samples whose 4x-oversampled
    peak passes the ceiling, merges those closer than 400 ms into one passage, and dips the gain over each
    passage by exactly what its worst peak needs (40 ms raised-cosine look-ahead, hold, 250 ms release). Kept as a
    safety net only: with this mix it finds nothing (limiter_clusters == [], the master is a pure gain)."""
    c = undb(ceil_db)
    up = resample_poly(y, 4, 1, axis=1)
    env = np.abs(up).max(axis=0)[: 4 * y.shape[1]].reshape(-1, 4).max(axis=1)
    over = np.flatnonzero(env > c)
    if over.size == 0:
        return y, 0.0, []
    br = np.flatnonzero(np.diff(over) > secs(0.4))
    starts = np.concatenate([[over[0]], over[br + 1]])
    ends = np.concatenate([over[br], [over[-1]]])
    D = np.zeros(y.shape[1])
    A, H, R = secs(0.04), secs(0.005), secs(0.25)
    clusters = []
    for a, b in zip(starts, ends):
        need = float(20 * np.log10(env[a:b + 1].max() / c)) + 0.02
        lo = max(0, a - A)
        D[lo:a] = np.maximum(D[lo:a], need * ramp_in(A)[A - (a - lo):])
        hi = min(len(D), b + 1 + H)
        D[a:hi] = np.maximum(D[a:hi], need)
        r1 = min(len(D), hi + R)
        D[hi:r1] = np.maximum(D[hi:r1], need * ramp_out(R)[:r1 - hi])
        clusters.append(dict(start_s=round(a / SR, 4), end_s=round(b / SR, 4), reduction_db=round(need, 2)))
    return y * undb(-D), float(D.max()), clusters


def master(mix, meter):
    gain_db, info = 0.0, {}
    for _ in range(6):
        y = mix * undb(gain_db)
        y, gr, clusters = tp_limit(y, TP_CEIL)
        y[:, S764:S776] = 0.0
        lufs = meter.integrated_loudness(y.T)
        info = dict(master_gain_db=round(gain_db, 3), master_gain_exact_db=float(gain_db), limiter_max_reduction_db=round(gr, 2),
                    limiter_clusters=clusters,
                    master_is_pure_gain=not clusters, lufs_pre_quantize=round(float(lufs), 3))
        if abs(lufs - LUFS_TARGET) < 0.02:
            break
        gain_db += LUFS_TARGET - lufs
    return y, info


def write_wav(y, path):
    q = np.clip(np.round(y * 8388607.0), -8388608, 8388607).astype(np.int64)
    q[:, S764:S776] = 0
    sf.write(path, (q << 8).astype(np.int32).T, SR, subtype='PCM_24')


# ---------------------------------------------------------------- measurement helpers (§10 Sound)
def tone_amp_db(x, s0, s1, f):
    seg = x[s0:s1]
    w = np.hanning(seg.size)
    c = np.sum(seg * w * np.exp(-2j * np.pi * f * np.arange(seg.size) / SR)) * 2 / w.sum()
    return float(to_db(np.abs(c)))


def peak_freq(x, s0, s1, lo, hi):
    seg = x[s0:s1] * np.hanning(s1 - s0)
    nfft = 1 << 20
    X = np.abs(np.fft.rfft(seg, nfft))
    fq = np.fft.rfftfreq(nfft, 1 / SR)
    m = (fq >= lo) & (fq <= hi)
    return float(fq[m][np.argmax(X[m])])


_FB = {}


def _fbank(nfft, fmin=100.0, fmax=12000.0, bpo=24):
    """Triangular filterbank, `bpo` bands per octave (cached)."""
    key = (nfft, fmin, fmax, bpo)
    if key not in _FB:
        fq = np.fft.rfftfreq(nfft, 1 / SR)
        cf = fmin * 2 ** (np.arange(int(np.log2(fmax / fmin) * bpo) + 2) / bpo)
        b = np.unique(np.round(cf / (SR / nfft)).astype(int))
        F = np.zeros((b.size - 2, fq.size))
        for i in range(b.size - 2):
            F[i, b[i]:b[i + 1] + 1] = np.linspace(0, 1, b[i + 1] - b[i] + 1)
            F[i, b[i + 1]:b[i + 2] + 1] = np.linspace(1, 0, b[i + 2] - b[i + 1] + 1)
        _FB[key] = F
    return _FB[key]


def superflux(x, s0, s1, nfft=2048, hop=240, mu=4, lam=0.1):
    """SuperFlux onset strength (Boeck & Widmer 2013): log-compressed (log10(1 + lam * band)) 24-band/octave
    filterbank 100 Hz-12 kHz, reference frame maximum-filtered over 3 bands, positive difference at a lag of mu frames
    (43 ms Hann frames, 5 ms hop). lam = 0.1 keeps the room tone (about -40 dBFS) in the linear part of the compression,
    so its random band jitter does not read as onsets while a soft felt note still does. Returns (end sample of each
    frame, strength)."""
    seg = np.asarray(x[s0 - nfft:s1], np.float64)
    fr = np.lib.stride_tricks.sliding_window_view(seg, nfft)[::hop]
    X = np.abs(np.fft.rfft(fr * np.hanning(nfft), axis=1))
    sg = np.log10(lam * (X @ _fbank(nfft).T) + 1.0)
    sm = maximum_filter1d(sg, 3, axis=1)
    d = np.maximum(sg[mu:] - sm[:-mu], 0).sum(axis=1)
    return s0 + hop * np.arange(mu, fr.shape[0]), d


def matched_lag(mono, ref, s, search=240, seg=None):
    """Where does a cue's own waveform sit in the written mix? Raw cross-correlation of first differences
    (pre-emphasis sharpens the peak) between the event's first 200 ms and the mix, lags +-5 ms around
    round(f*1600), refined to a fraction of a sample by a parabola through the peak. Returns the lag. `seg`, when
    given, replaces mono[s - search - 1 : s + search + len(ref)] (e.g. with other events cancelled)."""
    r = np.diff(np.asarray(ref, np.float64), prepend=0.0)
    seg = np.diff(np.asarray(mono[s - search - 1:s + search + ref.size] if seg is None else seg, np.float64))
    c = np.correlate(seg, r, 'valid')
    j = int(np.argmax(c))
    frac = 0.0
    if 0 < j < c.size - 1:
        den = c[j - 1] - 2 * c[j] + c[j + 1]
        frac = 0.5 * (c[j - 1] - c[j + 1]) / den if den != 0 else 0.0
    return float(j - search + frac)


def kweight(x):
    """ITU-R BS.1770-4 K-weighting at 48 kHz (pre-filter shelf + RLB high-pass), along the last axis."""
    b1, a1 = [1.53512485958697, -2.69169618940638, 1.19839281085285], [1.0, -1.69065929318241, 0.73248077421585]
    b2, a2 = [1.0, -2.0, 1.0], [1.0, -1.99004745483398, 0.99007225036621]
    return lfilter(b2, a2, lfilter(b1, a1, np.asarray(x, np.float64), axis=-1), axis=-1)


def loud_windows(x, ends, win=0.4, a=0):
    """BS.1770 loudness (LUFS, ungated) of the `win` s windows of stereo x (starting at absolute sample a) that END
    at absolute samples `ends`: 0.4 s = momentary, 3 s = short-term."""
    k = kweight(np.atleast_2d(x))
    c = np.concatenate([[0.0], np.cumsum((k * k).sum(axis=0))])
    w = secs(win)
    e = np.asarray(ends) - a
    return -0.691 + 10 * np.log10((c[e] - c[np.maximum(e - w, 0)]) / w + 1e-20)


def run_rms_db(x, win):
    """Running RMS (per-channel mean power) of `win` s windows; index = window start."""
    c = np.concatenate([[0.0], np.cumsum(power(x))])
    h = secs(win)
    return 10 * np.log10((c[h:] - c[:-h]) / h + 1e-24)


def line_env_db(m, f, win=0.1):
    """Heterodyne amplitude envelope (dBFS) of the component at f Hz in mono m (centred `win` s boxcar)."""
    z = m * np.exp(-2j * np.pi * f * np.arange(m.size) / SR)
    h = secs(win)
    return to_db(np.abs(np.convolve(z, np.ones(h) / h, 'same')) * 2)


def third_octave_snr(cue, rest, nfft=2400, hop=1200):
    """The review's masking test: 1/3-octave band levels in 50 ms frames (25 ms hop) of the cue and of the rest of
    the mix; bands within 30 dB of the cue's loudest count. Returns (best band SNR dB, its centre Hz, fraction of
    all frames in which some counted band of the cue is above the rest)."""
    cf = 1000 * 2 ** (np.arange(-17, 14) / 3)
    fq = np.fft.rfftfreq(nfft, 1 / SR)
    W = np.zeros((cf.size, fq.size))
    for i, c in enumerate(cf):
        W[i, (fq >= c / 2 ** (1 / 6)) & (fq < c * 2 ** (1 / 6))] = 1.0

    def bands(x):
        x = np.atleast_2d(x).mean(axis=0)
        nfr = 1 + (x.size - nfft) // hop
        fr = np.lib.stride_tricks.sliding_window_view(x, nfft)[::hop][:nfr]
        return 10 * np.log10((np.abs(np.fft.rfft(fr * np.hanning(nfft), axis=1)) ** 2) @ W.T + 1e-20)
    Bc, Br = bands(cue), bands(rest)
    sn = np.where(Bc > Bc.max() - 30, Bc - Br, -999.0)
    j = np.unravel_index(np.argmax(sn), sn.shape)[1]
    return float(sn.max()), float(cf[j]), float(np.mean((sn > 0).any(axis=1)))


REVIEW_FIXES = {
    '1_hook': 'APPLIED: flick keeps its -14 dBFS strike, table damping exp(-(t-t2)/0.15) from f2 (-35 dB by f15); CLACK 120 Hz sine for '
              'its full 40 ms. CHANGED: the review\'s 0 dB / 25 ms / ring -8 dB measured CLACK 50 ms RMS only +1.2 dB over the flick\'s '
              'ring at f2 and CLACK loudness -17.3 vs flick -15.7 LUFS (its own test fails), so the sine sits 2 dB over the bursts with '
              'a 30 ms decay and the D7 ring at -4 dB. Instead of a fixed -12.3 dBFS bus peak the whole hook group moves as one so the '
              'CLACK lands at -1.40 dBTP (the master gain moved from 10.96 to about 12 dB): same intent, no limiting. The whirr '
              'releases over 0.25 s into the rattle (no 11 dB step at f15).',
    '2_d5_over_pad': 'APPLIED at the CUES_v2 frames: one pad ride -4 dB, down f1598-f1606, held, back to 0 dB f1614-f1652; the E5 voice '
                     'pulled down. CHANGED: with E5 -8 dB and the pad at -24 RMS the D5 measured 3.8 LU under the pad and its line 8.8 dB '
                     'under 659 Hz, so the pad sits at -27 dBFS RMS (which also stops the ending being the loudest passage), E5 at -10 dB, '
                     'D5 at -17 dBFS ringing x2.4.',
    '3_cascade': 'APPLIED: sheet notes 6 dB under the cue sheet (one note -30 -> -26 dBFS peak) in CUES_v2 arrival order as chords; chord '
                 'notes 7.5 log10(k) dB under one note; the last two arrivals softer (-27, -28) into the absence; DRONE dip -6 dB reached in '
                 '1 f. No limiter anywhere.',
    '4_push': 'APPLIED: DRONE steered by its own 300 ms RMS onto -30 -> -24 (joining the ramp by f692 from wherever the LFO has it on '
              'f644, so no step); SHIMMER partners at 0.2, in phase on f764, peak envelope normalised to -36 -> -28.',
    '5_rattle': 'APPLIED: tick k where the integrated rate reaches k cycles, +-3 % jitter of the local period (13 ticks, the 13th at '
                '1.4448 s); bed pulses driven by the same tick times. The bed sits at -54 -> -44 dBFS RMS: the review\'s -46 -> -36 still '
                'left the bed level with the ticks in 3-7 kHz, -54 -> -44 puts every tick >= 6 dB over it.',
    '6_blooms': 'APPLIED exactly: at_strms(., -34 / -36, 0.1), no extra trim.',
    '7_hook_hf': 'APPLIED: 4th-order band-passes, 4th-order 7.5 kHz low-pass on rattle and CLACK, flick 4th-order 5 kHz. CHANGED: the '
                 'whirr (most of the hook\'s energy) needs an 8th-order 7 kHz low-pass: with 4th-order 7.5 kHz the hook measured -20.6 dB '
                 'above 8 kHz against the -25 dB target.',
    '8_sub_phone': 'APPLIED: a saturated harmonic layer on the sub\'s own glide, high-passed at 90 Hz, on both SUB moments. CHANGED: a '
                   '2nd/3rd-only layer at -10 dB measured 6.8 LU UNDER the riser through a 200 Hz high-pass (2nd/3rd of 32-52 Hz lie at '
                   '64-156 Hz, below a phone\'s range), and still -1.7 LU at 0 dB; the layer keeps the 2nd/3rd and continues the series '
                   'to the 10th (k^-0.5, 2nd/3rd at 0.7, tanh 1.5, low-pass 1.2 kHz), at -3 dB re the plunge and -12 dB re the swell.',
    '9_pings': 'APPLIED: tau x0.6, soft mallet, beat 0.2. CHANGED: coin_strike(focus=2.0) measured as low as -7.6 dB (fundamental under '
               'the 1.594 mode: independent doublet phases cancel it at birth), coherent doublets at focus 2.0 still 7.2 dB; '
               'coin_strike_coherent at focus 3.0 gives >= 10.9 dB on all 12. Calls landing 6 f apart play 2 dB lighter.',
    '10_drone_notches': 'APPLIED exactly: -15 dB at 183.55 / 367.10 / 734.20 Hz and -10 dB at 256.97 / 513.94 Hz, Q 12, both segments.',
    '11_levels': 'APPLIED: the convention (cue levels are mix-bus, master one uniform gain) is written in this script\'s docstring and in '
                 'levels_note; DESIGN_BIBLE §8.3 still needs that sentence (this script may not edit the bible). limiter_clusters is empty.',
}


def ev_seg(sc, tag, a, b, g=1.0):
    """A kept event on the absolute range [a, b) (zeros where it is silent), times g."""
    s0, x = sc.kept[tag]
    out = np.zeros((2, b - a))
    lo, hi = max(a, s0), min(b, s0 + x.shape[1])
    if hi > lo:
        out[:, lo - a:hi - a] = x[:, lo - s0:hi - s0] * g
    return out


def review_acceptance(y, sc, stems, info, rattle_times, rstats):
    """Every acceptance test of the independent review (fixes 1-11, 'Accept when ...'), plus the hard requirements it
    names, at the CUES_v2 frames. All levels are measured on the delivered file y (or on a cue's own signal at the
    delivered gain where a test compares one cue with another)."""
    g = undb(info['master_gain_db'])
    mono = 0.5 * (y[0] + y[1])
    A = {}
    r50 = run_rms_db(y, 0.05)

    # 1 -- the CLACK leads its hook
    s44, h50 = smp(44), secs(0.05)
    clack50 = float(r50[s44 - secs(0.005):s44 + secs(0.01)].max())
    pre = r50[smp(2):s44 - h50 + 1]
    pre50, pre_at = float(pre.max()), (smp(2) + int(np.argmax(pre))) / SPF

    def max_mom(tag):
        s0, x = sc.kept[tag]
        seg = ev_seg(sc, tag, s0 - secs(0.4), s0 + x.shape[1] + secs(0.4), g)
        L = loud_windows(seg, np.arange(secs(0.4), seg.shape[1] + 1, secs(0.005)))
        return float(L.max())
    Lc, Lf = max_mom('clack'), max_mom('flick')
    fl = sc.kept['flick'][1].mean(axis=0)
    f15 = smp(15) - smp(1)
    ring_db = float(10 * np.log10(np.mean(fl[f15 - secs(0.01):f15 + secs(0.01)] ** 2) / max(
        np.mean(fl[i:i + secs(0.02)] ** 2) for i in range(0, secs(0.03), secs(0.002)))))
    A['1_hook'] = dict(clack_rms50_dbfs=round(clack50, 2), max_rms50_f2_f43_dbfs=round(pre50, 2), at_frame=round(pre_at, 1),
                       margin_db=round(clack50 - pre50, 2), clack_max_momentary_lufs=round(Lc, 2), flick_max_momentary_lufs=round(Lf, 2),
                       flick_ring_at_f15_re_strike_db=round(ring_db, 1),
                       accept='CLACK 50 ms RMS >= every 50 ms window in f2-f43 + 2 dB, and its loudness >= the flick\'s',
                       passed=bool(clack50 - pre50 >= 2.0 and Lc >= Lf and ring_db <= -20.0))

    # 2 -- the withheld D5 over the PAD (f1604-f1621) and its line over the E5 through f1656
    a, b = smp(F_D5) - secs(0.5), smp(1621) + secs(0.5)
    ends = np.arange(smp(F_D5) + secs(0.1), smp(1621) + secs(0.4) + 1, secs(0.01))
    Lp = loud_windows(stems['pad'][:, a:b] * g, ends, a=a)
    Ld = loud_windows(ev_seg(sc, 'd5', a, b, g), ends, a=a)
    seg_p, seg_d = stems['pad'][:, smp(F_D5):smp(1621)] * g, ev_seg(sc, 'd5', smp(F_D5), smp(1621), g)
    Ip = loud_windows(seg_p, [seg_p.shape[1]], win=seg_p.shape[1] / SR)[0]
    Id = loud_windows(seg_d, [seg_d.shape[1]], win=seg_d.shape[1] / SR)[0]
    c0, c1 = smp(F_D5) - secs(0.2), smp(1660) + secs(0.2)
    e587, e659 = line_env_db(mono[c0:c1], 587.33), line_env_db(mono[c0:c1], 659.26)
    i0, i1 = smp(F_D5) + secs(0.05) - c0, smp(1656) - c0
    diff = e587[i0:i1 + 1] - e659[i0:i1 + 1]
    A['2_d5_over_pad'] = dict(window='f1604-f1621', d5_max_momentary_lufs=round(float(Ld.max()), 2), pad_max_momentary_lufs=round(float(Lp.max()), 2),
                              d5_minus_pad_max_momentary_lu=round(float(Ld.max() - Lp.max()), 2),
                              d5_minus_pad_loudness_over_window_lu=round(float(Id - Ip), 2),
                              line_587_minus_659_min_db_f1606_f1656=round(float(diff.min()), 2),
                              line_587_minus_659_at_f1656_db=round(float(diff[-1]), 2),
                              accept='D5 loudness within 1 LU of the PAD (or above) over f1604-f1621, and the 587 Hz line at or above 659 Hz through f1656',
                              passed=bool(Ld.max() >= Lp.max() - 1.0 and Id >= Ip - 1.0 and diff.min() >= 0.0))

    # 3 -- the f1187 absence: loudness falls >= 2 LU f1187 -> f1196, and no limiter anywhere near it
    L87, L96 = loud_windows(y, [smp(1187), smp(1196)])
    near = [c for c in info['limiter_clusters'] if c['end_s'] >= 1130 / FPS and c['start_s'] <= 1210 / FPS]
    A['3_f1187_absence'] = dict(momentary_f1187_lufs=round(float(L87), 2), momentary_f1196_lufs=round(float(L96), 2),
                                drop_lu=round(float(L87 - L96), 2), limiter_clusters_f1130_f1210=near,
                                accept='loudness drops >= 2 LU from f1187 to f1196; no limiter action in f1130-f1210',
                                passed=bool(L87 - L96 >= 2.0 and not near))

    # 4 -- the S04 push lands on its targets (DRONE 100 ms RMS on -30 -> -24, SHIMMER 50 ms peak on -36 -> -28)
    dr = stems['drone']
    r100 = run_rms_db(dr[:, smp(600):S764], 0.1)
    centre = smp(600) + np.arange(r100.size) + secs(0.05)
    tgt = lambda s: push_curve(S764 - smp(644), -30.0, -24.0)[np.clip(s - smp(644), 0, S764 - smp(644) - 1)]  # noqa: E731
    m = (centre >= smp(692)) & (centre <= S764 - secs(0.05))
    err = r100[m] - tgt(centre[m])
    at = {f'f{f}': round(float(r100[smp(f) - secs(0.05) - smp(600)]), 2) for f in (644, 700, 740)}
    at['f764 (last 100 ms)'] = round(float(r100[-1]), 2)
    s0, sh = sc.kept['shimmer644']
    pk = to_db(maximum_filter1d(np.abs(sh).max(axis=0), secs(0.05), mode='nearest'))
    sramp = push_curve(sh.shape[1], -36.0, -28.0)
    ms = slice(secs(0.65), sh.shape[1] - secs(0.025))
    serr = pk[ms] - sramp[ms]
    A['4_push'] = dict(drone_rms100_bus_dbfs=at, drone_target_f700=round(float(tgt(smp(700))), 2), drone_max_abs_err_f692_f764_db=round(float(np.abs(err).max()), 2),
                       shimmer_peak50_bus_dbfs={f'f{f}': round(float(pk[smp(f) - s0 - 1]), 2) for f in (700, 740, 764)},
                       shimmer_max_abs_err_f664_f764_db=round(float(np.abs(serr).max()), 2),
                       accept='DRONE on its -30 -> -24 dBFS ramp (+-1 dB) to the stop; SHIMMER peak on -36 -> -28 within +-1 dB',
                       passed=bool(np.abs(err).max() <= 1.0 and abs(r100[-1] + 24.0) <= 1.0 and np.abs(serr).max() <= 1.0))

    # 5 -- the rattle: integrated Euler-disk timing, 13 ticks, the bed under the ticks
    times, ideal = np.asarray(rattle_times), np.asarray(rstats['ideal'])
    dev = (times - ideal) * spin_rate(ideal)
    A['5_rattle'] = dict(ticks=int(times.size), last_tick_s=round(float(times[-1]), 4), ideal_last_tick_s=round(float(ideal[-1]), 4),
                         max_abs_deviation_of_local_period=round(float(np.abs(dev).max()), 4),
                         bed_pulses='driven by the tick times (no flam)', tick_over_bed_3_7k_min_db=round(float(min(rstats['tick_over_bed_db'])), 1),
                         accept='13 ticks where the integrated rate reaches k cycles, +-3 % of the local period; bed >= 6 dB under the ticks',
                         passed=bool(times.size == 13 and np.abs(dev).max() <= 0.0301 and min(rstats['tick_over_bed_db']) >= 6.0))

    # 6 -- the BLOOMs are heard: some 1/3-octave band above the rest of the mix in >= 30 % of the cue's frames
    blooms = {}
    for tag in ('bloom116', 'bloom380', 'bloom644', 'bloom1124'):
        s0, x = sc.kept[tag]
        e = min(s0 + min(x.shape[1], secs(3.0)), S764) if s0 < S764 else s0 + min(x.shape[1], secs(3.0))
        cue = ev_seg(sc, tag, s0, e, g)
        best, fc, frac = third_octave_snr(cue, y[:, s0:e] - cue)
        blooms[f'f{tag[5:]}'] = dict(best_band_snr_db=round(best, 1), at_hz=round(fc), frames_above_rest=round(frac, 3))
    A['6_blooms'] = dict(blooms, accept='a band above the rest in at least 30 % of frames, each BLOOM',
                         passed=bool(all(v['frames_above_rest'] >= 0.30 for v in blooms.values())))

    # 7 -- the hook is not harsh: energy above 8 kHz re the hook's total (f1-f44)
    f_, P = welch(y[:, smp(1):smp(44)], SR, nperseg=8192, axis=-1)
    P = P.mean(axis=0)
    hf = float(10 * np.log10(P[f_ >= 8000].sum() / P.sum()))
    A['7_hook_hf'] = dict(above_8k_re_hook_total_db=round(hf, 1), accept='at most -25 dB', passed=bool(hf <= -25.0))

    # 8 -- the SUB moments on a phone (4th-order high-pass at 200 Hz)
    yh = sosfilt(butter(4, 200.0, 'high', fs=SR, output='sos'), y, axis=-1)
    Lr = loud_windows(yh, [smp(1428)], win=0.3)[0]
    Ls = loud_windows(yh, [smp(1440)], win=(smp(1440) - smp(1428)) / SR)[0]
    s0, sw = sc.kept['swell']
    swb = sosfilt(butter(4, [150.0, 400.0], 'band', fs=SR, output='sos'), sw * g, axis=-1)
    swh = sosfilt(butter(4, 200.0, 'high', fs=SR, output='sos'), sw * g, axis=-1)
    best, fc, frac = third_octave_snr(swh[:, :secs(2.5)], yh[:, s0:s0 + secs(2.5)] - swh[:, :secs(2.5)])
    A['8_sub_on_a_phone'] = dict(hp200_riser_last_300ms_lufs=round(float(Lr), 2), hp200_f1428_f1440_lufs=round(float(Ls), 2),
                                 plunge_minus_riser_lu=round(float(Ls - Lr), 2),
                                 swell_150_400hz_max_rms100_dbfs=round(float(run_rms_db(swb, 0.1).max()), 1),
                                 swell_hp200_best_band_snr_db=round(best, 1), swell_hp200_frames_above_rest=round(frac, 3),
                                 accept='through a 200 Hz high-pass, f1428-f1440 at least 3 LU louder than the riser\'s last 300 ms',
                                 passed=bool(Ls - Lr >= 3.0))

    # 9 -- every router ping reads at its fundamental: >= 10 dB over the 1.594 mode across 0-0.8 s
    pings = []
    for k, (coin, f, nm, x) in enumerate(PINGS):
        m_ = sc.kept[f'ping{k + 1}'][1].mean(axis=0)
        d = line_env_db(m_, f, 0.02) - line_env_db(m_, f * 1.594, 0.02)
        pings.append(round(float(d[secs(0.01):secs(0.8)].min()), 1))
    A['9_pings'] = dict(min_fundamental_over_1594_mode_db=pings, frames=list(LANDS),
                        accept='fundamental >= 10 dB over the 1.594 mode across 0-0.8 s, all 12', passed=bool(min(pings) >= 10.0))

    # 10 -- the drone's F# (5th-harmonic) and flat-C (7th) lines are notched on both segments
    ref, cut = drone_voices(6.0, notches=False), drone_voices(6.0)
    rm, cm = sum(ref.values()).mean(axis=0), sum(cut.values()).mean(axis=0)
    depth = {f'{f0:.2f}': round(tone_amp_db(rm, secs(1), secs(6), f0) - tone_amp_db(cm, secs(1), secs(6), f0), 1) for f0, _ in DRONE_NOTCHES}
    dm = stems['drone'].mean(axis=0)
    lines = {f'{seg}_{f0:.2f}': round(tone_amp_db(dm, smp(a_), smp(b_), f0) + info['master_gain_db'], 1)
             for seg, a_, b_ in (('A_f400_f640', 400, 640), ('B_f1210_f1420', 1210, 1420)) for f0 in (183.55, 367.10, 734.20)}
    rough = dict(f650_f760_felt_F4_349=round(tone_amp_db(mono, smp(650), smp(760), 349.23), 1),
                 f650_f760_drone_367=round(tone_amp_db(mono, smp(650), smp(760), 367.10), 1))
    A['10_drone_notches'] = dict(notch_depth_db=depth, delivered_drone_lines_dbfs=lines, s04_349_vs_367_dbfs=rough,
                                 accept='F# lines -15 dB and 7th-harmonic lines -10 dB (Q 12) on both segments',
                                 passed=bool(all(depth[f'{f0:.2f}'] >= (13.0 if gdb <= -15 else 8.5) for f0, gdb in DRONE_NOTCHES)))

    # 11 -- one uniform master gain, no limiter anywhere
    A['11_pure_gain'] = dict(master_gain_db=info['master_gain_db'], limiter_clusters=info['limiter_clusters'],
                             convention='cue levels are mix-bus levels (score_cues.json); the master is one uniform gain',
                             accept='limiter_clusters empty: the master is a pure gain', passed=bool(not info['limiter_clusters']))

    # ---- the task's level hierarchy: the CLACK and the plunge SUB are the loudest events of the film
    up = resample_poly(y, 4, 1, axis=1)
    env = np.abs(up).max(axis=0)[:4 * N].reshape(-1, 4).max(axis=1)
    wc, ws = slice(s44 - secs(0.01), s44 + secs(0.3)), slice(smp(1428) - secs(0.01), smp(1428) + secs(0.6))
    tpc, tps = float(to_db(env[wc].max())), float(to_db(env[ws].max()))
    rest = env.copy()
    rest[wc] = 0.0
    rest[ws] = 0.0
    tpr = float(to_db(rest.max()))
    blk = secs(0.5)
    bl = to_db(env[:N // blk * blk].reshape(-1, blk).max(axis=1))
    top = [dict(frame=round(i * blk / SPF), tp_dbtp=round(float(bl[i]), 2)) for i in np.argsort(bl)[::-1][:8]]
    c56 = slice(smp(1156), smp(1156) + secs(0.4))
    chord_tp, chord50 = float(to_db(env[c56].max())), float(r50[smp(1156):smp(1156) + secs(0.35)].max())
    casc_tp = float(to_db(env[smp(1136):smp(1200)].max()))
    st_ends = np.arange(secs(3.0), N + 1, secs(0.1))
    Lst = loud_windows(y, st_ends, win=3.0)
    is_casc = (st_ends > smp(1136)) & (st_ends <= smp(1200) + secs(3.0))
    is_s08 = st_ends > smp(F_RELAY)
    Lmax = float(Lst.max())
    A['loudest_events'] = dict(
        clack_tp_dbtp=round(tpc, 2), plunge_sub_tp_dbtp=round(tps, 2), max_tp_elsewhere_dbtp=round(tpr, 2), loudest_half_seconds=top,
        chord_f1156_tp_dbtp=round(chord_tp, 2), chord_f1156_max_rms50_dbfs=round(chord50, 2), cascade_f1136_f1200_tp_dbtp=round(casc_tp, 2),
        max_short_term_lufs=round(Lmax, 2), loudest_passage_ends_at_frame=round(int(st_ends[np.argmax(Lst)]) / SPF),
        cascade_max_short_term_lufs=round(float(Lst[is_casc].max()), 2), s08_max_short_term_lufs=round(float(Lst[is_s08].max()), 2),
        accept='CLACK and plunge SUB above every other true peak; the f1156 chord under the CLACK (peak and 50 ms RMS); '
               'the cascade not the loudest passage (3 s short-term loudness)',
        passed=bool(tpr < min(tpc, tps) and chord_tp < tpc and chord50 < clack50 and Lst[is_casc].max() < Lmax))
    return A


def measure(path, sc, stems, rattle_times, rstats, info):
    data, sr = sf.read(path, dtype='int32', always_2d=True)
    meta = sf.info(path)
    q = data.T.astype(np.int64) >> 8                         # back to 24-bit integers
    y = q / 8388608.0
    L, R = y
    mono = 0.5 * (L + R)
    rep = dict(file=os.path.relpath(path, ROOT), sample_rate=sr, channels=meta.channels, subtype=meta.subtype,
               samples=int(y.shape[1]), expected_samples=N, duration_s=round(y.shape[1] / SR, 4),
               timing='DESIGN_BIBLE §8.2 as re-timed by f2/prod/CUES_v2.md (router landings from geom.LANDS)')
    meter = pyln.Meter(SR)
    rep['integrated_lufs'] = round(float(meter.integrated_loudness(y.T)), 2)
    rep['true_peak_dbtp'] = round(S.true_peak_db(y, 4), 2)
    rep['true_peak_method'] = '4x oversampling, scipy.signal.resample_poly, max over both channels'
    rep['sample_peak_dbfs'] = round(float(to_db(np.abs(y).max())), 2)
    rep['clipped_samples'] = int(np.sum(np.abs(q) >= 8388607))
    rep['dc_offset'] = [float(f'{v:.2e}') for v in y.mean(axis=1)]
    z = q[:, S764:S776]
    nzb = np.flatnonzero(np.any(q[:, :S764] != 0, axis=0))
    nza = np.flatnonzero(np.any(q[:, S776:] != 0, axis=0))
    rep['zero_window'] = dict(frames='f764-f775', first_sample=S764, last_sample=S776 - 1, samples=int(z.shape[1]),
                              all_exact_zero=bool(np.all(z == 0)), nonzero_count=int(np.count_nonzero(z)),
                              last_nonzero_before=int(nzb[-1]) if nzb.size else None,
                              first_nonzero_after=int(S776 + nza[0]) if nza.size else None)
    # D5 587.33 Hz after f1604 (the withheld 12th note)
    s = smp(F_D5)
    before = tone_amp_db(mono, s - secs(0.52), s - secs(0.02), 587.33)
    after = tone_amp_db(mono, s + secs(0.02), s + secs(0.52), 587.33)
    rep['d5_presence_f1604'] = dict(freq_hz=587.33, window_before_s=[round((s - secs(0.52)) / SR, 3), round((s - secs(0.02)) / SR, 3)],
                                    window_after_s=[round((s + secs(0.02)) / SR, 3), round((s + secs(0.52)) / SR, 3)],
                                    level_before_dbfs=round(before, 1), level_after_dbfs=round(after, 1), rise_db=round(after - before, 1),
                                    spectral_peak_hz_570_605=round(peak_freq(mono, s + secs(0.02), s + secs(1.02), 570, 605), 2))
    # f1187: no new onset. References: the six sheet arrivals and windows after the cascade where certainly nothing
    # starts. Same 40 ms window for all; SuperFlux strength.
    s87 = smp(F_NO_NOTE)
    ends, sfx = superflux(mono, smp(1120), smp(1230))

    def strength(sk, w=0.04):
        m = (ends >= sk) & (ends <= sk + secs(w))
        return float(sfx[m].max())
    cells = [strength(smp(f)) for f, _ in SHEET]
    bg = [strength(smp(f)) for f in range(1189, 1216)]          # every frame after the absence, f1189-f1215
    v87 = strength(s87)
    med = float(np.median(bg))
    mad = 1.4826 * float(np.median(np.abs(np.asarray(bg) - med)))
    z = lambda v: (v - med) / mad  # noqa: E731   robust z-score against the post-cascade background
    hpm = filt(mono[s87 - secs(0.6):s87 + secs(0.6)], 'high', 150.0)
    c = secs(0.6)
    e_before = to_db(np.sqrt(np.mean(hpm[c - secs(0.1):c] ** 2)))
    e_after = to_db(np.sqrt(np.mean(hpm[c:c + secs(0.1)] ** 2)))
    d5b = tone_amp_db(mono, s87 - secs(0.3), s87, 587.33)
    d5a = tone_amp_db(mono, s87, s87 + secs(0.3), 587.33)
    L87, L96 = loud_windows(y, [s87, smp(1196)])
    rep['f1187_no_onset'] = dict(
        superflux_f1187=round(v87, 2), superflux_sheet_arrivals=[round(v, 2) for v in cells], sheet_arrival_frames=[f for f, _ in SHEET],
        superflux_arrivals_median=round(float(np.median(cells)), 2), superflux_background_f1189_f1215_max=round(max(bg), 2),
        superflux_background_median=round(med, 2), robust_z_f1187=round(z(v87), 2), robust_z_arrivals=[round(z(v), 2) for v in cells],
        robust_z_background_max=round(z(max(bg)), 2), arrivals_detected_z_ge_3=int(sum(z(v) >= 3.0 for v in cells)),
        events_logged_f1180_f1200=[c['cue'] for c in sc.cues if 1180 <= c['frame'] <= 1200 and not c['cue'].startswith('NO NOTE')],
        hp150_level_100ms_before_dbfs=round(float(e_before), 2), hp150_level_100ms_after_dbfs=round(float(e_after), 2),
        d5_587_before_dbfs=round(d5b, 1), d5_587_after_dbfs=round(d5a, 1),
        momentary_f1187_lufs=round(float(L87), 2), momentary_f1196_lufs=round(float(L96), 2), loudness_drop_lu=round(float(L87 - L96), 2),
        no_onset=bool(z(v87) < 3.0 and v87 < float(np.median(cells)) and e_after <= e_before + 0.5 and d5a <= d5b + 1.0
                      and not any(1180 <= c['frame'] <= 1200 and not c['cue'].startswith('NO NOTE') for c in sc.cues)),
        note='SuperFlux (40 ms window from each frame): f1187 must not be an outlier against the post-cascade background '
             '(robust z < 3, where every sheet arrival scores z >= 3), no event is logged f1180-f1200, the HP150 level and the '
             '587.33 Hz (D5) component must not rise, and the momentary loudness must fall >= 2 LU by f1196')

    # correlation / mono compatibility
    def corr(st, a=0, b=None):
        l, r = st[0, a:b], st[1, a:b]
        return round(float(np.corrcoef(l, r)[0, 1]), 3)

    def mono_loss(st, a=0, b=None):
        l, r = st[0, a:b], st[1, a:b]
        return round(float(10 * np.log10(np.mean((l + r) ** 2) / (2 * np.mean(l * l + r * r)))), 2)
    act = slice(smp(870), smp(1100))
    act2 = slice(smp(1600), smp(1680))
    rep['correlation'] = dict(
        mix_lr=corr(y), mix_mono_sum_loss_db=mono_loss(y),
        pad_bb_lr=corr(stems['pad'][:, act]), pad_bb_mono_sum_loss_db=mono_loss(stems['pad'][:, act]),
        pad_dmaj_lr=corr(stems['pad'][:, act2]), pad_dmaj_mono_sum_loss_db=mono_loss(stems['pad'][:, act2]),
        room_lr=corr(stems['room'][:, :S764]), room_mono_sum_loss_db=mono_loss(stems['room'][:, :S764]),
        felt_lr=corr(stems['felt']), drone_lr=corr(stems['drone']),
        note='mono_sum_loss = 10 log10(E[(L+R)^2] / 2E[L^2+R^2]): 0 dB identical, -3 dB uncorrelated, below -3 dB cancels')
    # sample lock, measured in the written file for every cue with a transient onset (beds that fade in from silence
    # are not measurable this way: periodic waveforms make the peak ambiguous); and the first sample of every event
    transient = ('COIN', 'WHIRR', 'RATTLE', 'CLACK', 'PING', 'STAMP', 'RELAY', 'SUB sub_hit', 'DRAW', 'RISER', 'ROOM back', 'FELT')
    gx = undb(info['master_gain_exact_db'])
    km = {t: (s0, 0.5 * (x[0] + x[1])) for t, (s0, x) in sc.kept.items()}
    locks = []
    for fr, cue, ref, tag in sorted(sc.refs, key=lambda r: r[0]):
        if not cue.startswith(transient):
            continue
        s, a0 = smp(fr), smp(fr) - 241
        seg = mono[a0:s + 240 + ref.size].copy()
        gone = []
        for t, (s0, xm) in km.items():          # cancel the other logged events heard in this window (as logged)
            lo, hi = max(a0, s0), min(a0 + seg.size, s0 + xm.size)
            if t != tag and hi > lo:
                seg[lo - a0:hi - a0] -= gx * xm[lo - s0:hi - s0]
                gone.append(t)
        lag = matched_lag(mono, ref, s, seg=seg)
        locks.append(dict(frame=fr, sample=s, cue=cue, lag_samples=round(lag, 2), raw_lag_samples=round(matched_lag(mono, ref, s), 2),
                          cancelled=len(gone)))
    rep['placement_matched_filter'] = locks
    rep['placement_note'] = ("lag = offset in samples of the peak of the cross-correlation between each transient cue's own first 200 ms "
                             "(pre-emphasised) and the written mix, +-5 ms around round(f*1600), parabolic sub-sample refinement, after the "
                             "other logged events that sound in that window are cancelled from the file at their logged places (chord "
                             "partners, a same-pitch ping still ringing, the whirr's release under the rattle); raw_lag_samples = without "
                             "the cancellation. A wrongly placed cue would still show its own offset. Tolerance 1.5 samples (the parabolic "
                             "estimate on a near-sinusoidal ping wanders by about a sample)")
    rep['placement_max_abs_lag_samples'] = round(max(abs(l['lag_samples']) for l in locks), 2)
    mb = sum(stems.values())
    mb[:, S764:S776] = 0.0
    dev = np.abs(q - np.round(mb * undb(info['master_gain_exact_db']) * 8388607.0)).max()
    rep['file_equals_gain_times_mix_bus'] = dict(max_abs_deviation_lsb=int(dev), passed=bool(dev <= 1),
                                                 note='the written file is round(master gain x the mix bus) to 1 LSB everywhere: '
                                                      'a pure gain, so every event sits where it was placed')
    rep['event_first_samples'] = dict(events=len(sc.onsets), all_placed_at_round_f_x_1600=bool(all(s0 == smp(f) for f, _, s0, _ in sc.onsets)),
                                      max_offset_of_first_nonzero_sample=max(o for _, _, _, o in sc.onsets if o is not None))
    dr = stems['drone']
    rep['drone_dip_f1187_db'] = round(float(20 * np.log10(rms_of(dr, smp(1190), smp(1199)) / rms_of(dr, smp(1170), smp(1187)))), 2)
    rep['all_cues_sample_locked'] = bool(all(c['sample'] == round(c['frame'] * SPF) for c in sc.cues))
    rep['cue_count'] = len(sc.cues)
    rep['rattle_ticks'] = len(rattle_times)
    rep['rattle_last_tick_s'] = round(float(rattle_times[-1]), 4)
    rep['clack_s'] = round(T_CLACK, 4)
    rep.update(info)
    frames = sorted({c['frame'] for c in sc.cues})
    want = dict(pings=list(LANDS), slit2=[F_SLIT2], draw=[F_DRAW[0]], stamps=list(F_STAMPS), sheet=[f for f, _ in SHEET],
                drone_out=[F_DRONE_OUT[0]], relay=[F_RELAY], hum_pad=[F_LIGHT], d5=[F_D5], ting=[F_TING], hold=[F_HOLD[0]])
    rep['cues_v2'] = dict(want, all_present=bool(all(f in frames for v in want.values() for f in v)),
                          pad_ride=dict(down=[PAD_RIDE[0], PAD_RIDE[1]], up=[PAD_RIDE[2], PAD_RIDE[3]], db=PAD_RIDE[4]))
    rep['levels_note'] = ('cue gain_dbfs values are mix-bus levels: RMS where the bible says RMS (ROOM, WHIRR, DRONE, SLIT, PAD) and for '
                          'the BLOOMs (review fix 6), sample peak otherwise. Delivered file = mix-bus + master_gain_db, one uniform gain '
                          '(review fix 11; no limiter acts). The hook group carries hook_group_offset_db so the CLACK is the file\'s peak '
                          '(CLACK_DBTP), and the plunge SUB carries plunge_sub_offset_db so it lands with it (SUB_DBTP); both are '
                          'already included in the logged gain_dbfs')
    rep['interpretations'] = [
        'cue timing: f2/prod/CUES_v2.md wherever it differs from §8.2 (pings at geom.LANDS, SLIT f300, DRAW f950, STAMPs f968/f992/f1016, '
        'sheet notes in arrival order as chords f1136-f1179, DRONE out f1568, RELAY f1580, HUM + PAD f1581, D5 f1604, ting f1700, hold f1712)',
        'DRONE returns with the f1124 pull-back (1.5 s fade): the bible cuts it at f764 and dips it at f1187 but never says when it comes back',
        'unlabelled dBFS levels (RISER, DRAW, SHIMMER, STAMP, RELAY, COIN, PING, FELT) are sample peak, so CLACK and the plunge SUB stay the loudest (§8.3)',
        'SUB swell (f860) at -20 dBFS peak: no level given; kept under the -14 dBFS plunge SUB',
        'velocities not given: A3 and F3 0.50, sheet notes 0.52 (single) / 0.48 (pairs) / 0.45 (the four-note chord), dyad 0.45',
        'piano wet -14 dB and coin wet -18 dB are wet/dry energy ratios: 0.3 send into unit-energy room IRs',
        'FELT pan: player-side spread by pitch (+-0.3); the sheet notes are panned where their cells are on screen when they develop',
        'the f300 SLIT swell: 600 -> 2400 Hz over the slit\'s second move (0.6 s), 6 dB under the f260 one',
        'router pings keep the §3.3 table\'s pans (CUES_v2: same coins, notes and pans) and its -22 dBFS (last -20); a call landing 6 f '
        'after the previous one plays 2 dB lighter, so the accelerando\'s piled-up rings stay under the CLACK and the SUB',
        'ROOM: -52 inside the plate, back to -46 once the table is lit (f1581, over the pull-out to f1628)',
        'PAD D major add9 attack 0.8 s from the switch (§8.1: 0.8-1.0 s); the HUM has no fade-in (a 3 ms de-click and a +3 dB inrush)',
        'the final f1712 -> f1795 fade to ROOM also carries the D5 tail, the coin ting and the reverb returns']
    lr = rep['correlation']
    rep['review_fixes'] = REVIEW_FIXES
    rep['review_acceptance'] = review_acceptance(y, sc, stems, info, rattle_times, rstats)
    ra = rep['review_acceptance']
    rep['checks'] = dict(
        length_exact=rep['samples'] == N, format_48k_24bit_stereo=(sr == SR and meta.channels == 2 and meta.subtype == 'PCM_24'),
        lufs_within_0_5=abs(rep['integrated_lufs'] - LUFS_TARGET) <= 0.5, true_peak_le_minus_1=rep['true_peak_dbtp'] <= -1.0,
        no_clipping=rep['clipped_samples'] == 0, zeros_f764_f775=rep['zero_window']['all_exact_zero'],
        d5_present_after_f1604=rep['d5_presence_f1604']['rise_db'] >= 20 and abs(rep['d5_presence_f1604']['spectral_peak_hz_570_605'] - 587.33) < 1.5,
        d5_audible_over_pad=ra['2_d5_over_pad']['passed'],
        no_onset_f1187=rep['f1187_no_onset']['no_onset'] and rep['f1187_no_onset']['loudness_drop_lu'] >= 2.0,
        mono_compatible=(lr['pad_bb_lr'] > 0.3 and lr['pad_dmaj_lr'] > 0.3 and lr['room_lr'] > 0.5 and lr['mix_mono_sum_loss_db'] > -3.0),
        stop_and_return_on_frame=(rep['zero_window']['last_nonzero_before'] == S764 - 1 and rep['zero_window']['first_nonzero_after'] == S776),
        cues_sample_locked=(rep['all_cues_sample_locked'] and rep['placement_max_abs_lag_samples'] <= 1.5
                            and rep['event_first_samples']['all_placed_at_round_f_x_1600']
                            and rep['event_first_samples']['max_offset_of_first_nonzero_sample'] <= 1
                            and rep['file_equals_gain_times_mix_bus']['passed']),
        cues_v2_frames=rep['cues_v2']['all_present'],
        clack_and_sub_loudest=ra['loudest_events']['passed'] and ra['1_hook']['passed'],
        master_pure_gain=ra['11_pure_gain']['passed'],
        review_acceptance_all=all(v['passed'] for v in ra.values()))
    rep['checks'] = {k: bool(v) for k, v in rep['checks'].items()}
    rep['all_pass'] = bool(all(rep['checks'].values()))
    return rep, y


# ---------------------------------------------------------------- spectrogram pictures (numpy + PIL)
_CM = np.array([(0.0, 0, 0, 4), (0.13, 22, 11, 57), (0.28, 66, 10, 104), (0.42, 114, 25, 110), (0.55, 159, 42, 99),
                (0.68, 204, 66, 72), (0.80, 238, 105, 37), (0.90, 250, 160, 30), (0.96, 245, 215, 72), (1.0, 252, 255, 164)])


def spectrogram_png(x, path, t0, t1, title, marks=(), W=2400, H=720, fmin=30.0, fmax=20000.0, nfft=4096,
                    dbr=(-115.0, -20.0), tick=5.0, env_strip=True):
    x = np.asarray(x, np.float64)
    s0, s1 = int(t0 * SR), int(t1 * SR)
    xp = np.pad(x, (nfft // 2, nfft // 2))
    centres = s0 + np.round(np.arange(W) * (s1 - s0) / W).astype(int)      # exact, no integer-hop drift
    fr = np.lib.stride_tricks.sliding_window_view(xp, nfft)[centres]
    D = 20 * np.log10(np.abs(np.fft.rfft(fr * np.hanning(nfft), axis=1)) / (nfft / 4) + 1e-12)
    fq = np.fft.rfftfreq(nfft, 1 / SR)
    rows = np.geomspace(fmax, fmin, H)
    img = np.stack([np.interp(rows, fq, D[i]) for i in range(D.shape[0])], axis=1)
    v = np.clip((img - dbr[0]) / (dbr[1] - dbr[0]), 0, 1)
    rgb = np.stack([np.interp(v, _CM[:, 0], _CM[:, c + 1]) for c in range(3)], axis=-1).astype(np.uint8)
    w = rgb.shape[1]
    Lm, T, B, Rm, E = 70, 34, 40, 14, (110 if env_strip else 0)
    canvas = Image.new('RGB', (Lm + w + Rm, T + H + E + B), (14, 13, 12))
    canvas.paste(Image.fromarray(rgb), (Lm, T))
    d = ImageDraw.Draw(canvas)
    font, small = ImageFont.load_default(size=15), ImageFont.load_default(size=12)
    d.text((Lm, 9), title, fill=(236, 230, 218), font=font)
    for f in (50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000):
        if fmin <= f <= fmax:
            yy = T + int(round((np.log(fmax) - np.log(f)) / (np.log(fmax) - np.log(fmin)) * (H - 1)))
            d.line([(Lm - 6, yy), (Lm, yy)], fill=(200, 200, 200))
            d.text((8, yy - 7), f'{f / 1000:g}k' if f >= 1000 else f'{f}', fill=(200, 200, 200), font=small)
    if env_strip:                                     # short-term level (dBFS, 50 ms) under the spectrogram
        h = secs(0.05)
        seg = x[max(0, s0 - h // 2):s1 + h // 2]
        cc = np.concatenate([[0.0], np.cumsum(seg * seg)])
        e = 10 * np.log10((cc[h:] - cc[:-h]) / h + 1e-14)
        idx = np.clip(centres - max(0, s0 - h // 2) - h // 2, 0, e.size - 1)
        top, bot = T + H + 8, T + H + E - 4
        for lv in (-60, -40, -20, 0):
            yy = int(top + (0 - lv) / 70 * (bot - top))
            d.line([(Lm, yy), (Lm + w, yy)], fill=(48, 46, 44))
            d.text((18, yy - 7), f'{lv}', fill=(150, 150, 150), font=small)
        pts = [(Lm + i, int(top + (0 - np.clip(e[j], -70, 0)) / 70 * (bot - top))) for i, j in enumerate(idx)]
        d.line(pts, fill=(236, 200, 120), width=1)
    k = np.ceil(t0 / tick) * tick
    yb = T + H + E
    while k <= t1 + 1e-9:
        xx = Lm + int(round((k - t0) / (t1 - t0) * w))
        d.line([(xx, yb), (xx, yb + 6)], fill=(200, 200, 200))
        d.text((xx - 12, yb + 9), f'{k:g}s', fill=(200, 200, 200), font=small)
        k += tick
    for tt, lab in marks:
        if t0 <= tt <= t1:
            xx = Lm + int(round((tt - t0) / (t1 - t0) * w))
            for yy in range(T, T + H + E, 7):
                d.line([(xx, yy), (xx, yy + 2)], fill=(120, 220, 255))
            d.text((xx + 3, T + 3), lab, fill=(120, 220, 255), font=small)
    canvas.save(path)


# ---------------------------------------------------------------- main
def render():
    """compose -> reverb -> end fade -> hook level -> master. Returns (sc, stems at bus level, delivered y, info,
    rattle tick times, rattle stats)."""
    sc, rattle_times, rstats = compose()
    ret = sc.reverb_returns()
    stems = dict(sc.stems)
    stems['rev_music'], stems['rev_coin'], stems['rev_hook'] = ret['music'], ret['coin'], ret['hook']
    # f1712 -> f1795 (CUES_v2 hold, one beat later after review): everything but the room fades to the room
    fade = np.ones(N)
    a, b = smp(F_HOLD[0]), smp(F_HOLD[1])
    fade[a:b] = ramp_out(b - a)
    fade[b:] = 0.0
    for k in stems:
        if k != 'room':
            stems[k] = stems[k] * fade
    meter = pyln.Meter(SR)
    # The CLACK is the hook and the loudest peak of the film (§1, §8.3). At the cue sheet's -10 dBFS it would sit
    # above the ceiling after the uniform master gain that -16 LUFS needs, so the hook group (flick, whirr, rattle,
    # CLACK and their room, in the cue sheet's own balance) moves as one until the CLACK lands at CLACK_DBTP. The
    # master then stays a pure gain (no limiting anywhere).
    # The plunge SUB (§8.3: the other loudest event) is levelled the same way, to SUB_DBTP just under the CLACK
    # (with the drone's D1 under it, its -14 dBFS bus peak would sit on the ceiling).
    k_db, u_db = 0.0, 0.0
    wc, ws = slice(smp(43), smp(48)), slice(smp(1428) - secs(0.01), smp(1428) + secs(0.6))
    for _ in range(8):
        mix = sum(stems.values())
        mix[:, S764:S776] = 0.0
        g_db = LUFS_TARGET - float(meter.integrated_loudness(mix.T))
        dc = CLACK_DBTP - g_db - S.true_peak_db(mix[:, wc], 4)
        ds = SUB_DBTP - g_db - S.true_peak_db(mix[:, ws], 4)
        if abs(dc) < 0.003 and abs(ds) < 0.003:
            break
        stems['hook'] = stems['hook'] * undb(dc)
        stems['rev_hook'] = stems['rev_hook'] * undb(dc)
        stems['sub'] = stems['sub'] * undb(ds)
        k_db, u_db = k_db + dc, u_db + ds
    mix = sum(stems.values())
    mix[:, S764:S776] = 0.0
    for tag in ('flick', 'whirr', 'rattle', 'clack'):
        s0, xk = sc.kept[tag]
        sc.kept[tag] = (s0, xk * undb(k_db))
    s0, xk = sc.kept['plunge']
    sc.kept['plunge'] = (s0, xk * undb(u_db))
    for c in sc.cues:
        if c['cue'].startswith(('COIN flick', 'WHIRR', 'RATTLE', 'CLACK')):
            c['gain_dbfs'] = round(c['gain_dbfs'] + k_db, 2)
        if c['cue'].startswith('SUB sub_hit'):
            c['gain_dbfs'] = round(c['gain_dbfs'] + u_db, 2)
    mix_lufs = float(meter.integrated_loudness(mix.T))
    y, info = master(mix, meter)
    info['mix_bus_lufs'] = round(mix_lufs, 2)
    info['hook_group_offset_db'] = round(k_db, 2)
    info['clack_bus_peak_dbfs'] = round(-10.0 + k_db, 2)
    info['plunge_sub_offset_db'] = round(u_db, 2)
    info['plunge_sub_bus_peak_dbfs'] = round(-14.0 + u_db, 2)
    return sc, stems, y, info, rattle_times, rstats


def main():
    t_start = time.time()
    os.makedirs(OUT, exist_ok=True)
    sc, stems, y, info, rattle_times, rstats = render()
    wav = os.path.join(OUT, 'score.wav')
    write_wav(y, wav)
    with open(os.path.join(OUT, 'score_cues.json'), 'w') as f:
        json.dump(sc.cues, f, ensure_ascii=False, indent=1)
    rep, yr = measure(wav, sc, stems, rattle_times, rstats, info)
    rep['render_seconds'] = round(time.time() - t_start, 1)
    with open(os.path.join(OUT, 'score_report.json'), 'w') as f:
        json.dump(rep, f, ensure_ascii=False, indent=1)
    mono = 0.5 * (yr[0] + yr[1])
    marks = [(1 / 30, 'f1'), (T_CLACK, 'f44 CLACK'), (smp(380) / SR, 'f380'), (smp(LANDS[0]) / SR, f'f{LANDS[0]} pings'),
             (S764 / SR, 'f764 STOP'), (S776 / SR, 'f776'), (smp(860) / SR, 'f860'), (smp(SHEET[0][0]) / SR, f'f{SHEET[0][0]}'),
             (smp(F_NO_NOTE) / SR, 'f1187 (no note)'), (smp(1388) / SR, 'f1388'), (smp(1428) / SR, 'f1428'),
             (smp(F_RELAY) / SR, f'f{F_RELAY}'), (smp(F_D5) / SR, f'f{F_D5} D5')]
    spectrogram_png(mono, os.path.join(OUT, 'score_spec.png'), 0.0, N / SR,
                    f'score.wav  {rep["integrated_lufs"]} LUFS  TP {rep["true_peak_dbtp"]} dBTP  (mono sum, log f)', marks, W=2400, tick=5.0)
    hook_marks = [(1 / 30, 'f1 flick'), (2 / 30, 'f2'), (0.5, 'f15 rattle'), (T_CLACK, 'f44 CLACK'), (53 / 30, 'f53 drone'), (54 / 30, 'f54 D3')]
    spectrogram_png(mono, os.path.join(OUT, 'score_hook_spec.png'), 0.0, 4.0, 'hook 0-4 s (mono sum)', hook_marks,
                    W=2000, nfft=2048, tick=0.25)
    print(json.dumps({k: rep[k] for k in ('integrated_lufs', 'true_peak_dbtp', 'sample_peak_dbfs', 'master_gain_db',
                                         'limiter_max_reduction_db', 'checks', 'all_pass', 'render_seconds')}, indent=1))
    print(json.dumps({k: v.get('passed') for k, v in rep['review_acceptance'].items()}, indent=1))
    return 0 if rep['all_pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
