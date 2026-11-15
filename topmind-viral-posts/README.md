# topmind-viral-posts · X 段子、观察反差与互动短帖

[English](./README.en.md) | 中文

从内行观察、算账反差、装傻真问题、产品反转和自然接话中找角度，写出有内容、有特色、有人味的社交短帖与神回复。作者风格优先。

## 使用

```bash
npx @topmindspace/topmind-writing-skills install topmind-viral-posts
```

安装后直接告诉 agent 你要表达的核心观察、目标受众和已有素材；明确要一稿就直接给成品，探索任务再提供不同切口的候选。完整策略、12 类切口与脚本说明见 [SKILL.md](./SKILL.md) 与 [patterns.md](./references/patterns.md)。

按需知识包随技能独立安装。需要去 AI 味机制、邻座身位、装傻提问正反例或回复心法时，见 [知识使用与增补](./references/knowledge-library.md) 与 [知识导航](./knowledge/README.md)；也可随时向知识包扩展新的创作思考与策略。

## 方法与样张

[创作方法与样张](./references/creative-practice.md) 给同素材不同写法和阅读参考的方法。句式、口吻、标点力气活（`？？？` / `！！！` / `！！？`）、篇幅与 emoji 均为服务表达的灵活工具；不代编第一人称经历、守住事实边界与不擅自外发是底线。

## 常用脚本

在本技能目录运行；示例文件名替换为实际路径：

```bash
python3 scripts/lint_x_post.py 稿子.txt --duanzi
```

`lint_x_post.py` 检查 Markdown 格式残留并提供语境提示；提示不作为阻断交付的硬门禁。

## 交付

交付可直接复制使用的短帖、段子、引用转发或评论回复纯文本；由用户确认后完成对外发布。

MIT License。仓库维护、安装选项与版本说明见 [合集说明](https://github.com/topmindspace/topmind-writing-skills)。
