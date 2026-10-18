---
name: topmind-briefs
description: "干货短文：一件事讲透，X + 公众号双平台。短文不是长文——默认不出 HTML：工作流按「核实一手信源 → 找原帖原图 → 写内容 → 排版」；X 版交付一段可直接复制的纯文本（首行一句话题陈述、合理分段与列表、去 AI 味、emoji 可选且只用 TopMind 体系、末行默认 2 个话题标签），链接（含来源）、原图（1–2 张）、配图另发，绝不混进正文；公众号版是 300–800 字 Markdown；没有原图时主动询问是否配图，不擅自生图。尊重原始信息、原图、原文。只交付不代发。Use when 写短文、公众号短文、X 短文、发快讯、简讯、速报、数据榜单、榜单速报、论文解读、新品速递、来篇短的、短平快、brief；信息密度型（数据、榜单、发布）走本技能。Do NOT use for 把现成文字格式化、转段子、排版（→ topmind-format）、X 长文与发 X 文章（→ topmind-x-article）、公众号长文与公众号排版 HTML（→ topmind-wechat-post）、引流互动型短帖、段子、涨粉帖、互关帖、爆款短篇（→ topmind-viral-posts）、单独出长图/海报/信息图 PNG（→ topmind-poster）、封面与头图（→ topmind-cover）、单独改稿、去 AI 味与质检（→ topmind-revise）、把稿子发出去（→ topmind-x，须用户确认）。"
license: MIT
metadata:
  version: "0.2.24"
  action_category: "write"
  triggers: "写短文, 公众号短文, X 短文, 发快讯, 快讯, 简讯, 速报, 干货短文, 论文解读, 数据榜单, 榜单速报, 新品速递, brief, 来篇短的, 短平快, 发个快讯"
  author: "TopMindSpace"
  homepage: "https://github.com/topmindspace/topmind-writing-skills#readme"
  updated: "2026-10-18"
---

# topmind-briefs · 干货短文（X + 公众号）

一件事，一段话，讲完就停。短文不是长文：**默认不出 HTML、不做排版包**，交付的是可以直接复制粘贴的文字。

> **必读必守**：[references/x-delivery-contract.md](references/x-delivery-contract.md)——X 正文是一段可直接复制的纯文本，**不含 URL 和来源行**；链接一条、图片一条另发。分点默认「·」，行多用「1）」，短列表才用 emoji，禁用 `- ` `1. `；emoji 不强制。
> **写法规则**：[references/core-voice.md](references/core-voice.md) 的短文条目（V01 V05 V08–V13 V16 V20–V22 V24–V28 V32）；去 AI 味按 [references/de-ai-rules.md](references/de-ai-rules.md)。

- 跟 `topmind-viral-posts` 的区别：那是引流互动型段子（第一人称、钩子、涨粉）；这是**信息密度型干货短文**（数据、榜单、论文、新品，第三方客观口吻）。
- 跟 `topmind-x-article` / `topmind-wechat-post` 的区别：那两个是长文（数千字、多节多图、HTML 发布包）；本技能 X 版是一条纯文本短文（约 1000 字内），公众号版 300–800 字。
- 现成文字只要排版 → `topmind-format`。

## 先读：写作原则与信息设计

本技能建立在两份共享文件上，动笔前先读：

- [references/social-writing-principles.md](references/social-writing-principles.md)：8 条社交媒体写作原则（先想清楚、结论先行、每句都有新信息、形式跟内容走、简单清楚、原图优先、站在读者那边、真实有分寸）
- [references/information-design.md](references/information-design.md)：内容 → 形式决策表、篇幅和密度、去啰嗦的判断法
- 措辞和口吻在这两层之上，见 [references/core-voice.md](references/core-voice.md)

短文：首行给结论；3 个以上要点用「·」分行；原图另发，正文不复述图。

## 何时不用

- 把现成文字格式化、转段子、加空行和 emoji → `topmind-format`
- X 长文（数千字深度稿）、发 X 文章 → `topmind-x-article`
- 公众号长文、公众号排版 HTML → `topmind-wechat-post`
- 引流互动型短帖（第一人称、段子、钩子、涨粉、互关）→ `topmind-viral-posts`
- 单独出长图、海报、信息图 PNG → `topmind-poster`；只要封面、头图 → `topmind-cover`
- 单独改一篇现成稿子、去 AI 味、质检 → `topmind-revise`
- 把稿子发到 X → `topmind-x`（发帖连接器，须用户确认后才发）

## 语言铁律

- **默认中文**：标题、正文、配图说明一律用中文，不需要用户每次声明。
- **英文是例外**：只有用户**明确说**「写英文」时才用英文。消息里夹英文词、给英文素材、引用英文原文，都不算要求写英文。
- 官方产品名、论文标题保留英文；引语正文写「人名：中文意思」，英文原文记进素材来源，不在正文里原文加括注（core-voice V13）。

## 尊重原始信息（铁律）

