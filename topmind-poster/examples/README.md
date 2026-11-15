# topmind-poster 原创示例（信息长图与榜单海报简报）

两份高信息密度海报文案与版式简报（虚构教学演示），可直接交由 `topmind-poster` 按 [layout-recipes.md](../references/layout-recipes.md) 排成 HTML/CSS 并渲染高清 PNG：

- [`01-海报-阅读月报.md`](./01-海报-阅读月报.md)：浅底编辑风（`1080px` 宽），包含 2×2 卡片网格與高亮色条清单。
- [`02-海报-工具分级榜.md`](./02-海报-工具分级榜.md)：深底科技分级榜（`1180px` 宽），包含 S/A/B 三档色条与双列卡片。

渲染命令示例：
```bash
python3 scripts/render_poster.py poster.html -o poster.png
```
