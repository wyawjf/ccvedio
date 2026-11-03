"""Review kit for design critique: frames decoded from the ENCODED film (what viewers get), grouped as
key frames (1:1), motion sequences and an Xiaohongshu feed-overlay simulation.

    python3 f2/prod/review_kit.py [build/f2/F2_picture.mp4]
"""
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import BUILD  # noqa: E402

OUT = os.path.join(BUILD, 'review')
KEY = {  # frame: what it shows
    0: 'S01 frame 0 (hook, must be complete)', 30: 'S01 rattle / rack focus', 60: 'S01 settled + sub line',
    80: 'S01 labels', 140: 'S02 espresso develops', 200: 'S02 statement A', 275: 'S02 slit opening',
    320: 'S02 frontier statement + vertical caption', 400: 'S03 token fact', 470: 'S03 token fact end',
    540: 'S03 router mid', 600: 'S03 router + labels', 700: 'S04 Hubble push', 760: 'S04 just before stop',
    770: 'S04 after hard stop', 820: 'S04 hold', 870: 'S05 crescent', 925: 'S05 full disc', 990: 'S05 contained + notes',
    1060: 'S05 complete', 1140: 'S06 pull-back', 1200: 'S06 sheet + facts', 1300: 'S06 complete sheet',
    1395: 'S07 plunge', 1460: 'S07 inside plate', 1540: 'S07 complete', 1600: 'S07 outline only',
    1612: 'S08 lamp-up', 1630: 'S08 raking light', 1680: 'S08 reading', 1771: 'S08 last frame'}
SEQS = {'hook_settle': range(36, 56, 2), 'slit': range(258, 292, 3), 'router_hop': range(482, 502, 2),
        'hard_stop': range(758, 778, 2), 'contain': range(930, 966, 4), 'pullback': range(1122, 1176, 5),
        'cells_develop': range(1150, 1206, 6), 'plunge': range(1386, 1432, 5), 'lampup': range(1602, 1656, 6)}


def decode(video, frames):
    """Decode exact frames from the encoded video."""
    out = {}
    fs = sorted(set(frames))
    sel = '+'.join(f'eq(n\\,{f})' for f in fs)
    p = subprocess.run(['ffmpeg', '-v', 'error', '-i', video, '-vf', f"select='{sel}'", '-vsync', '0', '-f', 'rawvideo',
                        '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True)
    n = 1080 * 1920 * 3
    for i, f in enumerate(fs):
        out[f] = Image.fromarray(np.frombuffer(p.stdout[i * n:(i + 1) * n], np.uint8).reshape(1920, 1080, 3))
    return out


def strip(ims, labels, w=270, h=480):
    c = Image.new('RGB', (w * len(ims) + 6 * (len(ims) - 1), h + 26), (36, 36, 36))
    d = ImageDraw.Draw(c)
    for i, (im, lab) in enumerate(zip(ims, labels)):
        c.paste(im.resize((w, h), Image.LANCZOS), (i * (w + 6), 26))
        d.text((i * (w + 6) + 4, 6), lab, fill=(220, 220, 220))
    return c


def xhs_overlay(im):
    """Rough Xiaohongshu video-feed chrome: status/search bar on top, caption + author + actions at the bottom."""
    im = im.convert('RGBA')
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.rectangle((0, 0, 1080, 150), fill=(0, 0, 0, 110))
    d.rectangle((0, 1490, 1080, 1920), fill=(0, 0, 0, 120))
    for i in range(4):                                     # right action column
        d.ellipse((960, 1040 + i * 120, 1040, 1120 + i * 120), fill=(255, 255, 255, 140))
    d.rectangle((40, 1540, 760, 1580), fill=(255, 255, 255, 150))
    d.rectangle((40, 1610, 900, 1640), fill=(255, 255, 255, 110))
    d.rectangle((40, 1660, 700, 1690), fill=(255, 255, 255, 110))
    return Image.alpha_composite(im, ov).convert('RGB')


def main():
    video = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BUILD, 'F2_picture.mp4')
    os.makedirs(os.path.join(OUT, 'key'), exist_ok=True)
    allf = set(KEY) | {f for r in SEQS.values() for f in r}
    fr = decode(video, allf)
    with open(os.path.join(OUT, 'INDEX.md'), 'w') as fh:
        fh.write('# Review kit (frames decoded from the encoded film; 30 fps, frame f = f/30 s)\n\n## key/ (1:1 PNG)\n')
        for f, what in KEY.items():
            fr[f].save(os.path.join(OUT, 'key', f'f{f:04d}.png'))
            fh.write(f'- key/f{f:04d}.png  {f / 30:6.2f}s  {what}\n')
        fh.write('\n## sequences (consecutive frames, scaled 1/4)\n')
        for name, r in SEQS.items():
            strip([fr[f] for f in r], [f'f{f}' for f in r]).save(os.path.join(OUT, f'seq_{name}.jpg'), quality=90)
            fh.write(f'- seq_{name}.jpg  frames {list(r)}\n')
        ks = sorted(KEY)
        for i in range(0, len(ks), 8):
            part = ks[i:i + 8]
            strip([fr[f] for f in part], [f'f{f}' for f in part], 360, 640).save(os.path.join(OUT, f'overview_{i // 8 + 1}.jpg'), quality=90)
        fh.write('\n## overview_N.jpg: key frames side by side\n')
        os.makedirs(os.path.join(OUT, 'xhs'), exist_ok=True)
        for f in (0, 200, 320, 600, 820, 1060, 1300, 1540, 1771):
            xhs_overlay(fr[f]).save(os.path.join(OUT, 'xhs', f'f{f:04d}.jpg'), quality=90)
        fh.write('\n## xhs/: key frames under a rough Xiaohongshu feed overlay (top bar, bottom caption, right actions)\n')
    print('review kit ->', OUT)


if __name__ == '__main__':
    main()
