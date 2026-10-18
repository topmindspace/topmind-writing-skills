# topmind-revise · 改稿与质检

[English](./README.en.md) | 中文

把一篇稿子改得更短、更准、更像作者本人，并且能证明没改坏事实。长文、短文、段子、回复、标题都能用；可以单独用，也会被 `topmind-wechat-post`、`topmind-x-article` 写长文时默认调用。

- 版本：**v0.1.2**（随 `@topmindspace/topmind-writing-skills@0.8.46` 发布）

## 安装

```bash
npx @topmindspace/topmind-writing-skills install topmind-revise
```

## 用法

| 你说 | 模式 | 结果 |
|---|---|---|
| 检查一下 / 质检 / 看看哪里 AI 味 | 只审不改 | 改稿报告：命中、建议改法、未核实条目，原稿不动 |
| 改稿 / 精简 / 去 AI 味 / 按我的意见改 | 改稿 | 先备份，再改，写回原文件，附改稿报告 |
| （被长文技能调用） | 嵌入 | 只交回终稿和三行摘要，完整报告落盘 |
| 改标题 / 起标题 / 写摘要 / 改这条短文 | 快审 | 一个改后版本，最多附 2 个候选 |

流程：事实 → 逻辑 → 删冗余 → 去 AI 味 → 核心经验对照 → 排版 → 保真审计 → 过度改稿检查。

```bash
python3 scripts/de_ai_lint.py 稿子.md                     # W 警告 + H 提示
python3 scripts/de_ai_lint.py 短文.txt --genre short --no-hints
python3 scripts/count_words.py 改前.md 改后.md
python3 scripts/revise_check.py 改前.md 改后.md --report 改稿报告.md
```

## 三层规则

| 层 | 文件 | 管什么 |
|---|---|---|
| 核心经验 | [references/core-voice.md](./references/core-voice.md) | 场景规则：标题、开头、收尾、数字、引用、来源行、列表、emoji…… |
| 去 AI 味 | [references/de-ai-rules.md](./references/de-ai-rules.md) | 改写边界 + 结构模式（Z / E / P 编号），脚本 W / H 两级 |
| 执行 | 本技能 | 按 [references/revision-workflow.md](./references/revision-workflow.md) 跑完并出报告 |

## 防过度改稿

每处改动要对应一条规则编号或一句作者意见；没命中的段落不动；W 警告要求每条有结论，H 提示只供判断；`revise_check.py` 统计「没命中却被改写」的段落占比，超过 30% 提示可能改过头。

## 边界

从零写稿 → `topmind-wechat-post` / `topmind-x-article` / `topmind-briefs` / `topmind-viral-posts`；只排版 → `topmind-format`；封面配图 → `topmind-cover` / `topmind-poster`。本技能不代发。

## 开发

```bash
python3 scripts/audit_skill.py
python3 scripts/package_skill.py --check
python3 scripts/negative_tests.py
```
