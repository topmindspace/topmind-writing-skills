# Changelog

## 0.1.1 (2026-10-18)

- 随包新增共享脚本 `check_article.py`：长文文章文件夹（`<文章名>/<文章名>.md`）体检，改稿移动段落或图片后跑一次
- `de_ai_lint.py` 的 W18：图片下一行写了「来源：自制，数据：…」也算标清楚；`audit-provenance.py` 的 `--draft` 可以直接给文章文件夹

## 0.1.0 (2026-10-18)

- 首发：改稿与质检技能，四种模式（只审不改 / 改稿 / 嵌入 / 快审），流程「事实 → 逻辑 → 删冗余 → 去 AI 味 → 核心经验对照 → 排版 → 保真审计 → 过度改稿检查」
- 规则来自共享的 `core-voice.md`（场景规则）和 `de-ai-rules.md` v2（结构模式 + 改写边界）；脚本 `de_ai_lint.py` 分 W 警告 / H 提示两级
- 新增 `revise_check.py`（数字、引语、专名、确定性词保真比对 + 过度改稿比例）和 `count_words.py`（统一字数口径）
- topmind-wechat-post / topmind-x-article 写长文时默认组合本技能；单独安装时按随包的 `revision-workflow.md` 手动走一遍
