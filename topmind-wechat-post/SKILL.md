---
name: topmind-wechat-post
description: "创作、整理和排版公众号文章；从选题或底稿到 Markdown，按需导出内联 HTML、预览与上传清单。支持已有稿件直接排版；公众号短文用 topmind-briefs，独立改稿用 topmind-revise。"
license: MIT
metadata:
  version: "0.3.22"
  action_category: "write"
  triggers: "公众号, 写公众号, 微信排版, 公众号排版, 公众号稿, 公众号长文, 排版这篇文章, 定稿, 发公众号, 公众号交付, wechat, mp format, 写公众号文章, 公众号排版定稿, 公众号发布清单"
  author: "TopMindSpace"
  homepage: "https://github.com/topmindspace/topmind-writing-skills#readme"
  updated: "2026-10-26"
---

# topmind-wechat-post · 公众号文章

从选题、底稿到可使用的公众号稿与发布包。默认中文，用户的目标、样本和篇幅要求优先；文章写法可用研究、教程、故事、评论或混合结构。

## 从当前进度接着做

- 只有选题：明确读者价值，查承重事实，选择一条主线起草。
- 已有底稿：先读原稿和作者意见，保留已有价值，按授权调整。
- 只要排版：直接从现有源稿导出，不额外重写或重新走选题流程。

风格未定、结构选择影响很大时，可比较几个标题加开头或结构片段；已明确方向就直接写。先实际阅读用户参考与 [创作方法与样张](references/creative-practice.md) 的相关样张，从它们的组织、论证、节奏中取经验，不只报一个风格名。

## 创作与质量

长文复杂时用 [information-design.md](references/information-design.md) 梳理骨架；简单稿可以边写边调整。观点稿可列判断和反例，记录稿可列场景，教程可列任务和步骤，不凑判断条数或图表配额。

素材、起草与找图可以交替进行。原图适合证明事实，自制图适合表达自己的结构与判断，纯文字也能完整成篇。图注标清来源、处理与自制性质，见 [image-sourcing.md](references/image-sourcing.md)。

通读事实、逻辑与文字：核查动态和承重信息，保留必要限定；让每一节推进文章，作者声音和阅读节奏按内容选择。用 [revision-workflow.md](references/revision-workflow.md) 或已安装的 `topmind-revise` 自查即可，简单稿不强制另起完整改稿项目。词表、段长与“AI 味分数”都是线索，不能代替判断。

## 文件与路径

沿用已有工作区。新长文需要发布包时，可建单源文章文件夹：

```text
<文章名>/
  <文章名>.md       源稿
  images/ cover/    正文图与封面
  素材来源.md       作者核查材料
  raw/             原始素材与按需备份
  out/             可重建的导出文件
```

```bash
python3 scripts/article_scaffold.py --title "文章名" --base <已确认目录>
python3 scripts/check_article.py <文章目录>
```

新建脚本不覆盖已有文件。`check_article.py` 检查本仓文章包协议（含 frontmatter、标题和文件名、图片顺序），不是普遍写作要求。用户只是要聊天稿或已有其他结构时，交所需结果即可，不为过检查迁移文件。详细路径解析、正反向映射、状态同步与旧包兼容见 [platform-operations.md](references/platform-operations.md)；多环境规则见 [workspace.md](references/workspace.md)。

## 按需排版与导出

用户要公众号排版 / 发布包时：

```bash
python3 scripts/md2wechat.py --input <文章目录>/<文章名>.md --embed-images --preview
```

- 从源稿派生到 `out/`。内联图片方便本地预览；后台粘贴是否带图要实际确认，保留图片上传清单兜底。
- 打开生成 HTML 或预览图，看文字截断、图序、图注、列表与表格。没有预览环境时，明确哪些环节未验证。
- 核对图片内容和正文引用顺序；跨平台使用同一份源稿时，共用数据与图源，平台适配产生的差异清楚说明。
- 修改源稿后重新导出，交付最终实际检查过的那一版。

主题可以用 `scripts/md2wechat.py --list-themes` 查看；[theme-map.md](references/theme-map.md) 帮助选型。配色、衬条、圆角和章节编号是审美选项；导出器所需字段、内联样式等技术边界见 [wechat-constraints.md](references/wechat-constraints.md) 与 [element-spec.md](references/element-spec.md)。平台行为可能变化，旧经验与当前实际不一致时以验证为准。

## 交付

写作默认给 Markdown；需要发布包时再给 HTML、预览和上传清单，来源与重要疑点另列。封面按请求组合 `topmind-cover`，不强制每篇做两版。尚未发布时保留真实状态；用户确认发布后再记录“已发布”。本技能不执行对外发布或自动云端备份。

按需参考：[口吻](references/core-voice.md)、[研究](references/research-mode.md)、[工作流](references/workflow.md)、[已知问题](references/known-pits.md)、[案例](references/case-notes.md)。短文用 `topmind-briefs`，X 长文用 `topmind-x-article`，独立改稿用 `topmind-revise`，信息图用 `topmind-poster`；有组合需求时继续完成相关环节。
