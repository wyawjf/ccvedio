# 第十二张 · THE TWELFTH PLATE

**Concept pitch for F2: 微软CEO：大模型要打价格战了**
Vertical film 1080×1920 · 30 fps · **59.0 s** (1770 frames) · silent text + synthesized score · Xiaohongshu carousel 1080×1440 × **7 frames**

> **Logline.** Nadella's price-war thesis, told entirely through the **eleven public sample photos that ship inside open-source code** (the "public test set" of computer vision), ending on a **twelfth plate that is empty**: your private eval, the one image nobody else has.
>
> **一句话：** 用 11 张开源代码库自带的公开示例图，讲纳德拉的价格战判断；第 12 张是空的，那是你的私有评测集。

Look-dev frames rendered with the real fonts, grid and grade are in `f2/concepts/doc_lookdev/`. Start with `_film_strip.jpg` and `_carousel_strip.jpg`. The prototype grade, grain and layout code is in `doc_lookdev/src/` (reference only, not production). Every coordinate in this document was checked in those renders.

---

## 1. The idea

### 1.1 The big idea

Every photo we were given is a **standard test image**. I checked this rather than assuming it. The ten non-map photos in `assets/lib/` are **pixel-identical** (max diff 0) to `skimage.data.coins()`, `.camera()`, `.moon()`, `.text()`, `.astronaut()`, `.coffee()`, `.rocket()`, `.clock()`, `.hubble_deep_field()` and `.retina()`. `grace_hopper.jpg` is matplotlib's `sample_data` image (per `assets/SOURCES.md`). scikit-image describes this set as *"a curated set of general purpose and scientific images used in tests, examples, and documentation."* Each docstring names the test the image exists for: coins → segmentation, clock → deconvolution, moon → histogram equalization, text → corner detection, Hubble → multi-scale detection, retina → circular images.

So the constraint becomes the concept. A price war is fought over what everyone already has, and this film is built **only** from images everyone already has. We tell Nadella's four judgments through six of them, one photograph and one sentence per shot. Then the camera pulls back and the whole film turns out to be a **contact sheet of eleven public test images**, with one cell left: **№ 12 · 你的评测集 · 未公开**. The camera plunges into that empty cell. In its darkness, and only there, we set his line about private evals being a company's core IP.

The metaphor carries Nadella's points without stretching:

| His judgment (paraphrased, attributed on screen) | What we show | Why it fits |
|---|---|---|
| The price war; everyday compute commoditizes | A Pompeii coin spinning down like Euler's disk; then an espresso, the most everyday commodity on earth | A token is a coin. The coin settles, as prices do. |
| Frontier models serve only a few top niches | Falcon 9 on the pad, shown as a **narrow slit** | The layout itself is narrow: few, tall, rare |
| Copilot mixes cheap closed and open models daily | The 24 Pompeii coins; a violet ring hops to a different coin each weekday | Interchangeable tokens, routed |
| Alignment won't "fall out" of scale → zero trust | Hubble Deep Field (scale), push-in that **stops dead**; retina (identity); cameraman (every call recorded) | Scale, then identity and recording |
| Every company will have a private eval; it's core IP | The contact sheet of public test images, with an empty 12th cell | Public tests are shared by everyone; yours is the one not in any library |

### 1.2 Why it feels human-made (what a jury would notice)

1. **The limitation is the thesis.** We didn't decorate around small, cheap sample photos; we made a film *about* them. A generator can't make that move, because it requires knowing what these images are.
2. **Setup and payoff carried in micro-typography.** From the first frame, captions carry their library call, e.g. `skimage.data.coins()`. That reads as an archivist's tic until the contact sheet's header line, `from skimage import data`, pays it off. Plate numbers run 01 to 06 in order through the film, 07 to 11 complete on the sheet, and 12 is yours.
3. **Typography casts the speakers.** **宋 (Noto Serif SC)** is Nadella, always paraphrased and always under an attribution kicker. **黑 (Noto Sans SC)** is us: the attribution itself and "我们的解读", marked by a hanging violet square. **Mono (IBM Plex Mono)** is the archive. The client's attribution rule becomes the design system, so a paused frame always shows who is speaking.
4. **Geometry argues.** The everyday is the widest plate (espresso, 780 px); the frontier is the narrowest (rocket, a 400 px slit). Nobody has to explain it.
5. **Physical, not digital.** The coin's rattle accelerates to silence (real Euler's-disk kinematics). Prints develop highlights-first like paper in a tray. The camera stops dead when his mind changed. Grain, halation and gate weave stand in for any glows, particles, gradients or HUD.
6. **Music mirrors picture.** Eleven felt-piano notes sound as the eleven plates develop. The twelfth note is **withheld** and only resolves on the end card.
7. **Restraint.** Ten shots, one photo and one sentence each. One accent colour (brand violet), used in exactly three film moments. No boxes, no shadows, no stick figures, no centred title stacks.

### 1.3 Brand continuity without repeating the template

The account's DNA is kept as **material**, not layout: **ink** (a warmer #0B0A09 world), **paper** (the end card is the brand's #F2EEE7 paper) and **violet** (#5B2EFF on paper, lifted to #7A5CFF on dark, used as a *signal*, never a fill). Unlike both rejected attempts (`build/f/carousel/01.png`, `02.png`), this concept has no caption boxes, no hard shadows, no comic halftone, no purple gradient ground, no stick figure, no colour bars and no Anton numerals.

---

## 2. Film storyboard (59.0 s)

Conventions: coordinates are **CSS `left/top` of the text box** on the 1080×1920 grid. `⏎` = manual line break. Times are seconds at 30 fps (snap to the nearest frame). Styles (T-…) are defined in §4.2. bone / bone-7 / bone-5 / bone-4 are colour tokens (§4.3). Look-dev stills exist for every shot (`doc_lookdev/film_*.jpg`).

