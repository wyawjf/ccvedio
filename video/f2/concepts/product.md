# 侧光 · RAKING LIGHT
### Product-film concept for F2 — 「微软CEO：大模型要打价格战了」
*One light. One coin from Pompeii. Three photographs. The light is the only actor.*

**Files that come with this pitch** (all under `video/f2/concepts/product/`)

| What | Where |
|---|---|
| This spec | `video/f2/concepts/product.md` |
| Finished look-dev frames, 1:1, film texture applied | `proof/film_S01…S10_*.png` (13 moments; each filename carries its timecode), `proof/carousel_01…07_*.png` (all 7 frames) |
| Overview sheets | `proof/_film_sheet.jpg`, `proof/_carousel_sheet.jpg`, `proof/_cover_thumbnail_test.jpg` (cover and frame 5 at phone-feed size), `proof/_flattening_strip.jpg` (signature move 1 in six steps) |
| Reference code: every number in §7 comes from here | `kit/relight.py` (the relight model), `kit/prep.py` (plates; reads only `assets/lib/`), `kit/proof.html` + `kit/shoot.mjs` (layouts, the Three.js glass shot), `kit/look.json` (finishing, fed to the existing `f2/film.py`) |

Rebuild everything from `video/`: `python3 -I f2/concepts/product/kit/prep.py all && python3 -I f2/concepts/product/kit/prep.py tray2 && python3 -I f2/concepts/product/kit/prep.py strip && node f2/concepts/product/kit/shoot.mjs`, then for each raw frame `python3 -I f2/film.py --still f2/concepts/product/proof/raw/<f>.png <out>.png --look f2/concepts/product/kit/look.json`.

The proofs are static look-dev frames, not the film. They use the exact tokens below. Where a proof and this text disagree, this text wins.

---

## 1. The idea

### 1.1 Name and logline

**侧光 · RAKING LIGHT**

> One light and one ancient coin. Under flat light every token looks the same: that is the price war. Lower the light to your own angle and the face comes back: that is your private eval.

### 1.2 The big idea

A token is a coin-like disc (the general fact the brief allows). Coins carry relief, and relief only shows at an angle. Anyone who has photographed a coin knows the rule: **frontal light flattens, raking light reveals.** Museums read worn coins this way (raking-light and RTI imaging).

So the film has one actor, a single key light, and one variable that drives the plot: **the light's elevation above the table.**

| Act | Light | What we see | What it means |
|---|---|---|---|
| Hook | 4–6°, warm 3200 K | A 2,000-year-old face rises out of black | The token |
| Price war | rises to 84°, cold 5600 K | The face drains away; 24 different coins become 24 grey discs | Commoditisation, shown by physics instead of a filter |
| Frontier | the photo's own floodlights | A rocket at dusk is the only thing in the world that gets all the light | A few top niches |
| Mixing | a moving spot at 36° | The light lands on a different coin every beat while 一 二 三 … ticks | Copilot mixes models every day |
| Private eval | drops to 5°, warm 3000 K | The face returns, sharper than in the hook | His point. Our reading: a public leaderboard is flat light; your eval is your own raking light |
| Changed mind | Hubble | Years of exposure stacked into one frame; the push-in stops dead | Scale did not bring alignment |
| Zero trust | 12° | An invisible glass case shows only where the light finds its edges, then lowers over the coin | Wrap the model. Identity, logs and permissions sit outside the glass |
| End | off | One violet status light turns on | The account |

The film also argues about ownership through its own material. The coin is public: a museum photograph anyone can download. **The angle of the light is the only thing in each frame that we made.** Our closing reading says exactly that: 模型，人人都买得到；看它的角度，只有你有。

### 1.3 Why it reads as human-made (what a jury would notice)

1. **One physical light, consistent in every frame.** Relief contrast is computed: brightness ∝ 1 + cot(elevation)·k·(−∇h·l̂). At 84° the relief flattens by itself; at 5° it leaps out with matching cast shadows. Pause anywhere and the shading, shadow direction, colour temperature and the light gauge in the corner all agree.
2. **The method is real and declared.** Every coin caption says 本片重新打光 (relit for this film). A 56-pixel coin is presented as what it is, a macro under a raking lamp, never as a sharp photograph.
3. **The metaphor is demonstrated, not asserted.** In S6b the same coin, camera and frame flip flat, then raking, under two lines of copy. Carousel frame 5 does it in one glance as a diptych.
4. **Colour temperature carries meaning.** Commodity light is cold and flat (5600 K, from above). Your light is warm and low (3000–3200 K). The audience feels it before they read it.
5. **The light has a voice.** Warm filament hum when it is low and warm, thin fluorescent buzz when it goes flat and cold, a servo whir when it moves, a relay click when it switches. You could follow the lighting plot with your eyes closed.
6. **Restraint.** Three photographs, one light, one accent colour that appears in exactly two roles, two typefaces plus one mono. No boxes, no decorative gradients, no icons, no charts.
7. **Details only a close viewer finds.** Felt fibres that appear only under grazing light. Float-glass green on the case's inner edges. One caustic line where light passes through the wall. Two dust specks that exist only while the reflection crosses them.
8. **Typographic finish.** Three voices set in type: his statements always carry a grey kicker (他判断 / 纳德拉认为 / 据报道 / 他说); general facts carry none; our reading carries a violet dot and a 2 px violet rule. Other details: CJK–Latin spacing with U+2005, a 4 px baseline, and no terminal punctuation on display lines.
9. **The brand arrives as a status LED, not a logo sting.** Lights out, then one violet point turns on.
10. **Honest pixels.** No photograph is ever shown beyond the scale at which it stays plausible: coins ≤ 6.5×, rocket ≤ 2.1×, Hubble ≤ 1.27× (§7.5).

### 1.4 Content compliance map

| On screen | Voice (typographic marker) | Brief point |
|---|---|---|
| 微软 CEO 纳德拉判断 / 大模型 要打价格战了 | his judgment (kicker) | 1 |
| 大模型按 token 计价。token 在英文里，也指代币：一种代替钱流通的小圆片。 | general fact (no kicker) | allowed general fact |
| 他判断：大多数企业场景的日常算力，终将商品化。 | his (kicker 他判断) | 1 |
| 他判断：模型层，会有一场残酷的价格战。 | his | 1 |
| 他判断：最前沿的模型，只会服务少数顶尖场景。 | his | 1 |
| 据报道：微软 Copilot 内部，每天都在混用便宜的闭源与开源模型。 | reported (kicker 据报道) | 2 |
| 纳德拉认为：每家公司，都会有自己的私有评测。那会是它的核心 IP。 | his | 3 |
| ● 我们的理解：公开榜单像顺光……私有评测是你自己的侧光…… | ours (violet) | our reading |
| 被问到改变过什么看法：他以前以为，规模够大，对齐自然会来。现在，他不这么想了。 | his, in the third person | 4 |
| 他说：微软不等对齐问题解决，先给模型套上零信任架构。身份 / 记录 / 权限 | his | 4 |
| ● 我们的理解：模型，人人都买得到。看它的角度，只有你有。你的评测，你的规则。 | ours (violet) | our reading |
| Coo-Coo出海Ai实验室 + source line + photo credits | account | required ending |

Never on screen: quotation marks around any paraphrase; the neocloud line (earnings call); "assume the model is compromised" (X post); "private evals define what good looks like" (essay); any price, percentage or model name; any hype word. His changed mind is paraphrased in the third person (他以前以为…), so nothing reads as an unmarked direct quote.

### 1.5 What this is not

No globe, no network lines, no glowing data, no comic boxes, no drawn figures (the rejected F attempts). No collage of the whole library: 9 of the 14 assets are left out on purpose (§7.6).

---

## 2. Film storyboard

**Format:** 1080×1920, 30 fps, **58.333 s = 1750 frames**. The clock is 72 bpm (1 beat = 0.8333 s = 25 frames); every cut and every light landing sits on a beat or half-beat.

**Tokens** used in the table (D1, D2, D3, K, L, TAG, OURS, C1, C2, IDX, GAUGE, DAYS, BRAND) are defined in §4.3; motion tokens (T-IN, T-OUT, T-DIM, ease-light, ease-camera …) in §5. Text positions are the top-left of the text box in px on the 1080×1920 canvas.

**Coin world** means every shot made from relit `coins.png` (S1–S3, S5–S6b, S8–S9). Light angles: **az** is the direction the light comes from, counter-clockwise from screen-right (90° = from the top of the screen, 180° = from the left). **el** is the elevation above the table.

### 2.1 Shot table

