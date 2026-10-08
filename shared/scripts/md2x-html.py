#!/usr/bin/env python3
"""md2x-html.py — Markdown 原稿 → 可直接复制的 X 长文 HTML（单文件）。

用法：
    python3 md2x-html.py 原稿.md --out X长文.html \\
        --images 样张1.png 样张2.png ... [--cover cover-1500x600.png]

约定（与 md2x.py 对齐）：
- `[图N]` 独占一行 → 按顺序取 --images[N-1]，转成内嵌 data-URI 的 <figure>；
  点击图片弹出 lightbox 放大查看原图（右键可另存/截图，不拦截右键菜单）
- ``` 围栏代码块（直出提示词）→ <blockquote> + 「复制提示词」按钮。
  原因：X 文章编辑器没有"粘贴 <pre> 即代码块"的识别，原生代码块只能走
  Insert 菜单；<blockquote> 粘贴后即 X 原生引用块，格式不丢、读者全选即拷。
  支持嵌套围栏（```` 开栏不被内层 ``` 提前闭合）；未闭合围栏在文末自动收尾
- `#` → h1（X 标题栏专用，复制全文时自动剔除）；`##`/`###` → h2/h3
  （对应 X 的"标题/副标题"两级）
- `- ` / `1. ` → ul/ol；`**x**` → strong；`` `x` `` → code（X 粘贴后变纯文本）；
  `---` → hr（X 粘贴可能丢弃，需手动 Insert → 分割线，见 references/x-html-format.md）
- GFM 表格 → ul.xtable（X 粘贴会丢弃 <table>，转列表保内容）
- frontmatter（--- ... ---）跳过，只取 title

设计目标（对标 md2wechat 的公众号体验）：
- 文本+格式：页顶「一键复制全文」按钮 → 剪贴板富文本 → 粘贴进 X 文章编辑器。
  复制前自动剔除按钮/UI 与 .no-paste 块（标题、封面预览），只剩 X 可识别的
  语义标签：h2/h3/p/ul/ol/blockquote/a/hr/img
- 图片：data-URI 内嵌（X 若支持则随粘贴带入）；每张图带 [图N] 编号 + 「下载图片」
  按钮保底，图片没跟过去时按编号下载再上传，不用找文件、不用对顺序；
  点击图片 lightbox 放大看原图，方便核对、截图或右键另存
- 封面：X 有独立封面上传入口，始终单独文件；HTML 顶部仅作预览 + 下载链接

只用 Python 标准库。
"""

import argparse
import base64
import html
import os
import re
import sys

