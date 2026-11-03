# Brief — F, full redesign: "微软CEO：大模型要打价格战了"

## Who / where
- Account: **Coo-Coo出海Ai实验室** (Xiaohongshu). Audience: Chinese AI founders, product people, people building for overseas markets.
- Previous film by the account (for brand continuity only, NOT a template): `video/build/final.mp4`, its spec `video/DESIGN.md` (violet `#5B2EFF`, paper `#F6F3EE`, ink `#15121b`, comic caption boxes). Two earlier attempts at F (flat editorial cards, then comic boxes — see `video/build/f/carousel/*.png`) were **rejected by the client as rough / "looks AI-made" / not premium**.

## What the client asked for (verbatim, then meaning)
> 多加入一些真实的图片，有电影感，设计感一定要很高级，不要很粗糙，要很细节。你可以设计东西很少，但是每一个东西都要设计的很细节、很细致，像人类设计出来的，不要像 AI 做的东西，整个画面一定要很高级，有电影感，然后要顶级优异设计师的动效作品集。非常有创意这种感觉啊，重新设计整个从头到尾重新设计。

- More **real photographs**. **Cinematic**. Very **premium**, never rough; obsessive detail.
- **Few elements, each one crafted** — restraint over quantity.
- Must feel **human-designed, not AI-made** (no generic gradients, no box-everything layouts, no centered-everything, no clip-art, no emoji, no filler ornaments, no "tech glow" clichés, no random HUD junk).
- Standard: a **top motion designer's portfolio piece**. **Very creative**. Redesign **from scratch, start to finish**.