| # | In–out (s) · frames | Picture: asset, crop, treatment | Camera / light / motion | On-screen copy (exact) · token · position · timing | Transition out | Sound (§6.2) |
|---|---|---|---|---|---|---|
| **S1 Hook** | 0.000–3.333 · f0–100 | `coins.png` hero coin #23 (helmeted head, centroid src (45,259), ⌀56 px). Crop (0,214)–(94,303); neighbours masked; relit (§7.1); shown at **6.0×** (coin ⌀336 px) centred at (540,1040) on synthetic black felt with an elliptical light pool (r0 1.35R, r1 3.1R, ×1.45 along the light) | LX1–LX2: light from the left, az 200°→160°, el 4°→6°, 3200 K. Intensity 0.10→1.00 over 0–0.40 s (cubic-bezier(0.16,1,0.3,1)), so **frame 0 is a thin lit crescent on the left rim, never black**. Turntable: the table rotates −4°→+2° about the coin centre, 3.333 s, ease-camera. Push-in 1.000→1.035, ease-camera | **K** 微软 CEO 纳德拉判断 (96,300), T-IN at 0.20<br>**D1** 大模型 (96,352), T-IN at 0.36<br>**D1** 要打价格战了 (96,500), T-IN at 0.45<br>**GAUGE** 侧光 EL 04°→06° 3200K, fades in at 0.60<br>**C1** 古希腊钱币，庞贝出土 (96,1388) and **C2** 照片：布鲁克林博物馆　本片重新打光 (96,1420), at 1.20<br>K and D1 T-OUT at 3.00 | Continuous (no cut) | 0.000 THOOM; LAMP warm fades in (400 ms); PAD Dmaj9 (1.5 s attack). 0.533 GLINT E7 as the light first crosses the helmet crest |
| **S2 Token** | 3.333–7.500 · f100–225 | Same coin, same treatment | LX3: az 160°→150°, el 6°→10°, intensity 1.00→1.05, ease-light 4.167 s. Turntable +2°→+6°. Push 1.035→1.060 | **D2** 大模型按 token 计价。 (96,300), T-IN at 3.45<br>**D3** in ink-2: token 在英文里，也指代币：/ 一种代替钱流通的小圆片。 (96,408), T-IN at 4.20<br>(No kicker: it is a general fact, not his)<br>Both T-OUT at 7.10; captions T-OUT at 7.50 | Continuous | 3.333 KEY A4; 5.000 soft GLINT B6 |
| **S3a The Flattening** (signature 1) | 7.500–10.000 · f225–300 | Same coin; only the light changes | LX4: el 10°→84°, az 150°→90°, 3200 K→5600 K (linear in mired, 312.5→178.6), pool r0 1.35R→1.9R, r1 3.1R→3.8R, stretch 1.45→1.0, ease-light 2.5 s. The face drains to a grey disc. The gauge dot travels from the rim to the centre; its name crossfades 侧光→顺光 when el passes 60°. Turntable eases to rest at +6° by 8.0 | **IDX** 01 价格战 (96,222) at 7.60<br>**K** 他判断 (96,300) at 7.70<br>**D2** 大多数企业场景的日常算力，/ 终将商品化。 (96,352) at 7.85 | Continuous into the pull-back | 7.500 SERVO (follows the light's angular speed). LAMP→FLUORO crossfade 8.0–9.6. PAD moves to Bm7 and thins (high-pass 40→180 Hz, low-pass 900→2400 Hz) |
| **S3b Price war** | 9.600–15.000 · f288–450 | Full tray `coins.png` (0,0)–(384,303), flat-lit (el 84°, 5600 K), shown at **2.5×** (960×757) with its top-left at (60,760), 92 px edge feather, tray pool r0 0.30W, r1 0.62W. From 9.6 to 10.4 the isolated hero render crossfades to the full-tray render (identical light), so the neighbours "arrive" as the pool widens | Pull-back 9.600–12.000 (2.4 s, ease-camera): scale 6.0×→2.5×, view centre from the hero to the tray centre, table rolls +6°→0°. 12.0–15.0: drift up 12 px (linear). LX6 13.0–15.0: −0.25 EV (intensity 1.00→0.84) | 11.250: the first statement goes T-DIM (to 0.38)<br>**D2** 模型层，会有一场 / 残酷的价格战。 (96,552) T-IN at 11.25<br>GAUGE 顺光 EL 84° 5600K | **Light cut** LX7 at 14.850 (4 frames to void), hard cut at 15.000 | 11.250 KEY figure F#5–D5–B4 (descending). 14.850 RELAY; FLUORO stops with the light |
| **S4 Frontier** | 15.000–20.000 · f450–600 | `rocket.jpg` crop (196,24)–(444,427), **2.0×** → 496×806 at (292,580); graduated ND on the sky, saturation 0.85 (§7.2). The pad lights are the shot's only light (the gauge hides: these are the photo's own lamps) | Push-in 1.00→1.05, origin at the base (540,1300), plus 10 px upward drift, 5.0 s, cubic-bezier(0.33,0,0.67,1). Film flicker 0.004 for this shot only (sodium lamps) | **IDX** stays 01 价格战<br>**K** 他判断 (96,300) at 15.10<br>**D2** 最前沿的模型，/ 只会服务少数顶尖场景。 (96,352) at 15.25<br>**C1** 猎鹰 9 号与 DSCOVR 卫星，发射前，2015 (292,1400) and **C2** 照片：SpaceX　公有领域 (292,1434) at 15.60 | **Light cut**: plate exposure to 0 over 19.667–20.000 (10 frames, cubic-bezier(0.7,0,0.84,0)) | 15.000 PAD Gmaj7(#11), wide; FLOOD HUM; AIR swell. 19.667 all out with the plate |
| **S5 Mixing** | 20.000–26.667 · f600–800 | Tray again at 2.5×, top-left (60,720), now dark: ambient 0.035. A moving-head spot: el 36°, 3200 K, intensity 1.30, pool r0 52 px, r1 158 px on screen | LX8. Eight landings, one per beat from 20.417 (path in §2.3). Each hop: 380 ms, cubic-bezier(0.34,1.36,0.64,1) (servo overshoot ≈ 3%), pool −8% while travelling, blooms back on landing | **IDX** 02 混用 (96,222) at 20.00<br>**K** 据报道 (96,300) at 20.10<br>**D2** 微软 Copilot 内部，/ 每天都在混用 / 便宜的闭源与开源模型。 (96,352) at 20.25<br>**DAYS** 一 二 三 四 五 六 日 (96,648) at 20.30; the current day lights on each landing<br>**TAG** 闭源 / 开源 on the landed coin (geometry in §2.3); in 200 ms after landing, out 200 ms before the next hop<br>GAUGE 追光 EL 36° 3200K; the dot's azimuth is the direction from the tray centre to the spot | Continuous: landing 8 is the hero coin | RELAY + KEY on every landing (A4 = 闭源, D5 = 开源; panned to the coin's x); SERVO between landings. Landing 8: click only |
| **S6 Private eval: Your Angle** (signature 2) | 26.667–31.667 · f800–950 | Hero coin, back at 6.0×, centre (540,1060). From 28.3, once the neighbours are dark, the render switches back to the isolated-hero pass | 26.250–26.650 (LX9): ambient 0.035→0, the neighbours fall dark. 26.667–28.333: push-in 2.5×→6.0×, ease-camera 1.667 s. **LX10 28.333–29.583**: el 36°→5°, az 128°→170°, 3200→3000 K, intensity 1.30→1.18, spot pool → hero pool, ease-light 1.25 s. The face rises out of the flat disc | **IDX** 03 私有评测 (96,222) at 26.75<br>**K** 纳德拉认为 (96,300) at 26.85<br>**D2** 每家公司，都会有 / 自己的私有评测。 (96,352) at 27.00<br>**D2** 那会是它的核心 IP。 (96,552) T-IN at **29.583**, landing with the light<br>**C2** 同一枚钱币，光从 5° 掠过 (96,1424) at 29.80<br>GAUGE 追光→侧光 EL 05° 3000K | Continuous | 28.333 SERVO descending (240→160 Hz). 29.583 BLOOM (Dadd9) + GLINT E7. FLUORO→LAMP warm |
| **S6b Our reading** | 31.667–36.667 · f950–1100 | Same coin; the frame shifts the coin to y 1100 (40 px, ease-camera 600 ms) to give the text air | **LX11 32.000–33.000**: el 5°→84°, az 170°→90°, 3000→5600 K (the flattening, reprised in 1.0 s). **LX12 34.167–35.167**: back to el 5°, az 170°, 3000 K | His text T-OUT at 31.667<br>**OURS** violet rule draws at 31.70; tag ● 我们的理解 (124,300)<br>**D3** in ink-2: 公开榜单像顺光，/ 模型看起来都差不多。 (124,354) at 32.00<br>**D3** in ink-1: 私有评测是你自己的侧光，/ 照出你在乎的差别。 (124,524) at **34.167**, landing with the light<br>GAUGE follows: 顺光 84° → 侧光 05° | **Light cut** LX13 at 36.300 (10 frames to void) | 32.000 FLUORO on, LAMP off (120 ms); PAD thins. 34.167 FLUORO off, LAMP on; small BLOOM + soft GLINT |
| **S7 Changed mind** | 36.667–43.333 · f1100–1300 | `hubble_deep_field.jpg` crop (120,86)–(880,786), **1.168×** → 888×818 at (96,580), saturation 0.80 (§7.3). Gauge hidden | Push-in 1.00→1.08 about the plate centre, 36.667–40.833, cubic-bezier(0.33,0,0.67,1). **40.833: HARD STOP**: velocity to 0 in 4 frames, plate −0.7 EV (to 62%) over 300 ms | **IDX** 04 改变的看法 (96,222) at 36.75<br>**K** 被问到改变过什么看法 (96,300) at 36.85<br>**D2** 他以前以为，规模够大，/ 对齐自然会来。 (96,352) at 37.00<br>**C1** 哈勃极深场，2012 (96,1410) and **C2** 照片：NASA　公有领域 (96,1444) at 37.40<br>40.833: the first statement goes T-DIM<br>**D2** 现在，他不这么想了。 (96,552) T-IN at **41.000**, inside the silence | **Light cut**: plate to 0 over 43.000–43.333 (10 frames) | 36.667 SPACE BED + BELLS A5/E6/B6. **40.833 digital silence for 0.42 s.** 41.250 KEY D3, low, long |
| **S8 Zero trust: The Glass** (signature 3) | 43.333–50.833 · f1300–1525 | The hero coin (el 12°, az 150°, 3200 K) as the texture of a table plane in 3D, seen at 3/4 (§2.4). A CG glass case (§7.4): footprint 460×460, height 190, wall 6 (units = px of the 6× plate). Coin centre on screen (540,1010) | LX14: light comes up in 8 frames. Orbit −4°→+4° around the coin, 43.333–50.833, ease-camera. **Glass descends** z +420→0, 43.700–44.900, cubic-bezier(0.22,1,0.36,1), then a damped settle (ω 18 rad/s, ζ 0.62, −3 units overshoot, 240 ms). It is nearly invisible until its edges catch the light on the way down. **Sweep** (LX15) 45.000–45.900: a soft specular streak crosses the top glass left→right with the hot front-top edge segment; two dust specks flash inside it | **IDX** 04 零信任 (96,222) at 43.40<br>**K** 他说 (96,300) at 43.45<br>**D2** 微软不等对齐问题解决，/ 先给模型套上零信任架构。 (96,352) at 43.60<br>Hairline (96→984, y 1248) draws at 45.60, the label plate in front of a museum case<br>**L** 身份　每个 agent 都有自己的身份 (96,1270) at 45.80<br>**L** 记录　每一次工具与模型调用都留下记录 (96,1342) at 46.40<br>**L** 权限　规则放在模型之外 (96,1414) at 47.00<br>GAUGE 侧光 EL 12° 3200K | Continuous into S9 | 43.333 LAMP on. 43.700 WHOOSH. 44.900 SEAL. 45.450 GLASS TICK as the streak hits the edge. 45.80 / 46.40 / 47.00 TICK ×3. PAD Bm7 → Gmaj7 at 48.333 |
| **S9 Our reading** | 50.833–55.000 · f1525–1650 | Same 3D shot; the coin centre moves to (540,1110) (view offset, ease-camera 1.0 s) | Orbit continues. LX16: az 150°→200° over 4.0 s, ease-light; the relief shimmers as the light walks round | S8 text and labels T-OUT at 50.833<br>**OURS** rule + tag ● 我们的理解 (124,300)<br>**D2** 模型，人人都买得到。/ 看它的角度，只有你有。 (124,354) at 51.00<br>**D3** in ink-2: 你的评测，你的规则。 (124,552) at 53.00 | **Lights out** LX17 at 55.000 (4 frames) | 50.833 MOTIF F#5–E5–D5–A4; PAD Dmaj9 |
| **S10 End** | 55.000–58.333 · f1650–1750 | Void plus grain only | 0.4 s of darkness, then a 14 px violet dot turns on like a power LED (opacity 0→1 in 2 frames, glow 0→1 in 300 ms) | **BRAND** ● Coo-Coo出海Ai实验室: dot centre (103,844), text (126,820), T-IN at 55.60<br>**C1** 大模型要打价格战了　20VC 对话纳德拉　笔记 (96,896) at 55.90<br>**C2** (96,1288) at 56.30, three lines:<br>来源：20VC 播客，Harry Stebbings 对话 Satya Nadella（微软 CEO），2026.10.26 发布。<br>片中观点据公开报道转述，非原话；标注为我们的理解的部分，是本号观点。<br>图片：布鲁克林博物馆（本片重新打光）、SpaceX、NASA；公有领域或无已知版权限制。 | End (hold) | 55.000 RELAY; LAMP off; PAD tail 2.5 s. 55.400 LED TICK. Last 0.5 s silent |

