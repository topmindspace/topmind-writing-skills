# topmind-revise · 改稿与质检

[English](./README.en.md) | 中文

**改得更短、更准、更像你本人，还能证明没改坏事实。** 长文、短文、段子、回复、转发点评、标题都能用；可以单独用，也会被 `topmind-wechat-post`、`topmind-x-article` 写长文时默认调用。

- 版本：**v0.1.4**

```bash
npx @topmindspace/topmind-writing-skills install topmind-revise
```

你可以这样说：「改稿」「去 AI 味」「精简一下」「检查一下这篇」「看看这条回复」「起个标题」「按我以前的帖子改」。

## 四种模式

| 你说 | 模式 | 结果 |
|---|---|---|
| 检查一下 / 质检 / 看看哪里 AI 味 | 只审不改 | 改稿报告：命中、建议改法、未核实条目，原稿不动 |
| 改稿 / 精简 / 去 AI 味 / 按我的意见改 | 改稿 | 先备份，再改，写回原文件，附改稿报告 |
| （被长文技能调用） | 嵌入 | 交回终稿和三行摘要，完整报告落盘 |
| 改标题 / 改这条短文 / 看看这条回复 | 快审 | 按快审清单过一遍，给改后版本（回复给两个口吻） |

## 示例：改前 → 改后（原创）

```text
重磅！某编辑器 3.0 发布，AI 编程迎来新纪元！

更新内容：
🔹 补全更快
🔹 支持本地模型
🔹 插件市场改版

这不仅是一次更新，更是开发方式的变革。

#AI编程
```

```text
某编辑器 3.0 发布，可以接本地模型了

更新内容：
· 补全更快
· 支持本地模型
· 插件市场改版

#AI编程
```

改动依据：「重磅」「新纪元」是播报腔；「不仅…更是…」是递进套句；升华收尾删掉；首行换成读者最关心的变化。事实一条没动。更多见 [`examples/`](./examples/)。

## 流程

⓪ 结构 → ① 事实 → ② 逻辑 → ③ 删冗余 → ④ 去 AI 味 → ⑤ 措辞原则对照 → ⑥ 排版 → ⑦ 保真审计 → ⑧ 过度改稿检查。

快审清单（短文、段子、回复）：首行、口径、短帖模式 S01–S10、删尾测试、回复先接住对方再补自己的信息、精炼不砍双音词、对照作者样本。

```bash
python3 scripts/de_ai_lint.py 稿子.md                       # 长文：W 警告 + H 提示 + I 信息设计提示
python3 scripts/lint_x_post.py 短文.txt --kind news          # 快讯
python3 scripts/revise_check.py 改前.md 改后.md --report 改稿报告.md
python3 scripts/post_type_report.py 我的帖子.jsonl --samples-out 样本习惯.md   # 有往期帖子时
```

## 规则分层

| 层 | 文件 | 管什么 |
|---|---|---|
| 写作原则 | [references/social-writing-principles.md](./references/social-writing-principles.md) | 先想清楚传达什么、结论先行、形式跟着内容走 |
| 信息设计 | [references/information-design.md](./references/information-design.md) | ⓪ 结构诊断：骨架、我的判断、内容 → 形式、I1–I9 提示 |
| 措辞口吻 | [references/core-voice.md](./references/core-voice.md) | 十条措辞原则 + V01–V40 场景例子 |
| 审稿 | 本技能 + [references/de-ai-rules.md](./references/de-ai-rules.md) | 改写边界、长文模式、社交短帖 S01–S10，按 [revision-workflow.md](./references/revision-workflow.md) 出报告 |

## 防过度改稿

每处改动对应一条规则编号或一句作者意见；没命中的段落不动；W 警告每条有结论，H 提示只供判断；`revise_check.py` 统计「没命中却被改写」的段落占比，超过 30% 提示可能改过头。有作者样本时，句长和标点习惯跟样本走。

## 何时不用

从零写稿 → `topmind-wechat-post` / `topmind-x-article` / `topmind-briefs` / `topmind-viral-posts`；只排版 → `topmind-format`；封面配图 → `topmind-cover` / `topmind-poster`。本技能不代发。
