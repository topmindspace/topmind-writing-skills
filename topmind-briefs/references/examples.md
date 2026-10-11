# 示例 · 干货短文（自编示例）

> 说明：以下均为自己编写的示例，模型名、基准名、数字皆为虚构，仅用来演示各类型的结构，不对应任何真实帖子或账号。
> X 版不用 Markdown 列表（X 不渲染），分点一律用 emoji 项目符号，规则见 [x-post-format.md](x-post-format.md)；
> 每个 X 版示例末尾带“话题标签建议”（0–2 个，另给 1 个备选），规则见 `platform-specs.md`。
> 公众号版保留 Markdown 列表。
> 例 2、例 4 超过 280 字符，发布时按 thread 拆条（首条放结论和图，次条放细分与收束）；`lint_x_post.py` 对超长帖会给出字数警告，拆条后再检查。

## 例 1：数据榜单型

结构模式：先抛一个反直觉判断 → 甩基准 → 给最扎眼的数字 → 图证明。

```
A smaller model can still be the better buy.

On ToyBench-Tasks, Model A completes 64% of tasks at roughly $0.25 each.

For a 300-task run, that is about $75 in total,
several times cheaper per task than Model B.

[图：上下两张柱状图——任务完成率 vs 单任务成本]

#ToyBench #AIAgents
```

话题标签建议：`#ToyBench #AIAgents`（备选 `#LLMEval`）

结构拆解：
1. 判断句开头（观点一句）
2. 基准是什么（一句）
3. 最扎眼的数字（64%、~$75、几倍差价）
4. 图：完成率和成本两张图并置

## 例 2：榜单速报型

```
Just in: Model C now sits at #2 on ToyArena Chat with 1380 pts,
and #4 on ToyArena Code with 1310 pts.

Price: $3 per million tokens, the lowest among the top five.

Strongest categories:
🔹 Math
🔹 Long documents
🔹 Multilingual prompts

+12 pts over Model D; up three places since the last update.

[图：两个榜单的排行榜截图各一张]

#ToyArena
```

话题标签建议：`#ToyArena`（备选 `#AIRankings`）

结构拆解：
1. "Just in:" + 排名 + 分数（开头即全部关键信息）
2. 价格/性价比（一句）
3. 细分维度展开（emoji 列表，每条一行）
4. 纵向对比（比上次、比邻位）
5. 图：排行榜实拍

## 例 3：论文解读型

```
Short notes can replace long chat histories for agents.

New idea: let the agent write its own memory notes while it works.

🔹 Keep what the next step needs
🔹 Drop what it does not
🔹 Notes live in a plain file, no extra service

[图：论文信息图——流程示意 + 三组对比曲线]

#AIAgents #Memory
```

话题标签建议：`#AIAgents #Memory`（备选 `#PaperNotes`）

结构拆解：
1. 判断句开头（有观点，后面有实证；X 里不加粗，靠第一行位置突出）
2. 方法名/思路一句 + 3 条 emoji 要点（每条 ≤10 词）
3. 图：论文原图（流程 + 结果）

## 例 4：机制讲解型

```
How a cache saves your API bill, step by step.

Every request pays for the same long prompt prefix again.
A prompt cache stores that prefix so repeat calls skip the cost.

1️⃣ Put the stable text first
[机制，一句]

2️⃣ Send the changing part last
[机制，一句]

3️⃣ Check the hit rate in the usage report
[机制，一句]

In short:
🔹 Stable prefix: cached.
🔹 Variable tail: billed normally.
🔹 Savings show up as cache hits.

[视频：缓存命中流程动画]

#PromptCaching #LLMOps
```

话题标签建议：`#PromptCaching #LLMOps`（备选 `#APICost`）

结构拆解：
1. 标题句（"How X works, step by step."）
2. 痛点（一句：现有做法缺什么）
3. 机制分步（1️⃣ 2️⃣ 3️⃣ 序号，每步一句）
4. "In short:" 三行收束（🔹）
5. 媒体：流程图/动画 + 文章链接

---

## 公众号版改写示例（例 1 → 公众号）

```markdown
# 300 个任务约 $75：ToyBench-Tasks 基准实测

> 小模型也可能更划算——在 ToyBench-Tasks 上，模型 A 以更低成本拿到了不错的完成率。

- 基准：ToyBench-Tasks，测智能体完成多步任务的能力
- 完成率：模型 A 完成 64% 的任务
- 成本：单任务约 $0.25，跑 300 个任务总计约 $75，
  单任务成本比模型 B 低数倍

![ToyBench-Tasks：任务完成率 vs 单任务成本](图)

来源：某评测机构（示例）
```

改写要点：X 版英文直发；公众号版加一句中文背景（"这是什么基准"），
数字保留英文原样，结论不变。

### 公众号稿 → X 稿：列表怎么转

同一选题的两个版本只允许排版差异，数字、结论、条数、顺序保持一致：

```markdown
<!-- 公众号稿：Markdown 列表 -->
- 基准：ToyBench-Tasks
- 完成率：模型 A 完成 64% 的任务
  - 单任务成本约 $0.25
```

```text
X 稿：emoji 项目符号，二级条目缩进两格
🔹 基准：ToyBench-Tasks
🔹 完成率：模型 A 完成 64% 的任务
  ▫️ 单任务成本约 $0.25
```

---

## 反例（不要这样写）

❌ "众所周知，AI 发展日新月异。最近，Google 发布了一款新模型，
   引起了广泛关注。值得一提的是，这款模型在多个基准上表现出色…"
   → 铺垫三段，结论藏在最后，没有具体数字。

❌ "大幅提升""显著改善""表现优异"
   → 没有数据的形容词，删掉或换成数字。
