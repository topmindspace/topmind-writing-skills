# topmind-cover · 文章封面

[English](./README.en.md) | 中文

看实际参考与风格样张，选择摄影、字体、极简、场景等方向，核字与裁切。

## 使用

```bash
npx @topmindspace/topmind-writing-skills install topmind-cover
```

安装后直接告诉 agent 你要的结果、读者和已有材料；明确要一稿就直接给成品，探索任务再比较方向。完整能力、流程与脚本说明见 [SKILL.md](./SKILL.md)。

## 方法与样张

[创作方法与样张](./references/creative-practice.md) 给同素材不同写法和看参考的方法。模板、口吻、篇幅、emoji 与视觉风格是选项；事实准确、授权、隐私与输出完整性继续核对。当前用户要求和作者样本优先。

## 常用脚本

在本技能目录运行；示例文件名替换为实际路径：

```bash
python3 scripts/crop-cover.py 主图.png --out-dir 输出目录
```

风格提示按上下文判断，不要求警告清零或达到词面分数；平台与目录协议在采用相关导出工具时核对。生成预览需当前环境具备相应浏览器与依赖，未验证时如实说明。

## 交付

交当前请求所需的文本或文件，说明重要取舍和未核实项。需要图片、HTML 或完整报告时再扩展对应环节；本技能不执行对外发布。

MIT License。仓库维护、安装选项与版本说明见 [合集说明](https://github.com/topmindspace/topmind-writing-skills)。