| # | In → Out (s) | Picture: asset · crop · treatment | Camera / motion | On-screen copy (exact) · style · position | Transition out | Sound |
|---|---|---|---|---|---|---|
| **S01 Hook: Euler's disk** | 0.00 → 3.60 | `coins.png` coin **#18** (Athena in helmet; crop 313,153→381,221) as heads, coin **#16** (facing head; 188,169→237,217) as tails, mapped on a Three.js disc (r 1, thickness 0.075, metalness 1, roughness 0.38, luminance bump). Pure dark field; one warm raking key; env `hdri_warehouse.exr` ×0.35; soft contact shadow only. At rest: B/W warm-print face, **3.62× source**, ellipse rx 114 / ry 65 centred **(464, 972)**. | 0–0.50 spin on edge (tilt α 88°→62°, rate Ω 14→5 Hz). 0.50–1.45 wobble α∝(1.45−t)^⅔, Ω∝(1.45−t)^−⅓ capped 32 Hz, 8-sample motion blur. **Lands 1.45** (2-frame bounce, 1.2 px shake decaying over 6 f). Camera elevation 10°, then crane to **34.7°** over 1.55–3.40 with `cubic-bezier(.45,0,.2,1)`; coin grows rx 96→114. Frame 0 already shows the spinning coin (never a black first frame). | K `微软 CEO 纳德拉判断`: T-KICK @ (90,356), in 0.12. H `大模型⏎要打价格战了`: T-DISPLAY @ (84,416), lines in 0.30/0.42, **legible by 1.0 s**. Sub `而且，会很残酷。`: T-SECOND @ (90,1120), in 1.75. Caption right-aligned to x 990, top 920: `图 01 局部 · No.18 / 24` (T-MONO-IDX) ⏎ `庞贝出土的古希腊钱币` (T-CAP) ⏎ `skimage.data.coins()` (T-MONO), in 2.15. | **Hard cut** at 3.60. The coin ellipse becomes the espresso **crema** at identical centre and size (circle match). | Coin flick 0.03; whirr → accelerating rattle; **clack 1.45**; 0.30 s near-silence; drone in 1.75; felt piano D3 1.78 |
| **S02 Everyday** | 3.60 → 8.80 | `coffee.png` full frame → **1.30×** = 780×520 @ (90,790). Colour print grade, sat 0.84, halation on rim and spoon. Crema centre lands at (464,972) = the coin. | Develop-in 3.60–4.70 (highlights first: the crema appears exactly where the coin was). Linear drift scale 1.000→1.060, anchored at crema (464,972). | RH `01 / 04 价格战` + `20VC · 2026.10.26` (first appearance, fade 3.62–4.02). K `他判断` @ (90,330) in 3.95. St `大多数企业的日常算力，⏎终将商品化。` T-ST @ (90,396) in 4.10/4.22. Cap @ (90,1330): `图 02  一杯浓缩咖啡` ⏎ `skimage.data.coffee() · Rachel Michetti · CC0` in 4.90 | Text out 8.28 (caption 8.16); hard cut 8.80 | Bloom 3.60; piano A3 3.62 |
| **S03 Frontier** | 8.80 → 14.00 | `rocket.jpg` **slit crop 223,0→423,427** (200×427), sky deblocked, **2.0×** = 400×854 @ (590,470). Sat 0.74; sodium lamps halate. | Develop 8.80–9.90. Linear push 1.000→1.050 anchored at nose cone (790,750). Lamp glint ±8 % twinkle at 0.7 Hz. | K `而在他看来` @ (90,470) in 9.15. St `前沿模型，⏎只服务少数⏎顶级场景。` T-ST @ (90,542) in 9.30/9.42/9.54. **Vertical caption** (T-VCAP) box left 512, top 470: `图 03　猎鹰 9 号与 DSCOVR　SpaceX　公有领域` ⏎ `skimage.data.rocket()` in 10.10 | Out 13.48; hard cut 14.00 | Bloom; piano E4 8.82; drone adds A2 |
| **S04 Mixing** | 14.00 → 20.80 | `coins.png` full plate, B/W warm print. Opens on **coin #18 alone at 3.5×, at (464,972)**, a callback to the hook. Pulls back to **2.0×** = 768×606 @ (90,720); the other 23 coins develop around it. | Pull-back 14.40–16.00 `cubic-bezier(.65,0,.35,1)`, scale interpolated in log space. Coins develop by distance from #18 (30 ms per 100 px, 600 ms each). **Router ring** (2 px #7A5CFF) draws on Mon 16.30, then hops on a 300 ms arc at Tue 16.80, Wed 17.30, Thu 17.80, Fri 18.30. Past rings stay at 42 % (the week's log). | RH roll → `02 / 04 混着用` (14.10). K `据报道` @ (90,330) in 14.70. St `微软 Copilot 内部，⏎每天都在混用⏎便宜的闭源与开源模型。` T-ST64 @ (90,394) in 14.90/15.02/15.14. Ring labels (T-RING) `周一 闭源`, `周二 开源`, `周三 开源`, `周四 闭源`, `周五 开源`. Cap @ (90,1346): `示意  一周的模型路由　底图：图 01` ⏎ `skimage.data.coins() · Brooklyn Museum` in 18.70 | Out 20.28 (rings fade 300 ms); hard cut 20.80 | Coin develop: 23 micro-tinks at −38 dB; **pings** D6 F6 A6 C7 D7 on each hop |
| **S05 Scale → the hard stop** | 20.80 → 28.20 | `hubble_deep_field.jpg` full → **1.08×** = 1080×942 @ (0,650), alpha feather top 160 / bottom 260 px into ink. Two layers: bright galaxies (FG) and space (BG). | Develop 20.80–22.00 (stars first). Push BG 1.00→1.10, FG 1.00→1.14 (parallax), anchored at galaxy (785,1161), `cubic-bezier(.5,0,1,1)` (accelerating) over 20.80–26.00. **26.00 HARD STOP**: velocity to 0 in one frame. Grain and weave keep living; only the camera dies. | RH → `03 / 04 改过的看法`. K `他以前以为` @ (90,330) in 21.30. St `规模够大，⏎对齐自然会来。` T-ST @ (90,396) in 21.50/21.62; out 25.50 (gone before the stop). Cap @ (90,1412): `图 04  哈勃极深场，2012　NASA　公有领域` ⏎ `skimage.data.hubble_deep_field()`. **After stop**: `现在，⏎他不这么想了。` T-BIG96 @ (86,350), **prints on in 2 frames at 26.10** (no blur, no motion) | Out 27.70; hard cut 28.20 | Drone and high shimmer swell with the push; **26.00–26.40 total digital silence**; room back 26.40; low piano D2 26.45 |
| **S06 Identity** | 28.20 → 33.20 | `retina.jpg` full disc → **0.5245×** = 740×740 @ (170,650). Sat 0.86; optic disc halates; the fundus camera's orientation notch is kept, not retouched. | Develop 28.20–29.30 (optic disc first, vessels last). Rotation 0°→−3.0° linear about the disc centre (540,1020); scale 1.00→1.04. *The only centred object in the film: the eye looks back.* | RH → `03 / 04 零信任` (roll only the Chinese). K `他说，微软不等对齐问题解决，` @ (90,330) in 28.50. St `先把模型包进⏎零信任架构。` T-ST @ (90,396) in 28.65/28.77. Cap @ (90,1404): `图 05  人眼视网膜　血管纹路因人而异，可用于身份识别` ⏎ `skimage.data.retina() · CC0` in 29.60 | Out 32.68; hard cut 33.20 | Bloom; warm pad Bb2 F3 D4 (1 s attack) |
| **S07 Recording** | 33.20 → 39.20 | `camera.png` (the cameraman) full → **1.5×** = 768×768 @ (90,684). B/W warm print. Index `图 06` (T-MONO-IDX, bone-5) right-aligned to x 858, top 652. | Develop 33.20–34.50. Linear push 1.00→1.04 at the lens (525,924). Text leaves 38.70; **the pull-back starts 39.20**. | K `据他介绍` @ (90,330) in 33.55. List T-LIST at x 90, tops 398 / 472 / 546, items in 33.75 / 34.15 / 34.55, hanging mono indices `01 02 03` at x 44: `每个 agent，都有自己的身份。` ⏎ `每一次调用，都留下记录。` ⏎ `权限，放在模型之外。` | **Continuous pull-back** into the contact sheet | Bloom (B/W); piano C4 |
| **S08 The contact sheet** | 39.20 → 48.40 | All 11 test images, downscaled (sharp), each fitted bottom-left in a 284×170 box. Columns x 90 / 398 / 706; rows top 492 / 738 / 984 / 1230. Cell 12 = 1 px hairline box 227×170 @ (706,1230). | Pull-back 39.20–41.00, `cubic-bezier(.83,0,.17,1)`: sheet scale 4.5176→1 (camera plate 768 px → its cell (706,738) 170 px). Cells develop in reading order 40.10…41.20 (110 ms apart, 500 ms each). Cell 12's hairline draws on 41.31 with no note. | RH → `04 / 04 私有评测集`. Meta `这 11 张，都是代码库自带的⏎公开示例图。` T-ST52 @ (90,282), in 40.80, out 44.10. Header `from skimage import data　·　matplotlib sample_data　·　11 / 12` T-MONO @ (90,446) in 41.00. Cell captions (T-SHEET, §3 table). Then **our reading**: ■ @ (62,304) + `我们的解读⏎人人都见过的考题，考不出差别。` T-READ @ (90,282), in 44.60, out 47.90 | **Continuous plunge** into cell 12 | Reverse bloom (space opening); **11 notes** 40.10–41.20; **rest at 41.31** (drone dips −6 dB); piano E4 44.60 |
| **S09 The twelfth plate** | 48.40 → 55.00 | Inside cell 12: ink only. | Plunge 48.40–50.00, `cubic-bezier(.7,0,.84,0)`: scale 1→11.294 about the box centre (819.5,1315), with 4-sample motion blur over the last 0.6 s. Black complete at 50.00. | K `纳德拉认为` @ (90,700) in 50.20. St `每家公司，⏎都会有自己的⏎私有评测集。` T-ST @ (90,772) in 50.35/50.47/50.59. Second `那是它的核心 IP。` T-SECOND @ (90,1092) in 51.60. Cap @ (90,1396): `图 12  你的评测集 · 未公开` ⏎ `not in any library` in 52.80 | Text out 54.50; **lamp-up** at 55.00 | Inhale riser 48.40→50.00, cut; **sub thump 50.00**; piano A3+E4 dyad 50.35 |
| **S10 Colophon** | 55.00 → 59.00 | Paper #F2EEE7, grain 0.022, vignette 0.05. | Lamp-up 55.00–55.80: ink → paper, `cubic-bezier(.4,0,.2,1)`, plus a 120 px bloom peaking mid-ramp (a light table switching on). Holds to 59.00. | Title `大模型，要打价格战了` Song 600 44, ink 72 % @ (90,640) in 55.70. ■ 16×16 #5B2EFF @ (58,742). **`Coo-Coo出海Ai实验室`** Hei 700 56, ink @ (90,718) in 55.90. Source (Hei 500 24/1.65, ink 62 %, full-width punctuation) @ (90,1236) in 56.20: `来源　20VC 播客，Harry Stebbings 对话 Satya Nadella，2026.10.26` ⏎ `片中观点为转述整理，非原话；我们的解读为本号观点。` ⏎ `图像　scikit-image 与 matplotlib 自带示例图，公有领域 / CC0` | End (last frame is a complete, shareable still) | Pad D major add9; **piano D5 at 55.30: the withheld 12th note resolves**; soft coin "ting" 55.90; fade to room by 59.00 |

