# 公众号与 X：按目的适配

同一组事实可派生不同平台成品，必要归因、近似值、时间和状态保持一致；角度和篇幅可以适配读者，不要求逐字相同。

| 项 | X 普通帖 | 公众号短文 |
|---|---|---|
| 呈现 | 可复制纯文本 | Markdown，按需 HTML |
| 篇幅 | 按账号能力、内容和用户要求 | 常从 300–800 字起步，可调整 |
| 结构 | 短段、列表、对话、thread | 段落、列表、图、引用 |
| 来源 | 正文保留必要归因，链接可随文或另列 | 文内、图注、文末按需要 |
| 图片 | 有信息增益才配 | 同左，自制图也可解释结构 |
| 表情 / 标签 | 按作者与活动需要 | 按文章气质 |

短文默认文字交付，完整排版需求用平台技能；用户明确要 HTML 时也可用随包渲染器：

```bash
python3 scripts/md2wechat.py --input 公众号短文.md --embed-images --no-toc
python3 scripts/md2x-html.py X短文.md --images-from 公众号短文.md
python3 scripts/lint_x_post.py X短文.txt
```

有源稿图片时由渲染器按文档顺序读取，避免手工排序造成错位。生成后实际看导出和图序，X 的剪贴板和图片上传按当前平台行为核对。

开头可以事实、场景、问题或判断，结尾可以停下、落判断或邀请具体互动；更多完整样张见 [creative-practice.md](creative-practice.md)，交付见 [x-delivery-contract.md](x-delivery-contract.md)。

## 封面与组图

需要公众号宽封面、方形小图或把素材转为小红书 / 抖音图文时，先看 [平台封面参考](platform-cover-specs.md)。公众号普通文章与图片消息、抖音普通图文与商城内容分开处理；尺寸是制作预设，按当前入口验证。封面交 `topmind-cover`，密集内容页交 `topmind-poster`；这些适配不代表本技能已经提供各平台完整发布流程。
