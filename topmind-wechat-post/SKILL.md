---
name: topmind-wechat-post
description: "创作、整理和排版公众号文章；支持工具/插件推荐结构、产品实测评测、深度解读与叙事随笔，从选题或底稿到 Markdown，按需导出内联 HTML、预览与上传清单。公众号短文用 topmind-briefs，独立改稿用 topmind-revise。"
license: MIT
metadata:
  version: "0.3.25"
  action_category: "write"
  triggers: "公众号, 写公众号, 微信排版, 公众号排版, 公众号稿, 公众号长文, 插件推荐公众号, 工具介绍文章, 排版这篇文章, 定稿, 发公众号, 公众号交付, wechat, mp format, 写公众号文章, 公众号排版定稿, 公众号发布清单"
  author: "TopMindSpace"
  homepage: "https://github.com/topmindspace/topmind-writing-skills#readme"
  updated: "2026-11-15"
---

# topmind-wechat-post · 公众号深度文章与排版交付

从选题、底稿到可直接使用的公众号 Markdown 与 HTML 发布包。默认中文，当前用户的目标、作者样本和篇幅要求优先。

## 一、按文章体裁选结构（灵活匹配，不套死模板）

动笔或整理底稿前，先根据题材选择最适合读者的主线（详见 [information-design.md](references/information-design.md) 与知识卡 `wechat-plugin-and-review`）：

| 文章体裁 | 推荐结构与写法要点 | 边界与避坑 |
|---|---|---|
| **1. 工具 / 插件介绍推荐文（可选专项结构）** | **标题直接点名插件/工具** → **开头直给解决什么痛点与安装方式**（命令/链接前置） → **全景功能列表** → **每个小标题配简短例子 + 真实截图** | **仅适用于工具/插件推荐文**；简单直观的功能展示清楚例子和截图即可，**不要长篇大论讲道理或拔高行业意义** |
| **2. 产品实测 / 模型评测文** | 核心体感结论前置 → 按具体观察维度（如延迟、打断、准确率、账单）分节展示实测 → 真实优缺点与选型建议 | **完整保留作者个人褒贬与实测数据**；哪怕外部都在「吹爆」，也按具体维度客观展开，不洗成「各有千秋」的和稀泥套话 |
| **3. 规则变化 / 技术机制深解** | 通俗定位变化核心 → 拆解底层机制或开源代码参数 → 区分「代码/实验数据」与「实际体感」 → 给读者的具体建议 | 保留作者有温度的个人判断（「仔细聊了一轮，我倒觉得……」），同时守住事实边界，不写成确定性定律 |
| **4. 叙事随笔 / 行业观察** | 具体场景或反常细节切入 → 展开前因后果与人物动作 → 留有余味的落点 | 不代编作者未提供的第一人称亲历；做删尾测试，砍掉说教升华尾巴 |

需要检索体裁卡片或沉淀新经验时，见 [knowledge-library.md](references/knowledge-library.md) 与 [creative-practice.md](references/creative-practice.md)。

## 二、高信噪比图文配合与诚实标注

公众号文章支持完整配图、代码块与参考链接（不受 X 短帖「无 URL」习惯限制）：
1. **一图讲清变化、边界与建议**：制作总结卡或信息图时，把主要变化、事实边界与作者建议放在一张图里讲明白；将**「客观证据（代码参数/论文原文）」与「作者建议」在视觉上明確分区**。
2. **原文截图高亮 + 保留上下文，绝不伪造原页**：引用论文、文档或开源代码时，用真实原图高亮关键行并保留上下两行上下文，**严禁自己排版伪造一张看似论文原页或官方网页的假截图**。
3. **诚实标注图片性质**：概念封面或生成图涉及功能表现时标明 `功能示意，不是实拍`；使用旧版界面或演示数据时在图注标明「示例数据 / 版本示意」（不在图内硬塞大段免责文字）；学术技术图表保持干净克制，不贴卡通吉祥物 logo。详见 [image-sourcing.md](references/image-sourcing.md)。

## 三、单源文件结构与 HTML 导出

沿用已有工作区；纯聊天写稿直接交付 Markdown。需要完整发布包时，可建立单源文章目录（详见 [platform-operations.md](references/platform-operations.md) 与 [workspace.md](references/workspace.md)）：

```bash
python3 scripts/article_scaffold.py --title "文章名" --base <已确认目录>
python3 scripts/md2wechat.py --input <文章目录>/<文章名>.md --embed-images --preview
python3 scripts/check_article.py <文章目录>
```

- 主题可通过 `scripts/md2wechat.py --list-themes` 与 [theme-map.md](references/theme-map.md) 选择；内联样式与微信后台约束见 [wechat-constraints.md](references/wechat-constraints.md) 与 [element-spec.md](references/element-spec.md)。
- 导出后实际打开 HTML 或预览检查图序、图注、列表与表格；文字修改先回源稿 `.md` 再重新导出。
- 去 AI 味与成稿自查参考 [core-voice.md](references/core-voice.md)、[de-ai-rules.md](references/de-ai-rules.md) 与 [revision-workflow.md](references/revision-workflow.md)；脚本提示（W/H/I）仅作复查线索，**不要求清零，不作为定稿门禁**。

## 四、交付

默认交付 Markdown；需要发布包时一并交付内联 HTML、预览与图片上传清单。封面可组合 `topmind-cover`（公众号宽图 900×383 与方图 900×900 见 [platform-cover-specs.md](references/platform-cover-specs.md)）。更多细节见 [research-mode.md](references/research-mode.md)、[workflow.md](references/workflow.md)、[known-pits.md](references/known-pits.md)、[case-notes.md](references/case-notes.md)。只负责生成稿件与发布包，不自动执行对外发布。
