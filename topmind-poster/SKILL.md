---
name: topmind-poster
description: "用 HTML/CSS 创建和修改高信噪比长图、海报、榜单、一图流总结卡与分段配图，渲染高清 PNG 并交付可编辑源文件。坚持一图讲清变化、边界与建议，将客观证据与作者建议视觉分区。单张文章封面用 topmind-cover。"
license: MIT
metadata:
  version: "0.1.13"
  action_category: "write"
  triggers: "长图, 竖版长图, 海报, 信息图, 一图流, 总结卡, 分级榜, 榜单图, 月报长图, 分段图, HTML 转 PNG, 渲染成, 一张图讲清楚, 高清出图, poster, long image, 做一张长图, 重做这张图, 更新这张图, 把这张图优化一下, 出一张高清图, 把长图拆成几张, 给文章做信息图"
  author: "TopMindSpace"
  homepage: "https://github.com/topmindspace/topmind-writing-skills#readme"
  updated: "2026-11-15"
---

# topmind-poster · 一图流信息图、海报与高清长图

用可编辑 HTML/CSS 排版，输出文字与数字精准的高清 PNG。适用于「一张图讲清主要变化、边界与建议」的总结卡、榜单对比、流程架构图与分段配图。

## 一、高信噪比信息图四大准则（核心设计思想）

动笔写 HTML 前，先按 [information-design.md](references/information-design.md)、[image-sourcing.md](references/image-sourcing.md) 与知识卡 `visual-density-and-evidence` 确立信息结构：

1. **一图讲清三件事**：一张好的信息图优先把**主要变化（核心数字/对比）、事实边界（适用条件/何时别用）、作者具体建议**放在同一张图里讲明白，让读者保存一张图就能带走全部干货。
2. **客观证据与作者建议视觉分区**：
   - 把「开源代码参数、论文原表、官方原文（客观证据）」与「作者使用建议、个人推断（主观观点）」放在不同底色、边框或明确标注的区块里，不混排误导读者。
3. **适度视觉密度，拒绝两个极端**：
   - 既不做「大片留白 + 几个空洞大字」的假极简图，也不做「把未经核实的细碎参数和大段免责声明全塞进去、手机根本看不清」的拥挤技术长图。
   - 手机端一屏或舒适滑动即可看清核心字号；长内容按语义任务拆成多张分段图（见知识卡 `poster-paging`）。
4. **原文真实高亮与学术图表克制**：
   - 引用论文或文档证据时直接嵌入真实截图并高亮关键行、保留上下文，**绝不自己用 HTML 排版伪造一张看似论文原页或官方公告的假截图**。
   - 学术与硬核技术解释图采用干净克制的图表风格，**不添加卡通吉祥物或卖萌 logo**。
   - 涉及概念演示或旧版数据时诚实标注 `功能示意，不是实拍` 或「示例数据」。

更多检索见 [knowledge-library.md](references/knowledge-library.md) 与 [creative-practice.md](references/creative-practice.md)。

## 二、形式选择与 HTML/CSS 渲染

| 内容关系 | 推荐视觉形式 |
|---|---|
| **规则变化 / 技巧总结（一图流）** | 顶部核心结论 → 中部左/上「客观证据与对比」、右/下「作者建议与何时别用」 |
| **排名 / 分档 / 跑分榜单** | 条形对比图、分档卡片、同口径高亮表（标明测试口径与数据来源） |
| **时间演进 / 流程机制** | 时间轴、步骤路径图、因果架构图 |

[layout-recipes.md](references/layout-recipes.md) 提供起步版式；多平台尺寸参考 [platform-cover-specs.md](references/platform-cover-specs.md)。常用画布宽度为 1080 / 1180 / 1200 px：

```bash
python3 scripts/render_poster.py poster.html -o poster.png
```

## 三、工程要点与交付核对

- `span` 默认 inline，设宽高需用 `inline-block` / `block`；Python 生成 HTML 时注意避免 `.format()` 与 CSS `{}` 冲突。
- 渲染完成后**必须实际打开最终 PNG 检查**：字号在手机端是否清晰、末尾是否被裁断、客观证据与作者建议是否已明确分区、数据口径是否标清。
- 交付最终高清 PNG 与可编辑 HTML 源文件。本技能不执行对外发布。
