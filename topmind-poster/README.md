# topmind-poster · 一图流信息图、海报与高清长图

[English](./README.en.md) | 中文

用可编辑 HTML/CSS 构建高信噪比「一图流」总结卡、对比榜单、流程架构图与分段长图，渲染输出文字与数字精准的高清 PNG，并同步交付 HTML 源文件。

## 核心特点

- **一图讲清三件事**：优先把**主要变化（核心数字/对比）、事实边界（适用条件/何时别用）、作者具体建议**放在同一张图里讲明白，让读者存一张图就能带走核心干货。
- **客观证据与作者建议视觉分区**：将「开源代码参数、论文原表、实测数据（客观证据）」与「作者选型建议、个人推断（主观观点）」用不同底色或边框明确分区。
- **适度视觉密度与真实引证**：
  - 手机端一屏或舒适滑动即可看清核心字号（正文 ≥ 22px），拒绝假极简大留白与塞满细碎免责声明的拥挤长图。
  - 引用论文或文档时嵌入真实截图并高亮关键行，**绝不用 HTML 伪造假论文页或假官方截图**；学术技术图表保持干净克制，概念或演示数据标明 `功能示意，不是实拍`。

## 安装与使用

```bash
npx @topmindspace/topmind-writing-skills install topmind-poster
```

完整设计准则见 [SKILL.md](./SKILL.md)，HTML/CSS 版式配方（画布宽度、字阶、配色、栅格、进度条）见 [layout-recipes.md](./references/layout-recipes.md)，实战 HTML 与说明见 [examples/README.md](./examples/README.md)。

## 常用脚本

```bash
python3 scripts/render_poster.py poster.html -o poster.png
```

渲染完成后实际打开 PNG 核对字号、裁切、证据分区与数据口径。只负责生成图像与 HTML 源文件，由用户完成对外发布。

MIT License。仓库维护与合集说明见 [topmind-writing-skills](https://github.com/topmindspace/topmind-writing-skills)。
