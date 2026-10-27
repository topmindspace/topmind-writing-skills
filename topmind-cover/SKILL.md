---
name: topmind-cover
description: "设计文章封面、头图和缩略图，适配小红书图文、抖音图文、公众号、X Article 与短帖；按发布形态、真实参考和主题完成构图、成图、核字与裁切。密集信息图用 topmind-poster。"
license: MIT
metadata:
  version: "0.5.0"
  action_category: "write"
  triggers: "封面, 封面图, 小红书封面, 抖音封面, 图文封面, X 短文封面, 短帖封面, 头图, 题图, 首图, 封面配图, 缩略图, banner, cover, thumbnail, 公众号封面, 公众号题图, 公众号头图, X 封面, X 首图, X 长文头图, 文章封面, 封面风格"
  author: "TopMindSpace"
  homepage: "https://github.com/topmindspace/topmind-writing-skills#readme"
  updated: "2026-10-27"
---

# topmind-cover · 文章封面

让封面传达文章主题，在实际展示尺寸下有辨识度、文字可读、裁切完整。默认中文；用户已有品牌、参考和风格要求优先。

## 按需借鉴与积累

需要新方向、完整例子或相关经验时，用 [知识使用与增补](references/knowledge-library.md) 检索字体、场景、摄影、编辑、材料与系列设计；先读摘要，再选相关卡片。可以混合、改造或采用库外思路，简单任务直接完成。知识不替代当前用户要求；新反馈先作为有范围的候选，不自动改长期规则。

## 先看参考，再决定画法

读文章或摘要，抓住这次想传达的重点。用户给了参考就实际查看图片；没给时，从 `assets/examples/overview.png`、可打开的 `assets/examples/creative-atlas.html` 或本地单风格样张开始看。样张未安装可用总览和文字配方继续，说明实际看过哪些材料。

[cover-styles.md](references/cover-styles.md) 的 22 种风格是素材库；MD3、浅色、角色互动只是其中一些选项。可以用摄影、纯文字、极简、深色、线稿、拼贴或原创组合。原图承载事实时可以用原图，封面需要独立表达时也可以另设计。

风格明确直接做；需要探索时，给少量差别明显的缩略图或完成稿，比较构图、信息重心、字与图的关系，而不是只报风格名字。用户要一张就推荐并完成一张，不因存在多种可能反复追问。生成调用次数按任务规模与用户预算安排。

## 可用方向

| 方向 | 主体与标题关系 | 常见适用 |
|---|---|---|
| 字体主导 | 文字本身构成画面，纯色底也成立 | 评论、宣言、人文 |
| 摄影 / 原图 | 裁切、负空间与文字呼应 | 人物、产品、生活 |
| 编辑拼贴 | 多种真实素材形成清楚层级 | 资讯、复盘、合集 |
| 场景叙事 | 动作、隐喻或角色与标题互动 | 趣味教程、品牌故事 |
| 抽象 / 图形 | 形状、尺度、颜色表达主题 | 科技、研究、概念 |

选型与样张方法见 [creative-practice.md](references/creative-practice.md)。需要场景时读 [scene-builder.md](references/scene-builder.md)，字效看 [typography-system.md](references/typography-system.md)，构图与配方看 [cover-patterns.md](references/cover-patterns.md) / [cover-combos.md](references/cover-combos.md)。只加载所选方向需要的章节，不把每份配方累加到一张图。

## 平台、尺寸与出字

先确定发布形态：图文笔记、普通图文、商城内容、公众号普通文章与图片消息分别处理。相关场景的依据、来源、核验日期和待实测项见 [平台封面参考](references/platform-cover-specs.md)，按当前用途读取。以下为本包导出预设，平台要求或用户规格不同时按实际调整：

| 用途 | 常用尺寸 |
|---|---|
| X Article | 1500×600，5:2 |
| 公众号 | 900×383 |
| X 短帖 | 1200×675，16:9 |
| 小红书图文 | 1080×1440，3:4；比例有场景化官方建议，像素为本包选择 |
| 抖音普通图文 | 1080×1440，3:4；本包起点，需核对实际发布入口 |
| 公众号方图 | 900×900，1:1；本包高清预设，分别检查小图展示 |

系列多版可复用素材、字体与色彩；横竖版分别布局，需要时才裁切。宽图、方图直接从原图分别裁切并检查；裁切会损伤标题或主体时重新布局。标题长短、安全边距和字号由画幅、字体、缩略图可读性决定，不为字数阈值改坏意思；不把未经验证的占屏比例、遮挡区域或点击率写成平台规则。

可整张生成，也可生成场景后用 `scripts/title-engine.py` 或 `scripts/overlay-title.py` 叠字；纯文字封面可直接排版。文字多、生僻字或需要反复改字时，叠字可以从一开始采用。使用当前环境实际提供的生图工具，不假定某个固定 API 存在。完整 prompt 见 [cover-prompts.md](references/cover-prompts.md)，按当前方案删改槽位。

## 核对与交付

出图后实际看图，核对每个字、数字、归属、主题、缩略图可读性和各尺寸裁切。设计维度用于诊断，不用自评分数证明质量，不因纯色底、没有人物或道具少而重做。发现问题先局部修正；多次尝试无改善时换路径或说明具体限制，迭代次数与成本相称。

事实图、logo、产品截图来自真实素材；生成示意与摄影原图分清。参考可借构图原理、配色关系与叙事方法，独特标识和素材按许可使用，表达服务当前文章。

```bash
python3 scripts/crop-cover.py <主图> --out-dir <交付目录>
python3 scripts/crop-cover.py <主图> --preset x-post --out-dir <交付目录>
python3 scripts/crop-cover.py <竖版主图> --preset xiaohongshu --out-dir <交付目录>
python3 scripts/crop-cover.py <竖版主图> --preset douyin --out-dir <交付目录>
python3 scripts/crop-cover.py <原图> --preset wechat --anchor left --out-dir <交付目录>
```

默认 `article` 保持原有 X / 公众号双横图输出；`wechat` 单独输出公众号宽图与方图。`--anchor` 可选 center / left / right / top / bottom，只调整裁切位置；输出后逐版看图。无后台访问时说明尚未验证平台实际展示，文件格式与大小上限以当前入口为准。

交付实际成图和所需尺寸，必要时附一句方案差异。文件名沿用现有发布包；封面缺稿名时用可辨认名称，不猜个人路径。若标题工具的固定模板检查不适合设计，可调整 spec 或换直接排版路径，最终以实际可读性和裁切验证。

信息密集、逐字逐数准确的图交 `topmind-poster`；文字写作分别用 `topmind-briefs` / `topmind-viral-posts` / 长文技能。本技能完成封面，不执行发布。