### 2.1 Shot notes (rules that apply across the table)

- **Hook (first 1.5 s):** the motion (spinning coin with glints), the sound (metal rattle accelerating) and the claim (`大模型 / 要打价格战了`, fully in by 1.17 s) arrive together. The rattle's stop at 1.45 lands as the headline finishes, a physical full stop.
- **Exits:** all text of a shot leaves **520 ms before the cut** (420 ms fade + 100 ms of picture alone). Captions leave 120 ms earlier than everything else.
- **Reading load:** at most about **6 字/s** of visible time for every statement. Every frame is complete when paused (attribution kicker plus statement).
- **S01 compositing:** render the coin in its own 3D pass, then 2D-translate the layer so the coin's projected centre sits at (464,972) at every frame. The crane only changes elevation and size.
- **S04 opening:** plate origin at start = (464 − 347.0·3.5, 972 − 186.7·3.5) = (−750.5, 318.6); end = (90,720) at 2.0×. Coin #18 travels in a straight line (464,972)→(784,1093).
- **S04 ring geometry (end state, plate at (90,720), ring r = coin r·2 + 10):** Mon #18 (784,1093) r 73 · Tue #03 (401,822) r 56 · Wed #22 (578,1247) r 57 · Thu #11 (631,958) r 59 · Fri #20 (318,1251) r 52. Label box at (cx + 0.72r + 6, cy − 0.72r − 26) with a 3-step ink halo (`text-shadow: 0 0 4px, 0 0 8px, 0 0 12px #0B0A09`). Current day is bone; past days bone-5.
- **S07→S08 pull-back:** sheet transform at start s₀ = 768/170 = 4.5176, T₀ = (90 − 706·s₀, 684 − 738·s₀). Interpolate log(s) with the easing; draw each cell **from its source pixels** at the current scale (Canvas `drawImage` with transform). Never scale up a thumbnail: frame 0 of the pull-back must be pixel-identical to S07's last frame.
- **Running head:** shown S02–S09 only; it sits outside the camera transform (it doesn't zoom in S08/S09).

### 2.2 Optional soundbite slots (film is complete without them)

| Slot | Insert at | Content to look for in the 20VC audio | Frame design |
|---|---|---|---|
| A | 8.80 (between S02 and S03) | His commoditization / price-war point (6–10 s) | 16:9 picture 900×506 @ (90,700), same LUT (sat 0.80) and grain, develops in like any plate (600 ms). Running head left changes to `原声`. Mono caption @ (90,1226): `Satya Nadella · 20VC · 2026.10.26`. Subtitles Hei 500 46/1.4, bone, max 2 lines @ (90,1290). Subtitles must be a **verified translation of the actual audio**, marked `字幕为翻译`, with no quotation marks. |
| B | 28.20 (after the hard stop, before S06) | His "changed my mind" or zero-trust passage | same |

Music holds a drone bed at both points (loopable 4 s region), ducks −10 dB with 300 ms ramps, and the dialogue sits at −18 LUFS. **Runtime:** one slot of 8 s or less requires dropping S07 (its list lives on in carousel frame 4) and trimming S05 by 1.0 s to stay at or under 60 s. Two slots also drop S03 if slot A covers the frontier point.

### 2.3 Copy deck (every on-screen string, in order)

```
S01  微软 CEO 纳德拉判断 | 大模型⏎要打价格战了 | 而且，会很残酷。 | 图 01 局部 · No.18 / 24 ⏎ 庞贝出土的古希腊钱币 ⏎ skimage.data.coins()
S02  01 / 04 价格战 · 20VC · 2026.10.26 | 他判断 | 大多数企业的日常算力，⏎终将商品化。 | 图 02  一杯浓缩咖啡 ⏎ skimage.data.coffee() · Rachel Michetti · CC0
S03  而在他看来 | 前沿模型，⏎只服务少数⏎顶级场景。 | 图 03　猎鹰 9 号与 DSCOVR　SpaceX　公有领域 ⏎ skimage.data.rocket()
S04  02 / 04 混着用 | 据报道 | 微软 Copilot 内部，⏎每天都在混用⏎便宜的闭源与开源模型。 | 周一 闭源 · 周二 开源 · 周三 开源 · 周四 闭源 · 周五 开源 | 示意  一周的模型路由　底图：图 01 ⏎ skimage.data.coins() · Brooklyn Museum
S05  03 / 04 改过的看法 | 他以前以为 | 规模够大，⏎对齐自然会来。 | 图 04  哈勃极深场，2012　NASA　公有领域 ⏎ skimage.data.hubble_deep_field() | 现在，⏎他不这么想了。
S06  03 / 04 零信任 | 他说，微软不等对齐问题解决， | 先把模型包进⏎零信任架构。 | 图 05  人眼视网膜　血管纹路因人而异，可用于身份识别 ⏎ skimage.data.retina() · CC0
S07  据他介绍 | 01 每个 agent，都有自己的身份。⏎ 02 每一次调用，都留下记录。⏎ 03 权限，放在模型之外。 | 图 06
S08  04 / 04 私有评测集 | 这 11 张，都是代码库自带的⏎公开示例图。 | from skimage import data　·　matplotlib sample_data　·　11 / 12 | [12 cell captions, §3 C5 table] | 我们的解读⏎人人都见过的考题，考不出差别。
S09  纳德拉认为 | 每家公司，⏎都会有自己的⏎私有评测集。 | 那是它的核心 IP。 | 图 12  你的评测集 · 未公开 ⏎ not in any library
S10  大模型，要打价格战了 | Coo-Coo出海Ai实验室 | 来源 … (as in table)
```

---

## 3. Carousel: 7 frames, 1080×1440 (3:4)

Grid: margins 90 / 90. Running head top **96** (mono 500 20 + Hei 500 22). Kicker top **156** (Hei 500 40). Statements from top **212**. Bottom line top **1364**: ■ 12×12 #7A5CFF @ (90,1373), `Coo-Coo出海Ai实验室` Hei 500 26 bone-7 @ (114,1364), page index mono 500 20 right-aligned at x 990. Dark frames use the film grade and post (§4.4–4.5). Look-dev: `doc_lookdev/carousel_01/02/04/07*.jpg`.

**C1 · Cover (also the video cover)**: `carousel_01_cover.jpg`
- Kicker `微软 CEO 纳德拉判断` Hei 500 40 bone-5 @ (90,150). Right, same baseline: `20VC · 2026.10.26` mono 500 20 bone-4, right edge 990, top 162.
- Headline `大模型⏎要打价格战了`: Song 700 **150**/1.08, tracking −0.015em, bone @ (84,206). Line 2 is exactly 900 px wide. **No line-end comma** in display sizes; the line break is the pause.
- Plate: `coins.png` full, **2.0×** = 768×606 @ (222,650), right-aligned to the margin, B/W warm print.
- One violet ring (2 px #7A5CFF) around coin #18: centre (916,1023), r 73. The only saturated mark on the cover.
- Caption right-aligned at x 990, top 1276: `图 01  庞贝出土的古希腊钱币` ⏎ `No.18 / 24 · skimage.data.coins()`.
- Bottom line: account mark only, no page index.
- **As a thumbnail** (2-column feed, about 0.43×): the headline is about 65 px tall per glyph, two short lines that read in one glance. The coin grid reads as "money" even when tiny. The violet ring is the one point of colour, so the eye path is headline → ring → grid. A dark, warm cover in a mostly light feed gets contrast without shouting. Nothing essential is smaller than 40 px.

**C2 · 01 价格战** (`carousel_02_price_war.jpg`)
- RH `01 / 04 价格战` · `20VC · 2026.10.26`.
- Kicker `纳德拉判断` @ (90,156). St `大多数企业的日常算力，⏎终将商品化。` Song 600 64/1.28 @ (90,212).
- Espresso **1.30×** 780×520 @ (90,410). Caption @ (90,946): `图 02  一杯浓缩咖啡` ⏎ `skimage.data.coffee() · CC0`.
- Kicker `而在他看来` @ (90,1080). St `前沿模型，只服务⏎少数顶级场景。` Song 600 56/1.30 @ (90,1136).
- Rocket slit (same crop) downscaled to **132×282** @ (858,1012), sharp. Vertical caption (T-VCAP at 20 px) `图 03　猎鹰 9 号` box left 812, top 1012.
- Page `02 / 07`. *Wide everyday vs narrow frontier, on one page.*

**C3 · 02 混着用**
- RH `02 / 04 混着用`. Kicker `据报道` @ (90,156). St `微软 Copilot 内部，⏎每天都在混用⏎便宜的闭源与开源模型。` Song 600 60/1.28 @ (90,212).
- Coins 2.0× 768×606 @ (90,500). All five rings in end state (centres = (90+2x, 500+2y)): Mon (784,873) r 73 · Tue (401,602) r 56 · Wed (578,1027) r 57 · Thu (631,738) r 59 · Fri (318,1031) r 52. Fri at 100 %, others at 42 %. Labels as in the film.
- Caption @ (90,1122): `示意  一周的模型路由　底图：图 01` ⏎ `skimage.data.coins() · Brooklyn Museum`.
- Our reading: ■ 10×10 #7A5CFF @ (62,1214); `我们的解读` Hei 500 44 bone-5 @ (90,1196); `架构上，要能随时换模型。` Hei 500 44 bone @ (90,1260).
- Page `03 / 07`.

**C4 · 03 改过的看法 → 零信任** (`carousel_04_alignment_zero_trust.jpg`)
- RH `03 / 04 改过的看法`.
- Hubble band: source rows 214–658, full width → 1.08× = **1080×480** @ (0,136), bottom 140 px feathered into ink.
- Kicker `他以前以为` @ (90,640). `规模够大，对齐自然会来。` Song 500 52 bone-7 @ (90,694). `现在，他不这么想了。` Song 700 76 bone @ (88,772).
- 1 px rule (rgba 236,230,218,.22) x 90–990 at y 916.
- Kicker `据他介绍，微软不等对齐被解决，` @ (90,952). `先把模型包进零信任架构：` Song 600 52 @ (90,1004).
- List Song 500 44 / 64 px pitch, tops 1086 / 1150 / 1214, hanging mono indices at x 44: `每个 agent，都有自己的身份。` / `每一次调用，都留下记录。` / `权限，放在模型之外。`
- Page `04 / 07`.

**C5 · 04 公开示例图 (the reveal)**
- RH `04 / 04 私有评测集`.
- `这 11 张，都是代码库自带的⏎公开示例图。` Song 600 48/1.36 @ (90,150).
- Header `from skimage import data　·　matplotlib sample_data　·　11 / 12` mono 400 20 bone-4 @ (90,304).
- Sheet: box **284×150**, columns x 90/398/706, row tops **344 / 568 / 792 / 1016**. Thumbnails bottom-left aligned. Captions 8 px under the box: line 1 = mono 500 18 index (bone-4) + Hei 500 20 title (bone-7); line 2 = Hei 500 18 (bone-4). Cell 12: hairline box 200×150.

| № | Title | Line 2 (the "exam" it exists for, from its docstring) |
|---|---|---|
| 01 | 庞贝出土的钱币 | 分割测试 |
| 02 | 一杯浓缩咖啡 | 椭圆与纹理 |
| 03 | 猎鹰 9 号 | 示例 |
| 04 | 哈勃极深场 | 多尺度检测 |
| 05 | 人眼视网膜 | 圆形图像 |
| 06 | 摄影师 | 分割与去噪 |
| 07 | 宇航员 Eileen Collins | 示例 |
| 08 | Grace Hopper | 示例 · matplotlib |
| 09 | 月面 | 直方图均衡 |
| 10 | 手写公式 | 角点检测 |
| 11 | 运动模糊的钟 | 反卷积 |
| **12** | **你的评测集** (bone) | 未公开 |

- Our reading, one line @ (90,1250): ■ @ (62,1270) + `我们的解读　人人都见过的考题，考不出差别。` Hei 500 44, label bone-5, text bone. It measures about 858 px with `halt`.
- Page `05 / 07`. (The film's S08 uses the same table at 284×170 boxes, captions Hei 22 / 19.)

**C6 · 04 私有评测集**
- RH `04 / 04 私有评测集`.
- Kicker `纳德拉认为` @ (90,180). St `每家公司，⏎都会有自己的⏎私有评测集。` Song 600 76/1.26 @ (90,240). `那是它的核心 IP。` Song 500 56 bone-7 @ (90,556).
- **The empty plate:** 1 px hairline rgba(236,230,218,.22), **640×480 @ (90,700)**, nothing inside.
- Caption @ (90,1198): `图 12  你的评测集 · 未公开` ⏎ `not in any library`.
- Page `06 / 07`.

**C7 · 我们的解读 + colophon (paper)** (`carousel_07_reading_colophon.jpg`)
- Paper #F2EEE7, ink #15121B, grain 0.022, vignette 0.05.
- ■ 12×12 #5B2EFF @ (62,164) + `我们的解读` Hei 500 40, ink 55 % @ (90,150). `07 / 07` mono 500 20, ink 45 %, right edge 990, top 162.
- Title `价格战之后，⏎什么还属于你？` Song 700 76/1.22 @ (88,214).
- Three blocks, tops **470 / 646 / 822**: mono index (21, ink 45 %) at (44, top+12); lead Hei 700 44 at (90, top); body Hei 500 44, ink 78 %, at (90, top+62):
  - `01  多模型路由` / `架构上随时能换模型，别押一家。`
  - `02  私有评测集` / `用你自己的真实场景出题，别只看公开榜单。`
  - `03  零信任` / `身份、日志、权限，放在模型之外。`
- Rule 1 px, ink 16 %, at y 1030. ■ 14×14 #5B2EFF @ (62,1092). `Coo-Coo出海Ai实验室` Hei 700 40 @ (90,1074).
- Source, Hei 500 22/1.7, ink 62 %, **full-width punctuation (no `halt`)**, @ (90,1150), manual lines:
  `来源　20VC 播客，Harry Stebbings 对话 Satya Nadella，2026.10.26。`⏎`观点为转述整理，非原话；四个判断均据该期节目的二手报道整理。`⏎`我们的解读为本号观点。`⏎`图像　scikit-image / matplotlib 自带示例图，公有领域或 CC0：`⏎ mono 19: `NASA · SpaceX · Brooklyn Museum · U.S. Navy · Wikimedia Commons ·`⏎`Rachel Michetti · Lav Varshney · Stefan van der Walt`. Measured ink extent x 91–838, bottom 1367.

---

## 4. Design system

### 4.1 Grid

- **Film 1080×1920.** Margins 90/90 (text axis x 90, right margin 990). 12 columns × 64 px with 12 px gutters (column k starts at 90 + 76k). Optical indents: 148 px display at x 84, 96 px at x 86, 76 px titles on paper at x 88 (compensates the Song left side-bearing).
- **Horizontal zones:** 0–154 avoid (status bar) · **220** running head · **330–620** kicker + statement · **650–1460** plate zone · captions finish by **1476** · **≥1498 nothing essential** (XHS UI).
- **Vertical rhythm:** snap to 2 px. Kicker top + 66 = first statement line. Statement line pitch = size × leading. Caption 20 px under plates (or 10 px under sheet boxes).
- **Fixed anchors:** coin and crema centre (464,972), rocket slit x 590–990, sheet columns 90/398/706, empty plate (706,1230).
- **Carousel 1080×1440:** margins 90; running head 96; kicker 156; statements 212; bottom line 1364.

### 4.2 Type: three voices

| Voice | Face (installed, verified) | Used for |
|---|---|---|
| **宋 · the record** | Noto Serif SC 500/600/700 | Nadella's views (always paraphrased, always under a kicker), titles |
| **黑 · us** | Noto Sans SC 500/700 | Attribution kickers, 我们的解读, captions, labels, account mark |
| **Mono · the archive** | IBM Plex Mono 400/500 | Plate indices, library calls, dates, running-head numbers, list indices |

| Token | Face · weight | Size / leading | Tracking | Colour |
|---|---|---|---|---|
| T-DISPLAY | Song 700 | 148 / 1.10 (cover 150 / 1.08) | −0.015em | bone |
| T-BIG96 | Song 700 | 96 / 1.16 | −0.01em | bone |
| T-ST | Song 600 | 76 / 1.26 | 0 | bone |
| T-ST64 | Song 600 | 64 / 1.28 | 0 | bone |
| T-ST52 / T-LIST | Song 600 | 52 / 1.36 (list: 74 px pitch) | 0 | bone |
| T-SECOND | Song 500 | 56 / 1.34 | 0 | bone-7 |
| T-READ | Hei 500 | 52 / 1.42 (label in bone-5) | 0 | bone |
| T-KICK | Hei 500 | 44 / 1.0 (carousel 40) | +0.04em | bone-5 |
| T-CAP | Hei 500 | 26 / 1.35 | +0.04em | bone-5 |
| T-MONO | Plex Mono 400 | 21 / 1.5 | +0.02em | bone-4 |
| T-MONO-IDX | Plex Mono 500 | 21 | +0.06em | bone-5 |
| T-RH | Plex Mono 500 21 + Hei 500 22 | 24 px line | +0.10em / +0.06em | bone-4 |
| T-VCAP | Hei 500 24, `writing-mode: vertical-rl` (line 2 mono 20) | 1.7 | +0.14em | bone-5 / bone-4 |
| T-RING | Hei 500 24 + mono 500 20 day | 1.0 | +0.04em | bone or bone-5 |
| T-SHEET | Hei 500 22 + mono 500 19 index / Hei 500 19 | 1.3 / 1.45 | +0.03em | bone-7 / bone-4 |

**CJK typesetting rules. These were tested in this repo's Chromium 153, and the findings matter:**
- **`font-feature-settings: "halt" 1`** on all type **≥ 40 px**. It gives proper half-width punctuation compression. `palt` and `text-spacing-trim` have **no effect** with these fontsource subsets in this build (`CSS.supports('text-spacing-trim','trim-all')` is false). Type **< 40 px** (captions, colophon) keeps full-width punctuation, which reads better small.
- Hanzi–Latin spacing: type the ASCII spaces exactly as in the copy deck (`微软 Copilot 内部`). `text-autospace: normal` is supported if you prefer automatic spacing; never use both.
- **Never use LXGW WenKai for Chinese.** The installed `@fontsource/lxgw-wenkai` ships **only a Latin subset**, so Chinese silently falls back to WenQuanYi Zen Hei (an instant "cheap" tell). ZCOOL XiaoWei was tested and rejected (uneven spacing, tiny punctuation).
- **Never put Chinese inside a Plex Mono span.** Plex has no CJK; in vertical mode the fallback glyphs overlapped in look-dev. Split Chinese into a Hei span.
- Manual line breaks only, per the copy deck. No orphans. No line-end commas in display titles. No quotation marks anywhere.
- No per-character animation, no outlines, no text shadows (except the 3-step ink halo behind ring labels), no gradient text.

### 4.3 Colour tokens

| Token | Hex | Use |
|---|---|---|
| `--ink` | **#0B0A09** | The world. Never #000; photo blacks are lifted to exactly this so plates melt into the frame |
| `--bone` | #ECE6DA | Primary type (about 15:1 on ink) |
| `--bone-7` | #BDB5A7 | Second sentences, sheet titles |
| `--bone-5` | #8E877B | Kickers, captions, our-reading label (about 5.3:1) |
| `--bone-4` | #77716A | Mono lines, running head (about 4.1:1) |
| `--rule` | rgba(236,230,218,.22) | Hairlines: the empty plate, the C4 divider |
| `--signal` | **#7A5CFF** | Brand violet lifted for dark ground: router ring, our-reading square, account square on dark |
| `--brand` | **#5B2EFF** | Violet on paper only |
| `--paper` | **#F2EEE7** | Colophon (the brand's own end-card paper) |
| `--ink-p` | #15121B | Brand ink on paper |
| `--halation` | #FF6A3D | Halation tint (photo layer only) |

Violet appears in the film **three times**: the router ring (S04), the our-reading square (S08), the account square (S10).

### 4.4 Grade (the "warm print" LUT)

Apply to photos in Python before compositing. The prototype is `doc_lookdev/src/treat.py`.
- **Lift:** output black = 0.043 (= #0B0A09).
- **Gamma:** 1.06 (slightly denser mids).
- **Gain:** 0.94 (peak white ≈ #EFE7D9, never pure white).
- **Shoulder:** soft exponential roll-off above 0.82 (knee strength 1.4).
- **Saturation:** global 0.80; coffee 0.84, rocket 0.74, Hubble 0.86, retina 0.86, sheet colour thumbnails 0.82.
- **Tone:** one warm print tone, **no teal/orange split**. Shadows ×(1.04, 1.00, 0.94), highlights ×(1.02, 1.00, 0.95), blended by w = clamp(1 − 2L).
- **B/W images** (coins, camera, moon, text, clock): luminance → 3-stop ramp #0C0B0A → #8C857A → #EDE6D6 (warm, selenium-like), after the same curve.
- **Halation (photos only, never type):** threshold L 0.80 (Hubble 0.62, retina 0.70, rocket 0.78), Gaussian σ 10 px at display size, tint #FF6A3D (1.00, 0.42, 0.22), additive strength 0.22 (retina 0.28).
- **Upscaling:** Lanczos, then unsharp (radius 0.8×scale, 45 %, threshold 2). Rocket sky deblocked first (§7).

### 4.5 Film post (whole frame, after type; GLSL pass)

- **Print bloom:** Gaussian 0.6 px mixed 20 %. Removes the razor-digital type edge; type feels printed.
- **Vignette:** elliptical, amount 0.14, power 2.2 (paper 0.05).
- **Grain:** monochrome Gaussian noise generated at 1/1.35 resolution, bicubic up, σ **0.034** × (0.30 + 0.70·4L(1−L)), reseeded every frame. Paper σ 0.022. Grain runs from frame 0 and never stops, including through the hard stop.
- **Gate weave:** whole frame, x ±0.45 px, y ±0.30 px, rotation ±0.02°, from 0.8 Hz + 0.3 Hz sines plus low noise; bilinear sub-pixel.
- **Exposure flicker:** ±0.6 %, 6 Hz low-passed noise.
- **Not used:** chromatic aberration, light leaks, dust, scratches, letterbox, bloom on type, glow, lens flares.
- **Output:** dither before 8-bit. x264 CRF 16, preset slow, `-tune grain`, yuv420p, BT.709 tags. Test one upload: if XHS re-encoding blotches the dark grain, raise grain size to 1.5 px rather than lowering σ.

### 4.6 Micro-detail system

1. **Plate index** `图 NN` (mono 500 21, bone-5) with **one global numbering**: 01 coins, 02 coffee, 03 rocket, 04 Hubble, 05 retina, 06 camera, 07 astronaut, 08 Grace Hopper, 09 moon, 10 text, 11 clock, **12 yours**. The hook coin is `图 01 局部` (a detail of plate 01).
2. **Library call** under each plate title (mono 400 21, bone-4): the exact verified function, e.g. `skimage.data.hubble_deep_field()`. Paid off by the sheet header `from skimage import data`.
3. **Specimen number** `No.18 / 24`, from our row-major coin order. Seeds the 24-coin reveal in S04.
4. **Running head:** chapter `01 / 04 价格战`, right `20VC · 2026.10.26`. Changes with a 360 ms vertical roll (old −12 px and out, new from +12 px; `cubic-bezier(.2,0,0,1)`).
5. **Vertical captions** for vertical plates (rocket): native CJK vertical setting, 16 px off the plate edge.
6. **Hanging marks:** the violet our-reading square hangs at x 62 (28 px outside the text axis); list indices hang at x 44.
7. **Hairlines** exist only where something is absent (the empty plate) or a page divides (C4, C7). Photos are borderless prints with no frames and no shadows.
8. **Router ring:** 2 px stroke, r = coin r·2 + 10, a 42 % trail of past days (the week is a log).
9. **The withheld element:** the empty cell, the missing 12th note, and `not in any library`. Three channels say the same thing.

---

## 5. Motion language

### 5.1 Easing library

| Name | Curve | Duration | Use |
|---|---|---|---|
| E-DRIFT | linear | whole shot | Rostrum push/rotate (constant velocity, already moving at the cut) |
| E-SETTLE | `cubic-bezier(.16,1,.3,1)` | 900 ms | Text in |
| E-LEAVE | `cubic-bezier(.7,0,.84,0)` | 420 ms | Text out |
| E-DEVELOP | `cubic-bezier(.22,.61,.36,1)` | 1100 colour / 1300 B/W / 500 sheet cell / 600 coin | Develop threshold |
| E-TRAVEL | `cubic-bezier(.65,0,.35,1)` | 300 ring hop · 1600 coin pull-back | Moves between known points |
| E-REVEAL | `cubic-bezier(.83,0,.17,1)` | 1800 | Sheet pull-back |
| E-PLUNGE | `cubic-bezier(.7,0,.84,0)` | 1600 | Into the 12th plate |
| E-CRANE | `cubic-bezier(.45,0,.2,1)` | 1850 | S01 crane |
| E-ACCEL | `cubic-bezier(.5,0,1,1)` | 5200 | Hubble push into the hard stop |
| E-LAMP | `cubic-bezier(.4,0,.2,1)` | 800 | Lamp-up to paper |
| E-ROLL | `cubic-bezier(.2,0,0,1)` | 360 | Running head |

### 5.2 Rules

- **Text in:** opacity 0→1, blur 8 px→0, translateY +14 px→0, letter-spacing +0.04em→0, E-SETTLE 900 ms. **Text out:** opacity →0, blur 0→6 px, no movement, E-LEAVE 420 ms.
- **Stagger:** the kicker leads the statement by 150–200 ms; lines of one sentence 120 ms; list items 400 ms; captions arrive 400–600 ms after their plate finishes developing and leave 120 ms before everything else.
- **The one exception:** `现在，他不这么想了。` prints on in **2 frames** with no blur and no movement, matching the hard stop.
- **Photos never cross-dissolve.** They enter by develop and leave by hard cut, or by a continuous camera move (pull-back, plunge).
- **Drift rates:** colour plates 1.0–1.2 %/s scale; B/W 0.7–0.8 %/s; retina −0.6°/s rotation; Hubble about 1.9 %/s accelerating. **Parallax only in Hubble:** FG galaxies (L > 0.30 after a 2 px blur, dilated 3 px, feathered 2 px) move 40 % faster than BG. BG holes are filled with a 15 px median, which is invisible on black.
- **Transitions:** hard cuts on sound events; three continuous moves (S07→S08 pull-back, S08→S09 plunge, S09→S10 lamp-up). No wipes, slides, zoom-blur transitions, glitch or whip pans.
- Never: bounce, overshoot, elastic, text scale-pops, per-character typing, rotating text.

### 5.3 Signature moves

1. **Euler's disk (cold open).** A real Pompeii coin spins down with physically correct kinematics: tilt α ∝ (t₀−t)^⅔, precession Ω ∝ (t₀−t)^−⅓. Its rattle accelerates to an abrupt stop as the headline completes, then the camera cranes until the coin's ellipse equals the espresso crema and we cut on the circle. It is a hook made of physics, not effects.
2. **Develop.** Every photograph comes up like a print in the tray, by its own luminance:
   ```glsl
   float L = dot(c.rgb, vec3(.2126,.7152,.0722));
   float g = grain(fragCoord/1.35, frame) - .5;          // same grain field as post
   float e = 1.0 - 1.15*ease(t);                        // threshold sweeps bright → dark
   float a = smoothstep(e - .10, e + .02, L + g*.12);
   col = c.rgb*a + halation(c)*(1.8 - .8*ease(t))*step(.8, L);  // highlights flare, then settle
   ```
   Stars come first in Hubble, coins before the cloth, the crema before the cup.
3. **The Twelfth Plate.** The cameraman pulls back to become cell 06 of a contact sheet of eleven public test images. The cells develop one by one, each with a piano note. The twelfth is an empty hairline box and the twelfth note never comes. The camera plunges into it until the screen is its darkness, and Nadella's private-eval line appears inside it. The withheld note resolves only on the end card.
   *(Plus the **hard stop** in S05: an accelerating push through the deep field that dies in one frame, with total digital silence, when his mind changed.)*

---

## 6. Sound design (all synthesized in numpy, 48 kHz / 24-bit)

### 6.1 Palette

| Voice | Recipe |
|---|---|
| ROOM | Pink noise → band-pass 60 Hz–6 kHz, −46 dBFS RMS, ±1.5 dB wander at 0.05 Hz; stereo = two noises at 0.7 correlation |
| COIN | Damped sines, f₀ 2350 Hz, ratios 1.00 / 1.59 / 2.14 / 2.65 / 3.16, τ 0.9 / 0.6 / 0.45 / 0.30 / 0.20 s, random phase; excitation 1.5 ms (tick) or 4 ms (flick) noise burst |
| RATTLE | Tick train at instantaneous rate Ω(t)/2π (5→32 Hz, ±3 % jitter). Each tick: 1.5 ms noise band-passed 3–7 kHz (−18 dB) + COIN at −28 dB + 180 Hz "table" sine 8 ms (−26 dB). Phase A whirr: band-passed noise 4–8 kHz amplitude-modulated at Ω |
| CLACK | Tick ×3 + 120 Hz sine 40 ms + COIN with τ ×1.5; peak −10 dBFS |
| DRONE | Sines D1 36.71 Hz, D2 73.42 Hz (+ copy at +0.15 Hz for slow beating), A2 110 Hz; low-pass 300 Hz; ±2 dB LFO at 0.07 Hz |
| FELT PIANO | Partials n = 1…10, fₙ = n·f₀·√(1+Bn²), B = 3.5e-4; aₙ = n^−1.3 · 1/(1+(fₙ/1800)²); attack 8 ms; decay τₙ = 3.2 s/(1+0.35n); hammer = 5 ms noise low-passed 1.2 kHz at −24 dB |
| BLOOM | Pink noise → 2-pole low-pass sweeping 250→1600 Hz (exponential) over 0.9 s; attack 0.6 / release 0.6 s; −34 dBFS. Reverse version for the pull-back |
| PING | COIN partial set transposed to D6 1174.7 / F6 1396.9 / A6 1760 / C7 2093 / D7 2349.3 Hz; τ 0.35 s; −24 → −20 dBFS |
| SHIMMER | Sines D5 + A5, −36 dBFS rising to −28 with the Hubble push |
| RISER | Pink noise → low-pass 300→3000 Hz over 1.6 s, −30→−22 dB, hard cut at the end |
| SUB | 32.7 Hz + 65.4 Hz (−10 dB), attack 15 ms, τ 0.45 s; −14 dBFS |
| PAD | D3 146.83 / A3 220 / F♯4 369.99 / E5 659.26 Hz, 3 voices each at ±3 cents, attack 0.8 s, low-pass 3 kHz, −24 dBFS |
| REVERB | Convolution with a synthetic stereo IR: noise × exp(−6.91t/RT60), RT60 2.2 s (music) / 1.0 s (coin, ping). HF damping 8→2 kHz over the tail. Early taps 7/13/19/29/41 ms at −8…−18 dB; pre-delay 12 ms; wet −14 dB (piano) / −18 dB (coin) |

### 6.2 Cue sheet

| Time (s) | Picture | Event |
|---|---|---|
| 0.00 | S01 coin already spinning | ROOM fades in over 0.25 s (no hard digital start) |
| 0.03 | | COIN flick, −14 dBFS |
| 0.00–0.50 | spin on edge | Whirr |
| 0.50–1.45 | wobble | RATTLE accelerating 5→32 Hz |
| **1.45** | **coin lands** | **CLACK** |
| 1.45–1.75 | headline holds | Near-silence (ROOM + ring tail) |
| 1.75 | sub-line | DRONE in (1.5 s fade to −30); piano D3 at 1.78 |
| 3.60 | S02 cut | BLOOM; piano A3 |
| 8.80 | S03 cut | BLOOM; piano E4; DRONE adds A2 |
| 14.00 | S04 coin | BLOOM; piano F3 |
| 14.40–16.00 | 23 coins develop | 23 micro-tinks, −38 dB, in develop order |
| 16.30 / 16.80 / 17.30 / 17.80 / 18.30 | ring hops Mon–Fri | PING D6 / F6 / A6 / C7 / D7 |
| 20.80–26.00 | Hubble push | BLOOM; DRONE swell to −26; SHIMMER rising |
| **26.00** | **hard stop** | **Every track to digital zero, including ROOM, until 26.40** |
| 26.40 / 26.45 | `现在，他不这么想了` | ROOM back at −50; piano D2, long decay, −20 |
| 28.20 | S06 retina | BLOOM; PAD-lite Bb2 F3 D4 (1 s attack, −30) |
| 33.20 | S07 camera | BLOOM; piano C4 |
| 39.20–41.00 | pull-back | Reverse BLOOM (space opening) |
| 40.10–41.20 | cells 01–11 develop | **Eleven notes** 110 ms apart, −24→−20 dB: D4 A4 E5 · B♭3 F4 C5 · F4 C5 G5 · C4 G4 (Dm9, B♭, F, C arpeggios in 1-5-9) |
| **41.31** | cell 12 draws on | **The 12th note (D5) is withheld**; DRONE dips −6 dB for 0.6 s |
| 44.60 | our reading | Piano E4, soft |
| 48.40–50.00 | plunge | RISER, hard cut |
| **50.00** | darkness | **SUB**; ROOM drops to −52 |
| 50.35 | `纳德拉认为…` | Piano dyad A3 + E4, −24; DRONE D1 at −34 |
| 55.00 | lamp-up | PAD D major add9 |
| **55.30** | colophon | **Piano D5: the withheld 12th note resolves** |
| 55.90 | account mark | COIN "ting" at −30 (callback to frame 0) |
| 56.50–59.00 | hold | Everything fades to ROOM; ROOM out by 59.00 |

### 6.3 Mix and export

Music peaks around −6 dBFS. Integrated −16 LUFS, true peak −1 dBTP. Mono-compatible (check the pad and room in mono). 48 kHz WAV → AAC 256 kbps in the MP4. Every audio event is sample-locked to the frame-snapped picture time.

---

## 7. Asset treatment recipes

Max display scales were set by look-dev tests (`doc_lookdev/`): 1:1 views of each photo graded and grained at these sizes.

| Asset (source px) | Used in | Crop box (source px) | Display | Max | Grade / treatment notes |
|---|---|---|---|---|---|
| **coins.png** (384×303, gray) | S01, S04, C1, C3, sheet 01 | Hook coin **#18** centre (347.0,186.7), r 31.6, box **313,153→381,221**. Tails **#16** centre (212.4,193.1), r 23.5, box 188,169→237,217 (scaled to r 31.6). Plate: full frame | S01 rest 3.62× (rx 114, foreshortened ry 65); S04 start 3.5× (one coin, in motion); plate **2.0× = 768×606**; sheet 228×180→fit | Single coin 3.6× (only at rest after the crane); plate 2.0× | B/W warm ramp. **Mask:** the textbook skimage segmentation (Sobel elevation, watershed with markers <30 bg / >150 coin, fill holes), dilated 1 px, feathered 0.8 px. That is the very algorithm this image was made to test. **Bump** for 3D: G(L,0.7) − G(L,5), normalized, bumpScale 0.015. Coin order: row-major by row band then x (24 coins, radii 18.5–31.6) |
| **coffee.png** (600×400) | S02, C2, sheet 02 | Full frame. Crema ellipse centre **(288,140)**, semi-axes **88×50** (measured) | **1.30× = 780×520** | 1.5× | Sat 0.84; halation on rim, spoon, saucer glints. The crema at 1.30× = rx 114 / ry 65: the match target |
| **rocket.jpg** (640×427) | S03, C2, sheet 03 | Slit **223,0→423,427** (vehicle body x 302–344, nose about y 128) | S03 **2.0× = 400×854**; C2 0.66× = 132×282 | 2.0× | **Deblock the sky first:** mask = rows < 330 and gradient < 0.012 (after 1 px blur); blend a σ 1.4 Gaussian into the mask before upscaling (raw JPEG blocks show at 2×). Sat 0.74; halation thr 0.78 on sodium lamps; star-filter glint twinkle in motion |
| **hubble_deep_field.jpg** (1000×872) | S05, C4, sheet 04 | Full; carousel band rows **214–658** | **1.08× = 1080×942**, push to 1.10 BG / 1.14 FG; band 1080×480 | 1.2× | Sat 0.86; lift space to exactly #0B0A09 (no crush); halation thr 0.62 (stars bloom). Alpha feather top 160 / bottom 260 (film), bottom 140 (band). **Never mirror or extend the field.** Push anchor = galaxy (727,473) |
| **retina.jpg** (1411×1411) | S06, sheet 05 | Full disc, centre (705,702), Ø 1395; optic disc (233,655); fovea (703,705) | **0.5245× = 740×740** | 1.36× | Sat 0.86; halation thr 0.70, strength 0.28 (optic disc glows). Keep the orientation notch. Rotation about the disc centre only |
| **camera.png** (512×512, gray) | S07, sheet 06 | Full; lens about (290,160) | **1.5× = 768×768** | 1.75× | B/W warm ramp; push anchor at the lens. Credit: photographer Lav Varshney (CC0); the man pictured is not named |
| astronaut.png (512×512) | sheet 07 only | Full (no face crops: published test images stay whole) | about 0.33× | n/a | Sat 0.82 |
| grace_hopper.jpg (512×600) | sheet 08 only | Full | about 0.28× | n/a | Sat 0.82 |
| moon.png (512×512, gray) | sheet 09 only | Full | about 0.33× | n/a | B/W ramp (its low contrast is the point: "histogram equalization") |
| text.png (448×172, gray) | sheet 10 only | Full | 284×109 | n/a | B/W ramp |
| clock_motion.png (400×300, gray) | sheet 11 only | Full | about 0.57× | n/a | B/W ramp |
| hdri_warehouse.exr | S01 lighting | n/a | never visible | n/a | PMREM environment for coin reflections only, envMapIntensity 0.35 |
| earth-*.png/jpg, other HDRIs | **not used** | | | | Deliberate: no globe cliché, and they aren't test images, so the "11" stays exact |

**Pipeline sketch:**
1. Python prepares graded plates at exact display sizes (no browser rescaling) plus masks: the coin alpha and bump, the Hubble FG/BG split.
2. Three.js renders the S01 coin layer only (one disc, one shadow plane, PMREM 256). That is fine on SwiftShader at 8 sub-frames × 108 frames.
3. An HTML/Canvas compositor draws each frame (plates, develop shader, type, transforms; S08 draws cells from source images).
4. The GLSL post pass applies §4.5.
5. ffmpeg muxes with the synthesized WAV.

---

## 8. Risks, and how we avoid looking AI-made or cheap

| Risk | Mitigation |
|---|---|
| **Soft, low-res photos** | Every asset has a measured max scale (§7) and is shown at or below it. Softness reads as a print because grain is generated at final resolution, never upscaled with the image. B/W gets the most latitude. Big moments go to the only sharp large assets: Hubble (1.08×) and retina (0.52×). Thumbnails are always downscaled |
| **The meta idea reads as "they used free stock"** | Being specific makes it authorship: exact library calls, the docstring test-purpose for each image, the `from skimage import data` header, numbering 01–12, `not in any library`. The sheet appears after five chapters of carefully graded prints, not instead of them |
| **AI-look tells** (centred stacks, gradients, glow, particles, HUD, boxes, emoji, uniform timing) | Left text axis everywhere (only the eye is centred, on purpose). One accent colour, three uses. No glows or particles. Hairlines only for absence. Varied shot lengths (3.6–9.2 s), varied staggers, one deliberate violation (the 2-frame print-on). Optical indents. Real Chinese punctuation compression |
| **Font fallback** | LXGW WenKai is Latin-only here: forbidden for Chinese. No CJK in mono spans. Wait for `document.fonts.ready` per frame. Check one frame per shot for WenQuanYi glyphs |
| **Compression mush on XHS** | Ink is #0B0A09, not #000, with grain everywhere. Dither before 8-bit. CRF 16, `tune grain`. If dark areas blotch after a test upload, raise grain size, don't lower σ |
| **Reading speed in a slow film** | At most about 6 字/s. Every frame is complete when paused. Kicker 44 px or more, statements 52–148 px |
| **Attribution and content rules** | Every frame with his view carries a kicker: 纳德拉判断 / 他判断 / 而在他看来 / 据报道 / 他以前以为 / 他说 / 据他介绍 / 纳德拉认为. Our voice is only in Hei with ■ + `我们的解读`. Zero quotation marks. None of the three excluded lines appear (neocloud renting, "assume the model is compromised", "private evals define what good looks like"). Colophon states paraphrase, secondary reporting and our-reading ownership. No hype words (`残酷` is his "brutal") |
| **Factual claims we add** | "11 张都是代码库自带的公开示例图": verified pixel-identical for 10 against `skimage.data`, plus matplotlib `sample_data` per SOURCES.md. Test purposes are quoted from each docstring. "血管纹路因人而异，可用于身份识别" is a general biometric fact. We **don't** name coin types or mints, don't say "most used" or "benchmark leaderboard", and never caption the 3D coin as a photograph (it is `图 01 局部`, a detail of the real plate, and is only shown at rest after visible animation) |
| **Real people on the sheet** (Eileen Collins, Grace Hopper, the cameraman) | Shown whole, small, as the published test images they are, with neutral captions. No text near them, nothing implied |
| **Hard stop reads as a glitch** | The 2-frame print-on of `现在，他不这么想了。` and the D2 piano at +0.45 s make the stop authored. Grain and weave keep running, so the picture is alive but the camera has stopped |
| **SwiftShader cost** | 3D is used only for the hook coin. Everything else is 2D/Canvas/GLSL post |
| **Runtime creep with soundbites** | The slot rules in §2.2 keep the film at or under 60 s |
