# topmind-cover · 文章封面

[English](./README.en.md) | 中文

看实际参考与风格样张，选择摄影、字体、极简、场景等方向，核字与裁切。

适配小红书图文、抖音普通图文、公众号文章和 X。先确定发布形态，平台依据与导出预设分开处理；[平台封面参考](./references/platform-cover-specs.md) 记录来源、核验日期与未实测项。公众号图片消息、抖音商城和商品主图需分别确认，不能照搬普通图文规则。

## 使用

```bash
npx @topmindspace/topmind-writing-skills install topmind-cover
```

安装后直接告诉 agent 你要的结果、读者和已有材料；明确要一稿就直接给成品，探索任务再比较方向。完整能力、流程与脚本说明见 [SKILL.md](./SKILL.md)。

按需知识包随技能独立安装。需要方向、完整示例或经验时，见 [知识使用与增补](./references/knowledge-library.md) 与 [知识导航](./knowledge/README.md)；先读摘要再选卡片。可向指定私有包新增候选，不自动改长期规则。

## 方法与样张

[创作方法与样张](./references/creative-practice.md) 给同素材不同写法和看参考的方法。模板、口吻、篇幅、emoji 与视觉风格是选项；事实准确、授权、隐私与输出完整性继续核对。当前用户要求和作者样本优先。


[版式图册](./assets/examples/creative-atlas.html) 提供 8 组可切换横竖比例的 HTML/CSS 研究；[样张目录](./assets/examples/README.md) 说明 PNG、标题 spec 和分发差异。

## 常用脚本

在本技能目录运行；示例文件名替换为实际路径：

```bash
python3 scripts/crop-cover.py 主图.png --out-dir 输出目录
python3 scripts/crop-cover.py 竖版主图.png --preset xiaohongshu --out-dir 输出目录
python3 scripts/crop-cover.py 竖版主图.png --preset douyin --out-dir 输出目录
python3 scripts/crop-cover.py 原图.png --preset wechat --anchor left --out-dir 输出目录
```

默认 `article` 输出 1500×600 与 900×383 双横图；`x-post` 输出 1200×675；`xiaohongshu` / `douyin` 输出 1080×1440；`wechat` 输出 900×383 与 900×900。以上是本包预设，按当前发布入口与用户规格调整。`--anchor` 支持 center / left / right / top / bottom。每张直接从原图等比裁切，不能替代横竖版重新构图；标题或主体被切时重排，上传前逐版预览。脚本不会覆盖输入原图。

裁切需 Pillow；标题工具还需 NumPy。字体、字号和装饰提示用于设计判断，结构错误仍需修复。最终逐版核字、看图与检查裁切。

## 交付

交付封面成图与所需尺寸；有可编辑源文件时一并提供，说明重排和裁切取舍。 由用户完成对外发布。

MIT License。仓库维护、安装选项与版本说明见 [合集说明](https://github.com/topmindspace/topmind-writing-skills)。
