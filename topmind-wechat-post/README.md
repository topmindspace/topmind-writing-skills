# topmind-wechat-post · 公众号深度文章与排版交付

[English](./README.en.md) | 中文

从选题或底稿创作公众号文章，支持工具/插件推荐专项结构、产品实测评测、机制深解与叙事随笔；按需导出微信公众号全内联样式 HTML、手机端预览图与图片上传清单。

## 核心特点

- **按文章体裁灵活组织结构**：
  - **工具 / 插件推荐文（可选专项结构）**：标题直接点名工具 → 开头直给解决什么痛点与安装命令/入口 → 全景功能列表 → 每个小标题配简短例子与真实截图；简单直观的功能不长篇大论拔高。
  - **产品实测 / 模型评测文**：按具体观察维度（延迟、打断、准确率、账单）展示实测，完整保留作者个人褒贬，不洗成「各有千秋」的套话。
  - **机制深解 / 行业观察**：区分「开源代码参数/实验数据」与「线上实际体感」，保留作者有温度的同行判断。
- **高信噪比图文与诚实标注**：客观证据与作者建议视觉分区；论文/文档截图用真实原图高亮并保留上下文（严禁排版伪造假截图）；概念封面标注 `功能示意，不是实拍`。
- **单源 Markdown 与内联 HTML 渲染**：内置 6 套公众号主题（`md3-business-blue`、`minimal-ink`、`tech-blue`、`amber-review`、`graphite`、`newsprint`），自动处理微信编辑器标签兼容与图片 base64 内嵌。

## 安装与使用

```bash
npx @topmindspace/topmind-writing-skills install topmind-wechat-post
```

完整创作流程与主题说明见 [SKILL.md](./SKILL.md) 与 [platform-operations.md](./references/platform-operations.md)，精品示例稿见 [examples/README.md](./examples/README.md)，公众号封面尺寸（`900×383` 与 `900×900`）见 [platform-cover-specs.md](./references/platform-cover-specs.md)。

## 常用脚本

```bash
python3 scripts/md2wechat.py --input 文章.md --embed-images --preview
python3 scripts/check_article.py <文章目录>
python3 scripts/de_ai_lint.py 文章.md --genre long
```

只负责生成文稿与排版发布包，由用户在公众号后台确认发布。

MIT License。仓库维护与合集说明见 [topmind-writing-skills](https://github.com/topmindspace/topmind-writing-skills)。
