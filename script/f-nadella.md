# F｜微软CEO：大模型要打价格战了

> 原素材：20VC 播客专访 Satya Nadella，主持人 Harry Stebbings，2026-10-26（周一）上线，约 24 分钟。
> 节目标题：《Satya Nadella on Open vs Closed Models: Who Wins | Whether to Trust Frontier Model Providers | Why Companies Need to Own Their Own Intelligence》

## 现在的版本：F2《第十二张》

**创意**：片中的 11 张照片，全部是开源代码库（scikit-image、matplotlib）自带的公开示例图，也就是计算机视觉的公开考题。我们用它们讲纳德拉对模型价格战的四个判断。最后镜头拉远，它们原来是一张印样，第 12 格是空的：那是你的私有评测集，唯一下载不到的一张。

| 交付 | 状态 | 文件 |
|---|---|---|
| **视频**（1080×1920，59 秒，无配音，字幕 + 合成配乐） | ✅ | `video/build/f2/F2_final.mp4` |
| **图文**（7 张 3:4，01 是封面，也作视频封面） | ✅ | `video/build/f2/carousel/01.png`–`07.png` |

- 设计规范（文案、时间轴、配色、字体、动效、声音全部锁定）：`video/f2/DESIGN_BIBLE.md`
- 出片流程和每个文件的分工：`video/f2/prod/README.md`
- 之前两版（平面卡片版、漫画框版）客户已否掉，文件留在 `video/build/f/` 里作对照。

---

## 一、小红书文案（视频和图文通用）

**标题（主推）**：微软CEO：大模型要打价格战了（15 字符）

备选：
- 11 张公开图，第 12 张是你的（14）
- 纳德拉判断：模型层会有一场残酷的价格战（19）

**正文**：

> 20VC 播客 10 月 26 日这一期，纳德拉谈了四个判断。以下据公开报道整理，均为转述：
> 1. 大多数企业场景的日常算力终将商品化，模型层会有一场残酷的价格战；前沿模型只服务少数顶级场景。
> 2. 据报道，微软 Copilot 内部每天都在混用便宜的闭源与开源模型。
> 3. 每家公司都会有自己的私有评测集，那会是它的核心 IP。
> 4. 他以前以为规模够大、对齐自然会来，现在不这么想了；微软先把模型包进零信任架构。
>
> 我们的解读：模型会降价，眼光不会。
>
> 这 11 张照片，都是开源代码库自带的公开示例图。第 12 张，留给你。
> 你的评测集里，第一道题考什么？评论区聊聊。

**话题**：#AI出海 #大模型 #纳德拉 #20VC #AI创业

**置顶评论**：换模型之前，你会先拿哪道题考一遍？

---

## 二、拿到原片后（可选）

成片不依赖原片，单独就能发。如果之后拿到原片（要么在环境的网络设置里放行 `youtube.com`，要么把视频上传到 `video/build/f/source.mp4`），可以按 bible §3.4 插入一段原声：

- 只插一段，位置二选一：f380（价格战之后）或 f860（改变看法之前），长度为整拍，最多 8 拍（6.4 秒）。
- 为了保持在 60 秒内，按 §3.4 删掉 7 拍（token 一句、视网膜升起缩短、S06 第二行、片尾少一拍）。
- 字幕必须是这段音频的核实翻译，不加引号，下方标注「字幕为翻译」。

---

## 三、事实核查

| 内容 | 状态 |
|---|---|
| 节目存在、主持人、10/26 上线、约 24 分钟 | ✅ 多家报道一致，纳德拉本人也在 X 上转发过 |
| 算力商品化、价格战、前沿模型只属少数细分市场 | ⚠️ 36Kr、BigGo 转述，没见到逐字原话 |
| Copilot 每天混用便宜的闭源和开源模型 | ⚠️ 36Kr、BigGo 转述 |
| 「Every firm will have a private eval benchmark, which is their core IP」 | ⚠️ BigGo 引用，原话待核 |
| 以前以为对齐会随规模自然解决，现在转向零信任 | ⚠️ The Next Web、Scuttlebutt 报道 |
| 片中 10 张图与 scikit-image 0.26 自带数据逐像素一致；Grace Hopper 与 matplotlib 3.9.2 自带文件 sha256 一致 | ✅ 已复核（bible 附录 C） |
| 图片授权：除 09 月面图（scikit-image 未注明授权）外，均为公有领域、CC0 或无已知版权限制；05 视网膜图作者 Mikael Häggström | ✅ 片尾和图文第 7 张按这个口径写 |
| ❌ 不要混进来 | 「中性云租算力不是一门生意」是 10/28 **财报电话会**上说的。「用私有 eval 定义什么是好」那句出自他的**文章**，都不是这期播客 |
| ❌ 不要混进来 | 「假设模型已被攻破」是他 10/10 在 **X 上**发的帖子，不是播客原话 |

片中和图文里纳德拉的话全部写成转述（宋体，上方有「他判断」「据报道」之类的引导语），没有加引号当原话用。我们的观点都标了「■ 我们的解读」。发布前最好对照 20VC 的逐字稿（20VC newsletter 里说有 PDF）再扫一遍。

来源：
- https://thenextweb.com/news/satya-nadella-ai-alignment-20vc
- https://getscuttlebutt.substack.com/p/satya-nadella-treat-every-ai-model
- https://eu.36kr.com/en/p/4044987101762441
- https://finance.biggo.com/news/cb058c1f-332c-4939-9434-4b69f88c0df6
- https://finance.biggo.com/news/51a5c20b5cb5987e
- https://20vc.substack.com/p/20vc-newsletter-1st-november-2026
- https://x.com/satyanadella/status/2112986295547134430
