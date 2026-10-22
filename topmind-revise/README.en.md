# topmind-revise · Revision and quality checks

English | [中文](./README.md)

**Shorter, more accurate, more like you, and provably no facts broken.** Works on long-form, briefs, duanzi, replies, quote posts and titles; standalone, or called by `topmind-wechat-post` and `topmind-x-article` when they finish a draft.

- Version: **v0.1.4**

```bash
npx @topmindspace/topmind-writing-skills install topmind-revise
```

Say: "改稿", "去 AI 味", "精简一下", "检查一下这篇", "看看这条回复", "起个标题", "按我以前的帖子改".

## Four modes

| You say | Mode | Result |
|---|---|---|
| Check / QA / where does it sound like AI | audit | Report: hits, suggested fixes, unverified items; draft untouched |
| Revise / tighten / de-AI / apply my notes | revise | Back up, edit, write back, plus a report |
| (called by a long-form skill) | embed | Final draft + three-line summary; full report on disk |
| Title / this brief / this reply | quick | Quick checklist, one revised version (two tones for replies) |

## Example: before → after (original)

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

Why: newsreader hype removed, the "not just X but Y" construction and the uplifting closer cut, and the first line now carries the change readers care about. No fact changed. More in [`examples/`](./examples/).

## Flow

⓪ structure → ① facts → ② logic → ③ cut redundancy → ④ de-AI → ⑤ voice check → ⑥ layout → ⑦ fidelity audit → ⑧ over-editing check.

Quick checklist (briefs, duanzi, replies): first line, caliber, social patterns S01–S10, delete-the-tail test, replies pick up the other person's point first, keep two-character words intact, compare with the author's samples.

```bash
python3 scripts/de_ai_lint.py draft.md
python3 scripts/lint_x_post.py brief.txt --kind news
python3 scripts/revise_check.py before.md after.md --report report.md
python3 scripts/post_type_report.py my_posts.jsonl --samples-out habits.md   # with your own post history
```

## Rule layers

| Layer | File | Covers |
|---|---|---|
| Principles | [references/social-writing-principles.md](./references/social-writing-principles.md) | Know the message, lead with it, form follows content |
| Information design | [references/information-design.md](./references/information-design.md) | Structure diagnosis: skeleton, my judgments, content → form, I1–I9 hints |
| Voice | [references/core-voice.md](./references/core-voice.md) | Ten wording principles + V01–V40 examples |
| Review | this skill + [references/de-ai-rules.md](./references/de-ai-rules.md) | Rewrite boundaries, long-form patterns, social S01–S10; report via [revision-workflow.md](./references/revision-workflow.md) |

## Guarding against over-editing

Every edit cites a rule or an author note; untouched paragraphs stay untouched; each W warning needs a decision, H hints are for judgment; `revise_check.py` flags when more than 30% of rewritten paragraphs had no hit. With author samples, sentence length and punctuation follow the samples.

## When not to use

Writing from scratch → `topmind-wechat-post` / `topmind-x-article` / `topmind-briefs` / `topmind-viral-posts`; layout only → `topmind-format`; images → `topmind-cover` / `topmind-poster`. This skill never posts.
