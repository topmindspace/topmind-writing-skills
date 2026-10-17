# de-ai-rules.md · 去 AI 味规则表（必过步骤）

> 适用：topmind-briefs / topmind-viral-posts / topmind-x-article / topmind-wechat-post 成稿前**必过**；topmind-format 只报告命中、不改字（用户要求改写时才改）。
> 规则是我们自己在改稿里反复踩出来的：AI 味多半来自**句式和结构**，换掉几个词不够。
> 脚本列：`W9` `W15` `W16` `W17` `W18` = `scripts/lint_x_post.py` 会自动提示；`人工` = 脚本查不准，靠通读。

## 一、改写边界（先守住，再动手）

1. **只改表达，不改事实**：数字、日期、人名、产品名、引语原文、链接一个不动。
2. **确定性不升不降**：原文「可能」不改成「一定」，原文「已发布」不改成「据称」。厂商数字仍标「厂商口径」，传言仍标「传言」。
3. **不编**：不为了「像人」去加经历、对话、情绪、第一人称或口头禅；原文没有的细节，宁可空着。
4. **术语不换**：专业词、产品名保持原样，不为了避免重复换同义词。
5. **改完回读**：每一处改动都能说出「哪条规则、为什么」；说不出的，恢复原文。

## 二、中文结构模式

| 编号 | 模式 | 典型样子 | 改法 | 脚本 |
|---|---|---|---|---|
| Z01 | 否定式对照 | 「不是 A，而是 B」「真正的 X 从来不是……」 | 直接写 B；要留余地写「现在看起来更像 B」 | W9 |
| Z02 | 递进套句 | 「不仅……更……」「不仅……还……」 | 拆成两句，或只留更重要的那件 | W9 |
| Z03 | 三连排比 | 「更快、更稳、更聪明」 | 留有数据的那一项，配上数字 | W9 |
| Z04 | 四字词堆叠 | 「高效便捷、安全可靠、灵活多变」 | 换成一个具体事实 | 人工 |
| Z05 | 公式化计数标签 | 「三个词」「一句话说清」「五个分支」「三件事」 | 「简单总结」「主要 5 个方向」「有三大特征」，或直接列出来 | W9 |
| Z06 | 设问自答 | 「为什么？答案很简单：……」 | 直接给结论 | W15 |
| Z07 | 揭晓式冒号 | 「答案是：……」「真相是：……」 | 去掉揭晓，直接说 | W15 |
| Z08 | 升华收尾 | 「这才是 X 的意义」「这或许就是未来」 | 停在一个判断、建议或具体问题上 | W15 / W9 |
| Z09 | 抽象拔高 | 「归根结底」「本质上，」「某种程度上」 | 删掉，后面那句通常能单独成立 | W15 |
| Z10 | 铺垫过渡 | 「话不多说」「接下来让我们」「下面来看看」 | 删掉，直接进正文 | W15 |
| Z11 | 「进行 + 动词」 | 「进行了深入分析」「进行优化」 | 「分析了」「优化了」 | W15 / W9 |
| Z12 | 对冲叠加 | 「或许可能」「可能……也许」 | 只留一个，或给出依据 | W15 |
| Z13 | 无出处权威 | 「专家指出」「业内人士认为」 | 写清是谁、在哪说的；找不到就删 | W15（同行有数字 / 出处 / 引号不报） |
| Z14 | 空洞期许 | 「未来可期」「让我们共同期待」 | 删掉，或换成一个可验证的时间点 | W15 / W9 |
| Z15 | 客服腔 | 「希望对你有帮助」「欢迎留言交流讨论」 | 删掉；要互动就问一个具体问题 | W15 |
| Z16 | 机械连接 | 「首先 / 其次 / 最后」「综上所述」 | 用列表或序号承载顺序 | W9 |
| Z17 | 假强调 | 「值得注意的是」「划重点」 | 删掉，把内容挪到段首 | W9 |
| Z18 | 空泛形容 | 「颠覆性」「重磅」「全方位」「无缝」 | 换成参数、价格、日期、对比 | W9 |
| Z19 | 过度对称 | 每段一样长、每条列表同字数、「一方面……另一方面……」 | 长短交错，按信息量写 | 人工 |
| Z20 | 段段小结 | 每节最后一句复述本节 | 删掉复述，读者刚读过 | 人工 |
| Z21 | 同义轮换 | 同一个东西一会儿叫「模型」一会儿叫「系统」「方案」 | 全文一个叫法 | 人工 |
| Z22 | 处处平衡 | 每个观点后面都补「当然也有……」 | 只在确有反例时写，并给出反例 | 人工 |
| Z23 | 首段复述标题 | 开头把标题换个说法再讲一遍 | 首行给结论或最扎眼的事实 | 人工（短文 W10 查首行长度） |

