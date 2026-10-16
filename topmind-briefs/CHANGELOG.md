# Changelog

## 0.2.20 (2026-10-16)

- 新增 `examples/` 原创示例（X 短文 2 篇 + 链接配图另列 + 公众号短文 1 篇）；示例链接换成 example.com 占位

## 0.2.19 (2026-10-14)

- 变更：工作流改为「信源 → 原帖原图 → 内容 → 排版」；X 正文一段可复制纯文本，不含 URL 与来源行，链接 / 原图另发；emoji 不强制，分点可用「1）」「·」【小标题】
- 优化：示例与 platform-specs、style-guide 按新规约重写；去 AI 味 + 吸引力清单并入 writing-principles

## 0.2.18 (2026-10-14)

- 更正：共享规约改为「短文分点用 emoji 列表符号、段子完全不用 emoji」；`emoji-system.md` 标明只适用于短文体；`lint_x_post.py` 新增 `--duanzi`（W13）

## 0.2.17 (2026-10-14)

- 特性支持：接入共享 X 交付规约 `x-delivery-contract.md`（必读必守）——X 正文单独成块，信源 / 原图 / 说明另列；分点必须用 emoji 列表符号
- 优化：`examples.md` 改为中文示例并去掉正文里的图片占位；`platform-specs.md`、`style-guide.md` 去重；删除重复的「配图铁律」节

## 0.2.16 (2026-10-14)

- 特性支持：交付固定三块（可复制纯文本正文 / 原帖与信源地址 / 1–2 张原图）并附正例模板；没有原图时主动询问是否配图，不擅自生图
- 优化：X 版写作接入共享 `x-layout-patterns.md`（首行给结论、列表引导语、长条目间空行、【小标题】分节、中英混排、链接单独一行）；emoji 只引用共享 `emoji-system.md`
- 优化：`lint_x_post.py` 新增 E8/E9/W11（见根 CHANGELOG 0.8.33）

## 0.2.15 (2026-10-14)

- 变更：短文默认不出 HTML——X 版交付一段可直接复制的纯文本，公众号版交付 Markdown；`md2x-html.py` / `md2wechat.py` 仍随包自带，仅在用户明确要求时使用
- 特性支持：新增「尊重原始信息」铁律（原始信息 / 原文 / 原图 / 口径标注 / 不洗稿）与交付格式（X 版、公众号版、配图、信息来源：来源名称｜发布时间｜链接）
- 变更：配图原图优先，没有原图时封面可选（不再默认配封面）；接入共享 `emoji-system.md` 与 `format_text.py`
- 优化：新增「和其他技能怎么配合」表；description 的 Do NOT 增加格式化 / 转段子 → topmind-format

## 0.2.14 (2026-10-14)

- X 版来源行规范、默认 16:9 封面、lint W8/W9/W10 警告处理（见根 CHANGELOG 0.8.31）

## 0.2.13 (2026-10-11)

- 特性支持：X 版纯文本排版——不用 Markdown 列表、标题和加粗，分点改用 emoji 项目符号；新增共享规则文档 `references/x-post-format.md` 与检查脚本 `scripts/lint_x_post.py`
- 特性支持：X 版末尾给 0–2 个话题标签建议（公众号稿不加），规则写入 `platform-specs.md`；`examples.md` 的 4 个 X 示例同步改成 emoji 列表并附话题标签建议
- 优化：description 补充「公众号短文、X 短文、简讯、速报、论文解读」等说法，Do NOT 增加封面分流并点名 viral-posts 的段子、涨粉帖、互关帖；文案改用更平实的表述

## 0.2.12 (2026-10-11)

- 优化：description 的 Do NOT 增加「单独出长图/海报/信息图 PNG → topmind-poster」分流，与 poster 的触发词边界互相点名

## 0.2.11 (2026-10-11)

- 修文案：交付脚本 `md2wechat.py` 的 `--author` 帮助文本改为「留空则不输出署名行」，
  与 2026-10-01 起的实际行为对齐（原文案仍写「留空写 {{作者名}} 占位」，提示与实现不符）

## 0.2.10 (2026-10-10)

- 优化：`examples.md` 的 4 个示例与开场句式模板改为原创内容，通用写作原则中的示例同步整理

## 0.2.9 (2026-10-10)

- 优化：示例与风格参考改为自编通用内容，风格说明按通用类型归纳

## 0.2.8 (2026-10-08)

- 优化：交付脚本与 `writing-principles.md` 的唯一真源改为仓库 `shared/`，`negative_tests.py` 改为与 `shared/` 比对
- 优化：个人向短帖改指 `topmind-viral-posts`（原指向未发布的 `topmind-x-posts`），发帖由 `topmind-x` 负责且须用户确认
- 特性支持：frontmatter 迁入 `metadata`，通过 `agentskills validate`；`triggers_cn` 并入 `metadata.triggers` 与 description

## 0.2.7 (2026-10-08)

- 交付脚本随技能自带：`scripts/md2x-html.py`、`scripts/md2wechat.py`（x-article / wechat-post 同名脚本的逐字节副本），
  单独安装 briefs 即可出双版 HTML
- `negative_tests.py` 校验交付脚本随包存在，仓库内再校验与上游逐字节一致
- 交付命令对齐脚本实际参数：公众号版补 `--out-dir` / `--slug` / `--no-toc`；X 版统一 `--images-from`
- 公众号篇幅统一为「约 300–800 字」（style-guide 原写「500 字内」）；X 版写明每条 280 字符、thread 最多 3 条

## 0.2.0 (2026-10-01)

- `--images-from 公众号短文.md` 派生图片顺序，禁止手工拼 `--images`（根治配图错位）
- 构建后校验加：X 版内嵌图序列（无封面）与公众号版逐字节一致
- 新增交付铁律（用原文件原样呈现）；语言铁律同步（默认中文）


## 0.1.0 (2026-10-01)

- 初始版本：干货短文（公众号 + X 双平台）
- 工作流：定主题 → 找素材 → 写双版 → 自检 → 交付
- 四种内容类型：数据榜单型 / 论文解读型 / 新品速递型 / 对比实测型
- references：style-guide（开头扔结论/列表>段落/禁止清单）、
  platform-specs（X ≤280字符 / 公众号 300–800字对照）、examples（4 类示例 + 反例）
- 风格参考：数据榜单型、榜单速报型、论文解读型、机制讲解型等通用类型
- 运营铁律：只起草不代发、数字必有来源、厂商数字标口径、不洗稿
- 修订（2026-10-01）：字数口径统一为"X 一帖/短 thread，公众号约 300–800 字"；
  交付明确为双版一键复制 HTML（X 走 md2x-html，公众号走 md2wechat --embed-images）；
  构建后必跑嵌入图数量/顺序校验；配图位置铁律（图片紧跟相关段落）；
  推测/判断必须显式标注"（推测）"与事实切割
