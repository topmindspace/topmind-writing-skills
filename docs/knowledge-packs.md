# 创作知识包：检索、使用与扩展指南

知识包（Knowledge Pack）是随技能分发的**可检索经验、策略与实战卡片库**，采用轻量 JSON 索引（`index.json`）、独立 Markdown 卡片（`cards/*.md`）与零外部依赖的标准库检索脚本（`knowledge.py`）实现。当前内置 `v1.1.0` 共 **45 张卡片**，覆盖去 AI 味四大生成机制、平视同行视角、短文价值优先与新闻动态转化、爆款互动机制、改稿经验反哺、公众号插件审校、封面五大趋势与诚实标注等核心领域。

---

## 一、检索与使用路径

遇到复杂选题、跨平台改写或封面视觉探索时，先按关键词检索摘要，再按需读取命中的卡片正文；简单明确的任务可直接执行，无需强制检索。

```bash
# 校验知识包结构与卡片完整性
npm run knowledge:check

# 按技能与关键词检索相关卡片摘要
npm run knowledge:search -- "去AI味 连接词 升华" --skill topmind-revise --limit 3
npm run knowledge:search -- "编辑 字体 证据" --skill topmind-cover --limit 3

# 查看单张卡片完整内容
python3 shared/scripts/knowledge.py show de-ai-mechanisms
```

在独立安装的单个技能目录中，将 `shared/scripts/knowledge.py` 替换为 `scripts/knowledge.py` 即可；无 shell 执行环境的宿主可直接按 [knowledge/README.md](../shared/knowledge/README.md) 与 `index.json` 渐进读取。

---

## 二、目录结构与元数据规范

唯一真源位于 `shared/knowledge/`，通过 `shared/manifest.json` 自动同步到全部 8 个技能目录，保证单技能独立安装时完整可用：

```text
knowledge/
├── index.json       # 包版本与卡片元数据索引 (schema_version: 1)
├── README.md        # 按领域分组的快速导航表
└── cards/*.md       # 独立经验卡片正文，按需读取
```

每条索引记录包含以下字段：

| 字段 | 说明 |
|---|---|
| `id` / `title` / `summary` | 稳定标识、标题、检索摘要 |
| `skills` / `tags` / `kind` | 适用技能（支持 `"*"`）、检索标签、类型（`direction` / `technique` / `example` / `case` / `lesson`） |
| `scope` / `limits` | 适用场景与例外边界（防止将局部经验当成死板门禁） |
| `status` | `candidate`（待审候选）/ `active`（默认可检索）/ `retired`（退役保留） |
| `evidence` | `illustrative` / `observed` / `sourced` / `user-confirmed` / `unverified` |
| `path` / `sources` / `updated` | 包内相对路径、来源说明与更新日期 |

---

## 三、如何沉淀与扩展新经验

当用户在创作或改稿过程中提出新的思考、策略或纠偏经验并希望沉淀下来时：

1. **记录进作者私有包（默认安全路径）**：
   使用 `knowledge.py add` 将经验按「场景 — 选择 — 原因 — 例外」写入指定的本地知识包（自动标记为 `candidate`，原子写入且不污染内置公共包）：
   ```bash
   python3 scripts/knowledge.py add \
     --pack ./my-knowledge \
     --id my-new-insight \
     --title "经验标题" \
     --summary "一句话核心动作与价值" \
     --skills topmind-briefs,topmind-revise \
     --tags "标签1,标签2" \
     --scope "适用场景" \
     --limits "例外情况" \
     --body ./insight-note.md
   ```
2. **升级内置公共包（仓库维护者）**：
   在 `shared/knowledge/cards/` 下编写通用化脱敏后的 Markdown 卡片，登记到 `shared/knowledge/index.json` 与 `shared/knowledge/README.md`，然后运行 `npm run sync:shared` 与 `npm run knowledge:check`。
