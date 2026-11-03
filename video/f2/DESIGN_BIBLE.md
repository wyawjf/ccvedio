# 第十二张 · THE TWELFTH PLATE — Production Design Bible (LOCKED)

**Topic:** 微软CEO：大模型要打价格战了 · **Account:** Coo-Coo出海Ai实验室 (Xiaohongshu)
**Deliverables:** vertical film 1080×1920, 30 fps, **1772 frames = 59.067 s**, silent text + synthesized score · carousel 1080×1440 × **7 frames** (C1 is also the video cover)
**Spine:** `concepts/doc.md` (won 3/3 judges). **Grafts:** per-call router light, coin pitches from measured radii, honest-scale captions, zero-trust margin, plate-mark emboss, two copy lines (all from `editorial.md`); retina rising with a terminator, headline static from frame 0 (`idea.md`); light-foley at the lamp-up, licence wording, the 示意 honesty rule (`product.md`).
**Status:** locked. Production builds exactly this. If a number here conflicts with any concept doc or look-dev, this file wins.
**Layout proofs** (real fonts, real copy, approximate grade, no post): `f2/bible_proofs/` (`_final_film_a.jpg`, `_final_film_b.jpg`, `_final_car.jpg`, 1:1 frames, `_cover_thumb.jpg`, `_c7_emb2_crop.jpg`). They check geometry only. Final look = §5–§7.

---

## 0. What changed from doc.md (fix log)

| Judge must-fix | Resolution in this bible | Where |
|---|---|---|
| S01 Three.js coin = CG passed off as a photo (a coin that never existed) | **No 3D anywhere.** The hook is the real `coins.png` plate in darkroom "dissolve" printing, with a rack focus and one key light on coin #16. The Euler's-disk rattle survives as *sound only*. | S01 |
| S04 weekday rings misstate point 2 and look like detection boxes | Router = **one key light hopping per call** on eighth notes, 10-frame afterglow, no outlines, no labels, no weekdays. Caption `示意　每一束光，是一次调用。` | S03 |
| S02–S07 = six identical "photo + kicker + sentence" cards | Espresso → rocket is **one continuous move** (a slit opens in the everyday). Plate scale/position varies every shot (600 px right-hung print, 284×734 slit, 768 tray, full-bleed band, 748 → 438 eye). Every plate label carries its **docstring test purpose** and a **`图 NN / 12` counter** from its first appearance. | S01–S05 |
| Contact sheet ragged | Real proof-sheet logic: one row height (170 px), common top and bottom lines, three fixed slots, frame numbers in the rebate line. Only `text.png` is centre-cropped (the one wide format). | S06 |
| Setup captions unreadable (21 px, 4.1:1) | Labels 30/24/22 px in bone-5 (5.5:1); counter 30 px; sheet captions 28 px; cell 12 at 32 px in bone; reveal line 46 px. | all |
| S09 climax = plain text on black | The plunge lands with the 12th plate's hairline just inside the frame; his eval line sits **inside the plate**. At the lamp-up the same rectangle becomes an **intaglio plate mark** in paper, revealed by a raking light while the withheld 12th note resolves. | S07–S08 |
| Carousel C3/C5/C6 unproofed | All 7 frames layout-proofed (`bible_proofs/`); captions ≥ 24 px; final QA re-proofs with grade (§10). | §4 |
| Slow stretches 3.6–14 s and 28–39 s | Merged move in S02; S05 gets a reveal (planet → eye → contained) and annotations on beats. | S02, S05 |
| Headline fading in; coin small/game-like | Kicker + headline **static and complete on frame 0**; coin is a real photo at Ø 113 px with lit neighbours; clack + glint at 1.467 s. | S01 |
| `halt` makes mid-line commas half-width | **No `halt`/`palt`.** Full-width punctuation everywhere. | §5.2 |
| No CTA; cover needs a curiosity line | End card question `你的第一道题，考什么？`; cover line `11 张公开图，第 12 张是你的。` (`评论区聊聊` stays in the post caption only). | S08, C1 |
| Licence overclaim (公有领域 / CC0 for all) | `除 09（scikit-image 示例数据）外，均为公有领域、CC0 或无已知版权限制。` | S08, C7 |
| Credits incomplete in the film | Full numbered credit list on the end card and C7. | S08, C7 |
| Meta line set in Song (his voice) | The sheet's fact lines are **Hei** (our voice). | S06 |
| Blur + tracking text entrance (AE preset tell) | Text enters by opacity + 10 px rise only. | §6.3 |
| Coin never explained | `大模型按 token 计价。英文里，token 也指代币。` (permitted general fact). | S03, C3 |
| grace_hopper.jpg not verified | **Verified:** sha256 `a8ca6d73…7130` is byte-identical to matplotlib 3.9.2 `mpl-data/sample_data/grace_hopper.jpg`. All 10 skimage images: max pixel diff 0. | App. C |
| Private person (camera.png) used as the image for "logging" | camera.png appears **only** as a sheet thumbnail. | S06 |

