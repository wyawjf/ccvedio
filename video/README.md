# 《当智慧像电一样便宜》1 分钟视频

3D + 2.5D 风格的竖屏短片（1080×1920，30fps，约 62 秒），全部由代码生成：

- **画面**：Three.js 实时渲染（无头 Chromium + SwiftShader），后期叠加辉光、色差、暗角、胶片颗粒
- **2.5D 小人**：`src/lib/figure.js` 参数化骨骼 + 墨线排线风格，画在 canvas 上，再贴到朝向镜头的面片上
- **字幕与排版**：DOM 叠加层（Noto Sans SC / Anton / Inter），每帧由镜头代码给出
- **配音**：Kokoro v1.1-zh（sherpa-onnx 离线推理），用 SenseVoice 反向识别校对读音
- **配乐**：`audio/score.py` 程序化合成，所有重音卡在画面事件上（爆发、墙倒、开门、白场）

## 结构

| 文件 | 内容 |
|---|---|
| `script.json` | 口播稿：每句的配音文本、字幕文本、停顿 |
| `audio/tts.py` | 生成 `build/vo.wav` 和 `build/timeline.json`（每句起止时间，画面据此卡点） |
| `audio/score.py` | 生成配乐并与口播混音，输出 `build/mix.wav` |
| `src/shots/protein.js` | 镜头 1：17 万 vs 2 亿，蛋白质山爆发 |
| `src/shots/stairs.js` | 镜头 2：食物 / 力气 / 信息 / 智慧 四级台阶 |
| `src/shots/title.js` | 镜头 3：当智慧像电一样便宜 |
| `src/shots/walls.js` | 镜头 4：疾病 / 寿命 / 出身 / 梦想 / 时间 五堵墙倒下 |
| `src/shots/door.js` | 镜头 5：活下去 → 毕业 → 你敢不敢想 + 片尾 |
| `render.mjs` | 逐帧渲染，`--stills` 出静帧，`--from/--to` 出视频片段 |

## 重新生成

```bash
npm install
# 配音（需要 kokoro-multi-lang-v1_1 模型目录）
python3 audio/tts.py <kokoro_dir> script.json build 60 1.0
python3 audio/score.py build
# 画面：可分段并行
node render.mjs --from 0 --to 20.7 --out build/segments/a.mp4
node render.mjs --from 20.7 --to 41.3 --out build/segments/b.mp4
node render.mjs --from 41.3 --to 70 --out build/segments/c.mp4
# 合成
./mux.sh
```
