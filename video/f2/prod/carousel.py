"""Carousel C1-C7, 1080x1440 (§4). Python draws each frame's picture layer, the shared type page sets the
type, film.py finishes the stills. Output: build/f2/carousel/01.png ... 07.png (01 = cover).

    python3 f2/prod/carousel.py
"""
import json
import os
import subprocess
import sys

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import timeline as TL  # noqa: E402
from common import BUILD, INK, ROOT, load_npy, save_png, smoothstep, warp  # noqa: E402
from picture import Picture, hairline  # noqa: E402
from prep import paper_and_mark, plate_shade  # noqa: E402

CW, CH = 1080, 1440
OUT = os.path.join(BUILD, 'carousel')

TL.TOK.update({
    'C-DISPLAY': (('serif', 700, 150, -0.015, 'bone'), 162, None),
    'C-ST76': (('serif', 600, 76, 0, 'bone'), 96, None),
    'C-NEW76': (('serif', 700, 76, -0.01, 'bone'), 96, None),
    'C-ST60': (('serif', 600, 60, 0, 'bone'), 77, None),
    'C-ST52': (('serif', 600, 52, 0, 'bone'), 68, None),
    'C-OLD52': (('serif', 600, 52, 0, 'b5'), 68, None),
    'C-NOTE40': (('serif', 500, 40, 0, 'b7'), 56, None),
    'C-NOTE-L40': (('sans', 700, 40, 0.02, 'bone'), 56, None),
    'C-NOTEK28': (('sans', 500, 28, 0.04, 'b5'), 34, None),
    'C-KICK40': (('sans', 500, 40, 0.04, 'b5'), 40, None),
    'C-FACT44': (('sans', 500, 44, 0, 'bone'), 62, None),
    'C-TOK40': (('sans', 500, 40, 0, 'b7'), 56, None),
    'C-CURIO': (('sans', 500, 64, 0.02, 'bone'), 72, None),     # the hook must read in a 2-column feed
    'C-ENTRY': (('sans', 500, 40, 0, 'inkp'), 56, None),
    'C-ASK40': (('sans', 500, 40, 0, 'p78'), 56, None),
    'C-ACC40': (('sans', 700, 40, 0, 'inkp'), 46, None),
    'C-FOOT': (('sans', 500, 26, 0.02, 'b7'), 30, None),
    'C-PAGE': (('mono', 500, 24, 0.08, 'b5'), 24, None),
    'C-PAGEP': (('mono', 500, 24, 0.08, 'p70'), 24, None),
    'C-FOOTP': (('sans', 500, 26, 0.02, 'inkp'), 30, None),
    'C-DATE': (('mono', 500, 24, 0.08, 'b5'), 24, None),
    'C-EVAL': (('mono', 500, 26, 0.02, 'p70'), 26, None),
    'C-HDR22': (('mono', 400, 22, 0.02, 'b5'), 22, None),
    'C-VCAP24': (('sans', 500, 24, 0.12, 'b5'), 24, ('mono', 500, 24, 0.0, 'b5')),
})

FRAMES = []          # per frame: list of element ids


def T(fr, eid, tok, x, y, text, align='left', **kw):
    eid = f'C{fr}-{eid}'
    TL.EL[eid] = dict(id=eid, kind='text', layer='screen', x=x, y=y, lh=TL.TOK[tok][1], align=align,
                      runs=TL.runs(tok, text), tok=tok, **kw)
    FRAMES[fr - 1].append(eid)


def R(fr, eid, x, y, w, h, colour):
    eid = f'C{fr}-{eid}'
    TL.EL[eid] = dict(id=eid, kind='rect', layer='screen', x=x, y=y, w=w, h=h, c=TL.COL[colour])
    FRAMES[fr - 1].append(eid)


def RH(fr, num, name):
    T(fr, 'rhn', 'T-RHN', 90, 96, num + '  ')
    eid = f'C{fr}-rha'
    TL.EL[eid] = dict(id=eid, kind='text', layer='screen', x=90, y=96, lh=24, align='left',
                      runs=TL.runs('T-RHA', name), tok='T-RHA', xAfter=f'C{fr}-rhn')
    FRAMES[fr - 1].append(eid)
    T(fr, 'rhr', 'T-RHN', 990, 96, '20VC · 2026.10.26', align='right')


