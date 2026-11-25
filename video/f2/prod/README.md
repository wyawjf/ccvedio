# F2 出片流程：第十二张 · THE TWELFTH PLATE

视觉、文案、时间轴、声音都以 `../DESIGN_BIBLE.md` 为准，其中 §11 记录了两轮设计评审后的改动（优先于前面各节），配乐的帧号以 `CUES_v2.md` 为准。成片 1796 帧，59.867 秒。

## 环境

- Node：在 `video/` 运行 `npm ci`（字体和 Playwright 都在 package-lock 里）。Chromium 默认用 `/opt/pw-browsers/chromium`，别的位置用环境变量 `PW_CHROMIUM` 指定。
- Python：`pip install opencv-python scikit-image==0.26.0 scipy numpy pillow soundfile pyloudnorm`（本次出片用的版本：opencv 5.0.0、scikit-image 0.26.0、scipy 1.18.1、numpy 2.5.3、Pillow 12.3.0、soundfile 0.14.0）。
- ffmpeg ≥ 6.1，带 libx264。
- 上传版 `F2_final.mp4` 是 2-pass 编码，每次重编码的字节都不一样（画质等价）。发布的是哪一个，以 `script/f-nadella.md` 里记的 sha256 为准。

## 一次性出全片

在 `video/` 目录下依次运行：

```bash
python3 f2/prod/prep.py                      # 调色、钱币分割、哈勃前后景、纸张与压印 → build/f2/cache/
```

```bash
python3 f2/prod/timeline.py                  # 所有字幕的入场/出场、跑头、实时比例读数 → build/f2/type_film.json
```

```bash
node f2/prod/type_render.mjs --data build/f2/type_film.json --out build/f2/type --parts 3   # 字幕层（透明 PNG，按状态去重）
```

```bash
python3 f2/prod/compose.py --jobs 4          # 画面 + 字幕 + 胶片后期，分块并行编码 → build/f2/F2_picture.mp4
```

```bash
python3 -I f2/prod/score.py                  # 合成配乐（按 CUES_v2.md 逐帧对点，自检全部通过才退出 0）→ build/f2/score.wav
```

```bash
python3 f2/prod/compose.py --mux             # 混入配乐 → build/f2/F2_master.mp4（CRF 16 母版，留在本地）和 build/f2/F2_final.mp4（2-pass 约 10 Mbps 的上传版）
```

```bash
python3 f2/prod/carousel.py                  # 图文 7 张 → build/f2/carousel/01.png … 07.png（01 是封面）
```

设计评审用的抽帧包（从编码后的成片里解码）：

```bash
python3 f2/prod/review_kit.py build/f2/F2_final.mp4   # → build/f2/review/
```

查看单帧：

```bash
python3 f2/prod/compose.py --frames 0,770,1795   # 成品静帧 → build/f2/stills/
```

## 文件分工

| 文件 | 内容 |
|---|---|
| `common.py` | 色板、缓动曲线、调色（暖调相纸、硒调黑白）、带抗锯齿的缩放贴图 |
| `geom.py` | 每个镜头的机位：钩子对焦、咖啡漂移、窄缝、路由光、哈勃急停、视网膜升起与收进框、印样拉远与俯冲、纸面拉出 |
| `prep.py` | 只读 `assets/lib/`；输出调好色的全分辨率底片、24 枚钱币的分水岭蒙版和音高表、纸张与压印法线 |
| `picture.py` | 画面层：显影、光圈、窄缝、发丝线、按速度自适应的运动模糊 |
| `timeline.py` | 字幕层的全部文字与时间（bible §2.2、§3.3） |
| `type.html` / `type_render.mjs` | 用 Chromium 排字：两遍字体加载并逐个校验，字体不全就中止 |
| `compose.py` | 合成、调用 `../film.py` 做后期（颗粒、印刷柔化、暗角、片门晃动）、编码 |
| `carousel.py` | 图文 7 张，复用同一套字幕页和底片 |
| `review_kit.py` | 从编码后的成片里抽关键帧、动作序列、小红书界面遮挡模拟，供设计评审 |
| `look.json` | 后期参数和随时间变化的关键帧 |

## 规则提醒

- 片中 11 张照片全部是 scikit-image / matplotlib 自带的示例图，不能换图，也不能加地球、HDRI 之类的素材，否则「这 11 张」就不成立了。
- 纳德拉的话一律是转述（宋体，上方有引导语），不加引号；我们的观点一律加「■ 我们的解读」。
- 不能写进来的内容：财报会上的 neocloud 说法、X 帖子里的「假设模型已被攻破」、文章里的「私有 eval 定义什么是好」。
