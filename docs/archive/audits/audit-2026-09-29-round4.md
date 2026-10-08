# 第四轮整改审计报告（2026-09-29）

> 基线：`1410e00`（v0.3.1）→ 本轮 commit（待填）
> 起因：用户指出第三轮 cover 样张"照搬别人的例子"（7 张参考封面的文案与形象几乎原样挪用），
> 要求参考图只沉淀设计语言、样张必须原创；同时 wechat-post、x-article 做一次真正全面的优化。

## 一、cover 样张原创纠偏

### 问题定性
第三轮 16 张样张的标题与视觉概念直接挪用 7 张参考封面：
"实测精选干货"+蓝色毛怪抱卡片、"从入门到精通"+人物推巨书、"星火最佳实践"、
"100天AI绘画"+戴墨镜的猫等。属临摹第三方作品，不能作为技能自带素材发布。

### 纠偏方案
- **设计语言保留**（从参考图提炼的通用规律，不属任何作品）：
  巨型标题字当主角（占画面 25%~45%）、数字/关键词彩色突出、
  三层文字结构（大标题+短副标题+标签条/署名）、左文右图或中央构图、
  背景干净不繁杂、关键元素在中央 60% 安全区。
- **文案与形象全部原创**：8 种风格新标题与视觉概念取材 AI/科技/效率工具/评测/教程，
  与 7 张参考图逐项比对不构成临摹：

| 风格 | 原创标题 | 原创视觉 |
|---|---|---|
| gan-huo 爆款干货 | 7天玩转提示词 | 纸飞机机器人 + 提示词卡片 |
| big-type 巨字宣言 | AI效率手册 | 抽象光影几何（无人物推书） |
| brand-launch 品牌发布 | 星尘 OS 3.0（虚构品牌） | 品牌色渐变 + 产品界面 + 卖点条 |
| tutorial-steps 教程步骤 | 从想法到产品 | 步骤卡片拼贴 + 原创序号章 |
| ip-fun IP 趣味 | 30天AI绘画挑战 | 狐狸画家 IP（非猫） |
| news-flash 资讯快报 | AI早报！ | 报纸 + 咖啡 + 闹钟 |
| minimal 极简留白 | 慢思考 | 银杏叶点睛 |
| magazine 杂志编辑 | 创造者访谈 | 黑白人物肖像 |

- `topmind-cover/assets/examples/README.md` 重写：声明样张为原创设计、仅演示设计语言，
  标题/数字/品牌/署名均为虚构。
- `topmind-cover/references/cover-styles.md`：8 风格"示例"小节全部换为本轮原创标题；
  **新增原创铁律**：prompt 配方是设计语言，禁止照抄任何第三方封面的文案与形象；
  grep 确认旧仿版专有文案与形象描述（Muse/26篇/爆款干货/从入门到精通/Skill/星火/Jev/
  Reddit/600万播放/算法工程师/蓝色毛怪抱卡片/人物推巨书/戴墨镜的猫）零残留。

### 样张清单与目检
- 16 张：8 主图（1200×675，85KB~800KB）+ 8 公众号裁剪版（900×383，`scripts/crop-cover.py`
  中央裁剪）+ `overview.png`（2×4 八宫格，Noto Sans CJK SC 标注中英风格名）
- **8 张主图全部目检通过**：中文逐字正确、无乱码错字、关键元素在中央 60% 安全区、
  不繁杂、与参考图不构成临摹。返工记录：本轮生成一次成型率高，未发生返工
  （第三轮的 7 次返工均为"底部元素超出安全区"，本轮 prompt 已前置规避）。
- 旧 16 张"仿版"已覆盖删除。

## 二、topmind-wechat-post 全面优化

### 修的 bug（4）
1. **行内图片绕过图片管线**（高）：段落里的 `![alt](x.png)` 保留相对路径，
   `--embed-images` 报"未内嵌"、上传清单漏项、计数为 0，粘贴到公众号后整图消失。
   修法：`convert()` 注册 `CTX["img_resolve"]` 回调，行内图（表格/列表/容器内亦同）
   统一经管线解析、复制到 `images/`、登记清单。
2. **手写序号剥离漏大写数字**：`## 第叁章 X` 的"第叁章"不剥离；`CN_NUM` 补入
   壹贰叁肆伍陆柒捌玖拾。
3. **分隔线触发自家合规 WARN**：`render_hr` 输出 inline-block 又被 `audit_inline` 判 WARN，
   每篇带 `---` 的稿子必报；改用块级 `<section>` + `margin:0 auto` 居中，视觉一致，
   自检恢复干净。