1. **原始信息**：事实、数字、时间以一手来源为准（官方公告、更新日志、论文、原帖、财报）；二手报道至少找 2 个独立来源交叉确认，无法核实的承重事实删掉。
2. **原文**：引用原话时逐字照录并加「」，写明出处；不把转述写成引语，不改原文数字的单位和口径。
3. **原图**：配图用官方截图 > 官方基准图 > 第三方榜单实拍 > 论文原图，保留原图不裁掉关键信息，不用 AI 图冒充原图。
4. **口径标注**：厂商数字标「（厂商口径）」；有一手信源但还没完全确认的热点，短文直陈并在首行用一次「？！」，不写泛泛的「据报道」，纯传闻不写（core-voice V22）；自己的判断写成「预计」「大概率」「现在看起来…」，与事实分开写，不用「我认为」。
5. **不洗稿**：观点可以撞，表达必须原创；不照搬聚合站或别人帖子的行文。

## 工作流

顺序固定：**信源 → 原帖原图 → 内容 → 排版**，前一步没做完不进下一步（见交付规约第一节）。

1. **核实信源**：一篇只讲一件事（一个数据、一个榜单变化、一篇论文的核心结论、一个新品的关键参数）。先找一手来源（官方公告、更新日志、论文、仓库、当事人原帖）；厂商数字标「官方称 / 厂商口径」，传言标「据传 / 未证实」。记下每条的**来源名称、发布时间（时区）、URL**——这些另发给用户，不进正文。
2. **找原帖、原图**（写字之前，按 [references/image-sourcing.md](references/image-sourcing.md)）：原帖链接、官方图 / 截图 1–2 张，来源记进交付说明；自制图只作兜底，标「自制」和数据来源。
3. **写内容**：
   - 首行一句简单的话题陈述：「是什么 + 最关键的事实」，约 30 字内，只看首行也拿到信息；不用设问钩子，真里程碑把「第一」放句首（core-voice V05、V20）；
   - 具体数字和场景，说人话，事实讲完就停，不硬加收尾句，也不用「你会换吗？」拉互动（V10）；对比给出对象和定语，比的对象选读者认识的知名对手，不写「约 / 左右」，不用千分位（V12）；
   - 读者不关心的背景删掉，借来的热点一句带过；推测写成问句，不写成事实（V22）；不写「理由就一条：」这类总结腔，直接说理由（V08）；
   - **去 AI 味（必过）**：按 [references/de-ai-rules.md](references/de-ai-rules.md) 逐条过（先守改写边界：只改表达，不改事实和确定性），再对照 [references/core-voice.md](references/core-voice.md) 短文条目和 [references/writing-principles.md](references/writing-principles.md) 第五点五节「吸引力清单」；
   - 出处在正文里只用文字点到（「官方称」「据论文」），不贴 URL、不写来源行。
4. **排版**（目标：方便阅读），按 [references/platform-specs.md](references/platform-specs.md)、[references/x-post-format.md](references/x-post-format.md)、[references/x-layout-patterns.md](references/x-layout-patterns.md)：
   - 一段 1–3 行，段间空一行；3–7 条并列信息才用列表，前一行写「xx：」引导语，2 条就写成两句；
   - 分点默认「·」，行多或有顺序用「1）」，短列表（3–4 条）才用 emoji（🔹 / 1️⃣ / ✅❌），较长短文用【小标题】分节；禁用 `- ` `* ` `1. `（V25）；
   - emoji **不强制**；要用就只用 TopMind 体系（[references/emoji-system.md](references/emoji-system.md)）：标题 emoji 0–1 个且对上关键词，人设点缀 0–2 个只放首尾，严肃资讯不放；
   - 中英混排：英文专名保留原文，中英之间加半角空格；
   - 最后一行默认 2 个话题标签（宽泛词 + 主题词，V27）；不用 Markdown（X 不渲染）。
4. **写公众号版**（用户要双平台时）：300–800 字 Markdown，内容与 X 版一致，只允许排版差异；不写前言导读。
5. **配图**：原图优先，交付 1–2 张（官方图、原帖配图 / 原帖截图、基准图、榜单实拍），每张写一句图注说明它证明什么；给可直接打开的图片地址，能下载就下载到交付目录。**没有可用原图时，必须主动问用户「要不要配图？可以用 topmind-cover 出一张 16:9 封面」**，用户说要再调用 `topmind-cover` 的「X 短文封面」（16:9，1200×675）；不擅自生图。
6. **自检**：
   - 每个数字都能在另发的链接里找到出处；图和文字说的是同一件事；推测已标注；
   - `python3 scripts/lint_x_post.py X短文.txt`：E 错误清零（Markdown 残留，以及 E10 正文有 URL、E11 有来源行、E12 有配图说明）；W 警告每条要有结论（改掉，或在说明里写保留理由）；H 提示只供判断，不要求改；公众号版跑 `python3 scripts/de_ai_lint.py 公众号短文.md`；
   - 需要统一排版时可跑 `python3 scripts/format_text.py X短文.txt --mode short --out X短文.txt`（只动排版不改字；正文里的链接、来源行会被拿出来另列）。
   - 用户要求改稿时，转 `topmind-revise`（`mode=revise genre=short`）；没装时按 [references/revision-workflow.md](references/revision-workflow.md) 手动走：备份 → 事实 → 逻辑 → 删冗余 → 去 AI 味 → 核心经验对照 → 排版 → 保真审计，报改前 / 改后字数（`python3 scripts/count_words.py`）。
