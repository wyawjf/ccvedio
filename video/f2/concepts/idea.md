# 最后一片镜片 · THE LAST ELEMENT

**Concept pitch for F2: 微软CEO：大模型要打价格战了**
Vertical film 1080×1920 · 30 fps · **59.2 s** (1776 frames, 74 beats at 75 BPM) · silent text + synthesized score · Xiaohongshu carousel 1080×1440 × **7 frames** (frame 1 = video cover)

> **Logline.** Nadella's four judgments, told through the six parts of a camera lens. The token gets stopped down click by click. The frontier is a long lens. The model mix is three silver plates that show colour only where they overlap. Alignment is a focus that won't lock, and zero trust is the barrel. The last element turns out to be an eye: **models get cheaper; judgment doesn't.**
>
> **一句话：** 用一支镜头的六个部件，讲完纳德拉的四个判断。镜头里最后一片镜片，是你的眼睛：模型会降价，眼光不会。

**Proof frames** (real fonts, real grades, finishing pass applied; every coordinate below was checked in them):
`f2/concepts/idea/proof/_film_strip.jpg` (12 film beats), `proof/_carousel_strip.jpg` (7 frames), `proof/_cover_thumb.png` (cover at feed size), and the 1:1 frames `proof/f01.png … f11.png`, `proof/c1.png … c7.png`.
**Reference code**: `f2/concepts/idea/kit/prep.py` (every crop, grade and mask in §7, reads only `assets/lib/`), `kit/lookdev.html` (iris, barrel rings, text placement by baseline), `kit/render.mjs`, `kit/look.json` (finishing pass for `f2/film.py`).
Rebuild: `python3 -I f2/concepts/idea/kit/prep.py && node f2/concepts/idea/kit/render.mjs`, then `python3 f2/film.py --still f2/concepts/idea/proof/raw/X.png f2/concepts/idea/proof/X.png --look f2/concepts/idea/kit/look.json` (all from `video/`).

---

## 1. The idea

### 1.1 The big idea

Everyone is talking about the price of the model. We point a camera at it.

A camera lens is a near-perfect working model of what Nadella describes. Each part of a lens is ordinary, real optics, and each one maps to exactly one of his judgments. The film moves through the lens one part at a time, from the aperture inward, and ends behind the last piece of glass, where the eye is.

| Chapter (on screen) | The optical fact (true, no stretching) | His judgment it carries | What we see |
|---|---|---|---|
| **01 光圈 APERTURE** | Every stop halves the light. | Everyday compute commoditizes; the model layer faces a brutal price war. | A Greek coin with a face, the *token*. Its face wears away until 24 coins are 24 identical blank discs. Then a 9-blade iris clicks down on them, stop by stop. |
| **02 焦距 FOCAL LENGTH** | The longer the lens, the farther it sees and the narrower its view. | Frontier models will serve only a few top-tier niches. | Wide: an espresso, the everyday. Zoom to 600 mm: a Falcon 9 on the pad, small, far, rare. |
| **03 滤镜 FILTER** | A colour photograph is assembled from separate filtered plates. | Copilot reportedly mixes cheap closed and open models every day. | The Hubble Deep Field split into three silver channel plates. They drift together, and colour exists only where they overlap. |
| **04 对焦 FOCUS** | Opening the aperture wider does not bring focus. It makes focus harder. | He used to think alignment would fall out of scale. He no longer does. | Handwritten equations. The autofocus hunts, nearly locks, and never beeps. |
| **05 镜筒 BARREL** | A lens's controls live in the rings of its barrel, not in the glass. | Microsoft doesn't wait. It wraps models in zero trust: identity, logs, permissions outside the model. | The blank coin (the commodity model) gets three engraved rings: 身份, 记录, 权限. They rotate and lock so their labels line up on one index mark. The alignment happens outside the glass. |
| **06 眼睛 EYE** | In any visual instrument, the eye is the final optical element. | Every company will have a private eval; it will be its core IP. | A red planet rises in the eyepiece. It is a human retina. 最后一片镜片，是眼睛。Then our reading: 模型会降价。眼光不会。 |

The end card is a camera behaviour too. The iris closes, and in its centre the **violet focus-confirm light** comes on with the double *beep-beep* every DSLR user knows. That light is the account's violet dot, followed by **Coo-Coo出海Ai实验室**.

