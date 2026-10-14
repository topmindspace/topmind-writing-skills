# topmind-briefs · 干货短文（公众号 + X 双平台）

[English](./README.en.md) | 中文

一件事，讲完就停。干货向短文：数据榜单、论文解读、新品速递。短文不是长文——**默认不出 HTML**：
X 版是一段可直接复制的纯文本（分段换行 + 克制的 emoji + 来源链接），公众号版约 300–800 字 Markdown。
尊重原始信息、原图、原文；配图原图优先，没有原图时封面可选（`topmind-cover`）；交付时写明信息来源、发布时间与来源链接。

- 版本：**v0.2.18**（随 `@topmindspace/topmind-writing-skills@0.8.35` 发布）

## 安装

```bash
npx @topmindspace/topmind-writing-skills install topmind-briefs
```

## 用法

```bash
# 检查 X 版：无 Markdown 残留、符号一致、表情不过量、有来源
python3 scripts/lint_x_post.py X短文.txt
# 只动排版不改字：统一分段、列表改 emoji、加标题 emoji 与人设点缀
python3 scripts/format_text.py X短文.txt --mode short --title-emoji 📊 --out X短文.txt
```

交付格式：`【X 版】`纯文本 +（可选）`【公众号版】`Markdown + `【配图】`原图与来源 + `【信息来源】`来源名称 / 发布时间 / 链接。

用户明确要 HTML 时才用（脚本随包自带，唯一真源在仓库 `shared/scripts/`）：

```bash
python3 scripts/md2x-html.py X短文.md --out X短文.html --images-from 公众号短文.md
python3 scripts/md2wechat.py --input 公众号短文.md --out-dir 交付 --slug 短名 --embed-images --no-toc
```

工作流细节见 [SKILL.md](./SKILL.md)；emoji 体系见 [references/emoji-system.md](./references/emoji-system.md)。

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

现成文字格式化 / 转段子 → `topmind-format`；X 长文 → `topmind-x-article`；公众号长文 → `topmind-wechat-post`；
引流互动型短帖与段子 → `topmind-viral-posts`；单独出长图/海报 → `topmind-poster`；
封面/头图 → `topmind-cover`；发帖 → `topmind-x`（须用户确认）。
