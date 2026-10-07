"""Transcribe each voice-over line back with SenseVoice to catch mispronunciations."""
import sys, json, numpy as np, soundfile as sf, sherpa_onnx
from scipy.signal import resample_poly
M, BUILD = sys.argv[1], sys.argv[2]
rec = sherpa_onnx.OfflineRecognizer.from_sense_voice(
    model=f"{M}/model.int8.onnx", tokens=f"{M}/tokens.txt", language="zh", use_itn=True, num_threads=4)
vo, sr = sf.read(f"{BUILD}/vo.wav", dtype="float32")
tl = json.load(open(f"{BUILD}/timeline.json"))
for ln in tl["lines"]:
    x = vo[int(ln["start"] * sr):int(ln["end"] * sr)]
    x = resample_poly(x, 16000, sr).astype(np.float32)
    s = rec.create_stream(); s.accept_waveform(16000, x); rec.decode_stream(s)
    print(f'{ln["id"]:9s} want: {ln["sub"]}\n          heard: {s.result.text}')