### 2.2 Lighting cue list (the lighting plot)

`ease-light` = cubic-bezier(0.45, 0, 0.2, 1). R = hero coin radius on screen (168 px at 6×). W = tray texture width at 3× (1152).

| LX | t (s) | dur (s) | curve | az (°) | el (°) | K | intensity | pool | note |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.000 | 0.400 | (0.16,1,0.3,1) | 200 | 4 | 3200 | 0.10→1.00 | hero: 1.35R / 3.1R / ×1.45 | light on; frame 0 = rim crescent |
| 2 | 0.000 | 3.333 | ease-light | 200→160 | 4→6 | 3200 | 1.00 | hero | hook sweep |
| 3 | 3.333 | 4.167 | ease-light | 160→150 | 6→10 | 3200 | 1.00→1.05 | hero | token |
| 4 | 7.500 | 2.500 | ease-light | 150→90 | 10→84 | 3200→5600 (mired-linear) | 1.05→1.00 | → 1.9R / 3.8R / ×1.0 | **the Flattening** |
| 5 | 9.600 | 2.400 | ease-camera | 90 | 84 | 5600 | 1.00 | → tray 0.30W / 0.62W | follows the pull-back |
| 6 | 13.000 | 2.000 | linear | 90 | 84 | 5600 | 1.00→0.84 | tray | −0.25 EV |
| 7 | 14.850 | 0.133 | (0.7,0,0.84,0) | | | | →0 | | off (relay) |
| 8 | 20.000 | 0.267 | (0.16,1,0.3,1) | 128 | 36 | 3200 | 0→1.30, ambient 0.035 | spot 62 / 190 (3× texture px) | moving head, §2.3 |
| 9 | 26.250 | 0.400 | ease-light | 128 | 36 | 3200 | ambient 0.035→0 | spot on hero | neighbours fall dark |
| 10 | 28.333 | 1.250 | ease-light | 128→170 | 36→5 | 3200→3000 | 1.30→1.18 | spot → hero | **Your Angle** |
| 11 | 32.000 | 1.000 | ease-light | 170→90 | 5→84 | 3000→5600 | 1.18→1.00 | hero → flat | reprise: public leaderboard |
| 12 | 34.167 | 1.000 | ease-light | 90→170 | 84→5 | 5600→3000 | 1.00→1.18 | flat → hero | reprise: your eval |
| 13 | 36.300 | 0.333 | (0.7,0,0.84,0) | | | | →0 | | off |
| 14 | 43.333 | 0.267 | (0.16,1,0.3,1) | 150 | 12 | 3200 | 0→1.05 | 1.4R / 3.0R / ×1.3 | glass shot |
| 15 | 45.000 | 0.900 | ease-light | | | | | | reflection streak u 0→1 across the top glass |
| 16 | 50.833 | 4.000 | ease-light | 150→200 | 12 | 3200 | 1.05 | same | light walks round |
| 17 | 55.000 | 0.133 | (0.7,0,0.84,0) | | | | →0 | | lights out (relay) |

S4 and S7 use the photographs' own light; no LX cue, gauge hidden.

### 2.3 S5 spot path

Tray at 2.5×, top-left (60,720): screen = (60 + 2.5x, 720 + 2.5y). Landing n happens at 20.417 + (n−1)·0.8333 s.

| n | landing (s) | day | coin centroid, src px | ⌀ src | screen centre | tag | tag side |
|---|---|---|---|---|---|---|---|
| 1 | 20.417 | 一 | (155, 50) | 46 | (448, 845) | 闭源 | below |
| 2 | 21.250 | 二 | (270, 118) | 49 | (735, 1015) | 开源 | above |
| 3 | 22.083 | 三 | (101, 195) | 43 | (313, 1208) | 开源 | above |
| 4 | 22.917 | 四 | (300, 263) | 50 | (810, 1378) | 闭源 | above |
| 5 | 23.750 | 五 | (205, 123) | 39 | (573, 1028) | 开源 | above |
| 6 | 24.583 | 六 | (347, 186) | 63 | (928, 1185) | 闭源 | above |
| 7 | 25.417 | 日 | (172, 261) | 55 | (490, 1373) | 开源 | above |
| 8 | 26.250 | | (45, 259), hero | 56 | (173, 1368) | none | |

Tag geometry: a 1×32 px leader starts 14 px outside the coin's radius (r = 1.25·⌀src). The TAG text (44/52, centred on the coin's x, clamped to x 96–984) sits 8 px beyond the leader end. The leader draws in 160 ms (height 0→32, ease-camera). The order 闭 开 开 闭 开 闭 开 is deliberately irregular: mixing, not alternating.

### 2.4 Coin-world camera

