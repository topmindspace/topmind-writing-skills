# Writing Skills 创作体系演进与质量验证

本报告记录 `@topmindspace/topmind-writing-skills` 从早期“机械门禁驱动”向 **「创作思考、方法策略与可扩展知识卡驱动」** 的全面演进，以及各技能的设计落点与自动化验证体系。架构全景见 [creative-system.md](./creative-system.md)。

---

## 一、核心演进方向：给 AI 思考支点，而非死板镣铐

| 维度 | 早期痛点与局限 | 现行架构与创作范式 |
|---|---|---|
| **定位与格调** | 残留互关、互浇、出摊、打卡、差额冲刺等浅层起号套路 | 全面清理浅层水分，聚焦**一手实用价值、深度拆解、平视同行交流与高质量幽默段子** |
| **去 AI 味机制** | 靠堆砌禁用词表和机械分数卡死，容易误伤正常表达 | 拆解 **AI 味四大生成机制**（温室湿度过渡词、高频逻辑连接词、公式化段末升华、伪情绪句式），从根源改成人话 |
| **作者口吻** | 容易滑向“高高在上的导师腔”或“翻译腔公关稿” | 确立 **平视同行视角（Peer-to-Peer）**，分享真实体感、具体数字与踩坑细节，收尾克制自然 |
| **封面与配图** | 提示词模板僵化重复，或出现误导性的伪造截图与假极简 | 提炼 **当代五大高吸引力封面趋势** 与 **双出字路径**（直出 vs 负空间叠字），概念功能图诚实标注 **`功能示意，不是实拍`** |
| **平台尺寸匹配** | 尺寸说明淹没在免责文字里，竖版跨平台裁切缺预设 | 建立直观的全平台尺寸速查表，裁切工具支持 `article`、`wechat`、`x-post`、`xiaohongshu`、`douyin`、`landscape-pair`（16:9⇄4:3）与 `vertical-pair`（9:16⇄3:4） |
| **检查工具定位** | 将标点、字数、列表符号或词面打分当成阻断门禁 | 仅保留事实保真与排版防崩硬底线；`de_ai_lint.py` 等全部作为**启发式诊断参考**，给 AI 与作者留足创作空间 |
| **经验扩展性** | 经验散落在长文档里，难以检索与按需加载 | 内置 **45 张结构化知识卡**（`shared/knowledge/`），支持 CLI 按技能/标签检索与增量扩展 |

---

## 二、八大技能职责与核心抓手

| 技能 | 核心职责与升级重点 |
|---|---|
| `topmind-briefs` | **干货短文与快讯**：一手实用价值优先（怎么用、省多少钱、什么门槛）；根据热点传播阶段（刚发/已刷屏/深水区）动态切换切入角度 |
| `topmind-viral-posts` | **高互动短帖与段子**：聚焦扮猪吃老虎（`A1` 不懂就问留槽点）、量级换算、踩坑冷知识、产品反转与走心故事；去除浅层互关水分 |
| `topmind-revise` | **三关审校与经验反哺**：事实数字核查 → 逻辑主线梳理 → 去 AI 四大机制打磨；支持对比「AI 初稿 vs 作者终稿」沉淀个人写作偏好 |
| `topmind-format` | **X 纯文本零改字排版**：严格保真原文措辞、事实、顺序与有效符号，仅优化断行、空行节奏与列表视觉呈现 |
| `topmind-wechat-post` | **公众号深度长文与内联排版**：平视同行深度长文创作，单源 Markdown 导出全内联样式 HTML（自动避开微信 ProseMirror 吞标签坑），支持插件辅助与多模型交叉审校 |
| `topmind-x-article` | **X Article 长文与富文本交付**：适配手机快读节奏与证据穿插，导出带一键复制与图序占位的单文件 HTML 及纯文本兜底稿 |
| `topmind-cover` | **多平台高辨识度封面设计**：融合 Swiss 大字反差、Bento 信息卡、原文高亮拼贴、微距材质与手绘白板拆解；提供精炼导演级提示词与全平台等比裁切工具 |
| `topmind-poster` | **HTML/CSS 高密度信息长图**：针对多维对比表、分级榜、架构流转图输出像素级对齐的可编辑 HTML 与高清 PNG |

---

## 三、常用工具命令速查

```bash
# 1. 纯文本排版（默认保留表情、链接和来源；按需加 --separate-links 或 --strip-emoji）
python3 scripts/format_text.py 原文.txt --mode duanzi --out 排版稿.txt

# 2. 去 AI 味与排版启发式诊断（W/H/I 提示供语境判断，不设机械分数门槛）
python3 scripts/de_ai_lint.py 文稿.md
python3 scripts/lint_x_post.py 短帖.txt

# 3. 封面多平台裁切与确定性叠字
python3 scripts/crop-cover.py 主图.png --preset wechat --out-dir 输出目录
python3 scripts/crop-cover.py 横版16比9母图.png --preset landscape-pair --out-dir 输出目录
python3 scripts/crop-cover.py 竖版9比16母图.png --preset vertical-pair --out-dir 输出目录
python3 scripts/title-engine.py --check spec.json
```

---

## 四、全链路质量门禁

每次修改与发版前通过以下命令验证代码、文档、链接、隐私与分发产物完整性：

| 验证命令 | 覆盖范围 |
|---|---|
| `npm run sync:shared && npm run check:shared` | `shared/manifest.json` 声明的全部共享文档、脚本与 45 张知识卡在 8 个技能间逐字节一致 |
| `bash scripts/ci_skill_gates.sh` | 去 AI 规则回归（`test_lint_rules.py`）、CLI 创作契约回归（`test_creative_contracts.py`）、8 个技能的文档/链接/反引号路径可达性（`audit_docs.py`）、样式与 CSS 审计、异常输入与多平台裁切回归（`negative_tests.py`） |
| `npm run check:evals` | `evals/evals.json` 路由触发词覆盖与正负向评测集结构校验 |
| `npm run package:skill && npm run host:pack && npm run check:release` | 8 个独立技能 ZIP 与宿主运行包的清单、SHA-256 及源码一致性校验 |
| `npm run privacy && npm run check:pack && npm test` | 隐私与遗留标识零泄漏、npm 发包干跑校验、Node 运行时全量测试 |
