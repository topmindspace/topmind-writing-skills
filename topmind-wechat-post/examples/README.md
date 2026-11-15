# topmind-wechat-post 原创示例（公众号文章原稿）

两篇原创 Markdown 源稿示例，展示结论前置、表格/列表穿插与自然平视口吻：

- [`01-公众号-整理书架.md`](./01-公众号-整理书架.md)：方法论随笔，包含痛点切入、3 列精简对比表与金句引用块。
- [`02-公众号-第一次养绿植.md`](./02-公众号-第一次养绿植.md)：实用入门指南，包含品种对比表与可执行的实操判断标准。

可直接运行随包渲染脚本生成微信公众号内联样式 HTML：

```bash
python3 scripts/md2wechat.py --input examples/01-公众号-整理书架.md --out-dir /tmp/wechat-demo
```