## 三、英文结构模式

| 编号 | 模式 | 典型样子 | 改法 | 脚本 |
|---|---|---|---|---|
| E01 | Negation pivot | "It's not X, it's Y" / "This isn't just X" | State Y directly | W16 |
| E02 | Not-just-but | "not just fast, but also cheap" | Two plain claims, or the one that matters | W16 |
| E03 | Signpost opener | "Here's the thing", "Let's dive in", "Without further ado" | Start with the point | W16 |
| E04 | Wrap-up filler | "In conclusion", "At the end of the day", "The bottom line is" | End on a claim or a question | W16 |
| E05 | Transition stack | Sentences opening with "Moreover," "Furthermore," "Additionally," | Drop the connector; order carries the logic | W16 |
| E06 | Inflated vocabulary | delve, tapestry, testament to, pivotal, vibrant, seamless, game-changer | Plain verbs and concrete facts | W16 |
| E07 | Role inflation | "plays a pivotal role", "serves as a", "stands as a" | "is", "does", or the actual effect | W16 |
| E08 | Hedge stack | "It's worth noting that", "It is important to note" | Delete; say the thing | W16 |
| E09 | Chatbot residue | "I hope this helps", "Great question", "Feel free to reach out" | Delete | W16 |
| E10 | Era opener | "In today's fast-paced world" | Start with the fact | W16 |
| E11 | Rule of three | Three adjectives or three clauses every time | Keep the one with evidence | 人工 |
| E12 | Uniform rhythm | Every sentence 15–20 words, every paragraph 3 sentences | Vary length; short sentences are fine | 人工 |

## 四、标点与版面

| 编号 | 模式 | 改法 | 脚本 |
|---|---|---|---|
| P01 | 破折号堆叠（短文超过 2 处；长文每千字超过 3 处） | 多数换成逗号、句号或冒号 | W17 |
| P02 | 感叹号堆叠（短文超过 2 个；长文每千字超过 3 个） | 语气靠事实 | W17 |
| P03 | 标点连用「！！」「？！」 | 一个就够 | W17 |
| P04 | 大段文字（长文单段超过约 110 字） | 拆短段，或「一句概要 + 列表」 | W14 |
| P05 | 自制图不标注 | 图注写「自制」和数据来源，例如「自制，数据：xx 官方」 | W18（`--long` / `--md`） |
| P06 | 表情堆砌 | 短文按 emoji 体系；段子零 emoji | W8 / W13 |

## 五、怎么跑

```bash
python3 scripts/lint_x_post.py X稿.txt              # 短文：W9 W15 W16 W17
python3 scripts/lint_x_post.py X发布稿.txt --long    # 长文：再加 W14
python3 scripts/lint_x_post.py 公众号稿.md --md      # Markdown 稿：W9 W14–W18，不查 Markdown 语法
```

- 警告不影响退出码；交付前要么改掉，要么能说明为什么保留（例如引语原文、专有名词里恰好有这个词）。
- 脚本刻意收窄，宁可漏报也不误报；「人工」列的模式要靠通读：朗读一遍，拗口、像念稿的地方就改。
