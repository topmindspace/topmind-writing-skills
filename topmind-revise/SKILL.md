---
name: topmind-revise
description: "改稿与质检：改稿、精简、去 AI 味、质量三关（事实 / 逻辑 / 去 AI 味）与保真审计，长文、短文、段子、回复、标题都能用。四种模式：只审不改（出改稿报告）、改稿（先备份再写回）、嵌入（topmind-wechat-post / topmind-x-article 写长文时默认调用，只回终稿）、快审（标题、短文、段子、回复）。规则来自共享的 core-voice（场景规则）和 de-ai-rules（结构模式 + 改写边界）；脚本分 W 警告 / H 提示两级；防过度改稿：没命中的段落不动，每处改动对应规则编号。Use when 改稿、帮我改改、精简、润色、去 AI 味、去AI味、AI 味太重、改得像人写的、审稿、质检、质量检查、三关、保真审计、按我的意见改、改标题、起标题、写摘要、revise、de-AI、proofread。Do NOT use for 从零写一篇新文章（→ topmind-wechat-post / topmind-x-article / topmind-briefs / topmind-viral-posts）、只排版不改字（→ topmind-format）、出 HTML 或排版导出（→ topmind-x-article / topmind-wechat-post）、封面与配图（→ topmind-cover / topmind-poster）、发布。"
license: MIT
metadata:
  version: "0.1.1"
  action_category: "write"
  triggers: "改稿, 帮我改改, 改一下这篇, 精简, 润色, 去 AI 味, 去AI味, AI 味太重, 改得像人写的, 审稿, 质检, 质量检查, 三关, 事实核查这篇, 保真审计, 按我的意见改, 改标题, 起标题, 写摘要, 检查一下这篇, revise, edit this draft, proofread, de-AI, make it sound human, quality check"
  author: "TopMindSpace"
  homepage: "https://github.com/topmindspace/topmind-writing-skills#readme"
  updated: "2026-10-18"
---

# topmind-revise · 改稿与质检

把一篇稿子改得更短、更准、更像作者本人，并且能证明没改坏事实。可以单独用，也可以被写作技能组合调用。

```
声明 + 备份 → ① 事实 → ② 逻辑 → ③ 删冗余 → ④ 去 AI 味 → ⑤ 核心经验对照 → ⑥ 排版 → ⑦ 保真审计 → ⑧ 过度改稿检查 → 报告
```

## 先读：写作原则与信息设计

本技能建立在两份共享文件上，动笔前先读：

- [references/social-writing-principles.md](references/social-writing-principles.md)：8 条社交媒体写作原则（先想清楚、结论先行、每句都有新信息、形式跟内容走、简单清楚、原图优先、站在读者那边、真实有分寸）
- [references/information-design.md](references/information-design.md)：内容 → 形式决策表、篇幅和密度、去啰嗦的判断法
- 措辞和口吻在这两层之上，见 [references/core-voice.md](references/core-voice.md)

改稿：先做结构诊断（⓪），再改措辞；去 AI 味模式表只在改稿和自查时读。

## 语言：默认中文

- **默认中文**：改稿、报告、候选标题都用中文；只有用户明确说要英文时才用英文。
- 英文稿按同一流程走，结构模式用 `references/de-ai-rules.md` 第三节。

## 四种模式

| 模式 | 用户怎么说 | 行为 | 产出 |
|---|---|---|---|
| `audit` 只审不改 | 「检查一下」「质检」「看看哪里 AI 味」 | 跑三关和脚本，不动原稿 | 改稿报告：命中、建议改法、未核实条目 |
| `revise` 改稿 | 「改稿」「精简」「去 AI 味」「按我的意见改」 | 先备份到新时间戳目录，再改，写回原文件 | 改后稿 + 改稿报告（对话里给要点） |
| `embed` 嵌入 | 被 topmind-wechat-post / topmind-x-article 调用 | 步骤、备份、报告和 revise 完全一样；只有对话里的交付更短 | 终稿 + 三行摘要（字数前后、未核实条数、保留的提示）；完整报告照样落盘 |
| `quick` 快审 | 标题、短文、段子、回复、摘要 | 一次通读 + 脚本，给一个改后版本，最多附 2 个候选 | 文本 + 一行理由 |

**revise 和 embed 的边界**：用户直接说「改稿」就是 revise，哪怕稿子是长文技能写的；长文技能在写作流程里自动调用才是 embed。两者都先备份、都落盘完整报告，embed 的报告头写「模式：embed（调用方：xx）」。用户看了三行摘要想要细节时，打开 `out/改稿报告.md` 即可，不用换模式重跑。

## 参数（调用方或用户可以给）

