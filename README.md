# topmind-writing-skills

[English](./README.en.md) | 中文

[![Release](https://img.shields.io/github/v/release/topmindspace/topmind-writing-skills?style=flat-square&color=blue)](https://github.com/topmindspace/topmind-writing-skills/releases)
[![npm](https://img.shields.io/npm/v/@topmindspace/topmind-writing-skills?style=flat-square)](https://www.npmjs.com/package/@topmindspace/topmind-writing-skills)
[![CI](https://img.shields.io/github/actions/workflow/status/topmindspace/topmind-writing-skills/ci.yml?style=flat-square&label=CI)](https://github.com/topmindspace/topmind-writing-skills/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)

**TopMindSpace 写作技能合集**：公众号文章、X 长文、干货短文、引流段子、排版、改稿质检、封面、长图，八个技能一个仓库。写法上原则优先：先想清楚要传达什么、用什么形式最好读，再谈措辞；脚本只提示，人来判断。

<p align="center">
  <img src="docs/assets/writing-cover.png" alt="topmind-writing-skills · 写作技能合集" width="960" />
</p>

```bash
npx @topmindspace/topmind-writing-skills list
npx @topmindspace/topmind-writing-skills install topmind-briefs
```

## 技能一览

> 术语：**短文** = X 纯文本帖，约 1000 字以内都行（没有 280 字限制）；**长文** = X Article 或公众号长文；**段子** = 一句一行的短文体裁。

| 技能 | 版本 | 做什么 |
|---|---|---|
| [`topmind-wechat-post`](./topmind-wechat-post/) | **0.3.18** | 公众号长文：单源文章文件夹、质量三关（默认组合 revise）、按需出微信内联排版（图片内嵌）、发布清单与状态同步 |
| [`topmind-x-article`](./topmind-x-article/) | **0.4.24** | X 长文：单源 Markdown（默认组合 revise）→ 按需出一键复制 HTML / 纯文本兜底 + 封面 + 发布清单 |
| [`topmind-briefs`](./topmind-briefs/) | **0.2.26** | 干货短文（X + 公众号）：一件事讲完就停；信源 → 原图 → 内容 → 排版；X 版一段可复制纯文本，链接、原图另发 |
| [`topmind-viral-posts`](./topmind-viral-posts/) | **0.3.18** | X 引流段子 / 爆款短篇：18 类模板 + 钩子 × 主体 × 收尾组合，段子体零 emoji |
| [`topmind-format`](./topmind-format/) | **0.1.11** | X 纯文本格式化：转段子 / 格式化成短文，只动排版不改字，带保真校验 |
| [`topmind-revise`](./topmind-revise/) | **0.1.3** | 改稿与质检：⓪ 结构 → 事实 → 逻辑 → 去 AI 味 → 保真审计；四种模式，每处改动对应规则编号 |
| [`topmind-cover`](./topmind-cover/) | **0.4.15** | 封面配图（X 1500×600 / 公众号 900×383）：22 种风格、七层场景配方、整张生成 + 标题核对 |
| [`topmind-poster`](./topmind-poster/) | **0.1.8** | HTML+CSS → 高清长图 / 海报 / 信息图：无头 Chrome 2× 截图 + 自动裁白，「一段一图」批量出图 |

安装器 [`@topmindspace/topmind-writing-skills`](https://www.npmjs.com/package/@topmindspace/topmind-writing-skills) 为 **0.8.47**（整仓同 tag 发版）。

## 写作理念：原则优先

社交媒体内容是为了把信息和观点传达给读者：清楚、简单、好读；能用图、表、列表的不写长段。所有写作技能共用一套分层规则（唯一真源 `shared/references/`，各技能自带副本，单独安装也能用）：

| 层 | 文件 | 管什么 |
|---|---|---|
| 第 0 层 · 写作原则 | `social-writing-principles.md` | 8 条原则：先想清楚传达什么、结论先行、每句给新信息、形式跟着内容走、常用词、原图和数据胜过转述、站在读者那边、真实有分寸 |
| 第 1 层 · 信息设计 | `information-design.md` | 先写骨架、内容 → 形式决策表（列表 / 表格 / 图 / 段落）、篇幅和密度、去啰嗦的判断法、I1–I8 提示的含义 |
| 第 2 层 · 措辞口吻 | `core-voice.md` | 十条措辞原则，V01–V33 是它们在标题、开头、数字、引用、回复、段子里的例子 |
| 第 3 层 · 审稿 | `topmind-revise` + `de-ai-rules.md` | ⓪ 结构 → 事实 → 逻辑 → 删冗余 → 去 AI 味 → 排版 → 保真审计；去 AI 味规则只在成稿后用，写的时候不对着它写 |

几条贯穿全部技能的做法：

- **原则写成「为什么 + 怎么判断 + 例子」**：例子说明怎么想，不是词表；只有平台限制、事实和合规这类硬约束保留硬性写法，并标「硬约束」。
- **人设是还在学习的普通人**：不是专家，不站讲台；可以带一点老司机式的自嘲，不确定就直说。
- **原图优先**（`image-sourcing.md`）：写字前先找官方 / 原帖 / 第三方原图，来源记进 `素材来源.md`；自制图兜底，标「自制」和数据来源。
- **脚本只提示**：E 错误必须清零；W 警告每条给结论；H 提示和 I1–I8 信息设计提示只供判断，永远不进 `--strict`。
- **改稿只动有问题的地方**：先守改写边界（只改表达，不改事实和确定性）；重排章节要 `depth=structure`。

### 长文的文章文件夹

一篇长文一个文件夹，只有一份源稿；`article_scaffold.py`（或 wechat-post 的 `new-article.py`）一条命令建好：

```text
<文章名>/
├─ <文章名>.md    唯一源稿（Obsidian 直接看；HTML 注释里的写作提示不进派生产物）
├─ 骨架.md        动笔前定主要信息、读者、每节要点 / 形式 / 图表计划 / 字数
├─ 素材来源.md    每张图、每个数字的出处
├─ images/  cover/
├─ raw/           原稿、截图、笔记（不发布）
├─ out/           派生产物：X 长文 HTML、纯文本、公众号 HTML（可随时重建）
└─ 参考/          其他环境写的同主题稿件和素材（只作参考，永远不当源稿）
```

多环境协作（可选）：源稿 frontmatter 写 `updated_at`（ISO 8601，带时区）、`updated_env`、`updated_by`，新旧以 `updated_at` 为准；两边都改过又分不清先后时不覆盖，旧的一份存进 `参考/`。详见 `workspace.md`。旧的 `公众号稿.md` 交付包只读兼容。

## 怎么选、怎么组合

| 你要做的事 | 用哪个 | 常见组合 |
|---|---|---|
| 一件事的干货短文（数据、榜单、发布） | `topmind-briefs` | → `topmind-format` 统一排版；没有原图先问，同意后 `topmind-cover` 出 16:9 首图 |
| 引流段子、涨粉帖、互关帖 | `topmind-viral-posts` | → `topmind-format` 重排段子体 |
| 现成文字只要排版 | `topmind-format` | 只动排版不改字；要改内容转 `topmind-revise` |
| 改稿、精简、去 AI 味、质检 | `topmind-revise` | 单独用，或被长文技能写完时调用 |
| 数千字 X 长文 | `topmind-x-article` | + `topmind-revise` + `topmind-cover`（5:2 封面） |
| 公众号长文与排版 | `topmind-wechat-post` | + `topmind-revise` + `topmind-cover`；300–800 字短文走 briefs |
| 长图、海报、信息图 | `topmind-poster` | 文案先由 briefs / wechat-post 写好 |

## 各技能要点

### topmind-wechat-post · 公众号长文

- 单源文章文件夹，审校改写默认组合 `topmind-revise`；排版产物进 `out/`，图片 base64 内嵌，粘贴即带图。
- 手写小标题序号原样保留；脚本纯 Python 标准库，零依赖。

### topmind-x-article · X 长文

- 默认只交付 `<文章名>.md`；要发 X 时派生一键复制 HTML（按 `![]()` 顺序嵌图，「来源：」行成图注）或纯文本兜底（`md2x.py`：图片 → `[图N]`、表格 → 「项：值」、列表 → 「·」「1）」）。
- 发布走人工粘贴，发布后抓回核对。

### topmind-briefs · 干货短文

- 默认不出 HTML：核实一手信源 → 找原帖原图 → 写内容 → 排版。
- X 版一段可复制纯文本（emoji 可选、0–2 个话题标签），链接（含来源和发布时间）、原图另发；公众号版约 300–800 字。只起草不代发。

### topmind-viral-posts · X 引流段子 / 爆款短篇

- 18 类模板（干货忠告、自嘲幽默、热点资讯、冷知识揭秘、反差对照、自问自答等）+ 钩子 × 主体 × 收尾组合，示例全部自编。
- 段子体一句一行、行间空行、完全不用 emoji；话题标签 1–3 个放末行，分类标签另列。

### topmind-format · X 纯文本格式化

- **转段子**：每句一行、行间空一行，去掉 emoji 和列表符号；**格式化成短文**：合理分段，列表改「·」「1）」或 emoji。
- `format_text.py` 只动排版不改字，自带保真校验；链接、来源行、配图行拿出来另发。

### topmind-revise · 改稿与质检

- 四种模式：只审不改（出报告）、改稿（先备份再写回）、嵌入（长文技能调用，只回终稿）、快审（标题、短文、段子、回复）。
- `revise_check.py` 比对数字、引语、专名和确定性词，统计「没命中却被改写」的段落占比，防过度改稿。

### topmind-cover · 封面配图

- 主题 → 七层场景配方 → 2–3 个风格组合 → 分层 prompt → 七项评分；默认整张生成 + 逐字核对，兜底才用 `title-engine.py` 叠字。
- `crop-cover.py` 一键裁双平台尺寸；风格索引见 [`cover-styles.md`](./topmind-cover/references/cover-styles.md)。

<p align="center">
  <img src="https://github.com/topmindspace/topmind-writing-skills/raw/main/topmind-cover/assets/examples/overview.png" alt="topmind-cover · 22 封面风格总览" width="960" />
</p>

### topmind-poster · HTML → 高清长图

- HTML+CSS 排版 → 无头 Chrome 2× 截图 → 自动裁白，`render_poster.py` 一条命令跑完；版式配方见 [`layout-recipes.md`](./topmind-poster/references/layout-recipes.md)。
- 为什么不用生图模型：榜单里的文字和数字要逐字正确，生图会改字、编数字。封面没有密集文字，走 `topmind-cover`。

> 正式商务演示技能已独立成仓库：[`topmind-presentation`](https://github.com/topmindspace/topmind-presentation)。

## X 文本统一规约

所有产出 X 纯文本的技能共用（`shared/references/`）：

| 文档 | 管什么 |
|---|---|
| `x-delivery-contract.md` | 短文工作流（信源 → 原帖原图 → 内容 → 排版）；正文一段可复制纯文本，话题标签在末行；链接、原图、配图另发 |
| `x-post-format.md` | 不用 Markdown、列表符号、留白、来源、配图、公众号稿 → X 稿 |
| `emoji-system.md` | emoji 体系（只用于短文，且不强制）：人设点缀 0–2 个、标题 emoji 0–1 个、列表符号一帖一套 |
| `x-layout-patterns.md` | 版式规律：首行给结论、列表引导语、【小标题】分节 |

`lint_x_post.py` / `de_ai_lint.py` 的三级输出：

| 级别 | 含义 | 要求 |
|---|---|---|
| E 错误 | Markdown 残留（E1–E9）；正文里有 URL / 来源行 / 配图说明（E10–E12） | 必须清零 |
| W 警告 | AI 套话、首行太长、单段过长、结构套话、标点腔、自制图没标来源等 | 每条给结论：改，或写明保留理由 |
| H 提示 / I1–I8 | 语境词、对仗收句、emoji 过密；信息设计（连续长段、可转列表 / 表格、首段没交底等） | 只供判断，不进 `--strict` |

`--genre long|short|duanzi|reply|title` 选文体，`--no-hints` 关掉提示。

## 原创示例

示例都是我们自己写的（虚构或中性题材，不收录第三方原文、原图）：[viral-posts](./topmind-viral-posts/examples/) · [briefs](./topmind-briefs/examples/) · [format](./topmind-format/examples/) · [revise](./topmind-revise/examples/) · [x-article](./topmind-x-article/examples/) · [wechat-post](./topmind-wechat-post/examples/) · [poster](./topmind-poster/examples/) · [cover](./topmind-cover/assets/examples/)。

## 安装

**npm = 钉版本快照；GitHub = 跟仓库 HEAD。**

```bash
npx @topmindspace/topmind-writing-skills install topmind-briefs --to ./.claude/skills
npx @topmindspace/topmind-writing-skills@latest install topmind-briefs   # 升级：已装旧版直接覆盖
npx @topmindspace/topmind-writing-skills install topmind-briefs --force   # 同版本重装 / 降级
npx @topmindspace/topmind-writing-skills@0.8.4 install topmind-briefs     # 钉版本
npx @topmindspace/topmind-writing-skills uninstall topmind-briefs --to ./.claude/skills
npx github:topmindspace/topmind-writing-skills install topmind-briefs     # 跟 HEAD
```

- 默认探测 `./.agents` → `./.claude` → `./.cursor` → `./.codex` → `./.mimocode`，再用户级 `~/.claude` 等；安装摘要会打印实际目标目录。
- 已装版本更旧就覆盖（打印 `Upgraded <技能> <旧> -> <新>`）；版本相同打印 `Already up to date`；已装更新的版本时拒绝降级，需 `--force`。
- 不要 `npm install topmind-briefs`：技能 id 不是独立包。旧包 `tms-skills` 已停更，`^2`（2.0.0–2.1.1）已弃用。

## 仓库结构

```text
topmind-writing-skills/
├─ topmind-*/                    # 八个技能（SKILL.md + references + scripts + examples）
├─ shared/                       # 共享脚本与写作规则的唯一真源（manifest.json 声明分发目标）
├─ bin/topmind-writing-skills.js # CLI：list / install / uninstall
├─ evals/                        # 路由评测用例（不进 npm 包）
├─ docs/                         # 发布规范 · CI 说明
├─ scripts/                      # 仓库级门禁、同步、隐私扫描
└─ package.json · CHANGELOG.md · LICENSE
```

- 改共享文件只改 `shared/`，再跑 `npm run sync:shared`；CI 用 `--check` 校验各技能副本逐字节一致。
- SKILL.md frontmatter 顶层只用 Agent Skills 规范字段（`name` / `description` / `license` / `metadata`），自定义字段放 `metadata` 下，能通过 `skills-ref validate`。
- npm 包里 cover 只带 `overview.png`；单风格样张见 GitHub 或 Release zip。

## 发布与 CI

| 动作 | GitHub | npm |
|---|:---:|:---:|
| push main | 立即可见 | 不变 |
| tag `vX.Y.Z` | Release + zip | 自动 publish |

```bash
npm run check && npm run audit && npm run privacy
```

详见 [docs/PUBLISHING.md](./docs/PUBLISHING.md) · [docs/ci.md](./docs/ci.md)。

## 许可证

MIT © TopMindspace — [LICENSE](./LICENSE)
