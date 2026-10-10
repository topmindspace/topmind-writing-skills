# topmind-poster · HTML → 高清长图 PNG

[English](./README.en.md) | 中文

榜单、信息图、月报长图、海报，以及「一段一图」的分段图批量出图。文本 100% 可控、可 diff、可迭代。

- 版本：**v0.1.2**（随 `@topmindspace/topmind-writing-skills@0.8.27` 发布）

## 安装

```bash
npx @topmindspace/topmind-writing-skills install topmind-poster
```

## 为什么不用图片生成模型

榜单 / 信息图里有大量精确文本、数字、品牌名。图片生成模型会改字、糊字、编造数字。**这类图必须走「HTML 排版 → 无头浏览器截图」**。封面是例外——封面没有密集文本，走 `topmind-cover` 的生图路线。

## 能做什么

| 场景 | 产物 |
|---|---|
| 榜单 / 分级榜 / 信息图 | 一张竖版长图（1080 或 1180 宽，2× 高清） |
| 月报 / 周报长图 | 同上，可含图表卡片 |
| 一篇长文配 N 张图 | 分段图：一段一图，逐张可单独转发 |
| 已有 HTML | 直接导出高清 PNG 并自动裁掉底部空白 |

## 用法

最省事的一条命令：

```bash
python3 scripts/render_poster.py poster.html -o poster.png
```

脚本做完整三步：调无头 Chrome 2× 截图 → 按背景色扫底 → 裁掉底部空白。批量出分段图：

```bash
python3 scripts/render_poster.py build/*.html --out-dir images/ --width 1180
```

手写流程、参数含义、以及 7 个实测注意点（沙箱参数、柱状图填充消失、背景取色点、PNG 重采样反而变大等）见 [SKILL.md](./SKILL.md)。版式配方见 [references/layout-recipes.md](./references/layout-recipes.md)。

## 依赖

- 无头浏览器：Chrome / Chromium / Edge（`--chrome` 指定，或设 `CHROME_PATH`）
- `Pillow`（裁切用）：`python3 -m pip install --user Pillow`

## 边界

- **不做**文章封面 → `topmind-cover`
- **不做**多页演示 / PPTX → `topmind-presentation`
- **不做**纯数据图表 SVG → `svg-infographic-kit`
- **不做**文章正文排版 → `topmind-wechat-post` / `topmind-x-article`

本技能负责出图那一环：它们写好文章，本技能把其中一段做成能单独转发的图。
