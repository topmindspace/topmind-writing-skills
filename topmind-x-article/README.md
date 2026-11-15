# topmind-x-article · X Article 深度长文与导出

[English](./README.en.md) | 中文

创作、整理与导出 X Article（推特长文），支持观点与机制深解、工具/插件推荐、产品实测评测与跨平台派生；一键导出带富文本复制与图片占位的单文件 HTML、纯文本兜底稿与发布清单。

## 核心特点

- **按题材组织长文推进**：
  - **观点与机制深解（`x-argument` / `x-evidence`）**：核心结论或反差前置，逐节用实测数据与证据推进，保留作者有温度的同行判断。
  - **工具推荐与实测评测（`wechat-plugin-and-review`）**：支持代码块、安装命令与随文链接（不受普通 X 短帖「无外链」限制）；完整保留作者具体褒贬。
  - **跨平台引流隔离（`x-adapt`）**：长文保留完整命令与链接，派生的引流短帖按 X 短帖习惯采用「结果前置 + 段落空行 + 紧凑 `1）2）`」。
- **单源保序与提示词双通道复制**：
  - `md2x-html.py` 直接按源稿 `![]()` 顺序嵌图并生成 `[图N]` 占位，彻底杜绝配图错位。
  - 针对 X Article 粘贴限制，提供「一键复制全文 + 逐块复制提示词转原生 Code 块」双通道体验。

## 安装与使用

```bash
npx @topmindspace/topmind-writing-skills install topmind-x-article
```

完整策略与导出规范见 [SKILL.md](./SKILL.md) 与 [x-html-format.md](./references/x-html-format.md)，示例长文见 [examples/README.md](./examples/README.md)，X Article 头图尺寸（`1500×600` `5:2`）见 [platform-cover-specs.md](./references/platform-cover-specs.md)。

## 常用脚本

```bash
python3 scripts/md2x-html.py 文章.md --preview
python3 scripts/md2x.py 文章.md
python3 scripts/check_article.py <文章目录>
```

只负责生成长文与导出包，由用户在 X Article 编辑器确认发布。

MIT License。仓库维护与合集说明见 [topmind-writing-skills](https://github.com/topmindspace/topmind-writing-skills)。
