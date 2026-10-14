---
name: topmind-briefs
description: "干货短文：一件事讲透，X + 公众号双平台。短文不是长文——默认不出 HTML：X 版是一段可直接复制的纯文本（首行给结论、合理分段换行、emoji 项目符号列表，emoji 只用 TopMind 体系，带来源链接，0–2 个话题标签），公众号版是 300–800 字 Markdown；交付遵守 X 交付规约：正文单独成块可直接复制（含来源行与话题标签），信源、原图（1–2 张）、说明各自分块；分点必须用 emoji 列表符号；没有原图时主动询问是否配图，不擅自生图。尊重原始信息、原图、原文。只交付不代发。Use when 写短文、公众号短文、X 短文、发快讯、简讯、速报、数据榜单、榜单速报、论文解读、新品速递、来篇短的、短平快、brief；信息密度型（数据、榜单、发布）走本技能。Do NOT use for 把现成文字格式化、转段子、排版（→ topmind-format）、X 长文与发 X 文章（→ topmind-x-article）、公众号长文与公众号排版 HTML（→ topmind-wechat-post）、引流互动型短帖、段子、涨粉帖、互关帖、爆款短篇（→ topmind-viral-posts）、单独出长图/海报/信息图 PNG（→ topmind-poster）、封面与头图（→ topmind-cover）、把稿子发出去（→ topmind-x，须用户确认）。"
license: MIT
metadata:
  version: "0.2.17"
  action_category: "write"
  triggers: "写短文, 公众号短文, X 短文, 发快讯, 快讯, 简讯, 速报, 干货短文, 论文解读, 数据榜单, 榜单速报, 新品速递, brief, 来篇短的, 短平快, 发个快讯"
  author: "TopMindSpace"
  homepage: "https://github.com/topmindspace/topmind-writing-skills#readme"
  updated: "2026-10-14"
---

# topmind-briefs · 干货短文（X + 公众号）

一件事，一段话，讲完就停。短文不是长文：**默认不出 HTML、不做排版包**，交付的是可以直接复制粘贴的文字。

> **必读必守**：[references/x-delivery-contract.md](references/x-delivery-contract.md)——分点必须用 emoji 列表符号（禁用 `- ` `1. `）；X 正文单独一个 `text` 块、只放可发布内容；信源、原图、说明各自分块。

- 跟 `topmind-viral-posts` 的区别：那是引流互动型段子（第一人称、钩子、涨粉）；这是**信息密度型干货短文**（数据、榜单、论文、新品，第三方客观口吻）。
- 跟 `topmind-x-article` / `topmind-wechat-post` 的区别：那两个是长文（数千字、多节多图、HTML 发布包）；本技能 X 版一帖或 ≤3 条 thread，公众号版 300–800 字。
- 现成文字只要排版 → `topmind-format`。

## 何时不用

- 把现成文字格式化、转段子、加空行和 emoji → `topmind-format`
- X 长文（数千字深度稿）、发 X 文章 → `topmind-x-article`
- 公众号长文、公众号排版 HTML → `topmind-wechat-post`
- 引流互动型短帖（第一人称、段子、钩子、涨粉、互关）→ `topmind-viral-posts`
- 单独出长图、海报、信息图 PNG → `topmind-poster`；只要封面、头图 → `topmind-cover`
- 把稿子发到 X → `topmind-x`（发帖连接器，须用户确认后才发）

## 语言铁律

- **默认中文**：标题、正文、配图说明一律用中文，不需要用户每次声明。
- **英文是例外**：只有用户**明确说**「写英文」时才用英文。消息里夹英文词、给英文素材、引用英文原文，都不算要求写英文。
- 引用英文一手素材（论文标题、官方公告、图表原文）时保留原文，必要时在旁给中文翻译。

## 尊重原始信息（铁律）

