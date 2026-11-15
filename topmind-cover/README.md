# topmind-cover · 文章与多平台封面设计

[English](./README.en.md) | 中文

结合当代高辨识度封面趋势（Swiss 大字与数字反差、Bento 模块化信息卡、原文高光证据拼贴、微距工业材质、手绘白板拆解等），为公众号、X、小红书与抖音设计一眼抓人的封面，并精准适配各平台尺寸。

## 安装与使用

```bash
npx @topmindspace/topmind-writing-skills install topmind-cover
```

安装后直接告诉 Agent 你的文章主题、目标平台和手头已有的素材（如论文截图、实测数据或参考图）。完整设计心法、五大视觉流派与工作流见 [SKILL.md](./SKILL.md)。

按需知识包随技能独立安装。检索视觉方向或沉淀新经验见 [知识使用说明](./references/knowledge-library.md) 与 [知识导航](./knowledge/README.md)。

## 核心参考与样张图册

- [封面视觉方向库 (cover-styles.md)](./references/cover-styles.md)：5 大当代封面趋势与 22 个风格起点
- [高表现力提示词指南 (cover-prompts.md)](./references/cover-prompts.md)：区分「字图一体直出」与「留白底图+脚本叠字」双路径，提供 12 组精炼提示词范本
- [构图动线 (cover-patterns.md)](./references/cover-patterns.md) & [跨媒介组合 (cover-combos.md)](./references/cover-combos.md)：16 种视觉重心法则与 24 组媒介配色配方
- [全平台封面尺寸指南 (platform-cover-specs.md)](./references/platform-cover-specs.md)：公众号、X、小红书、抖音/视频号尺寸速查与安全区法则
- [交互版式图册 (creative-atlas.html)](./assets/examples/creative-atlas.html) & [样张说明](./assets/examples/README.md)：可切换横竖比例的 HTML/CSS 版式研究与历史样张总览

## 多平台裁切与叠字工具

在本技能目录运行（需 Pillow；`title-engine.py` 另需 NumPy）：

```bash
# 默认导出 X Article (1500×600) 与公众号宽图 (900×383)
python3 scripts/crop-cover.py 主图.png --out-dir 输出目录

# 公众号宽图 (900×383) + 转发方图 (900×900) 独立裁切
python3 scripts/crop-cover.py 原图.png --preset wechat --anchor center --out-dir 输出目录

# X 短帖单图 (1200×675) / 小红书与抖音 3:4 竖图 (1080×1440)
python3 scripts/crop-cover.py 主图.png --preset x-post --out-dir 输出目录
python3 scripts/crop-cover.py 竖版主图.png --preset xiaohongshu --out-dir 输出目录

# 横版一图双投 (16:9 1920×1080 + 中央 4:3 1080×810)
python3 scripts/crop-cover.py 横版母图.png --preset landscape-pair --out-dir 输出目录

# 竖版一图双投 (9:16 1080×1920 + 中央 3:4 1080×1440)
python3 scripts/crop-cover.py 竖版母图.png --preset vertical-pair --out-dir 输出目录
```

可用 `python3 scripts/title-engine.py --list-fonts` 查看本机可用中文字体与字重。每张封面交付前均在实际缩略图尺寸下核对文字、数据与裁切完整性；概念功能图诚实标注 `功能示意，不是实拍`。

MIT License。仓库维护、安装选项与版本说明见 [合集说明](https://github.com/topmindspace/topmind-writing-skills)。
