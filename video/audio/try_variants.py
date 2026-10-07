"""Synthesize text variants and transcribe them back, to pick pronunciations that survive."""
import sys, numpy as np, sherpa_onnx
from scipy.signal import resample_poly
TM, AM = sys.argv[1], sys.argv[2]; SID = int(sys.argv[3]); texts = sys.argv[4:]
cfg = sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
    kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(model=f"{TM}/model.onnx", voices=f"{TM}/voices.bin",
        tokens=f"{TM}/tokens.txt", data_dir=f"{TM}/espeak-ng-data", dict_dir=f"{TM}/dict",
        lexicon=f"{TM}/lexicon-us-en.txt,{TM}/lexicon-zh.txt"), num_threads=4),
    rule_fsts=f"{TM}/date-zh.fst,{TM}/phone-zh.fst,{TM}/number-zh.fst", max_num_sentences=1)
tts = sherpa_onnx.OfflineTts(cfg)
rec = sherpa_onnx.OfflineRecognizer.from_sense_voice(model=f"{AM}/model.int8.onnx", tokens=f"{AM}/tokens.txt",
    language="zh", use_itn=True, num_threads=4)
for t in texts:
    a = tts.generate(t, sid=SID, speed=1.0)
    x = resample_poly(np.array(a.samples, np.float32), 16000, a.sample_rate).astype(np.float32)
    s = rec.create_stream(); s.accept_waveform(16000, x); rec.decode_stream(s)
    print(f"{t}  ->  {s.result.text}   ({len(a.samples)/a.sample_rate:.2f}s)")
