# PUBLIC DOMAIN · 公有领域
### Editorial concept for F2 — 「微软CEO：大模型要打价格战了」
Swiss / Japanese editorial school: strict grid, vast negative space, the photograph as an artifact, typography to the half-point.

**Files that come with this pitch**

| What | Where |
|---|---|
| This spec | `video/f2/concepts/editorial.md` |
| Proof frames, 1:1 (static layout proofs, not the film) | `video/f2/concepts/editorial/proof/` (`film_f1…f11.png`, `carousel_c1…c7.png`) |
| Overview sheets | `proof/_film_sheet.jpg`, `proof/_carousel_sheet.jpg`, `proof/_cover_thumbnail_test.jpg` |
| Treatment tests | `proof/_focus_pull_test.png` (hook rack focus), `proof/_rake_sweep_test.png` (blind-emboss light sweep) |
| Reference code for every number in §7 | `video/f2/concepts/editorial/kit/prep.py` (reads only `assets/lib/`), `kit/proof.html`, `kit/render_proofs.mjs` |

Rebuild the proofs: `python3 -I f2/concepts/editorial/kit/prep.py && node f2/concepts/editorial/kit/render_proofs.mjs` (from `video/`).

---

## 1. The idea

### 1.1 Name and logline
**PUBLIC DOMAIN · 公有领域**

> Every photograph in this film is a free, standard test image that algorithms are routinely graded on. That makes it a public exam anyone can download. When models turn into cheap, interchangeable coins, the only plate nobody else can download is your own eval.

### 1.2 What we found
The ten small photos in `assets/lib/` are not stock photos. They are **pixel-identical** to scikit-image's bundled test images (`skimage.data.coins()`, `camera()`, `moon()`, `text()`, `clock()`, `coffee()`, `astronaut()`, `rocket()`, `retina()`, `hubble_deep_field()`). I checked this: the mean absolute difference is 0.0 for all ten. `grace_hopper.jpg` is matplotlib's sample image. The library docstrings even record what each picture is *for*: coins are a segmentation test, moon is for histogram equalisation, clock is for deconvolution, text is for corner detection, retina is for circular images.

In other words, the whole photo library is a **public benchmark**, which is exactly the subject of Nadella's third point.

### 1.3 The big idea
The film's material and its argument are the same thing.

- **Act I, Night (0–27 s): the market.** One ancient coin, a *token*, glows in a dark vitrine. The token gets copied 256 times until it is a grey commodity texture. One narrow slit in that texture shows the only expensive thing left, a rocket at dusk: the frontier niche. A beam of light hops from coin to coin like a router picking models (据报道，Copilot 每天都在混用多家模型).
- **The turn (21.6–27.2 s): the reveal.** The camera pulls back and the coins become one cell in a contact sheet of eleven numbered test images, each captioned with its function call and the skill it tests. Cell 12 is empty. On-screen: 片中的照片，全是开源软件自带的测试图。谁都能下载，谁都能拿它考算法。
- **Act II, Paper (27.2–59.2 s): what is private.** A hard cut inverts the world from darkroom to paper. Cell 12 is now a **blind emboss**, an empty plate pressed into the paper and visible only when a raking light passes over it. This is the private eval, Nadella's core IP. Then comes his changed mind, typeset as a proofreader's erratum, then zero-trust drawn with the film's own grammar (the model is the plate inside the frame; identity, record and permission sit outside it, in the margin). Then our reading, and the end, where the first coin shrinks into the brand's violet dot.

