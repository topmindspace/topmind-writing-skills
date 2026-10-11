# 示例 · 干货短文（自编示例）

> 说明：以下均为自己编写的示例，模型名、基准名、数字皆为虚构，仅用来演示各类型的结构，不对应任何真实帖子或账号。
> 自己写 X 版时，列表符号按 `style-guide.md` 用纯文本 `• ` / `▪ ` / emoji
>（X 不渲染 Markdown）；下面示例里为了便于阅读使用了 `- `，实际发布时请替换。

## 例 1：数据榜单型

结构模式：先抛一个反直觉判断 → 甩基准 → 给最扎眼的数字 → 图证明。

```
A smaller model can still be the better buy.

On ToyBench-Tasks, Model A completes 64% of tasks at roughly $0.25 each.

For a 300-task run, that is about $75 in total,
several times cheaper per task than Model B.

[图：上下两张柱状图——任务完成率 vs 单任务成本]
```

结构拆解：
1. 判断句开头（一句话观点）
2. 基准是什么（一句话）
3. 最扎眼的数字（64%、~$75、几倍差价）
4. 图：完成率和成本两张图并置

## 例 2：榜单速报型

```
Just in: Model C now sits at #2 on ToyArena Chat with 1380 pts,
and #4 on ToyArena Code with 1310 pts.

Price: $3 per million tokens, the lowest among the top five.

Strongest categories: math, long documents, multilingual prompts.
+12 pts over Model D; up three places since the last update.

[图：两个榜单的排行榜截图各一张]
```

结构拆解：
1. "Just in:" + 排名 + 分数（开头即全部关键信息）
2. 价格/性价比（一句话）
3. 细分维度展开（列表）
4. 纵向对比（比上次、比邻位）
5. 图：排行榜实拍

## 例 3：论文解读型

```
Short notes can replace long chat histories for agents.

New idea: let the agent write its own memory notes while it works.
• Keep what the next step needs
• Drop what it does not
• Notes live in a plain file, no extra service

[图：论文信息图——流程示意 + 三组对比曲线]
```

结构拆解：
1. 加粗判断（有观点，后面有实证）
2. 方法名/思路一句话 + 3 条 bullet（每条 ≤10 词）
3. 图：论文原图（流程 + 结果）

## 例 4：机制讲解型

```
How a cache saves your API bill, step by step.

Every request pays for the same long prompt prefix again.
A prompt cache stores that prefix so repeat calls skip the cost.

→ Put the stable text first
[一句话机制]

→ Send the changing part last
[一句话机制]

→ Check the hit rate in the usage report
[一句话机制]

In short:
- Stable prefix: cached.
- Variable tail: billed normally.
- Savings show up as cache hits.

[视频：缓存命中流程动画]
```

结构拆解：
1. 标题句（"How X works, step by step."）
2. 痛点（一句话：现有做法缺什么）
3. 机制分步（→ 标记，每步一句话）
4. "In short:" 三行收束
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

---

## 反例（不要这样写）

❌ "众所周知，AI 发展日新月异。最近，Google 发布了一款新模型，
   引起了广泛关注。值得一提的是，这款模型在多个基准上表现出色…"
   → 铺垫三段，结论藏在最后，没有具体数字。

❌ "大幅提升""显著改善""表现优异"
   → 没有数据的形容词，删掉或换成数字。
