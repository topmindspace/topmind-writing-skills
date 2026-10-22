# Changelog

## 0.1.4 (2026-10-22)

- 快审清单：首行、口径、社交短帖模式 S01–S10、删尾测试、回复与转发点评（两个口吻）、精炼、作者样本
- 新增 `samples=` 参数和随包脚本 `post_type_report.py`（作者往期帖子的习惯摘要）；`calibration-drill.md` 新增「用数据校准」
- 随包 `core-voice.md` 扩到 V40，`de-ai-rules.md` 新增 S01–S10，`info_design_hints.py` 新增 I9

## 0.1.2 (2026-10-18)

- 新增 ⓪ 结构复查和 `depth` 参数：默认 light 只诊断 + 低风险结构改动（并列段转列表、对照转表格、删重复段），`depth=structure` 才重排章节
- 改稿报告新增「信息设计诊断」，`revise_check.py` 给出改前 / 改后 I 提示数；改动依据可写「⓪ 结构」，`--declare` 时不计入过度改稿
- 随包新增 `info_design_hints.py`、`social-writing-principles.md`、`information-design.md`、`research-mode.md`；`core-voice.md` 改为十条原则，`de-ai-rules.md` 按根因归组

## 0.1.1 (2026-10-18)

- 随包新增共享脚本 `check_article.py`：长文文章文件夹（`<文章名>/<文章名>.md`）体检，改稿移动段落或图片后跑一次
- `de_ai_lint.py` 的 W18：图片下一行写了「来源：自制，数据：…」也算标清楚；`audit-provenance.py` 的 `--draft` 可以直接给文章文件夹

## 0.1.0 (2026-10-18)

- 首发：改稿与质检技能，四种模式（只审不改 / 改稿 / 嵌入 / 快审），流程「事实 → 逻辑 → 删冗余 → 去 AI 味 → 核心经验对照 → 排版 → 保真审计 → 过度改稿检查」
- 规则来自共享的 `core-voice.md`（场景规则）和 `de-ai-rules.md` v2（结构模式 + 改写边界）；脚本 `de_ai_lint.py` 分 W 警告 / H 提示两级
- 新增 `revise_check.py`（数字、引语、专名、确定性词保真比对 + 过度改稿比例）和 `count_words.py`（统一字数口径）
- topmind-wechat-post / topmind-x-article 写长文时默认组合本技能；单独安装时按随包的 `revision-workflow.md` 手动走一遍
