# F｜微软CEO：大模型要打价格战了

> 原素材：20VC 播客专访 Satya Nadella，主持人 Harry Stebbings，2026-10-26（周一）上线，约 24 分钟。
> 节目标题：《Satya Nadella on Open vs Closed Models: Who Wins | Whether to Trust Frontier Model Providers | Why Companies Need to Own Their Own Intelligence》

做了两个版本：

| 版本 | 状态 | 文件 |
|---|---|---|
| **图文版**（7 张 3:4 图，小红书图文笔记） | ✅ 已出图，核对完文案就能发 | `video/build/f/carousel/01.png`–`07.png`（01 就是封面） |
| **视频版**（9:16，约 65 秒，原声加中文字幕） | ⏳ 排版和节奏已经定好，还差原片 | 版式预览：`video/build/f/F_preview.mp4`（原声位置是测试图） |

---

## 一、小红书文案（图文版和视频版通用）

**标题（主推）**：微软CEO：大模型要打价格战了（15 字符）

备选：
- 微软自己每天混用模型，你呢？（14）
- 纳德拉：别把宝押在一家模型上（14）
- 做AI产品的注意：模型要变便宜了（16）

**正文**：

> 微软 CEO 纳德拉上周上了 20VC 播客，聊了 24 分钟。给做 AI 产品、做出海的朋友，提炼 4 个判断👇
>
> 01｜算力会变成大宗商品
> 大多数企业日常场景用的算力终将商品化，底层模型会打一场残酷的价格战。最前沿的模型，只属于少数细分市场。
>
> 02｜微软自己每天都在混用模型
> 据报道，Copilot 内部每天都在大量混搭便宜的闭源和开源模型，而不是只押一家。
>
> 03｜私有评测集，才是核心资产
> 他认为每家公司都会有一套自己的私有评测基准（eval），这是最核心的知识产权。
>
> 04｜他承认想错了一件事
> 以前以为模型做大了，「对齐」自然会解决。现在微软不再等，用零信任架构把每个模型包起来。
>
> 我们的理解，3 个动作：
> ① 架构支持多模型切换，别绑死一家
> ② 建一套自己的私有评测集
> ③ Agent 的权限和日志，放在模型之外
>
> 你现在的产品接了几家模型？评论区聊聊～
>
> 来源：20VC 播客专访 Satya Nadella（2026.10.26）

**话题**：#AI创业 #大模型 #微软 #纳德拉 #AI出海 #AIAgent #AI产品经理

**置顶评论**：你们现在接的是哪几家模型？按什么规则切换？

---

## 二、视频版剪辑表（约 65 秒）

| # | 时长 | 画面 | 内容 |
|---|---|---|---|
| 1 | 2.6s | 封面卡 | 大模型要打价格战了 |
| 2 | 1.4s | 章节卡 | 01 算力会变成大宗商品 |
| 3 | ~14s | **原声 c1** | 讲算力商品化、价格战、前沿模型只占少数细分市场 |
| 4 | 1.4s | 章节卡 | 02 微软自己每天都在混用模型 |
| 5 | ~10s | **原声 c2** | 讲 Copilot 混用便宜的闭源和开源模型 |
| 6 | 1.4s | 章节卡 | 03 私有评测集才是核心资产 |
| 7 | ~10s | **原声 c3** | 讲每家公司都会有私有 eval，这是核心 IP |
| 8 | 1.4s | 章节卡 | 04 他承认想错了一件事 |
| 9 | ~14s | **原声 c4** | 主持人问改变过什么看法：对齐不会随规模自然出现，转向零信任 |
| 10 | 5.0s | 卡片 | 给出海 / AI 创业者的 3 个动作 |
| 11 | 3.4s | 结尾卡 | 你现在的产品接了几家模型？加来源 |

原声画面的版式：上面是章节标题，中间是 16:9 原片，下面是中文大字幕和英文小字幕，最底下标注说话人和出处。

### 拿到原片后怎么出片

1. 原片放到 `video/build/f/source.mp4`。
2. 用逐字稿找 4 段原话，关键词写在 `video/f/edl.json` 每段的 `find` 字段里（如 commodit、Copilot、eval、alignment），然后填上 `in` 和 `out`（秒）。
3. 把每段 `subs` 换成**原话的翻译**，`en` 填英文原文，删掉 `draft`。草稿字幕只是意思方向，不能当原话用。
4. 运行下面两条命令：

```bash
node f/render.mjs subs
```

```bash
python3 f/build.py
```

输出在 `video/build/f/F_final.mp4`。如果还有段落没填 in/out，或者字幕还是草稿，`build.py` 会拒绝出片，并列出缺哪些。

改图文或卡片的文字：编辑 `video/f/slides.json`，然后运行：

```bash
node f/render.mjs carousel cards
```

---

## 三、事实核查

| 内容 | 状态 |
|---|---|
| 节目存在、主持人、10/26 上线、约 24 分钟 | ✅ 多家报道一致，纳德拉本人也在 X 上转发过 |
| 算力商品化、价格战、前沿模型只属少数细分市场 | ⚠️ 36Kr、BigGo 转述，没见到逐字原话 |
| Copilot 每天混用便宜的闭源和开源模型 | ⚠️ 36Kr、BigGo 转述 |
| 「Every firm will have a private eval benchmark, which is their core IP」 | ⚠️ BigGo 引用，原话待核 |
| 以前以为对齐会随规模自然解决，现在转向零信任 | ⚠️ The Next Web、Scuttlebutt 报道 |
| ❌ 不要混进来 | 「中性云租算力不是一门生意」是 10/28 **财报电话会**上说的。「用私有 eval 定义什么是好」那句出自他的**文章**，都不是这期播客 |
| ❌ 不要混进来 | 「假设模型已被攻破」是他 10/10 在 **X 上**发的帖子，不是播客原话 |

图文版的措辞已经全部写成转述（「他认为」「据报道」），没有加引号当原话用。发布前最好对照 20VC 的逐字稿（20VC newsletter 里说有 PDF）再扫一遍。

来源：
- https://thenextweb.com/news/satya-nadella-ai-alignment-20vc
- https://getscuttlebutt.substack.com/p/satya-nadella-treat-every-ai-model
- https://eu.36kr.com/en/p/4044987101762441
- https://finance.biggo.com/news/cb058c1f-332c-4939-9434-4b69f88c0df6
- https://finance.biggo.com/news/51a5c20b5cb5987e
- https://20vc.substack.com/p/20vc-newsletter-1st-november-2026
- https://x.com/satyanadella/status/2112986295547134430
