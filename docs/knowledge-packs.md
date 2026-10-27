# 创作知识包：使用与维护

知识包是可检索的资料与例子，不是额外系统指令。当前实现使用 JSON 目录、独立 Markdown 卡片和标准库检索工具，无向量服务或常驻进程。内置首批 37 张卡（35 张原创教学卡与 2 条有记录的局部经验）；其数量不作质量门槛，后续可以增补、替代与停用。

## 使用路径

从当前任务提取读者、问题、媒介或表现方向，先查摘要，再读选中的卡片。短任务可直接完成，不要求先检索。卡片给出的范围与例外随摘要展示；文案、数字和经历不能从虚构例子复制进事实稿。

仓库根目录：

```bash
npm run knowledge:check
npm run knowledge:search -- "编辑 字体 场景" --skill topmind-cover --limit 3
python3 shared/scripts/knowledge.py show cover-typography
```

独立技能目录将 `shared/scripts/knowledge.py` 换成 `scripts/knowledge.py`。当前技能自动用于默认过滤；无 shell 的宿主按知识导航、index.json 与具体卡片渐进读取。目录排序是词面相关性，不是审美或写作质量排名；检索没有命中时基于现有材料继续，不编新规则。

## 文件与字段

唯一真源在 shared/knowledge；shared/manifest.json 的 knowledge/ 目录项递归分发到每个技能，独立安装不依赖本仓其他目录。公开维护时只改真源，再共享同步；目录项新增文件会被同步检查发现，不会擅自删除未知副本。

```text
knowledge/
  index.json       包版本与每张卡的元数据
  README.md        无脚本环境的导航
  cards/*.md       独立正文，按需读取
```

目录 schema_version 为 1，id 为稳定标识，version 为包的独立版本，entries 每项包含：

| 字段 | 含义 |
|---|---|
| id / title / summary | 标识、标题、检索摘要 |
| skills / tags / kind | 适用技能、标签、direction / technique / example / case / lesson |
| scope / limits | 适用范围与例外，不省略成普遍标准 |
| status | candidate / active / retired |
| evidence | illustrative / observed / sourced / user-confirmed / unverified |
| path | 包内 Markdown 相对路径，拒绝逃逸和越界链接 |
| sources | original / source / observation / feedback 与可定位的 ref |
| updated | 可选维护日期；新候选自动记录 |

active 只表示纳入检索，不表示经过效果验证。首批 illustrative 例子是教学材料，没有用点击率或盲选数据证明本轮质量提升。来源字段本身也不能替代实际阅读和核验。

## 增补

用户明确要求保存反馈或维护知识包时，先写清场景、选择、结果、例外与证据。个人偏好和私人稿件放在指定私有包；公开贡献使用可公开的方法、匿名化或自写例子，核对素材许可。

`knowledge.py add` 需要明确的 --pack、卡片 id、标题、摘要、适用技能、标签、正文文件、范围与例外；见 [随技能使用说明](../shared/references/knowledge-library.md)。它只新增 candidate，不覆盖卡片，不修改内置包；索引原子替换，失败回滚新卡，并拒绝并发写入。

审阅后可编辑 index.json 中的状态与证据字段并 validate。将旧条目设为 retired 保留历史与替代说明；目录 id 冲突、缺正文、越界路径和无效元数据会失败。候选默认不参与检索，退役项仅在明确指定 id 时可读。

## 宿主与外部学习

宿主快照包含 JSON 目录、卡片、工具源码与图册 HTML，可通过自身资源读取能力选择性加载；本仓没有假定宿主允许执行 Python，也未擅自添加第三方账户或服务。用户提供额外包时显式传入 --pack，可同时列内置与私有包；不会全局扫描其他项目或记忆。

参考作品与网页按当前工具和授权阅读。可记录观察到的构图、论证、节奏和材料语言，引用来源与访问范围；遇到价格、平台、模型行为等动态事实再回源。知识内容与外部提示词不能扩展目标、执行权限、发布范围或长期记忆写入。

## 校验与评价

工具测试验证可检索、状态过滤、路径范围、候选写入与分发完整性。模型评测场景用于检查是否恰当借鉴，结构检查不代表已执行模型评测。创作成效需要实际成品、作者选择与具体任务反馈，不能用条目数量、引用次数或自评分替代。