The film tells the story through a protagonist and through a colour arc:
- **One coin carries the film.** It is the facing-head Greek coin (#15 of the 24): a token with a face. It loses its face (commodity) and gets stopped down (price). It comes back blank inside a barrel of rules (architecture).
- **The colour arc is the argument.** Commodity is silver, the everyday is warm, the frontier is cold, the mix is silver and blooms into colour, and the eye is the warmest red in the film.

### 1.2 Why it feels human-made (what a jury would notice)

1. **One metaphor, held with discipline.** Six devices, all from the same instrument, each optically true, each carrying exactly one claim. Generators mix metaphors; this film never leaves the lens. Even the chapter names are everyday Chinese camera words (光圈, 焦距, 滤镜, 对焦, 镜筒, 眼睛). Xiaohongshu's photography-literate audience already owns that vocabulary.
2. **The resolution limit becomes the visual language.** The photos are small (most ≤ 640 px), so we never pretend otherwise. We see them through an eyepiece, at the size their pixels allow. Small apertures, telephoto haze and defocus are all *native* camera states, so softness reads as optics, not as upscaling.
3. **A protagonist you can follow.** It's the same coin from the first frame to the barrel, and its face disappears from the outside of the tray inward. The hero is the last to go.
4. **The sound is the mechanism.** Nine blade ticks in the iris snap. Price detents that drop a semitone each. A detuned chord that comes into tune as the plates register. A focus motor that never beeps. A bayonet click-clunk for each ring. Finally the beep, tuned to the ninth of the closing chord.
5. **Typography casts the voices.** 宋 (Noto Serif SC) is reported speech: him, always under an attribution kicker. 楷 (LXGW WenKai) is us. 黑 (Noto Sans SC) is labels. Mono (Geist Mono) is the instrument. The violet dot means *us* everywhere: the 我们的理解 kicker, the focus-confirm light, the brand mark. The client's attribution rule becomes part of the design system.
6. **Micro-details that reward pausing.** The barrel rings carry engraved agent IDs (ID·01–12), call timestamps (09:41:02…) and ALLOW · ASK · DENY. There's a zoom-ring focal scale, real f-stops, a field-of-view cone drawn as tangent hairlines, and a chromatic fringe at the field stop. Every photograph carries a credit.
7. **Restraint.** One photograph and one sentence per beat, on warm black. No boxes, no gradients-as-decoration, no glow, no particles, no globe, no stick figures. One accent colour. The only centred elements are the eyepiece (a real eyepiece is centred) and the end card.
8. **A reveal.** The red planet is an eye. The proof is `proof/f09.png`.

### 1.3 Brand continuity without repeating the template

The account's DNA survives as **material**, not layout. Paper `#F6F3EE` becomes the text colour on dark (`#EEE8DE`). Ink `#15121b` moves to a warmer cinema black `#0B0A09`. Violet `#5B2EFF` is kept exactly and used as a *signal*: a 10–24 px dot, never a fill. The previous film's thesis (当智慧像电一样便宜) is answered rather than repeated: if intelligence gets cheap, judgment is what gets expensive. Nothing from the rejected attempts returns: no caption boxes, hard shadows, comic halftone, purple-haze grounds, stick figures, Anton numerals, or TOKEN rectangles.

### 1.4 Content compliance map

| On screen | Voice / typeface | Rule satisfied |
|---|---|---|
| 微软 CEO 纳德拉判断 / 大模型要打价格战了 | kicker + serif title | Point 1, attributed (判断) |
| 先说一个词 / 大模型按 token 计价 / token…也是代替钱用的小圆片：代币 | neutral kicker + serif | Permitted general fact |
| 纳德拉判断 / 大多数企业场景的日常算力，终将被商品化 / 模型这一层，会有一场残酷的价格战 | kicker + serif | Point 1, paraphrase, no quotes |
| 他判断 / 前沿模型，只会服务少数顶尖的细分市场 | kicker + serif | Point 1 (frontier) |
| 据报道 / 微软 Copilot 内部，每天都在混着用便宜的闭源模型和开源模型 | kicker + serif | Point 2, marked 据报道 |
| 他说 / 他以前以为：规模足够大，对齐会自然出现 / 现在，他不这么想了 | kicker + serif | Point 4 (changed mind) |
| 他说 / 微软不等对齐问题先被解决，而是给模型套上零信任架构 / 身份·记录·权限 | kicker + serif + list | Point 4 (zero trust) |
| 最后一片镜片，是眼睛。 | 楷, no kicker | An optics fact, not attributed to him |
| 他认为 / 每家公司，都会有自己的私有评测集（eval），那会是它的核心知识产权 | kicker + serif | Point 3 |
| ● 我们的理解 / 模型会降价。眼光不会。 | violet-dot kicker + 楷 | Our takeaway, visibly labelled |
| Carousel: 看得越远，视野越窄 · three takeaways | violet-dot kicker + 楷 / serif | Labelled 我们的理解 |
| 来源 line + 纳德拉的观点均为转述，非原话 | sans, small | Source line on every final frame |

These do not appear anywhere: "neocloud capacity renting is not a business", "assume the model is compromised", "private evals define what good looks like". No quotation marks are used around any paraphrase. No hype words.

---

## 2. Film storyboard (59.2 s)

### 2.0 Conventions

- **Grid**: 1080×1920. Margins 96 px, so the text column runs x 96–984. **Eyepiece centre E = (540, 700)**. All y values are **text baselines** on a **4 px baseline grid**. The proofs use the same numbers.
- **Beat grid**: 75 BPM, so 1 beat = 0.8 s = 24 frames. Scene cuts and mechanical events land on beats.
- **Text zone (default)**: kicker at **y 1176**, statement lines at **1260 / 1344 / 1428**, all at x 96. There are three exceptions. The hook puts the kicker at 1148 and the title at 1296 / 1436. Zero trust puts the kicker at 1108, the header at 1192 and the list at 1276 / 1352 / 1428. The thesis puts the kicker at 1176 and its lines at 1308 / 1444. Nothing essential sits below y 1460 or above y 214.
- **Type shorthand** (full table in §4.3):
  **[K]** kicker, his voice: Noto Sans SC 500, 32 px, line-height 40, +0.10em, `#A39C92`, x 96, no marker.
  **[K●]** kicker, our voice: same, but `#8C72FF` at x 120, with a violet dot ⌀10 `#5B2EFF` centred at (101, baseline − 12).
  **[S]** statement: Noto Serif SC 500, 60/84, +0.02em, `#EEE8DE`. Latin words inside are Instrument Serif *Italic* at 1.12 em.
  **[O]** our voice: LXGW WenKai 500, +0.04em, `#EEE8DE`.
  **[M]** micro line at y 236. Index: Geist Mono 500, 22 px, `#8A847B`, x 96. Chapter name: Noto Sans SC 500, 26 px, +0.06em, `#CFC7BA`, x 134. Latin chapter name: Geist Mono 16 px, +0.22em, `#6E685F`, 14 px after the CJK. Live readout: Geist Mono 400, 24 px, `#A39C92`, right-aligned at x 984.
  **[C]** photo credit: Geist Mono 400, 16 px, +0.04em, `#6E685F`, right-aligned at x 984.
- **Text entrance** for everything except the hook title is **focus-in**: blur 10→0 px, opacity 0→1, scale 1.015→1 from the left baseline, 560 ms, `cubic-bezier(.16,1,.3,1)`. **Exit** is **defocus-out**: blur 0→8 px, opacity 1→0, 320 ms, `cubic-bezier(.7,0,.84,0)`. Kicker leads its first line by 120 ms; each following line adds 140 ms. *Nothing slides; everything focuses.*
- **Eyepiece float** (applies to the aperture and its photo, never to text): x = 2.2·sin(2πt/7.3), y = 1.6·sin(2πt/9.1 + 1.0) px. The photo inside moves −1.3× that (parallax against the field stop).

### 2.1 Storyboard

| # | in → out (s) | What we see (asset, exact crop, treatment) | Camera / motion | On-screen copy (final) | Transition out | Sound |
|---|---|---|---|---|---|---|
| **S1 HOOK** | 0.00 → 2.40 | **Iris** (9 blades, R_o 368, ring 368–384) on E. Inside: `coins.png` hero coin #15, centre (212.4, 193.1), r 23.5, warm-silver toned (`coin_hero_w0.png`). Frame 0: iris wide open r 300; content is the tray at 2.6× centred on the hero, Gaussian blur 14 px (a defocused silver glow). Proof f01 shows 0.6 s. | **0.20 SNAP**: r 300→118, scale 2.6→4.4×, blur 14→0, all 180 ms `cubic-bezier(.7,0,.2,1)`, then settle r 116→118 over 90 ms `cubic-bezier(.3,0,.3,1)`. 0.47→2.40: push 4.4→4.5× `cubic-bezier(.33,0,.67,1)`. | **Static from frame 0 (no entrance)**: [K] at 34 px 微软 CEO 纳德拉判断 (y 1148). Title Noto Serif SC 700 124/140, −0.01em, x 91 (−5 optical): **大模型** (y 1296) / **要打价格战了** (y 1436). [M] 01 光圈 APERTURE; readout ƒ/1.4 → **ƒ/4** at 0.20. | Title defocus-out 2.40→2.72; iris holds | Room tone + drone fade in (400 ms). **0.20 iris clack**: 9 blade ticks over 18 ms, main click, 58 Hz thump. Peak −8 dBFS. |
| **S2 TOKEN** | 2.40 → 7.20 | Same coin at 4.5× in r 118. [C] Greek coins from Pompeii · Brooklyn Museum (y 1132). | Float + parallax only. | 2.52 [K] 先说一个词 · 2.64 [S] 大模型按 *token* 计价。(1260) · 4.00 [S] *token* 在英文里，(1344) · 4.14 [S] 也是代替钱用的小圆片：代币。(1428) | 7.20 all text out; the iris opens | 2.40 felt piano A4 *pp*; 4.00 F4 *pp*. |
| **S3 COMMODITY** | 7.20 → 12.00 | Iris opens to **r 300** while the content pulls back to the whole tray `tray.png` at **2.0×**, centre (192, 152). **Faces wear off** 8.00→11.20 (§7.1): the farthest coin from the hero goes first, 110 ms stagger, 600 ms each, `cubic-bezier(.45,0,.55,1)`. The hero starts 0.3 s late (10.60→11.20). End state `tray_worn.png`. Proof f03 shows the mid-cascade at 9.6 s; f04 shows S4 after the third detent. | 7.20→7.80 open: r 118→300, scale 4.5→2.0×, centre hero→tray, 600 ms `cubic-bezier(.22,.61,.12,1)`. Then hold. | 7.32 [K] 纳德拉判断 · 7.44 [S] 大多数企业场景的日常算力，(1260) · 7.58 [S] 终将被商品化。(1344). Readout ƒ/1.4. | None (continuous into S4) | 7.20 piano D4. 8.00–11.20: 24 tiny "wear" ticks (detent recipe, p 1.6, −34 dB, each with 40 ms of soft brushed noise). The hero's tick at 10.60 is lower and closer (p 1.2, −28 dB). |
| **S4 PRICE WAR** | 12.00 → 16.80 | Worn tray at 2.0×. Content pans from tray centre to hero (212.4, 193.1) over 12.0→16.0 so the final pinhole frames the **blank hero coin**. | **5 detents on the beat**: 12.8 / 13.6 / 14.4 / 15.2 / 16.0. r steps 300→212→150→106→75→53. Each step is 110 ms `cubic-bezier(.5,0,.1,1)`, overshoot 3 %, settle 70 ms. **16.40 SNAP closed**: 53→0, 140 ms. Black 16.40→16.80. | S3 lines out at 12.00, [K] stays · 12.12 [S] 模型这一层，(1260) · 12.26 [S] 会有一场残酷的价格战。(1344). Readout steps ƒ/2 → ƒ/2.8 → ƒ/4 → ƒ/5.6 → ƒ/8, then "—" at 16.40. All text cuts at 16.40 (100 ms). | Iris closed; 0.4 s of black | A detent click on every step, each **a semitone lower**, each doubled by piano D3 · C♯3 · C3 · B2 · B♭2. 16.40 soft clack. Drone cuts (60 ms) → **0.4 s silence**. |
| **S5 FRONTIER** | 16.80 → 24.00 | Chapter 02. **Field stop r 300**, no iris from here on. `espresso.png` at 1.5×, centre (292, 200). [C] Espresso · Rachel Michetti · CC0 (y 1048). At **20.30, cut on frame** to `rocket.png`: 1.05×, centre (322, 213), r 220. Push to 2.0×, centre (322, 228) by 24.0. Heat shimmer from 22.0 (0.6 px, 1.8 Hz). A **focal-scale arc** sits at the aperture's left (§4.8). [C] Falcon 9 / DSCOVR · SpaceX · 2015 (y 968). Proofs: f05a (wide end), f05 (tele end). | 16.80→17.30 iris opens 0→300 (the iris then fades out over 200 ms). 19.60→20.30 **zoom-through** toward the crema (288, 148): scale 1.5→2.4×, radial blur 0→18 px (12 samples), r 300→255, `cubic-bezier(.65,0,.35,1)`. 20.30→21.00 rocket blur 18→0, r 255→220. 21.0→24.0 tele push `cubic-bezier(.33,0,.67,1)`. | Readout **24 mm · 大多数场景** (16.8→19.6). It counts in log steps 24→600 (19.6→21.0), then **600 mm · 少数顶尖**. 20.96 [K] 他判断 · 21.10 [S] 前沿模型，(1260) · 21.24 [S] 只会服务少数顶尖的细分市场。(1344) | Tilt up into the sky | 16.80 iris-open breath; warm pad F maj add9 (F3 A3 C4 G4) −30 dB; warmer room tone. 19.6–21.0 servo whir + whoosh rising 400→3000 Hz. 20.30 a tiny tick at the cut. 21.0 cold pad Dm9 (D3 F3 A3 E4) + floodlight hum −46 dB. |
| **S6 MIX** | 24.00 → 30.40 | Chapter 03. The rocket slides down out of the aperture, revealing a graded dusk gradient that runs to black. The **registered silver Hubble plate** enters from the top. `hubble_deep_field.jpg` crop (220, 150)–(780, 710) is split into its R, G, B channels; each becomes a **silver plate** (§7.4), screen-blended. 24.8: the one plate **splits into three**, drifting to offsets (−160, −120) / (+160, −120) / (0, +150) from E, each r 280. They then **converge** and **colour blooms** (`venn_film_mid.png`, `venn_film_done.png`). [C] Hubble eXtreme Deep Field · NASA at (984, 272). Proof f06 shows the plates on their way in at 27.4 s. | 24.0→24.8 tilt: content +520 px down, `cubic-bezier(.65,0,.35,1)`. 24.8→25.6 split, r 220→280, `cubic-bezier(.22,.61,.12,1)` 800 ms. 26.4→28.8 converge, same curve, 2.4 s. 28.8→29.6 silver→true colour, `cubic-bezier(.4,0,.2,1)`. | Readout **R · G · B** → **RGB** at 28.8. 25.20 [K] 据报道 · 25.32 [S] 微软 *Copilot* 内部，(1260) · 25.46 [S] 每天都在混着用 (1344) · 25.60 [S] 便宜的闭源模型和开源模型。(1428) | Defocus bridge | 24.0 air whoosh. 24.8 three **glass bells** A4 / C♯5 / E5, detuned −38 / +27 / −19 cents (audible beating). 26.4→28.8 the detune glides to 0. 28.8 the chord is in tune: +4 dB swell, reverse-reverb bloom. |
| **S7 CHANGED MIND** | 30.40 → 36.80 | Chapter 04. The colour field blurs 0→22 px and crossfades into `text.png` (circle centre (224, 86), r 86 source) at 2.45× in **r 210**, also at 22 px. **AF hunting** uses synthetic depth of field on the paper's plane (§7.5): blur(px) = min(22, 9·A·\|d − d_f\|), A 1.0→1.6. d_f(t′) = 0.35 + 0.45·sin(2π·0.85·t′) with t′ = t − 31.0. From 34.4 it glides to **0.50 and stays**, so it is **never sharp**. Proof f07. | 30.4→31.0 bridge, `cubic-bezier(.65,0,.35,1)`. The field stop stays still; only focus breathes. | Readout **AF ·  ··  ···** cycling at 4 Hz, then **AF —** from 35.2. 31.00 [K] 他说 · 31.12 [S] 他以前以为：(1260) · 31.26 [S] 规模足够大，对齐会自然出现。(1344) · 34.40 out · 34.72 [S] **现在，他不这么想了。**(1260) | **Hard cut** on the first clock tick | 30.4 the chord low-passes 8 kHz→700 Hz. A servo whir follows the focus velocity. **No confirm beep: its absence is the cue.** 34.4 piano D2 + F3. 36.0 faint ticking fades in (−40 dB). |
| **S8 ZERO TRUST** | 36.80 → 44.80 | Chapter 05. 36.8→38.4: `clock_motion.png` (circle centre (212, 152), r 140 source) at 1.5× in r 210, with horizontal jitter ±1.5 px on each tick (proof f08a). **38.40 hard cut** to the **barrel**: the blank hero `coin_hero_w4.png` at 4.6× in r 134 (dark plate to r 158), and three engraved rings (§5.6): A 160–198 **身份 IDENTITY**, B 210–250 **记录 LOG**, C 262–306 **权限 POLICY** (knurled). Index ticks at 12 o'clock. Proof f08. | Each ring enters from scale 1.06 at −24° / +18° / −12°, opacity 0. It locks at **38.40 / 39.20 / 40.00**: 700 ms `cubic-bezier(.22,.61,.12,1)`, with the last 120 ms on `cubic-bezier(.34,1.56,.64,1)` (2° overshoot). The labels land exactly on the index. 40.0→44.8: push 1.00→1.03. | Readout **1/8 s** (clock) → **ID · LOG · POLICY**. [K] 他说 (1108, from 36.8) · 36.92 [S] 微软不等对齐问题先被解决，(1192) · 38.40 out · 38.52 [S] 而是给模型套上零信任架构：(1192). The list arrives with each lock (term Noto Sans SC 700 40/76 +0.06em `#A39C92` x 96; definition Noto Serif SC 500 52/76 x 228): 38.60 **身份** 每个智能体都有一个 (1276) · 39.40 **记录** 每一次调用都留痕 (1352) · 40.20 **权限** 放在模型之外 (1428) | 44.80 rings recede (scale 1→0.92, opacity→0, 800 ms ease-out); black from 45.6 | 36.8–38.4 ticks accelerate from 8 to 10 Hz. **38.40 / 39.20 / 40.00 bayonet locks** (click + clunk + metal ring tail at 1.6k / 1.35k / 1.1k Hz), panned −0.2 / 0 / +0.2. 40.0–44.8 pad B♭ (B♭2 D3 F3) −32 dB; sub pulse 41 Hz every 1.6 s. |
| **S9 THE EYE** | 44.80 → 52.80 | Chapter 06. Darkness. `retina.jpg` (mask r 690 about (704, 703), which drops the camera's notch) **rises like a planet** in **field stop r 420** at 0.62×. A lower-right terminator darkens it (0.55 → 0 by 47.6). The optic disc catches the halation like a sun glint. Then a push toward the **fovea (703, 705)**. [C] 人眼眼底照片 · fundus · Wikimedia Commons · CC0 at (984, 1158), from 46.6. Proof f09. | 45.2→47.2 emerge: opacity 0→1, scale 0.58→0.62, `cubic-bezier(.25,.1,.25,1)` 2 s. 47.6→52.8 push 0.62→0.95× `cubic-bezier(.33,0,.67,1)`. | Readout **∞**. 46.40 [O] 76/96 **最后一片镜片，是眼睛。**(1268) · 48.60 out · 48.80 [K] 他认为 · 48.92 [S] 每家公司，都会有自己的 (1260) · 49.06 [S] 私有评测集（*eval*），(1344) · 49.20 [S] 那会是它的核心知识产权。(1428) | Continuous | 44.8 everything out: **0.4 s silence**. 45.2 sub swell 32→45 Hz plus a high pad, D maj add9. 46.4 piano D5 over D2. 48.8 phrase A4–F♯4–D4, 0.4 s apart. |
| **S10 OUR READING** | 52.80 → 56.00 | Push continues 0.95→1.36× into the fovea. The vessels thin out, leaving warm red with the dark fovea at E. Proof f10. | `cubic-bezier(.33,0,.67,1)` | 52.80 eval block out · 52.92 [K●] **我们的理解** (1176) · 53.04 [O] 112/136 **模型会降价。**(1308) · 53.60 [O] **眼光不会。**(1444) | Iris closes | 52.8 piano D3–A3–F♯4. 53.6 A4 + D5, which completes the D major that the opening D minor never had. |
| **S11 END** | 56.00 → 59.20 | 56.00 text out. An iris (R_o 440, ring 440–456) fades in over 200 ms and **closes** over the retina, r 420→0, 420 ms `cubic-bezier(.6,0,.2,1)`. **56.48: a violet dot ⌀24 `#5B2EFF` lights at E**, the focus-confirm light. Glow: `0 0 18px 4px rgba(91,46,255,.55), 0 0 60px 18px rgba(91,46,255,.22)`. It flickers off between beeps (56.535–56.60), then holds. Proof f11. | No other motion. The last frame loops cleanly into frame 0 (closed iris → open iris). | Centred, the only centred text in the film. 56.80 **Coo-Coo出海Ai实验室**, Noto Sans SC 700 44/56 (y 800). 57.20 Noto Sans SC 400 26/40 `#8A847B`: 来源：20VC 播客 · Harry Stebbings 对谈 Satya Nadella · 2026-10-26 (y 940) / 纳德拉的观点均为转述，非原话；「我们的理解」为本号解读 (y 980). Credits in Geist Mono 17/26 `#6E685F`: Photos · Brooklyn Museum · Rachel Michetti (CC0) · SpaceX · NASA (y 1044) / S. van der Walt · Wikimedia Commons (CC0) · handwriting: public domain (y 1072) | End | 56.0 soft clack (9 blade ticks, −14 dB). **56.48 + 56.60 AF beep-beep**: E7 2637 Hz sine, 55 ms, dry, −16 dBFS, the 9th of the sustained D-major chord. 59.2 tail cut with a 30 ms fade. |

### 2.2 Shot notes (rules the table can't hold)

- **The hook is the only text that doesn't animate in.** Frame 0 must already be the poster: title, kicker and an open iris with a glowing defocused coin. The snap at 0.20 s is the hook's motion and sound.
- **The coin is only ever sharp at ≤ 4.5×.** Larger views of it are either defocused (S1 frame 0) or blank (S8). A blank coin has no detail left to go soft.
- **Text never overlaps a photograph.** The aperture zone and the text zone are separate by construction: the largest aperture (r 420) ends at y 1120, and the highest kicker is at 1108 only in S8, where the barrel ends at y 1006.
- **Chapter changes always happen on a beat and on a mechanical event**: an iris close/open, a cut on a tick, or a cut on a bayonet click. Picture and sound always share one cause.
- **The readout is the only "live" UI element.** It changes when the optics change, and never decoratively.

### 2.3 Optional soundbite slots (the film is complete without them)

| Slot | Where | Length | Picture | Text |
|---|---|---|---|---|
| **A** | Replaces 现在，他不这么想了 at 34.40 (S7) | 6–10 s | The AF hunt keeps looping (same d_f curve, mirrored); the readout keeps cycling. | [K] 原声 (1176). Chinese translation of his actual words, Noto Serif SC 500 52/76 at 1260 / 1336. The 「」 marks are allowed **here only**, because this is his recorded voice. English original in Inter Tight 500 28/40 `#8A847B` at 1404 / 1444. |
| **B** | Replaces the eval block at 48.80 (S9) | 6–8 s | The retina push continues at the same speed and starts S10 from wherever it reached. | Same style. |

Music ducks −10 dB under the voice (80 ms attack, 600 ms release). With one slot the film runs ≤ 69 s. With both, trim S2 to 3.2 s (merge the token lines into two), shorten the espresso hold in S5 by 1.6 s, and drop 0.8 s from S3's hold.

### 2.4 Copy deck (every string, in order)

1. 微软 CEO 纳德拉判断 2. 大模型 / 要打价格战了 3. 先说一个词 4. 大模型按 token 计价。 5. token 在英文里， / 也是代替钱用的小圆片：代币。 6. 纳德拉判断 7. 大多数企业场景的日常算力， / 终将被商品化。 8. 模型这一层， / 会有一场残酷的价格战。 9. 24 mm · 大多数场景 → 600 mm · 少数顶尖 10. 他判断 11. 前沿模型， / 只会服务少数顶尖的细分市场。 12. 据报道 13. 微软 Copilot 内部， / 每天都在混着用 / 便宜的闭源模型和开源模型。 14. 他说 15. 他以前以为： / 规模足够大，对齐会自然出现。 16. 现在，他不这么想了。 17. 他说 18. 微软不等对齐问题先被解决， 19. 而是给模型套上零信任架构： 20. 身份　每个智能体都有一个 / 记录　每一次调用都留痕 / 权限　放在模型之外 21. 最后一片镜片，是眼睛。 22. 他认为 23. 每家公司，都会有自己的 / 私有评测集（eval）， / 那会是它的核心知识产权。 24. 我们的理解 25. 模型会降价。 / 眼光不会。 26. Coo-Coo出海Ai实验室 27. 来源：20VC 播客 · Harry Stebbings 对谈 Satya Nadella · 2026-10-26 28. 纳德拉的观点均为转述，非原话；「我们的理解」为本号解读

Micro: 01 光圈 APERTURE · 02 焦距 FOCAL LENGTH · 03 滤镜 FILTER · 04 对焦 FOCUS · 05 镜筒 BARREL · 06 眼睛 EYE · ƒ/1.4 ƒ/2 ƒ/2.8 ƒ/4 ƒ/5.6 ƒ/8 · 24–600 mm · R · G · B / RGB · AF · / AF — · 1/8 s · ID · LOG · POLICY · ∞

---

## 3. Carousel: 7 frames, 1080×1440

**Grid**: margins 96, text column 96–984, baselines on a **2 px grid**. [M] micro line at **y 120**, using the same styles as the film. **Footer** at y 1378: violet dot ⌀14 at (103, 1369), then **Coo-Coo出海Ai实验室** in Noto Sans SC 700 26 px `#CFC7BA` at x 124, and the page index "0N / 07" in Geist Mono 20 px `#6E685F`, right-aligned at x 984. Body text is never below 44 px. The proof strip is `proof/_carousel_strip.jpg`.

**C1 · Cover** (`proof/c1.png`; also the video cover)
- [K] at 34 px **微软 CEO 纳德拉判断** (96, 198).
- Title, Noto Serif SC 700 **144/164**, −0.01em, x 90: **大模型** (360) / **要打价格战了** (524).
- Iris centred at (540, 920): aperture r 112, R_o 290, ring to 306. Hero coin `coin_hero_w0` at 4.2×.
- Subtitle, Noto Serif SC 500 40/56 `#A39C92`: **一支镜头的六个部件，讲完他的四个判断** (96, 1300).
- Footer, plus a right-hand label **20VC · 2026.10.26** in Geist Mono 20 px.
- *As a thumbnail* (2-column feed, about 0.5×; see `_cover_thumb.png` at 0.25×): a black card with a 72-px-equivalent white serif title on two lines, above a single bright coin inside a dark iris. It's a camera you recognise at a glance. Among bright, busy covers it reads as the one quiet, expensive object. The title stays legible even at 0.25×.

**C2 · 01 光圈** (`proof/c2.png`)
- [M] 01 光圈 APERTURE / **ƒ/2.8 → ƒ/11**.
- [K] 纳德拉判断 (214).
- [S] 52/76: 大多数企业场景的日常算力， (296) / 终将被商品化； (372) / 模型这一层， (448) / 会有一场残酷的价格战。 (524).
- **Five apertures in a row**, all centred on y 820: diameters 232 / 164 / 116 / 82 / 58 at x 212 / 469 / 668 / 826 / 955. Each holds the hero coin, worn 0 / 25 / 50 / 75 / 100 % (`coin_hero_w0…w4`), coin diameter 94 % of its aperture. Under each, its f-number in Geist Mono 20 px `#A39C92` (y 990). The row shows smaller and faceless at the same time.
- [C] Greek coins from Pompeii · Brooklyn Museum (984, 1300). Footer 02 / 07.

**C3 · 02 焦距** (`proof/c3.png`)
- [M] 02 焦距 FOCAL LENGTH / **24 mm → 600 mm**.
- Espresso circle at (356, 500), r 260, at 1.3×, source centre (292, 200). Rocket circle at (852, 690), r 110, at 1.15×, source centre (322, 212).
- **Field-of-view cone**: the two external tangents between the circles, 1 px `rgba(238,232,222,.18)`.
- Labels: **24 mm** (Geist Mono 20, 96, 812) + 广角 · 大多数场景 (Noto Sans SC 500 26 px `#8A847B`, 96, 850). **600 mm** (right-aligned at 962, y 852) + 长焦 · 少数顶尖 (962, 890).
- [K] 他判断 (1000). [S] 52/76: 前沿模型，只会服务 (1080) / 少数顶尖的细分市场。 (1156).
- [K●] 我们的理解 (1240). [O] 52/72: **看得越远，视野越窄。** (1308).
- Footer.

**C4 · 03 滤镜** (`proof/c4.png`)
- [M] 03 滤镜 FILTER / **R · G · B**.
- Three silver plates of the Hubble crop at 0.82× (⌀ 460), centred (410, 525), (670, 525), (540, 750). **Only the triple intersection is in true colour** (`venn_carousel.png`).
- Channel letters R (196, 330), G (884, 330), B (540, 1012) in Geist Mono 18 px.
- [K] 据报道 (1080). [S] 52/76: 微软 *Copilot* 内部，每天都在混用 (1160) / 便宜的闭源模型和开源模型。 (1236).
- [C] Hubble eXtreme Deep Field · NASA (984, 1300). Footer.

**C5 · 04 对焦 · 05 镜筒** (`proof/c5.png`)
- [M] 04 对焦 · 05 镜筒 FOCUS · BARREL / **零信任**.
- [K] 他说 (214). [S] **48/70**: 他以前以为：规模足够大， (290) / 对齐会自然出现。现在不这么想了。 (360) / 微软不等这个问题被解决， (450) / 先给模型套上零信任架构： (520).
- Barrel centred at (340, 850): blank coin r 106 (4.4×), ring A 112–140 身份, B 150–178 记录, C 188–222 权限 (knurled). Index tick 2×12 px at y 608.
- **Callouts**: from points on the rings at −40° (r 126), 0° (r 164) and +40° (r 205), each marked with a ⌀5 dot. Hairline leaders (1 px `rgba(238,232,222,.28)`) elbow to x 600–626. At x 640, a term in Noto Sans SC 700 30 px `#A39C92` (y 712 / 850 / 988) above a definition in Noto Serif SC 500 **44/60** (y 768 / 906 / 1044): 每个智能体一个 / 每次调用都留痕 / 放在模型之外.
- Footer.

**C6 · 06 眼睛** (`proof/c6.png`)
- [M] 06 眼睛 EYE / **∞**.
- Retina circle at (540, 560), r 360, 0.53×.
- [C] 人眼眼底照片 · fundus · Wikimedia Commons · CC0 (984, 962).
- [O] 60/80: **最后一片镜片，是眼睛。** (96, 1062).
- [K] 他认为 (1150). [S] 48/70: 每家公司都会有私有评测集（*eval*）， (1222) / 这会是它的核心知识产权。 (1292).
- Footer.

**C7 · 我们的理解 + source** (`proof/c7.png`)
- [K●] 我们的理解 (200).
- [O] **120/140**: **模型会降价。** (360) / **眼光不会。** (500).
- Hairlines at y 600 / 700 / 800 / 900, x 96–984, 1 px `rgba(238,232,222,.16)`.
- Three rows: index in Geist Mono 500 22 px `#8C72FF` at x 96, text in Noto Serif SC 500 44/60 at x 160 (y 666 / 766 / 866):
  01 别押单一模型，做多模型路由。 / 02 把私有评测集，当成资产来建。 / 03 权限和记录，放在模型外面。
- Brand block: dot ⌀18 at (105, 1047), then **Coo-Coo出海Ai实验室** in Noto Sans SC 700 36 px (132, 1058).
- Source in Noto Sans SC 400 24/38 `#8A847B`: 来源：20VC 播客 · Harry Stebbings 对谈 Satya Nadella · 2026-10-26 (1140) / 纳德拉的观点均为转述，非原话；「我们的理解」为本号解读。 (1178).
- Credits in Geist Mono 16/26 `#6E685F` (1240 / 1266). Index 07 / 07.

The film and the carousel share the coin, the iris, the plates, the barrel and the retina, at the same grades and with the same type voices. The carousel is the film's frames, laid out for reading.

---

## 4. Design system

### 4.1 Grid

| | Film 1080×1920 | Carousel 1080×1440 |
|---|---|---|
| Columns | 12 × 52 px, gutter 24, margins 96 | same |
| Baseline | 4 px; text leadings 84 / 76 / 136 / 140 (multiples of 4) | 2 px |
| Anchors | micro line y 236 · eyepiece E (540, 700) · kicker y 1176 · lines 1260 / 1344 / 1428 | micro y 120 · footer y 1378 |
| Safe | x 96–984, y 214–1460 (brief: 64–1000, 200–1480) | x 96–984, y 100–1400 |
| Aperture radii used | 53–118 (iris), 210, 220, 280, 300, 420 | 29–360 |

### 4.2 Typefaces (fixed roles)

- **Noto Serif SC** 500 / 700: everything *reported*, meaning his paraphrases, general facts and the hook title. Song type reads as print, and as record.
- **LXGW WenKai** 500: *our* voice only (three lines in the film). Kai type reads as a hand.
- **Noto Sans SC** 400 / 500 / 700: kickers, list terms, chapter names, the brand, the source.
- **Geist Mono** 400 / 500: the instrument. Readouts, indices, credits, engravings and the focal scale, with tabular figures.
- **Instrument Serif** Italic 400: Latin words inside serif lines (token, Copilot, eval).
- **Inter Tight** 500: English subtitles in the optional soundbite slots only.

### 4.3 Type scale (px)

| Role | Face | Size / leading | Tracking | Colour |
|---|---|---|---|---|
| Hook title | Noto Serif SC 700 | 124 / 140 (cover 144 / 164) | −0.01em, −5 px optical left | `#EEE8DE` |
| Thesis (ours) | LXGW WenKai 500 | 112 / 136 (C7 120 / 140) | +0.04em | `#EEE8DE` |
| Our line | LXGW WenKai 500 | 76 / 96 (C6 60 / 80, C3 52 / 72) | +0.04em | `#EEE8DE` |
| Statement | Noto Serif SC 500 | 60 / 84 (carousel 52 / 76 and 48 / 70) | +0.02em | `#EEE8DE` |
| List definition | Noto Serif SC 500 | 52 / 76 (C5 44 / 60) | +0.02em | `#EEE8DE` |
| End brand | Noto Sans SC 700 | 44 / 56 | +0.02em | `#EEE8DE` |
| List term | Noto Sans SC 700 | 40 / 76 (C5 30) | +0.06em | `#A39C92` |
| Kicker | Noto Sans SC 500 | 32 / 40 (hook and cover 34) | +0.10em | `#A39C92`; ours `#8C72FF` |
| Source line | Noto Sans SC 400 | 26 / 40 (C7 24 / 38) | +0.02em | `#8A847B` |
| Chapter name | Noto Sans SC 500 | 26 | +0.06em | `#CFC7BA` |
| Readout | Geist Mono 400 | 24 | +0.02em | `#A39C92` |
| Index | Geist Mono 500 | 22 | +0.02em | `#8A847B` |
| Ring label | Noto Sans SC 700 | 22, set on the arc | +2 px per glyph | `#EEE8DE` with a 1 px engraved shadow |
| Credits | Geist Mono 400 | 16–17 / 26 | +0.04em | `#6E685F` |
| Chapter Latin | Geist Mono 400 | 16 | +0.22em | `#6E685F` |
| Focal scale | Geist Mono 400 | 15 | 0 | `rgba(207,199,186,.45)`; current value `#EEE8DE` |
| Ring legends | Geist Mono 400 | 11–12, on the arc | +1.2 to 2.2 px | `rgba(207,199,186,.62–.75)` |

### 4.4 Typographic rules

- Paraphrases are never quoted. 「」 is used only for the label 「我们的理解」 in source lines, and for a real soundbite translation.
- Mixed scripts get a four-per-em space (U+2005) between CJK and Latin, inserted by the copy pipeline, not left to the browser. Latin inside serif lines is Instrument Serif Italic at 1.12 em, with no extra tracking.
- Full-width punctuation stays. At ≥ 60 px, wrap ，：； in `font-feature-settings:"halt"` so the comma doesn't open a hole mid-line. Sentence-final 。 stays: it is the smallest circle in the film.
- Line breaks are always set by hand at phrase boundaries, never auto-wrapped. A line holds ≤ 14 CJK characters at 60 px.
- Text is placed by **baseline** (`lookdev.html` measures each style's baseline offset with a zero-height inline-block probe). Layout runs in **two passes**: the first loads every unicode-range font subset, the second measures. Without this, @fontsource's lazy subsets make widths wrong; the look-dev hit exactly that bug.

### 4.5 Colour tokens

| Token | Hex | Use |
|---|---|---|
| `--ink` | `#0B0A09` | page and surround (warm cinema black) |
| `--plate` | `#121110` | inside an empty aperture; blade base |
| `--blade-hi` | `#1F1D1A` | lit blade edge, ring highlight (max of the gradients) |
| `--paper` | `#EEE8DE` | primary text (brand paper `#F6F3EE` dimmed for a dark ground; 16:1 on ink) |
| `--paper-2` | `#CFC7BA` | chapter names, engraving fills |
| `--dim` | `#A39C92` | kickers, readouts, list terms (7.2:1) |
| `--source` | `#8A847B` | source lines, indices (5.3:1) |
| `--mute` | `#6E685F` | credits, Latin micro (3.6:1, non-essential only) |
| `--hair` | `rgba(238,232,222,.18)` | hairlines: FOV cone, focal arc, leaders (.28) |
| `--violet` | `#5B2EFF` | **the dot** only: our-voice kicker, focus-confirm light, brand mark |
| `--violet-t` | `#8C72FF` | violet text on dark (5.6:1) |
| fringe | `rgba(255,96,64,.10)` / `rgba(80,140,255,.08)` | field-stop chromatic fringe, ±0.8 px |

### 4.6 Grade (the "eyepiece" LUT)

The grade is implemented as `grade()` and `silver()` in `kit/prep.py`, and can be baked to a 33³ `.cube` if needed. Values are in display-referred 0–1.

- **Lift / gamma / gain**: `y = (0.93 · (x + 0.012·(1−x)))^(1/0.95)`. That means lift +0.012 (blacks sit just above the surround, so the field stop reads), gamma 0.95 (denser mids) and gain 0.93 (highlights never touch white).
- **Saturation** 0.82 globally, with per-photo overrides in §7.
- **Split-tone**: shadows toward 210° (blue-teal) at 0.06 weighted by (1−L)²; highlights toward 36° (amber) at 0.08 weighted by L².
- **Shoulder**: above 0.82, an exponential soft-clip, `y = k + (1−k)(1−e^(−(x−k)/(1−k)))`.
- **Monochrome plates (coins, handwriting, clock)** are **warm silver**:
  - S-curve with contrast 0.15 around a 0.42 pivot.
  - Per-channel gammas R 0.97 / G 1.00 / B 1.06.
  - Mapped between `#0D0C0B` and `#EDE6D9`, like a selenium-toned gelatin print.

### 4.7 Film texture (finishing pass)

`f2/film.py` runs over the composited frame, type included, with `kit/look.json`.
- **Grain**: σ 0.030 at mid-grey, size 1.25 px, chroma 0.15, mid-tone weighted, refreshed every frame.
- **Halation**: threshold 0.74, radius 16 px, strength 0.16, tint (1, .36, .16).
- **Bloom**: 0.05 at radius 48.
- **Chromatic aberration**: 0.0005 (radial).
- **Vignette**: 0.24, round.
- **Gate weave**: 0.25 px (film only).
- **Flicker**: 0.4 % (film only).
- **Per-scene keys**:
  - S1–S4 (silver): halation 0.12.
  - S5 rocket: halation 0.22, so the pad lights star.
  - S6: bloom 0.08 during the colour bloom (28.8–29.6).
  - S9–S10: halation 0.20, so the optic disc glows like a sun on a planet.
  - S11: halation 0.10. The dot's glow is drawn, not post.
- **Heat shimmer** (S5, 22.0–24.0) is added in the same pass, restricted to the aperture mask: a 0.6 px displacement, noise scale 40 px, 1.8 Hz.
- **Inside every aperture**: lens fall-off of 18 % at the rim (radial 0.35r→r), and a field-stop hairline `rgba(238,232,222,.10)` with the ±0.8 px fringe.

### 4.8 Micro-detail system (every item has a job)

1. **Chapter label** (top-left) and **live readout** (top-right). The readout changes *only* when the optics change: f-stops step with the detents; the focal length counts in log steps; R · G · B becomes RGB at registration; AF dots cycle, then become a dash; 1/8 s shows on the blurred clock.
2. **Credits** on every photograph, in Geist Mono 16 px, right-aligned 38–48 px under the aperture (S9 uses 38 so it clears the kicker line). In S6 the credit sits under the readout instead, at (984, 272). Full credits close the film and the carousel.
3. **Focal scale** (S5): an arc at r + 30 from 144° to 216° on the aperture's left, 1 px `rgba(238,232,222,.16)`. Nine ticks (24 35 50 85 135 200 300 400 600): 8 px at .30 opacity, and the current value at 14 px / 2 px / `#EEE8DE`. Labels in Geist Mono 15 at r + 52. The current tick moves with the readout.
4. **Barrel engravings** (S8, C5): agent IDs, timestamps, ALLOW · ASK · DENY, knurling, and the 12 o'clock index (§5.6).
5. **FOV cone** (C3): the two exact external tangents between the wide and tele circles.
6. **The violet dot** is the only accent. It appears in three places: our kicker, the focus-confirm light, and the brand mark.
7. **Page index** (carousel) "02 / 07", and the episode date **2026.10.26** on the cover.

---

## 5. Motion language

### 5.1 Easing tokens

| Token | cubic-bezier | Use |
|---|---|---|
| `snap` | (.7, 0, .2, 1), 140–180 ms, plus settle (.3, 0, .3, 1) 90 ms | iris snaps |
| `detent` | (.5, 0, .1, 1), 110 ms + 3 % overshoot, settle 70 ms | every aperture click |
| `glide` | (.22, .61, .12, 1), 600–2400 ms | irises opening, plates splitting and converging, rings arriving |
| `lock` | (.34, 1.56, .64, 1), the last 120 ms of a ring | the 2° overshoot on lock |
| `zoom` | (.65, 0, .35, 1), 700–1400 ms | focal-length zoom, tilt, defocus bridge |
| `drift` | (.33, 0, .67, 1), whole shot | push-ins, pans, aperture growth |
| `reveal` | (.25, .1, .25, 1), 2000 ms | the retina rising |
| `focus-in` | (.16, 1, .3, 1), 560 ms | text entrance (blur 10→0, opacity, scale 1.015→1) |
| `focus-out` | (.7, 0, .84, 0), 320 ms | text exit (blur 0→8, opacity) |
| `bloom` | (.4, 0, .2, 1), 800 ms | silver to colour |

### 5.2 Durations and rhythm

- **Durations**: 3 / 4 / 6 / 9 / 12 / 17 / 18 / 24 / 48 / 72 frames (100 / 133 / 200 / 300 / 400 / 560 / 600 / 800 / 1600 / 2400 ms). 24 frames is one beat.
- **Events on the beat**: cuts, detents, ring locks, the colour bloom, and the second line of the thesis.
- **Stagger**: kicker to first line 120 ms, line to line 140 ms. List items arrive *with the mechanical event* they describe, not on a timer.
- **Limits**: never more than three text elements in motion at once. Exits are simultaneous. A new block never starts before the previous one has fully exited.

### 5.3 Photographs

- **Push-ins**: 3–6 % per shot with `drift`, never past the asset's max scale (§7).
- **Inside-aperture parallax**: the photo moves −1.3× the eyepiece float, so the field stop feels like a real eyepiece in front of the image.
- **No Ken Burns pans across flat photos.** Every move is an optical event: a zoom, a focus change or an aperture change.

### 5.4 The iris (exact geometry)

- **Blades**: N = 9.
- **Twist**: φ = −π/2 + 1.6·(1 − r/r_open)·π/9. The blades rotate as they close, as real ones do.
- **Vertices**: V_i at angle θ_i = φ + 2πi/9, radius r.
- **Aperture edge**: the edge between vertices is a quadratic curve whose control point sits at the mid-angle, at radius r_c = r·cos(π/9) + (r/cos(π/9) − r·cos(π/9))·k, with k = 0.55 + 0.40·r/r_open. The aperture is rounder open and more polygonal stopped down.
- **Visible blade edge i**: P(u) = E + ρ(u)·(cos θ, sin θ), with θ = θ_i + 0.95u and ρ = r + (R_o − r)·u^0.8, for u ∈ [0, 1].
- **Blade i's region**: curve i, then the outer arc from θ_i + 0.95 through +2π/9, then curve i+1 reversed, then the aperture edge back to V_i.
- **Blade fill**: a linear gradient from P_i(0.45) to P_{i+1}(0.45), going rgb(22+9κ) → rgb(15+4κ). Warmth is +1 on R and −2 on B. κ = 0.5 + 0.5·cos(θ_mid + 135°) is the key light from the upper left.
- **Blade edges**: a shadow first, 3 px `rgba(0,0,0,.55)` offset (1.2, 1.2) with 7 px blur, then a highlight, 1.1 px `rgba(238,232,222, .08 + .16κ)`.
- **Blade tips**: the aperture outline at 1 px `rgba(238,232,222,.14)`.
- **Outer ring**: 16 px, with a conic gradient `#141312 → #211F1C (upper left) → #141312 → #0F0E0D`, an inner hairline at .12 and an outer one at .06.
- **Instances**: the film iris uses r_open 300 and R_o 368. The cover uses r 112 and R_o 290. The end iris uses r_open 420 and R_o 440.
- **Proofs**: f01, f04, c1. Drawn in Canvas2D (vector, crisp at any scale), not WebGL.

### 5.5 Transitions (complete list)

- **Iris snap** (S1)
- **Iris open with pull-back** (S2 → S3)
- **Detent stops, then close to black** (S4)
- **Iris open on a new subject** (S4 → S5)
- **Zoom-through** (S5): 12-sample radial blur, cut on the peak frame
- **Tilt into the sky** (S5 → S6)
- **One plate splits into three** (S6)
- **Defocus bridge** (S6 → S7): both images at 22 px blur, 0.6 s crossfade
- **Hard cut on a clock tick** (S7 → S8)
- **Hard cut on a bayonet click** (S8, clock → barrel)
- **Barrel recedes into darkness** (S8 → S9)
- **Planet rises from black** (S9)
- **Iris closes on the eye** (S10 → S11)

There are no dissolves between unrelated images, no slides, no glitch effects and no whip pans.

### 5.6 The barrel rings (exact geometry)

- **Ring band** (r0–r1):
  - Base: conic gradient `#151413 → #23201D (upper left) → #151413 → #100F0E`.
  - Inner-edge highlight: an arc from 0.85π to 1.85π at 1 px, `rgba(238,232,222,.14)`.
  - Outer edge: 1 px `rgba(0,0,0,.9)`.
- **Ticks** on the inner edge: major 9 px at `rgba(207,199,186,.55)`, minor 5 px at .28. They are skipped within ±15° of 12 o'clock.
- **Labels**: the CJK label sits on the mid-radius, centred at 12 o'clock, engraved (1 px dark offset below the fill). The Latin tag starts 14 px after it.
- **Legends**: they never enter the zone from canvas angle −140° to −25°.
- **Ring C**: knurled with 300 radial 1.2 px lines on its outer 11 px, skipping ±17° at the top.
- **Index**: 2×14 px `#EEE8DE` at r 314–328, plus 2×8 px at r 148–156.

| Ring | Radii (film) | Label | Ticks (minor / major) | Engraved legends |
|---|---|---|---|---|
| A | 160–198 | 身份 IDENTITY | 6° / 30° | ID·01 … ID·12 every 30° |
| B | 210–250 | 记录 LOG | 2° / 10° | 09:41:02 … 09:41:10 every 40° |
| C | 262–306 | 权限 POLICY | 10° / 30°, knurled | ALLOW · ASK · DENY at 160° / 180° / 200° |

**Motion**: each ring arrives from scale 1.06 and −24° / +18° / −12°, then locks with `glide` + `lock`. The point of the scene is the last frame of each lock: **the labels land exactly on the index**. The alignment is done mechanically, outside the glass, while the blank coin in the middle never changes.

### 5.7 Signature moves (the portfolio moments)

1. **Price by the stop (S4).** A mechanically correct 9-blade iris clicks down five stops on 24 faceless tokens. Each detent is a semitone lower, and the readout steps ƒ/2 → ƒ/8. Then the iris snaps shut, and there is 0.4 s of real silence. You hear the price war.
2. **Colour only where they overlap (S6, C4).** Three silver plates of the deepest image ever taken drift together. A detuned triad comes into tune as they register, and colour exists only at the moment, or in the region, where all three agree. Tested in look-dev: pure RGB primaries read as a cheap glitch and were rejected. Silver plates read as glass negatives on a lightbox.
3. **The last element (S9–S11).** A red planet rises in the eyepiece and turns out to be a human retina. The camera pushes into the fovea, the iris closes on it, and the violet focus-confirm light comes on with the double beep. The brand appears as the moment the picture is in focus.

Bonus craft moment: **aligned outside the glass** (S8), with the rings locking onto the index.

---

## 6. Sound design (all synthesized: numpy / scipy, 48 kHz float32, stereo)

Built on the helpers in `f2/synth.py` (`env_exp`, `lp`, `hp`, `bp`, `fade`, …). The harmony runs from D minor (opening) to **D major** (the eye), with the major third withheld until 53.6 s.

### 6.1 Instruments (recipes)

| Name | Recipe |
|---|---|
| **Drone** | D2 73.42 Hz + A2 110 Hz sines at −30 dBFS, plus a saw on D2 through a 2-pole LPF at 300 Hz (cutoff LFO ±80 Hz at 0.07 Hz). Two decorrelated copies, detuned 0.3 %, width 70 %. |
| **Felt piano** | Additive. Partials n = 1…14 at f_n = n·f0·√(1 + B·n²), B = 0.00035. Amplitude n^−1.4·e^(−n/9). Decay τ_n = τ0 / (1 + 0.35(n−1)), with τ0 = 2.8 s·(220/f0)^0.4. Attack 6 ms raised-cosine. Hammer felt: white noise × e^(−t/3 ms) through BP 900–2800 Hz at −26 dB. Release 120 ms. |
| **Glass bell** (plates) | FM. Carrier f_c, modulator 1.4·f_c, index 1.6·e^(−t/0.35) + 0.3, amplitude e^(−t/2.4 s). Plus a sine pad at f_c with a 400 ms attack. A `cents` parameter glides to 0 with `glide`. |
| **Detent click** | Noise × e^(−t/0.6 ms) through BP 2.5–6 kHz. Modes 3.2k / 5.1k / 7.4k·p Hz with τ 12 / 8 / 5 ms and amplitudes 1 / .6 / .35. Body: a 180·p Hz sine, τ 12 ms, −8 dB. 60 ms total. p = 2^(−k/12) for detent k. |
| **Iris clack** | 9 detent ticks at p 1.2 and −12 dB, spread over 0–18 ms with ±1 ms jitter (one per blade). Then a main click at 20 ms (p 0.9), an FM metal ring (2.1 kHz carrier, 3.3 kHz modulator, index 2, τ 60 ms, −10 dB) and a 58 Hz sine thump (τ 45 ms, −6 dB). |
| **Bayonet lock** | A detent click (p 0.8). 20 ms later, a clunk: noise LPF 700 Hz × e^(−t/25 ms) plus a 92 Hz sine (τ 40 ms). Then a metal tail: FM with modulator 2.71·f_c, index 1.2, τ 0.9 s, −22 dB, f_c = 1.6k / 1.35k / 1.1k for rings A / B / C. |
| **Servo whir** | Saw at 160–240 Hz, its frequency following the optical move's speed, through BP 400–1500 Hz. Amplitude follows \|velocity\|, −32 dB. |
| **Air** | Pink noise through a band-pass whose centre sweeps 400→3000 Hz (log), Q 1.2, raised-cosine envelope, −24 dB. |
| **Clock** | Tick: noise τ 0.8 ms through BP 1.8–2.4 kHz, plus a 2.0 kHz sine (τ 6 ms). Tock: the same at 1.7 kHz. Alternating, accelerating from 8 to 10 Hz. |
| **AF beep** | E7 2637 Hz sine, 55 ms, 3 ms fades, two onsets 120 ms apart, −16 dBFS, **dry**. It is a device, not music. |
| **Room / café / hum** | Pink noise LPF 1.2 kHz at −56 dBFS throughout; the café is −48 dB and warmer. Floodlight hum: 120 / 240 / 360 Hz at 1/n amplitudes, −46 dB, 0.3 Hz AM. |
| **Sub swell** | Sine sweeping 32→45 Hz over 2 s, raised-cosine, −24 dB. |
| **Reverb** | Synthetic IR: decorrelated stereo noise × e^(−t·6.91/T60), T60 2.6 s, 18 ms pre-delay, LPF 6 kHz, plus 6 early taps between 7 and 31 ms (−10 to −18 dB). Applied with `fftconvolve`. Sends: piano 22 %, bells 30 %, clicks 6 %, beep 0 %. |

### 6.2 Cue sheet (aligned to §2.1)

| t (s) | Event | Sound | Level / pan |
|---|---|---|---|
| 0.00 | Film starts | Room tone + drone fade-in 400 ms | −56 / −30 dBFS, wide |
| 0.20 | Iris snap | Iris clack (9 blade ticks) | peak −8 dBFS, centre |
| 2.40 / 4.00 | Token lines | Piano A4, F4 *pp* | −22 dB RMS, ±0.15 |
| 7.20 | Pull-back to the tray | Piano D4 | −20 dB |
| 8.00–11.20 | Faces wear off | 24 soft ticks + brushed noise; the hero's tick lower at 10.60 | −34 / −28 dB, scattered ±0.4 |
| 12.80, 13.60, 14.40, 15.20, 16.00 | Detents | Detent click k = 0…4 + piano D3 · C♯3 · C3 · B2 · B♭2 | −10 dB peak, centre |
| 16.40 | Iris closes | Soft clack; drone out in 60 ms | −14 dB |
| 16.40–16.80 | Black | **Silence** (room tone only) | −60 dB |
| 16.80 | Iris opens on the espresso | Breath (air, 300 ms) + F maj add9 pad + café tone | −30 / −48 dB |
| 19.60–21.00 | Zoom-through | Servo whir + air sweep 400→3000 Hz | −32 / −24 dB |
| 20.30 | Cut to the rocket | One tiny tick | −30 dB |
| 21.00 | Tele | Dm9 pad (D3 F3 A3 E4) + floodlight hum | −30 / −46 dB |
| 24.00–24.80 | Tilt into the sky | Air sweep down→up | −26 dB |
| 24.80 | Plates split | Glass bells A4 / C♯5 / E5, detuned −38 / +27 / −19 cents | −24 dB, L / R / C |
| 26.40–28.80 | Plates converge | Detune glides to 0 | — |
| 28.80 | Colour bloom | Chord +4 dB, reverse-reverb swell 800 ms | −20 dB |
| 30.40–31.00 | Defocus bridge | Chord LPF 8 kHz → 700 Hz | — |
| 31.00–36.80 | AF hunting | Servo whir following focus velocity; **no beep** | −32 dB |
| 34.40 | 现在，他不这么想了 | Piano D2 + F3 | −20 dB |
| 36.00 | (pre-lap) | Ticking fades in | −40 dB |
| 36.80–38.40 | Clock | Ticks 8→10 Hz | −24 dB |
| 38.40 / 39.20 / 40.00 | Rings lock | Bayonet locks A / B / C | −10 dB peak, −0.2 / 0 / +0.2 |
| 40.00–44.80 | Barrel | B♭ pad (B♭2 D3 F3) + 41 Hz pulse every 1.6 s | −32 / −30 dB |
| 44.80–45.20 | Darkness | **Silence** | — |
| 45.20–47.20 | Planet rises | Sub swell 32→45 Hz + high pad D maj add9 | −24 / −30 dB |
| 46.40 | 最后一片镜片，是眼睛。 | Piano D5 over D2 | −18 dB |
| 48.80 | Eval line | Piano A4 – F♯4 – D4, 0.4 s apart | −20 dB |
| 52.80 | 模型会降价。 | Piano D3 · A3 · F♯4 | −18 dB |
| 53.60 | 眼光不会。 | Piano A4 + D5 (the D major completes) | −18 dB |
| 56.00 | Iris closes on the eye | Soft clack, 9 blade ticks | −14 dB |
| 56.48 / 56.60 | Focus-confirm light | **AF beep-beep** (E7, the chord's 9th) | −16 dBFS, dry, centre |
| 56.80–59.20 | End card | Chord tail + room tone; 30 ms fade at 59.2 | — |

### 6.3 Mix

- **Loudness**: −14 LUFS integrated, using a K-weighting implemented with scipy biquads per BS.1770. True peak ≤ −1 dBTP, checked at 4× oversampling.
- **Output**: 48 kHz / 24-bit WAV, then AAC 256 kbps at mux.
- **Mono-compatible**: clicks and the beep are centre-mono.
- **Feel**: no compression on the clicks. Their dynamics *are* the tactility.

---

## 7. Asset treatment recipes

These are the reference implementation in `kit/prep.py`, and the outputs are in `kit/img/`. Crop boxes are in **source** pixels. "Max display" is the largest scale at which the photo still holds detail; past it, the film uses only defocused or blank states.

| Photo | Used in | Crop (source px) | Grade | Masks / extras | Max display |
|---|---|---|---|---|---|
| `coins.png` 384×303 L | S1–S4, S8; C1, C2, C5 | Hero #15: box (182, 163)–(243, 224), centre (212.4, 193.1), r 23.5. Tray: full frame, centre (192, 152). | warm silver | Watershed segmentation (§7.1), 24 masks feathered 0.7 px; wear model | Faces **4.5×** (coin ⌀ ≤ 212). Blank coin 4.6× in r ≤ 134. Tray 2.0× sharp; 2.6× only while defocused (S1 frame 0). |
| `coffee.png` 600×400 | S5; C3 | Circle centre (292, 200), r 200 (film) / r 200 at 1.3× (C3). Zoom anchor = crema (288, 148). | sat 0.84, highlight amber 0.07 | — | **1.5×** |
| `rocket.jpg` 640×427 | S5–S6; C3 | Film: circle centre (322, 213) r 210 → (322, 228) r 110. C3: centre (322, 212) r 96. | sat 0.80, shadow teal 0.05, gain 0.95 | Heat shimmer at the tele end | **2.0×** |
| `hubble_deep_field.jpg` 1000×872 | S6; C4 | (220, 150)–(780, 710), 560×560 | Plates: each channel ×1.35 + 0.035 → silver × 0.72, screen-blended. Colour: ×1.25, sat 0.86, lift 0. | Disc mask r 277 feathered 0.8 px; triple intersection mask (C4) | 1.0× (plates), 1.5× crops |
| `text.png` 448×172 L | S7 | Circle centre (224, 86), r 86 | warm silver | Planar depth d = (y−64)/86 + 0.15(x−224)/224; DOF stack (§7.5) | **2.45×**, and only while blur ≥ 2 px |
| `clock_motion.png` 400×300 L | S8 | Circle centre (212, 152), r 140 | warm silver | ±1.5 px jitter per tick | 1.5× (already motion-blurred) |
| `retina.jpg` 1411×1411 | S9–S11; C6 | Circle centre (704, 703), **r 690** (excludes the fundus camera's orientation notch at about 1:30) | sat 0.92, gain 0.92, highlight 0.06, shadow 0.04 | Planet terminator: linear gradient lower-right, 0.55 → 0 | Full disc 0.62×; fovea end **1.36×** of source |

### 7.1 Coins: segmentation and wear
- **Masks**: Sobel elevation, then watershed with markers below 30/255 (cloth) and above 150/255 (metal), then fill holes. That gives 24 regions, sorted by row then column. The table (centre, radius, bbox) is in `kit/img/coins.json`. The hero is #15, the facing head.
- **Wear** (`wear()`), with ρ = distance/r:
  - Blank: `blank = μ·(1 + 0.07·(−(dx+dy)/(√2·r))) + 0.12·highpass(σ 1.5)`, where μ is the mean tone inside 0.9r and the 0.07 term is a key light from the upper left.
  - Local wear: `w_loc = clip(1.4w − 0.4ρ)`, so the high relief at the centre goes first.
  - The outer 10 % (the rim) is kept, so the token still reads as struck metal.
- **Order**: coins wear farthest-from-the-hero first, with a 110 ms stagger; the hero gets an extra 0.3 s. `tray_mid.png` is the state at 1.6 s into the cascade (proof f03).
- **Upscale**: Lanczos3 + unsharp (radius 1.2 display px, 25 %), then silver. Grain is applied at display resolution, so it is sharper than the image and masks the softness.

### 7.2 Espresso
- Wide view at 1.5×, which fills the r 300 aperture (source r 200 = the full image height).
- The zoom-through targets the crema at (288, 148), stopping at 2.4×, already under 18 px of radial blur.

### 7.3 Rocket
- The rocket's body sits in columns 314–329, nose at y ≈ 127. All crops keep the nose in frame.
- Pad lights get halation 0.22 in the finishing pass so they star. Shimmer happens only at ≥ 1.6×, where atmospheric softness is what a real 600 mm lens shows.

### 7.4 Hubble plates
- The three channels are near-identical in structure (correlation .88–.97), but individual galaxies differ in brightness, which is true of filtered exposures.
- They are presented as *R / G / B channel plates of the published colour composite*, never as Hubble filter names.
- Film offsets are (−160, −120), (+160, −120), (0, +150) from E. Plates are always screen-blended on `--ink`. Composite with `lighten` on a canvas pre-filled with ink: a transparent canvas shows a seam, which the look-dev caught.

### 7.5 Handwriting: synthetic depth of field
- A focus stack at σ levels 0, .5, 1, 1.5, 2, 3, 4, 5 source px is interpolated per pixel.
- Blur is `σ_display = min(22, 9·A·|d − d_f|)`.
- The original photo is sharp only in the band y ≈ 40–90 (measured by Laplacian energy), so d = 0 is placed there. Focus can only reach that band, and the hunt is written so that it never rests there.
- Pre-render all 174 frames (S7) or a 16-step stack and crossfade between them in the page.

### 7.6 Clock
- The image is already a motion blur, so magnification is free. It appears for 1.6 s, as "time running", under 微软不等…

### 7.7 Retina
- The r 690 mask removes the camera notch, so the disc reads as a planet until the caption.
- The optic disc at (249, 657) gets halation 0.20, which reads as sunlight on a planet.
- The fovea at (703, 705) sits at the eyepiece centre, so the final push needs no pan.

**Not used, and why**:
- `earth-*`: the globe is the AI cliché, and a world-map crop on a Chinese platform risks 问题地图 compliance.
- `astronaut.png`, `grace_hopper.jpg`: US flags and real people as metaphors would distract.
- `camera.png`: the "observer" beat was cut for clarity.
- `moon.png`: redundant with the retina-as-planet.
- HDRIs: there is no 3D in this film.

---

## 8. Risks, and how we avoid looking AI-made or cheap

| Risk | Mitigation |
|---|---|
| Small photos look soft | Every photo has a measured max scale (§7). Apertures are sized to the pixels. Larger views happen only in states that are *meant* to be soft: defocus, telephoto haze, a blank coin. Lanczos + unsharp happen in prep, and grain is applied at display resolution. |
| The iris or rings read as clip-art or HUD | The geometry is that of real irises and lens barrels (9 blades with twist; engraved, knurled bands). Anodised material is built from two gradients and two hairline weights. There is no glow, no animated HUD and no scanning lines. Rings hold still once locked. Proofs: f01, f08, c5. |
| The RGB split looks like a glitch effect | Silver plates, slow `glide` convergence, colour only at registration or in the intersection. Pure-primary RGB was tested and rejected. |
| The metaphor is too nerdy | Each optical device is paired with one plain sentence. The chapter names are everyday words on Xiaohongshu. The film works even if you ignore the metaphor, because the copy carries all four judgments. The cover subtitle invites the decoding (一支镜头的六个部件…). |
| The "planet" feels like a trick | We claim nothing false. The terminator is just lighting. The caption 人眼眼底照片 arrives at 46.6 s, 1.4 s after the disc is fully visible, and the line itself says it is an eye. |
| Attribution slips | A kicker system (判断 / 他说 / 他认为 / 据报道 / ● 我们的理解) sits above every non-fact line. The copy deck (§2.4) is proofread against §1.4. No quotation marks. The forbidden lines are absent. |
| WenKai reads too casual | It is used only three times in the film. If test viewers find it soft, switch our voice to Noto Serif SC at weight 300 at the same sizes; the violet-dot kicker still labels it. |
| A dark film feels monotonous or dim on phones | Text contrast is 16:1. The colour script runs silver → warm → blue → silver/colour → red → violet. The retina is the brightest, warmest image, by design, at the climax. Two 0.4 s silences reset the ear. |
| Text collides with Xiaohongshu UI | All essential text is within y 1148–1444 and x 96–953 (the longest line). Nothing essential sits below 1460 or in the right-hand button column. |
| Fonts measure wrong in headless Chromium | Two-pass layout plus baseline probes (§4.4). |
| Render cost on SwiftShader | No WebGL is needed: Canvas2D plus DOM, with deterministic `renderAt(t)`. DOF and shimmer are precomputed or run in the Python finishing pass. |
| Too many devices start to feel like a showreel | Each device appears in exactly one chapter, with one photo and one sentence, and the transitions are optical events from the same camera. Restraint is enforced by the beat grid: there is no beat with two simultaneous ideas. |

**Build path.** Write `f2/film.html` with `window.renderAt(t)`, porting `iris()`, `ring()`, `photo()`, `T()` and `K()` from `kit/lookdev.html`, with every animation a pure function of t. Render with `f2/render.mjs`, finish with `f2/film.py` (keyed `look.json`), score with a `synth.py`-based script following §6, mux with ffmpeg. The carousel is `post.html` with the frame layouts in §3; every one is already proofed in `kit/lookdev.html?f=c1…c7`.