- **Top-down, orthographic** for S1–S3b, S5–S6b (the source is a top-down photograph; we never fake parallax on it).
- Scale s = display px per source px: hero 6.0 (push to 6.36 by 7.5 s), pull-back 6.0→2.5 (9.6–12.0), tray 2.5, push-in 2.5→6.0 (26.667–28.333).
- **Turntable:** the whole table rotates about the hero centre (S1 −4°→+2°, S2 +2°→+6°), then rolls back +6°→0° during the pull-back so the tray lands square. Because the light stays fixed while the table turns, the highlights crawl realistically.
- **Render order per frame:** warp the source maps (L, A, M, h; §7.1) into screen space at the frame's scale, rotation and offset (INTER_AREA when shrinking, INTER_CUBIC when enlarging), then relight in screen space. Multiply screen-space height gradients by s so slopes stay in source-px units (the model is scale-invariant).
- **S8–S9, 3/4 view:** Three.js PerspectiveCamera, vertical fov 24°, aspect 0.5625, `up = (0,0,1)`, position (0, −sin34°·D, cos34°·D) with D = 4150 (tilt 34° from vertical), `lookAt(0,0,0)`, `setViewOffset(1080,1920, 0, −(coinY−960), 1080,1920)` with coinY = 1010 (S8) → 1110 (S9). The table is a 1080×1000 plane carrying the per-frame relit hero texture. The orbit rotates the camera about the z axis.

### 2.5 Optional soundbite slots (the film is complete without them)

- **Slot A** at 15.000 (after the price war, before the frontier). **Slot B** at 43.333 (after the changed mind, before zero trust). Each takes 6–10 s and pushes everything after it later by that amount.
- **Look:** the coin world stays lit at 15% intensity (the lamp waits; nothing is cut). A 16:9 window 888×500 sits at (96,640) with a 1 px hairline frame (ink-1 at 20%). Above it, Geist Mono 16 px #6B655D at (96,610): 原声 · 20VC · 2026.10.26. Subtitles in D3 (52/76, ink-1) at (96,1172), at most 2 lines. The gauge reads "—".
- **Exit:** the window fades in 320 ms (T-OUT curve); the lamp returns to full over 8 frames.
- **Audio:** LAMP and PAD duck −12 dB under dialogue (attack 120 ms, release 400 ms).
- **Rule:** subtitles in a slot are a translation of his actual audio and are labelled 原声字幕（翻译）. Paraphrase elsewhere stays paraphrase.

---

## 3. Carousel (1080×1440, 7 frames)

**Grid:** margins 96 (measure 888), 6 columns of 128 + 24 gutters, 4 px baseline. Rails: IDX top-left at (96,112); GAUGE right-aligned to 984, top 104. Text zone y 176–420; stage 420–1190; captions 1190–1300; footer row y 1336: BRAND-S (Noto Sans SC 700, 30/36, 11 px violet dot) at x 96, and the page number (Geist Mono 400, 18/24, ink-3) right-aligned to 984. Every body line is ≥ 44 px; only captions and credits are smaller. Finishing uses the same `look.json` with weave 0.

| # | Layout (coordinates are top-left) | Exact copy | Asset · crop · treatment |
|---|---|---|---|
| **1 Cover** | K (96,132) 30/40. D1-C (96,180) 148/164, two lines. Coin centred (600,870). C1 (96,1196), C2 (96,1232). GAUGE. Footer 01 / 07 | 微软 CEO 纳德拉判断<br>大模型<br>要打价格战了<br>古希腊钱币，庞贝出土<br>照片：布鲁克林博物馆　本片重新打光 | Hero #23 at 6.0× (⌀336), az 160°, el 6°, 3200 K, felt pool 1.35R/3.1R/×1.45 |
| **2 价格战** | IDX 01 价格战. K (96,184). D2-C 48/72 three lines (96,230). Tray (60,470) 960×757. C1 (96,1252). GAUGE 顺光 84° 5600K. Footer 02 / 07 | 他判断<br>大多数企业场景的日常算力，/ 终将商品化；/ 模型层，会有一场残酷的价格战。<br>顺光下，24 枚各不相同的古币，看起来都差不多。 | Tray at 2.5×, el 84°, 5600 K, pool 0.30W/0.62W, 92 px feather |
| **3 前沿** | IDX 01 价格战. K (96,184). D2-C 56/80 (96,230). Plate (329,430) 422×686. C1 (329,1136), C2 (329,1172). No gauge. Footer 03 / 07 | 他判断<br>最前沿的模型，/ 只会服务少数顶尖场景。<br>猎鹰 9 号与 DSCOVR 卫星，发射前，2015<br>照片：SpaceX　公有领域 | Rocket, same crop as S4, at 1.70× |
| **4 混用** | IDX 02 混用. K (96,184). D2-C 48/72 (96,230). DAYS 30/40 (96,404), 四 lit. Tray (0,470) 1080×852 with two pools; TAGs 44 px with leaders. GAUGE 追光 36°. Footer 04 / 07 | 据报道<br>微软 Copilot 内部，每天都在混用 / 便宜的闭源模型和开源模型。<br>一 二 三 四 五 六 日<br>闭源 · 开源 | Dark tray (ambient 0.035) with two spots: coins src (155,50) 闭源 and (270,118) 开源. Read it as one day, long exposure |
| **5 私有评测** (the save-worthy frame) | IDX 03 私有评测. K (96,184). D2-C 48/72 (96,230). Diptych: two 470×445 cells at (64,420) and (546,420) with a radial mask (closest-side, 62%→100%); 1 px hairline divider x 540, y 470–990. Under each, L head (120 / 602, 876) and C1 (940). OURS block (96,1040): tag 26 px, D3 44/64 three lines. Footer 05 / 07 | 纳德拉认为<br>每家公司，都会有自己的私有评测。/ 那会是它的核心 IP。<br>顺光 · 公开榜单　EL 84°　5600K<br>侧光 · 你的私有评测　EL 05°　3000K<br>● 我们的理解<br>公开榜单像顺光，模型看起来都差不多；/ 私有评测是你自己的侧光，/ 照出你在乎的差别。 | The same coin twice at 5×: left el 84°, 5600 K, pool 1.9R/3.8R; right el 5°, az 170°, 3000 K. Same crop, same scale; only the light differs |
| **6 改变的看法 · 零信任** | IDX 04 改变的看法　零信任. K (96,176). D3 44/64 two lines (96,220). Hubble strip (96,372) 888×120. C2 (96,500). Glass shot, coinY 708, D 6000. K (96,880). D3 44/64 (96,924). Three L rows 44/60 at y 1072, 1132, 1192. Footer 06 / 07 | 被问到改变过什么看法<br>他以前以为，规模够大，对齐自然会来。/ 现在，他不这么想了。<br>哈勃极深场，2012　照片：NASA<br>他说<br>微软不等对齐问题解决，/ 先给模型套上零信任架构。<br>身份　每个 agent 都有自己的身份<br>记录　每一次工具与模型调用都留下记录<br>权限　规则放在模型之外 | Hubble src (120,361)–(880,463) at 1.168×; hero under glass at 3/4 (as S8) |
| **7 我们的理解** | OURS (96,132): tag 30 px + D2-C 56/80 title. Three items at y 380, 576, 772: Geist Mono numeral (96,y+14) 22 px ink-2; D3 44/64 at (160,y); a 1 px hairline above each (y−26). Closing D3 44/64 ink-2 at (96,948). Coin (masked) at (580,790). C2 credits 18/28 at (96,1240). Footer 07 / 07 | ● 我们的理解<br>给出海团队的三件事<br>1 接入多家模型，按任务路由，/ 别绑死一家。<br>2 用你自己的数据和标准，/ 建一套私有评测。<br>3 给每个 agent 身份，调用全记录，/ 权限放在模型之外。<br>模型，人人都买得到；/ 看它的角度，只有你有。<br>来源：20VC 播客，Harry Stebbings 对话 Satya Nadella，2026.10.26 发布。观点据公开报道转述，非原话。<br>图片：布鲁克林博物馆（本片重新打光）、SpaceX、NASA。 | Hero at 5×, el 12°, az 150°, 3200 K, radial mask |

**Cover as a thumbnail** (`proof/_cover_thumbnail_test.jpg`): in a 2-column feed (tile ≈ 350 px at 2×, 175 px at 1×) the title reads first (≈ 48 px glyphs at 2×), the coin second: it is the only warm, bright mass in the frame. The near-black field stands out among bright pastel covers. Frame 5 doubles as the most shareable page: the whole argument fits in one diptych.

---

## 4. Design system

### 4.1 Grid

| | Film 1080×1920 | Carousel 1080×1440 |
|---|---|---|
| Margins / measure | 96 / 888 (x 96–984) | 96 / 888 |
| Columns | 6 × 128, gutters 24 | same |
| Baseline | 4 px; all leadings are multiples of 4 | same |
| Rails | IDX (96,222); GAUGE right edge 984, top 220 | IDX (96,112); GAUGE top 104 |
| Zones | text 296–744 · stage 744–1380 (object centre y 1040) · captions 1384–1480 · **≥ 1498: feed UI, nothing essential** | text 176–420 · stage 420–1190 · captions 1190–1300 · footer 1336 |

