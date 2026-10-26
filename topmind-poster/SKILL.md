---
name: topmind-poster
description: "用 HTML/CSS 创建和修改长图、海报、榜单、信息图与分段配图，渲染高清 PNG 并交付可编辑源文件。适用于精确文字和数据排版；单张文章封面用 topmind-cover，多页演示另用演示工具。"
license: MIT
metadata:
  version: "0.1.10"
  action_category: "write"
  triggers: "长图, 竖版长图, 海报, 信息图, 分级榜, 榜单图, 月报长图, 分段图, HTML 转 PNG, 渲染成, 一张图讲清楚, 高清出图, poster, long image, 做一张长图, 重做这张图, 更新这张图, 把这张图优化一下, 出一张高清图, 把长图拆成几张, 给文章做信息图"
  author: "TopMindSpace"
  homepage: "https://github.com/topmindspace/topmind-writing-skills#readme"
  updated: "2026-10-26"
---

# topmind-poster · 长图、海报与信息图

用可编辑 HTML/CSS 排版，输出文字与数字准确的高清 PNG。适合榜单、月报、流程、对照、单页海报和文章分段配图。

## 内容先明确，形式可探索

读用户素材、原图与数据，明确读者要看懂的内容。已有参考时实际查看其网格、读序、密度和图文关系；方法见 [creative-practice.md](references/creative-practice.md)。

| 内容 | 可尝试的形式 |
|---|---|
| 排名 / 分档 | 条形图、分档榜、卡片 |
| 时间 / 演进 | 时间线、折线、分阶段叙事 |
| 多对象多维对比 | 表格、分行对照、小多图 |
| 步骤 / 因果 | 流程、路径、编号图 |
| 单个判断 / 概念 | 巨字、摄影、抽象图形、留白 |

[layout-recipes.md](references/layout-recipes.md) 提供起步版式，不强制双栏、圆角或阴影；一栏、非对称、无卡片、纯文字也可以。模糊的复杂任务可先比较不同读序的小样；已有明确版式就直接完成。

## 制作与渲染

常用 CSS 画布宽为 1080 / 1180 / 1200 px，按平台和内容调整。确定宽度，给文字足够空间；字体从当前环境实际可用的中文字体选，离线颜色与资源在文件里可解析。

```bash
python3 scripts/render_poster.py poster.html -o poster.png
```

先用随包脚本发现浏览器，不照抄某台电脑的应用路径。2× 是清晰文本的常用起点，画布高度留足并检查末尾是否完整。失败时查看具体错误再调整参数；没有渲染环境时保留 HTML，说明 PNG 尚未完成。

密集文字用排版工具保证准确，插画或纹理可由生图工具生成后作为素材嵌入；生成素材不承担真实数据或证据图职责。

## 工程经验（出现对应症状时查）

- `span` 默认 inline，宽高不生效时改成 block / inline-block；百分比高度要有确定的父级高度。
- 等宽卡片可用 Grid；不同叙事节奏可用其他布局，不为了统一改掉合适的设计。
- 扫底裁切适合纯色空白尾部，底色从窗口底部取。全页纹理、渐变可能使颜色扫描失效，应检查裁切结果或改用内容边界。
- 预览缩小后的假乱码先回原尺寸局部看；PNG 缩小重采样可能反而更大，压缩时比较实际大小和文字质量。
- Python `.format()` 与 CSS 花括号冲突时用模板或明确占位符替换。

文章一段一图可按节生成多个 HTML，统一尺寸、页眉或页码；独立海报不必套分段协议。源码与输出保持可对应，压缩内嵌版与上传原图按视觉内容和映射核对，编码不同不要求字节相同。

## 核对与交付

实际打开最终 PNG，看全文和局部：缺字、溢出、图形缺失、末尾截断、过小字号。长图可分段查看。关键数字、时点、量纲和来源核对；不同口径比较需要明确解释，自制图标来源或“示意”。

交最终 PNG 与可编辑 HTML；有数据时附来源和口径，纯文字活动海报无需凑数据来源报告。样例与流程见 `examples/`、[information-design.md](references/information-design.md)、[image-sourcing.md](references/image-sourcing.md)。本技能不执行发布。

文章封面用 `topmind-cover`，文案用 `topmind-briefs` / `topmind-viral-posts` / 长文技能；当前用户要完整交付时可组合执行。
