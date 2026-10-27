# topmind-revise · 改稿与质检

[English](./README.en.md) | 中文

按用户目标选择局部、结构或全面改写，核对事实与作者声音。

## 使用

```bash
npx @topmindspace/topmind-writing-skills install topmind-revise
```

安装后直接告诉 agent 你要的结果、读者和已有材料；明确要一稿就直接给成品，探索任务再比较方向。完整能力、流程与脚本说明见 [SKILL.md](./SKILL.md)。

按需知识包随技能独立安装。需要方向、完整示例或经验时，见 [知识使用与增补](./references/knowledge-library.md) 与 [知识导航](./knowledge/README.md)；先读摘要再选卡片。可向指定私有包新增候选，不自动改长期规则。

## 方法与样张

[创作方法与样张](./references/creative-practice.md) 给同素材不同写法和看参考的方法。模板、口吻、篇幅、emoji 与视觉风格是选项；事实准确、授权、隐私与输出完整性继续核对。当前用户要求和作者样本优先。

## 常用脚本

在本技能目录运行；示例文件名替换为实际路径：

```bash
python3 scripts/revise_check.py 改前.md 改后.md --report 改稿报告.md
```

对照原稿与改稿核对数字、实体、引用和确定性。句式提示用于定位问题，不能判断作者身份或替代编辑判断。

## 交付

交付修订稿；按需附修改理由或审查意见，不强制长报告。 由用户完成对外发布。

MIT License。仓库维护、安装选项与版本说明见 [合集说明](https://github.com/topmindspace/topmind-writing-skills)。