4. **图片 title 属性致源码泄漏**：`![a](x "t")` 标准写法正则匹配不上，整段 markdown
   原文进 HTML；两处图片正则加可选 `(?:\s+"[^"]*")?` 分组。

### SKILL.md / 文档
- 主题表"适用"列与各主题 JSON 的 `genre` 声明逐字对齐（之前是拍脑袋写的）；
  补"行内图片同样走图片管线"；补 `--link-mode` 参数说明（此前完全没提）。
- description 经 `audit_skill.py` 校验通过，未动；渐进披露结构 OK，未动。
- README（中/英）：新增 9 行"最小示例"（输入→输出片段）+ `md2wechat` 9 行参数表。
- `negative_tests.py` 5→8 项。

### 验证
negative 8/8；`package_skill.py --check` 全过；audit_styles/audit_docs/audit_skill/audit_css
全过；实跑回归 21/21（含 1.7MB 大稿 1.1s）；sync in sync；privacy PASS。

### 未改（记入遗留）
- `border-radius` WARN 每次运行必报（生成器自己输出的圆角），属提醒噪音；
  降为静默会改变门禁输出行为，未擅自改。
- `--link-mode note` 与默认分支行为无差，历史遗留，未动。

## 三、topmind-x-article 全面优化

### 修的 bug（12，均在 `scripts/md2x.py`）
1. 标题内行内标记残留（`# 见[文档](url)`）→ 标题文本走行内清理
2. 引用内标题残留（`> # 标题`）→ 引用剥离移到标题识别前，支持多级 `>>`
3. 表格单元格内标记残留 → 单元格走行内清理
4. 引用式链接/图片不转、定义行残留 → 预收集定义，支持行内式/引用式/`[]`省略式/快捷式
5. URL 含括号断裂（`.../X_(消歧义)`）→ 平衡括号扫描替代 `[^)]*`
6. 带空格分割线（`* * *`）不识别 → 正则放宽
7. Setext 标题（`标题\n===`）残留 → 转纯文本标题行
8. 转义符残留（`\*`）→ 私有用区占位保护，还原放最后
9. 文首 `---` 被 frontmatter 误吞 → 块内非空行必须都含 `:` 才认定
10. 代码块内 `---` 被误判分割线 → 围栏/代码态检查前置
11. 文档以代码块开头时首行缩进丢失 → 只去首尾空行（旧 bug 一并修）
12. BOM 头致首个 `#` 标题识别失败 → `utf-8-sig` 读取

### SKILL.md / 文档
- description 补 `Do NOT use for 公众号（→ topmind-wechat-post）`，与短推文路由对称；
  其余经核查准确；触发词完备，未动。
- `references/x-format.md` 转换规则表与脚本实际行为对齐。
- README（中/英）：转换规则更新 + 10 行"最小示例"（输出经实测逐字一致）。

### 刻意没改的
- `#标题`（# 后无空格）仍不认作标题：避免误伤行首 hashtag（如 `#AI`）。
- `2 * 3 = 6` 类孤立星号仍可能被斜体正则配对：修它会误伤真斜体，属 trade-off。
- 复杂表格仍需手动拆段落：`x-format.md` 已澄清为人工步骤。

### 验证
negative 6/6；package_skill/audit_* 全过；sync in sync；privacy PASS；版本一致（0.1.0=0.1.0）。

## 四、发版准备 0.3.2
- 根 `package.json` 0.3.1 → **0.3.2**（patch）；README（中/英）、top-ppt-html README（中/英）、
  docs/PUBLISHING.md 的 9 处版本引用同步；CHANGELOG 新增 0.3.2 条目；4 技能 version 不动。
- 全门禁（本轮复跑）：`ci_privacy_scan.py` PASS（197 文件）、`sync_npm_files.js --check` in sync、
  `ci_skill_gates.sh --with-pptx` all skills green、4 技能 negative_tests 全过、
  `run_skill_gates.js versions` 通过、`test_install_guards.js` 全部通过。
- **本地 commit，不 push、不打 tag**（发版由用户定夺）。

## 五、遗留项
1. wechat-post `border-radius` WARN 噪音（见第二节未改项），是否降为静默待定。
2. x-article 两处 trade-off（`#标题`、孤立星号斜体配对），属设计选择。
3. 第一、二轮遗留：Windows/macOS CI 完整矩阵、安装器 2 个中等问题、x-article 4 个
   可能改变行为的改进项，仍未动。
4. npm README 总览图 URL 指向 main 分支，push 后生效。