CSS = """
:root { color-scheme: light; }
* { box-sizing: border-box; }
body { margin: 0; background: #f7f9fa; color: #0f1419;
       font-family: -apple-system, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif; }
.toolbar { position: sticky; top: 0; z-index: 50; background: rgba(255,255,255,.96);
           border-bottom: 1px solid #eff3f4; padding: 10px 16px;
           display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
.toolbar .hint { font-size: 13px; color: #536471; }
.toolbar .steps { font-size: 13px; color: #0f1419; font-weight: 700; }
.btn { appearance: none; border: 1px solid #cfd9de; background: #fff; color: #0f1419;
       border-radius: 9999px; padding: 8px 18px; font-size: 14px; font-weight: 700;
       cursor: pointer; }
.btn.primary { background: #0f1419; color: #fff; border-color: #0f1419; }
.btn:active { transform: scale(.97); }
.article { max-width: 680px; margin: 0 auto; background: #fff;
           padding: 32px 28px 64px; }
.article h1 { font-size: 26px; line-height: 1.4; margin: 0 0 20px; }
.article h2 { font-size: 20px; margin: 34px 0 12px; padding-top: 6px; }
.article h3 { font-size: 18px; margin: 26px 0 10px; }
.article p { font-size: 17px; line-height: 1.85; margin: 0 0 14px; word-break: break-word; }
.article ul, .article ol { font-size: 17px; line-height: 1.85; margin: 0 0 14px; padding-left: 1.4em; }
.article hr { border: none; border-top: 1px solid #eff3f4; margin: 28px 0; }
.article a { color: #1d9bf0; }
.article code { background: #f1f3f4; border-radius: 4px; padding: 1px 6px;
                font-size: .92em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
.article ul.xtable { list-style: none; padding-left: 0; }
.article ul.xtable li { background: #f7f9fa; border: 1px solid #eff3f4;
                       border-radius: 8px; padding: 8px 12px; margin-bottom: 8px; }
.cover-note { background: #f7f9fa; border: 1px dashed #cfd9de; border-radius: 12px;
              padding: 14px 16px; font-size: 14px; color: #536471; margin-bottom: 24px; }
.cover-note img { width: 100%; border-radius: 8px; display: block; margin-bottom: 10px;
                  cursor: zoom-in; }
figure.ximg { margin: 22px 0; }
figure.ximg img { width: 100%; border-radius: 10px; display: block;
                 border: 1px solid #eff3f4; cursor: zoom-in; }
figure.ximg figcaption { display: flex; justify-content: space-between; align-items: center;
                        margin-top: 8px; font-size: 13px; color: #536471; }
.prompt { position: relative; margin: 14px 0 20px; }
.prompt blockquote { margin: 0; background: #f7f9fa; border-left: 4px solid #1d9bf0;
                     border-radius: 0 10px 10px 0; padding: 16px 18px;
                     font-size: 14px; line-height: 1.8; }
.prompt blockquote code { background: none; padding: 0; font-size: 1em;
                         font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
.prompt .btn { position: absolute; top: 8px; right: 8px; padding: 5px 12px;
               font-size: 12px; }
.toast { position: fixed; left: 50%; bottom: 40px; transform: translateX(-50%);
         background: #0f1419; color: #fff; font-size: 14px; padding: 10px 20px;
         border-radius: 9999px; opacity: 0; transition: opacity .25s; pointer-events: none;
         z-index: 200; }
/* 图片 lightbox：点击放大看原图；不拦截右键，可右键另存/截图 */
.lightbox { position: fixed; inset: 0; z-index: 100; background: rgba(10,14,20,.93);
            display: none; align-items: center; justify-content: center; padding: 24px; }
.lightbox.open { display: flex; }
.lb-inner { max-width: 96vw; max-height: 94vh; display: flex; flex-direction: column;
            gap: 10px; align-items: center; }
.lb-inner img { max-width: 94vw; max-height: 76vh; border-radius: 8px; background: #fff; }
.lb-bar { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; justify-content: center; }
.lb-cap { color: #cfd9de; font-size: 13px; }
.lb-tip { color: #8a93a6; font-size: 12px; }
"""

JS = """
var lbFname = '';
function toast(msg){ var t=document.getElementById('toast'); t.textContent=msg;
  t.style.opacity=1; setTimeout(function(){ t.style.opacity=0; }, 1800); }
function cleanClone(){
  var el=document.getElementById('article');
  var c=el.cloneNode(true);
  var kill=c.querySelectorAll('button, .no-paste');
  for(var i=0;i<kill.length;i++){ kill[i].parentNode.removeChild(kill[i]); }
  return c;
}
async function copyArticle(){
  var c=cleanClone();
  var htm='<meta charset="utf-8">'+c.innerHTML;
  try{
    var item=new ClipboardItem({
      'text/html': new Blob([htm],{type:'text/html'}),
      'text/plain': new Blob([c.innerText],{type:'text/plain'})
    });
    await navigator.clipboard.write([item]);
    toast('已复制全文（含格式），去 X 粘贴吧');
  }catch(e){
    try{ await navigator.clipboard.writeText(c.innerText); toast('已复制纯文本（富文本复制失败）'); }
    catch(e2){ toast('复制失败，请手动全选复制'); }
  }
}
async function copyPrompt(btn){
  var code=btn.parentElement.querySelector('code').innerText;
  try{ await navigator.clipboard.writeText(code); toast('提示词已复制，去 AI 生图工具粘贴'); }
  catch(e){ toast('复制失败，请手动复制'); }
}
function dlImg(btn){
  var fig=btn.closest('figure');
  var img=fig ? fig.querySelector('img') : document.querySelector('#coverbox img');
  if(!img){ toast('找不到图片'); return; }
  var a=document.createElement('a');
  a.href=img.src; a.download=btn.getAttribute('data-fname') || 'image.png';
  document.body.appendChild(a); a.click(); a.remove();
  toast('开始下载 '+(btn.getAttribute('data-fname')||'图片'));
}
/* 复制图片：把 PNG 以 image/png 写进剪贴板，X 编辑器支持直接粘贴图片（不认 data-URI 随文粘贴）。
   流程：点某张图下的「复制图片」→ 去 X 编辑器对应位置 Ctrl/Cmd+V。 */
async function copyImg(btn){
  var fig=btn.closest('figure');
  var img=fig ? fig.querySelector('img') : document.querySelector('#coverbox img');
  if(!img){ toast('找不到图片'); return; }
  try{
    var res=await fetch(img.src);
    var blob=await res.blob();
    await navigator.clipboard.write([new ClipboardItem({'image/png': blob})]);
    toast('图片已复制，去 X 编辑器对应位置粘贴');
  }catch(e){ toast('复制失败，改用「下载图片」按钮'); }
}
/* lightbox：点击图片放大看原图。刻意不拦截右键，放大后可右键另存 / 直接截图。 */
function openLightbox(img){
  var lb=document.getElementById('lightbox');
  document.getElementById('lbimg').src=img.src;
  document.getElementById('lbimg').alt=img.alt||'原图';
  lbFname=img.getAttribute('data-fname')||'image.png';
  document.getElementById('lbcap').textContent=(img.alt||'原图')+' · '+lbFname;
  lb.classList.add('open');
  document.body.style.overflow='hidden';
}
function closeLightbox(){
  document.getElementById('lightbox').classList.remove('open');
  document.body.style.overflow='';
}
function openFullsize(){
  var src=document.getElementById('lbimg').src;
  var parts=src.split(','), mime='image/png';
  var m=parts[0].match(/:(.*?);/); if(m){ mime=m[1]; }
  try{
    var bin=atob(parts[1]), arr=new Uint8Array(bin.length);
    for(var i=0;i<bin.length;i++){ arr[i]=bin.charCodeAt(i); }
    var url=URL.createObjectURL(new Blob([arr],{type:mime}));
    window.open(url,'_blank');
  }catch(e){ toast('打开失败，可右键图片另存'); }
}
function dlLightbox(){
  var a=document.createElement('a');
  a.href=document.getElementById('lbimg').src; a.download=lbFname;
  document.body.appendChild(a); a.click(); a.remove();
  toast('开始下载 '+lbFname);
}
document.addEventListener('keydown', function(e){
  if(e.key==='Escape'){ closeLightbox(); }
});
"""