Rejected grafts (and why): the 256-tile step-and-repeat (reads as a filter when paused), the `token /ˈtəʊkən/ n.` dictionary card (worn trope), any `三件事` list in the film and the question `你的产品，现在接了几家模型？` (both are the rejected F carousel's last frames), coin→dot morph, glass case, light gauge, barrel rings, live typing, WenKai "our voice".

---

## 1. The idea

**Two sentences.** Every photograph in this film is one of the eleven public test images that ship inside scikit-image and matplotlib, the "public exam" of computer vision, and we use them, graded as warm darkroom prints, to tell Nadella's four judgments about the coming model price war. At the end the camera pulls back to reveal them as a contact sheet whose twelfth plate is empty: your private eval, the one image nobody can download.

**一句话：** 片中每一张照片，都是代码库自带的公开示例图——计算机视觉的公开考题；最后镜头拉远，它们原来是一张印样，第 12 格是空的：你的私有评测集，唯一下载不到的那一张。

### The three signature moves

1. **The Settle (S01, 0–1.467 s).** Frame 0 is already a finished title over a defocused tray of Pompeii coins. Off screen, a coin spins down: whirr, then a rattle accelerating to 32 Hz. At **f44 (1.467 s)** the rattle ends in a clack, the rack focus lands, and one glint crosses the face of coin #16. Sound, focus and claim land on the same frame. Then a hard graphic match: the bright coin becomes the espresso crema at the same centre (678, 1000).
2. **The Hard Stop (S04, f764 = 25.467 s).** An accelerating push through the Hubble Deep Field dies in one frame. Every audio track goes to digital zero for 12 frames. In 2 frames, his old belief is struck through and `现在 / 他不这么想了。` prints on. Grain and gate weave keep living; only the camera has died.
3. **The Twelfth Plate (S05 → S08, 37.467–59.067 s).** The framed eye pulls back to become cell 05 of a contact sheet of eleven public test images. Eleven felt-piano notes sound as the cells develop; the twelfth cell is an empty hairline window and its note is withheld. The camera dives into the 12th plate, where his line about private evals sits inside its outline. A light table switches on: the darkness becomes paper and the plate becomes an intaglio plate mark, revealed by a raking light. As the light crosses it, the withheld note (D5) finally sounds.

Supporting moves (not signatures): the **develop** (every print comes up highlights-first, like paper in a tray), the **slit** (a narrow window opens in the everyday), the **router light**, the **contain** move (the eye is put inside a frame; the rules sit outside it).

---

## 2. Final copy deck

### 2.1 Voice system (applies to every frame)

| Voice | Face | Used for | Marker |
|---|---|---|---|
| **His view (paraphrased)** | 宋 Noto Serif SC | Everything Nadella judged, said or is reported to do | Always under a Hei kicker: 微软 CEO 纳德拉判断 / 他判断 / 而在他看来 / 据报道 / 他以前以为 / 他说 / 纳德拉认为. Third person only. Never in quotation marks. |
| **Us (facts and readings)** | 黑 Noto Sans SC | Kickers, general facts (token, test images, biometrics), captions, our reading, the question, account, sources | Our *opinions* additionally carry the violet ■ + `我们的解读`. Facts carry no ■. |
| **The archive** | IBM Plex Mono | Library calls, plate numbers, sizes, scale readouts, dates, `your_eval()`, `not in any library` | Never contains a CJK character (including U+3000 and full-width punctuation). |

### 2.2 Film — every on-screen string (exact; one row = one line box)

`␣` is shown only where a space is easy to miss; type ordinary U+0020 spaces exactly as written. `　` = U+3000 (always inside a Hei span).

**S01 · Hook**
| ID | Text |
|---|---|
| S01-K | 微软 CEO 纳德拉判断 |
| S01-H1 | 大模型 |
| S01-H2 | 要打价格战了 |
| S01-SUB | 而且，会很残酷。 |
| S01-L1 | 图 01 / 12　古希腊钱币，庞贝出土 |
| S01-L2 | skimage.data.coins()　分割测试 |
| S01-L3 | 384 × 303 px · × 2.43 → 2.45 (live readout of the current scale; see §5.5) |

**S02 · Everyday → frontier**
| ID | Text |
|---|---|
| RH left | `01 / 04␣␣价格战` |
| RH right | `20VC · 2026.10.26` |
| S02-K1 | 他判断 |
| S02-A1 | 在大多数企业场景里， |
| S02-A2 | 日常算力终将商品化。 |
| S02-L1 | 图 02 / 12　一杯浓缩咖啡 |
| S02-L2 | skimage.data.coffee()　椭圆与纹理 |
| S02-L3 | 600 × 400 px · × 1.01 → 1.02 (live) |
| S02-K2 | 而在他看来 |
| S02-B1 | 前沿模型， |
| S02-B2 | 只服务少数 |
| S02-B3 | 顶级场景。 |
| S02-V1 (vertical) | 图 03／12　猎鹰 9 号与 DSCOVR　示例图 |
| S02-V2 (vertical) | skimage.data.rocket() · 640 × 427 px · × 2.02 → 2.05 (live) |

**S03 · Token · router**
| ID | Text |
|---|---|
| RH left | `02 / 04␣␣混着用` |
| S03-T1 | 大模型按 token 计价。 |
| S03-T2 | 英文里，token 也指代币。 |
| S03-K | 据报道 |
| S03-C1 | 微软 Copilot 内部， |
| S03-C2 | 每天都在混用 |
| S03-C3 | 便宜的闭源与开源模型。 |
| S03-N1 | 示意　每一束光，是一次调用。 |
| S03-N2 | 底图　图 01 / 12　skimage.data.coins() |
| S03-N3 | 384 × 303 px · × 2.01 → 2.02 (live) |

**S04 · Scale · hard stop**
| ID | Text |
|---|---|
| RH left | `03 / 04␣␣改过的看法` |
| S04-K | 他以前以为 |
| S04-OLD | 规模够大，对齐自然会来。 (struck through at the stop) |
| S04-N1 | 现在 |
| S04-N2 | 他不这么想了。 |
| S04-L1 | 图 04 / 12　哈勃极深场，2012 |
| S04-L2 | skimage.data.hubble_deep_field()　多尺度检测 |
| S04-L3 | 1000 × 872 px · × 1.09 → 1.14 (live; freezes at f764) |

**S05 · Zero trust**
| ID | Text |
|---|---|
| RH left | `03 / 04␣␣零信任` (only the name rolls) |
| S05-K | 他说 |
| S05-S1 | 微软不等对齐问题解决， |
| S05-S2 | 先把模型包进零信任架构。 |
| S05-aL | 身份 |
| S05-a1 | 每个 agent， |
| S05-a2 | 各有身份 |
| S05-bL | 记录 |
| S05-b1 | 每一次调用， |
| S05-b2 | 都留下记录 |
| S05-cL | 权限 |
| S05-c1 | 规则与权限， |
| S05-c2 | 在模型之外 |
| S05-L1 | 图 05 / 12　人眼视网膜 |
| S05-L2 | skimage.data.retina()　圆形图像 |
| S05-L3 | 1411 × 1411 px · × 0.31 |
| S05-L4 | 血管纹路因人而异，可用于身份识别 |

**S06 · Contact sheet**
| ID | Text |
|---|---|
| RH left | `04 / 04␣␣私有评测集` |
| S06-F1 | 这 11 张，都是代码库自带的公开示例图， |
| S06-F2 | 谁都能下载，谁都能拿它考算法。 |
| S06-HDR | from skimage import data · matplotlib sample_data · 11 / 12 |
| cell 01–03 | `01␣␣分割测试` · `02␣␣椭圆与纹理` · `03␣␣示例图` |
| cell 04–06 | `04␣␣多尺度检测` · `05␣␣圆形图像` · `06␣␣分割与去噪` |
| cell 07–09 | `07␣␣示例图` · `08␣␣示例图` · `09␣␣直方图均衡` |
| cell 10–11 | `10␣␣角点检测` · `11␣␣反卷积` |
| cell 12 line 1 | `12␣␣你的评测集` |
| cell 12 line 2 | `未公开` |

**S07 · Inside the twelfth plate**
| ID | Text |
|---|---|
| S07-K | 纳德拉认为 |
| S07-E1 | 每家公司， |
| S07-E2 | 都会有自己的 |
| S07-E3 | 私有评测集。 |
| S07-E4 | 那会是它的核心 IP。 |
| S07-L1 | 图 12 / 12　你的评测集 |
| S07-L2 | your_eval()　未公开 |
| S07-L3 | not in any library |

**S08 · Colophon (paper)**
| ID | Text |
|---|---|
| S08-RL | ■ 我们的解读 |
| S08-R1 | 公开的考题，谁都能刷分； |
| S08-R2 | 你的考题，只有你有。 |
| S08-Q | 你的第一道题，考什么？ |
| S08-ACC | ■ Coo-Coo出海Ai实验室 |
| S08-SRC1 | 来源　20VC 播客，Harry Stebbings 对话 Satya Nadella，2026.10.26 发布。 |
| S08-SRC2 | 片中观点据该期节目的公开报道转述整理，非原话；我们的解读为本号观点。 |
| S08-SRC3 | 图像　均为 scikit-image 与 matplotlib 自带示例图； |
| S08-SRC4 | 除 09（scikit-image 示例数据）外，均为公有领域、CC0 或无已知版权限制。 |
| S08-SRC5 | 01 Brooklyn Museum　02 Rachel Michetti　03 SpaceX　04 NASA |
| S08-SRC6 | 05 Wikimedia Commons　06 Lav Varshney　07 NASA　08 U.S. Navy |
| S08-SRC7 | 10 Wikipedia　11 Stefan van der Walt |

(In SRC4–SRC7 the two-digit plate numbers are IBM Plex Mono; everything else is Hei.)

### 2.3 Carousel — every string

Each `code span` is one line box, in reading order. Footer on C2–C6 = `■ Coo-Coo出海Ai实验室` + page index.

| Frame | Strings |
|---|---|
| **C1 Cover** | `微软 CEO 纳德拉判断`<br>`20VC · 2026.10.26`<br>`大模型`<br>`要打价格战了`<br>`图 01 / 12　古希腊钱币，庞贝出土`<br>`skimage.data.coins()␣␣No.16 / 24`<br>`11 张公开图，第 12 张是你的。`<br>`■ Coo-Coo出海Ai实验室` (no page index) |
| **C2** | RH `01 / 04␣␣价格战` / `20VC · 2026.10.26`<br>`他判断`<br>`在大多数企业场景里，`<br>`日常算力终将商品化。`<br>`图 02 / 12　一杯浓缩咖啡`<br>`skimage.data.coffee()　椭圆与纹理`<br>`600 × 400 px · × 1.00`<br>`而在他看来`<br>`前沿模型，只服务`<br>`少数顶级场景。`<br>vertical: `图 03／12　猎鹰 9 号`<br>page `02 / 07` |
| **C3** | RH `02 / 04␣␣混着用`<br>`据报道`<br>`微软 Copilot 内部，`<br>`每天都在混用`<br>`便宜的闭源与开源模型。`<br>`示意　每一束光，是一次调用。`<br>`底图　图 01 / 12　skimage.data.coins()`<br>`384 × 303 px · × 2.00`<br>`大模型按 token 计价；英文里，token 也指代币。`<br>page `03 / 07` |
| **C4** | RH `03 / 04␣␣改过的看法`<br>`他以前以为`<br>`规模够大，对齐自然会来。` (struck)<br>`现在，他不这么想了。`<br>`他说`<br>`微软不等对齐问题解决，`<br>`先把模型包进零信任架构。`<br>`身份` + `每个 agent，各有身份`<br>`记录` + `每一次调用，都留下记录`<br>`权限` + `规则与权限，在模型之外`<br>`图 05 / 12　视网膜`<br>page `04 / 07` |
| **C5** | RH `04 / 04␣␣私有评测集`<br>`这 11 张，都是代码库自带的公开示例图，`<br>`谁都能下载，谁都能拿它考算法。`<br>`from skimage import data · matplotlib sample_data · 11 / 12`<br>cell captions identical to S06<br>page `05 / 07` |
| **C6** | RH `04 / 04␣␣私有评测集`<br>`纳德拉认为`<br>`每家公司，`<br>`都会有自己的`<br>`私有评测集。`<br>`那会是它的核心 IP。`<br>`图 12 / 12　你的评测集`<br>`your_eval()　未公开`<br>`not in any library`<br>page `06 / 07` |
| **C7** | `■ 我们的解读`<br>page `07 / 07`<br>`公开的考题，谁都能刷分；`<br>`你的考题，只有你有。`<br>`your_eval()`<br>`用你自己的真实场景出题；`<br>`换模型、混用模型之前，先拿它考一遍。`<br>`你的第一道题，考什么？`<br>`■ Coo-Coo出海Ai实验室`<br>SRC1–SRC7, identical to the film |

### 2.4 Source line and account mark (canonical)

- Account mark: **`Coo-Coo出海Ai实验室`** — exact capitalisation, no spaces, always preceded by the violet ■ (film end card, C7, carousel footers, cover).
- Source block: S08-SRC1…SRC7 above, identical in film and C7. Never shorten SRC4 (the moon has no licence statement in scikit-image).

### 2.5 Post caption (XHS text body, not on screen)

```
微软CEO：大模型要打价格战了
20VC 播客最新一期（2026.10.26），纳德拉谈了四个判断。以下据公开报道整理，均为转述：
1. 大多数企业场景的日常算力终将商品化，模型层会有一场残酷的价格战；前沿模型只服务少数顶级场景。
2. 据报道，微软 Copilot 内部每天都在混用便宜的闭源与开源模型。
3. 每家公司都会有自己的私有评测集，那会是它的核心 IP。
4. 他以前以为规模够大、对齐自然会来，现在不这么想了；微软先把模型包进零信任架构。
我们的解读：模型会降价，眼光不会。
片中 11 张照片，都是开源代码库自带的公开示例图。第 12 张，留给你。
你的评测集里，第一道题考什么？评论区聊聊。
#AI出海 #大模型 #纳德拉 #20VC #AI创业
```

### 2.6 Compliance check (every claim on screen)

| Line | Basis | Voice / marker | Check |
|---|---|---|---|
| 大模型要打价格战了 / 而且，会很残酷。 | Brief point 1 (brutal price war) | Song, kicker 微软 CEO 纳德拉判断 | ✓ attributed, no quotes |
| 在大多数企业场景里，日常算力终将商品化。 | Point 1 | Song, 他判断 | ✓ |
| 前沿模型，只服务少数顶级场景。 | Point 1 | Song, 而在他看来 | ✓ |
| 大模型按 token 计价。英文里，token 也指代币。 | Permitted general fact | Hei, no ■ | ✓ |
| 微软 Copilot 内部，每天都在混用便宜的闭源与开源模型。 | Point 2 (reported) | Song, 据报道 | ✓ no weekday schedule; light = per call, 示意 |
| 规模够大，对齐自然会来。→ 现在 / 他不这么想了。 | Point 4 | Song, 他以前以为 (third person) | ✓ |
| 微软不等对齐问题解决，先把模型包进零信任架构。身份 / 记录 / 权限 | Point 4 | Song, 他说 | ✓ grammatical (不等…，先…) |
| 血管纹路因人而异，可用于身份识别 | General biometric fact | Hei caption | ✓ |
| 这 11 张，都是代码库自带的公开示例图，谁都能下载，谁都能拿它考算法。 | Verified (App. C) | Hei, no ■ (fact) | ✓ |
| Docstring purposes (分割测试 …) | skimage docstrings (App. C) | Hei captions | ✓ |
| 每家公司，都会有自己的私有评测集。那会是它的核心 IP。 | Point 3 | Song, 纳德拉认为 | ✓ |
| 公开的考题，谁都能刷分；你的考题，只有你有。 / C7 entry | Our reading | Hei + ■ 我们的解读 | ✓ labelled |
| Excluded (neocloud renting; "assume the model is compromised"; "private evals define what good looks like") | Not this podcast | — | ✓ absent everywhere |
| Hype words (颠覆、炸裂、彻底、震撼、重磅), exclamation marks, emoji | — | — | ✓ none (残酷 is his "brutal") |
| Quotation marks of any kind (“” "" 「」 『』) | — | — | ✓ none on screen |

---

## 3. Film

### 3.1 Conventions

- **Canvas** 1080×1920, 30 fps CFR. **Frame f** starts at f/30 s. Times are given as `fN (s.sss)`.
- **Beat grid:** 75 BPM, 1 beat = 24 f, anchored to the clack: **B(k) = 44 + 24k**. Every cut lands on a B-frame. Eighth notes = 12 f.
- **Coordinates:** `(x, y)` = CSS left/top of the **line box**, line-height as given by the token (§5.2). One element per line; manual breaks only; left-aligned unless "right-aligned to x".
- **Layers (back → front):** ink ground → photo layer (camera transforms apply) → hairlines (1 px, drawn in screen space at any scale) → type (screen space, never zoomed except sheet captions) → running head (screen space) → post (§5.4).
- **Safe zone:** nothing essential at y < 200 or y > 1476; essential text inside x 64–1000; in the band y 1150–1476, essential text ends ≤ x 940. All positions below comply.
- **Text in/out** (unless stated): IN = opacity 0→1 over 16 f (E-FADE) + translateY +10→0 px over 22 f (E-SETTLE). OUT = opacity 1→0 over 12 f (E-LEAVE), no movement. "in f128" = first frame of the fade.
- **Before a hard cut**, all text is gone ≥ 4 f before the cut (labels leave 4 f before the rest).

### 3.2 Timeline overview

| Shot | Name | Frames | Seconds | Length | Beats | Enters by | Leaves by |
|---|---|---|---|---|---|---|---|
| **S01** | Hook · the coin settles | f0 → f115 | 0.000 → 3.867 | 116 f · 3.867 s | — → B3 | — | Hard cut, graphic match (coin #16 → crema at 678,1000) |
| **S02** | Everyday → frontier (one move) | f116 → f379 | 3.867 → 12.667 | 264 f · 8.800 s | B3 → B14 | Match cut | Hard cut on COIN D6 |
| **S03** | Token · the router light | f380 → f643 | 12.667 → 21.467 | 264 f · 8.800 s | B14 → B25 | Hard cut | Hard cut on BLOOM + FELT F3 |
| **S04** | Scale · the hard stop | f644 → f859 | 21.467 → 28.667 | 216 f · 7.200 s | B25 → B34 | Hard cut | Hard cut on SUB swell |
| **S05** | Zero trust · the eye in the frame | f860 → f1123 | 28.667 → 37.467 | 264 f · 8.800 s | B34 → B45 | Hard cut | Continuous pull-back |
| **S06** | The contact sheet | f1124 → f1387 | 37.467 → 46.267 | 264 f · 8.800 s | B45 → B56 | Pull-back | Continuous plunge |
| **S07** | Inside the twelfth plate | f1388 → f1603 | 46.267 → 53.467 | 216 f · 7.200 s | B56 → B65 | Plunge | Continuous lamp-up |
| **S08** | Lamp-up · plate mark · colophon | f1604 → f1771 | 53.467 → 59.067 | 168 f · 5.600 s | B65 → B72 | Lamp-up | End; f1771 is a complete shareable still |

### 3.3 Shot specifications

---

#### S01 · Hook — the coin settles (f0 → f115, 0.000 → 3.867 s)

**Picture.** `coins.png`, full frame (0,0)–(384,303), B/W warm print (§7), **dissolve mode**: the cloth is pulled toward ink through the watershed matte, coin #16 (the facing head) is key-lit, every other coin sits at fill 0.10.
- Light map: `L = max(fill, fill + (k − fill)·exp(−½·(max(d/r − 0.85, 0)/1.035)²))`, fill 0.10, k 1.0, d = screen distance to #16's centre, r = #16's screen radius (56.4 px at ×2.40).
- Cloth outside the matte: `cloth = ((g − 0.10)/0.90)^1.6 × 0.55`; pixel = ramp((m·g + (1 − m)·cloth) · L).
- Radial visibility mask (S01 only), fixed in screen space: ellipse centre (678, 1000), radii 460 × 300; `vis = 1 − smoothstep(0.45, 1.0, d_ellipse)`.
- Coin #16 is anchored at screen **(678, 1000)** for the whole shot. At ×2.40 the plate's top-left is (168.2, 536.6) and its size 921.6 × 727.2.

**Camera / optics.**
| Move | Frames | From → to | Curve |
|---|---|---|---|
| Rack focus (disc blur on the photo layer only) | f0 → f44 | radius 16 px → 0 | E-FOCUS `cubic-bezier(.33,0,.15,1)` |
| Focus breathing (scale about 678,1000) | f0 → f44 | ×2.43 → ×2.40 | E-FOCUS |
| Rostrum drift (scale about 678,1000) | f44 → f115 | ×2.40 → ×2.46 | linear |
| Glint across #16 | f44 → f52 | band from −1.2r to +1.2r | E-GLINT `cubic-bezier(.2,.6,.3,1)` |

Bokeh: linearise (γ 2.2), multiply pixels with L > 0.55 by up to ×2.2, convolve with an anti-aliased disc, re-encode. Glint: an 18 px band (Gaussian profile, σ 6 px) at 30° (rising to the right), additive +0.30 in linear light, colour #F4EEDC, clipped by #16's matte. **Frame 0 shows the finished title over the defocused field; it is never black.**

**Text.**
| ID | Token (resolved) | x, y | In | Out |
|---|---|---|---|---|
| S01-K | T-KICK · Noto Sans SC 500 44/44 +0.04em bone-5 | 90, 330 | **static from f0** | f100 (3.333) |
| S01-H1 | T-DISPLAY · Noto Serif SC 700 148/163 −0.015em bone | 84, 390 | **static from f0** | f100 |
| S01-H2 | T-DISPLAY | 84, 553 | **static from f0** | f100 |
| S01-SUB | T-SECOND · Noto Serif SC 500 56/75 bone-7 | 90, 1262 | f53 (1.767) | f100 |
| S01-L1 | T-CAP1 · Hei 500 30/42 +0.04em bone-5, `01 / 12` in Plex Mono 500 30 | 90, 1356 | f66 (2.200) | f96 (3.200) |
| S01-L2 | T-CAP2 · Plex Mono 400 24/34 +0.02em + Hei 500 24 +0.04em, bone-5 | 90, 1400 | f70 | f96 |
| S01-L3 | T-CAP3 · Plex Mono 400 22/31 +0.02em bone-5 (live ×2.43 → 2.45) | 90, 1434 | f74 | f96 |

Picture alone f112–f115. **Cut f116** (B3) onto the crema, same centre.

**Sound:** f0 ROOM in · f1 COIN flick (D7) · f2–f15 WHIRR · f15–f44 RATTLE · **f44 CLACK** · f53 DRONE in · f54 FELT D3 (cue sheet §8.2).

---

#### S02 · Everyday → frontier (f116 → f379, 3.867 → 12.667 s)

**Picture A — espresso.** `coffee.png` full (0,0)–(600,400), colour print grade, sat 0.84, halation (thr 0.80, σ 10, 0.22) on rim, spoon and saucer glints. **×1.00 = 600×400 at (390, 860)**, right-hung to x 990. Crema centre (288,140) lands on **(678, 1000)** = the coin. Develops f116–f149 (33 f, E-DEVELOP): the crema comes up first, exactly where the coin was.
**Picture B — slit.** `rocket.jpg`, sky deblocked first (§7), crop **(250,60)–(392,427)** = 142×367, **×2.00 = 284×734**, slit rect **x 706–990, y 693–1427**. Sat 0.74, halation thr 0.78 on the sodium lamps. Hard-edged mask (1 px anti-alias), no border.

| Event | Frames | Spec | Curve |
|---|---|---|---|
| Espresso drift | f116 → f259 | scale 1.000 → 1.020 about (678,1000) | linear |
| House lights down | f244 → f256 | espresso exposure ×1.00 → ×0.35 (linear light) | linear |
| **Slit opens** | f260 → f287 | mask width 0 → 284, centred on x 848, full height 693–1427 | E-SNAP `cubic-bezier(.7,0,.2,1)` |
| Rocket develops inside the slit | f260 → f290 | highlights first (pad lamps, white vehicle) | E-DEVELOP |
| Espresso develops **out** (outside the slit) | f287 → f314 | threshold rising: shadows vanish first, crema last | E-DEVELOP |
| Slit content push | f260 → f379 | 1.000 → 1.030 about the nose cone (848, 827) | linear |

The slit is taller than the espresso print (it overhangs 167 px above and below): the frontier is a narrow, tall window cut through the everyday.

**Text.**
| ID | Token | x, y | In | Out |
|---|---|---|---|---|
| RH left `01 / 04` + `价格战` | T-RH | 90, 220 | f118 (fade 12 f, no rise) | stays (rolls in S03) |
| RH right `20VC · 2026.10.26` | T-RH mono | right-aligned to 990, y 220 | f118 | stays until f1580 |
| S02-K1 他判断 | T-KICK | 90, 330 | f128 (4.267) | f228 (7.600) |
| S02-A1 | T-ST · Noto Serif SC 600 72/91 bone | 90, 396 | f134 | f228 |
| S02-A2 | T-ST | 90, 487 | f138 | f228 |
| S02-L1 / L2 / L3 | T-CAP1 / T-CAP2 / T-CAP3 | 390, 1280 / 1324 / 1358 | f150 / f154 / f158 | f224 |
| S02-K2 而在他看来 | T-KICK | 90, 330 | f266 (8.867) | f344 (11.467) |
| S02-B1 / B2 / B3 | T-ST | 90, 396 / 487 / 578 | f272 / f276 / f280 | f344 |
| S02-V1 | T-VCAP · Hei 500 30, vertical-rl, +0.12em, bone-5; `03` `12` `9` upright-combined (Plex Mono 500 for 03/12) | box left 652, top 693 | f290 | f340 |
| S02-V2 | Plex Mono 400 24, vertical-rl (sideways), bone-5, live scale | box left 614, top 693 | f294 | f340 |

Picture alone f356–f379. **Cut f380** (B14).
**Sound:** f116 BLOOM + FELT A3 · f244 drone LP closes · f260 SLIT swell + FELT E4 · f272 SHIMMER.

---

#### S03 · Token · the router light (f380 → f643, 12.667 → 21.467 s)

**Picture.** `coins.png` full, B/W print, **dissolve mode, ×2.00 = 768×606 at (222, 700)**, right-hung. No radial mask (all 24 coins faintly present at fill 0.10). Develops f380–f418 (39 f, B/W develop), #16 first because it is already lit (k 1.0 from f380, a callback to the hook). Drift scale 1.000 → 1.010 about the tray centre (606, 1003), f380–f643, linear (lights stay attached to their coins).

**The router light.** One key light. It leaves #16 at f484 and lands on a new coin every 12 f (eighth notes): **travel 4 f** (E-HOP `cubic-bezier(.5,0,.2,1)`; centre and radius interpolate), **hold 8 f**. The coin just left keeps an **afterglow** k 0.45 → 0.10, linear over 10 f. Light radius = the target coin's screen radius. 180° motion blur on travel frames.

| Hop | Lands | Coin | Note (Hz) | Screen centre | r (px) | Pan |
|---|---|---|---|---|---|---|
| — | f380 | #16 (start) | D6 1174.66 | 646.8, 1086.2 | 47.0 | +0.12 |
| 1 | f488 (16.267) | #06 | F5 698.46 | 891.4, 787.0 | 57.6 | +0.39 |
| 2 | f500 | #23 | C6 1046.50 | 823.2, 1226.4 | 50.4 | +0.31 |
| 3 | f512 | #19 | G5 783.99 | 313.8, 1219.6 | 56.0 | −0.25 |
| 4 | f524 | #04 | D6 1174.66 | 652.4, 802.2 | 45.4 | +0.12 |
| 5 | f536 | #14 | F6 1396.91 | 425.4, 1091.2 | 43.2 | −0.13 |
| 6 | f548 | #09 | G6 1567.98 | 529.0, 954.4 | 37.0 | −0.01 |
| 7 | f560 | #24 | F6 1396.91 | 938.4, 1235.8 | 43.4 | +0.44 |
| 8 | f572 | #17 | D6 1174.66 | 769.0, 1087.2 | 43.6 | +0.25 |
| 9 | f584 | #11 | C6 1046.50 | 763.2, 937.6 | 49.4 | +0.25 |
| 10 | f596 | #21 | G5 783.99 | 566.6, 1222.4 | 54.8 | +0.03 |
| 11 | f608 | #18 | D5 587.33 | 916.0, 1073.4 | 63.2 | +0.42 |
| 12 | f620 (20.667) | **#16 (home)** | D6 1174.66 | 646.8, 1086.2 | 47.0 | +0.12 |

(Centres at drift 1.000; apply the drift transform per frame.) The light holds on #16 from f620 to the cut.

**Text.**
| ID | Token | x, y | In | Out |
|---|---|---|---|---|
| RH roll → `02 / 04` + `混着用` | T-RH, roll | 90, 220 | f382 | — |
| S03-T1 | T-FACT · Noto Sans SC 500 52/74 bone | 90, 330 | f386 (12.867) | f478 (15.933) |
| S03-T2 | T-FACT | 90, 404 | f390 | f478 |
| S03-K 据报道 | T-KICK | 90, 330 | f488 (16.267) | f616 (20.533) |
| S03-C1 / C2 / C3 | T-ST64 · Noto Serif SC 600 64/83 bone | 90, 396 / 479 / 562 | f494 / f498 / f502 | f616 |
| S03-N1 | T-KEY · Hei 500 32/45 +0.04em bone-7 | 222, 1326 | f512 | f612 |
| S03-N2 | T-CAP4 Hei 24 + Plex Mono 24 (`01 / 12`, `skimage.data.coins()`), bone-5 | 222, 1372 | f516 | f612 |
| S03-N3 | T-CAP3 (live ×2.01 → 2.02) | 222, 1406 | f520 | f612 |

Picture alone f628–f643. **Cut f644** (B25).
**Sound:** f380 COIN D6 (#16's own pitch) + BLOOM · f488…f620 twelve PINGs at the hop notes.

---

#### S04 · Scale · the hard stop (f644 → f859, 21.467 → 28.667 s)

**Picture.** `hubble_deep_field.jpg` full, colour grade sat 0.86, space lifted to exactly ink, halation thr 0.62. **×1.08 = 1080×942 placed at (0, 544)**, seen through a **full-width band mask y 760–1330** with 72 px linear feathers top and bottom (source rows ≈ 200–728). Two layers: FG = bright galaxies (§7), BG = the rest with holes median-filled. Develops f644–f677 (stars first).

| Event | Frames | Spec | Curve |
|---|---|---|---|
| Push, parallax | f644 → f764 | BG ×1.000 → ×1.060, FG ×1.000 → ×1.090, about the anchor galaxy (727,473) = screen (785.2, 1054.8) | E-ACCEL `cubic-bezier(.5,0,1,1)` |
| **HARD STOP** | **f764 (25.467)** | velocity → 0 in one frame; f764 onward the camera transform is frozen at its f764 value | — |
| Strike + print-on | f767 (50 %) → f768 (100 %) | S04-OLD turns bone → bone-5; a 3 px bone-5 strike appears; S04-N1/N2 appear | 2 frames, no blur, no motion |

Max magnification at the stop: 1.08 × 1.09 = 1.177 (≤ 1.20 limit). Grain, gate weave and flicker continue through the stop.

**Text.**
| ID | Token | x, y | In | Out |
|---|---|---|---|---|
| RH roll → `03 / 04` + `改过的看法` | T-RH | 90, 220 | f646 | — |
| S04-K 他以前以为 | T-KICK | 90, 330 | f656 (21.867) | f836 (27.867) |
| S04-OLD | T-ST64 (bone; bone-5 from f767) | 90, 396 | f662 | f836 |
| Strike | rect 3 px, bone-5, x 84 → 864, y 438 → 441 | — | f767–f768 | f836 |
| S04-N1 现在 | T-BIG · Noto Serif SC 700 112/125 −0.01em bone | 86, 488 | **f767–f768 print-on** | f836 |
| S04-N2 他不这么想了。 | T-BIG | 86, 613 | **f767–f768 print-on** | f836 |
| S04-L1 / L2 / L3 | T-CAP1 / T-CAP2 / T-CAP3 (live ×1.09 → 1.14, frozen from f764) | 90, 1354 / 1398 / 1432 | f680 / f684 / f688 | f832 |

Picture alone f848–f859. **Cut f860** (B34).
**Sound:** f644 BLOOM + FELT F3, swell · **f764–f775 digital silence** · f776 ROOM back · f777 FELT D2.

---

#### S05 · Zero trust — the eye in the frame (f860 → f1123, 28.667 → 37.467 s)

**Picture.** `retina.jpg` full (1411²), colour grade sat 0.86, halation thr 0.70, strength 0.28 (the optic disc glows). The fundus camera's orientation notch is kept (never retouched).

| State / move | Frames | Spec | Curve |
|---|---|---|---|
| **Rise (planet)** | f860 → f920 | image **748×748 (×0.5301) at (166, 636)**, centre (540,1010); terminator lighting (below); translateY +36 → 0 | E-RISE `cubic-bezier(.25,.1,.25,1)` (light) · E-SETTLE (rise) |
| **Contain** | f932 → f962 | image 748 → **438 (×0.3104)**, centre (540,1010) → **(747, 943)** (top-left 528, 724); scale interpolated in log space | E-TRAVEL `cubic-bezier(.65,0,.35,1)` |
| Frame draws | f962 → f978 | 1 px hairline rule-30, rect **(504,700)–(990,1186)**, clockwise from the top-left corner | E-DRAW `cubic-bezier(.45,0,.2,1)` |
| Frame fades | f1096 → f1108 | hairline opacity → 0 | E-LEAVE |

Terminator: for the disc (centre and radius of the visible disc), `n = (nx, ny, √(1−nx²−ny²))`; `l(t) = normalize(mix(l0, l1, E))`, l0 = (−0.97, −0.22, −0.10), l1 = (−0.30, −0.20, 0.93); `I = smoothstep(−0.10, 0.30, dot(n, l) + 0.8·E)`; apply I to the plate in linear light **before** halation. At f860 only a thin crescent on the left limb (with the optic disc) is lit; by f920 the disc is the untreated photograph. The caption names it only after it is fully lit.

**Text.**
| ID | Token | x, y | In | Out |
|---|---|---|---|---|
| RH roll (name only) → `零信任` | T-RH | 90, 220 | f862 | — |
| S05-K 他说 | T-KICK | 90, 330 | f908 (30.267) | f1084 (36.133) |
| S05-S1 / S2 | T-ST | 90, 396 / 487 | f914 / f918 | f1084 |
| S05-aL 身份 | T-NOTE-L · Noto Sans SC 700 44/62 +0.02em bone | 90, 700 | f980 (32.667) | f1084 |
| S05-a1 / a2 | T-NOTE · Noto Serif SC 500 44/62 bone-7 | 200, 700 / 200, 762 | f984 / f988 | f1084 |
| S05-bL 记录 | T-NOTE-L | 90, 866 | f1004 (33.467) | f1084 |
| S05-b1 / b2 | T-NOTE | 200, 866 / 200, 928 | f1008 / f1012 | f1084 |
| S05-cL 权限 | T-NOTE-L | 90, 1032 | f1028 (34.267) | f1084 |
| S05-c1 / c2 | T-NOTE | 200, 1032 / 200, 1094 | f1032 / f1036 | f1084 |
| S05-L1 / L2 / L3 / L4 | T-CAP1 / T-CAP2 / T-CAP3 / T-CAP4 | 504, 1210 / 1254 / 1288 / 1319 | f974 / f978 / f982 / f986 | f1080 |

The rules (身份/记录/权限) sit **outside** the frame; the eye (the model) sits inside it. Picture alone f1108–f1123. **Continuous pull-back from f1124.**
**Sound:** f860 SUB swell + PAD-lite B♭ · f962 DRAW whisper · STAMPs on f980 / f1004 / f1028.

---

#### S06 · The contact sheet (f1124 → f1387, 37.467 → 46.267 s)

**Sheet geometry (sheet space = screen space at scale 1).** Three slots at x **90 / 405 / 720** (window width ≤ 270, gutter 45). Four rows, tops **508 / 744 / 980 / 1216**; every thumbnail is exactly **170 px tall** (common top and bottom lines), left-aligned in its slot. Thumbnails are drawn **from full-resolution graded sources at the current transform** (never upscale a small thumbnail). Captions sit in the rebate line 10 px below the window.

| Cell | Asset | Crop (source px) | Size | Scale | Top-left | Caption top-left |
|---|---|---|---|---|---|---|
| 01 | coins.png | full | 215×170 | 0.5611 | 90, 508 | 90, 688 |
| 02 | coffee.png | full | 255×170 | 0.4250 | 405, 508 | 405, 688 |
| 03 | rocket.jpg | full | 255×170 | 0.3981 | 720, 508 | 720, 688 |
| 04 | hubble_deep_field.jpg | full | 195×170 | 0.1950 | 90, 744 | 90, 924 |
| 05 | retina.jpg | full | 170×170 | 0.1205 | 405, 744 | 405, 924 |
| 06 | camera.png | full | 170×170 | 0.3320 | 720, 744 | 720, 924 |
| 07 | astronaut.png | full | 170×170 | 0.3320 | 90, 980 | 90, 1160 |
| 08 | grace_hopper.jpg | full | 145×170 | 0.2833 | 405, 980 | 405, 1160 |
| 09 | moon.png | full | 170×170 | 0.3320 | 720, 980 | 720, 1160 |
| 10 | text.png | **(87,0)–(360,172)** centre crop | 270×170 | 0.9884 | 90, 1216 | 90, 1396 |
| 11 | clock_motion.png | full | 227×170 | 0.5667 | 405, 1216 | 405, 1396 |
| **12** | — | — | **255×170 window, 1 px rule-30 hairline** | — | 720, 1216 | 720, 1396 / 720, 1432 |

**Pull-back** f1124 → f1172 (48 f), E-REVEAL `cubic-bezier(.83,0,.17,1)`. The sheet transform is `screen = s·p + T`. With u = E-REVEAL(t): `s = s0^(1−u)`, s0 = 438/170 = **2.5765**; anchor P = cell 05 top-left on screen, `P = P0 + (P1 − P0)·w`, `w = (s0 − s)/(s0 − 1)`, P0 = (528, 724), P1 = (405, 744); `T = P − s·(405, 744)`. At f1124, T0 = (−515.5, −1192.9) and the frame is pixel-identical to S05's last frame (only cell 05 drawn). 180° motion blur on frames moving > 8 px/f.

**Cells develop** (15 f each, E-DEVELOP) in reading order, **3 f apart**: 01 f1154 · 02 f1157 · 03 f1160 · 04 f1163 · (05 already present; its note sounds at f1166) · 06 f1169 · 07 f1172 · 08 f1175 · 09 f1178 · 10 f1181 · 11 f1184. Each cell's caption fades in 6 f after its cell starts (E-FADE 12 f, no rise). **Cell 12's hairline draws f1187 → f1199** (clockwise from top-left, E-DRAW) with **no note**; its caption: line 1 f1199, line 2 f1203.

**Text (screen space unless noted).**
| ID | Token | x, y | In | Out |
|---|---|---|---|---|
| RH roll → `04 / 04` + `私有评测集` | T-RH | 90, 220 | f1126 | — |
| S06-F1 | T-FACT46 · Noto Sans SC 500 46/65 bone | 90, 290 | f1190 (39.667) | f1360 (45.333) |
| S06-F2 | T-FACT46 | 90, 355 | f1196 | f1360 |
| S06-HDR | T-HDR · Plex Mono 400 24/24 +0.02em bone-5 | 90, 446 | f1172 | f1360 |
| Cell captions 01–11 (sheet layer) | T-SHEET · Plex Mono 500 28 bone-5 index + 2 spaces + Hei 500 28 bone-7 | per table | per cell | f1364 |
| Cell 12 line 1 (sheet layer) | Plex Mono 500 28 bone-5 `12␣␣` + Hei 500 32 **bone** `你的评测集` | 720, 1396 | f1199 | f1364 |
| Cell 12 line 2 (sheet layer) | Hei 500 28 bone-5 `未公开` | 720, 1432 | f1203 | f1364 |

Picture alone f1376–f1387 (sheet + empty window only). **Plunge from f1388.**
**Sound:** f1124 reverse BLOOM · eleven FELT notes f1154…f1184 · **f1187 the 12th note is withheld** (drone dips).

---

#### S07 · Inside the twelfth plate (f1388 → f1603, 46.267 → 53.467 s)

**Plunge** f1388 → f1428 (40 f), E-DIVE `cubic-bezier(.6,0,.1,1)`: cell 12's window grows from (720,1216, 255×170) to **(42, 600, 996×664)**. With u = E-DIVE(t): `s = s1^u`, s1 = 996/255 = **3.9059**; `P = P0 + (P1 − P0)·w`, `w = (s − 1)/(s1 − 1)`, P0 = (720,1216), P1 = (42,600); `T = P − s·(720,1216)`; end T1 = (−2770.2, −4149.6). The other cells fly out of frame with motion blur; the window's hairline stays 1 px and **becomes rule-18 with a 6 px corner radius** by f1428 (the plate outline). Interior and surround are ink.

**Text (inside the plate).**
| ID | Token | x, y | In | Out |
|---|---|---|---|---|
| S07-K 纳德拉认为 | T-KICK | 90, 660 | f1430 (47.667) | f1580 (52.667) |
| S07-E1 / E2 / E3 | T-ST | 90, 726 / 817 / 908 | f1436 / f1440 / f1444 | f1580 |
| S07-E4 | T-SECOND | 90, 1040 | f1464 (48.800) | f1580 |
| S07-L1 | T-CAP1 (`你的评测集` in bone) | 90, 1290 | f1470 | f1576 |
| S07-L2 | Plex Mono 400 24 `your_eval()` + Hei 500 24 `　未公开`, bone-5 | 90, 1334 | f1474 | f1576 |
| S07-L3 | T-CAP3 `not in any library` | 90, 1368 | f1478 | f1576 |
| RH (both sides) | — | — | — | f1580 → f1592 |

Picture alone (ink + plate outline) f1592–f1603. **Lamp-up at f1604.**
**Sound:** f1388 RISER, hard cut f1428 · f1428 SUB · f1444 FELT dyad A3+E4 · f1592 drone out.

---

#### S08 · Lamp-up · plate mark · colophon (f1604 → f1771, 53.467 → 59.067 s)

| Event | Frames | Spec | Curve |
|---|---|---|---|
| **Lamp-up** | f1604 → f1628 | ground ink #0B0A09 → paper #F2EEE7 (linear light); paper texture fades in with it; film bloom 0 → 0.18 → 0 (peak f1616) | E-LAMP `cubic-bezier(.4,0,.2,1)` |
| Outline out | f1604 → f1616 | the rule-18 plate outline fades | E-LEAVE |
| **Pull-out** | f1604 → f1652 | plate rect (42,600, 996×664) → **(90, 540, 642×428)**; `s = (642/996)^u`, `P = P0 + (P1 − P0)·(1 − s)/(1 − 0.6446)` | E-SETTLE-L `cubic-bezier(.22,1,.36,1)` |
| **Raking light** | f1604 → f1652 | directional light az 215° → 135°, el 8° → 24°; crosses the plate's midpoint at **f1628** | E-RAKE `cubic-bezier(.45,0,.55,1)` |
| Rest | f1652 → f1771 | az 135°, el 24° (from the top-left) | — |

The plate mark is the intaglio emboss of §7.3, computed per frame at the current rect (all its px parameters scale with rect width / 642). Rest-light result (measured): top and left walls −15 % / −16 %, bottom and right walls +5.5 %, interior −3 % (plate tone). It survives a 2.5 Mbps H.264 re-encode (−13 % / −15 %).

**Text (paper; colours §5.1).**
| ID | Token | x, y | In | Out |
|---|---|---|---|---|
| ■ (our reading) | 14×14 #5B2EFF | 62, 287 | f1652 (55.067) | end |
| S08-RL 我们的解读 | T-RL · Noto Sans SC 500 40/40 +0.04em ink-p-55 | 90, 274 | f1652 | end |
| S08-R1 / R2 | T-READ · Noto Sans SC 500 56/78 ink-p | 90, 336 / 90, 414 | f1656 / f1660 | end |
| Plate mark | emboss (§7.3) | rect (90,540)–(732,968), r 9 | f1604 → f1652 | end |
| S08-Q | T-ASK · Noto Sans SC 500 44/62 ink-p-78 | 90, 1000 | f1688 (56.267) | end |
| ■ (account) | 16×16 #5B2EFF | 58, 1124 | f1700 (56.667) | end |
| S08-ACC | T-ACC · Noto Sans SC 700 56/56 ink-p | 90, 1104 | f1700 | end |
| S08-SRC1 … SRC7 | T-SRC · Noto Sans SC 500 20/31 +0.02em ink-p-62 (plate numbers Plex Mono 500 20) | 90, 1226 + 31k (k = 0…6) | f1712 + 2k | end |

Last frame **f1771** must read as a complete, shareable card. No RH on paper.
**Sound:** f1604 RELAY + light-table HUM + PAD D major add9 · **f1628 FELT D5 (the 12th note)** · f1700 COIN ting D7 · fade to room by f1771.

### 3.4 Optional soundbite slot (the film is complete without it)

- **One slot only**, at **f380 (A: price war, before S03)** or **f860 (B: changed mind, before S05)**. Length = whole beats, **≤ 8 beats (192 f = 6.4 s)**.
- **To stay ≤ 60 s** when a slot is used, remove 7 beats: drop the S03 token beat (S03-T1/T2; the router starts at f392 instead of f488; −4 beats; the token fact stays on C3), shorten the S05 rise to 36 f and move the annotations to half-beats (−1 beat), drop S06-F2 (−1 beat; it stays on C5), end S08 at B71 (−1 beat). Result ≤ 59.87 s. Everything after the slot shifts by whole beats, so the grid is preserved.
- **Frame:** 16:9 picture 900×506 at (90, 700), colour grade sat 0.80 + film grain, develops in 33 f. RH left reads `原声`. Plex Mono 400 24 bone-5 at (90, 1226): `Satya Nadella · 20VC · 2026.10.26 · 原片 mm:ss`. Subtitles Hei 500 46/64 bone at (90, 1290), ≤ 2 lines of ≤ 18 字, no quotation marks. Hei 500 24 bone-5 at (90, 1424): `字幕为翻译`. Subtitles must be a verified translation of the actual audio.
- **Audio:** dialogue −18 LUFS; music ducks −10 dB with 300 ms ramps; room tone continues.

---

## 4. Carousel 1080×1440 (7 frames)

**Shared furniture.** Margins 90 / 990. RH at **y 96** (T-RH: left `0N / 04␣␣name`, right `20VC · 2026.10.26` right-aligned to 990). Footer at **y 1364**: ■ 12×12 #7A5CFF at (90, 1373) + `Coo-Coo出海Ai实验室` (Noto Sans SC 500 26/30 +0.02em bone-7) at (114, 1364); page index Plex Mono 500 22 +0.08em bone-5, right-aligned to 990, y 1366. Dark frames: ink ground, same grade, post §5.4 (stills: grain 0.030, vignette 0.12, no weave/flicker). Labels use the film's T-CAP tokens.

### C1 · Cover (also the video cover)
| Element | Spec | Position |
|---|---|---|
| Kicker 微软 CEO 纳德拉判断 | Noto Sans SC 500 44/44 +0.04em bone-5 | 90, 120 |
| Date 20VC · 2026.10.26 | Plex Mono 500 24 +0.08em bone-5 | right-aligned to 990, y 132 |
| 大模型 / 要打价格战了 | C-DISPLAY · Noto Serif SC 700 150/162 −0.015em bone | 84, 184 / 84, 346 (line 2 = 900 px wide) |
| Plate | coins.png ×2.00 = 768×606, **full exposure** (house lights up), B/W print | 222, 548 |
| Ring | circle around #16, centre **(647, 934)**, r 58 (stroke centre), **3 px #7A5CFF** — the only colour on the cover | — |
| Label L1 | T-CAP1 `图 01 / 12　古希腊钱币，庞贝出土` | 222, 1174 |
| Label L2 | Plex Mono 400 24 bone-5 `skimage.data.coins()␣␣No.16 / 24` | 222, 1218 |
| Curiosity line | Noto Sans SC 500 40/56 +0.02em bone `11 张公开图，第 12 张是你的。` | 90, 1290 |
| Footer | account only, no page index | 1364 |

Thumbnail behaviour (tested at 180×240 and 360×480, `bible_proofs/_cover_thumb.jpg`): the headline reads first, the coin grid reads as money, the ring is the single point of colour.

### C2 · 01 价格战
| Element | Spec | Position |
|---|---|---|
| Kicker 他判断 | C-KICK40 · Hei 500 40/40 +0.04em bone-5 | 90, 160 |
| 在大多数企业场景里， / 日常算力终将商品化。 | C-ST60 · Noto Serif SC 600 60/77 bone | 90, 216 / 90, 293 |
| Espresso | coffee.png ×1.00 600×400, as film | 390, 420 |
| Label L1 / L2 / L3 | T-CAP1 / T-CAP2 / T-CAP3 (`600 × 400 px · × 1.00`) | 390, 840 / 884 / 918 |
| Kicker 而在他看来 | C-KICK40 | 90, 980 |
| 前沿模型，只服务 / 少数顶级场景。 | C-ST52 · Noto Serif SC 600 52/68 bone | 90, 1036 / 90, 1104 |
| Rocket slit | crop (250,60)–(392,427) ×0.7324 = **104×269**, sharp | 886, 980 |
| Vertical label | Hei 500 24 vertical-rl +0.12em bone-5 `图 03／12　猎鹰 9 号` (digits upright) | box left 850, top 980 |

### C3 · 02 混着用
| Element | Spec | Position |
|---|---|---|
| Kicker 据报道 | C-KICK40 | 90, 160 |
| Statement 3 lines | C-ST60 | 90, 216 / 293 / 370 |
| Plate | coins ×2.00 768×606, dissolve mode, **long exposure of the last five calls**: #17 k 0.22, #11 0.36, #21 0.55, #18 0.78, #16 1.00, fill 0.10 | 222, 500 |
| 示意 line | T-KEY | 222, 1126 |
| 底图 line / scale | T-CAP4 + mono / T-CAP3 `384 × 303 px · × 2.00` | 222, 1172 / 222, 1206 |
| Token line | C-TOK40 · Hei 500 40/56 bone-7 `大模型按 token 计价；英文里，token 也指代币。` (885 px) | 90, 1250 |

### C4 · 03 改过的看法 → 零信任
| Element | Spec | Position |
|---|---|---|
| Hubble band | ×1.08 image at (0, −120), band mask y 140–470, 56 px feathers | full width |
| Kicker 他以前以为 | C-KICK40 | 90, 500 |
| Old belief | C-OLD52 · Noto Serif SC 600 52/68 bone-5 + strike 2.5 px bone-5 (x 85 → 719, centre y 592) | 90, 556 |
| 现在，他不这么想了。 | C-NEW76 · Noto Serif SC 700 76/96 −0.01em bone (760 px, mid-line comma full-width) | 88, 630 |
| Kicker 他说 | C-KICK40 | 90, 800 |
| Statement 2 lines | C-ST52 | 90, 856 / 90, 924 |
| Retina | 208×208 (×0.1474) in a 240×240 rule-30 frame | image 766, 1056 · frame (750,1040)–(990,1280) |
| Notes (outside the frame) | label Hei 700 40/56 bone at x 90; body Noto Serif SC 500 40/56 bone-7 at x 180 | rows y 1048 / 1122 / 1196 |
| Frame label | Hei 500 24 + mono `图 05 / 12　视网膜` | 750, 1296 |

### C5 · 04 私有评测集 (the reveal)
| Element | Spec | Position |
|---|---|---|
| Fact 2 lines | C-FACT44 · Hei 500 44/62 bone | 90, 150 / 90, 212 |
| Header | Plex Mono 400 22 +0.02em bone-5 | 90, 300 |
| Sheet | as film but **row height 150**: slots x 90/405/720, rows y **352 / 582 / 812 / 1042**; thumbs 190, 225, 225 / 172, 150, 150 / 150, 128, 150 / 238 (text crop), 200, window 225×150 | — |
| Captions | T-SHEET (28 px) at y + 160; cell 12: `12␣␣你的评测集` (Hei 30 bone) at y+160, `未公开` at y+196 | — |

### C6 · 04 私有评测集 (his line)
| Element | Spec | Position |
|---|---|---|
| Kicker 纳德拉认为 | C-KICK40 | 90, 170 |
| 每家公司， / 都会有自己的 / 私有评测集。 | C-ST76 · Noto Serif SC 600 76/96 bone | 90, 226 / 322 / 418 |
| 那会是它的核心 IP。 | T-SECOND | 90, 546 |
| The empty plate | 1 px rule-18, corner radius 4, **810×540** | 90, 690 |
| Label L1 / L2 / L3 | as S07 | 90, 1250 / 1294 / 1328 |

### C7 · 我们的解读 + colophon (paper)
| Element | Spec | Position |
|---|---|---|
| Ground | paper #F2EEE7 + paper texture (§7.3); stills grain 0.020, vignette 0.05 | — |
| ■ + 我们的解读 | ■ 14 #5B2EFF at (62,133); T-RL | 90, 120 |
| Page | Plex Mono 500 22 +0.08em ink-p-55 `07 / 07` | right-aligned 990, y 128 |
| Reading 2 lines | T-READ | 90, 184 / 90, 262 |
| Plate mark | emboss §7.3 at rest light (az 135°, el 24°), seed 9 | rect (90,392)–(732,820), r 9 |
| your_eval() | Plex Mono 500 26 +0.02em ink-p-55 | 90, 852 |
| Entry 2 lines | C-ENTRY · Hei 500 40/56 ink-p | 90, 896 / 90, 952 |
| Question | Hei 500 40/56 ink-p-78 | 90, 1030 |
| ■ + account | ■ 14 at (60,1128); C-ACC40 · Hei 700 40/46 ink-p | 90, 1112 |
| Sources | T-SRC, 7 lines | 90, 1180 + 31k |

---

## 5. Design tokens

### 5.1 Colour
| Token | Value | Use |
|---|---|---|
| `--ink` | **#0B0A09** | Dark ground. Photo blacks are lifted to exactly this (never #000). |
| `--bone` | #ECE6DA | Primary type on ink (15.9:1) |
| `--bone-7` | #BDB5A7 | Second sentences, annotation bodies, 示意 line, sheet purposes (9.7:1) |
| `--bone-5` | #8E877B | Kickers, labels, RH, mono (5.5:1) |
| `--rule-30` | rgba(236,230,218,0.30) | Retina frame, cell-12 window |
| `--rule-18` | rgba(236,230,218,0.18) | Plate-12 outline (S07, C6) |
| `--signal` | **#7A5CFF** | Violet on ink: cover ring, carousel footer ■ |
| `--brand` | **#5B2EFF** | Violet on paper: our-reading ■, account ■ (5.55:1 on paper) |
| `--paper` | **#F2EEE7** | S08, C7 |
| `--ink-p` | #15121B | Type on paper |
| `--ink-p-78` / `-62` / `-55` | rgba(21,18,27,.78 / .62 / .55) | Question / sources / labels on paper |
| `--halation` | #FF6A3D (1.00, 0.42, 0.22) | Photo layer only, never type |
| `--glint` | #F4EEDC | S01 glint only |

**Violet budget.** Film: exactly two marks, both in S08 (our-reading ■, account ■). Carousel: C1 ring, footer ■ on C1–C6, two ■ on C7. Violet is never text, never a fill area, never a glow.

### 5.2 Type
Faces (installed, verified): **Noto Serif SC** 500/600/700, **Noto Sans SC** 500/700, **IBM Plex Mono** 400/500. Nothing else.

| Token | Face · weight | Size / line-height (px) | Tracking | Colour |
|---|---|---|---|---|
| T-DISPLAY | Serif 700 | 148 / 163 | −0.015em | bone |
| C-DISPLAY | Serif 700 | 150 / 162 | −0.015em | bone |
| T-BIG | Serif 700 | 112 / 125 | −0.01em | bone |
| C-ST76 / C-NEW76 | Serif 600 / 700 | 76 / 96 | 0 / −0.01em | bone |
| T-ST | Serif 600 | 72 / 91 | 0 | bone |
| T-ST64 | Serif 600 | 64 / 83 | 0 | bone (OLD → bone-5) |
| C-ST60 | Serif 600 | 60 / 77 | 0 | bone |
| T-SECOND | Serif 500 | 56 / 75 | 0 | bone-7 |
| C-ST52 / C-OLD52 | Serif 600 | 52 / 68 | 0 | bone / bone-5 |
| T-NOTE / C-NOTE40 | Serif 500 | 44 / 62 · 40 / 56 | 0 | bone-7 |
| T-FACT | Sans 500 | 52 / 74 | 0 | bone |
| T-FACT46 / C-FACT44 | Sans 500 | 46 / 65 · 44 / 62 | 0 | bone |
| T-READ | Sans 500 | 56 / 78 | 0 | ink-p |
| T-KICK | Sans 500 | 44 / 44 | +0.04em | bone-5 |
| C-KICK40 / T-RL | Sans 500 | 40 / 40 | +0.04em | bone-5 / ink-p-55 |
| T-NOTE-L / C-NOTE-L40 | Sans 700 | 44 / 62 · 40 / 56 | +0.02em | bone |
| T-ASK | Sans 500 | 44 / 62 | 0 | ink-p-78 |
| T-ACC / C-ACC40 | Sans 700 | 56 / 56 · 40 / 46 | 0 | ink-p |
| C-ENTRY / C-TOK40 / curiosity | Sans 500 | 40 / 56 | 0 (curiosity +0.02em) | ink-p / bone-7 / bone |
| T-KEY | Sans 500 | 32 / 45 | +0.04em | bone-7 |
| T-CAP1 | Sans 500 + Mono 500 numbers | 30 / 42 | +0.04em / +0.02em | bone-5 |
| T-SHEET | Mono 500 index + Sans 500 purpose | 28 / 34 | +0.02em | bone-5 / bone-7 |
| T-RH | Mono 500 24 + Sans 500 26 | 24 / 24 | +0.08em / +0.06em | bone-5 |
| T-CAP2 / T-HDR | Mono 400 (+ Sans 500) | 24 / 34 | +0.02em (+0.04em) | bone-5 |
| T-CAP4 | Sans 500 | 24 / 34 | +0.04em | bone-5 |
| T-VCAP | Sans 500 vertical-rl (+ Mono 400 24 sideways line) | 30 | +0.12em | bone-5 |
| T-CAP3 | Mono 400 | 22 / 31 | +0.02em | bone-5 |
| T-SRC | Sans 500 + Mono 500 numbers | 20 / 31 | +0.02em | ink-p-62 |

**CJK typesetting rules (tested in this repo's Chromium).**
1. `font-feature-settings: normal` — **no `halt`, no `palt`, no `chws`**; `text-spacing-trim: space-all`. Every comma, full stop and semicolon is full-width, mid-line and at line end.
2. `text-autospace: no-autospace`; CJK–Latin spaces are the literal U+0020 in the copy (微软 CEO, 按 token 计价, Copilot 内部, 核心 IP, 每个 agent). Never both.
3. One element per line, `white-space: pre`; no browser wrapping. No line starts with punctuation. Display lines ≥ 96 px carry no line-end punctuation except the final 。 (S04-N1 `现在` is deliberately bare).
4. Never put CJK (including U+3000 `　`, U+FF0F `／`, full-width punctuation) inside a Plex Mono span. Split spans.
5. Vertical caption: `writing-mode: vertical-rl; text-orientation: mixed`; wrap `03`, `12`, `9` in spans with `text-combine-upright: all`; Latin (DSCOVR) runs sideways.
6. Optical indents: 148–150 px display at x 84; 112 px at x 86; 76 px at x 88; everything else at x 90.
7. Two-pass font loading (mandatory): for every element, `await document.fonts.load('<weight> <size>px "<family>"', text)`, then `await document.fonts.ready`, then assert `document.fonts.check(...) === true` for every element, then render. Abort the render if any check fails (lazy unicode-range subsets otherwise fall back to WenQuanYi).
8. No text shadows, outlines, gradients, glows, underlines or tracking animation. The strike (S04, C4) is the only line drawn through type.

### 5.3 Grid
- **Film:** text axis x 90, right margin 990. Plates hang from the right margin (S02 espresso 390–990, slit 706–990, S03 tray 222–990, S05 frame 504–990) or run full-bleed (S04 band) or sit on the 3-slot sheet (S06). Vertical zones: 0–199 empty · RH 220 · statements 330–760 · plates 536–1460 · labels end ≤ 1466 · nothing essential ≥ 1477.
- **Kicker rhythm:** kicker top + 66 = first statement line; statement pitches 91 / 83 / 125 px; label lines +44 / +34 / +31.
- **Fixed anchors:** coin #16 = crema centre (678, 1000); slit x 706–990; sheet slots 90/405/720; plate-12 rect (42,600,996×664) → paper (90,540,642×428).
- **Carousel:** margins 90/990; RH 96; kickers 120–170; footer 1364.

### 5.4 Texture and finishing (whole frame, after type)
Implemented by `f2/film.py` with `f2/prod/look.json`:

```json
{"default": {"grain": 0.034, "grain_size": 1.35, "grain_chroma": 0.0,
             "halation": 0.0, "bloom": 0.0, "bloom_radius": 120, "ca": 0.0,
             "vignette": 0.14, "vig_round": 1.0, "weave": 0.45, "flicker": 0.006,
             "lift": 0.0, "gain": 1.0, "print_bloom": 0.20, "print_bloom_sigma": 0.6},
 "keys": [{"t": 53.467, "grain": 0.034, "vignette": 0.14, "bloom": 0.0},
          {"t": 53.867, "bloom": 0.18},
          {"t": 54.267, "grain": 0.022, "vignette": 0.05, "bloom": 0.0}]}
```

- **Print bloom (add to film.py):** before grain, `img = img·(1 − m) + Gauss(img, σ 0.6 px)·m`, m = 0.20. Kills the razor-digital type edge.
- **Grain:** monochrome, σ 0.034 at mid-grey (paper 0.022), generated at 1/1.35 resolution and upsampled, response `(4L(1−L))^0.7·0.85 + 0.15`, reseeded every frame, never stops (including f764–f775). Never scaled with an image.
- **Halation:** per plate in prep (§7), never in post, never on type.
- **Vignette:** 0.14 elliptical (follows frame aspect), paper 0.05.
- **Gate weave:** ≤ 0.45 px x, 0.36 px y (film.py sines). **Flicker:** ±0.6 %.
- **Letterbox:** none. The Hubble band is a plate mask, not bars.
- **Not used:** chromatic aberration, light leaks, dust, scratches, film burns, lens flares, bloom on type (except print bloom), scan lines.
- **Stills (carousel):** `film.py --still` with grain 0.030, vignette 0.12, weave 0, flicker 0, print bloom 0.20; C7 grain 0.020, vignette 0.05.

### 5.5 Micro-detail system (each has one job)
1. **Plate label** (museum label, 3 lines): `图 NN / 12　title` · `library call　docstring purpose` · `W × H px · × S.SS`. Under or beside every plate from its first appearance (S01, S02, S03, S04, S05, S07).
2. **Global numbering:** 01 coins · 02 coffee · 03 rocket · 04 Hubble · 05 retina · 06 camera · 07 astronaut · 08 Grace Hopper · 09 moon · 10 text · 11 clock · **12 yours**. "/ 12" from frame 66 plants the empty twelfth.
3. **Honest-scale readout:** Plex Mono, two decimals, `×` U+00D7, `·` U+00B7. Updates every frame during pushes (changes only when the rounded value changes), **freezes at the hard stop**.
4. **Running head:** chapter `0N / 04␣␣name` left, `20VC · 2026.10.26` right; changes roll in 11 f (old −12 px out, new from +12 px; E-ROLL), only the changing part rolls.
5. **Vertical caption** for the vertical plate (rocket): native CJK vertical setting; Hei column 24 px from the plate edge, mono column 14 px further out.
6. **Hairlines** mean absence or boundary only: retina frame, cell-12 window, plate-12 outline. Photographs are borderless prints.
7. **■ markers** hang at x 58–62, 28–32 px outside the text axis.
8. **The strike:** 3 px (film) / 2.5 px (C4) in the struck text's own colour, through the CJK centre, 5–6 px overhang on both sides; appears in 2 frames.
9. **The withheld element:** the empty cell, the missing 12th note, `not in any library` — three channels, one meaning.
10. **Specimen number** `No.16 / 24` (cover only).

---

## 6. Motion system

### 6.1 Easing tokens
| Token | cubic-bezier | Duration | Use |
|---|---|---|---|
| E-FADE | (.33, 0, .2, 1) | 16 f | Text opacity in; cell captions (12 f) |
| E-SETTLE | (.16, 1, .3, 1) | 22 f (text) · 60 f (retina rise) | Text rise +10 → 0 px; retina vertical rise |
| E-LEAVE | (.7, 0, .84, 0) | 12 f | Text out, outline/frame fades |
| E-ROLL | (.2, 0, 0, 1) | 11 f | Running head roll |
| E-DEVELOP | (.22, .61, .36, 1) | 33 f colour · 39 f B/W · 30 f slit · 15 f sheet cell | Develop in/out |
| E-FOCUS | (.33, 0, .15, 1) | 44 f | Rack focus + breathing |
| E-GLINT | (.2, .6, .3, 1) | 8 f | Hook glint |
| E-SNAP | (.7, 0, .2, 1) | 27 f | Slit opening |
| E-HOP | (.5, 0, .2, 1) | 4 f travel + 8 f hold | Router light |
| E-ACCEL | (.5, 0, 1, 1) | 120 f | Hubble push into the stop |
| E-RISE | (.25, .1, .25, 1) | 60 f | Retina terminator |
| E-TRAVEL | (.65, 0, .35, 1) | 30 f | Retina contain move |
| E-DRAW | (.45, 0, .2, 1) | 16 f frame · 12 f cell-12 window | Hairline draws |
| E-REVEAL | (.83, 0, .17, 1) | 48 f | Sheet pull-back |
| E-DIVE | (.6, 0, .1, 1) | 40 f | Plunge into plate 12 |
| E-LAMP | (.4, 0, .2, 1) | 24 f | Lamp-up |
| E-SETTLE-L | (.22, 1, .36, 1) | 48 f | Paper pull-out |
| E-RAKE | (.45, 0, .55, 1) | 48 f | Raking light sweep (symmetric: midpoint = f1628) |
| E-DRIFT | linear | whole shot | Rostrum drifts |

Never: bounce, overshoot, elastic, springs, per-glyph animation, rotation of text, text scale-pops.

### 6.2 Stagger and rhythm
Kicker → first statement line +6 f · line → line +4 f · label lines +4 f · annotation label → body +4 f · sheet cells 3 f · source lines 2 f. Text enters on beats or on picture events (develop done, light landed, frame drawn), never on a uniform timer. Reading load ≤ 6.3 字/s of visible time (kickers excluded); every statement ≥ 2.0 s; every paused frame shows a kicker + its statement.

### 6.3 Text reveal technique
- **In:** whole line box, opacity 0 → 1 (E-FADE 16 f) and translateY +10 → 0 (E-SETTLE 22 f). No blur, no tracking change, no scale, no mask wipe, no typing.
- **Out:** opacity → 0 (E-LEAVE 12 f), no movement.
- **Exceptions (deliberate):** S01 kicker + headline are static from f0; the hard-stop print-on (2 frames, 50 % then 100 %); RH roll; sheet captions fade without rise.

### 6.4 Photo move technique
- **Rostrum only:** scale + translate in the picture plane. No rotation, no 3D, no camera shake. Drifts are constant-velocity (E-DRIFT) at ≤ 1.5 %/s. Large scale changes interpolate in log space with the anchor-point formula (§3.3 S06/S07/S08).
- **Parallax** only in Hubble (two layers, FG 50 % faster than BG).
- **Develop (every plate's entrance):**
  ```glsl
  float L = dot(c.rgb, vec3(.2126,.7152,.0722));
  float g = grain(fragCoord/1.35, frame) - .5;            // same grain field as post
  float e = 1.0 - 1.15*E_DEVELOP(t);                      // threshold sweeps bright -> dark
  float a = smoothstep(e - .10, e + .02, L + g*.12);
  vec3 col = mix(INK, c.rgb, a) + hal*(0.8*(1.0 - E_DEVELOP(t)))*step(.8, L);  // hal = the plate's own halation glow layer: highlights flare, then settle
  ```
  Develop-out: `e = -0.15 + 1.15*E_DEVELOP(t)` (shadows vanish first).
- **Light** is the animated property: key/fill maps (S01, S03), the glint, the terminator, the raking light. We select with light, never with boxes, arrows, rings or cursors (the cover ring is a still editor's mark, carousel only).
- **Focus:** only the S01 rack focus.
- **Motion blur:** 5 sub-frame samples over a 180° shutter, averaged in linear light, only on frames where anything moves > 8 px/f (slit, light travel, contain, pull-back, plunge, pull-out).

### 6.5 Transition technique
- Hard cuts on B-frames, each on a sound event: f116 (graphic match), f380, f644, f860.
- Continuous moves: the slit (inside S02), contain (inside S05), pull-back (S05→S06), plunge (S06→S07), lamp-up + pull-out (S07→S08).
- One deliberate violation of continuity: the hard stop.
- Photographs never cross-dissolve, wipe, slide, whip-pan, zoom-blur or glitch.

---

## 7. Image recipes

### 7.1 Global rules
- **Grade (colour, "warm print"):** in sRGB values: saturation (per asset) → curve `y = lift + (gain − lift)·x^γ` with **lift 0.043** (= #0B0A09), **γ 1.06**, **gain 0.94**, soft shoulder above 0.82 (`y = 0.82 + (1 − e^{−(y−0.82)/0.18·1.4})·(gain − 0.82)/(1 − e^{−1.4})`) → warm tone: shadows ×(1.04, 1.00, 0.94), highlights ×(1.02, 1.00, 0.95), blended by w = clamp(1 − 2L). No teal/orange split.
- **Grade (B/W, "selenium print"):** `curve(g; lift 0, gain 1, γ 1.06, shoulder 0.82)` then 3-stop ramp **#0C0B0A (0) → #8C857A (0.5) → #EDE6D6 (1)**. No halation on B/W plates.
- **Halation (colour plates only):** mask = clamp((L − thr)/(1 − thr)), Gaussian σ 10 px at display size, tint (1.00, 0.42, 0.22), additive strength 0.22 (retina 0.28).
- **Resampling:** Lanczos. Upscales (> ×1.05) get unsharp mask radius 0.8×scale px, 45 %, threshold 2. Downscales get nothing.
- **Keeping small photos crisp and intentional:** respect the max scale table; prefer native or downscaled display; add grain at output resolution after scaling; deblock JPEG skies before upscaling; declare scale in the label; reserve the only > ×2.06 moment (S01) for dissolve mode under defocus and drift; inspect every plate at 1:1 for halos, ringing and blocks. No AI upscaling, no invented detail, no mirroring, cloning or extension of any image.

### 7.2 Per-asset table
| Asset (source) | Used in | Crop (source px) | Display / scale | Max | Grade and treatment |
|---|---|---|---|---|---|
| **coins.png** 384×303 gray | S01, S03, S06 cell 01, C1, C3, C5 | full | S01 ×2.43→2.40→2.46 (dissolve); S03 ×2.00→2.02 (dissolve); C1/C3 ×2.00; sheet 215×170 / 190×150 | ×2.46 dissolve only; full-exposure holds ×2.00 | B/W. **Matte = the textbook skimage segmentation:** Sobel elevation, watershed with markers < 30 (bg) / > 150 (coin), fill holes, Gaussian feather σ 0.8 src px → 24 coins (App. A). Light maps per §3.3. |
| **coffee.png** 600×400 | S02, sheet 02, C2, C5 | full; crema centre (288,140), semi-axes 88×50 | ×1.00→1.02 (600×400); sheet 255×170 / 225×150 | ×1.5 | Colour, sat 0.84, halation thr 0.80 |
| **rocket.jpg** 640×427 | S02 slit, sheet 03, C2 | slit **(250,60)–(392,427)**; vehicle x ≈ 314–329, nose y ≈ 127 | ×2.00→2.06 (284×734); C2 ×0.7324 (104×269); sheet 255×170 | ×2.06 | **Deblock first:** L = mean RGB; g = \|∇ Gauss(L, 1.0)\|; mask = (g < 0.012) and row < 330; mask = Gauss(mask, 2); out = mix(src, Gauss(src, 1.4), mask). Then colour, sat 0.74, halation thr 0.78. No lamp twinkle. |
| **hubble_deep_field.jpg** 1000×872 | S04, sheet 04, C4 | full; anchor galaxy (727,473) | ×1.08 base, BG ×1.06 / FG ×1.09 push; sheet 195×170 | ×1.20 | Colour, sat 0.86, halation thr 0.62. **FG mask:** L > 0.30 after Gauss 2 px (display), dilate 3 px, feather 2 px. **BG fill:** 15 px median into FG holes. Never mirrored or extended. |
| **retina.jpg** 1411×1411 | S05, sheet 05, C4 | full; disc centre (704,703), Ø ≈ 1390; optic disc (233,655); fovea (702,705) | ×0.5301 (748) → ×0.3104 (438); sheet 170; C4 208 | ×1.36 (never upscaled here) | Colour, sat 0.86, halation thr 0.70, strength 0.28; keep the notch; terminator §3.3 |
| camera.png 512² gray | sheet 06 only | full | 170 (×0.332) | — | B/W. Never a hero image (private person). |
| astronaut.png 512² | sheet 07 only | full | 170 | — | Colour sat 0.82. Never cropped, never captioned beyond 示例图. |
| grace_hopper.jpg 512×600 | sheet 08 only | full | 145×170 | — | Colour sat 0.82. Never cropped. |
| moon.png 512² gray | sheet 09 only | full | 170 | — | B/W; keep its low contrast (its test is histogram equalisation) |
| text.png 448×172 gray | sheet 10 only | **(87,0)–(360,172)** (the only cropped thumbnail) | 270×170 (×0.9884) | — | B/W |
| clock_motion.png 400×300 gray | sheet 11 only | full | 227×170 | — | B/W |
| earth-*, hdri_* | **not used** | — | — | — | They are not test images; using any would make "这 11 张" false. |

### 7.3 Paper and the intaglio plate mark (S08, C7)
Reference implementation (numpy; the shader must match within ±1 % luminance):
```python
# paper
low = gauss(randn(H,W), 48); low /= low.std()
f   = randn(H,W)
fib = 0.7*gauss(f, (0.7, 2.2)) + 0.3*gauss(f, (2.2, 0.7)); fib /= fib.std()   # (sigma_y, sigma_x)
albedo = PAPER * (1 + 0.008*low + 0.0025*fib)                                    # PAPER = #F2EEE7
# rounded-rect signed distance, corner radius 9 (inside < 0)
t = smoothstep01(0.5 - sd/14.0)                       # wall width 14
h = -0.8*t + 0.22*0.8*exp(-((sd - 8.4)/12.6)**2)*(sd > 0)   # recess + squeezed-paper ridge outside
h = gauss(h, 4.0)                                     # rounded shoulders, no hard rim
h += 0.006*fib*(1 - 0.65*t)                           # fibres pressed flat inside
n = normalize(-dh/dx, -dh/dy, 1)
L = (cos az·cos el, -sin az·cos el, sin el)           # az from screen-right, counter-clockwise
shade = clip(dot(n, L)/L.z, 0.70, 1.25)
wipe = gauss(randn(H,W), (30, 90)); wipe /= wipe.std()      # hand-wiped plate tone
albedo *= (1 - 0.018*(1 + 0.35*wipe)*t) * (1.0, 0.995, 0.985)**t
out = min(albedo*shade, 0.985)
```
All px parameters (14, 8.4, 12.6, 4.0, 9) scale with plate width / 642 during the S08 pull-out. Rounded corners, a soft shoulder, a faint ridge of squeezed paper just outside the edge, a faint warm plate tone inside, pressed fibres. It must never look like a CSS bevel (no mitred corners, no uniform rim, no hard light/dark lines).

---

## 8. Sound design (all synthesized, 48 kHz / 24-bit, built on `f2/synth.py`)

### 8.1 Instruments
| Name | Recipe |
|---|---|
| ROOM | Pink noise, band-pass 60 Hz–6 kHz, −46 dBFS RMS, ±1.5 dB wander at 0.05 Hz; stereo from two noises at 0.7 correlation |
| COIN | `coin_ping(freq)`: modes ×1.000/1.594/2.136/2.653/3.156/4.06, decays 0.9/0.7/0.55/0.45/0.35/0.25 s, 1.5 ms (tick) or 4 ms (flick) noise excitation, 0.4 % pitch settle. τ×0.6 for router pings |
| WHIRR | Band-passed noise 4–8 kHz, amplitude-modulated at the spin rate 14 → 9 Hz, −30 dBFS RMS |
| RATTLE | Tick train at instantaneous rate Ω(t) = 9 Hz·((1.467 − 0.5)/(1.467 − t))^{1/3}, capped 32 Hz, ±3 % jitter; each tick = 1.5 ms noise BP 3–7 kHz (−18 dB) + COIN D7 τ×0.1 (−28 dB) + 180 Hz "table" sine 8 ms (−26 dB); ticks −24 → −18 dBFS |
| CLACK | 3 ticks within 12 ms + 120 Hz sine 40 ms + COIN D7 τ×1.5; −10 dBFS peak |
| DRONE | `drone()` voices on D1 36.71, D2 73.42 (+ copy at +0.15 Hz), A2 110.00; low-pass 900 Hz (automatable), LFO 0.07 Hz ±2 dB; −30 dBFS RMS |
| FELT | `felt_piano(freq, dur 4–6 s, vel, bright 0.4)`; 30 % reverb send |
| BLOOM | `whoosh(0.9 s, 250 → 1600 Hz, peak 0.6)` on pink noise, −34 dBFS; reverse version for the pull-back |
| SLIT | Band-pass noise sweeping 300 → 1800 Hz over 0.9 s, −28 dBFS RMS |
| SHIMMER | Sines A6 1760 + E7 2637.02, 3 s Gaussian envelope, −44 dBFS (S02); sines D5 587.33 + A5 880, −36 → −28 dBFS (S04 push) |
| SUB | `sub_hit(f0 52 → f1 32 Hz, decay 0.45 s)`, −14 dBFS peak (plunge); swell version 32 → 45 Hz over 2 s (retina) |
| PAD | Additive voices (8 partials, 1/n²), ±3 cents ×3, attack 0.8–1.0 s, low-pass 3 kHz. B♭ (S05): B♭2 116.54 / F3 174.61 / D4 293.66 at −30 RMS. D major add9 (S08): D3 146.83 / A3 220.00 / F♯4 369.99 / E5 659.26 at −24 RMS |
| STAMP | Modal click f0 900 Hz, ratios 1 / 2.76 / 5.40, decays 40/20/10 ms + 140 Hz knock (30 ms); −26 dBFS |
| DRAW | Band-pass noise 3–7 kHz, envelope = the hairline's draw velocity (derivative of E-DRAW), −40 dBFS |
| RISER | Pink noise, low-pass 300 → 3000 Hz (exponential) over 1.333 s, −30 → −22 dBFS, hard cut |
| RELAY | Two clicks 18 ms apart (1.2 ms noise, BP 2–5 kHz) + 80 Hz thump 25 ms; −28 dBFS |
| HUM | Light table: 100 / 200 / 300 Hz sines at −46 / −52 / −58 dBFS, 0.5 Hz ±1 dB wobble, 0.3 s fade-in |
| REVERB | `reverb_ir(2.2 s music / 1.0 s coin)`, pre-delay 12 ms, damping 4.5 kHz; wet −14 dB (piano), −18 dB (coin) |

### 8.2 Cue sheet (sample-locked: sample = round(f × 1600))
| Frame (s) | Picture | Cue |
|---|---|---|
| f0 (0.000) | title over defocused coins | ROOM fades in over 0.25 s |
| f1 (0.033) | — | COIN flick **D7 2349.3 Hz**, −14 dBFS, pan +0.15 |
| f2–f15 (0.067–0.500) | rack focus | WHIRR |
| f15–f44 (0.500–1.467) | rack focus | RATTLE accelerating to 32 Hz |
| **f44 (1.467)** | **focus lands, glint** | **CLACK** |
| f44–f53 | headline holds | near silence: ROOM + clack tail |
| f53 (1.767) | sub-line | DRONE in (1.5 s fade) |
| f54 (1.800) | — | FELT D3 146.83, vel 0.50, −22 dBFS |
| f116 (3.867) | crema develops | BLOOM + FELT A3 220.00 |
| f244 (8.133) | espresso dims | DRONE low-pass 900 → 500 Hz over 0.4 s |
| f260 (8.667) | slit opens | SLIT + FELT E4 329.63, vel 0.55 |
| f272 (9.067) | rocket at dusk | SHIMMER A6 + E7 |
| f380 (12.667) | coin #16 returns | COIN **D6 1174.66** (#16's own pitch), −24 + BLOOM −36; DRONE low-pass back to 900 Hz |
| f488 … f620, every 12 f | router hops 1–12 | PING at each landing: F5 C6 G5 D6 F6 G6 F6 D6 C6 G5 D5 **D6** (−22 dBFS; last −20), panned per §3.3 S03 |
| f644 (21.467) | Hubble develops; push | BLOOM + FELT F3 174.61; DRONE −30 → −24 and SHIMMER D5+A5 −36 → −28 (exponential to f764) |
| **f764 (25.467)** | **hard stop** | **every track, reverb tails included, to digital zero** |
| f764–f775 (0.400 s) | frozen camera, live grain | exact zeros |
| f776 (25.867) | — | ROOM back at −50 dBFS (2 ms fade) |
| f777 (25.900) | 现在 / 他不这么想了。 | FELT D2 73.42, vel 0.6, decay ×1.5, −20 dBFS |
| f860 (28.667) | planet rises | SUB swell 32 → 45 Hz + PAD B♭ |
| f962 (32.067) | frame draws | DRAW |
| f980 / f1004 / f1028 | 身份 / 记录 / 权限 | STAMP ×3, pan −0.35 |
| f1124–f1172 | pull-back | reverse BLOOM (space opening), ends at f1172 |
| f1154 + 3k, k = 0…10 | cells 01–11 | **FELT D4 A4 E5 · B♭3 F4 C5 · F4 C5 G5 · C4 G4** (293.66 440 659.26 · 233.08 349.23 523.25 · 349.23 523.25 783.99 · 261.63 392.00), −24 → −20 dBFS |
| **f1187 (39.567)** | cell 12 draws | **no note**; DRONE dips −6 dB for 18 f |
| f1388–f1428 | plunge | RISER, hard cut at f1428 |
| f1428 (47.600) | inside the plate | SUB −14 dBFS; ROOM −52; DRONE reduced to D1 at −34 |
| f1444 (48.133) | 每家公司… | FELT dyad A3 + E4, −24 |
| f1592 (53.067) | darkness, outline only | DRONE fades out over 12 f |
| f1604 (53.467) | lamp-up | RELAY + HUM in + PAD D major add9 (the film's first F♯) |
| **f1628 (54.267)** | **raking light crosses the plate** | **FELT D5 587.33, vel 0.75, −18 dBFS — the withheld 12th note** |
| f1700 (56.667) | account mark | COIN ting D7 2349.3, τ×0.8, −30 (frame-0 callback) |
| f1712–f1771 | hold | PAD + HUM fade to ROOM; ROOM ends at f1772 |

Harmonic plan: D minor (drone, piano, router pentatonic D F G A C, sheet arpeggio i–VI–III–VII) resolving to **D major add9** only on paper.

### 8.3 Mix and export
Integrated **−16 LUFS ±0.5**, true peak ≤ **−1.0 dBTP** (4× oversampled check). Loudest events: CLACK and the plunge SUB. Mono-compatible (check PAD and ROOM summed). WAV 48 kHz/24-bit → AAC-LC 256 kbps in the MP4. No sidechain pumping. Router pings panned by coin x (pan = (x − 540)/540 × 0.6).

---

## 9. Never do (specific to this piece)

1. No 3D, no Three.js, no CG coin, no reconstructed object. Every pixel of picture comes from the eleven library images, paper, light, or a hairline.
2. Never present a treated frame as an untreated photograph: the router frame always carries `示意`; every label declares its scale.
3. No Earth maps, globes, HDRI backgrounds, stock or generated images. The number 11 must stay exact.
4. No text entrance with blur, tracking, scale, mask wipes, per-glyph stagger or typing. No text shadows, glows, outlines, gradients.
5. No `halt`/`palt`; no half-width Chinese punctuation; no quotation marks; no hype words; no exclamation marks; no emoji or icons; no arrows on screen.
6. No LXGW WenKai, ZCOOL, Inter, Geist, Anton, Instrument Serif, Fraunces. No CJK (including `　` and `／`) inside Plex Mono.
7. Violet never as text, fill, glow or gradient; never more than the budget in §5.1.
8. No boxes around text, cards, panels, drop shadows, rounded containers. Hairlines only for the retina frame, the cell-12 window and the plate-12 outline.
9. No HUD vocabulary: rings on coins in the film, weekday labels, 闭源/开源 tags, crosshairs, corner brackets, gauges, timestamps, IDs, scan lines. The scale readout is the only live number.
10. No upscaling beyond §7.2 maxima, no AI upscaling, no sharpening halos, no mirroring or extending (Hubble), no crops of people, camera.png never as a hero.
11. No cross-dissolves between photographs, wipes, slides, whip pans, zoom-blur transitions, glitch, light leaks, chromatic aberration, lens flares, dust, letterbox bars.
12. No bounce/overshoot/elastic easing; no rotating text; no tilted or 3D-rotated photos; no camera shake.
13. No particles, glows, bokeh overlays (the only bokeh is the real rack focus), decorative gradients, purple ground.
14. No `三件事` / `给创业者的 N 个动作` list and no `你的产品，现在接了几家模型？` in the film (both are the rejected F frames); no `评论区聊聊` on screen.
15. No pure #000 or #FFF; photo highlights ≤ 0.94, paper ≤ 0.985.
16. Never attribute the excluded lines; never claim a licence beyond SRC3–SRC7; never name coin types or mints.
17. The emboss must never read as a CSS bevel or an empty image placeholder.
18. Grain never scales with an image and never stops (not even at the hard stop).
19. Never centre a text block; the only centred object is the retina during its rise.
20. Never time every shot or every text the same; never animate text without a picture or sound reason.

---

## 10. QA checklist (renders must pass every item)

**Type and copy**
- [ ] Every string matches §2 character-for-character (diff the render's text log against the deck).
- [ ] Two-pass font load done; `document.fonts.check` true for every element on every rendered frame range; one frame per shot visually checked for WenQuanYi fallback glyphs.
- [ ] No CJK code point (U+3000–303F, U+4E00–9FFF, U+FF00–FFEF) inside any Plex Mono span.
- [ ] All Chinese punctuation full-width; no `halt`/`palt` in computed styles; `text-autospace: no-autospace`; zero quotation marks on screen.
- [ ] Every Nadella line under its kicker; ■ 我们的解读 present on S08 and C7; account mark and SRC1–SRC7 on S08 and C7.

**Layout and legibility**
- [ ] No essential element at y < 200 or y > 1476; essential text inside x 64–1000, and ≤ x 940 in y 1150–1476. Check every shot on a phone mock with the XHS overlay.
- [ ] Minimum sizes: Chinese body ≥ 44 px; labels ≥ 24 px (scale line 22 px mono); sources 20 px; contrast bone-5 ≥ 5.5:1 on ink, ink-p-62 ≥ 4.5:1 on paper.
- [ ] Reading rate ≤ 6.3 字/s; paused frames sampled every 15 frames are complete (kicker + statement, or label).
- [ ] Positions match §3–§4 within ±1 px (compare against `bible_proofs/` layouts).

**Timing**
- [ ] 1772 frames at 30 fps CFR (59.067 s). All cuts at f116, f380, f644, f860; continuous moves at f260, f932, f1124, f1388, f1604.
- [ ] Event log from `renderAt` equals the frames in §3 (text in/out, hops, develops, draws).
- [ ] Hard stop: camera transform identical on f764–f859; grain and weave still change frame to frame.
- [ ] Audio events sample-locked (sample = f × 1600); exact digital zeros f764–f775; no note at f1187; D5 at f1628.

**Images**
- [ ] Logged effective scale per plate per frame ≤ §7.2 maxima (S01 ≤ 2.46, slit ≤ 2.06, Hubble ≤ 1.18, retina ≤ 0.53, thumbnails ≤ 1.0).
- [ ] 1:1 inspection: no halos, no ringing, rocket sky free of JPEG blocks, no mirrored or extended regions, people uncropped.
- [ ] Develop order visible (crema first, stars first, lamps first); terminator ends on the untreated retina by f920.
- [ ] Re-run App. C verification (10 × max diff 0; Grace Hopper sha256).

**Colour and texture**
- [ ] Violet count matches §5.1 exactly (film: two ■ in S08 only).
- [ ] Ink ≥ (11,10,9) before grain on dark frames; paper highlights ≤ 0.985; grain present in every frame.
- [ ] Emboss at rest (f1700): top/left walls −13…−17 %, bottom/right +4…+7 %, interior −2…−4 %; after a 2.5 Mbps H.264 re-encode, top/left walls still ≤ −12 %.

**Sound**
- [ ] −16 LUFS ±0.5 integrated, true peak ≤ −1.0 dBTP, no clipping, mono-compatible.

**Encode and platform**
- [ ] Master: H.264 High, 1080×1920, 30 fps, yuv420p, CRF 16, preset slow, `-tune grain`, BT.709 tags, `+faststart`; AAC-LC 256 kbps 48 kHz.
- [ ] Private XHS test upload: no blotching or banding in dark grain (if it blotches, raise `grain_size` to 1.5, do not lower σ); first 1.5 s checked on a phone.
- [ ] Cover (C1) checked at 180×240 and 360×480: headline legible, coins read as money, ring visible.
- [ ] Carousel: 7 files 1080×1440, correct order and page numbers, C5 captions legible on a phone at 100 %.

---

## Appendix A · Coin table (watershed segmentation of coins.png)

Row-major order (row bands of 60 px, then x). Pitch: target MIDI = 74 + 18·(r_max − r)/(r_max − r_min), r_max 31.6, r_min 18.5, quantised to **D minor pentatonic** {D, F, G, A, C}.

| # | cx | cy | r | Note | Hz | | # | cx | cy | r | Note | Hz |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 01 | 44.2 | 54.4 | 20.8 | F6 | 1396.91 | | 13 | 43.7 | 197.4 | 18.9 | G6 | 1567.98 |
| 02 | 100.2 | 56.1 | 18.7 | G6 | 1567.98 | | 14 | 101.7 | 195.6 | 21.6 | F6 | 1396.91 |
| 03 | 155.3 | 50.8 | 22.9 | D6 | 1174.66 | | 15 | 154.1 | 197.7 | 19.1 | G6 | 1567.98 |
| 04 | 215.2 | 51.1 | 22.7 | D6 | 1174.66 | | **16** | **212.4** | **193.1** | **23.5** | **D6** | **1174.66** |
| 05 | 276.1 | 52.4 | 19.7 | G6 | 1567.98 | | 17 | 273.5 | 193.6 | 21.8 | D6 | 1174.66 |
| 06 | 334.7 | 43.5 | 28.8 | F5 | 698.46 | | 18 | 347.0 | 186.7 | 31.6 | D5 | 587.33 |
| 07 | 44.7 | 124.3 | 20.3 | F6 | 1396.91 | | 19 | 45.9 | 259.8 | 28.0 | G5 | 783.99 |
| 08 | 102.3 | 125.6 | 18.8 | G6 | 1567.98 | | 20 | 113.9 | 265.5 | 21.2 | F6 | 1396.91 |
| 09 | 153.5 | 127.2 | 18.5 | G6 | 1567.98 | | 21 | 172.3 | 261.2 | 27.4 | G5 | 783.99 |
| 10 | 205.3 | 123.7 | 19.6 | G6 | 1567.98 | | 22 | 244.0 | 263.3 | 23.7 | C6 | 1046.50 |
| 11 | 270.6 | 118.8 | 24.7 | C6 | 1046.50 | | 23 | 300.6 | 263.2 | 25.2 | C6 | 1046.50 |
| 12 | 336.2 | 124.5 | 19.3 | G6 | 1567.98 | | 24 | 358.2 | 267.9 | 21.7 | F6 | 1396.91 |

Hero = **#16** (the facing head). Hook: screen (678, 1000) at ×2.40, r 56.4. Router: screen (646.8, 1086.2) at ×2.00, r 47.0. Cover ring centre (647, 934).

## Appendix B · Build pipeline (recommended)

| Step | Tool | Output |
|---|---|---|
| 1. Prep | `python3 -I f2/prod/prep.py` (reads only `assets/lib/`) | Graded full-res plates, coin matte + `coins.json`, Hubble FG/BG, rack-focus frames f0–f44 (numpy disc blur), emboss frames f1604–f1652 + rest plate, paper textures |
| 2. Film raw | `f2/prod/film.html` implementing `window.__ready`, `window.__duration = 1772/30`, `window.renderAt(t)`; WebGL2 photo layer (develop, light maps, terminator, motion blur) + DOM type; `node f2/render.mjs --page f2/prod/film.html --out build/f2/raw.mp4` with **PNG frames** (switch `frameAt` to `'png'` and the ffmpeg input codec to `png` to avoid JPEG banding in the darks) | `build/f2/raw.mp4` |
| 3. Finish | `python3 f2/film.py build/f2/raw.mp4 build/f2/graded.mp4 --look f2/prod/look.json` (after adding `print_bloom`) | graded video |
| 4. Score | `python3 -I f2/prod/score.py` (uses `f2/synth.py`, cue sheet §8.2) | `build/f2/score.wav` |
| 5. Master | ffmpeg mux + final encode per §10 | `build/f2/F2_final.mp4` |
| 6. Carousel | `f2/prod/carousel.html` → `node f2/render.mjs --page f2/prod/carousel.html --w 1080 --h 1440 --frames 0,1,2,3,4,5,6 --out build/f2/carousel` → `film.py --still` per frame (§5.4) | `build/f2/carousel/01…07.png` |

## Appendix C · Verified facts (re-run before release)

- `skimage.data.{coins, coffee, rocket, camera, hubble_deep_field, retina, moon, text, clock, astronaut}()` are pixel-identical to the files in `assets/lib/` (max abs diff 0, scikit-image 0.26.0).
- `grace_hopper.jpg` sha256 `a8ca6d734765703b09728ab47fe59f473d93ae3967fc24c7c0288c3c7adb7130` = matplotlib 3.9.2 `mpl-data/sample_data/grace_hopper.jpg`.
- Docstring purposes: coins "segmentation tests" → 分割测试; coffee "elliptical shapes … varying texture" → 椭圆与纹理; camera "segmentation and denoising" → 分割与去噪; hubble "multi-scale detection" → 多尺度检测; retina "circular images" → 圆形图像; moon "histogram equalization" → 直方图均衡; text "corner detection" → 角点检测; clock "inverse filters and deconvolution" → 反卷积; rocket, astronaut, Grace Hopper state no test purpose → 示例图.
- Licences (docstrings / SOURCES.md): coins no known copyright restrictions · coffee CC0 · rocket public domain · hubble public domain · retina CC0 (Wikimedia Commons) · camera CC0 · astronaut public domain · Grace Hopper public domain (U.S. Navy) · text public domain (Wikipedia) · clock public domain · **moon: no statement** (hence SRC4).

---

## 11. Post-review revisions (supersede the sections they name)

After the first full render, six independent critics (typography, cinematography, AI-look, motion, phone/platform,
facts) reviewed frames decoded from the encoded film (`build/f2/review/`). The production follows these revisions;
where they disagree with §0–§10, this section wins. IDs refer to the review findings.

**Image and grade**
- Develop is a continuous ramp, not a threshold stipple: `a = smoothstep(e − 0.40, e + 0.04, L + g·0.03)`, `e = 1 − 1.30E`
  (in) / `−0.04 + 1.38E` (out), flare mask `smoothstep(0.70, 0.90, L)`, E-DEVELOP `(.30,.10,.30,1)` (DOP-01).
  The espresso develops crema-first through a priority map, so the coin → crema match cut lands (DOP-02).
- Unsharp mask 20 %, radius 0.5×scale, threshold 4/255; coin display matte from per-coin convex hulls (DOP-10).
- Coins: the key light lifts the cloth weave inside its pool, `cloth = ((g − 0.04)/0.96)^1.1 · 0.90`, faded out at the scan
  edge; S03 light falloff 0.6 (CD-04, DOP-07, MO-05).
- Hubble: sky floor `(src − 0.05)/0.95` before the grade; FG = galaxies and halos (L > 0.14), BG inpainted (Telea) with
  sky noise; push FG 1.00 → 1.11, BG 1.00 → 1.075 on `(.75,0,.95,.55)` plus an accelerating tilt (FG −140 px, BG −93 px);
  motion blur from 3 px/f; f764 razor sharp; readout reports the FG scale and freezes at × 1.20 (DOP-04/05/06, MO-01, COPY-10).
- Retina: light travels linearly f860 → f920 with a Lambert-like terminator; crescent with the optic disc at f860 (DOP-09).
- Plate mark: wall /7, Gaussian 1.8, ridge at sd 4.5 (σ 6), ±12 % pressure variation, plate tone 2.8 %, soft-knee shading
  `1 + 0.30·tanh((x − 1)/0.30)`, depth 0.46 → rest walls −15.9 / −15.5 / +5.7 / +5.7 %, interior −3.8 % (DOP-03).
  Paper mottle σ 140 at 0.4 % plus a 1.5 % fall-off from the light (DOP-11).

**Layout (clear of the feed's action column, x ≥ 950 in y 1040–1480)**
- Sheet slots 90 / 390 / 690; cell 12 = (690, 1216, 255 × 170) (CJK-05, DOP-12). Coin tray origin (182, 700), centre
  (566, 1003); retina frame (454, 700)–(940, 1186), contain centre x 697, pull-back P0 (478, 724) (XHS-06).
- Espresso drift scales about the right-hung edge (990, 1000) (CD-12).
- Cell 10 crop (95, 0)–(353, 172), so the thumbnail is 255 px wide and every sheet gutter is 45 px (CJK-05, verified).
- Plate-12 outline stays rule-30 (an 0.18 line vanishes on a phone) (XHS-05).

**Motion and timing**
- Type prints on as light: opacity only, PRINT `(.25,.6,.3,1)` over 10 f, no rise; line stagger = clamp(round(1.5 ×
  characters of the previous line), 6, 16) f (CD-02).
- Hook: focus on E-ACCEL into the clack; glint f44–f58 on `(.25,.1,.25,1)` with a 180° shutter (DOP-08).
- Slit in two beats: inside the espresso print f260–f287, then grows to 693–1427 f300–f318 (CD-10).
- Router: twelve calls as an accelerando landing f488, 512, 530, 542, 554, 560, 566, 572, 578, 590, 602, 620; travel =
  min(4, interval/3) f; the beam narrows and dims mid-flight (CD-07, MO-05).
- S05 12 f earlier: contain f920–f950, frame draws f950–f966, text leaves into the pull-back (out f1108–f1112);
  E-REVEAL `(.5,0,.15,1)` (MO-02).
- Sheet develops as a ripple from the eye: 02/08 f1140, 04/06 f1146, 01/03/07/09 f1156, 11 f1171, 10 f1179; the 12th
  window develops f1187–f1202 (no stroke draw-on) (CD-01). A 2 % lean toward cell 12 during the hold, and the dive starts
  from it (MO-06).
- Inside plate 12 the outline dissolves after the dive (f1432–f1444) and re-forms f1564–f1576 (CD-06).
- S08 one beat earlier: the light table is a switch (dark f1580, lit f1581) with a 10 f bloom (0.30) as the eye adapts;
  the raking light lowers until the relief peaks on f1604, where the withheld D5 now sounds (CD-08, MO-03, MO-04).
- Score cue changes: `f2/prod/CUES_v2.md`.

**Type and copy**
- bone-5 `#9C9589`; ink-p-70 for sources, labels and page numbers on paper; caption tier 30 / 28 / 24 (CJK-04).
- Running head: only the chapter digit and name roll, one after the other, through a 28 px slot (CJK-11).
- S05 rules as 28 px kickers over couplets (second line in bone) (CD-09). The film's sheet shows frame numbers only;
  the docstring purposes stay on C5 (CD-05).
- End card: account 40 px heading the colophon; `your_eval()` and 换模型、混用模型之前，先拿它考一遍。 under the
  plate (our reading, under ■ 我们的解读); sources 22 px, hung labels (CJK-02, XHS-03).
- Copy: 前沿模型，/ 只服务 / 少数顶级场景。; 示意　每一束光，是一次调用 (captions carry no final 。); 底图　01 / 12;
  谁都能拿它们考算法; SRC2 嘉宾观点…; SRC4 除 09（未注明授权）外…; SRC6 05 Mikael Häggström; counters set as 图 + mono
  ` 01 / 12`; vertical caption ends …号与 DSCOVR (CJK-08/09/10, COPY-05/06/08/09).
- Carousel: hand-drawn china-marker loop on the cover (two passes, #7A5CFF at 85 %), cover hook 64 px (CD-03, XHS-02);
  C3 tray × 1.80; C2 frontier block 40 px lower; C4 plate label 图 04 / 12; C6 shows C5's cell 12 in place with a wall
  label; C7 uses the shared footer and a 540 × 360 plate mark (CJK-01/06/07, CD-11, XHS-04/08).