def footer(fr, page=True):
    R(fr, 'fsq', 90, 1373, 12, 12, 'signal')
    T(fr, 'facc', 'C-FOOT', 114, 1364, 'Coo-Coo出海Ai实验室')
    if page:
        T(fr, 'fpage', 'C-PAGE', 990, 1366, f'{fr:02d} / 07', align='right')


def build_type():
    TL.EL.clear()
    FRAMES.clear()
    FRAMES.extend([[] for _ in range(7)])
    # C1 cover
    T(1, 'k', 'T-KICK', 90, 120, '微软 CEO 纳德拉判断')
    T(1, 'date', 'C-DATE', 990, 132, '20VC · 2026.10.26', align='right')
    T(1, 'h1', 'C-DISPLAY', 84, 184, '大模型')
    T(1, 'h2', 'C-DISPLAY', 84, 346, '要打价格战了')
    # the photo editor's pick on a contact sheet: one china-marker loop with an overshoot (review CD-03)
    loop = ('M584.9 926.9 C587.1 922.3 591.5 906.6 598.2 899.1 C604.9 891.5 615.3 885.2 625.0 881.8 '
            'C634.7 878.3 646.2 877.3 656.4 878.4 C666.5 879.5 677.3 882.9 685.8 888.2 C694.3 893.6 702.7 901.7 '
            '707.2 910.6 C711.7 919.5 714.2 931.5 712.8 941.6 C711.4 951.7 705.8 963.2 698.7 971.2 C691.6 979.2 '
            '680.6 985.9 670.3 989.5 C660.1 993.2 647.9 994.2 637.1 993.0 C626.4 991.9 615.0 988.2 606.0 982.5 '
            'C597.1 976.8 588.1 968.2 583.4 958.8 C578.6 949.3 578.5 931.4 577.5 925.9')
    import math as _m

    def sm(e0, e1, x):
        t = min(1.0, max(0.0, (x - e0) / (e1 - e0)))
        return t * t * (3 - 2 * t)
    strokes = []
    for j in range(16):                                    # the marker lands thin, presses, lifts (tapered)
        p0 = j * 100 / 16
        pm = (j + 0.5) / 16
        w = 2.4 + 2.6 * sm(0, 0.25, pm) - 1.8 * sm(0.75, 1.0, pm)
        strokes.append(dict(w=round(w, 2), d=loop, dash=[round(100 / 16 + 0.8, 2), 200, round(-p0, 2)]))
    strokes.append(dict(w=3.0, op=0.7, d='M583.4 958.8 C582.6 952.3 575.6 932.3 578.6 920.2 C581.5 908.2 597.4 892.0 601.2 886.4'))
    TL.EL['C1-ring'] = dict(id='C1-ring', kind='path', layer='screen', c=TL.COL['signal'], op=0.85, tex=True, strokes=strokes)
    FRAMES[0].append('C1-ring')
    T(1, 'l1', 'T-CAP1', 222, 1174, '图` 01 / 12`　古希腊钱币，庞贝出土')
    T(1, 'l2', 'T-CAP2', 222, 1218, 'skimage.data.coins()  No.16 / 24')
    T(1, 'cur', 'C-CURIO', 90, 1268, '11 张公开图，第 12 张是你的。')
    footer(1, page=False)
    # C2
    RH(2, '01 / 04', '价格战')
    T(2, 'k1', 'C-KICK40', 90, 160, '他判断')
    T(2, 'a1', 'C-ST60', 90, 216, '在大多数企业场景里，')
    T(2, 'a2', 'C-ST60', 81, 293, '日常算力终将商品化。')
    T(2, 'l1', 'T-CAP1', 390, 840, '图` 02 / 12`　一杯浓缩咖啡')
    T(2, 'l2', 'T-CAP2', 390, 884, 'skimage.data.coffee()`　椭圆与纹理')
    T(2, 'l3', 'T-CAP3', 390, 918, '600 × 400 px · × 1.00')
    T(2, 'k2', 'C-KICK40', 90, 1020, '而在他看来')
    T(2, 'b1', 'C-ST52', 90, 1076, '前沿模型，只服务')
    T(2, 'b2', 'C-ST52', 90, 1144, '少数顶级场景。')
    b, m = TL.TOK['C-VCAP24'][0], TL.TOK['C-VCAP24'][2]
    TL.EL['C2-v'] = dict(id='C2-v', kind='vtext', layer='screen', x=850, y=1020, lh=24, align='left', tok='C-VCAP24', runs=[
        TL.run(*b, '图'), TL.run(*m, '03', tcu=True), TL.run(*b, '／'), TL.run(*m, '12', tcu=True),
        TL.run(*b, '　猎鹰'), TL.run(*b, '9', tcu=True), TL.run(*b, '号')])
    FRAMES[1].append('C2-v')
    footer(2)
    # C3
    RH(3, '02 / 04', '混着用')
    T(3, 'k', 'C-KICK40', 90, 160, '据报道')
    T(3, 'c1', 'C-ST60', 90, 216, '微软 Copilot 内部，')
    T(3, 'c2', 'C-ST60', 90, 293, '每天都在混用')
    T(3, 'c3', 'C-ST60', 90, 370, '便宜的闭源与开源模型。')
    T(3, 'n1', 'T-KEY', 299, 1065, '示意　每一束光，是一次调用')
    T(3, 'n2', 'T-CAP4', 299, 1111, '底图　`01 / 12`　`skimage.data.coins()')
    T(3, 'n3', 'T-CAP3', 299, 1145, '384 × 303 px · × 1.80')
    T(3, 'tok', 'C-TOK40', 90, 1236, '大模型按 token 计价；英文里，token 也指代币。')
    footer(3)
    # C4
    RH(4, '03 / 04', '改过的看法')
    T(4, 'k1', 'C-KICK40', 90, 500, '他以前以为')
    T(4, 'hl', 'T-CAP4', 990, 506, '图` 04 / 12`　哈勃极深场', align='right')
    T(4, 'old', 'C-OLD52', 90, 556, '规模够大，对齐自然会来。')
    R(4, 'strike', 85, 590.75, 600, 2.5, 'b5')
    T(4, 'new', 'C-NEW76', 88, 630, '现在，他不这么想了。')
    T(4, 'k2', 'C-KICK40', 90, 800, '他说')
    T(4, 's1', 'C-ST52', 90, 856, '微软不等对齐问题解决，')
    T(4, 's2', 'C-ST52', 90, 924, '先把模型包进零信任架构。')
    for i, (lab, body) in enumerate((('身份', '每个 agent，各有身份'), ('记录', '每一次调用，都留下记录'), ('权限', '规则与权限，在模型之外'))):
        y = 1036 + 98 * i                                   # small kicker over each rule (review CD-09)
        T(4, f'nl{i}', 'C-NOTEK28', 90, y, lab)
        T(4, f'nb{i}', 'C-NOTE40', 90, y + 30, body)
    T(4, 'fl', 'T-CAP4', 750, 1296, '图` 05 / 12`　视网膜')
    footer(4)
    # C5
    RH(5, '04 / 04', '私有评测集')
    T(5, 'f1', 'C-FACT44', 90, 150, '这 11 张，都是代码库自带的公开示例图，')
    T(5, 'f2', 'C-FACT44', 90, 212, '谁都能下载，谁都能拿它们考算法。')
    T(5, 'hdr', 'C-HDR22', 90, 300, 'from skimage import data · matplotlib sample_data · 11 / 12')
    purposes = TL.PURPOSES
    for i in range(11):
        r, c = divmod(i, 3)
        x, y = (90, 390, 690)[c], (352, 582, 812, 1042)[r]
        T(5, f'c{i + 1:02d}', 'T-SHEET', x, y + 160, f'{i + 1:02d}  `{purposes[i]}')
    base = TL.TOK['T-SHEET'][0]
    TL.EL['C5-c12a'] = dict(id='C5-c12a', kind='text', layer='screen', x=690, y=1042 + 160, lh=34, align='left', tok='T-SHEET',
                            runs=[TL.run(*base, '12  '), TL.run('sans', 500, 30, 0.02, 'bone', '你的评测集')])
    TL.EL['C5-c12b'] = dict(id='C5-c12b', kind='text', layer='screen', x=760, y=1042 + 196, lh=34, align='left', tok='T-SHEET',
                            runs=[TL.run('sans', 500, 28, 0.02, 'b5', '未公开')])
    FRAMES[4] += ['C5-c12a', 'C5-c12b']
    footer(5)
    # C6
    RH(6, '04 / 04', '私有评测集')
    T(6, 'k', 'C-KICK40', 90, 170, '纳德拉认为')
    T(6, 'e1', 'C-ST76', 90, 226, '每家公司，')
    T(6, 'e2', 'C-ST76', 90, 322, '都会有自己的')
    T(6, 'e3', 'C-ST76', 90, 418, '私有评测集。')
    T(6, 'e4', 'T-SECOND', 90, 546, '那会是它的核心 IP。')
    T(6, 'l1', 'T-CAP1', 90, 1042, '图` 12 / 12`　|bone|你的评测集')     # a wall label beside the object
    T(6, 'l2', 'T-CAP2', 90, 1086, 'your_eval()`　未公开')
    T(6, 'l3', 'T-CAP3', 90, 1120, 'not in any library')
    footer(6)
    # C7 paper
    R(7, 'sq1', 62, 133, 14, 14, 'brand')
    T(7, 'rl', 'T-RL', 90, 120, '我们的解读')
    T(7, 'r1', 'T-READ', 90, 184, '公开的考题，谁都能刷分；')
    T(7, 'r2', 'T-READ', 90, 262, '你的考题，只有你有。')
    T(7, 'eval', 'C-EVAL', 90, 784, 'your_eval()')
    T(7, 'en1', 'C-ENTRY', 90, 828, '用你自己的真实场景出题；')
    T(7, 'en2', 'C-ENTRY', 90, 884, '换模型、混用模型之前，先拿它考一遍。')
    T(7, 'q', 'C-ASK40', 90, 962, '你的第一道题，考什么？')
    for k, (x, y) in enumerate(TL.source_layout(1084)):
        T(7, f'src{k + 1}', 'T-SRC', x, y, TL.SOURCES[k])
    R(7, 'fsq', 90, 1373, 12, 12, 'brand')
    T(7, 'facc', 'C-FOOTP', 114, 1364, 'Coo-Coo出海Ai实验室')
    T(7, 'fpage', 'C-PAGEP', 990, 1366, '07 / 07', align='right')
    import hashlib
    states = []
    for fr in range(7):
        st = {'e': {eid: [1.0, 0.0] for eid in FRAMES[fr]}}
        st['key'] = 'car' + hashlib.sha1(json.dumps([st['e'], [TL.EL[e] for e in FRAMES[fr]]], sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:13]
        states.append(st)
    data = dict(w=CW, h=CH, elements=list(TL.EL.values()), states=states, frames=list(range(7)))
    path = os.path.join(BUILD, 'type_car.json')
    json.dump(data, open(path, 'w'), ensure_ascii=False)
    return data


# ---------------------------------------------------------------- picture layers
def canvas():
    img = np.empty((CH, CW, 3), np.float32)
    img[:] = INK
    return img


def place(img, src, s, ox, oy):
    sh, sw = src.shape[:2]
    x0, y0 = max(0, int(np.floor(ox)) - 2), max(0, int(np.floor(oy)) - 2)
    x1, y1 = min(CW, int(np.ceil(ox + sw * s)) + 2), min(CH, int(np.ceil(oy + sh * s)) + 2)
    rgb, cov = warp(src, s, ox, oy, (x0, y0, x1, y1))
    a = cov[..., None]
    img[y0:y1, x0:x1] = img[y0:y1, x0:x1] * (1 - a) + np.clip(rgb, 0, 1) * a


def hair(img, rect, alpha, radius=0.0):
    pad = np.empty((1920, 1080, 3), np.float32)              # hairline() draws on a film-sized canvas
    pad[:CH] = img
    hairline(pad, rect, alpha, radius=radius)
    img[:] = pad[:CH]


def pictures():
    P = Picture()
    out = []
    # C1: house lights up, x2.00
    img = canvas()
    place(img, P.cells['coins_full'], 2.0, 222, 548)
    out.append(img)
    # C2: espresso x1.00 + rocket slit crop x0.7324 (sharp)
    img = canvas()
    place(img, P.cells['coffee_rgb'], 1.0, 390, 420)
    rk = P.cells['rocket_rgb'][60:427, 250:392]
    small = cv2.resize(rk, (104, 269), interpolation=cv2.INTER_AREA)
    img[1020:1020 + 269, 886:886 + 104] = small
    out.append(img)
    # C3: long exposure of the last five calls
    img = canvas()
    C = {c['id']: c for c in P.coins}
    lights = [(C[k]['cx'], C[k]['cy'], C[k]['r'], v) for k, v in ((17, .22), (11, .36), (21, .55), (18, .78), (16, 1.0))]
    box, rgb, cov = P.coins_dissolve(1.8, 299, 500, lights, 0.16)
    x0, y0, x1, y1 = box
    y1c = min(y1, CH)
    a = cov[:y1c - y0, ..., None]
    img[y0:y1c, x0:x1] = img[y0:y1c, x0:x1] * (1 - a) + rgb[:y1c - y0] * a
    out.append(img)
    # C4: Hubble band + retina in its frame
    img = canvas()
    hub = load_npy('hubble_full.npy')
    rgb, _ = warp(hub, 1.08, 0, -120 - 140, (0, 0, CW, 470 - 140))
    ys = np.arange(140, 470, dtype=np.float32) + 0.5
    mk = np.clip((ys - 140) / 56, 0, 1) * np.clip((470 - ys) / 56, 0, 1)
    img[140:470] = INK + (np.clip(rgb, 0, 1) - INK) * mk[:, None, None]
    place(img, P.cells['retina_full'], 208 / 1411, 766, 1056)
    hair(img, (750, 1040, 240, 240), 0.30)
    out.append(img)
    # C5: contact sheet at row height 150
    img = canvas()
    order = ['coins_full', 'coffee_rgb', 'rocket_rgb', 'hubble_full', 'retina_full', 'camera', 'astronaut',
             'grace_hopper', 'moon', 'text', 'clock']
    for i, name in enumerate(order):
        r, c = divmod(i, 3)
        x, y = (90, 390, 690)[c], (352, 582, 812, 1042)[r]
        src = P.cells[name]
        place(img, src, 150 / src.shape[0], x, y)
    hair(img, (690, 1042, 225, 150), 0.30)
    out.append(img)
    # C6: the empty plate
    img = canvas()
    hair(img, (690, 1042, 225, 150), 0.30)              # exactly C5's cell 12: the swipe removes the other 11
    out.append(img)
    # C7: paper + plate mark at rest light (seed 9)
    alb, n = paper_and_mark(CW, CH, (90, 392, 630, 752), seed=9, depth=0.46)
    out.append(np.minimum(alb * plate_shade(n, 135, 24)[..., None], 0.985).astype(np.float32))
    return out


def finish(img, paper=False):
    from film import Film
    f = Film(CW, CH, seed=11)
    look = {'default': dict(grain=0.020 if paper else 0.030, grain_size=1.35, grain_chroma=0.0, halation=0.0, bloom=0.0,
                            ca=0.0, vignette=0.05 if paper else 0.12, vig_round=1.0, weave=0.0, flicker=0.0,
                            shoulder=0.97, print_bloom=0.20, print_bloom_sigma=0.6), 'keys': []}
    f.look = look
    return f(np.clip(img, 0, 1), 0.0)


def main():
    data = build_type()
    subprocess.run(['node', os.path.join(HERE, 'type_render.mjs'), '--data', 'build/f2/type_car.json', '--out',
                    'build/f2/type_car', '--force'], check=True, cwd=ROOT)
    from PIL import Image
    pics = pictures()
    os.makedirs(OUT, exist_ok=True)
    for i, pic in enumerate(pics):
        key = data['states'][i]['key']
        tp = np.asarray(Image.open(os.path.join(BUILD, 'type_car', key + '.png')).convert('RGBA')).astype(np.float32) / 255
        al = tp[..., 3:4]
        img = tp[..., :3] * al + pic * (1 - al)
        fin = finish(img, paper=(i == 6))
        Image.fromarray(fin).save(os.path.join(OUT, f'{i + 1:02d}.png'), optimize=True)
        print('carousel', f'{i + 1:02d}.png')


if __name__ == '__main__':
    main()