1. **原始信息**：事实、数字、时间以一手来源为准（官方公告、更新日志、论文、原帖、财报）；二手报道至少找 2 个独立来源交叉确认，无法核实的承重事实删掉。
2. **原文**：引用原话时逐字照录并加「」，写明出处；不把转述写成引语，不改原文数字的单位和口径。
3. **原图**：配图用官方截图 > 官方基准图 > 第三方榜单实拍 > 论文原图，保留原图不裁掉关键信息，不用 AI 图冒充原图。
4. **口径标注**：厂商数字标「（厂商口径）」，未证实消息标「（传言）」，自己的判断标「（推测）」或写成「现在看起来…」，与事实分开写。
5. **不洗稿**：观点可以撞，表达必须原创；不照搬聚合站或别人帖子的行文。

## 工作流

1. **定主题**：一篇只讲一件事——一个数据、一个榜单变化、一篇论文的核心结论、一个新品的关键参数。定不下来就问：这篇让读者记住哪一个数字或结论？
2. **找素材**：先核实，再找图。记下每条信息的**来源名称、链接、发布时间**（交付时要报给用户）。
3. **写 X 版**：一段纯文本，按 [references/platform-specs.md](references/platform-specs.md)、[references/style-guide.md](references/style-guide.md) 和参考帖版式规律 [references/x-layout-patterns.md](references/x-layout-patterns.md)：
   - 标题一行，写出「是什么 + 最扎眼的事实」（只看首行也拿到信息），行首可放 1 个与关键词对应的 emoji（发布 🆕、数据 📊、论文 📄 …）；
   - 正文一段 1–3 行，段与段空一行；并列信息用 emoji 列表（默认 🔹，步骤 1️⃣，对比 ✅/❌），一帖一套；列表前一行写「xx：」引导语，列表后一句收尾；
   - 中英混排：英文专名保留原文，中英之间加半角空格；链接单独一行写明用途；
   - 信息量大（约 500 字以上、账号支持长帖）时用【小标题】分节，不用 `#`；
   - 正文后单独一行 `来源：名称 URL`，最后一行 0–2 个话题标签；
   - emoji 只用 TopMind 体系，唯一出处 [references/emoji-system.md](references/emoji-system.md)：标题 emoji 按关键词对照表取（对不上就不放，不用 🔥 😍 凑数），人设点缀（🐔 🐱 🌱）最多 2 个、只放首尾，严肃资讯不放；
   - 不用 Markdown（X 不渲染），规则见 [references/x-post-format.md](references/x-post-format.md)。
4. **写公众号版**（用户要双平台时）：300–800 字 Markdown，内容与 X 版一致，只允许排版差异；不写前言导读。
5. **配图**：原图优先，交付 1–2 张（官方图、原帖配图 / 原帖截图、基准图、榜单实拍），每张写一句图注说明它证明什么；给可直接打开的图片地址，能下载就下载到交付目录。**没有可用原图时，必须主动问用户「要不要配图？可以用 topmind-cover 出一张 16:9 封面」**，用户说要再调用 `topmind-cover` 的「X 短文封面」（16:9，1200×675）；不擅自生图。
6. **自检**：
   - 每个数字都有来源；图和文字说的是同一件事；推测已标注；
   - 按 [references/writing-principles.md](references/writing-principles.md)「去 AI 味清单」过一遍；
   - `python3 scripts/lint_x_post.py X短文.txt`：错误清零（含 Markdown 列表/标题/加粗/引用/链接/删除线/代码围栏残留），W8（表情过多）/ W9（AI 套话）/ W10（缺来源）逐条处理；
   - 需要统一排版时可跑 `python3 scripts/format_text.py X短文.txt --mode short --out X短文.txt`（只动排版不改字）。
7. **交付**（只交付，不发布）：见下节「交付格式」；落盘时 `X短文.txt` 只放正文，信源 / 配图 / 说明写进 `交付说明.md`。

## 交付格式

默认交付纯文本，不生成 HTML，严格按 [references/x-delivery-contract.md](references/x-delivery-contract.md)（含正反例）：

