# topmind-briefs · 干货短文（公众号 + X 双平台）

[English](./README.en.md) | 中文

一件事，一张图，讲完就停。干货向短文：数据榜单、论文解读、新品速递——
X 一帖或短 thread，公众号约 300–800 字，双版一键复制 HTML。

- 版本：**v0.2.14**（随 `@topmindspace/topmind-writing-skills@0.8.31` 发布）

## 安装

```bash
npx @topmindspace/topmind-writing-skills install topmind-briefs
```

## 用法

在本技能目录下运行：

```bash
# X 版（图片顺序从公众号稿派生，禁止手工拼 --images）
python3 scripts/md2x-html.py X短文.md --out X短文.html --images-from 公众号短文.md

# 公众号版（图片 base64 内嵌，输出 <短名>-公众号版.html + 图片上传清单.md）
python3 scripts/md2wechat.py --input 公众号短文.md --out-dir 交付 --slug 短名 --embed-images --no-toc
```

两个脚本随本技能自带（纯 Python 标准库），单独安装 briefs 即可出 HTML。
唯一真源在仓库 `shared/scripts/`，与 `topmind-x-article` / `topmind-wechat-post` 是同一份逐字节副本，
仓库 CI 用 `node scripts/sync_shared.js --check` 校验一致。工作流细节见 [SKILL.md](./SKILL.md)。

## X 版格式与话题标签

X 不渲染 Markdown，X 版不用 `- ` 列表、`#` 标题和 `**加粗**`：分点用 emoji 项目符号（🔹 并列、▫️ 二级、1️⃣ 步骤、✅/❌ 对比），
同帖风格一致、每条一行、最多两层。公众号稿继续用 Markdown 列表；X 稿由公众号稿派生，只允许排版差异，内容一致。
X 版末尾附 0–2 个话题标签建议（单独成行放最后，公众号稿不加）。规则见 [references/x-post-format.md](./references/x-post-format.md)
与 [references/platform-specs.md](./references/platform-specs.md)。

```bash
# 检查 X 版：无 Markdown 列表/标题/加粗，话题标签在末行；加 --fix --out 自动改写
python3 scripts/lint_x_post.py X短文.md
```

## 内容类型

- 数据榜单型 / 榜单速报型 / 论文解读型 / 机制讲解型（见 SKILL.md，四种常用结构）
- 运营铁律：只起草不代发、数字必有来源、厂商数字标口径、不洗稿

## 何时不用

X 长文 → `topmind-x-article`；公众号长文 → `topmind-wechat-post`；
引流互动型短帖与段子 → `topmind-viral-posts`；单独出长图/海报 → `topmind-poster`；
封面/头图 → `topmind-cover`；发帖 → `topmind-x`（须用户确认）。
