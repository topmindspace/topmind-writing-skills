# topmind-cover · 封面配图生成

[English](./README.en.md) | 中文

为 X 长文和公众号文章生成封面图的可复用技能。目标：**震撼、醒目、主题突出**。

- 版本：**v0.4.17**

你可以这样说：「做个封面」「公众号头图」「X 长文头图」「X 短文封面」。

## 风格样张

<p align="center">
  <img src="https://github.com/topmindspace/topmind-writing-skills/raw/main/topmind-cover/assets/examples/overview.png" alt="topmind-cover · 22 封面风格总览" width="960" />
</p>

22 种风格（**白色清新**（主风格，4 种版式：单行居中 / 双行标题 / 左文右图 / 点题词高亮）/ 背景虚化 / 纸感拼贴 / 资讯快报 / 巨字宣言 / 教程步骤 / 极简留白 / 杂志编辑 / 3D萌系潮玩 / 日系动漫 / 微缩立体书 / 学院版画 / 样张矩阵 / 暗色SaaS / 电影科技流 / 硬核立体字 / 爆款干货 / 品牌发布 / IP 趣味 / 橙色暖阳 / 卡通素描 / 赛博霓虹，浅色优先排序）：适用场景、配色故事、抽象设计原则、中英 prompt 配方见 [`references/cover-styles.md`](./references/cover-styles.md)；单风格大图在 [`assets/examples/`](./assets/examples/)；白色清新 4 版式总览见 [`assets/examples/white-clean-showcase.png`](./assets/examples/white-clean-showcase.png)。想自己写提示词直接给 AI 生图（不走技能流程），看 [`references/cover-prompts.md`](./references/cover-prompts.md)（可直接拷贝的提示词大全 + 全平台爆款流派调研）。

## 安装

```bash
npx @topmindspace/topmind-writing-skills install topmind-cover
```

## 用法

0. **选风格与组合**：按题材从 `references/cover-styles.md` 选主风格（22 选 1，浅色优先），再按 [`references/scene-builder.md`](./references/scene-builder.md) 第四节配一个辅风格；看示例图确认视觉语言。
1. **标题提炼**：先定标题文案（主标题 ≤ 8 字最稳，另配一行副标题），先跑 `scripts/check-title.py` 排除生僻字、繁体和形近字，用该风格章节的标题写法规范；不满意重写，不先画图。
2. **七层场景配方**：主题 → 隐喻 / 冲突 → 主角（可用 TopMind 小鸡 / 小猫 / 小植物 IP）→ 与标题互动的动作 → 2–4 个道具 → ≥3 层背景 → 光线；不画可识别的真实人物。
3. **默认出 2–3 个方案**：方案卡 `方案 A｜隐喻｜风格：主 + 辅｜骨架：L1–L10｜配色`，四项至少换三项；相邻封面不重复主风格。
4. **整张生成**：从 [`references/cover-patterns.md`](./references/cover-patterns.md) 选范式（X1–X16），或直接用 [`references/cover-combos.md`](./references/cover-combos.md) 的 22 个命名组合，把标题原文、字的材质与立体方式、与场景一致的光照、层级、对齐和留白写进英文 prompt，让模型把字和场景一起画出来。出图后按 [`design-system.md`](./references/design-system.md) 第九节逐字核对：错 1–2 个字就局部修正，错得多就整张重出（最多 3 次），仍不对才兜底：场景图加 `scripts/title-engine.py` 叠字。
5. **评分与自检**（必做）：七项设计评分（层级清晰 / 可读性 / 对齐统一 / 色彩和谐 / 主题契合 / 焦点单一 / 细节品质）总分 ≥26 且无项 ≤2，再过 [SKILL.md 冲击力自检清单](./SKILL.md#冲击力自检清单)；不通过→改 prompt 重生成，最多 3 次，仍不过就换方案。
6. 裁剪落盘：

```bash
python3 scripts/crop-cover.py <主图> --out-dir <包>/images/
# 产出 00-封面.png (1500×600) + 00-封面-公众号.png (900×383，中央裁剪)

# X 短文 / 短帖封面：16:9 主图单独生成
python3 scripts/crop-cover.py <16:9 主图> --preset x-post --out-dir <目录>
# 产出 00-封面-X短文.png (1200×675)

# 整张生成前：标题风险检查（长度、生僻字、繁体、形近字）
python3 scripts/check-title.py "主标题" "副标题"

# 兜底：场景底图 + 多层叠字（--check 静态检查，--strict 查对比度与安全区）
python3 scripts/title-engine.py <场景图> <spec.json> --out <成图> --strict
# 快速单层叠字
python3 scripts/overlay-title.py <底图> <spec.json> --out <成图> [--font <字体>]
```

## 尺寸

| 平台 | 尺寸 | 比例 |
|------|------|------|
| X Article 封面 | 1500×600 | 5:2（主图） |
| 公众号封面大图 | 900×383 | 2.35:1（中央裁） |
| X 短文 / 短帖封面 | 1200×675 | 16:9（单独生成） |

## 设计原则

一图一主题；主体占画面 40%+；大标题 ≤10 字高对比；忌元素堆砌、小字密排、多主体打架。**安全区（硬约束）**：标题字与关键主体必须落在画面中央垂直 60% 安全区内。

## 开发

```bash
python3 scripts/package_skill.py --check
python3 scripts/negative_tests.py
```
