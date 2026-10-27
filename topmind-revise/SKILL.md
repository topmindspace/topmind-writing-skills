---
name: topmind-revise
description: "审查、润色、精简或重写已有稿件，按用户目标选择修改深度，核对事实与作者声音。支持长文、短帖、回复、标题和只审不改；纯排版用 topmind-format，平台导出用对应长文技能。"
license: MIT
metadata:
  version: "0.1.8"
  action_category: "write"
  triggers: "改稿, 帮我改改, 改回复, 看看这条回复, 改转发点评, 按我以前的帖子改, 改一下这篇, 精简, 润色, 去 AI 味, 去AI味, AI 味太重, 改得像人写的, 审稿, 质检, 质量检查, 三关, 事实核查这篇, 保真审计, 按我的意见改, 改标题, 起标题, 写摘要, 检查一下这篇, revise, edit this draft, proofread, de-AI, make it sound human, quality check"
  author: "TopMindSpace"
  homepage: "https://github.com/topmindspace/topmind-writing-skills#readme"
  updated: "2026-10-27"
---

# topmind-revise · 改稿与质检

让稿子更贴近作者想表达的内容。先理解修改目标，再决定动结构、补解释、压冗余还是只修局部；成效由读者是否理解、事实是否准确、作者是否认可来判断。

## 按需借鉴与积累

需要新方向、完整例子或相关经验时，用 [知识使用与增补](references/knowledge-library.md) 检索修改深度、有效保留与作者反馈；先读摘要，再选相关卡片。可以混合、改造或采用库外思路，简单任务直接完成。知识不替代当前用户要求；新反馈先作为有范围的候选，不自动改长期规则。

## 先绑定目标

使用宿主明确传入的文章路径、选区或用户直接提供的原文。目标文章与参考资料分开；不能通过全局遍历猜“当前文章”。没有目标先问清楚；已有目标直接读它，未保存或执行中发生变化则请用户核对后继续。简单改稿只读必要参考，不把整套方法论、所有脚本和作者所有旧文当作必读清单。

区分只审不改与实质改稿。默认根据已读原稿核对事实表述、数字、归因和内部逻辑；明确要求外部核查、补新事实或对动态事实存疑时才检索相关来源，并遵守宿主的联网范围。交付完成后结束；重复无进展、连续失败或能力不足时说明卡点，不无条件续跑。

## 选择合适深度

| 模式 | 何时用 | 交付 |
|---|---|---|
| `audit` | 用户只要检查 | 具体问题、证据与建议，不改原稿 |
| `revise` | 用户要求改稿、润色、精简 | 改后稿与关键改动理由 |
| `embed` | 写作技能成稿后的自查 | 完成稿；重要疑点另说 |
| `quick` | 短帖、标题、回复、局部修改 | 一份可用版本，必要时加备选 |

默认中文，用户要求与原文语言优先。`genre`、`reader`、`notes`、`samples`、`sources`、`source_draft`、`depth` 可作上下文，不要求用户逐项填参数。只改措辞就局部处理；全面重写或结构整改的授权已包含对应结构调整，不重复请求许可。

## 看参考，找真正的问题

有作者样本就实际读几段，辨认其句长、幽默、术语、情绪与叙事习惯；一篇样本说明一种场景，不自动成为所有体裁的标准。[创作方法与样张](references/creative-practice.md) 展示同一素材的多种成立方式。

先通读再看 lint。把“读者会误解什么、哪里断了、哪里重复”说具体，而不是从某个词推断“像 AI”。选择 [口吻经验](references/core-voice.md)、[信息设计](references/information-design.md) 或 [修改流程](references/revision-workflow.md) 的相关部分即可。

## 改稿方法

1. 对现有文件实质修改前保留可恢复版本：已有版本控制、用户指定备份或时间戳副本都可以。聊天里的短文本可直接给改后稿。
2. 看主线与结构。资讯可以结论先行，故事可以从场景进入，教程可以按操作展开。改动深度跟用户目标走。
3. 核对承重事实、论证与归因；优先核动态、新增、存疑或被改动的内容。保留范围、近似值和确定性；查不到的明确列出，见 [fact-check.md](references/fact-check.md)。
4. 尝试更合适的表达。可以删重复，也可以补必要解释；类比、问句、第一人称、长句、对仗都有适用场景。有效段落保留，合理改动无需命中规则编号。
5. 回读改前改后：事实、态度和引用是否被改坏，读者是否更容易理解，作者是否还认得自己的声音。重要取舍给一句理由；小改无需逐条报告。

## 检查工具

```bash
python3 scripts/de_ai_lint.py 稿子.md
python3 scripts/lint_x_post.py 短帖.txt
python3 scripts/revise_check.py 改前.md 改后.md --report 改稿报告.md
python3 scripts/audit-provenance.py --draft 改后.md --source 源稿.md
python3 scripts/count_words.py 稿子.md
```

`revise_check.py` 的事实变化与改动比例是复查线索，不证明事实错误或过度修改；全面改写本来就可能改动很多无 lint 命中的段落。`--declare 报告.md` 可记录结构、事实、作者意见等依据。段落级溯源适合同构派生稿；重组、多源综述改用主张与数字逐项核对。

[de-ai-rules.md](references/de-ai-rules.md) 是需要定位问题时的诊断表，所有写法信号都需要上下文。W/H/I 不要求清零，分数不作定稿门槛。格式破损、缺图等实际问题修复后再交付。

## 报告与作者校准

简单改稿给结果和一两句重要说明。长文全面审校、多源整合或用户要审计时，写完整报告：主要改动、事实依据、未核实项、保留的取舍；[report-template.md](references/report-template.md) 可按需取用。

作者要校准风格时，可按 [calibration-drill.md](references/calibration-drill.md) 做匿名候选对比：保持素材、篇幅与事实相同，给作者选并说明喜欢什么。未经真实选择不声称质量提高。只在用户要求记录时沉淀带场景与例外的偏好。

更多改前改后见 [examples.md](references/examples.md) 和 `examples/`。作者帖子统计可用 `scripts/post_type_report.py`，不把相关性当成因果或爆款保证。

独立使用无需外部技能；格式化用 `topmind-format`，平台导出用 `topmind-wechat-post` / `topmind-x-article`。本技能改稿，不执行发布。