| 参数 | 取值 | 默认 |
|---|---|---|
| `genre` 文体 | long / short / duanzi / reply / title / summary / release | 按文件和长度推断：`.md` 或超过约 1000 字当 long |
| `reader` 读者 | 大众 / 有背景 / 专业 | 有背景（懂基础概念） |
| `heat` 时机 | 首发热点 / 真里程碑 / 后续迭代 / 热度一般 | 不确定时问作者（决定强势还是诚恳，见 `core-voice.md` V20） |
| `notes` 作者意见 | 作者的修改意见原话 | 无；有就优先，作者改过的说法就是标准答案 |
| `sources` 素材来源 | 私有 `素材来源.md` 的路径 | 稿子同目录下自动找 |
| `source_draft` 源稿 | 改写前的源稿路径 | 无；有就加跑段落级保真审计 |
| `depth` 结构改动深度 | light / structure | light：⓪ 只诊断，外加低风险的结构改动（并列段转列表、对照转表格、删重复段）；structure：允许重排小节、合并拆分章节、按骨架重组 |

## 工作流

0. **声明与备份**：先说「技能 topmind-revise · 模式 · 文体」；revise / embed 模式把稿子和配图复制到新的带时间戳目录（不覆盖旧备份）：长文文章文件夹固定放 `<文章文件夹>/raw/备份-YYYYMMDD-HHMMSS/`，单个短文件放同目录的 `备份-YYYYMMDD-HHMMSS-<稿名>/`。再跑 `python3 scripts/count_words.py 稿子.md` 记改前字数。
1. **⓪ 结构复查**（方法见 `references/information-design.md`）：先不看措辞，回答四个问题——主要信息是什么、在不在开头；每节要点能不能一句话说出；哪些内容的形状适合列表 / 表格 / 图却写成了段落；哪里重复、哪里超出篇幅预算。有 `骨架.md` 就对着它看；先跑 `python3 scripts/info_design_hints.py 稿子.md` 拿 I 提示做线索（只供判断）。结论写进报告「信息设计诊断」。默认 `depth=light`：只做低风险的结构改动（并列段转列表、对照转表格、删重复段），重排章节先列建议交作者；`depth=structure` 时才动章节顺序和拆合。随笔类稿子（type: essay）整篇段落是正常的，不按「段落太多」诊断。
2. **① 事实**（细则见 `references/fact-check.md`）：承重事实（数字、排名、日期、引语、「第一」）逐条对素材来源，上一版的数字全部重核；有一手信源但未完全确认的热点，短文可直陈加「？！」；纯传闻不写；「第一」核实不了就换说法；引语逐字照录、语气不升级；否定结论换一种查法再查一遍。查不到的列进「未核实条目」交给作者，不替作者决定。
3. **② 逻辑**：结论是否靠前；长文结构「过去一句 + 图、现在汇总加分析、未来判断 + 一条支撑事实」；定性准不准；对比有对象、有定语；同一事实全文同值、同一事物一个叫法（写法也统一）；导语、小结和后文对得上，没有以偏概全。

   事实关和逻辑关靠人工判断，改稿报告骨架里有一份「人工检查」清单，逐项勾过再交付。
4. **③ 删冗余**：删不言自明的引导语、复述图的句子、小节过渡句、无效信息、段段小结。直白但啰嗦的句子只删多余部分，不整句推倒。
5. **④ 去 AI 味**：按 `references/de-ai-rules.md` 走，先守改写边界；强信号见一次就改，弱信号叠在一起才改，语境词（H 提示）按 `references/core-voice.md` 的场景判断要不要留。

   ```bash
   python3 scripts/de_ai_lint.py 稿子.md                  # 长文：W 警告 + H 提示
   python3 scripts/lint_x_post.py 短文.txt                # 短文 / 段子 / 回复：再加 X 格式检查
   python3 scripts/lint_x_post.py 段子.txt --duanzi
   ```

6. **⑤ 核心经验对照**：按文体抽查 `references/core-voice.md` 速查表里的条目（标题、开头、收尾、数字、引用、来源行、列表、emoji……）。
7. **⑥ 排版**：长文 Markdown（图紧跟它证明的文字，一段 2–3 句，小标题「序号、阶段：概括」）；短文纯文本；段子一句一行、行间空一行；回复一行。
8. **⑦ 保真审计**：

   ```bash
   python3 scripts/revise_check.py 备份/稿子.md 稿子.md --report 改稿报告.md
   python3 scripts/audit-provenance.py --draft 稿子.md --source 源稿.md   # 有源稿时
   ```

   `revise_check.py` 比对数字、日期、引语、英文专名、确定性词（可能 / 预计 / 已经 / 据传…）的消失和新增；数字、引语的每处变化都要有依据。
9. **⑧ 过度改稿检查**：同一脚本统计「没有任何 W 命中却被改写」的段落占比，超过 30% 提示「可能改过头」，逐段确认或恢复原文。结构复查、事实关、逻辑关和作者意见带来的改动不算过度改稿：在改动表里把依据写成「⓪ 结构」「① 事实」「② 逻辑」「作者意见」，再跑 `revise_check.py 备份/稿子.md 稿子.md --declare out/改稿报告.md`，这些段落会单独列出、不计入比例。
10. **报告**（模板见 `references/report-template.md`）：字数改前 → 改后；信息设计诊断；改动表（骨架已按段落 diff 预填原文 / 改后，补依据）；保留未改的命中（骨架已列出改后稿全部 W 和 H，W 写理由，H 写一句判断，不能写「无」却还有命中）；人工检查清单；未核实条目。

