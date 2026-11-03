"""Type timeline of the film (§2.2 copy deck, §3.3 text tables, §5.2 tokens, §6 motion).
Writes build/f2/type_film.json: element specs, the unique per-frame type states and the frame -> state map.
The DOM page (type.html) only applies these states; every number lives here.

    python3 f2/prod/timeline.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import BUILD, EASE, NFRAMES  # noqa: E402
import geom  # noqa: E402

COL = dict(bone='#ECE6DA', b7='#BDB5A7', b5='#8E877B', inkp='#15121B', p78='rgba(21,18,27,0.78)',
           p62='rgba(21,18,27,0.62)', p55='rgba(21,18,27,0.55)', brand='#5B2EFF', signal='#7A5CFF')

# token: (base face, weight, size, tracking em, colour), line-height px, alt face (same tuple) or None
TOK = {
    'T-DISPLAY': (('serif', 700, 148, -0.015, 'bone'), 163, None),
    'T-BIG': (('serif', 700, 112, -0.01, 'bone'), 125, None),
    'T-ST': (('serif', 600, 72, 0, 'bone'), 91, None),
    'T-ST64': (('serif', 600, 64, 0, 'bone'), 83, None),
    'T-SECOND': (('serif', 500, 56, 0, 'b7'), 75, None),
    'T-NOTE': (('serif', 500, 44, 0, 'b7'), 62, None),
    'T-FACT': (('sans', 500, 52, 0, 'bone'), 74, None),
    'T-FACT46': (('sans', 500, 46, 0, 'bone'), 65, None),
    'T-KICK': (('sans', 500, 44, 0.04, 'b5'), 44, None),
    'T-NOTE-L': (('sans', 700, 44, 0.02, 'bone'), 62, None),
    'T-KEY': (('sans', 500, 32, 0.04, 'b7'), 45, None),
    'T-CAP1': (('sans', 500, 30, 0.04, 'b5'), 42, ('mono', 500, 30, 0.02, 'b5')),
    'T-CAP2': (('mono', 400, 24, 0.02, 'b5'), 34, ('sans', 500, 24, 0.04, 'b5')),
    'T-CAP3': (('mono', 400, 22, 0.02, 'b5'), 31, None),
    'T-CAP4': (('sans', 500, 24, 0.04, 'b5'), 34, ('mono', 400, 24, 0.02, 'b5')),
    'T-HDR': (('mono', 400, 24, 0.02, 'b5'), 24, None),
    'T-SHEET': (('mono', 500, 28, 0.02, 'b5'), 34, ('sans', 500, 28, 0.02, 'b7')),
    'T-RHN': (('mono', 500, 24, 0.08, 'b5'), 24, None),
    'T-RHA': (('sans', 500, 26, 0.06, 'b5'), 24, None),
    'T-VCAP': (('sans', 500, 30, 0.12, 'b5'), 30, ('mono', 500, 30, 0.0, 'b5')),
    'T-VMONO': (('mono', 400, 24, 0.02, 'b5'), 24, None),
    'T-RL': (('sans', 500, 40, 0.04, 'p55'), 40, None),
    'T-READ': (('sans', 500, 56, 0, 'inkp'), 78, None),
    'T-ASK': (('sans', 500, 44, 0, 'p78'), 62, None),
    'T-ACC': (('sans', 700, 56, 0, 'inkp'), 56, None),
    'T-SRC': (('sans', 500, 20, 0.02, 'p62'), 31, ('mono', 500, 20, 0.02, 'p62')),
}


def run(face, weight, size, track, colour, text, tcu=False):
    return dict(t=text, f=face, w=weight, s=size, tr=track, c=COL.get(colour, colour), tcu=tcu)


def runs(tok, text, over=None):
    """Backticks toggle the token's alt face; '|' + colour-name + '|' prefixes a segment to recolour it,
    e.g. '图 `12 / 12`　|bone|你的评测集'."""
    base, _, alt = TOK[tok]
    out = []
    for i, seg in enumerate(text.split('`')):
        if not seg:
            continue
        face = alt if (i % 2 and alt) else base
        colour = face[4]
        parts = seg.split('|')
        if len(parts) == 3 and parts[0] == '' or (len(parts) >= 3 and parts[1] in COL):
            pre, colour, seg = parts[0], parts[1], '|'.join(parts[2:])
            if pre:
                out.append(run(face[0], face[1], face[2], face[3], face[4], pre))
        out.append(run(face[0], face[1], face[2], face[3], colour, seg))
    if over:
        for r in out:
            r.update(over)
    return out


EL = {}        # id -> spec
ANIM = {}      # id -> callable(f) -> (opacity, dy, extra dict)


def E(eid, tok, x, y, text, fin, fout, mode='std', layer='screen', align='left', live=None, **kw):
    spec = dict(id=eid, kind='text', layer=layer, x=x, y=y, lh=TOK[tok][1], align=align, runs=runs(tok, text), tok=tok)
    spec.update(kw)
    EL[eid] = spec
    ANIM[eid] = (mode, fin, fout, live)


def ease(name, u):
    return EASE[name](u)


def fade_in(f, fin, n):
    return ease('FADE', (f - fin + 1) / n) if f >= fin else 0.0


def leave(f, fout, n=12):
    return 1 - ease('LEAVE', (f - fout + 1) / n) if (fout is not None and f >= fout) else 1.0


def state_of(eid, f):
    mode, fin, fout, live = ANIM[eid]
    extra = {}
    if mode == 'static':
        op, dy = (1.0 if f >= fin else 0.0), 0.0
    elif mode == 'norise12':
        op, dy = fade_in(f, fin, 12), 0.0
    elif mode == 'printon':
        op, dy = (0.0 if f < fin else 0.5 if f == fin else 1.0), 0.0
    else:
        op = fade_in(f, fin, 16)
        dy = 10 * (1 - ease('SETTLE', (f - fin + 1) / 22)) if f >= fin else 10.0
    op *= leave(f, fout)
    if live and op > 0:
        extra['text'] = live(f)
    return op, dy, extra


# ---------------------------------------------------------------- live readouts (§5.5.3)
def sc(v):
    return f'{v:.2f}'


LIVE = {
    'S01-L3': lambda f: f'384 × 303 px · × {sc(geom.hook_scale(f))}',
    'S02-L3': lambda f: f'600 × 400 px · × {sc(geom.coffee_scale(f))}',
    'S02-V2': lambda f: f'skimage.data.rocket() · 640 × 427 px · × {sc(2.0 * geom.slit_push(f))}',
    'S03-N3': lambda f: f'384 × 303 px · × {sc(2.0 * geom.tray_drift(f))}',
    'S04-L3': lambda f: f'1000 × 872 px · × {sc(1.08 * geom.hubble_k(f)[0])}',
}


def build():
    # ---------------- S01 hook
    E('S01-K', 'T-KICK', 90, 330, '微软 CEO 纳德拉判断', 0, 100, 'static')
    E('S01-H1', 'T-DISPLAY', 84, 390, '大模型', 0, 100, 'static')
    E('S01-H2', 'T-DISPLAY', 84, 553, '要打价格战了', 0, 100, 'static')
    E('S01-SUB', 'T-SECOND', 90, 1262, '而且，会很残酷。', 53, 100)
    E('S01-L1', 'T-CAP1', 90, 1356, '图 `01 / 12`　古希腊钱币，庞贝出土', 66, 96)
    E('S01-L2', 'T-CAP2', 90, 1400, 'skimage.data.coins()`　分割测试', 70, 96)
    E('S01-L3', 'T-CAP3', 90, 1434, LIVE['S01-L3'](74), 74, 96, live=LIVE['S01-L3'])
    # ---------------- running head
    rh_n = [('RH-N1', '01 / 04', 118, None, 382), ('RH-N2', '02 / 04', None, 382, 646),
            ('RH-N3', '03 / 04', None, 646, 1126), ('RH-N4', '04 / 04', None, 1126, None)]
    rh_a = [('RH-A1', '价格战', 118, None, 382), ('RH-A2', '混着用', None, 382, 646),
            ('RH-A3', '改过的看法', None, 646, 862), ('RH-A4', '零信任', None, 862, 1126),
            ('RH-A5', '私有评测集', None, 1126, None)]
    for lst, tok, after in ((rh_n, 'T-RHN', None), (rh_a, 'T-RHA', 'RH-N1')):
        for eid, text, first, rin, rout in lst:
            EL[eid] = dict(id=eid, kind='text', layer='screen', x=90, y=220, lh=24, align='left',
                           runs=runs(tok, text + ('  ' if tok == 'T-RHN' else '')), tok=tok, clip=True, xAfter=after)
            ANIM[eid] = ('rh', first, rout, rin)
    EL['RH-R'] = dict(id='RH-R', kind='text', layer='screen', x=990, y=220, lh=24, align='right',
                      runs=runs('T-RHN', '20VC · 2026.10.26'), tok='T-RHN')
    ANIM['RH-R'] = ('norise12', 118, 1580, None)
    # ---------------- S02
    E('S02-K1', 'T-KICK', 90, 330, '他判断', 128, 228)
    E('S02-A1', 'T-ST', 90, 396, '在大多数企业场景里，', 134, 228)
    E('S02-A2', 'T-ST', 90, 487, '日常算力终将商品化。', 138, 228)
    E('S02-L1', 'T-CAP1', 390, 1280, '图 `02 / 12`　一杯浓缩咖啡', 150, 224)
    E('S02-L2', 'T-CAP2', 390, 1324, 'skimage.data.coffee()`　椭圆与纹理', 154, 224)
    E('S02-L3', 'T-CAP3', 390, 1358, LIVE['S02-L3'](158), 158, 224, live=LIVE['S02-L3'])
    E('S02-K2', 'T-KICK', 90, 330, '而在他看来', 266, 344)
    E('S02-B1', 'T-ST', 90, 396, '前沿模型，', 272, 344)
    E('S02-B2', 'T-ST', 90, 487, '只服务少数', 276, 344)
    E('S02-B3', 'T-ST', 90, 578, '顶级场景。', 280, 344)
    b = TOK['T-VCAP'][0]
    m = TOK['T-VCAP'][2]
    EL['S02-V1'] = dict(id='S02-V1', kind='vtext', layer='screen', x=652, y=693, lh=30, align='left', tok='T-VCAP', runs=[
        run(*b, '图 '), run(*m, '03', tcu=True), run(*b, '／'), run(*m, '12', tcu=True),
        run(*b, '　猎鹰 '), run(*b, '9', tcu=True), run(*b, ' 号与 DSCOVR　示例图')])
    ANIM['S02-V1'] = ('std', 290, 340, None)
    EL['S02-V2'] = dict(id='S02-V2', kind='vtext', layer='screen', x=614, y=693, lh=24, align='left', tok='T-VMONO',
                        runs=runs('T-VMONO', LIVE['S02-V2'](294)))
    ANIM['S02-V2'] = ('std', 294, 340, LIVE['S02-V2'])
    # ---------------- S03
    E('S03-T1', 'T-FACT', 90, 330, '大模型按 token 计价。', 386, 478)
    E('S03-T2', 'T-FACT', 90, 404, '英文里，token 也指代币。', 390, 478)
    E('S03-K', 'T-KICK', 90, 330, '据报道', 488, 616)
    E('S03-C1', 'T-ST64', 90, 396, '微软 Copilot 内部，', 494, 616)
    E('S03-C2', 'T-ST64', 90, 479, '每天都在混用', 498, 616)
    E('S03-C3', 'T-ST64', 90, 562, '便宜的闭源与开源模型。', 502, 616)
    E('S03-N1', 'T-KEY', 222, 1326, '示意　每一束光，是一次调用。', 512, 612)
    E('S03-N2', 'T-CAP4', 222, 1372, '底图　图 `01 / 12`　`skimage.data.coins()', 516, 612)
    E('S03-N3', 'T-CAP3', 222, 1406, LIVE['S03-N3'](520), 520, 612, live=LIVE['S03-N3'])
    # ---------------- S04
    E('S04-K', 'T-KICK', 90, 330, '他以前以为', 656, 836)
    E('S04-OLD', 'T-ST64', 90, 396, '规模够大，对齐自然会来。', 662, 836)
    EL['S04-STRIKE'] = dict(id='S04-STRIKE', kind='rect', layer='screen', x=84, y=438, w=780, h=3, c=COL['b5'])
    ANIM['S04-STRIKE'] = ('printon', 767, 836, None)
    E('S04-N1', 'T-BIG', 86, 488, '现在', 767, 836, 'printon')
    E('S04-N2', 'T-BIG', 86, 613, '他不这么想了。', 767, 836, 'printon')
    E('S04-L1', 'T-CAP1', 90, 1354, '图 `04 / 12`　哈勃极深场，`2012', 680, 832)
    E('S04-L2', 'T-CAP2', 90, 1398, 'skimage.data.hubble_deep_field()`　多尺度检测', 684, 832)
    E('S04-L3', 'T-CAP3', 90, 1432, LIVE['S04-L3'](688), 688, 832, live=LIVE['S04-L3'])
    # ---------------- S05
    E('S05-K', 'T-KICK', 90, 330, '他说', 908, 1084)
    E('S05-S1', 'T-ST', 90, 396, '微软不等对齐问题解决，', 914, 1084)
    E('S05-S2', 'T-ST', 90, 487, '先把模型包进零信任架构。', 918, 1084)
    for (lab, l1, l2, y, f0) in (('身份', '每个 agent，', '各有身份', 700, 980), ('记录', '每一次调用，', '都留下记录', 866, 1004),
                                 ('权限', '规则与权限，', '在模型之外', 1032, 1028)):
        k = {700: 'a', 866: 'b', 1032: 'c'}[y]
        E(f'S05-{k}L', 'T-NOTE-L', 90, y, lab, f0, 1084)
        E(f'S05-{k}1', 'T-NOTE', 200, y, l1, f0 + 4, 1084)
        E(f'S05-{k}2', 'T-NOTE', 200, y + 62, l2, f0 + 8, 1084)
    E('S05-L1', 'T-CAP1', 504, 1210, '图 `05 / 12`　人眼视网膜', 974, 1080)
    E('S05-L2', 'T-CAP2', 504, 1254, 'skimage.data.retina()`　圆形图像', 978, 1080)
    E('S05-L3', 'T-CAP3', 504, 1288, '1411 × 1411 px · × 0.31', 982, 1080)
    E('S05-L4', 'T-CAP4', 504, 1319, '血管纹路因人而异，可用于身份识别', 986, 1080)
    # ---------------- S06 (screen) + sheet captions (sheet layer)
    E('S06-F1', 'T-FACT46', 90, 290, '这 11 张，都是代码库自带的公开示例图，', 1190, 1360)
    E('S06-F2', 'T-FACT46', 90, 355, '谁都能下载，谁都能拿它考算法。', 1196, 1360)
    E('S06-HDR', 'T-HDR', 90, 446, 'from skimage import data · matplotlib sample_data · 11 / 12', 1172, 1360)
    purposes = ['分割测试', '椭圆与纹理', '示例图', '多尺度检测', '圆形图像', '分割与去噪', '示例图', '示例图', '直方图均衡', '角点检测', '反卷积']
    starts = [1154, 1157, 1160, 1163, 1166, 1169, 1172, 1175, 1178, 1181, 1184]
    for i in range(11):
        r, c = divmod(i, 3)
        x, y = geom.SHEET_XS[c], geom.SHEET_ROWS[r] + 180
        E(f'S06-C{i + 1:02d}', 'T-SHEET', x, y, f'{i + 1:02d}  `{purposes[i]}', starts[i] + 6, 1364, 'norise12', layer='sheet')
    base = TOK['T-SHEET'][0]
    EL['S06-C12a'] = dict(id='S06-C12a', kind='text', layer='sheet', x=720, y=1396, lh=34, align='left', tok='T-SHEET',
                          runs=[run(*base, '12  '), run('sans', 500, 32, 0.02, 'bone', '你的评测集')])
    ANIM['S06-C12a'] = ('norise12', 1199, 1364, None)
    EL['S06-C12b'] = dict(id='S06-C12b', kind='text', layer='sheet', x=720, y=1432, lh=34, align='left', tok='T-SHEET',
                          runs=[run('sans', 500, 28, 0.02, 'b5', '未公开')])
    ANIM['S06-C12b'] = ('norise12', 1203, 1364, None)
    # ---------------- S07
    E('S07-K', 'T-KICK', 90, 660, '纳德拉认为', 1430, 1580)
    E('S07-E1', 'T-ST', 90, 726, '每家公司，', 1436, 1580)
    E('S07-E2', 'T-ST', 90, 817, '都会有自己的', 1440, 1580)
    E('S07-E3', 'T-ST', 90, 908, '私有评测集。', 1444, 1580)
    E('S07-E4', 'T-SECOND', 90, 1040, '那会是它的核心 IP。', 1464, 1580)
    E('S07-L1', 'T-CAP1', 90, 1290, '图 `12 / 12`　|bone|你的评测集', 1470, 1576)
    E('S07-L2', 'T-CAP2', 90, 1334, 'your_eval()`　未公开', 1474, 1576)
    E('S07-L3', 'T-CAP3', 90, 1368, 'not in any library', 1478, 1576)
    # ---------------- S08 paper
    EL['S08-SQ1'] = dict(id='S08-SQ1', kind='rect', layer='screen', x=62, y=287, w=14, h=14, c=COL['brand'])
    ANIM['S08-SQ1'] = ('std', 1652, None, None)
    E('S08-RL', 'T-RL', 90, 274, '我们的解读', 1652, None)
    E('S08-R1', 'T-READ', 90, 336, '公开的考题，谁都能刷分；', 1656, None)
    E('S08-R2', 'T-READ', 90, 414, '你的考题，只有你有。', 1660, None)
    E('S08-Q', 'T-ASK', 90, 1000, '你的第一道题，考什么？', 1688, None)
    EL['S08-SQ2'] = dict(id='S08-SQ2', kind='rect', layer='screen', x=58, y=1124, w=16, h=16, c=COL['brand'])
    ANIM['S08-SQ2'] = ('std', 1700, None, None)
    E('S08-ACC', 'T-ACC', 90, 1104, 'Coo-Coo出海Ai实验室', 1700, None)
    for k, line in enumerate(SOURCES):
        E(f'S08-SRC{k + 1}', 'T-SRC', 90, 1226 + 31 * k, line, 1712 + 2 * k, None)


SOURCES = [
    '来源　20VC 播客，Harry Stebbings 对话 Satya Nadella，2026.10.26 发布。',
    '片中观点据该期节目的公开报道转述整理，非原话；我们的解读为本号观点。',
    '图像　均为 scikit-image 与 matplotlib 自带示例图；',
    '除 `09`（scikit-image 示例数据）外，均为公有领域、CC0 或无已知版权限制。',
    '`01` Brooklyn Museum　`02` Rachel Michetti　`03` SpaceX　`04` NASA',
    '`05` Wikimedia Commons　`06` Lav Varshney　`07` NASA　`08` U.S. Navy',
    '`10` Wikipedia　`11` Stefan van der Walt',
]


def rh_state(eid, f):
    _, first, rout, rin = ANIM[eid]
    op, dy = 0.0, 0.0
    if first is not None and f >= first:
        op = fade_in(f, first, 12)
    if rin is not None and f >= rin:
        u = ease('ROLL', (f - rin + 1) / 11)
        op, dy = u, 12 * (1 - u)
    if rout is not None and f >= rout:
        u = ease('ROLL', (f - rout + 1) / 11)
        op, dy = op * (1 - u), -12 * u
    if rout is None or f < rout:                       # the last chapter leaves with the whole head
        op *= leave(f, 1580)
    return op, dy, {}


def frame_state(f):
    st = {}
    sheet_vis = False
    for eid in EL:
        mode = ANIM[eid][0]
        op, dy, extra = rh_state(eid, f) if mode == 'rh' else state_of(eid, f)
        if op < 0.002:
            continue
        s = [round(op, 3), round(dy, 2)]
        if eid == 'S04-OLD' and f >= 767:
            s.append({'color': COL['bone'] if f < 767 else ('#BDB6AA' if f == 767 else COL['b5'])})
        if extra.get('text'):
            s.append({'text': extra['text']})
        st[eid] = s
        if EL[eid]['layer'] == 'sheet':
            sheet_vis = True
    out = {'e': st}
    if sheet_vis:
        s, tx, ty = geom.sheet_tf(f)
        out['sheet'] = [round(s, 5), round(tx, 3), round(ty, 3)]
    return out


def main():
    build()
    import hashlib
    states, index, frames = [], {}, []
    for f in range(NFRAMES):
        st = frame_state(f)
        key = json.dumps(st, sort_keys=True, ensure_ascii=False)
        if key not in index:
            index[key] = len(states)
            st['key'] = hashlib.sha1(key.encode()).hexdigest()[:16]
            states.append(st)
        frames.append(index[key])
    os.makedirs(BUILD, exist_ok=True)
    out = dict(w=1080, h=1920, fonts=dict(serif='Noto Serif SC', sans='Noto Sans SC', mono='IBM Plex Mono'),
               elements=list(EL.values()), states=states, frames=frames)
    json.dump(out, open(os.path.join(BUILD, 'type_film.json'), 'w'), ensure_ascii=False)
    # event log for QA (§10 timing)
    with open(os.path.join(BUILD, 'type_events.txt'), 'w') as fh:
        for eid, (mode, fin, fout, live) in ANIM.items():
            fh.write(f'{eid:12s} mode={mode:8s} in={fin} out={fout}\n')
    print(f'type timeline: {len(EL)} elements, {len(states)} unique states for {NFRAMES} frames')


if __name__ == '__main__':
    main()
