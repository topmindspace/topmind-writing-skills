# topmind-revise · 改稿、去 AI 味与经验沉淀

[English](./README.en.md) | 中文

用**「这句话是在完成一项写作任务，还是在跟朋友说话？」**诊断原稿，砍掉通稿负担与 AI 任务腔，核对事实边界，保留作者真实口吻与个人褒贬。支持长文、短帖、评论回复、标题打磨及改稿复盘沉淀。

## 核心特点

- **去 AI 味八大机制诊断**：精准清除「替读者把话讲完、自我解释元话语、新闻通报腔、说教收尾与金句包圆、凑排比与套类比、强制情绪妆、堆参数显专业、讲师命令腔」。
- **保留真人温度与真实褒贬**：减弱缺乏实证的绝对因果，但**绝不把作者有温度的主观判断（「仔细聊了一轮，我倒觉得……」或鲜明优缺点实测）洗成冰冷和稀泥的官方综述**。
- **向作者改稿学习（Scope Tagging）**：支持对比作者修改前后的定稿，拆解「删了什么负担、补了什么支点」，按体裁标注适用范围并写入知识包（见 `revise-learn-from-edits` 与 `de-ai-mechanisms`）。
- **事实与引语保真**：配合 `revise_check.py` 与 `audit-provenance.py` 核对数字、引语、专有名词与段落溯源，严禁为凑人味代编第一人称「我」。

## 安装与使用

```bash
npx @topmindspace/topmind-writing-skills install topmind-revise
```

完整原则、4 种模式（`audit` / `revise` / `quick` / `learn`）见 [SKILL.md](./SKILL.md)，长短文改前改后实战对照见 [examples/README.md](./examples/README.md)，按需知识包见 [knowledge/README.md](./knowledge/README.md)。

## 常用脚本

```bash
python3 scripts/de_ai_lint.py 稿子.md
python3 scripts/revise_check.py 改前.md 改后.md --report 改稿报告.md
python3 scripts/audit-provenance.py --draft 改后.md --source 源稿.md
```

脚本提示仅用于辅助定位问题，不要求警告清零，也不替代编辑判断。只负责改稿与审校，由用户完成对外发布。

MIT License。仓库维护与合集说明见 [topmind-writing-skills](https://github.com/topmindspace/topmind-writing-skills)。
