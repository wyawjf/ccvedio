"""Synthesize one sentence with many Kokoro voices and report pitch/duration stats."""
import sys, os, numpy as np, sherpa_onnx, soundfile as sf

M = sys.argv[1]
OUT = sys.argv[2]
sids = [int(s) for s in sys.argv[3].split(",")]
os.makedirs(OUT, exist_ok=True)
cfg = sherpa_onnx.OfflineTtsConfig(
    model=sherpa_onnx.OfflineTtsModelConfig(
        kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(
            model=f"{M}/model.onnx", voices=f"{M}/voices.bin", tokens=f"{M}/tokens.txt",
            data_dir=f"{M}/espeak-ng-data", dict_dir=f"{M}/dict",
            lexicon=f"{M}/lexicon-us-en.txt,{M}/lexicon-zh.txt"),
        num_threads=4),
    rule_fsts=f"{M}/date-zh.fst,{M}/phone-zh.fst,{M}/number-zh.fst",
    max_num_sentences=1)
tts = sherpa_onnx.OfflineTts(cfg)
print("num speakers", tts.num_speakers)
text = "这不是高潮。这只是预告片。人类花了几十万年，学会活下去。"

def f0(x, sr):
    fr = int(0.04 * sr); hop = int(0.01 * sr); vals = []
    for i in range(0, len(x) - fr, hop):
        w = x[i:i + fr]
        if np.sqrt(np.mean(w ** 2)) < 0.02: continue
        w = w - w.mean(); ac = np.correlate(w, w, "full")[fr - 1:]
        lo, hi = int(sr / 400), int(sr / 60)
        k = lo + np.argmax(ac[lo:hi])
        if ac[k] > 0.3 * ac[0]: vals.append(sr / k)
    return np.median(vals) if vals else 0

for sid in sids:
    a = tts.generate(text, sid=sid, speed=1.0)
    x = np.array(a.samples, dtype=np.float32)
    sf.write(f"{OUT}/sid{sid}.wav", x, a.sample_rate)
    print(f"sid={sid} dur={len(x)/a.sample_rate:.2f}s f0={f0(x, a.sample_rate):.0f}Hz peak={np.abs(x).max():.2f}")