Text is always left-aligned at x 96 (or 124 inside an OURS block). Objects are centred on x 540: the product-film convention, text on the margin and object on the axis. Captions align to the left edge of the plate they describe.

### 4.2 Typefaces

| Role | Family | Weights used |
|---|---|---|
| All Chinese | **Noto Sans SC** | 400 (statements, captions), 500 (display, kickers, tags, label heads), 700 (brand only) |
| Latin inside Chinese lines (token, CEO, API, Copilot, IP, agent, 2015) | **Inter Tight**, via the stack `"Inter Tight", "Noto Sans SC"` | same weight as the line; `font-variant-numeric: tabular-nums` in captions |
| Instruments (gauge numbers, index numerals, page numbers) | **Geist Mono** | 400, 500 |

Deliberately unused: every serif (Noto Serif SC, EB Garamond and the rest belong to an editorial voice; this film speaks like a keynote super), plus WenKai, ZCOOL, Anton and Instrument Serif. One sans voice, quiet and precise.

### 4.3 Type scale (px)

| Token | Size / leading | Weight | Tracking | Colour | Use |
|---|---|---|---|---|---|
| D1 | 132 / 148 | 500 | +0.005em | ink-1 | hook title only |
| D1-C | 148 / 164 | 500 | +0.005em | ink-1 | carousel cover title |
| D2 | 64 / 88 | 400 | +0.02em | ink-1 | his statements, our closing line |
| D2-C | 56 / 80 (48 / 72 for long lines) | 400 | +0.02em | ink-1 | carousel statements |
| D3 | 52 / 76 (carousel 44 / 64) | 400 | +0.02em | ink-1 or ink-2 | general fact, our reading |
| L | 44 / 60 | head 500 ink-1, body 400 ink-2, gap 0.75em | +0.02em | | zero-trust labels |
| TAG | 44 / 52 | 500 | +0.04em | ink-1 | 闭源 / 开源 |
| K | 32 / 44 (carousel 30 / 40) | 500 | +0.08em | ink-2 | attribution kickers |
| OURS tag | 30 / 40 (carousel 26) | 500 | +0.06em | violet-t #A98DFF, dot 12 px #5B2EFF | 我们的理解 |
| DAYS | 32 / 40 | 400 | +0.62em | ink-3, current day ink-1 | weekday row |
| C1 | 24 / 32 | 400 | +0.02em | ink-2 | plate caption |
| C2 | 20 / 28 (carousel 18 / 28) | 400 | +0.02em | ink-3 | credit / source |
| IDX | Geist Mono 500 18/24 +0.06em ink-3, then Noto Sans SC 400 22/24 +0.06em ink-2 | | | | chapter slate |
| GAUGE | name: Noto 400 22/28 +0.06em ink-2; readout: Geist Mono 400 16/20 +0.06em ink-3 | | | | light gauge |
| BRAND | 40 / 48 (carousel 30 / 36) | 700 | +0.01em | ink-1, dot 14 px (11 px) | account mark |

### 4.4 Typographic rules

1. **Three voices.** His content always has a K kicker above it at (96,300). General facts start at (96,300) with no kicker. Our reading always sits in an OURS block: a 2 px #5B2EFF rule from the tag's top to the last line's baseline at x 96, with text at x 124.
2. **CJK–Latin spacing:** U+2005 (¼ em) at every script boundary, inserted automatically. **Exception: the account name is always exactly `Coo-Coo出海Ai实验室`, with no inserted spaces.**
3. **Line breaks are set by hand** (shown with "/" in the copy deck). No line begins with punctuation. D1 lines carry no punctuation; D2 and D3 keep full-width ，。：；
4. Never more than 3 lines in a D2 block, never more than 2 blocks visible at once (the older one dimmed to 0.38).
5. No text over a bright area of any photograph: text lives in the void.

### 4.5 Colour tokens

| Token | Hex | Use |
|---|---|---|
| void | `#0A0908` | the world; also the render floor (no pixel darker than void) |
| ink-1 | `#F1ECE3` | primary type (≈ 16:1 contrast on void) |
| ink-2 | `#A49D92` | kickers, secondary lines, label bodies, C1 |
| ink-3 | `#6B655D` | credits, gauge readout, inactive days |
| hair | `rgba(241,236,227,.20)` | 1 px rules |
| tungsten | `#FFC98F` | gauge dot when K < 4500 (glow at 22%) |
| daylight | `#CFE0FF` | gauge dot when K ≥ 4500 |
| violet | `#5B2EFF` | **only** the OURS dot and rule, and the brand dot |
| violet-t | `#A98DFF` | **only** the 我们的理解 tag text |
| glass-edge | `rgba(250,248,240,.26–.70)` outer, `rgba(170,214,192,×0.55)` inner | glass case edges |

### 4.6 Grade (LUT-equivalent)

The coin world is graded *by the light* rather than afterwards. Its sources are monochrome, so all colour comes from the Kelvin tint × a metal tint (1.00, 0.96, 0.905):

| K | tint (r, g, b) |
|---|---|
| 2700 | 1.00, 0.82, 0.63 |
| 3000 | 1.00, 0.86, 0.71 |
| 3200 | 1.00, 0.885, 0.745 |
| 4300 | 1.00, 0.94, 0.87 |
| 5600 | 0.93, 0.96, 1.00 |
| 6500 | 0.88, 0.93, 1.00 |

Interpolate between rows in mired (1e6/K).

Then, in order:

- **Lift / gamma / gain.** Floor at void, plus a +0.006 lift in finishing. Gamma 1.00 for the coin world and 0.96 for the rocket and Hubble plates. Gain 1.00. Highlights pass through a soft shoulder, `x/(1+0.12x)` in the plate stage and film.py's shoulder from 0.85 in finishing.
- **Saturation.** Rocket 0.85, Hubble 0.80; coin world as tinted.
- **Split-tone.** Shadows sit on the warm-neutral void. Highlights carry the light's own temperature: warm 3000–3200 K or cold 5600 K, never both in one frame. No teal-orange, and no violet in the image.

### 4.7 Film texture (`kit/look.json`, consumed by the existing `f2/film.py`)

```json
{"default": {"grain": 0.042, "grain_size": 1.25, "grain_chroma": 0.18, "halation": 0.16, "hal_thresh": 0.74, "hal_radius": 22,
             "bloom": 0.05, "bloom_radius": 56, "ca": 0.0008, "vignette": 0.24, "vig_round": 0.85, "weave": 0.25,
             "flicker": 0.0, "lift": 0.006, "gain": 1.0},
 "keys": [{"t": 14.99, "flicker": 0.0}, {"t": 15.0, "flicker": 0.004}, {"t": 19.99, "flicker": 0.004}, {"t": 20.0, "flicker": 0.0}]}
```

Grain is luminance-weighted, so it is quiet in the void (no codec mush) and alive on lit metal. Carousel: the same values with weave 0 and grain 0.036. The proof stills use the default block with weave 0.

### 4.8 Micro-detail system

1. **Light gauge (光位)**, the film's one instrument. A 58 px SVG: outer ring r 27, 1 px, ink-1 at 32%; inner ring r 13.5 at 10%; a 4 px north tick; the light dot (r 3.6) with a halo (r 9, 22%) in tungsten or daylight, placed at (cos az, −sin az)·cos(el)·27; a 1 px line from the centre to the dot at 55%. To its left, right-aligned: the lighting name (侧光 when el < 20°, 追光 for a moving spot, 顺光 when el > 60°; 200 ms crossfade) and the readout `EL 06°  3200K`. It updates every frame from the rig and fades out (200 ms) over photographs that bring their own light (S4, S7) and in S10.
2. **Chapter slate (IDX):** 01 价格战 / 02 混用 / 03 私有评测 / 04 改变的看法 / 04 零信任. It changes with a 1-frame cut, like a slate, never animated.
3. **Plate captions:** C1 says what the object is; C2 says who made the photo and what we did to it. Every coin caption carries 本片重新打光.
4. **The violet appears in two roles only:** our reading and the brand. Nowhere else, ever.
5. **Hairlines:** 1 px `hair`, drawn left→right (scaleX 0→1, 400 ms, ease-camera). Used for the case-label rule (S8), carousel item separators and the diptych divider.
6. **Tags (S5):** see §2.3. Leaders are 1 px at 55% ink-1.
7. **Weekday row:** the current day switches hard on each landing; no transitions.
8. **Glass details:** float-green inner edges, a 1 px meniscus line above the contact seam, one caustic line, two 1.3 px dust specks visible only inside the reflection streak.

---

## 5. Motion language

### 5.1 Clock
72 bpm. Cuts, light landings and statement entries sit on beats (25 frames) or half-beats. Light motion is slower than text motion: the light is heavy, the type is light.

### 5.2 Easing tokens

