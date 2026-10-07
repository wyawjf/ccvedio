"""Synthesize the voice-over line by line and write vo.wav + timeline.json.

usage: python3 tts.py <kokoro_model_dir> <script.json> <out_dir> [sid] [speed]
"""
import sys, os, json, numpy as np, sherpa_onnx, soundfile as sf
from scipy.signal import resample_poly

M, SCRIPT, OUT = sys.argv[1:4]
SID = int(sys.argv[4]) if len(sys.argv) > 4 else 60
SPEED = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0
SR = 48000
LEAD_IN = 0.9  # seconds of silence before the first line (room for the opening hit)

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


def trim(x, sr, thresh=0.01, pad=0.04):
    env = np.convolve(np.abs(x), np.ones(int(0.01 * sr)) / int(0.01 * sr), "same")
    idx = np.where(env > thresh)[0]
    if len(idx) == 0:
        return x
    a = max(0, idx[0] - int(pad * sr)); b = min(len(x), idx[-1] + int(pad * sr))
    return x[a:b]


script = json.load(open(SCRIPT))
os.makedirs(OUT, exist_ok=True)
chunks = [np.zeros(int(LEAD_IN * SR), np.float32)]
t = LEAD_IN
timeline = []
for line in script["lines"]:
    a = tts.generate(line["tts"], sid=SID, speed=SPEED)
    x = np.array(a.samples, dtype=np.float32)
    x = resample_poly(x, SR, a.sample_rate).astype(np.float32)
    x = trim(x, SR)
    # short fades so trimmed edges never click
    f = int(0.008 * SR); x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
    dur = len(x) / SR
    timeline.append({**line, "start": round(t, 3), "end": round(t + dur, 3)})
    chunks += [x, np.zeros(int(line["pause"] * SR), np.float32)]
    t += dur + line["pause"]
    print(f'{line["id"]:9s} {timeline[-1]["start"]:6.2f} -> {timeline[-1]["end"]:6.2f}  ({dur:.2f}s)')

vo = np.concatenate(chunks)
vo = vo / (np.abs(vo).max() + 1e-9) * 0.89
sf.write(f"{OUT}/vo.wav", vo, SR)
json.dump({"duration": round(len(vo) / SR, 3), "sid": SID, "speed": SPEED, "lines": timeline},
          open(f"{OUT}/timeline.json", "w"), ensure_ascii=False, indent=1)
print("total", round(len(vo) / SR, 2), "s")
