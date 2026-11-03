"""Composite picture + type, run the finishing pass (film.py + look.json) and encode (Appendix B steps 2-5).

    python3 f2/prod/compose.py --jobs 4                 # whole film -> build/f2/F2_picture.mp4 (no audio)
    python3 f2/prod/compose.py --frames 0,500 --still   # finished stills -> build/f2/stills/
    python3 f2/prod/compose.py --mux                    # + build/f2/score.wav -> build/f2/F2_final.mp4
"""
import json
import os
import subprocess
import sys
import time
from multiprocessing import Pool

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
from common import BUILD, FPS, H, NFRAMES, W, save_png  # noqa: E402

LOOK = os.path.join(HERE, 'look.json')
SEG = os.path.join(BUILD, 'seg')
X264 = ['-c:v', 'libx264', '-preset', 'slow', '-tune', 'grain', '-crf', '16', '-pix_fmt', 'yuv420p',
        '-profile:v', 'high', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
        '-color_range', 'tv']


class Composer:
    def __init__(self):
        from film import Film, load_look
        from picture import Picture
        self.pic = Picture()
        self.film = Film(W, H, seed=7)
        self.film.look = load_look(LOOK)
        self.data = json.load(open(os.path.join(BUILD, 'type_film.json')))
        self._tkey, self._timg = None, None

    def type_layer(self, f):
        from PIL import Image
        key = self.data['states'][self.data['frames'][f]]['key']
        if key != self._tkey:
            p = os.path.join(BUILD, 'type', key + '.png')
            if not os.path.exists(p):
                raise FileNotFoundError(f'type state for frame {f} not rendered: {p}')
            a = np.asarray(Image.open(p).convert('RGBA')).astype(np.float32) / 255.0
            self._tkey, self._timg = key, a
        return self._timg

    def frame(self, f, post=True):
        img = self.pic.frame(f)
        tp = self.type_layer(f)
        al = tp[..., 3:4]
        img = tp[..., :3] * al + img * (1 - al)
        if not post:
            return img
        self.film.rng = np.random.default_rng(1000 + f)     # grain/weave reseeded per frame: segments agree
        return self.film(np.clip(img, 0, 1), f / FPS)


def encode_chunk(args):
    a, b, out = args
    C = Composer()
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                            '-r', str(FPS), '-i', '-', *X264, '-threads', '2', '-r', str(FPS), out], stdin=subprocess.PIPE)
    t0 = time.time()
    for f in range(a, b):
        enc.stdin.write(C.frame(f).tobytes())
    enc.stdin.close()
    enc.wait()
    return a, b, time.time() - t0


def run_all(jobs, a=0, b=NFRAMES, chunk=48):
    os.makedirs(SEG, exist_ok=True)
    chunks = []
    for s in range(a, b, chunk):
        e = min(b, s + chunk)
        chunks.append((s, e, os.path.join(SEG, f'seg_{s:04d}.mp4')))
    # expensive chunks first (motion blur, lamp-up), so the pool drains evenly
    heavy = lambda c: -sum(1 for f in range(c[0], c[1]) if 1124 <= f <= 1172 or 1388 <= f <= 1428 or 1604 <= f <= 1652 or 484 <= f <= 621)
    t0 = time.time()
    with Pool(jobs) as pool:
        for s, e, dt in pool.imap_unordered(encode_chunk, sorted(chunks, key=heavy)):
            print(f'  chunk {s}-{e} done in {dt:.0f} s (elapsed {time.time() - t0:.0f} s)', flush=True)
    lst = os.path.join(SEG, 'list.txt')
    with open(lst, 'w') as fh:
        for s, e, p in chunks:
            fh.write(f"file '{p}'\n")
    out = os.path.join(BUILD, 'F2_picture.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', out], check=True)
    print('picture ->', out, f'({time.time() - t0:.0f} s)')


def mux():
    """Master (CRF 16 picture + AAC, local only) and the upload copy F2_final.mp4 (2-pass ~10 Mbps, < 100 MB)."""
    pic = os.path.join(BUILD, 'F2_picture.mp4')
    wav = os.path.join(BUILD, 'score.wav')
    master = os.path.join(BUILD, 'F2_master.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', pic, '-i', wav, '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy',
                    '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-movflags', '+faststart', '-shortest', master], check=True)
    print('master ->', master)
    out = os.path.join(BUILD, 'F2_final.mp4')
    v = ['-c:v', 'libx264', '-preset', 'slow', '-tune', 'grain', '-b:v', '10M', '-maxrate', '14M', '-bufsize', '20M',
         '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-color_primaries', 'bt709', '-color_trc', 'bt709',
         '-colorspace', 'bt709', '-color_range', 'tv']
    log = os.path.join(BUILD, 'x264_2pass')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', pic, *v, '-pass', '1', '-passlogfile', log, '-an', '-f', 'null', '-'], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', pic, '-i', wav, '-map', '0:v:0', '-map', '1:a:0', *v, '-pass', '2',
                    '-passlogfile', log, '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-movflags', '+faststart',
                    '-shortest', out], check=True)
    print('upload copy ->', out)


def main():
    a = sys.argv[1:]
    if '--mux' in a:
        mux()
        return
    if '--frames' in a:
        frames = [int(x) for x in a[a.index('--frames') + 1].split(',')]
        C = Composer()
        out = os.path.join(BUILD, 'stills')
        for f in frames:
            t0 = time.time()
            img = C.frame(f)
            save_png(os.path.join(out, f'f{f:04d}.png'), img.astype(np.float32) / 255.0 if img.dtype == np.uint8 else img)
            print(f'still {f}: {time.time() - t0:.2f} s')
        return
    jobs = int(a[a.index('--jobs') + 1]) if '--jobs' in a else 4
    lo = int(a[a.index('--from') + 1]) if '--from' in a else 0
    hi = int(a[a.index('--to') + 1]) if '--to' in a else NFRAMES
    run_all(jobs, lo, hi)


if __name__ == '__main__':
    main()
