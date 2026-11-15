# topmind-briefs · 高信噪比干货短文与快讯改写

[English](./README.en.md) | 中文

把经验技巧、提示词交付、行业快讯、新品发布、论文解读与实测观点写成高信噪比短文（X 短帖与公众号 300–800 字短文），让读者第一眼看懂跟自己有什么关系、拿走就能用。

## 核心特点

- **按稿型选开口，不套单一模板**：
  - **经验技巧 / 提示词交付**：结果或反差数字直接做第一句，正文附上可直接复制的原件（命令/提示词 + 一句中文大意），结尾画清「什么时候别用」的负面边界。
  - **新品 / 硬件 / 行业快讯**：砍掉公关致谢、购买门槛与冗长头衔，把冰冷参数译成日常体感（如「41 克」译成「跟普通眼镜差不多重」）。
  - **安全事件 / 突发传闻**：接住读者第一反应的真疑问，紧接一句澄清真实影响范围，再用紧凑 `1）2）` 列出核心事实与应对建议。
- **邻座同行口吻**：像坐在旁边的同行朋友分享实测，不摆讲师架子，不代编第一人称亲历，查证过程放在正文代码块外。
- **按需知识包**：内置 `brief-value-first`、`brief-news-to-post`、`voice-peer-stance`、`de-ai-mechanisms` 等实战卡片（见 [知识导航](./knowledge/README.md) 与 [知识库说明](./references/knowledge-library.md)）。

## 安装与使用

```bash
npx @topmindspace/topmind-writing-skills install topmind-briefs
```

完整策略、稿型表格与工作流见 [SKILL.md](./SKILL.md)，实战改稿前后对比见 [examples/README.md](./examples/README.md) 与 [references/examples.md](./references/examples.md)，多平台封面尺寸见 [platform-cover-specs.md](./references/platform-cover-specs.md)。

## 常用脚本

```bash
python3 scripts/lint_x_post.py X短文.txt --kind news
python3 scripts/de_ai_lint.py 公众号短文.md
python3 scripts/format_text.py X短文.txt --mode short --out 排版稿.txt
```

脚本仅检查格式残留并提供语境提示，不作为阻断交付的硬门禁。只负责生成文稿，由用户确认后对外发布。

MIT License。仓库维护与合集说明见 [topmind-writing-skills](https://github.com/topmindspace/topmind-writing-skills)。