| Token | Curve | Character |
|---|---|---|
| ease-light | cubic-bezier(0.45, 0, 0.2, 1) | a motorised lamp head with mass: slow start, long settle |
| ease-camera | cubic-bezier(0.65, 0, 0.35, 1) | symmetric dolly / crane |
| ease-servo | cubic-bezier(0.34, 1.36, 0.64, 1) | spot landing with ≈ 3% overshoot |
| ease-glass | cubic-bezier(0.22, 1, 0.36, 1), then spring ω 18 rad/s, ζ 0.62 | weight settling onto felt |
| type-in | cubic-bezier(0.16, 1, 0.3, 1) | expo out |
| type-out | cubic-bezier(0.7, 0, 0.84, 0) | expo in |
| drift | cubic-bezier(0.33, 0, 0.67, 1) | plate push-ins |

### 5.3 Durations and stagger
Text in 700 ms (opacity done in 400). Text out 320 ms. Dim 500 ms. Light moves 1.0–2.5 s. Camera moves 1.667–2.4 s. Spot hop 380 ms. Glass descent 1.2 s + 0.24 s settle. Stagger: lines 90 ms apart; the kicker leads the first line by 160 ms; the OURS rule leads its tag by 120 ms; labels 600 ms apart.

### 5.4 Text
- **T-IN:** opacity 0→1 (400 ms), translateY +14→0 px (700 ms), and tracking from rest+0.06em to rest (900 ms), all type-in. The settling tracking gives the keynote-super quality.
- **T-OUT:** opacity→0 and translateY 0→−8 px, 320 ms, type-out.
- **T-DIM:** opacity→0.38, 500 ms, ease-light.
- Captions fade in only (600 ms linear, 300 ms after the plate settles).
- **Never:** per-character typing, blur-in, scale-in, bounce, or masks sliding over text.

### 5.5 Photographs and camera
- Coin world: turntable ≤ 10° per shot; push ≤ 6% per shot; pull-back and push-in between hero and tray as single continuous moves.
- Plates: push ≤ 5% (rocket) and ≤ 8% (Hubble); drift ≤ 12 px; never diagonal (no Ken Burns).
- **No fake parallax** on any photograph. The only real depth in the film is the 3D table and glass in S8–S9, and the light.

### 5.6 Transitions
- **Light cut** (the default between worlds): intensity→0 in 4 frames (type-out), 0–2 frames of void, the next light up in 8 frames (type-in). Used at 14.85, 19.667, 36.3, 43.0 and 55.0.
- **Continuous** inside the coin world (S1→S2→S3, S5→S6→S6b, S8→S9): the camera moves, nothing cuts.
- **Hard stop** (S7, 40.833): motion dies in 4 frames while the sound drops to digital silence.
- **Never:** crossfades between photographs, wipes, zoom-blur, glitch, light-leak transitions.

### 5.7 Signature moves (portfolio grade)
1. **The Flattening (S3a, reprised in S6b).** One lamp rises from 10° to 84° and cools from 3200 K to 5600 K. A 2,000-year-old face dissolves into a grey disc while the gauge dot slides to its centre and the hum turns to fluorescent buzz. Commoditisation shown by physics. (`proof/_flattening_strip.jpg`)
2. **Your Angle (S6, reprised in S6b).** The reverse, timed so that 那会是它的核心 IP。 lands on the frame where the light reaches 5°. The face returns sharper than in the hook, with a chord bloom and a glint on its edge.
3. **The Glass (S8).** A case you cannot see until the light finds it: edges catch the lamp on the way down, a damped touchdown with a pneumatic seal, then one reflection streak crosses the top and lights two specks of dust. The three labels sit outside the glass, on the case's label plate.

---

## 6. Sound design (all synthesised; 48 kHz, float32, stereo)

### 6.1 Instruments (built on `f2/synth.py`)

| Name | Recipe | Peak level |
|---|---|---|
| LAMP (warm filament) | sum of `sine` at 100 / 200 / 300 / 400 Hz with amplitudes 1 / .45 / .22 / .10; slow AM ±6% (noise low-passed at 0.3 Hz); blockwise `lp` at 600 + 2400·intensity Hz; level follows the LX intensity (dB = −40 + 20·log10 I) | −40 dBFS |
| FLUORO (cold, flat) | odd harmonics of 120 Hz (120 / 360 / 600 / 840 at 1 / .33 / .2 / .14) + `bp(noise, 2000, 4000)` × 0.08; random AM 0.8% (noise low-passed at 8 Hz) | −42 |
| SERVO | `saw_additive(f(t), partials=12)` with f = 180 + 60·speed → `bp(200, 1600)`, plus `bp(pink, 800, 3000)` × 0.3; amplitude = normalised angular speed of the light | −36 at full speed |
| RELAY | `tick(3100, 0.018, 0.6)` + `sine(900)`·`env_exp(0.06, 0.04)` + a 2 ms `noise` burst | −20 |
| GLINT | `fm_bell(f, dur=1.6, ratio=3.5, decay=0.9)` with index 4→0 over 0.35 s (extend `fm_bell` with an index envelope); f = E7 2637 Hz or B6 1975.5 Hz | −26 (soft −32) |
| THOOM | `sub_hit(dur=2.2, f0=62, f1=44, decay=0.7)` + `tick(1200, 0.01, 0.3)` | −10 |
| PAD | `drone(freq, dur, voices=5, spread_cents=9, cutoff=900, lfo=0.07)` per chord tone. Dmaj9 = D3 A3 C#4 E4 F#4; Bm7 = B2 D3 F#3 A3; Gmaj7(#11) = G2 D3 F#3 B3 C#4 (wide: spread 12 cents) | −30 (S4 −24) |
| KEY | `felt_piano(freq, dur=4, vel, bright=0.45)`. Motif F#5–E5–D5–A4; S5 ostinato A4 (闭源) / D5 (开源) | −20 to −30 |
| BLOOM | KEY D4 A4 E5 F#5 A5, strummed 30 ms apart, vel .35, + PAD Dadd9 swell over 0.6 s | −18 |
| FLOOD HUM | 50 / 150 / 250 Hz sines (1 / .3 / .1), `lp` 400 Hz | −46 |
| AIR / SPACE BED | `pink` → `lp` 800 Hz (AIR); `pink` → `sweep_bp(400→2400, q=4)` over 4.2 s (SPACE) | −42 / −40 |
| BELLS | `fm_bell` A5 880, E6 1318.5, B6 1975.5 (ratio 2.0, index 0.6, decay 3.0), staggered 0 / 0.6 / 1.2 s | −28 |
| WHOOSH | `whoosh(dur=1.0, f0=300, f1=1200, peak=0.6)` | −30 |
| SEAL | `sine(120)`·`env_exp(0.06)` + `tick(1800, 0.012, 0.5)` | −20 |
| GLASS TICK | `fm_bell(5200, ratio=2.76, index=1.2, decay=0.4)` | −34 |
| TICK / LED | `tick(4200, 0.03, 0.4)` / `tick(4000, 0.03, 0.2)` | −30 / −36 |
| Reverb | `reverb_ir(dur=3.2, predelay=0.022, damp=4500)`. Sends: GLINT 30%, KEY 22%, PAD 15%, TICK 10%, RELAY 6%, LAMP / FLUORO / SERVO 0% (the lamp is close) | |

### 6.2 Cue sheet