HTML_TMPL = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>@@TITLE@@</title>
<style>@@CSS@@</style>
</head>
<body>
<div class="toolbar">
  <span class="steps">1. 标题填入 X 标题栏 → 2. 一键复制全文 → 3. 粘贴到 X 正文</span>
  <button class="btn primary" onclick="copyArticle()">一键复制全文</button>
  <span class="hint">图片随粘贴带入则直接用；没带入就点每张图下的「复制图片」到 X 对应位置粘贴（或「下载图片」后上传）。封面始终单独上传。点击图片可放大查看原图。</span>
</div>
<article class="article" id="article">
@@BODY@@
</article>
<div class="lightbox" id="lightbox" onclick="if(event.target===this)closeLightbox()">
  <div class="lb-inner">
    <img id="lbimg" alt="原图">
    <div class="lb-bar">
      <span class="lb-cap" id="lbcap"></span>
      <button class="btn" onclick="openFullsize()">新标签页打开原图</button>
      <button class="btn" onclick="dlLightbox()">下载原图</button>
      <button class="btn" onclick="closeLightbox()">关闭</button>
    </div>
    <div class="lb-tip">可右键图片另存 / 直接截图 · Esc 关闭</div>
  </div>
</div>
<div class="toast" id="toast"></div>
<script>@@JS@@</script>
</body>
</html>
"""

COVER_FNAME = "cover-1500x600.png"


def data_uri(path):
    try:
        with open(path, "rb") as f:
            raw = f.read()
    except OSError:
        print("图片读取失败：%s" % path, file=sys.stderr)
        sys.exit(1)
    ext = os.path.splitext(path)[1].lower()
    mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
            "webp": "image/webp", "gif": "image/gif"}.get(ext.lstrip("."), "image/png")
    return "data:%s;base64,%s" % (mime, base64.b64encode(raw).decode("ascii"))


def inline_md(s):
    """行内 markdown → html：加粗、行内代码、裸链接。"""
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`([^`]+?)`", r"<code>\1</code>", s)
    s = re.sub(r"(https?://[^\s<>()\uff08\uff09\u3010\u3011\u300c\u300d\u300e\u300f]+)",
               r'<a href="\1">\1</a>', s)
    return s


def md_to_html(md_text, images, cover):
    lines = md_text.split("\n")
    out = []
    cover_uri = data_uri(cover) if cover else None

    i = 0
    if lines and lines[0].strip() == "---":
        i = 1
        while i < len(lines) and lines[i].strip() != "---":
            i += 1
        i += 1

    in_fence = None  # 开栏的反引号串（如 '```'）；None 表示不在围栏内
    code_buf = []
    in_ul = False
    in_ol = False
    in_table = False
    table_buf = []

    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    def flush_table():
        nonlocal in_table, table_buf
        if not in_table:
            return
        rows = []
        for r in table_buf:
            cells = [c.strip() for c in r.strip().strip("|").split("|")]
            rows.append(cells)
        rows = [r for r in rows if not all(re.fullmatch(r":?-+:?", c or "-") for c in r)]
        if rows:
            out.append('<ul class="xtable">')
            for j, r in enumerate(rows):
                cells = " ｜ ".join(inline_md(c) for c in r)
                if j == 0:
                    out.append("<li><strong>%s</strong></li>" % cells)
                else:
                    out.append("<li>%s</li>" % cells)
            out.append("</ul>")
        in_table = False
        table_buf = []

    def flush_prompt():
        body = "\n".join(code_buf)
        esc = html.escape(body).replace("\n", "<br>")
        out.append(
            '<div class="prompt"><blockquote><code>%s</code></blockquote>'
            '<button class="btn" onclick="copyPrompt(this)">复制提示词</button>'
            "</div>" % esc
        )

    while i < len(lines):
        line = lines[i]
        s = line.strip()

        fm = re.match(r"^(`{3,})", s)
        if fm:
            fence = fm.group(1)
            if in_fence is None:
                # 开栏
                close_lists()
                flush_table()
                in_fence = fence
                code_buf = []
            elif len(fence) >= len(in_fence) and s.strip("`") == "":
                # 闭栏：纯反引号行且长度不短于开栏（内层短围栏视为代码内容）
                flush_prompt()
                in_fence = None
                code_buf = []
            else:
                code_buf.append(line)
            i += 1
            continue
        if in_fence is not None:
            code_buf.append(line)
            i += 1
            continue

        if re.match(r"^\|.*\|\s*$", s) and "|" in s.strip("|"):
            if not in_table:
                close_lists()
                in_table = True
                table_buf = []
            table_buf.append(s)
            i += 1
            continue
        else:
            flush_table()

        m = re.fullmatch(r"\[图(\d+)\]", s)
        if m:
            close_lists()
            n = int(m.group(1))
            if 1 <= n <= len(images):
                uri = data_uri(images[n - 1])
                fname = "图%d-%s" % (n, os.path.basename(images[n - 1]))
                out.append(
                    '<figure class="ximg"><img src="%s" alt="图%d" data-fname="%s" '
                    'onclick="openLightbox(this)">'
                    '<figcaption><span class="cap">[图%d]</span>'
                    '<button class="btn" data-fname="%s" '
                    'onclick="dlImg(this)">下载图片</button>'
                    '<button class="btn" onclick="copyImg(this)">复制图片</button></figcaption></figure>'
                    % (uri, n, html.escape(fname, quote=True), n,
                       html.escape(fname, quote=True))
                )
            else:
                out.append("<p>[图%d]（图片缺失）</p>" % n)
            i += 1
            continue

        if s.startswith("### "):
            close_lists()
            out.append("<h3>%s</h3>" % inline_md(s[4:]))
            i += 1
            continue
        if s.startswith("## "):
            close_lists()
            out.append("<h2>%s</h2>" % inline_md(s[3:]))
            i += 1
            continue
        if s.startswith("# "):
            close_lists()
            out.append('<h1 class="no-paste">%s</h1>' % inline_md(s[2:]))
            i += 1
            continue

        if s in ("---", "***"):
            close_lists()
            out.append("<hr>")
            i += 1
            continue

        m = re.match(r"^(\d+)\.\s+(.*)$", s)
        if m:
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if not in_ol:
                out.append("<ol>")
                in_ol = True
            out.append("<li>%s</li>" % inline_md(m.group(2)))
            i += 1
            continue

        if s.startswith("- "):
            if in_ol:
                out.append("</ol>")
                in_ol = False
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append("<li>%s</li>" % inline_md(s[2:]))
            i += 1
            continue

        if not s:
            close_lists()
            i += 1
            continue

        close_lists()
        out.append("<p>%s</p>" % inline_md(s))
        i += 1

    close_lists()
    flush_table()
    if in_fence is not None:
        # 未闭合围栏：文末自动收尾，不丢内容
        flush_prompt()

    body = "\n".join(out)

    cover_html = ""
    if cover_uri:
        cover_html = (
            '<div class="cover-note no-paste" id="coverbox">'
            '<img src="%s" alt="封面预览（点击放大）" data-fname="%s" onclick="openLightbox(this)">'
            '<div>封面图预览（1500×600 · 5:2）。X 文章有独立封面上传入口，'
            '请单独上传，不要随正文粘贴。<br>'
            '<button class="btn" data-fname="%s" '
            'onclick="dlImg(this)">下载封面图</button>'
            '<button class="btn" onclick="copyImg(this)">复制封面图</button></div></div>'
        ) % (cover_uri, COVER_FNAME, COVER_FNAME)
    return cover_html + "\n" + body


def main():
    ap = argparse.ArgumentParser(description="Markdown 原稿 → X 长文 HTML（一键复制）")
    ap.add_argument("md", help="原稿 markdown 路径")
    ap.add_argument("--out", required=True, help="输出 HTML 路径")
    ap.add_argument("--images", nargs="*", default=[], help="[图N] 对应的图片路径（按顺序）")
    ap.add_argument("--images-from", default=None, metavar="WECHAT_MD",
                    help="从指定的 markdown（如公众号稿.md）中按文档顺序提取 ![]() 本地图片路径，"
                         "作为 [图N] 的图片来源。X 稿必须从公众号稿派生时用此项，"
                         "禁止手工拼 --images 顺序（曾因此出现配图错位）")
    ap.add_argument("--cover", default=None, help="封面图路径（1500×600，5:2）")
    args = ap.parse_args()

    if not os.path.isfile(args.md):
        print("输入文件不存在：%s" % args.md, file=sys.stderr)
        sys.exit(1)
    with open(args.md, encoding="utf-8") as f:
        md_text = f.read()

    # 图片来源：优先 --images-from（从公众号稿等源 md 按文档顺序派生），杜绝手工排序错位
    images = list(args.images)
    if args.images_from:
        if not os.path.isfile(args.images_from):
            print("图片来源文件不存在：%s" % args.images_from, file=sys.stderr)
            sys.exit(1)
        with open(args.images_from, encoding="utf-8") as f:
            src_md = f.read()
        base = os.path.dirname(os.path.abspath(args.images_from))
        found = []
        for q in re.findall(r"!\[[^\]]*\]\(([^)\s]+)\)", src_md):
            if re.match(r"https?://", q):
                print("警告：跳过远程图片（无法内嵌）：%s" % q, file=sys.stderr)
                continue
            fp = q if os.path.isabs(q) else os.path.normpath(os.path.join(base, q))
            found.append(fp)
        if args.images:
            print("警告：同时给了 --images 和 --images-from，采用 --images-from 派生顺序",
                  file=sys.stderr)
        images = found
        print("从 %s 派生图片顺序：%d 张" % (args.images_from, len(images)), file=sys.stderr)

    for p in images:
        if not os.path.isfile(p):
            print("图片不存在：%s" % p, file=sys.stderr)
            sys.exit(1)

    # 校验：[图N] 标记数量必须与图片数量一致，且编号连续 1..N
    markers = sorted({int(n) for line in md_text.split("\n")
                      for n in re.findall(r"^\[图(\d+)\]$", line.strip())})
    if markers:
        if markers != list(range(1, len(markers) + 1)):
            print("图编号不连续：发现 %s，应为 1..%d" % (markers, len(markers)), file=sys.stderr)
            sys.exit(1)
        if len(images) != len(markers):
            print("图片数量不匹配：[图N] 标记 %d 个，图片 %d 张" % (len(markers), len(images)),
                  file=sys.stderr)
            sys.exit(1)
    if args.cover and not os.path.isfile(args.cover):
        print("封面图不存在：%s" % args.cover, file=sys.stderr)
        sys.exit(1)

    # 标题取 frontmatter 之后的第一个 #（frontmatter 里可能有 # 开头的行）
    body_lines = md_text.split("\n")
    if body_lines and body_lines[0].strip() == "---":
        j = 1
        while j < len(body_lines) and body_lines[j].strip() != "---":
            j += 1
        body_lines = body_lines[j + 1:]
    m = re.search(r"^#\s+(.+)$", "\n".join(body_lines), re.M)
    title = m.group(1).strip() if m else "X长文"

    body = md_to_html(md_text, images, args.cover)
    page = HTML_TMPL.replace("@@TITLE@@", html.escape(title)) \
                    .replace("@@CSS@@", CSS) \
                    .replace("@@BODY@@", body) \
                    .replace("@@JS@@", JS)

    out_dir = os.path.dirname(os.path.abspath(args.out))
    os.makedirs(out_dir, exist_ok=True)
    tmp = args.out + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(page)
        os.replace(tmp, args.out)
    except OSError as e:
        print("写入失败：%s" % e, file=sys.stderr)
        sys.exit(1)
    print("已生成：%s" % args.out)


if __name__ == "__main__":
    main()
