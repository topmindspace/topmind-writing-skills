# topmind-x-article 原创示例（X Article 长文原稿）

两篇原创 Markdown 长文源稿示例，展示清晰的手机端阅读节奏、小标题推进与列表结构：

- [`01-长文-慢慢写.md`](./01-长文-慢慢写.md)：观点与方法论长文，演示痛点切入、三步推进与自然口语节奏。
- [`02-长文-周末短途.md`](./02-长文-周末短途.md)：结构化指南长文，演示时间线分点与极简清单。

可用随包脚本一键转换为 X Article 富文本粘贴页或纯文本兜底稿：

```bash
python3 scripts/md2x-html.py examples/01-长文-慢慢写.md --out /tmp/X长文.html
python3 scripts/md2x.py examples/01-长文-慢慢写.md --out /tmp/X发布稿.txt
```