## Deliverables
1. **Vertical film** 1080×1920, 30 fps, **45–60 s**, standalone (we do NOT have the interview footage; the film must work without it — text-led + real photos + motion + sound). No voice-over (the account's films are silent-text + music). Optionally design 1–2 "slots" where a 6–10 s soundbite of Nadella could later be inserted, but the film must be complete without them.
2. **Xiaohongshu carousel** 1080×1440 (3:4), **5–7 frames**; frame 1 doubles as the cover (it is also the video cover). Must read as one designed set with the film.

## Content — what we may say (all from secondary reporting of one interview; paraphrase only, never present as verbatim quotes)
Source: 20VC podcast, host Harry Stebbings, guest Satya Nadella (Microsoft CEO), published **2026-10-26** (Monday), ~24 min. Episode title: "Satya Nadella on Open vs Closed Models: Who Wins | Whether to Trust Frontier Model Providers | Why Companies Need to Own Their Own Intelligence".

1. Everyday compute for most enterprise scenarios will ultimately be **commoditized**; the model layer will face a **brutal price war**; cutting-edge (frontier) models will serve only a **small number of top-tier niches**.
2. Reportedly, Microsoft **Copilot internally mixes and matches cheap closed-source and open-source models every day** (not one provider).
3. He believes **every company will have its own private evaluation benchmark (eval), and that will be its core IP**.
4. Asked what he changed his mind about: he used to think **alignment would just "fall out" of scale**; he no longer thinks so. Microsoft doesn't wait for alignment to be solved — it **wraps models in a zero-trust architecture** (each agent gets an identity, its tool/model calls are logged, policy/permissions live outside the model).

Rules:
- Attribute as 纳德拉认为 / 他判断 / 据报道 / 他说. No quotation marks around Chinese paraphrases of his words.
- Do **not** attribute to this podcast: "neocloud capacity renting is not a business" (that was the 10/28 earnings call); "assume the model is compromised" (an X post on 10/10); "private evals define what good looks like" (an essay).
- Our own takeaways (e.g. "build multi-model routing", "build your private eval") must be visibly labelled as **our reading** (我们的理解 / 我们的解读), not his words.
- General fact OK: AI APIs are priced per **token**. "Token" in English also means a coin-like disc used instead of money (subway token, trade token).
- Tone: crisp, intelligent, calm. No hype words (颠覆、炸裂、彻底), no fear-mongering. Simplified Chinese.
- Always end with the account mark **Coo-Coo出海Ai实验室** and a small source line.

## Real photographs available (ONLY these; no internet, no stock, no AI image generation)
Contact sheet: `video/assets/lib/_contact.jpg` (open it). Files in `video/assets/lib/`:

| file | px | what | license / credit |
|---|---|---|---|
| earth-night.jpg | 4096×2048 equirect | NASA Earth at Night (city lights) | NASA, public domain |
| earth-blue-marble.jpg | 4096×2048 equirect | NASA Blue Marble | NASA, public domain |
| earth-topology.png | 2048×1024 | relief/bump map for a globe | (derived elevation map) |
| coins.png | 384×303 gray | Greek coins from Pompeii (24 coins on dark cloth) | Brooklyn Museum, no known copyright |
| coffee.png | 600×400 | espresso cup on saucer, wood table | Rachel Michetti, CC0 |
| rocket.jpg | 640×427 | Falcon 9 / DSCOVR on the pad at dusk, 2015 | SpaceX, public domain |
| astronaut.png | 512×512 | astronaut Eileen Collins in orange suit, flag, helmet | NASA, public domain |
| camera.png | 512×512 gray | man with a film camera on tripod, campus | Lav Varshney, CC0 |
| clock_motion.png | 400×300 gray | wall clock, horizontal motion blur | S. van der Walt, public domain |
| hubble_deep_field.jpg | 1000×872 | Hubble eXtreme Deep Field (2012) | NASA, public domain |
| retina.jpg | 1411×1411 | fundus photograph of a human retina (orange disc) | CC0 |
| moon.png | 512×512 gray | lunar surface | (scikit-image sample) |
| text.png | 448×172 gray | handwritten equations on paper, angled | public domain |
| grace_hopper.jpg | 512×600 | Grace Hopper portrait | US Navy, public domain |
| hdri_city/night/lobby/warehouse.exr | 512×256 | Poly Haven HDRIs — lighting/reflections ONLY (too small to show) | CC0 |

**Resolution reality:** most photos are small (≤640 px). Showing them full-bleed at 1080×1920 will look soft. Good designs will show them at or near native size inside large negative space, crop tightly where detail survives, or use them as texture/plates under heavy, deliberate treatment. The Earth maps are 4K and can drive a 3D globe (Three.js) or large crops. Never pass off CG as a photograph.

## Tools (what can actually be built)
- Frames rendered in headless Chromium (Playwright) at 1080×1920: HTML/CSS/SVG/Canvas2D, **Three.js r169** WebGL (SwiftShader — CPU, so keep 3D scenes modest), custom GLSL post (grain, halation, bloom, chromatic aberration, vignette, gate weave, letterbox, light leaks, depth-of-field approximations).
- Python: numpy, scipy, PIL, scikit-image, OpenEXR — image processing (crops, grading, segmentation masks, depth/parallax layers by hand-made masks, duotones, halftones).
- ffmpeg for assembly. **Audio must be synthesized in Python** (no sample libraries): drones, pads, sine/FM bells, felt-piano-like additive tones, filtered-noise whooshes, sub hits, clicks, coin-like metallic FM pings, reverb via convolution with synthetic IR.
- Fonts installed (npm @fontsource): Chinese — **Noto Serif SC 200–900**, **Noto Sans SC** (500/700/900), **LXGW WenKai** (300/500/700), **ZCOOL XiaoWei**; Latin/mono — Inter, **Inter Tight**, **Geist Sans**, **Geist Mono**, **IBM Plex Mono**, **JetBrains Mono**, **DM Mono**, **Instrument Serif** (400 + italic), **Fraunces**, **EB Garamond**, **Cormorant Garamond**, **Newsreader**, Anton.

## Platform constraints (Xiaohongshu)
- Feed UI covers the bottom ~22% (caption, author, buttons) and a right-side button column near the bottom; top ~8% has status/search. Keep essential text inside roughly x 64–1000, y 200–1480 of 1080×1920.
- First 1.5 s must hook. Text must be legible on a phone at a glance (Chinese body ≥ 44 px, headlines much larger); a slow film still has to be readable when paused.
- Cover/frame 1 must work as a small thumbnail in a 2-column grid.