### 1.4 Why it reads as human-made: what a jury would notice
1. **The material is the argument.** Nobody gets the test-image twist from a prompt. It comes from looking at the files.
2. **Honest magnification.** Every plate's caption prints its true pixel size and display scale (`384 × 303 px · × 2.00`). The small resolution is declared, not hidden. The scale number updates live when the camera pushes.
3. **The coins were cut out with the test they were made for.** The coin mattes come from the watershed segmentation that `data.coins()` exists to exercise. (Credited in the kit, not on screen.)
4. **The score is measured from the photo.** Each coin rings at a pitch quantised from its own measured radius (bigger coin = lower note, D-major pentatonic). With that mapping fixed (largest coin = D5, 1.5 octaves), the hero coin (#16, the facing head) lands on the tonic, D6, by measurement rather than by choice. The router's light literally plays the tray.
5. **One accent colour with one meaning.** Violet `#5B2EFF`, the account's existing colour, appears only on *our reading* and on the brand dot. Everything reported about Nadella is ink or paper. The compliance rule becomes a visual system.
6. **Dramaturgy by inversion.** Dark (public, market) flips to paper (private, yours) on a bar line, after 0.4 s of silence.
7. **Blind emboss.** The single most "Japanese print" gesture: the most valuable object in the film has no image at all.
8. **The changed mind as an erratum.** A proofreader's strike-through with the classic deletion pigtail, drawn like a pen.
9. **Typographic finish.** Display commas are `halt`-compressed plus 0.12 em; there is no line-end punctuation in display lines; CJK/Latin spacing comes from `text-autospace`; figures are tabular; leading sits on a 4 px baseline with a 24 px rhythm; hairlines are 1.5 px.
10. **Bookend.** The coin from frame 1 becomes the violet dot of 「Coo-Coo出海Ai实验室」, with the same D6 ring.

### 1.5 Content compliance map
| On screen | Voice / colour | Brief point |
|---|---|---|
| 微软CEO纳德拉判断 / 大模型要打价格战了 | 他判断 (kicker), ink | 1 |
| token: 大模型API的计价单位 / 代币：代替钱流通的小圆片 | general fact (dictionary layout) | allowed general fact |
| 纳德拉判断：大多数企业的日常算力，终将变成大宗商品 | kicker, ink | 1 |
| 他判断：模型层，会有一场残酷的价格战 | kicker, ink | 1 |
| 他认为：最前沿的模型，只会服务少数顶尖场景 | kicker, ink | 1 |
| 据报道：微软Copilot内部，每天都在混用多家模型；便宜的闭源模型，和开源模型 | kicker 据报道, ink | 2 |
| 片中的照片，全是开源软件自带的测试图 / 谁都能下载，谁都能拿它考算法 | film's own factual voice (no attribution needed, true by §1.2) | — |
| 纳德拉认为：每家公司都会有自己的私有评测集，这会是它的核心IP | kicker, ink | 3 |
| ● 我们的理解：公开的考题，谁都能刷分；你的考题，只有你有 | **violet**, labelled | our reading |
| 被问到改变过什么看法，他说：以前以为……对齐就会自然出现（struck）/ 现在，他不这么想了 | kicker 他说, ink, no quotation marks | 4 |
| 他说：微软不等对齐问题解决，先给模型套上零信任架构；身份 / 记录 / 权限 | kicker, ink | 4 |
| ● 我们的解读：三件事 + 以上是我们的理解，不是纳德拉原话 | **violet**, labelled twice | our reading |
| Source line, photo credits, account mark | end card | required |

Nothing from the earnings call, the X post or the essay is used. No Chinese paraphrase sits inside quotation marks. No hype words appear (残酷 is his "brutal", attributed).

---

## 2. Film storyboard (1080×1920, 30 fps, 59.2 s = 1776 frames)

**Clock.** Music at 75 BPM: 1 beat = 0.8 s = **24 frames**, 1 bar = 3.2 s = 96 f. Every cut and every major event lands on the 24-frame grid; annotations land on beats; hops land on eighth notes (12 f).
**Global anchors (film):** running head (RH) top y 196; kicker (K) top y 288; display (D) top y 360; margins x 72 / 1008; essential text inside y 200–1480.
**Easing tokens** (defined in §5.2): `set` (.2,.7,.1,1), `out` (.4,0,1,1), `glide` (.65,0,.35,1), `drift` (.37,0,.63,1), `focus` (.33,0,.15,1), `snap` (.7,0,.2,1), `hop` (.5,0,.2,1), `draw` (.45,0,.2,1).
**Type tokens** (defined in §4.3): D1 144/168, D2 96/120, D3 72/96, D4 64/88, D5 52/76 (Noto Serif SC 600, −0.01 em); B1 48/72 and B2 44/60 (Noto Serif SC 500); K 44/48 (Noto Sans SC 500, +0.02 em); F 28/36 and C 22/30 (Noto Sans SC 400, +0.02 em); M 20/30 (Geist Mono 400, +0.02 em, tabular).
Colours: n1 `#E9E4DA`, n2 `#A39D92`, n3 `#6F6A62` on night `#0D0C0B`; ink `#171513`, p2 `#5F5B55`, p3 `#8C877F` on paper `#EFEBE3`; violet `#5B2EFF`.

| # | In–out (s) / frames | What we see (asset, crop, treatment) | Camera / motion | On-screen copy (final) — font · size · weight · tracking · position | Transition out | Sound |
|---|---|---|---|---|---|---|
| **1 HOOK** 一枚硬币 | 0.00–3.20<br>f0–96 | `coins.png` resampled ×2.40 → 922×727 at (234,653), so coin 16 (facing head, src centre 212.4,193.1) sits on **(744,1116)**. *Dissolve mode*: cloth pulled into night through the watershed matte; key light on coin 16 only (flat to 0.85 r, gaussian falloff σ 1.035 r), fill 0.10; selenium tone; radial edge mask (ellipse 62%×58% at 55%/63%, opaque to 55%). No frame, no caption. | f0–27 rack focus: disc (lens) blur r 16→0 px, `focus`, with focus breathing scale 2.46→2.40 anchored on coin 16. f27–96 push 2.40→2.47, `drift`. f12–20 glint: 18 px specular band at 30° crosses coin 16 (additive +0.35, `#F4EEDC`, inside the coin matte). | K「微软CEO纳德拉判断」Sans 500 44/48 +.02em n2 at (72,288), **visible from frame 0**.<br>D1「大模型」/「要打价格战了」Serif 600 144/168 −.01em n1 at (68,360). Glyph set-in from f3 (line 1) and f15 (line 2), 40 ms stagger, 11 f per glyph. **Fully legible at 1.10 s.** | Continuous. f88–96 K + D1 fade 8 f `out`. | f0 night room tone + D/A drone, 1.2 s fade-in. f9 sub thump 52→38 Hz. **f12 coin-16 strike, D6 1174.7 Hz**, RT60 2.4 s. |
| **2 TOKEN** | 3.20–6.40<br>f96–192 | Same plate, same light; the key pool tightens σ 1.035 r→0.80 r (f96–120, `glide`) so the cloth around the coin sinks. | Push continues 2.47→2.52, `drift`, anchored on coin 16. | RH appears (f96, 8 f): left「纳德拉 × 20VC」C 22/30 + `2026.10.26` M 20/30, n2, at (72,196); right「01 价格战」.<br>「token」Instrument Serif *Italic* 200/200 n1 at (62,268), whole word, opacity + y 12→0, 16 f `set`, f100.<br>`/ˈtəʊkən/  n.` M 24/30 n2 at (72,476), types on at 24 ms/char from f112.<br>「1」M 24 n3 at (72,540) +「大模型API的计价单位」B1 48/72 n1 at (112,540), f118.<br>「2」at (72,612) +「代币：代替钱流通的小圆片」B1 at (112,612), f130. Body glyph stagger 20 ms. | Continuous. f184–192 all copy except RH fades 8 f `out`. | f100 felt-piano D3 (146.8 Hz). Type ticks −44 dBFS. |
| **3 COMMODITY** step-and-repeat | 6.40–12.80<br>f192–384 | *House lights up*: hook plate cross-fades to the full-exposure plate (cloth back to graded tone, plate edges appear). Plate rect **(72,696) 766×606** (×2.00). Then the plate **divides**: f216 → 2×2 (tiles 381×301, gutter 4), f240 → 4×4 (190×150, g 2), f264 → 8×8 (94×74, g 2), f288 → 16×16 (46×36, g 2). The block stays 766×606 throughout. Gutters are night. | f192–216 rostrum from coin-anchored ×2.52 to the plate rect, 24 f `glide`. Each split: every tile becomes four children that start stacked on the parent rect, scale to 0.5 and slide to their quadrants, 10 f `snap`, 180° motion blur. f288–384 field push 1.000→1.015 about (455,999), `drift`. | K「纳德拉判断」(72,288) f196.<br>D3「大多数企业的日常算力」/「终将变成大宗商品」Serif 600 72/96 n1 at (68,360), f200; exits f280–288.<br>f288 K →「他判断」; D3「模型层，会有一场」/「残酷的价格战」f292.<br>Counter M 20/30 n2 at (862,1242) (its last line sits on the field's bottom edge, y 1302): `× 4` f216, `× 16` f240, `× 64` f264, `× 256` f288 (hard swaps), line 2 `= 6,144 枚` types f300. | Continuous. f376–384 copy fades `out`. | f192 drone low-pass opens 600→2400 Hz over 0.8 s. **Coin clusters** at each split: 4 / 16 / 64 / 256 micro-strikes over 40 / 80 / 160 / 320 ms; the last is a full coin pour. f292 felt-piano A2. |
| **4 NICHE** the slit | 12.80–16.00<br>f384–480 | Field dims to 42% (f384–392). Tile columns 5–10 (field-local x 240–526) fade to night (f388–394). A **slit 286×606** opens at screen x 312–598, y 696–1302: `rocket.jpg` crop (250,120)–(393,423) ×2.00, Vitrine CDL, halation on the pad lights. The slit edges sit exactly on tile gutters. | Slit mask width 0→286 centred on x 455, 27 f `snap`. f419–472 push inside the slit ×2.00→×2.06 about the slit centre, `drift`. f472–480 slit closes 8 f `out`; tiles return 4 f; field un-dims. | K「他认为」(72,288) f388.<br>D3「最前沿的模型」/「只会服务少数顶尖场景」(68,360) f396.<br>No caption (labels are held back until the reveal). | Continuous. f464–472 copy fades. | f392 slit swell (band-pass noise 300→1800 Hz, 0.9 s, −28 dBFS) + E1 41.2 Hz rumble 2.4 s. f400 dusk shimmer (2637/3136/3951 Hz, −44 dBFS). |
| **5 MIX** the router's light | 16.00–21.60<br>f480–648 | 256 tiles **collapse into one plate** (all glide to (72,696) 766×606; identical images converge exactly). House lights down (fill 0.10, f496–504). One key light hops coin to coin on eighth notes: f504, 516, … 636 → coins **06, 21, 03, 14, 10, 02, 13, 24, 22, 11, 21, 18** (src centres in Appendix A). The last coin (18, the big helmeted Athena) holds to f648. | Collapse 16 f `glide` with motion blur. Each hop: light travels 4 f `hop`, holds 8 f; the coin just left keeps an afterglow 0.45→0.10 over 10 f (linear). Light radius follows each coin's measured r. | RH right →「02 混用」(hard swap f480).<br>K「据报道」(72,288) f484.<br>D4「微软Copilot内部」/「每天都在混用多家模型」Serif 600 64/88 n1 at (68,360), f488.<br>B2「便宜的闭源模型，和开源模型」Serif 500 44/60 n2 at (72,560), f540. | Continuous. f640–648 copy fades. | f480 reverse coin pour (the 256-cluster reversed, 0.5 s): *the coins gather*. Hops ring each coin's own pitch: **F♯5 A5 D6 E6 F♯6 A6 F♯6 E6 D6 B5 A5 D5**, −20 dBFS, panned by coin x. f480 felt-piano D3, f576 A2. |
| **6 REVEAL** the contact sheet | 21.60–27.20<br>f648–816 | Pull back: the plate becomes **cell 01** of a 4×3 contact sheet (cells 216×162, x = 72 + 240·col, y = 640 + 270·row; thumbnails fit-contain, bottom-left aligned): 01 coins, 02 rocket, 03 coffee, 04 camera, 05 astronaut, 06 moon, 07 text, 08 clock, 09 hubble, 10 retina, 11 grace_hopper, **12 empty** (1.5 px hairline, n-hair). Lights up to full (f648–664). | Rostrum: (72,696,766×606) → (72,640,205×162), 48 f `glide`, motion blur. Cells 02–11 appear in reading order, 3 f stagger, 8 f opacity each (no movement). f714–730 cell-12 hairline draws clockwise, 16 f `draw`. | RH right「03 测试图」(f648).<br>D4「片中的照片，全是」/「开源软件自带的测试图」(68,360) f696.<br>B2「谁都能下载，谁都能拿它考算法」n2 at (72,552), f736.<br>Cell captions, from f714 (3 f stagger, 12 ms/char): line 1 M 18/28 n2「01␣␣coins()」(index at 60% opacity) at (x, y+174); line 2 C 20/28 n3 test purpose at (x, y+202): 分割 / 示例图 / 椭圆 · 纹理 / 分割 · 去噪 / 彩色图 / 直方图均衡 / 角点检测 / 去模糊 / 多尺度检测 / 圆形图像 / matplotlib. Cell 12 shows only「12」.<br>C 22/30 n3 at (72,1428): 「前10张来自scikit-image（skimage.data），1张来自matplotlib」 f760. | **Hard cut to paper on the bar line, f816.** f804–816 picture holds; sound is silent. | f648 *breath* (pink noise, low-pass sweep 500→3000 Hz, 1.6 s, −32 dBFS). f684–714 paper ticks per cell (−36 dBFS). f792–804 reverse-reverb swell of D6. **f804–816 silence.** |
| **7 THE PRESS** private eval | 27.20–36.00<br>f816–1080 | Paper `#EFEBE3` + procedural paper (§4.8). The contact sheet stays in place as **ghost prints**: thumbnails at 14% opacity, multiply; captions at 30%. **Cell 12 is now a blind emboss** (deboss depth 1.0, bevel 7 px, SDF), revealed by a raking light. Then the push lands on **plate 12 at (72,672) 696×522** (9 columns, 4:3). | f822–870 raking light: azimuth 215°→135° (linear), elevation 10°→24° (`glide`); then rests. f870–918 rostrum into cell 12: (792,1180,216×162) → (72,672,696×522), ×3.222, 48 f `glide`. The emboss is evaluated per frame in screen space, so it is crisp at every scale; the ghost cells leave frame with the paper plane. | RH right「03 评测集」(p2).<br>K「纳德拉认为」p2 (72,288) f900.<br>D4「每家公司，都会有」/「自己的私有评测集」/「这会是它的核心IP」ink (68,360), f906, lines 4 f apart.<br>Plate caption at (792,672): C 22「图版 12」p2 + M 20/30 p3 `your_eval()` /「未公开」/「尺寸：只有你知道」, types f972.<br>f996: K violet「● 我们的理解」(14 px dot) at (72,1242); D5 violet「公开的考题，谁都能刷分」/「你的考题，只有你有」at (70,1306). | Hard cut f1080. (Rule: on hard cuts, copy cuts with the picture and never fades.) | f816 paper-air room tone; felt-piano chord D3 A3 E4 F♯4 (−18 dBFS), *the page*. **f822 the press**: felt-hammer thud 80 Hz + paper crunch. f996 felt-piano A4 → D5. |
| **8 ERRATUM** changed mind | 36.00–41.60<br>f1080–1248 | Paper. `text.png` (handwritten formulae, shallow focus) resampled to **696×267 (9 columns, ×1.55)**, paper selenium ramp, at (72,360). | Plate fades in 8 f; push ×1.55→×1.58 about plate centre, `drift`. Strike 1: f1140–1156; strike 2: f1152–1168; pigtail f1168–1176. Each is a 2.5 px ink line through the glyph centre, drawn left→right, `draw`. | RH right「04 改口」.<br>K「被问到改变过什么看法，他说」p2 (72,288) f1080.<br>M 20 p3 at (72,651): `图版 07 · text() · 448 × 172 px · × 1.55` f1092.<br>Serif **500** 64/88 p2 at (72,732):「以前以为：模型规模够大」/「对齐就会自然出现」f1104, then struck.<br>D2「现在，他不这么想了」Serif 600 96/120 ink at (68,944), f1176. | Hard cut f1248. | f1140 / f1152 pen strokes (band-pass noise 2.5–7 kHz, velocity-shaped, −30 dBFS); f1168 flick. **f1176 harmonic shift**: felt-piano G2+B2, pad moves to G. |
| **9 ZERO-TRUST** policy outside the model | 41.60–48.80<br>f1248–1464 | Paper. `retina.jpg` → **488×488 (×0.35)**, fundus black surround kept, Vitrine CDL (paper variant), at (96,648). **Frame** = 1.5 px p-hair square (72,624)–(608,1160), 24 px outside the image (7 columns). Leaders 608→688 at each label's centre. Annotations in the margin column x 712–1008. | Image fade 12 f (f1260). Frame draws clockwise 16 f (f1272, 4 f per side, `draw`). Push ×0.346→×0.356 inside the image rect, `drift`. Annotations on beats f1296 / f1344 / f1392: leader 6 f `draw` → label set → body set. | RH right「04 零信任」.<br>K「他说」(72,288) f1248.<br>D4「微软不等对齐问题解决」/「先给模型套上零信任架构」ink (68,360) f1252.<br>Labels K ink at (712, 624 / 812 / 1000): 身份 / 记录 / 权限. Bodies B2 **44/56** p2 at (712, y+56):「每个Agent」/「都有身份」·「每次调用」/「都留痕」·「规则放在」/「模型之外」.<br>M 20 p2 at (72,1184): `图版 10 · retina() · 1411 × 1411 px · × 0.35` + C 22 p3 at (72,1216):「视网膜的血管分布因人而异，常被用作身份识别」 f1416. | Hard cut f1464. | f1272 frame whisper (high noise, 0.5 s, −40 dBFS). **Registry stamps** at f1300 / f1348 / f1396 (wood-block modal click). Pad G → D. |
| **10 OUR READING** | 48.80–55.20<br>f1464–1656 | Paper. Four rules (1.5 px p-hair, 936 wide) at y 520 / 752 / 984 / 1216. Index thumbnails 96×72 at (912, y+36): the 16×16 coin field, the blind emboss, the retina. | Rules draw left→right 16 f each, 4 f stagger, from f1484. Items on beats f1488 / f1536 / f1584: numeral set 11 f, text glyph stagger 20 ms, thumbnail fade 8 f. | RH right「05 我们的解读」.<br>K violet「● 我们的解读」(72,288) f1464; D4 ink「给出海创业者的三件事」(68,360) f1468.<br>Numerals Instrument Serif roman 120/120 **violet** at (70, y+20); text B1 48/68 ink at (192, y+32):<br>1「架构上支持多模型路由」/「别绑死一家」<br>2「建一套自己的」/「私有评测集」<br>3「Agent的身份、日志、权限」/「放在模型之外」<br>F 28/36 p2 at (72,1240):「以上是我们的理解，不是纳德拉原话」 f1608. | Hard cut f1656. | Felt-piano F♯4, A4, D5 on the three items (rising, resolving). Pad D add9. |
| **11 END** coin → dot | 55.20–59.20<br>f1656–1776 | Paper; no RH. Coin 16 matte (selenium-toned, ×2.00, disc ⌀ 94 px) appears with its left edge on x 72, centre y 1166. It then **shrinks to the 16 px brand dot** in place and turns violet. | Coin fade-in 8 f (f1668). f1692–1708 scale 94→16 px anchored at left-centre, 16 f `glide`; photo→flat `#5B2EFF` cross-fade over the last 8 f. No particles, no glow. | D3「你的产品，现在」/「接了几家模型？」ink (68,360) f1656. B2「评论区聊聊」p2 (72,576) f1676.<br>Brand: dot + 「Coo-Coo出海Ai实验室」Noto Sans SC **700** 48/56 +.01em ink, block at (72,1140); name sets f1708 (16 f).<br>Source C 22/32 p2 at (72,1236), types from f1716 at 4 chars/frame:<br>「来源：20VC 播客（主持 Harry Stebbings），嘉宾 Satya Nadella（微软CEO）」<br>「2026.10.26 发布。文中观点据公开报道整理，均为转述，非逐字引用」<br>「图片：scikit-image 与 matplotlib 自带的测试图」<br>「Brooklyn Museum · SpaceX · NASA · Rachel Michetti · Lav Varshney」<br>「Stefan van der Walt · Wikimedia Commons · U.S. Navy」 | End f1776 (loops to the hook; its D6 ring rhymes with this one). | **f1680 coin-16 strike D6** (bookend), RT60 2.4 s. f1708 felt-piano D3+A3. Room tone fades f1740–1776. |

### 2.1 Notes the table cannot hold
- **Hook, frame 0.** The first frame already shows the kicker and a bokeh of coins with one bright disc. The headline is complete at 1.10 s. The cover (carousel frame 1) is the post cover, so frame 0 never has to work as the thumbnail.
- **Cinema mode → catalogue mode.** Shots 1–5 carry **no** function names, plate numbers or captions (only the neutral counter in shot 3). Labels appear first in shot 6, which is what makes the reveal land.
- **Continuity.** Shots 1–6 are one continuous rostrum take on one plate (no cuts). The plate rect (72,696,766×606) is shared by shots 3, 4 and 5, so changes read as the light or the subdivision changing, never as edits.
- **Afterglow.** In shot 5 the router light remembers its last call for 10 frames, like phosphor. That is the only "trail" effect in the film.
- **Running head.** Present from 3.2 s to 55.2 s. Section names change by hard swap on cuts or bar lines: 01 价格战 → 02 混用 → 03 测试图 → 03 评测集 → 04 改口 → 04 零信任 → 05 我们的解读.
- **Safe area.** All essential copy sits inside y 288–1480 and x 68–1008. Nothing but grain lives below y 1480.

### 2.2 Optional Nadella soundbite slots (the film is complete without them)
| Slot | Insert at | Length | Design |
|---|---|---|---|
| **A** (price war) | f384 (12.80 s), between shots 3 and 4 | 8–12 beats (6.4–9.6 s); trim the clip to a whole number of beats | Night. RH「01 价格战」. K「他在节目里说」(72,288). Clip as a 16:9 plate **936×527 at (72,696)** (12 columns), no border, Vitrine CDL plus film grain so it matches. Subtitles B1 48/72 n1 at (72,1247), at most 2 lines of 18 字. M 20 n3 at (72,1428): `20VC · 2026.10.26 · 原片 mm:ss` +「字幕为意译」. |
| **B** (alignment) | f1080 (36.00 s), between shots 7 and 8 | same | Paper. Same plate geometry at (72,600). Subtitles ink. A 1.5 px p-hair frame 24 px outside the clip (the clip is also "a model", so it sits inside a frame). |

Audio for both slots: dialogue normalised to −18 LUFS. Music ducks −8 dB with 300 ms ramps. Room tone continues. Cut in and out on beats. Everything after a slot shifts by the slot length, and the beat grid is preserved.

---

## 3. Carousel: 7 frames, 1080×1440 (3:4)
**Shared furniture.** Margins 72. RH top y 96 (same style as the film; right side「0N / 07」+ section). Footer at (72,1356): 10 px violet dot + 「Coo-Coo出海Ai实验室」 Noto Sans SC 500 24/30, n2 or p2. Frames 1–4 are night and 5–7 are paper, so the swipe from 4 to 5 *is* the inversion. All Chinese body ≥ 44 px. Kicker top 168; display top 236.

| # | Layout (coordinates in px) | Copy (final) | Asset / treatment |
|---|---|---|---|
| **1 COVER** (also the video cover) | K (72,168) Sans 500 **48/56** n2. D1′ (68,244) Serif 600 **148/172** n1, 2 lines → bottom y 588. Plate at (234,537), coin 16 on (744,1000), same radial mask as the film. Footer left: brand; right (aligned to x 1008):「4个判断 · 3点解读 →」C 24/30 n2. | 微软CEO纳德拉判断 / 大模型 / 要打价格战了 | `coins.png` ×2.40 dissolve mode, coin 16 lit (= film frame ~f40, sharp). |
| **2 价格战** | K (72,168). D4 (68,236) 2 lines. B2 44/64 n2 (72,436) 2 lines. Field + slit 766×606 at (72,600). M 20 n3 (72,1230). | 纳德拉判断 / 大多数企业的日常算力 / 终将变成大宗商品 / 模型层会有一场残酷的价格战 / 最前沿的模型，只会服务少数顶尖场景 / `同一张照片 × 256　= 6,144 枚` | 16×16 field at 42% with the rocket slit (crop as film shot 4). |
| **3 混用** | K (72,168). D4 (68,236). B2 (72,436). Plate 766×606 at (72,552). F 28/36 n2 (72,1182). | 据报道 / 微软Copilot内部 / 每天都在混用多家模型 / 便宜的闭源模型，和开源模型 / 示意：每一束光，是一次调用 | Multiple exposure of the last five hops: coin 24 (22%) → 22 (36%) → 11 (55%) → 21 (78%) → 18 (100%), fill 0.10. This is the still-image equivalent of the moving light. |
| **4 测试图** (the reveal) | K (72,168). D4 (68,236). B2 44/60 (72,424). Contact sheet top **512** (rows 512 / 782 / 1052), same cells and captions as the film. Cell 12 empty, index「12」only. | 关于这组照片 / 前面的照片，全是 / 开源软件自带的测试图 / 谁都能下载，谁都能拿它考算法 | 11 thumbnails, grades as §7. |
| **5 评测集** | Paper. K (72,168). D4 (68,236) 3 lines. **Blind-emboss plate 12 (72,548)–(688,1010)** (8 columns). Caption column (712,548). Violet K (72,1058); violet D5 (70,1122) 2 lines. | 纳德拉认为 / 每家公司，都会有 / 自己的私有评测集 / 这会是它的核心IP / 图版 12 · `your_eval()` · 未公开 · 尺寸：只有你知道 / ● 我们的理解 / 公开的考题，谁都能刷分 / 你的考题，只有你有 | Static emboss at azimuth 135°, elevation 24° (a still needs a single light that reads well). |
| **6 零信任** | Paper. K (72,168). Struck lines Serif 500 52/72 p2 (72,236) + pigtail. D3 72/96 ink (68,404). B2 44/64 ink (72,520) 2 lines. Frame (72,680)–(608,1216), retina 488 at (96,704). Leaders 608→688. Labels K at (712, 704 / 888 / 1072); bodies B2 44/56 p2 at y+56. M 20 p3 (72,1240). | 被问到改变过什么看法，他说 / ~~以前以为：模型规模够大 / 对齐就会自然出现~~ / 现在，他不这么想了 / 微软不等对齐问题解决，/ 先给模型套上零信任架构：/ 身份 每个Agent 都有身份 / 记录 每次调用 都留痕 / 权限 规则放在 模型之外 / `图版 10 · retina() · 1411 × 1411 px · × 0.35` | Retina as film shot 9. |
| **7 我们的解读 + end** | Paper. Violet K (72,168). D4 (68,236). Rules y 364 / 540 / 716 / 892. Numerals Instrument Serif 96/96 violet (70, y+22). Items B 44/60 ink (160, y+30). Thumbnails 96×72 (912, y+32). F 28/36 p2 (72,912). D5 52/72 ink (68,1000). B2 44/60 p2 (72,1076). Sources C 20/30 p3 (72,1164), 4 lines. Brand (72,1340): 12 px dot + Noto Sans SC 700 36/44. | ● 我们的解读 / 给出海创业者的三件事 / 1 架构上支持多模型路由，别绑死一家 / 2 建一套自己的私有评测集 / 3 Agent的身份、日志、权限，放在模型之外 / 以上是我们的理解，不是纳德拉原话 / 你的产品，现在接了几家模型？/ 评论区聊聊 / sources / Coo-Coo出海Ai实验室 | Index thumbnails as film shot 10. |

**How frame 1 reads as a thumbnail** (tested at 360×480 and 180×240, see `proof/_cover_thumbnail_test.jpg`):
- A near-black tile stands out in a mostly light feed.
- The two-line serif headline stays legible at 180 px wide (about 25 px per line).
- One bright disc, the coin, gives the eye a single focal point.
- The thumbnail has no clutter: one kicker, one headline, one object.

Order of reading: 价格战 → coin → (curiosity) "why a coin?". The answer comes in frames 2–4.

---

## 4. Design system

### 4.1 Grid
- **Canvas.** Film 1080×1920; carousel 1080×1440.
- **Columns.** 12 columns × 56 px, gutter 24, margins 72. Column *n* starts at x = 72 + 80(n−1); the measure is 936.
- **Plates snap to columns.** Contact sheet: 4 cells × 3 columns (216). Plate 12: 9 columns (696). Retina frame: 7 columns (536). Text plate: 9 columns (696).
- **One declared exception.** The coins plate and field are **766** wide (= 384 × 2.00 − 2), because the honest ×2.00 scale wins over the grid. Its caption column starts one gutter after it (x 862).
- **Vertical rhythm.** 4 px unit and 24 px major rhythm. Display and body leadings are multiples of 4 (168, 120, 96, 88, 76, 72, 60, 56, 48). Micro captions use 30, half of the 60 px B2 leading, so two caption lines equal one body line. Free-standing blocks sit on the 4 px unit, and key anchors on the 24 px rhythm (288, 360, 624, 672, 696). Anything placed relative to a photograph is measured from that plate's edge (24 px gaps). Photographs keep their true aspect ratio, so their heights (606, 522, 267) are not forced onto the unit.
- **Film anchors.** RH 196, K 288, D 360, plate tops 624–696, essential bottom 1480. Carousel anchors: RH 96, K 168, D 236, footer 1356.

### 4.2 Typefaces (four families, fixed roles)
| Role | Face | Weights used |
|---|---|---|
| Chinese display and body | **Noto Serif SC** (Mincho-like; editorial, calm) | 600 display, 500 body |
| Chinese labels, kickers, captions, brand | **Noto Sans SC** | 400 captions, 500 kickers, 700 brand only |
| Latin display (the word *token*; list numerals) | **Instrument Serif** | 400 italic, 400 roman |
| Technical captions (function names, px, scale, dates, counters) | **Geist Mono** | 400 only, tabular figures |

Not used: Anton, ZCOOL, LXGW (too casual), Inter/Geist Sans (one sans is enough), Fraunces/Garamonds (one Latin serif is enough).

### 4.3 Type scale (px, on the 1080 canvas)
| Token | Face / weight | Size / leading | Tracking | Use |
|---|---|---|---|---|
| D1 | Serif SC 600 | 144/168 (cover 148/172) | −0.01 em | hook headline |
| D2 | Serif SC 600 | 96/120 | −0.01 em | 现在，他不这么想了 |
| D3 | Serif SC 600 | 72/96 | −0.01 em | price-war statements, end question |
| D4 | Serif SC 600 | 64/88 | −0.01 em | statements |
| D5 | Serif SC 600 | 52/76 | −0.01 em | our reading on plate 12; carousel question |
| B1 | Serif SC 500 | 48/72 (list items 48/68) | 0 | definitions, list items, subtitles |
| B2 | Serif SC 500 | 44/60 (annotations 44/56) | 0 | secondary statements, annotations (**floor for essential copy**) |
| K | Sans SC 500 | 44/48 (cover 48/56) | +0.02 em | attribution kickers, labels |
| F | Sans SC 400 | 28/36 | +0.02 em | footnotes (示意…, 以上是我们的理解…) |
| C | Sans SC 400 | 22/30 (sources 22/32; carousel 20/30) | +0.02 em | running head, plate notes, sources |
| M | Geist Mono 400 | 20/30 (sheet 18/28; IPA 24/30) | +0.02 em | technical captions |
| L1 | Instrument Serif Italic | 200/200 | 0 | *token* |
| L2 | Instrument Serif Roman | 120/120 (carousel 96) | 0 | 1 2 3 |
| Brand | Sans SC 700 | 48/56 (end), 36/44 (carousel 7), 24/30 500 (footers) | +0.01 em | Coo-Coo出海Ai实验室 |

### 4.4 Typographic rules
1. **Display punctuation** (≥ 52 px). 「，：；、」 use `font-feature-settings:"halt" 1` plus `margin-right:.12em`. This is verified with the fontsource build: 「现在，他不这么想了」 narrows from 864 to 816 px with `halt`, and the 0.12 em gives back air. Body sizes keep full-width punctuation.
2. **No line-end punctuation in display lines** (no 「，」「。」 at line ends). Exception: 「？」, because it carries meaning.
3. **CJK–Latin spacing.** Use `text-autospace: normal` (supported in the renderer). Source copy has **no** manual spaces between Chinese and Latin. Inline Latin (Copilot, IP, API, Agent) uses Noto Serif SC's own Latin at the same weight, never tracked caps.
4. **Line breaks are set by hand** (`<br>`), never by the browser. Breaks fall at phrase boundaries; a line never starts with punctuation; a Latin word never splits.
5. **Figures.** Geist Mono tabular. The multiplication sign is U+00D7 with thin spaces (`384 × 303 px`, `× 2.00`). Scales always print 2 decimals.
6. **Optical alignment.** Display lines sit at x 68 (4 px left of the 72 margin) so Serif SC glyph side bearings align with the kicker's stems at 72. Instrument Serif numerals sit at x 70.
7. **Strike-through.** 2.5 px ink at the glyph centre (line-box centre + 0.02 em), overhanging 4 px each side. The last struck line ends in a proofreader's deletion pigtail (SVG path in `kit/proof.html`).

### 4.5 Colour tokens
| Token | Hex | Use | Contrast (measured) |
|---|---|---|---|
| night | `#0D0C0B` | Act I ground (warm black, never `#000`) | — |
| paper | `#EFEBE3` | Act II ground (warm, never `#FFF`) | — |
| ink | `#171513` | primary type on paper | 15.32:1 on paper |
| n1 | `#E9E4DA` | primary type on night | 15.42:1 on night |
| n2 | `#A39D92` | kickers and secondary on night | 7.25:1 |
| n3 | `#6F6A62` | micro captions on night (non-essential only) | 3.64:1 |
| p2 | `#5F5B55` | kickers and secondary on paper | 5.67:1 |
| p3 | `#8C877F` | micro captions on paper (non-essential only) | 3.00:1 |
| **violet** | `#5B2EFF` | **our reading + brand dot only** (account colour) | 5.39:1 on paper |
| violet-n | `#9A84FF` | reserved: our reading if it ever falls on night | 6.62:1 on night |
| hair-n | `rgba(233,228,218,.30)` | hairlines on night | — |
| hair-p | `rgba(23,21,19,.32)` | hairlines on paper | — |
| halation | `#FF5A36` | halation tint (night only) | — |

There are no gradients anywhere, except the physical light falloff on the coins and the vignette.

### 4.6 Grade (the "LUTs")
- **Vitrine** (colour plates) is an ASC-CDL in sRGB code values.
  - slope (0.96, 0.95, 0.92), offset (0.045, 0.040, 0.035), power (1.05, 1.04, 1.02), then Rec.709 saturation 0.82.
  - In lift/gamma/gain terms: lift raises blacks to about RGB (10, 9, 8), sitting just under night, so plates never punch a digital-black hole. Gamma is slightly denser (≈1.04). Gain caps highlights at a cream about (245, 242, 231), never pure white. Saturation is 0.82.
  - Split-tone falls out of the channel offsets: warm shadows (R lifted most), cream highlights (B gained least). There is no teal/orange.
  - **Paper variant** (retina): offset (0.05, 0.045, 0.04), saturation 0.90, so the warm reds survive on paper.
- **Selenium** (grey plates) is a piecewise-linear ramp: L 0 → `#0E0D0C`, L 0.5 → `#78736B`, L 1 → `#ECE6DA`. It reads as a toned silver print. **Paper variant**: `#282623` / `#8C877F` / `#E2DDD3`, a lighter print that sits in the paper.
- **Coins cloth toe** (outside the segmentation matte only): cloth = ((g − 0.10)/0.90)^1.6 × 0.55.

### 4.7 Film texture (final pass over the composited frame, everything included)
| Parameter | Night (Act I) | Paper (Act II) |
|---|---|---|
| Grain | monochrome gaussian, white noise blurred σ 0.65 px, amplitude ±2.6/255 × w(L), where w(L) = 0.35 + 0.65·4L(1−L); new seed every frame | ±2.0/255, same weighting |
| Halation | threshold L > 0.80, gaussian σ 14 px, tint `#FF5A36`, screen 10% | none |
| Vignette | multiply 1 − 0.12·smoothstep(0.55, 1.15, d), d = distance from (540,900) / 960 | 0.04, same curve |
| Motion blur | 180° shutter: 5 sub-frames over the first half of the frame interval, averaged in linear light, only on frames where something moves > 8 px/frame (splits, collapse, pull-back, slit, push into plate 12, coin→dot) | same |

**Never added:** chromatic aberration, gate weave, light leaks, lens flares, bloom (beyond halation), letterbox bars, scan lines, HUD, film burn, dust.

### 4.8 Paper and blind emboss
- **Paper.** `#EFEBE3` × (1 + 0.008·low + 0.0035·fibre).
  - low = gaussian noise, σ 48 px, unit variance.
  - fibre = anisotropic noise (σ 0.6×5.0 px and 5.0×0.6 px blend, 0.6/0.4), unit variance.
  - The texture is static (paper does not boil); the grain on top is dynamic.
- **Blind emboss.**
  - Height field: h = −depth·smoothstep(bevel) of the rectangle's signed distance, plus 0.0025·fibre·(1 − 0.6·inside). Fibres are flattened inside the deboss, as real pressed paper is.
  - Normal from the gradient × 2.2. Lambert term normalised by L.z, clamped to [0.86, 1.06], output capped at 0.97 (no clipped whites).
  - Rest light: azimuth 135° (from top-left), elevation 24°.
  - Defaults: depth 1.0, bevel 7 px. Index thumbnail: elevation 14°, depth 1.6, bevel 5.
  - Implement as a fragment shader on the screen-space rectangle, so it stays crisp during the ×3.22 push. `kit/prep.py::emboss()` is the reference.

### 4.9 Micro-detail system
| Element | Spec | Appears |
|---|---|---|
| Running head | left: C「纳德拉 × 20VC」+ 16 px + M `2026.10.26`; right-aligned to 1008: M section number + 12 px + C section name; n2/p2 | shots 2–10, carousel 1–7 |
| Kicker (attribution) | K, n2/p2; violet with a 14 px dot only for our reading | every claim |
| Plate caption | line 1 M:「图版 NN · fn() · W × H px · × S.SS」(c2); line 2 C: one factual note (c3). The scale value updates live during pushes. | shot 6 onward (catalogue mode) |
| Sheet caption | M 18/28 `NN␣␣fn()` (NN at 60% opacity) + C 20/28 test purpose in c3 | contact sheet |
| Counter | M 20/30 tabular, hard swaps (no rolling digits) | shot 3 |
| Hairline | 1.5 px hair-n/hair-p. **Hairlines only ever mean a boundary, slot or rule**: empty cell, policy frame, leaders, list rules. Never decoration. | 6, 9, 10 |
| Strike + pigtail | §4.4.7 | 8, carousel 6 |
| Brand dot | 14 px (16 at the end) `#5B2EFF` disc, vertically centred on the CJK x-height | end, footers |
| Folio | carousel only, in the RH: `0N / 07` | carousel |

---

## 5. Motion language

### 5.1 Clock
30 fps. A beat is 24 frames; a bar is 96. Every event is quantised to whole frames. All motion runs on one global time function: frames are rendered as a pure function of t (no accumulated state), so any frame can be re-rendered alone.

### 5.2 Easing tokens
| Token | cubic-bezier | Used for |
|---|---|---|
| `set` | (0.20, 0.70, 0.10, 1.00) | text and element entrances |
| `out` | (0.40, 0.00, 1.00, 1.00) | exits (only inside continuous shots) |
| `glide` | (0.65, 0.00, 0.35, 1.00) | rostrum moves, collapse, pull-back, push into plate 12, coin→dot |
| `drift` | (0.37, 0.00, 0.63, 1.00) | slow pushes across a whole shot |
| `focus` | (0.33, 0.00, 0.15, 1.00) | rack focus |
| `snap` | (0.70, 0.00, 0.20, 1.00) | splits, slit shutter |
| `hop` | (0.50, 0.00, 0.20, 1.00) | router light travel |
| `draw` | (0.45, 0.00, 0.20, 1.00) | hairlines, strikes, frame, rules |

No springs, bounces, overshoot or elastic easing, ever.

### 5.3 Durations (frames)
XS 4 · S 8 · M 11 · L 16 · XL 27 · XXL 48 · beat 24. Per-glyph set-in is M; block exits are S; draws are L; rostrum moves are XXL; the slit is XL.

### 5.4 Text
- **Enter.** Per glyph: opacity 0→1 and y +8 px→0 (display) or +4 px (body), over M with `set`. Stagger is 40 ms per glyph for display, 20 ms for body, and 4 f between lines. Kickers enter whole (no stagger). Mono captions type on at 12–24 ms per character.
- **Exit.** Inside continuous shots, the whole block fades over S with `out`, finishing on the cut frame. On hard cuts, copy cuts with the picture.
- **Never:** blur-in, scale-in, tracking animation, per-letter rotation, typewriter on display type, highlight swipes, underline wipes.

### 5.5 Photographs
Photographs move like prints under a **rostrum camera**: scale and translate in the picture plane only.
- No rotation, no 3D, no fake parallax, no depth maps. The photo is an object, not a scene.
- Slow pushes are capped at **1.5% per second** (shots travel 1.5–6%).
- The only optical effect is the hook's rack focus (lens-disc blur with 2% focus breathing).
- Light is the main animated property: the key light, house lights up/down, the router light, the raking light.
- **Principle: we select with light, never with boxes, arrows or cursors.**

### 5.6 Transitions
- **Shots 1–6:** one continuous take (text swaps, light changes, splits, collapse, pull-back).
- **6→7:** hard cut on the bar line at 27.20 s, preceded by 0.4 s of silence. This is the only tonal inversion.
- **7→8→9→10→11:** hard cuts on beats. The running head persists, so the page feels bound and the cuts feel like page turns.

### 5.7 Signature moves
1. **The Reveal (catalogue mode).** A 48-frame pull-back turns the cinematic coin into cell 01 of a numbered contact sheet. Captions type themselves on with function names, pixel sizes and the skill each picture tests. The empty cell 12 draws in last. The film re-reads itself in two seconds.
2. **Step-and-Repeat → Collapse.** One plate divides into 4 → 16 → 64 → 256 copies on the beat, with sound that goes from four clicks to a pouring hiss of coins (commoditisation you can hear). Later, the 256 copies converge back into one plate in 16 frames, and the router's light starts picking among them.
3. **The Press.** Hard cut to paper. The empty cell is a blind emboss that only exists when the raking light passes (azimuth 215→135°, elevation 10→24°, 48 f). A 9-column push follows, while the felt-hammer "press" lands on the cut.

Supporting moves: the rack focus with breathing (hook); the slit shutter (niche); the router light with afterglow and the coin-pitch melody; the erratum strike and pigtail; the policy frame drawn around the retina; the coin→dot bookend.

### 5.8 Build notes
- **Layers.** DOM for all type, because Noto renders best in Chromium text. A single Canvas 2D or WebGL2 layer for plates, light, emboss and paper. A final **Python post pass** (§4.7) on the PNG frames: grain, halation, vignette, sub-frame averaging. Three.js is not needed; there is no 3D in this film by design.
- **Plate lighting.** Per frame: base plate × light map. Light map = max over active lights of fill + (k − fill)·exp(−½((max(d/r − 0.85, 0))/1.035)²), using the coin centres and radii in `coins.json`. It is cheap enough for SwiftShader, or precompute in numpy (`kit/prep.py::_lit`).
- **Rack focus.** Precompute 28 frames with `disc_blur(r)` for r = 16·(1 − focus(t)) (`kit/prep.py::disc_blur`).
- **Encode.** H.264 High, yuv420p, 1080×1920, 30 fps, CRF 15 / maxrate 16 Mbps, `-tune grain`. AAC 320 kbps 48 kHz. Grain doubles as dither against banding on the night ground after the platform re-encodes.

---

## 6. Sound design (all synthesised in Python: numpy / scipy, 48 kHz, float32, stereo)

### 6.1 Instruments
| Name | Recipe |
|---|---|
| **ROOM-night** | Pink noise (FFT 1/f), HP 40 Hz, LP 2.2 kHz (2nd order). L/R independent, mixed to correlation 0.3. −46 dBFS RMS. |
| **ROOM-paper** | Pink noise HP 300 Hz, LP 9 kHz, −50 dBFS RMS, plus Poisson fibre crackle (3/s, 0.3 ms clicks, BP 4–8 kHz, −48 dBFS). |
| **DRONE** | D2 73.42 Hz + A2 110 Hz, each 3 sines detuned ±0.07 Hz; tanh(1.2x)/tanh(1.2) saturation; amplitude LFO 0.05 Hz ±1.5 dB; 2-pole LP, cutoff automated. −30 dBFS RMS. Night only. |
| **PAD** | Additive voices, 8 partials (1/n²), attack 1.2 s, release 3 s, chorus ±4 cents. −28 dBFS RMS. Chords: D3 A3 E4 F♯4 (shot 7), G2 B2 D3 A3 (from 39.2 s), back to D (shot 9), D A E F♯ + D5 (shot 10). |
| **COIN** (modal) | Σ aₖ e^(−t/τₖ) sin(2π f₀ rₖ t + φₖ). r = [1, 1.592, 2.136, 2.653, 3.156, 4.044]; a = [1, .55, .38, .22, .14, .08]; τ = [1.4, .9, .6, .42, .3, .2] s (×0.6 for hops); random φ. Add a 3 ms white-noise contact, HP 4 kHz, at −12 dB, and a 1.003× detuned copy at −10 dB for shimmer. **f₀ per coin from `coins.json`.** |
| **POUR** | N COIN grains with f₀ ~ U(2.2, 6.5) kHz and τ×0.15. Exponential onset distribution over window W. Gains U(−24, −6) dB, pan U(±0.7). A 120 Hz, 30 ms "table" knock on the first grain. N/W: 4/40 ms, 16/80, 64/160, 256/320. |
| **SUB** | Sine with exponential glide 52→38 Hz over 260 ms, attack 4 ms, decay τ 90 ms, soft clip. −14 dBFS peak. |
| **FELT** (piano) | Partials n = 1…12, fₙ = n f₀ √(1 + B n²) with B = 0.0004; amplitudes n^−1.6 with −6 dB/oct above 1.2 kHz; attack 6 ms; two-stage decay (τ 0.25 s to −9 dB, then τ 3.5 s); felt thump (12 ms noise LP 300 Hz, −18 dB). 30% reverb send. |
| **VERB** | Synthetic stereo IR: gaussian noise × exp decay, RT60 1.6 s (general) or 2.4 s (hook and end), pre-delay 22 ms, early reflections at 7/13/19/29 ms (−8/−10/−12/−14 dB). IR one-pole LP 6 kHz, HP 120 Hz. `scipy.signal.fftconvolve`; wet −14 dB. |
| **BREATH** | Pink noise through a resonant LP (Q 0.9) sweeping 500→3000 Hz exponentially over 1.6 s, raised-cosine envelope. −32 dBFS. |
| **REVERSE** | The D6 COIN's 2.4 s reverb tail, reversed, ending exactly on the cut frame. −24 dBFS peak. |
| **PRESS** | 80 Hz sine τ 60 ms + BP 1.5–4 kHz noise burst (60 ms, τ 20 ms) + 150 ms paper crackle tail. −18 dBFS peak. |
| **PEN** | BP 2.5–7 kHz noise × envelope equal to the strike's eased velocity (derivative of `draw`), plus 40 Hz grain AM (paper tooth). −30 dBFS. |
| **STAMP** | Modal click f₀ 900 Hz, r [1, 2.76, 5.40], τ [40, 20, 10] ms, + 140 Hz knock τ 30 ms. −24 dBFS. |
| **TICK** | 0.3 ms impulse → BP 3 kHz Q 3, −44 dBFS ±3 dB, timing jitter ±4 ms. One per typed character in the mono captions only. |
| **SLIT / SHIMMER** | BP noise 300→1800 Hz over 0.9 s (−28 dBFS) + E1 41.2 Hz sine 2.4 s (−22 dBFS); sines 2637 / 3136 / 3951 Hz with a 3 s gaussian envelope (−44 dBFS). |

### 6.2 Cue sheet
| t (s) | frame | Cue | Picture event |
|---|---|---|---|
| 0.00 | 0 | ROOM-night + DRONE fade-in 1.2 s | coins in bokeh, kicker |
| 0.30 | 9 | SUB | headline line 1 setting |
| 0.40 | 12 | **COIN D6** (coin 16), VERB 2.4 s | glint on coin 16 |
| 3.33 | 100 | FELT D3 | *token* |
| 3.73–4.40 | 112–132 | TICK × chars | IPA + senses |
| 6.40 | 192 | DRONE LP opens 600→2400 Hz over 0.8 s | house lights up |
| 7.20 / 8.00 / 8.80 / 9.60 | 216 / 240 / 264 / 288 | POUR 4 / 16 / 64 / 256 | splits |
| 9.73 | 292 | FELT A2 | 残酷的价格战 |
| 13.07 | 392 | SLIT swell + E1 rumble | slit opens |
| 13.33 | 400 | SHIMMER | rocket at dusk |
| 16.00 | 480 | POUR 256 reversed (0.5 s) + FELT D3 | 256 → 1 collapse |
| 16.80 → 21.20 | 504 → 636, every 12 f | 12 × COIN (hop τ×0.6, −20 dBFS): F♯5 A5 D6 E6 F♯6 A6 F♯6 E6 D6 B5 A5 D5 | router light hops |
| 19.20 | 576 | FELT A2 | — |
| 21.60 | 648 | BREATH | pull-back |
| 22.80–23.80 | 684–714 | paper tick per cell (12 ms noise, BP 2–6 kHz, −36 dBFS) | cells appear |
| 26.40–26.80 | 792–804 | REVERSE (D6) | holding |
| 26.80–27.20 | 804–816 | **silence** | holding |
| 27.20 | 816 | ROOM-paper + PAD D3 A3 E4 F♯4 (−18) | **cut to paper** |
| 27.40 | 822 | **PRESS** | raking light begins |
| 33.20 | 996 | FELT A4 → D5 | our reading (violet) |
| 38.00 / 38.40 | 1140 / 1152 | PEN × 2 (+ flick at 38.93) | strike-through |
| 39.20 | 1176 | FELT G2+B2; PAD → G | 现在，他不这么想了 |
| 42.40 | 1272 | high-noise whisper 0.5 s (−40) | frame draws |
| 43.33 / 44.93 / 46.53 | 1300 / 1348 / 1396 | STAMP × 3 | 身份 / 记录 / 权限 |
| 46.40 | 1392 | PAD G → D | — |
| 49.60 / 51.20 / 52.80 | 1488 / 1536 / 1584 | FELT F♯4 / A4 / D5 | items 1 / 2 / 3 |
| 56.00 | 1680 | **COIN D6** (coin 16), VERB 2.4 s | the coin returns |
| 56.93 | 1708 | FELT D3 + A3 | dot lands, brand sets |
| 58.00–59.20 | 1740–1776 | ROOM fade to silence | end |

### 6.3 Mix
- Integrated loudness −16 LUFS (BS.1770-4 K-weighting and gating, implementable with two scipy biquads); true peak ≤ −1 dBTP (4× oversampled check + 2 ms look-ahead soft limiter).
- Music bed (DRONE/PAD/FELT) around −24 LUFS short-term. COIN peaks never exceed −6 dBFS (hook strike −8).
- Stereo: COIN hops panned by coin x; everything else is centred or decorrelated. No sidechain pumping.
- The single loudest moment is the PRESS on the inversion, not the hook. The film gets quieter as it gets more private.

---

## 7. Asset treatment recipes (reference implementation: `kit/prep.py`)
All sources come from `video/assets/lib/`. Crop boxes are in source pixels (x0, y0, x1, y1).

| File (src px) | Role | Crop box | Display size (scale) | Grade | Masks / extras | Max display (sharpness rule) |
|---|---|---|---|---|---|---|
| **coins.png** 384×303 L | **Hero.** Hook, token, commodity, mix, cell 01, cover, carousel 2–4 | full | Hook 922×727 (×2.40, dissolve) · plate 766×606 (×2.00) · tiles 381×301 / 190×150 / 94×74 / 46×36 · cell 205×162 (×0.534) | Selenium; cloth toe outside the matte | Watershed matte: Sobel elevation, markers < 30 bg / > 150 coin, fill holes, gaussian feather σ 1.2 src px → 24 coins (Appendix A). Key light per §5.8. Coin 16 matte crop (185,166)–(239,220) ×2.00 → coin ⌀ 94 px (end move). | ×2.40 only in dissolve mode (≤ 6.4 s, under motion and grain); **×2.00 for holds**; never larger. |
| **rocket.jpg** 640×427 | Hero. Niche slit; cell 02 | slit (250,120)–(393,423) = 143×303 | slit 286×606 (×2.00 → ×2.06 push) · cell 216×144 (×0.3375) | Vitrine CDL | Halation picks up the pad lights | ×2.06 |
| **retina.jpg** 1411×1411 | Hero. Identity (zero-trust); cell 10; index thumb | full (keep the black surround and the notch) | 488×488 (×0.346 → ×0.356) · cell 162 · index 96×72 centre-crop | Vitrine, paper variant (offset .05/.045/.04, sat .90) | none | never upscaled (native 1411) |
| **text.png** 448×172 L | Hero. Erratum plate (the old belief); cell 07 | full | 696×267 (×1.554 → ×1.58) · cell 216×83 | Selenium, paper variant | none; the source's shallow focus hides the upscale | ×1.58 (soft by nature) |
| coffee.png 600×400 | cell 03 | full | 216×144 (×0.36) | Vitrine | — | downscale only |
| camera.png 512² L | cell 04 | full | 162×162 (×0.316) | Selenium | — | downscale only |
| astronaut.png 512² | cell 05 (catalogue thumbnail only) | full | 162×162 | Vitrine | Real person: never used as a metaphor; only her library label. | downscale only |
| moon.png 512² L | cell 06 | full | 162×162 | Selenium | — | downscale only |
| clock_motion.png 400×300 L | cell 08 | full | 216×162 (×0.54) | Selenium | — | downscale only |
| hubble_deep_field.jpg 1000×872 | cell 09 | full | 186×162 (×0.186) | Vitrine | — | downscale only |
| grace_hopper.jpg 512×600 | cell 11 (catalogue thumbnail only) | full | 138×162 (×0.27) | Vitrine | Real person: same rule as astronaut. | downscale only |
| earth-*.jpg/png, hdri_*.exr | **Not used** | — | — | — | Deliberate. They are not test images, so using any of them would make the line 「片中的照片，全是开源软件自带的测试图」 false. It also keeps us clear of the globe cliché. | — |

Derived plates: `field_slit` (16×16 field at 42% + rocket slit), `coins_hops_multi_x2` (carousel 3 exposure: 24 .22, 22 .36, 11 .55, 21 .78, 18 1.0), `emboss_*` (§4.8), `paper_*` (static paper), `idx_*` index thumbnails.

---

## 8. Risks, and how we avoid looking AI-made or cheap
| Risk | Mitigation |
|---|---|
| Small sources look soft | Holds never exceed ×2.00. Anything above (hook ×2.40) is in dissolve mode, in motion, under grain and behind a rack focus. Every other photo is shown at or below native size. The captions *declare* scale, so softness reads as honesty, not failure. Grain is applied at output resolution. |
| The twist is too nerdy | It is delivered in one plain sentence (片中的照片，全是开源软件自带的测试图). The viewer needs no knowledge of scikit-image. The payoff (公开的考题，谁都能刷分；你的考题，只有你有) is a founder-level truth labelled as ours. |
| The twist becomes false | **Do not add any photo that is not a library test image** (no Earth maps, no stock). Only CG that is obviously graphic (the field, the emboss, the dot) is allowed. |
| Misattribution | Every Nadella claim carries a kicker (判断 / 认为 / 据报道 / 他说). No quotation marks. Violet means ours, plus two textual labels. Sources on the end card and carousel 7. Nothing from the earnings call, the X post or the essay. |
| Real people used as props | The astronaut and Grace Hopper appear only as catalogue thumbnails with their library labels: never cropped, never captioned with invented context, never matched to a claim. |
| Dark first half feels heavy | Act I is 27 s and carries five distinct light events (focus, lights up, slit, router, pull-back). The inversion then gives 32 s of paper. |
| The emboss is invisible on a phone | The raking light gives it motion contrast. The rest-light shadow is a soft 1.5–2 px edge, and the caption names it (图版 12 · 未公开). In carousel 5 it sits in a framed composition with its caption beside it. |
| Platform re-encode banding on night | Grain doubles as dither, there are no large smooth gradients (vignette 0.12 only), and the master is high-bitrate (§5.8). |
| SwiftShader load | No 3D. All shaders are 2D (light map, emboss) or precomputed in numpy; the post pass is in Python. |
| The coin→dot morph feels gimmicky | 16 frames, no particles, no glow, no trail. It is a scale and a colour change anchored to the dot's own position, closed by the same D6 as the opening. |
| "AI look" checklist (banned) | Purple-blue gradients; neon glow; centred-everything; boxes around text; comic caption boxes (previous film); hard drop shadows; emoji; icons; HUD rings; data dashboards; fake numbers; floating particles; plexus networks; spinning globe; lens flares; chromatic aberration; glitch; bounce easing; blur-in text; kinetic-type jumbles; stock "tech" textures. |
| What we do instead | One grid, one accent with one meaning, real light on real photographs, honest scale, a 4 px baseline, hand-set line breaks, measured music, and long silences where nothing moves except grain. |

---

## Appendix A: coin table (from the watershed segmentation of `coins.png`)
Centres and radii in source px; pitch = radius mapped linearly over 1.5 octaves above D5 (largest = D5), quantised to D-major pentatonic.

| # | cx | cy | r | note | Hz | | # | cx | cy | r | note | Hz |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 01 | 44.2 | 54.4 | 20.8 | E6 | 1318.5 | | 13 | 43.7 | 197.4 | 18.9 | F♯6 | 1480.0 |
| 02 | 100.2 | 56.1 | 18.7 | A6 | 1760.0 | | 14 | 101.7 | 195.6 | 21.6 | E6 | 1318.5 |
| 03 | 155.3 | 50.8 | 22.9 | D6 | 1174.7 | | 15 | 154.1 | 197.7 | 19.1 | F♯6 | 1480.0 |
| 04 | 215.2 | 51.1 | 22.7 | D6 | 1174.7 | | **16** | **212.4** | **193.1** | **23.5** | **D6** | **1174.7** |
| 05 | 276.1 | 52.4 | 19.7 | F♯6 | 1480.0 | | 17 | 273.5 | 193.6 | 21.8 | E6 | 1318.5 |
| 06 | 334.7 | 43.5 | 28.8 | F♯5 | 740.0 | | 18 | 347.0 | 186.7 | 31.6 | D5 | 587.3 |
| 07 | 44.7 | 124.3 | 20.3 | F♯6 | 1480.0 | | 19 | 45.9 | 259.8 | 28.0 | F♯5 | 740.0 |
| 08 | 102.3 | 125.6 | 18.8 | A6 | 1760.0 | | 20 | 113.9 | 265.5 | 21.2 | E6 | 1318.5 |
| 09 | 153.5 | 127.2 | 18.5 | A6 | 1760.0 | | 21 | 172.3 | 261.2 | 27.4 | A5 | 880.0 |
| 10 | 205.3 | 123.7 | 19.6 | F♯6 | 1480.0 | | 22 | 244.0 | 263.3 | 23.7 | D6 | 1174.7 |
| 11 | 270.6 | 118.8 | 24.7 | B5 | 987.8 | | 23 | 300.6 | 263.2 | 25.2 | B5 | 987.8 |
| 12 | 336.2 | 124.5 | 19.3 | F♯6 | 1480.0 | | 24 | 358.2 | 267.9 | 21.7 | E6 | 1318.5 |

Router sequence (shot 5): 06 → 21 → 03 → 14 → 10 → 02 → 13 → 24 → 22 → 11 → 21 → 18.

## Appendix B: copy deck in order (for proofreading)
1. 微软CEO纳德拉判断｜大模型｜要打价格战了
2. token｜/ˈtəʊkən/ n.｜1 大模型API的计价单位｜2 代币：代替钱流通的小圆片
3. 纳德拉判断｜大多数企业的日常算力｜终将变成大宗商品 → 他判断｜模型层，会有一场｜残酷的价格战｜× 4 / × 16 / × 64 / × 256｜= 6,144 枚
4. 他认为｜最前沿的模型｜只会服务少数顶尖场景
5. 据报道｜微软Copilot内部｜每天都在混用多家模型｜便宜的闭源模型，和开源模型
6. 片中的照片，全是｜开源软件自带的测试图｜谁都能下载，谁都能拿它考算法｜01 coins() 分割 … 11 grace_hopper.jpg matplotlib｜12｜前10张来自scikit-image（skimage.data），1张来自matplotlib
7. 纳德拉认为｜每家公司，都会有｜自己的私有评测集｜这会是它的核心IP｜图版 12 · your_eval() · 未公开 · 尺寸：只有你知道｜● 我们的理解｜公开的考题，谁都能刷分｜你的考题，只有你有
8. 被问到改变过什么看法，他说｜图版 07 · text() · 448 × 172 px · × 1.55｜~~以前以为：模型规模够大｜对齐就会自然出现~~｜现在，他不这么想了
9. 他说｜微软不等对齐问题解决｜先给模型套上零信任架构｜身份 每个Agent 都有身份｜记录 每次调用 都留痕｜权限 规则放在 模型之外｜图版 10 · retina() · 1411 × 1411 px · × 0.35｜视网膜的血管分布因人而异，常被用作身份识别
10. ● 我们的解读｜给出海创业者的三件事｜1 架构上支持多模型路由，别绑死一家｜2 建一套自己的私有评测集｜3 Agent的身份、日志、权限，放在模型之外｜以上是我们的理解，不是纳德拉原话
11. 你的产品，现在｜接了几家模型？｜评论区聊聊｜● Coo-Coo出海Ai实验室｜来源：20VC 播客（主持 Harry Stebbings），嘉宾 Satya Nadella（微软CEO）｜2026.10.26 发布。文中观点据公开报道整理，均为转述，非逐字引用｜图片：scikit-image 与 matplotlib 自带的测试图｜Brooklyn Museum · SpaceX · NASA · Rachel Michetti · Lav Varshney｜Stefan van der Walt · Wikimedia Commons · U.S. Navy

Running head throughout: 纳德拉 × 20VC · 2026.10.26 · (01 价格战 / 02 混用 / 03 测试图 / 03 评测集 / 04 改口 / 04 零信任 / 05 我们的解读). Cover footer: 4个判断 · 3点解读 →.
