# topmind-writing-skills

[English](./README.en.md) | 中文

[![Release](https://img.shields.io/github/v/release/topmindspace/topmind-writing-skills?style=flat-square&color=blue)](https://github.com/topmindspace/topmind-writing-skills/releases)
[![npm](https://img.shields.io/npm/v/@topmindspace/topmind-writing-skills?style=flat-square)](https://www.npmjs.com/package/@topmindspace/topmind-writing-skills)
[![CI](https://img.shields.io/github/actions/workflow/status/topmindspace/topmind-writing-skills/ci.yml?style=flat-square&label=CI)](https://github.com/topmindspace/topmind-writing-skills/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)

**TopMindSpace 写作技能合集** —— 公众号文章、X 长文、干货短文、引流段子、封面配图、长图出图：六个技能，一个仓库。

<p align="center">
  <img src="docs/assets/writing-cover.png" alt="topmind-writing-skills · 写作技能合集" width="960" />
</p>

> 正式商务演示技能已独立出去：[`topmind-presentation`](https://github.com/topmindspace/topmind-presentation)（仓库 `topmind-presentation`，仓库即技能，clone 后复制根目录到技能目录即可）。

### topmind-wechat-post · 公众号创作

公众号文章全生命周期：交付包、审校改写、质量三关（事实 / 逻辑 / 去 AI 味）、微信内联排版（图片必内嵌）、发布清单与状态同步。脚本纯 Python 标准库，零依赖。

```bash
npx @topmindspace/topmind-writing-skills install topmind-wechat-post
```

### topmind-x-article · X 长文一键发布

Markdown 原稿 → 一键复制 HTML（富文本，配图内嵌）/ 纯文本兜底（`md2x.py`：图片→`[图N]`、表格→"项：值"列表、列表→emoji 项目符号，因为 X 纯文本不渲染 Markdown 列表）+ 封面图 + 发布清单。发布走人工粘贴，发布后抓回核对。

```bash
npx @topmindspace/topmind-writing-skills install topmind-x-article
```

### topmind-briefs · 干货短文

公众号 + X 双平台干货短文：一件事讲透（数据榜单 / 论文解读 / 新品速递 / 机制讲解）。短文不是长文，**默认不出 HTML**：X 版是一段可直接复制的纯文本（分段换行、克制的 emoji、来源链接、0–2 个话题标签），公众号版约 300–800 字 Markdown。尊重原始信息、原图、原文；按 X 交付规约交付：正文单独一块可直接复制，信源（含发布时间）、1–2 张原图、说明各自另列；没有原图时主动询问是否配图（可选 topmind-cover），不擅自生图。只起草不代发。

```bash
npx @topmindspace/topmind-writing-skills install topmind-briefs
```

### topmind-viral-posts · X 引流段子/爆款短篇

基于对 X 中文区常见高互动写法的归纳，提供 18 类型模板 + 钩子×主体×收尾组合玩法（示例均为自编），默认**段子体**（一句一行、行与行之间空一行）、口语化、带互动钩子，配图原图优先（官方 / 第三方 / 自己的后台截图），没有原图时先问是否配图、同意后走 topmind-cover 出图，话题标签（1–3 个）在正文末行，内部分类标签另列；段子**完全不用 emoji**，分点不加符号、一条一行靠行间空行区分；每条正文单独一块。

```bash
npx @topmindspace/topmind-writing-skills install topmind-viral-posts
```

> 18 类型：干货忠告 / 互关求粉 / 自嘲幽默 / 互动提问 / 打卡日常 / 新人报到 / **热点资讯**（基于真实检索，配官方原图可多图）/ 暴论 / 数据晒单 / 真诚交友 / 吐槽共鸣 / 干货技巧 / 经验忠告 / 执行清单 / **冷知识揭秘** / **差额冲刺** / **反差对照** / **自问自答**。

### topmind-format · X 纯文本格式化

用户贴一段现成文字：**转段子** → 每句一行、行间空一行，去掉所有 emoji 与列表符号；**格式化成短文** → 合理分段换行、列表改 emoji、标题 emoji 对应关键词、开头结尾加鸡/猫/植物人设点缀（🐔 🐱 🌱 🌸）。只动排版不改字，`format_text.py` 自带原文保真校验。

```bash
npx @topmindspace/topmind-writing-skills install topmind-format
```

### X 文本统一规约（所有产出 X 纯文本的技能共用）

共享文档在 `shared/references/`，经 manifest 分发到各技能 `references/`：

| 文档 | 管什么 |
|---|---|
| `x-delivery-contract.md`（必读必守） | 短文分点必须用 emoji 列表符号，段子完全不用 emoji（分点不加符号），都禁用 `- ` `1. `；正文单独一个可直接复制的块（含来源行与话题标签），信源、原图、配图建议、内部标签、说明各自另列；多条帖子每条一块 |
| `x-post-format.md` | 不用 Markdown、列表符号、留白、来源、骨架、配图、公众号稿→X 稿 |
| `emoji-system.md` | TopMind emoji 体系唯一出处（只用于短文体）：人设点缀 🐔 🐱 🌱 0–2 个只放首尾；标题 emoji 0–1 个对上关键词；列表符号一帖一套 |
| `x-layout-patterns.md` | 参考帖拆出的版式规律（首行给结论、列表引导语、【小标题】分节等） |

检查：`lint_x_post.py`（E1–E9 Markdown 残留；W12 正文混入信源 / 配图 / 说明 / 内部标签；`--duanzi` 时 W13 段子里出现 emoji）。

### topmind-cover · 封面配图生成

X 长文与公众号共用的封面图：震撼、醒目、主题突出。**选风格 → 看示例 → 按配方组 prompt** 三步出图，`crop-cover.py` 一键裁出双平台尺寸（X 1500×600、公众号 900×383），`--preset x-post` 落盘 X 短文封面（1200×675）。22 种风格索引与配方见 [`references/cover-styles.md`](./topmind-cover/references/cover-styles.md)。

```bash
npx @topmindspace/topmind-writing-skills install topmind-cover
```

<p align="center">
  <img src="https://github.com/topmindspace/topmind-writing-skills/raw/main/topmind-cover/assets/examples/overview.png" alt="topmind-cover · 22 封面风格总览" width="960" />
</p>

> 让 idea 飞，好想法被看见。

### topmind-poster · HTML → 高清长图

榜单、信息图、月报长图、海报的**出图环节**：HTML+CSS 排版 → 无头 Chrome 2× 截图 → 自动裁掉底部空白。含「一段一图」分段图批量出图工作流（生成器 + 渲染器），一篇长文拆成 N 张可单独转发的图。`render_poster.py` 一条命令跑完三步；版式配方（画布 / 字号层级 / 浅底深底配色 / 栅格 / 进度条）见 [`references/layout-recipes.md`](./topmind-poster/references/layout-recipes.md)。

```bash
npx @topmindspace/topmind-writing-skills install topmind-poster
```

> 为什么不用生图模型：榜单里有大量必须逐字正确的文本和数字，生图会改字、糊字、编造数字。封面是例外（无密集文本），走 `topmind-cover`。

> **改名说明**：本仓由 `tms-skills` 改名为 `topmind-writing-skills`，
> npm 包为 `@topmindspace/topmind-writing-skills`，旧包不再更新。
> 也不要安装旧包的 `^2`（2.0.0–2.1.1 已弃用）。

## 技能一览

| 技能 | 版本 | 做什么 |
|------|------|--------|
| [`topmind-wechat-post`](./topmind-wechat-post/) | **0.3.10** | 公众号文章全生命周期：交付包、审校改写、质量三关、微信内联排版与发布清单 |
| [`topmind-x-article`](./topmind-x-article/) | **0.4.16** | X 长文一键发布：Markdown 原稿 → 一键复制 HTML（含配图/提示词复制、图片点击放大）/ 纯文本兜底 + 封面图 + 发布清单 |
| [`topmind-cover`](./topmind-cover/) | **0.4.8** | 文章封面配图（X / 公众号共用，X 主尺寸 1500×600 / 5:2）：震撼醒目主题突出；22 种封面风格库 + X 短文 16:9 封面场景 + 12 种标题花式 + 55 张示例图（22 种风格 × 2 尺寸 + 11 张变体样张） + 1 张风格总览图 |
| [`topmind-briefs`](./topmind-briefs/) | **0.2.18** | 干货短文（公众号 + X 双平台）：一件事讲透，数据榜单/论文解读/新品速递；X 版一段纯文本（默认不出 HTML）+ emoji 列表 + 来源链接 + 话题标签建议；正文单独成块，信源 / 原图另列，无原图先询问配图 |
| [`topmind-viral-posts`](./topmind-viral-posts/) | **0.3.10** | X 引流段子/爆款短篇：18 大类型模板 + 组合玩法，段子体（行间空行，零 emoji，分点不加符号）、每条正文单独成块、话题标签在正文、分类标签另列；无原图先询问再走 topmind-cover |
| [`topmind-format`](./topmind-format/) | **0.1.3** | X 纯文本格式化：转段子（行间空行，零 emoji）/ 格式化成短文（分段 + emoji 体系），只动排版不改字，带原文保真校验；正文单独成块 |
| [`topmind-poster`](./topmind-poster/) | **0.1.5** | HTML+CSS → 高清长图 / 海报 / 信息图 PNG：无头 Chrome 2× 截图 + 自动裁白；「一段一图」分段图批量出图（生成器 + 渲染器） |

安装器 [`@topmindspace/topmind-writing-skills`](https://www.npmjs.com/package/@topmindspace/topmind-writing-skills) 为 **0.8.35**（整仓同 tag 发版）。

### 怎么选、怎么组合

| 你要做的事 | 用哪个 | 常见组合 |
|---|---|---|
| 一件事的干货短文（数据、榜单、发布） | `topmind-briefs` | → `topmind-format` 统一排版；没有原图 → 先问，同意后 `topmind-cover` 出 16:9 首图 |
| 引流段子、涨粉帖、互关帖 | `topmind-viral-posts` | → `topmind-format` 重排段子体；同一事件可配一条 briefs 干货版 |
| 现成文字只要排版（转段子 / 格式化） | `topmind-format` | 只动排版不改字；要改写内容再转 briefs / viral-posts |
| 数千字 X 长文 | `topmind-x-article` | + `topmind-cover`（5:2 封面）；短于一帖的内容走 briefs |
| 公众号长文与排版 | `topmind-wechat-post` | + `topmind-cover`；300–800 字短文走 briefs |
| 长图、海报、信息图 PNG | `topmind-poster` | 文案先由 briefs / wechat-post 写好 |

> SKILL.md frontmatter 顶层只用 Agent Skills 规范字段（`name` / `description` / `license` / `metadata`），版本、`action_category`、`triggers` 等自定义字段放在 `metadata` 下（字符串值），能通过官方校验器 `skills-ref validate`。
>
> 共享脚本与共享文档（`writing-principles.md`、X 文本规约四件套）的唯一真源在 `shared/`，各技能目录保留逐字节副本（单独安装也能用）；改共享文件只改 `shared/`，再跑 `npm run sync:shared`，CI 用 `--check` 校验。
>
> npm 包不含 cover 的单风格样张（`assets/examples/<style>*.png`），只保留 `overview.png`；完整样张见 GitHub 仓库或 Release zip。

## 安装

**npm = 钉版本快照**；**GitHub = 跟仓库 HEAD**。

```bash
npx @topmindspace/topmind-writing-skills list
npx @topmindspace/topmind-writing-skills install topmind-briefs
npx @topmindspace/topmind-writing-skills install topmind-briefs --to ./.claude/skills
npx @topmindspace/topmind-writing-skills@0.8.4 install topmind-briefs   # 钉版本
npx @topmindspace/topmind-writing-skills uninstall topmind-briefs --to ./.claude/skills
```

```bash
# 跟 HEAD
npx github:topmindspace/topmind-writing-skills install topmind-briefs
```

默认探测：`./.agents` → `./.claude` → `./.cursor` → `./.codex` → `./.mimocode`，再用户级 `~/.claude` 等；也可用 `--to`。未给 `--to` 时安装摘要会明确打印探测到的目标目录。不要 `npm install topmind-briefs`（技能 id 不是独立包）。

`install` 细节：若同名技能已存在，会报出已装版本并拒绝覆盖，需加 `--force` 才替换（或先 `uninstall` 再装）。安装成功后打印三行摘要：装到哪里 / 装的技能版本与安装器版本 / 下一步。

## 仓库结构

```
topmind-writing-skills/
├─ topmind-briefs/               # 技能（SKILL.md + assets + references + scripts）
├─ topmind-viral-posts/          # 技能（X 引流段子/爆款短篇，段子体）
├─ topmind-format/               # 技能（X 纯文本格式化：转段子 / 格式化成短文）
├─ topmind-poster/               # 技能（HTML → 高清长图 / 分段图）
├─ topmind-cover/                # 技能
├─ topmind-wechat-post/          # 技能
├─ topmind-x-article/            # 技能
├─ bin/topmind-writing-skills.js # CLI：list / install / uninstall
├─ shared/                       # 共享脚本与写作原则的唯一真源（manifest.json 声明分发到哪些技能）
├─ evals/                        # 路由评测用例（不进 npm 包）
├─ docs/                         # 发布规范 · CI 说明
├─ scripts/                      # 仓库级门禁 / 隐私扫描
├─ package.json                  # @topmindspace/topmind-writing-skills
└─ LICENSE · CHANGELOG.md · README.md · README.en.md
```

## 发布与 CI

| 动作 | GitHub | npm |
|------|:------:|:---:|
| push main | 立即可见 | **不变** |
| tag `vX.Y.Z` | Release + zip | **自动 publish** |

```bash
npm run check && npm run audit && npm run privacy
```

详见 [docs/PUBLISHING.md](./docs/PUBLISHING.md) · [docs/ci.md](./docs/ci.md)。

## 许可证

MIT © TopMindspace — [LICENSE](./LICENSE)