| t (s) | frame | Shot | Cue |
|---|---|---|---|
| 0.000 | 0 | S1 | THOOM; LAMP in (400 ms); PAD Dmaj9 (attack 1.5 s) |
| 0.533 | 16 | S1 | GLINT E7, pan −0.25 (light crosses the crest) |
| 3.333 | 100 | S2 | KEY A4 vel .30, −28 |
| 5.000 | 150 | S2 | GLINT B6 soft, pan +0.2 |
| 7.500 | 225 | S3a | SERVO follows LX4; PAD → Bm7 and thins over 2.5 s |
| 8.000–9.600 | 240–288 | S3a | LAMP → FLUORO crossfade |
| 11.250 | 338 | S3b | KEY F#5, D5, B4 at +0 / +0.28 / +0.56 s, vel .32, −24 |
| 14.850 | 446 | S3b | RELAY; FLUORO cut |
| 15.000 | 450 | S4 | PAD Gmaj7(#11) (attack 0.8 s); FLOOD HUM; AIR swell 0→1 over 3 s |
| 19.667 | 590 | S4 | all S4 layers fade out over 0.333 s |
| 20.000 | 600 | S5 | LAMP in (spot) |
| 20.417 → 26.250 (8×, every 0.833 s) | 613, 638, 663, 688, 713, 738, 763, 788 | S5 | RELAY (pan = 0.6·(x−540)/540), plus KEY A4 on 闭源 / D5 on 开源 for landings 1–7, vel .25, −30; SERVO between landings |
| 28.333 | 850 | S6 | SERVO glide 240→160 Hz |
| 29.583 | 888 | S6 | BLOOM; GLINT E7, pan −0.15; FLUORO → LAMP |
| 32.000 | 960 | S6b | LAMP → FLUORO (120 ms); PAD high-pass to 180 Hz |
| 34.167 | 1025 | S6b | FLUORO → LAMP (120 ms); small BLOOM (D4 A4 E5, vel .3, −24); GLINT soft |
| 36.300 | 1089 | S6b | everything fades over 0.333 s |
| 36.667 | 1100 | S7 | SPACE BED; BELLS |
| **40.833** | 1225 | S7 | **digital silence on every bus for 0.42 s** |
| 41.250 | 1238 | S7 | KEY D3 (146.83 Hz) vel .45, 5 s decay, −22 |
| 43.333 | 1300 | S8 | LAMP in |
| 43.700 | 1311 | S8 | WHOOSH |
| 44.900 | 1347 | S8 | SEAL |
| 45.450 | 1364 | S8 | GLASS TICK, pan +0.1 |
| 45.800 / 46.400 / 47.000 | 1374 / 1392 / 1410 | S8 | TICK ×3, pan −0.2 |
| 45.000 → 48.333 | 1350 → 1450 | S8 | PAD Bm7 → Gmaj7 |
| 50.833 | 1525 | S9 | MOTIF F#5 E5 D5 A4 at +0 / +0.42 / +0.84 / +1.26 s, vel .40, −20; PAD Dmaj9 |
| 55.000 | 1650 | S10 | RELAY; LAMP cut; PAD tail 2.5 s |
| 55.400 | 1662 | S10 | LED tick |
| 57.833–58.333 | 1735–1750 | S10 | silence |

### 6.3 Mix and delivery
Integrated loudness −16 LUFS, true peak −1.0 dBTP (look-ahead limiter, no audible pumping), high-pass at 28 Hz on the master. 48 kHz / 24-bit WAV, then AAC 256 kbps at mux. The film is silent-text plus score, with no voice-over, as the account requires.

---

## 7. Asset treatment recipes

### 7.1 `coins.png` (384×303, grey): the hero

**Segmentation** (scikit-image's own recipe for this test image): elevation = `sobel(im)`; markers bg < 0.25, coin > 0.55; `watershed`, `binary_fill_holes`, `label`; drop regions < 300 px. That gives 24 coins. Refer to coins by **centroid**, which is stable, rather than by label id.

**Hero coin:** centroid (45,259), bounding box (18,233)–(75,288), ⌀ ≈ 56 px. It reads as a helmeted head in profile (Athena-type iconography). We **never name the figure**: the archive photograph does not identify individual coins, so the caption only says 古希腊钱币，庞贝出土.

- Crop (0,214)–(94,303) (94×89 src px). Mask = this coin's label only; neighbours replaced by synthetic felt.
- Embed the crop centred in a **1080×1000 synthetic-felt canvas** at 6× (felt L = 0.055).

**Tray:** the full frame (0,0)–(384,303). Maps at 3× (1152×909) for the carousel, and at 6× (2304×1818) as the source for the film's pull-back and push-in. Display 2.5×. Edge feather 110 px at 3× (92 px on screen). The real cloth is kept, darkened by the relight's cloth term.

**Maps** (computed once, at the map scale s; stored as 16-bit PNG):
```
L  = clip(resize(crop, ×s, cubic))                         # luminance
M  = smoothstep(.35,.65, blur(resize(mask, ×s, linear), .7s))
A  = blur(L, 5s)                                           # patina / albedo
h  = blur( (0.22·smoothstep(0, 2.2, edt(M>.5)/s) + 0.55·(blur(L,.9s) − blur(L,4.5s))) · M , .6s )
gx, gy = gradient(h) · s                                   # slope per source px
felt slopes: n = N(0,1); n = .6·blur(n,.8) + 1.4·blur(n,2.2); fgx, fgy = gradient(n)·.35   # display-res microtexture
```

**Relight**, per pixel (screen space, y down; `kit/relight.py → Plate.render`):
```
l̂ = (cos az, −sin az); e = max(el, 2°)
facing = −(gx·l̂x + gy·l̂y)
r   = clamp(1 + min(cot e, 9)·2.2·facing, 0, 3)                    # relief contrast ∝ cot(el)
sh  = soft height-field shadow toward the light (el < 40°): H = h·s·6; for step = 2,4,…,10s:
      sh = min(sh, clamp(1 − (H(x + step·l̂) − H − step·tan e)·0.8, 0, 1))
k   = 0.35 + 0.65·smoothstep(80°, 30°, el)                         # baked photo shading fades as the light goes frontal
base = A + (L − A)·k
n̂ = normalize(−gx, −gy, 1); ĥ = normalize(l + v), v = (0,0,1)
spec = (n̂·ĥ)^90 · 1.1 · sh · smoothstep(.35,.8,L) · smoothstep(70°,20°,el)
expo = I · (0.92 − 0.16·smoothstep(30°, 85°, el))
coin = (base·r·(0.30 + 0.70·sh))·metal·tint(K) + spec·tint(K)        metal = (1, .96, .905)
cloth = (0.42·cloth_src + 0.012)·clamp(1 + min(cot e,9)·0.9·(−f∇·l̂), .2, 2.2)·(.95,.93,.90)·tint(K)·(0.55 + 0.45·smoothstep(60°,10°,el))
out = (coin·M + cloth·(1−M))·expo · pool                              # pool: elliptical, stretched ×s along l̂, smoothstep(r1, r0, d)
out = out/(1 + 0.12·out); floor at void
```

**GLSL port** (optional speed-up; same math; textures uploaded with flipY = false so uv (0,0) is top-left; screen y down):
```glsl
uniform sampler2D uMaps;   // R = L, G = A, B = M
uniform sampler2D uH;      // R = h
uniform vec2 uTexel; uniform float uS, uAz, uEl, uI, uAmb; uniform vec3 uTint; uniform vec4 uPool; uniform float uStretch;
varying vec2 vUv;
float ss(float a,float b,float x){float t=clamp((x-a)/(b-a),0.,1.);return t*t*(3.-2.*t);}
void main(){
  vec3 m=texture2D(uMaps,vUv).rgb; float L=m.r,A=m.g,M=m.b;
  float h=texture2D(uH,vUv).r;
  vec2 g=vec2(texture2D(uH,vUv+vec2(uTexel.x,0)).r-texture2D(uH,vUv-vec2(uTexel.x,0)).r,
              texture2D(uH,vUv+vec2(0,uTexel.y)).r-texture2D(uH,vUv-vec2(0,uTexel.y)).r)*0.5*uS;
  float a=radians(uAz), e=radians(max(uEl,2.)); vec2 l2=vec2(cos(a),-sin(a));
  float r=clamp(1.+min(1./tan(e),9.)*2.2*(-dot(g,l2)),0.,3.);
  float sh=1.; if(uEl<40.){ float H0=h*uS*6.;
    for(int i=1;i<=12;i++){ float st=float(i)*uS*0.84; float Hs=texture2D(uH,vUv+l2*st*uTexel).r*uS*6.;
      sh=min(sh,clamp(1.-(Hs-H0-st*tan(e))*0.8,0.,1.)); } }
  float base=A+(L-A)*(0.35+0.65*ss(80.,30.,uEl));
  vec3 n=normalize(vec3(-g,1.)), l=vec3(cos(e)*l2,sin(e)), hv=normalize(l+vec3(0,0,1));
  float spec=pow(max(dot(n,hv),0.),90.)*1.1*sh*ss(.35,.8,L)*ss(70.,20.,uEl);
  vec3 coin=base*r*(0.3+0.7*sh)*vec3(1.,.96,.905)*uTint+spec*uTint;
  vec3 felt=vec3(.95,.93,.90)*uTint*(0.42*A*(1.-M)+0.012)*(0.55+0.45*ss(60.,10.,uEl));
  vec3 c=mix(felt,coin,M)*uI*(0.92-0.16*ss(30.,85.,uEl));
  vec2 d=vUv-uPool.xy; float dist=length(vec2(dot(d,l2)/uStretch,dot(d,vec2(-l2.y,l2.x))));
  c*=uAmb+(1.-uAmb)*ss(uPool.w,uPool.z,dist); c=c/(1.+0.12*c);
  gl_FragColor=vec4(max(c,vec3(.039,.035,.031)),1.);
}
```
The reference path is Python: `kit/relight.py` reproduces every proof exactly. Use the GLSL port only if render time matters, and validate it against the proofs at el 5° and 84°.

### 7.2 `rocket.jpg` (640×427)
- Crop (196,24)–(444,427), 248×403, the vehicle centred. Bicubic **2.0×** → 496×806.
- Graduated ND: multiply by 2^(−1.3·(1 − smoothstep(0, 0.62, y/H))), so the sky is −1.3 stops at the top and untouched from 62% of the height down.
- Saturation 0.85; gain 1.06; black −0.012.
- No mask and no relight: the pad lights are real, and finishing halation (threshold 0.74) blooms them warm.
- Max on-screen scale 2.1× (end of the push).

### 7.3 `hubble_deep_field.jpg` (1000×872)
- Crop (120,86)–(880,786), 760×700, at **1.1684×** → 888×818, exactly the measure.
- Saturation 0.80; black point 0.02 (rescale (c − 0.02)/0.98).
- Push to 1.08 gives a maximum of 1.262×.
- Carousel strip: source (120,361)–(880,463) at 1.1684× → 888×120.

### 7.4 Synthetic elements (never captioned as photographs)
- **Felt:** a constant 0.055 with display-resolution microtexture whose relief follows the same cot(el) term, so fibres appear only under grazing light. It is the stage, not a subject.
- **Glass case** (`kit/proof.html → glassScene`): a 460×460×190 box, wall 6, projected with the scene camera and drawn in a 2D overlay. Layers, in order:
  1. Cast shadow on the felt: a linear gradient, 26% → 0, blur 34 px, falling right/back.
  2. Far edges seen through two walls: 1 px at 15%, float-green.
  3. Front wall Fresnel gradient: 2.5% → 5%, plus a 10% reflection band at 90% height.
  4. Top glass: a radial reflection of the soft box (13% → 0, r 330 px, centred back-left), the moving streak (peak 17%, ±120 px), and two dust specks.
  5. Caustic: 2 px at 18%, blur 7, just inside the far right wall.
  6. Contact seam: 2.4 px black at 70%, plus a 1 px meniscus at 30%.
  7. Every edge drawn as two lines: outer 1.3 px warm white at 26–70% by facing, inner 1 px float-green at 55% of that.
  8. The hot front-top segment: 2 px at 95% with a 12 px bloom; it travels with the streak.

  No frosted blur anywhere: this is glass, not glassmorphism.

### 7.5 Maximum display sizes

| Asset | Crop (src px) | Normal | Maximum | Where |
|---|---|---|---|---|
| coins.png, hero #23 | (0,214)–(94,303) | 6.0× (⌀336) | 6.5× (S2 ends at 6.36×) | S1–S3a, S6–S6b, S8–S9 (3D), C1, C5–C7 |
| coins.png, tray | (0,0)–(384,303) | 2.5× (960×757) | 2.81× (carousel 4 only) | S3b, S5, C2, C4 |
| rocket.jpg | (196,24)–(444,427) | 2.0× | 2.1× | S4; C3 at 1.70× |
| hubble_deep_field.jpg | (120,86)–(880,786) | 1.168× | 1.262× | S7; C6 strip |

### 7.6 Unused, on purpose
- **coffee.png:** a lovely product shot, but it would be a second metaphor for 日常; flat light on coins already says it.
- **earth-night / blue-marble / topology:** the obvious global-compute image, the globe cliché, and the previous film already owns "as cheap as electricity".
- **astronaut / grace_hopper:** real people; using their portraits as stand-ins for AI agents would be disrespectful and confusing.
- **camera / clock / moon / text / retina:** each would be a one-word illustration (camera = log, retina = identity). The glass case says identity, log and permission in one object.
- **HDRIs:** the glass reflects our own key light, not an environment.

---

## 8. Risks, and how we avoid looking AI-made or cheap

| Risk | Mitigation |
|---|---|
| **The coin is 56 px.** At 6× it is soft | It is never shown above 6.5× and never fills the frame. Its softness is motivated (a macro under a lamp, shallow focus). Detail perception comes from what we control at full resolution: moving speculars, cast shadows, sharp felt fibres beside the coin, and grain. Captions disclose the relight. If a reviewer still finds it soft, drop the hero to 5× (⌀280) and keep everything else |
| The relight looks like an emboss filter | Low gain (k 2.2, cot clamped at 9), height blurred 0.6s, no outline ringing, speculars gated to bright metal and to el < 70°, soft multi-step shadows, Kelvin tint instead of grey. Always check el 5° and el 84° side by side: if edges ring, raise the height blur to 0.9s |
| Monotony: coins for about 60% of the runtime | Four distinct coin rooms (single macro, flat tray, dark tray with a moving spot, 3/4 under glass). Two out-of-world plates at 15 s and 36.7 s. Temperature swings, a camera that turns, pulls, pushes and tilts, and a score that changes texture with the light |
| The metaphor overreaches (eval = light angle) | It is always labelled 我们的理解 and set in the violet voice. His words are always the plain line above. The image demonstrates; it does not attribute |
| The glass reads as glassmorphism UI | It is a 3D object in perspective, with wall thickness, a contact seam, a caustic and a physical descent. Transparency 3–7%; no frosted blur, no rounded panel |
| The gauge reads as HUD junk | One 58 px instrument that reports a real, visibly changing variable, and hides whenever it would mean nothing |
| "Dark + sans = generic AI promo" | Everything that signals AI promo is absent: no gradients, glows or particles, no centred everything, no neon. Present instead: physical light, honest captions, a typographic voice system, hand-set line breaks and a foley score |
| Legibility on a phone | Body ≥ 44 px everywhere (film statements 52–64 px), ink-1 at ≈ 16:1 on void, never on a bright area, at most two blocks on screen |
| Content drift | Kickers are mandatory for his lines; 据报道 keeps point 2 hedged; no numbers, no prices, no model names; his changed mind is in the third person; our readings are labelled. Never imply Copilot picks at random; the copy says 混用 |
| Factual risk about the coin | Caption only what the archive says (Greek coins found at Pompeii; Brooklyn Museum). No dates, no deity names |
| Platform compression | Grain is luminance-weighted (quiet in the void, so no blocking). Export x264 CRF 13, preset slow, yuv420p, 1080×1920; check banding in the S3 pool falloff and add 0.4 LSB dither if needed |
| Render time on SwiftShader | The coin world is precomputed in numpy (≈ 1.5 s per frame for about 1300 frames, ≈ 33 min). Only S8–S9 use WebGL (one textured plane); the glass is a 2D overlay |

---

## Appendix A: Copy deck, in order (for proofreading)

```
S1  微软 CEO 纳德拉判断
    大模型
    要打价格战了
    古希腊钱币，庞贝出土
    照片：布鲁克林博物馆　本片重新打光
S2  大模型按 token 计价。
    token 在英文里，也指代币：
    一种代替钱流通的小圆片。
S3  01 价格战
    他判断
    大多数企业场景的日常算力，
    终将商品化。
    模型层，会有一场
    残酷的价格战。
S4  他判断
    最前沿的模型，
    只会服务少数顶尖场景。
    猎鹰 9 号与 DSCOVR 卫星，发射前，2015
    照片：SpaceX　公有领域
S5  02 混用
    据报道
    微软 Copilot 内部，
    每天都在混用
    便宜的闭源与开源模型。
    一 二 三 四 五 六 日
    闭源 / 开源（标签）
S6  03 私有评测
    纳德拉认为
    每家公司，都会有
    自己的私有评测。
    那会是它的核心 IP。
    同一枚钱币，光从 5° 掠过
S6b ● 我们的理解
    公开榜单像顺光，
    模型看起来都差不多。
    私有评测是你自己的侧光，
    照出你在乎的差别。
S7  04 改变的看法
    被问到改变过什么看法
    他以前以为，规模够大，
    对齐自然会来。
    现在，他不这么想了。
    哈勃极深场，2012
    照片：NASA　公有领域
S8  04 零信任
    他说
    微软不等对齐问题解决，
    先给模型套上零信任架构。
    身份　每个 agent 都有自己的身份
    记录　每一次工具与模型调用都留下记录
    权限　规则放在模型之外
S9  ● 我们的理解
    模型，人人都买得到。
    看它的角度，只有你有。
    你的评测，你的规则。
S10 ● Coo-Coo出海Ai实验室
    大模型要打价格战了　20VC 对话纳德拉　笔记
    来源：20VC 播客，Harry Stebbings 对话 Satya Nadella（微软 CEO），2026.10.26 发布。
    片中观点据公开报道转述，非原话；标注为我们的理解的部分，是本号观点。
    图片：布鲁克林博物馆（本片重新打光）、SpaceX、NASA；公有领域或无已知版权限制。
```

## Appendix B: Build pipeline and render budget

1. `coinworld.py` (new; wraps `kit/relight.py`): reads the LX (§2.2) and camera (§2.4) cues as JSON, warps the 6× source maps per frame, relights, and writes `build/f2/coin/%04d.png`. Frames are 1080×1920 for the top-down shots and 1080×1000 textures for S8–S9. About 1300 frames at ≈ 1.5 s each.
2. `f2/film.html`: `renderAt(t)` places the coin-world frame, or transforms the rocket and Hubble plates. It drives the Three.js plane and the glass overlay in S8–S9, and the DOM type, gauge (SVG), days and tags from one cue table. `window.__duration = 58.333`.
3. `node f2/render.mjs --page f2/film.html --from 0 --to 58.333 --out build/f2/raw.mp4`
4. `python3 f2/film.py build/f2/raw.mp4 build/f2/graded.mp4 --look f2/concepts/product/kit/look.json`
5. `score.py` (new): the §6.2 cue sheet built on `f2/synth.py`, written to `build/f2/score.wav`.
6. Mux: `ffmpeg -i graded.mp4 -i score.wav -c:v copy -c:a aac -b:a 256k -shortest final.mp4`
7. Carousel: the `kit/proof.html` frames c01–c07, then `film.py --still` with weave 0.

Total about 1 h of CPU on this machine.
