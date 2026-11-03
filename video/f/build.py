"""Assemble the F (Nadella) vertical video from f/edl.json.

usage:
  python3 f/build.py            # real cut: needs build/f/source.mp4, every clip's in/out, no draft subs
  python3 f/build.py --preview  # layout/pacing preview: clips replaced by a labelled test pattern

Run `node f/render.mjs cards subs` first (cards, clip frames and subtitle strips).
Output: build/f/F_final.mp4 or build/f/F_preview.mp4 (1080x1920, 30fps, AAC 48k).
"""
import json, os, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
B = os.path.join(ROOT, 'build/f')
FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
HOLE_X, HOLE_Y, HOLE_W, HOLE_H = 48, 600, 984, 554   # must match slides.html frame mode
SUB_Y = 1236
V = ['-r', '30', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p']
A = ['-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2']

preview = '--preview' in sys.argv
edl = json.load(open(os.path.join(ROOT, 'f/edl.json')))
src = os.path.join(ROOT, edl['source'])

if not preview:
    problems = []
    if not os.path.exists(src):
        problems.append(f'missing source video: {src}')
    for it in edl['items']:
        if it['type'] != 'clip':
            continue
        if it['in'] is None or it['out'] is None:
            problems.append(f"{it['id']}: in/out not set")
        if any(s.get('draft') for s in it['subs']):
            problems.append(f"{it['id']}: subtitles are still drafts (translate the actual words, drop draft)")
    if problems:
        sys.exit('refusing to build the real cut:\n  ' + '\n  '.join(problems) + '\n(use --preview for a layout preview)')


def run(cmd):
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', *cmd], check=True)


os.makedirs(os.path.join(B, 'seg'), exist_ok=True)
segs = []
for n, it in enumerate(edl['items']):
    out = os.path.join(B, f'seg/{n:02d}.mp4')
    if it['type'] == 'card':
        d = it['dur']
        run(['-loop', '1', '-t', f'{d}', '-i', os.path.join(B, it['img']),
             '-f', 'lavfi', '-t', f'{d}', '-i', 'anullsrc=r=48000:cl=stereo',
             '-vf', 'fps=30,format=yuv420p,fade=t=in:st=0:d=0.15',
             *V, *A, '-shortest', out])
    else:
        if preview:
            d = it['dur_est']
            label = f"PLACEHOLDER {it['id']}  -  find in transcript = {it['find']}"
            clip_in = ['-f', 'lavfi', '-t', f'{d}', '-i', 'testsrc2=s=1920x1080:r=30',
                       '-f', 'lavfi', '-t', f'{d}', '-i', 'sine=f=220:r=48000']
            pre = (f"drawbox=x=0:y=440:w=1920:h=200:color=black@0.75:t=fill,"
                   f"drawtext=fontfile={FONT}:text='{label}':fontsize=50:fontcolor=white:x=(w-tw)/2:y=510,")
            amap = '2:a'
        else:
            d = it['out'] - it['in']
            clip_in = ['-ss', f"{it['in']}", '-t', f'{d}', '-i', src]
            pre = ''
            amap = '1:a'
        # inputs: 0 frame (stage + taped panel), 1.. clip, then frame top layer (tape + speaker tag), then subtitle boxes
        n_clip = 2 if preview else 1
        top_idx = 1 + n_clip
        top_png = os.path.join(B, it['frame'].replace('frame', 'frametop'))
        subs = [(j, s) for j, s in enumerate(it['subs']) if s['t0'] < d]
        sub_in = []
        for j, _ in subs:
            sub_in += ['-i', os.path.join(B, f"subs/{it['id']}_{j}.png")]
        fc = [f"[1:v]{pre}scale={HOLE_W}:{HOLE_H}:force_original_aspect_ratio=decrease,"
              f"pad={HOLE_W}:{HOLE_H}:(ow-iw)/2:(oh-ih)/2,setsar=1[clip]",
              f"[0:v][clip]overlay={HOLE_X}:{HOLE_Y}[vc]",
              f"[vc][{top_idx}:v]overlay=0:0[v0]"]
        for k, (j, s) in enumerate(subs):
            fc.append(f"[v{k}][{top_idx + 1 + k}:v]overlay=0:{SUB_Y}:enable='between(t,{s['t0']},{min(s['t1'], d)})'[v{k + 1}]")
        fc.append(f"[v{len(subs)}]fps=30,format=yuv420p[vout]")
        fc.append(f"[{amap}]afade=t=in:st=0:d=0.08,afade=t=out:st={max(0, d - 0.12)}:d=0.12,"
                  f"aresample=48000,aformat=channel_layouts=stereo[aout]")
        run(['-loop', '1', '-t', f'{d}', '-i', os.path.join(B, it['frame']), *clip_in,
             '-loop', '1', '-t', f'{d}', '-i', top_png, *sub_in,
             '-filter_complex', ';'.join(fc), '-map', '[vout]', '-map', '[aout]', '-t', f'{d}', *V, *A, out])
    segs.append(out)
    print(f'{n:02d} {it["type"]:5s} ok')

lst = os.path.join(B, 'seg/list.txt')
open(lst, 'w').write(''.join(f"file '{s}'\n" for s in segs))
final = os.path.join(B, 'F_preview.mp4' if preview else 'F_final.mp4')
run(['-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', '-movflags', '+faststart', final])
print('wrote', final)