1. **X 正文块**：一个 `text` 代码块，只放可发布内容——标题、正文、emoji 列表、`来源：名称 URL` 行、末行话题标签。thread 每条一块。
2. **公众号版**（用户要时）：单独一个 `markdown` 块。
3. **信源**：`来源名称｜发布时间（注明时区）｜URL`，每条承重事实一行；发布时间取原文页面，没有就写「未标注」。
4. **原图**：1–2 张，`[图1] 图片地址或文件名 — 图注；来源`；视频给封面帧地址并注明。没有原图写「未找到原图」，最后问：「要不要配图？可以用 topmind-cover 出一张 16:9 封面。」
5. **说明**（可选）：口径提醒、改动说明，放最后。

**HTML 只在用户明确要求时出**（例如「出个一键复制 HTML」「公众号要排版好的版本」）：
`python3 scripts/md2x-html.py X短文.md --out X短文.html --images-from 公众号短文.md`、
`python3 scripts/md2wechat.py --input 公众号短文.md --out-dir <交付目录> --slug <短名> --embed-images --no-toc`。
两个脚本的唯一真源在仓库 `shared/scripts/`，本目录是逐字节副本；`[图N]` 顺序由脚本校验，禁止手工拼 `--images`。
需要完整公众号排版包时转 `topmind-wechat-post`。

## X 版示例

```text
📊 SWE-bench Verified 榜单 10 月 13 日更新，第一名换人了

🔹 模型 A：78.2%
🔹 模型 B：76.9%
🔹 模型 C：74.5%

前三名差距不到 4 个百分点，成本差距见图 1。

来源：SWE-bench 官方榜单 https://www.swebench.com

#SWEbench #AI编程
```

（示例中的模型名与分数为虚构演示。更多示例见 [references/examples.md](references/examples.md)。）

## 话题标签

X 版末尾给 0–2 个话题标签（属正文；备选标签写在正文块外），单独成行放在最后：榜单、发布类取榜单名或产品通用名，再加 1 个领域词；
不堆砌，不蹭无关热点，不用诱导互动或敏感标签；中文帖用中文话题，英文帖用英文驼峰。公众号稿不加话题标签。细则见 `references/platform-specs.md`。

## 内容类型（四种）

| 类型 | 适用 | 结构 |
|------|------|------|
| 数据榜单型 | 基准评测、成本对比 | 判断句开头 → 基准一句 → 最扎眼数字 → 核心图（解决率 / 成本） |
| 榜单速报型 | 排行榜更新、排名变动 | 排名 + 分数 → 性价比 → 细分展开 → 纵向对比 → 榜单实拍 |
| 论文解读型 | 新论文、新方法 | 判断句开头 → 核心方法一句 + 3 条 emoji 要点 → 论文原图 |
| 机制讲解型 | 技术原理、流程拆解 | 痛点一句 → 1️⃣2️⃣3️⃣ 分步 → 「简单来说」一句 → 流程图 |

## 和其他技能怎么配合

| 场景 | 组合 |
|---|---|
| 写完再统一排版 | 本技能 → `topmind-format` 短文体（只排版不改字） |
| 没有原图、用户同意配图 | 本技能 → `topmind-cover`「X 短文封面」 |
| 内容太多、写成长文 | 转 `topmind-x-article`（X 长文）或 `topmind-wechat-post`（公众号长文） |
| 要一张数据长图 | 本技能出文案 → `topmind-poster` 出图 |
| 同一事件出段子 | 本技能出干货版，`topmind-viral-posts` 出引流版，事实与来源保持一致 |

## 运营铁律

- 只起草，不代发。发布前用户确认。
- 数字必须有来源；厂商数字标「厂商口径」。
- 不碰医疗建议、投资建议、政治站队。

## 发文铁律

精炼客观 + 素材优先 + 研究深度，见 [references/writing-principles.md](references/writing-principles.md)。触发本技能时默认执行。
