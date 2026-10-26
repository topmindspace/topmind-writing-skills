# 工作流 · 文章文件夹 · 状态机

## 生命周期

```text
forward:        底稿 notes/*.md → 审校改写 → 质量三关 → 定稿 → 排版 → 发布
reverse:        选题包 → 调研/素材 → 多轮改稿 → 质量三关 → 定稿 → 排版 → 发布 →（可选）回推
站外拉取 (ext):  在线精选站/转载整合 → 创作/整合 → 质量三关 → 定稿 → 排版 → 发布 →（可选）回推
```

`direction` 写在 frontmatter：`forward | reverse`。**站外拉取也用 `reverse` + `target_file: pending`**（站外源不进 `notes/`，`forward` 会因 `source_file` 校验失败）。

## 建文章文件夹

```bash
export TOPMIND_WORKSPACE=/path/to/ws
python3 scripts/new-article.py --title "中文标题" \
  [--base <专题目录>] [--date YYYY-MM-DD] [--tags AI,Agent] [--images a.png b.png] \
  [--direction forward --source-file notes/xxx.md]   # 对接 topstream 时
```

产出 `<文章名>/`：`<文章名>.md`（五项 frontmatter + H1）、`images/ cover/ raw/ out/`、`素材来源.md`。
文件夹已存在就报错，不覆盖。

**单源、按需派生**：默认只交付 `<文章名>.md`；用户说「公众号排版 / 公众号版」时跑 `md2wechat.py`，
说「出 X 版」时交给 `topmind-x-article`，产物都进 `out/`，是生成文件，不手改。改稿永远只改 `<文章名>.md`，改完重新派生。

**旧交付包**（`YYYY-MM-DD-<短名>/公众号稿.md`）只读兼容，不自动迁移；要新建旧结构时加 `--legacy --slug <短名>`。

### 站外拉取取源注意

- Next.js 站点正文常在 RSC 载荷里：优先探 `GET /api/notes/<id>` 读 `item.body`，别只 `curl` HTML。
- 图片可能在 `/api/uploads/<hash>`；下载时记录 hash → 本地名映射。
- 同图可能双 hash：`md5` 去重；截图带页面残留时按面板边框裁切。
- 与源差异、图片处理、口径边界写进 `素材来源.md`；一手来源抓不到必须写明。

## 反向选题包（可选，长文建议）

```text
YYYY-MM-DD-选题策划/
├── 选题策划.md
├── T1-<题>-调研与框架.md
├── 素材总库.md
├── 图表与配图方案.md
└── 发布前待办.md
```

多轮调研**每轮回头找反证**。

## 状态机

新结构：状态只写在 frontmatter 的 `status`，文件夹名 = 文章名，不随状态改。

| status | 含义 |
|--------|------|
| 草稿 | 写作中 |
| 定稿 | 可发 |
| 已发布 | 已上线（作者手动改） |

旧交付包保留原规则：草稿 `YYYY-MM-DD-名`，定稿 / 已发布 `…-released`。

```bash
python3 scripts/sync-status.py                 # dry-run
python3 scripts/sync-status.py --apply         # 刷字数（旧交付包另外纠目录名）
python3 scripts/sync-status.py --set 定稿 <专题>/<文章名> --apply
```

## 字数口径（三处别混）

| 输出 | 口径 | 用途 |
|------|------|------|
| frontmatter `word_count` | 正文**全文**的 `[\u4e00-\u9fff]` 计数：frontmatter 之后的一切都算，含图注、也含图片路径里的中文 | 映射真源 |
| lint「字数」 | 视觉长度（中 1 + 英数 ×0.6，URL 不计） | 阅读时长 / 段长 |
| md2wechat「正文字数」 | 渲染后字符 | 仅展示 |

`word_count` **只由 `sync-status.py --apply` 回写，不手算**。它的口径与直觉不同：一篇 9 图稿，`images/NN-中文名.png` 这一串路径就贡献 40+ 字。自制口径（如剔掉图注与路径）会得出更小的值，写进 frontmatter 后会被 `sync-mapping.py` 判为漂移，而且同一个错值会同时落进 `topic.md` 总表与 `素材来源.md`。

## 定稿验收命令串

```bash
A=<专题>/<文章名>
python3 scripts/check_article.py $A                       # 结构：E 级清零
python3 scripts/de_ai_lint.py $A/<文章名>.md --genre long  # 去 AI 味：W 每条有结论，H 只供判断（装了 topmind-revise 时由它跑）
python3 scripts/scan_ai_flavor.py $A/<文章名>.md          # 词面诊断参考，不设定稿分数门槛
python3 scripts/lint-wechat.py --input $A/<文章名>.md
python3 scripts/sync-mapping.py --no-topstream
python3 scripts/sync-status.py
python3 scripts/md2wechat.py --input $A/<文章名>.md --embed-images   # 按需 → $A/out/
python3 scripts/audit-provenance.py --draft $A --source $A/raw/源稿-*.md   # 有源稿时
```

最后一行只在**有源稿**时跑（`reverse` / 站外拉取；`forward` 的底稿在 `notes/` 也一样适用）。退出码 **0 = 双向干净**、**1 = 有待判定项**、2 = 参数错。**1 不等于稿子有问题**：它只是把「本稿有、源稿找不到」和「源稿有、本稿落下」两类段摆出来，由人逐条判，归入已声明的修正/增补，或改回去。判定结论写进 `素材来源.md`，这一关才算收口。

三个注意点：

- **阈值别乱调**：默认 `0.72`。调高会把正常改写（换词、调序）判成新增，调低会漏掉真扩写。
- **源稿后加的块用 `--skip`**：源稿顶部若有本包后补的勘误/说明块（`> [!note] …`），本稿侧不存在，会恒定报一条反向待判定。用 `--skip '^>\s*\[!'` 排除，不要去改稿子。
- **图注不算遗漏**：脚本反向侧额外建了「去掉 `▲ 图 N` 前缀」的候选池，图注编号不会被误判为漏段。

## 收尾

1. 更新专题 `topic.md` 总表（派生视图）  
2. reverse 且要回推：**务必带 `--assets`**，否则 GitHub 上 `images/` 全裂：

   ```bash
   python3 scripts/push-to-topstream.py <包> --target notes/xxx.md --assets          # dry-run
   python3 scripts/push-to-topstream.py <包> --target notes/xxx.md --assets --apply \
     --asset-names "00-封面.jpg=01-cover.jpg,…"   # 仓库约定 ASCII 图名
   ```

   仓库图路径约定：`notes/<slug>.md` 引用 `../assets/images/<slug>/NN-name.png`。
   脚本只降级转换 + 写 notes + 搬图；**不自动改** README 索引 / `docs/公众号映射.md` / frontmatter（防索引漂移）。手工完成后再把 `target_file` 改实际路径。
3. 提醒：外链只能进「阅读原文」；图已 base64 内嵌，占位符按清单补传
4. 需要进交付层时：`save-output` 拷贝终稿到工作区 role:delivery 类别（以 `topmind.yaml` 实际目录为准，如 `88-输出/`；文件名 `YYYY-MM-DD-描述.ext`）

## Desktop

| 步骤 | Desktop「公众号创作」 |
|------|----------------------|
| 建包/列表 | 扫工作区包根 |
| 改稿 | 写闸回执 |
| 三关 | AI 味 + lint + 事实勾选 |
| 排版 | 主题预览 + 调脚本导出 |
| 状态 | 调 `sync-status` |
