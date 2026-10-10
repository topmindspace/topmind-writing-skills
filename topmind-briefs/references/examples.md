# 示例 · 干货短文（自编示例）

> 说明：以下均为自己编写的示例，模型名、基准名、数字皆为虚构，仅用来演示各类型的结构，不对应任何真实帖子或账号。
> 自己写 X 版时，列表符号按 `style-guide.md` 用纯文本 `• ` / `▪ ` / emoji
>（X 不渲染 Markdown）；下面示例里为了便于阅读使用了 `- `，实际发布时请替换。

## 例 1：数据榜单型

结构模式：先抛一个反直觉判断 → 甩基准 → 给最扎眼的数字 → 图证明。

```
Cheaper models are not always weaker models.

On DemoBench-Agent, Model A solves 71% of tasks at about $0.40 per task.

The good news: for a 200-task batch, the total bill is ~$80 —
up to 10x cheaper per task than Model B.

[图：上下两张柱状图——任务解决率 vs 单任务成本]
```

结构拆解：
1. 判断句开头（一句话观点）
2. 基准是什么（一句话）
3. 最扎眼的数字（71%、~$80、10x）
4. 图：解决率和成本两张图并置

## 例 2：榜单速报型

```
Big news: Model C just landed #1 in DemoArena Text with 1500 pts,
and #5 in DemoArena Code with 1400 pts!

Blended $5/MToken — the most cost-efficient model on the Pareto frontier.

#1 in Coding, Hard Prompts, Instruction Following, Creative Writing.
+15 pts above #2 Model D; up from #9 in the previous release.

[图：两个榜单的排行榜截图各一张]
```

结构拆解：
1. "Big news:" + 排名 + 分数（开头即全部关键信息）
2. 价格/性价比（一句话）
3. 细分维度展开（列表）
4. 纵向对比（比上次、比第二名）
5. 图：排行榜实拍

## 例 3：论文解读型

```
‼️Letting a model manage its own context can beat hand-designed pipelines!

Introducing 🩵Demo Context Models🩵
- Decide what to keep and what to drop
- Treat context as an editable file
- Learn the policy in the weights, no extra harness

[图：论文信息图——架构示意 + 四组结果曲线]
```

结构拆解：
1. 加粗判断（有观点，但后面有实证）
2. "Introducing X" + 3 条 bullet（每条 ≤10 词）
3. 图：论文原图（架构 + 结果）

## 例 4：机制讲解型

```
Reranking for RAG, clearly explained!

Hybrid search gives you a shortlist. It does not decide which passages
actually contain the evidence. That missing judgment is where a reranker fits.

→ Retrieve wide
[一句话机制]

→ Score every candidate together
[一句话机制]

→ Let code apply the threshold
[一句话机制]

To summarise:
- Retrieval finds the candidates.
- The reranker decides what deserves context.
- The LLM writes the grounded answer.

[视频：RAG 流程架构动画]
```

结构拆解：
1. 标题句（"X, clearly explained!"）
2. 痛点（一句话：现有方案缺什么）
3. 机制分步（→ 标记，每步一句话）
4. "To summarise:" 三行收束
5. 媒体：流程图/动画 + 文章链接

---

## 公众号版改写示例（例 1 → 公众号）

```markdown
# 200 个任务只要 $80：DemoBench-Agent 基准实测

> 便宜的模型不一定弱——在 DemoBench-Agent 上，模型 A 以更低成本拿到了不错的解决率。

- 基准：DemoBench-Agent，测智能体完成多步任务的能力
- 解决率：模型 A 解决 71% 的任务
- 成本：单任务约 $0.40，跑 200 个任务总计约 $80，
  单任务成本比模型 B 便宜 up to 10 倍

![DemoBench-Agent：任务解决率 vs 单任务成本](图)

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