完整流程与完成标准见 `references/revision-workflow.md`。

## 防过度改稿（硬约束）

1. 每处改动对应一条规则编号（Z / P / V）或一句作者意见；说不出来就恢复原文。
2. 没有命中的段落原样保留。
3. 不追求字数一定变短：变短是删冗余的结果，不是目标。
4. 不动：引语原文、专名、术语、讨论某个词本身的句子、作者故意的口语和括号里的自我纠正。
5. 有作者以前的稿子时，句长、用词、标点习惯跟样本走，优先于通用规则。
6. W 警告不要求「清零」，要求每条有结论；H 提示只供判断，不要求改。
7. 结构改动也要说得出依据（写「⓪ 结构」加一句诊断）；默认只做低风险的结构改动，重排章节要 `depth=structure` 或作者同意。转列表、转表格时原句的事实和措辞照搬，不顺手改写。

## 被其他技能调用时

| 调用方 | 默认 | 调用约定 |
|---|---|---|
| topmind-wechat-post | 默认组合：成稿后由本技能执行质量三关 | `mode=embed genre=long sources=<文章目录>/素材来源.md` |
| topmind-x-article | 默认组合：工作流第 0 步 | 同上 |
| topmind-briefs / topmind-viral-posts | 不默认调用；直接按共享的 `core-voice.md` 写，跑 lint | 用户说「改稿 / 过一遍」时：`mode=revise genre=short` 或 `mode=quick genre=duanzi` |
| topmind-format | 不调用；只报告命中、不改字 | 用户要改写时建议转本技能 |
| topmind-cover | 不调用 | 用户要改封面文案时：`mode=quick genre=title` |

- 嵌入模式交回：终稿文本 + 三行摘要；完整报告写到文章目录（例如 `out/改稿报告.md`），改稿报告和素材来源都是作者的私有文件，不进本仓库。
- 本技能单独安装也能用；调用方没装本技能时，按它随包的 `revision-workflow.md` 手动走一遍，效果一致。

## 脚本

| 脚本 | 用途 |
|---|---|
| `scripts/de_ai_lint.py` | 去 AI 味检查：W 警告（强信号）+ H 提示（语境词）；长文 Markdown 另附 I 级信息设计提示；`--genre`、`--json`、`--no-hints`、`--no-design`、`--strict`（I、H 永远不算失败） |
| `scripts/info_design_hints.py` | 信息设计提示 I1–I8（连续纯文字、图表列表少、可转列表 / 表格、重复、首段没交底、长节全是段落、超出 `骨架.md` 篇幅预算）；⓪ 结构复查时先跑，只供判断；`type: essay` 不提示 I1、I2、I7 |
| `scripts/lint_x_post.py` | X 短文 / 段子 / 回复的格式检查（E 级），去 AI 味部分复用 `de_ai_lint.py` |
| `scripts/count_words.py` | 统一口径的字数统计（改前 / 改后、单段最长） |
| `scripts/revise_check.py` | 保真比对（按次数比，不只看有没有）+ 过度改稿检查（`--declare` 排除已登记的事实 / 逻辑 / 作者意见改动）+ 报告骨架（预填改动表和全部剩余命中；长文附改前 / 改后的 I 提示，填进「信息设计诊断」） |
| `scripts/audit-provenance.py` | 有源稿时的双向逐段溯源审计 |
| `scripts/check_article.py` | 长文文章文件夹体检（`<文章名>/<文章名>.md`）：frontmatter、标题一致、图片存在且按出现顺序编号、无容器 / callout / `![[ ]]`；草稿期还没补的占位截图（文件名带「待补 / 占位 / 截图」或登记在素材来源里）只给 W4，定稿时才算错；改稿移动段落或图片后跑一次 |

这些脚本的唯一真源在仓库 `shared/scripts/`，本目录是逐字节副本。

## 风格校准（可选）

作者想让规则更贴近自己的写法时，可以做一轮「对练」：AI 出候选、作者答选择和理由，冲突记下来，下一轮复测，最后用整篇验收。方法见 `references/calibration-drill.md`。校准结果写进作者自己的私有规则文件，不改本仓库的共享规则。

## 示例

改前 / 改后对照（虚构示例）见 `references/examples.md` 和 `examples/`。

## When NOT to use

- 从零写一篇新文章 → `topmind-wechat-post`（公众号长文）、`topmind-x-article`（X 长文）、`topmind-briefs`（短文）、`topmind-viral-posts`（段子）
- 只排版、不改字 → `topmind-format`
- 出 HTML、排版导出 → `topmind-x-article` / `topmind-wechat-post`
- 封面、配图、长图 → `topmind-cover` / `topmind-poster`
- 只改一两个错别字 → 直接改
- 发布 → 本技能只改稿，不代发

## 外部依赖

无。规则文件和脚本都随包自带，只用 Python 标准库。
