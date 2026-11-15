---
name: topmind-revise
description: "审查、润色、精简或重写已有稿件，用“跟朋友说话 vs 完成写作任务”诊断去 AI 味，核对事实边界并保留作者真实口吻与褒贬。支持长文、短帖、回复、标题和改稿复盘学习；纯排版用 topmind-format，平台导出用对应长文技能。"
license: MIT
metadata:
  version: "0.1.9"
  action_category: "write"
  triggers: "改稿, 帮我改改, 改回复, 看看这条回复, 改转发点评, 按我以前的帖子改, 改一下这篇, 精简, 润色, 去 AI 味, 去AI味, AI 味太重, 改得像人写的, 审稿, 质检, 质量检查, 三关, 事实核查这篇, 保真审计, 按我的意见改, 改标题, 起标题, 写摘要, 检查一下这篇, 复盘改稿, revise, edit this draft, proofread, de-AI, make it sound human, quality check"
  author: "TopMindSpace"
  homepage: "https://github.com/topmindspace/topmind-writing-skills#readme"
  updated: "2026-11-15"
---

# topmind-revise · 改稿、去 AI 味与经验沉淀

让稿子更贴近作者真正想表达的内容：砍掉通稿负担与 AI 任务腔，立住认知切口、干货原件与真人温度。成效由**读者是否一眼看懂、事实边界是否准确、作者是否还认得自己的声音**来判断，而不是靠清空词表警告来证明。

## 一、核心诊断总开关与改稿五大原则

每看到一句别扭或像 AI 写的话，先问这一个问题：
> **「这句话是在完成一项写作任务，还是在跟朋友说话？」**

1. **砍掉八类 AI 任务负担**：
   - 删掉替读者把话讲完的说教尾巴、自我解释的元话语（「先别急着」「准确说」「官方建议很直接」）、新闻通报式的购买门槛与致谢花絮、凑整齐的排比与套类比、以及文末强行升华的漂亮比喻。
   - 把居高临下的讲师命令（「别无脑开最高档」）改成邻座商量（「都开最高档吗？可能大多数时候次高档就够了...」）；把抽象参数译成日常体感。
2. **执行删尾测试**：把最后半句或最后一段删掉读一遍，只要意思已经到位或留白更有张力，就直接删掉。
3. **减弱无依据的绝对因果 ≠ 洗掉作者个人口吻**：
   - 当原稿带有作者的主观态度（如「仔细聊了一轮，实际上感觉对认真做原创的作者绝对是更利好了」），改稿时把缺乏实证的「绝对」减弱，补上「代码参数变动 ≠ 线上已全面生效」的事实边界，但**必须保留「仔细聊了一轮，我倒觉得……未必是坏事 / 感觉更有利」的个人温度**，严禁洗成冷冰冰的官方通报腔。
4. **评测与观点稿保留真实褒贬**：
   - 即使外部都在「吹爆」某个产品，只要作者原稿有具体观察维度和实测褒贬，就按具体维度客观展开，不改成「各有优劣，看场景吧」的和稀泥套话。
5. **严守第一人称「我」的边界，不瞎改已认可的好稿**：
   - 原稿没有个人亲历时，绝不为了「去 AI 味」代编「我看到」「刚打开试了下」。
   - 如果初稿的钩子、算账或切口已获作者认可，只做段落空行或标点微调，绝不推翻大改。

需要完整改前改后案例时，按 [knowledge-library.md](references/knowledge-library.md) 检索 `de-ai-mechanisms`、`revise-learn-from-edits`、`brief-value-first`、`brief-news-to-post`、`voice-peer-stance` 等卡片。

## 二、选择合适深度与绑定目标

使用宿主明确传入的文章路径、选区或用户直接提供的原文；对现有文件做实质修改前保留可恢复版本，聊天中的短文本直接交付改后稿。

| 模式 | 何时用 | 交付 |
|---|---|---|
| `audit` | 用户只要检查或诊断 | 具体问题（切口/负担/事实边界）、证据与修改建议，不动原稿 |
| `revise` | 用户要求改稿、润色、去 AI 味、精简 | 可直接使用的改后稿 + 关键删加理由 |
| `quick` | 短帖、标题、回复、局部调整 | 直接给可用成品，必要时附 1 个不同切口的备选 |
| `learn` | 用户给出自己的定稿，要求复盘学习或沉淀经验 | 拆解「删了什么负担、补了什么支点」，标明适用范围后沉淀卡片 |

## 三、向作者改稿学习与扩展知识库

当用户展示自己修改后的定稿、或提出新的创作思考时（详见 [revision-workflow.md](references/revision-workflow.md)）：
1. **先做删加对照**：列出作者删掉了哪些通报/说教负担，增加了哪些钩子、原件或边界。
2. **标注适用范围（Scope Tagging）**：明确该经验适用于哪类稿型（如 X 短帖、评论回复、还是公众号插件介绍文），不把单篇修改意见外推成全库硬门禁。
3. **方便扩展入库**：使用 `python3 scripts/knowledge.py add` 将「场景—机制—正反例—负面边界」写入知识包，供后续任务按需调用。

## 四、辅助检查工具（只供复查，不卡死创作）

```bash
python3 scripts/de_ai_lint.py 稿子.md
python3 scripts/lint_x_post.py 短帖.txt
python3 scripts/revise_check.py 改前.md 改后.md --report 改稿报告.md
python3 scripts/audit-provenance.py --draft 改后.md --source 源稿.md
python3 scripts/count_words.py 稿子.md
```

- [de-ai-rules.md](references/de-ai-rules.md) 是定位问题的诊断思路表，所有信号均由上下文决定去留。`W/H/I` 提示不要求清零，词面分数不作为定稿门槛。
- 承重事实、数字与引语核对见 [fact-check.md](references/fact-check.md)；长文全面审校需要完整报告时可参考 [report-template.md](references/report-template.md)；风格盲选校准见 [calibration-drill.md](references/calibration-drill.md)；更多示例见 [examples.md](references/examples.md)。
- 仅做纯文本排版用 `topmind-format`，平台导出用 `topmind-wechat-post` / `topmind-x-article`。本技能只负责改稿与审校，不执行对外发布。
