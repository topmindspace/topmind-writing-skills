# Changelog

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