7. **交付**（只交付，不发布）：见下节「交付格式」；落盘时 `X短文.txt` 只放正文，链接 / 图片 / 说明写进 `交付说明.md`。

## 交付格式

默认交付纯文本，不生成 HTML，严格按 [references/x-delivery-contract.md](references/x-delivery-contract.md)（含正反例）：

1. **正文**（一条消息或一个独立 `text` 块）：一段可直接复制的纯文本——标题行、正文、列表、末行话题标签；**不含 URL、来源行、配图说明**。thread 每条一块。
2. **链接**（单独一条）：`来源名称｜发布时间（注明时区）｜URL`，每条承重事实一行，原帖链接也放这里；发布时间取原文页面，没有就写「未标注」。
3. **图片**（单独一条）：1–2 张，`[图1] 图片地址或文件名 — 图注；来源`；视频给封面帧地址并注明。没有原图写「未找到原图」，并问：「要不要配图？可以用 topmind-cover 出一张 16:9 封面。」
4. **公众号版**（用户要时）：单独一个 `markdown` 块，可以有文内链接。
5. **说明**（可选）：口径提醒、改动说明，放最后。

**HTML 只在用户明确要求时出**（例如「出个一键复制 HTML」「公众号要排版好的版本」）：
`python3 scripts/md2x-html.py X短文.md --out X短文.html --images-from 公众号短文.md`、
`python3 scripts/md2wechat.py --input 公众号短文.md --out-dir <交付目录> --slug <短名> --embed-images --no-toc`。
两个脚本的唯一真源在仓库 `shared/scripts/`，本目录是逐字节副本；`[图N]` 顺序由脚本校验，禁止手工拼 `--images`。
需要完整公众号排版包时转 `topmind-wechat-post`。

## X 版示例

```text
SWE-bench 榜单换了第一：领先只有 1.3 分

10 月 13 日更新后的前三名：

1）模型 A：78.2%
2）模型 B：76.9%
3）模型 C：74.5%

#AI #SWEbench
```

链接（另发）：`ToyBench 官方榜单｜2026-10-13（UTC）｜https://example.com/toybench`
图片（另发）：`[图1] 榜单截图 — 前三名分数；来源：官方榜单`

（示例中的模型名与分数为虚构演示；事实讲完就停，不加收尾句。更多示例见 [references/examples.md](references/examples.md)。）

## 话题标签

X 版末尾默认给 2 个话题标签（属正文，是正文最后一行；备选标签写在说明里）：一个宽泛词（如 #AI）+ 一个主题词（榜单名、产品通用名或领域词）；
不堆砌，不蹭无关热点，不用诱导互动或敏感标签；中文帖用中文话题，英文帖用英文驼峰。公众号稿不加话题标签。细则见 `references/platform-specs.md`。

## 内容类型（四种）

| 类型 | 适用 | 结构 |
|------|------|------|
| 数据榜单型 | 基准评测、成本对比 | 判断句开头 → 基准一句 → 最扎眼数字 → 核心图（解决率 / 成本） |
| 榜单速报型 | 排行榜更新、排名变动 | 排名 + 分数 → 性价比 → 细分展开 → 纵向对比 → 榜单实拍 |
| 论文解读型 | 新论文、新方法 | 判断句开头 → 核心方法一句 + 3 条要点 → 论文原图（另发） |
| 机制讲解型 | 技术原理、流程拆解 | 痛点一句 → 1）2）3）分步 → 流程图（另发） |

## 和其他技能怎么配合

| 场景 | 组合 |
|---|---|
| 写完再统一排版 | 本技能 → `topmind-format` 短文体（只排版不改字） |
| 用户要改稿、过一遍质检 | 本技能 → `topmind-revise`（`mode=revise genre=short`） |
| 没有原图、用户同意配图 | 本技能 → `topmind-cover`「X 短文封面」 |
| 内容太多、写成长文 | 转 `topmind-x-article`（X 长文）或 `topmind-wechat-post`（公众号长文） |
| 要一张数据长图 | 本技能出文案 → `topmind-poster` 出图 |
| 同一事件出段子 | 本技能出干货版，`topmind-viral-posts` 出引流版，事实与来源保持一致 |

## 运营铁律

- 只起草，不代发。发布前用户确认。
- 数字必须有一手来源（链接另发）；厂商数字标「官方称 / 厂商口径」。
- 不碰医疗建议、投资建议、政治站队。

## 发文铁律

精炼客观 + 素材优先 + 研究深度，见 [references/writing-principles.md](references/writing-principles.md)。触发本技能时默认执行。
