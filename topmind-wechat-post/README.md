# topmind-wechat-post · 公众号文章

[English](./README.en.md) | 中文

从选题或底稿写作，按需输出内联 HTML、预览和图片上传清单。

平台封面、图文形态与跨平台裁切见 [平台参考](./references/platform-cover-specs.md)，按需读取；预设不等于强制上传规格，平台展示需实际验证。

## 使用

```bash
npx @topmindspace/topmind-writing-skills install topmind-wechat-post
```

安装后直接告诉 agent 你要的结果、读者和已有材料；明确要一稿就直接给成品，探索任务再比较方向。完整能力、流程与脚本说明见 [SKILL.md](./SKILL.md)。

按需知识包随技能独立安装。需要方向、完整示例或经验时，见 [知识使用与增补](./references/knowledge-library.md) 与 [知识导航](./knowledge/README.md)；先读摘要再选卡片。可向指定私有包新增候选，不自动改长期规则。

## 方法与样张

[创作方法与样张](./references/creative-practice.md) 给同素材不同写法和看参考的方法。模板、口吻、篇幅、emoji 与视觉风格是选项；事实准确、授权、隐私与输出完整性继续核对。当前用户要求和作者样本优先。

## 常用脚本

在本技能目录运行；示例文件名替换为实际路径：

```bash
python3 scripts/md2wechat.py --input 文章.md --embed-images --preview
```

采用 HTML 导出时核对内联样式、图片清单与图文顺序。预览需可用浏览器及相应依赖；上传后仍需检查编辑器展示。

## 交付

交付当前请求所需的 Markdown；需要发布包时附内联 HTML、预览与图片上传清单。 由用户完成对外发布。

MIT License。仓库维护、安装选项与版本说明见 [合集说明](https://github.com/topmindspace/topmind-writing-skills)。
