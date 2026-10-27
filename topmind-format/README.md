# topmind-format · X 文本排版

[English](./README.en.md) | 中文

已有文字保留措辞与事实，只调整呈现；默认保留表情、链接与来源。

## 使用

```bash
npx @topmindspace/topmind-writing-skills install topmind-format
```

安装后直接告诉 agent 你要的结果、读者和已有材料；明确要一稿就直接给成品，探索任务再比较方向。完整能力、流程与脚本说明见 [SKILL.md](./SKILL.md)。

按需知识包随技能独立安装。需要方向、完整示例或经验时，见 [知识使用与增补](./references/knowledge-library.md) 与 [知识导航](./knowledge/README.md)；先读摘要再选卡片。可向指定私有包新增候选，不自动改长期规则。

## 方法与样张

[方法参考](./references/creative-practice.md) 用于判断节奏与表达作用。只调整断行、空行和允许的呈现符号，保留原文措辞、事实与顺序；改写另用 topmind-revise。

## 常用脚本

在本技能目录运行；示例文件名替换为实际路径：

```bash
python3 scripts/format_text.py 原文.txt --mode duanzi --out 排版稿.txt
```

保留链接和有表达作用的符号；仅在明确要求时使用 --separate-links 或 --strip-emoji。排版后核对措辞、事实与顺序。

## 交付

交付可直接复制的排版文本；需要改写时转交改稿技能。 由用户完成对外发布。

MIT License。仓库维护、安装选项与版本说明见 [合集说明](https://github.com/topmindspace/topmind-writing-skills)。
