---
name: topmind-x-article
description: "创作或整理 X Article 深度长文，支持论点推进、工具/插件介绍、产品实测评测与多源研究；按需导出可复制 HTML、纯文本、封面与发布清单。普通短帖用 topmind-briefs 或 topmind-viral-posts，纯格式化用 topmind-format。"
license: MIT
metadata:
  version: "0.4.30"
  action_category: "write"
  triggers: "X 长文, 发 X 文章, 写 X 文章, X article, 长文发 X, X 发长文, X 文章排版, 转纯文本, X 纯文本, X发布稿, 发 article, 一键复制, 写 X 长文, X 长文发布, 推特长文, twitter 长文, Twitter Article"
  author: "TopMindSpace"
  homepage: "https://github.com/topmindspace/topmind-writing-skills#readme"
  updated: "2026-11-15"
---

# topmind-x-article · X Article 深度长文与导出

创作或整理 X Article 长文，并按需导出可复制 HTML、纯文本、封面和发布清单。默认中文；从用户当前进度接着做，保留作者鲜明的判断与声音。

## 一、按题材选择长文结构（给思考留出空间）

根据文章目的选择最利落的结构（见 [information-design.md](references/information-design.md)、[creative-practice.md](references/creative-practice.md) 与 [knowledge-library.md](references/knowledge-library.md)）：
1. **观点与机制深解（`x-argument` / `x-evidence`）**：结论或核心反差前置，逐节用证据推进；保留作者有温度的个人判断（「仔细聊了一轮，我倒觉得……」），同时区分「开源代码参数/实验结果」与「线上全面生效」。
2. **工具 / 插件推荐长文（可选结构 `wechat-plugin-and-review`）**：标题直接点名工具/插件 → 开头直给解决什么痛点与安装命令/入口 → 核心功能列表 → 小标题配简短例子与真实截图；简单直观的功能不长篇讲道理。
3. **产品实测与模型评测**：按具体观察维度（如延迟、报数字停顿是否被打断、准确率、账单成本）展开实测，完整保留作者个人褒贬，不洗成「各有千秋」的套话。
4. **跨平台适配（`x-adapt`）**：X Article 正文支持小标题、代码块、安装命令与参考链接；若需同时派生一条普通 X 短帖引流，短帖按 [x-delivery-contract.md](references/x-delivery-contract.md) 采用「结果前置、段落空行、紧凑 `1）2）`、默认无外链」习惯。

## 二、图文证据设计与去 AI 味边界

- **证据与建议视觉分区**：自制信息图力求一图讲清主要变化、事实边界与作者建议，并将客观证据（代码/论文/原文）与作者建议分区呈现。
- **原文高亮 + 保留上下文**：展示论文、文档或代码截图时，用真实原图高亮关键句并保留上下两行上下文，**绝不自己排版伪造假论文页或假官方截图**。
- **诚实标注**：概念封面或生成图涉及界面表现时标明 `功能示意，不是实拍`；旧界面截图在图注标明示例数据或版本；学术技术图采用干净图表风，不贴卡通吉祥物 logo（详见 [image-sourcing.md](references/image-sourcing.md)）。
- **去 AI 味自查**：不代编第一人称亲历，删掉元话语与文末升华金句（见 [core-voice.md](references/core-voice.md)、[de-ai-rules.md](references/de-ai-rules.md)、[revision-workflow.md](references/revision-workflow.md) 与 [research-mode.md](references/research-mode.md)）。所有脚本提示（W/H/I）仅作参考，**不作为阻断交付的硬门禁**。

## 三、单源文件与可重建导出

纯聊天写稿直接交 Markdown；需要完整发布包时使用单源目录（详见 [platform-operations.md](references/platform-operations.md) 与 [workspace.md](references/workspace.md)）：

```bash
python3 scripts/article_scaffold.py --title "文章名" --base <已确认目录>
python3 scripts/md2x-html.py <文章目录>/<文章名>.md --preview
python3 scripts/md2x.py <文章目录>/<文章名>.md
python3 scripts/check_article.py <文章目录>
```

- `out/X长文.html` 供作者复制富文本与 `[图N]` 占位位置；配图与 1500×600 头图（见 [platform-cover-specs.md](references/platform-cover-specs.md)）在 X Article 编辑器上传。
- 提示词与代码块的导出规则见 [x-html-format.md](references/x-html-format.md)，纯文本转换见 [x-format.md](references/x-format.md)，发布前核对见 [publish-checklist.md](references/publish-checklist.md)。

## 四、交付

用户只要文章就交 Markdown；要发布包再给 HTML、纯文本、预览与封面。本技能只交付成稿与发布包，由用户在编辑器确认发布。
