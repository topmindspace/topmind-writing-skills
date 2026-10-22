#!/usr/bin/env python3
"""md2x-html.py — Markdown 原稿 → 可直接复制的 X 长文 HTML（单文件）。

用法：
    python3 md2x-html.py <文章名>/<文章名>.md
        # 文章文件夹结构：直接读源稿里的 ![说明](images/xx.png)，按文档顺序嵌图；
        # --out 缺省 <文章名>/out/X长文.html，--cover 缺省读 frontmatter 的 cover
    python3 md2x-html.py X长文.md --out X长文.html --images-from 公众号稿.md   # 旧结构
    python3 md2x-html.py 原稿.md --out X长文.html --images 1.png 2.png [--cover c.png]

约定（与 md2x.py 对齐）：
- 源稿没有 `[图N]`、只有独占一行的 `![说明](本地路径)` 时，按文档顺序直接取图（路径相对 md 所在目录），
  内部换成 `[图N]`，不需要再派生 X长文.md；远程图片无法内嵌，跳过并告警
- 图片后紧跟（或隔一个空行）的「来源：……」行渲染成小号灰字图注，复制时作为一段文字保留
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
- GFM 表格 → ul.xtable（X 粘贴会丢弃 <table>，转列表保内容）；加 --tables-as-images 时改成表格图片
  （无头 Chrome 截图后内嵌，X 粘贴能保住表格的样子；找不到浏览器时退回列表并提示）
- --preview：再把生成的页面截成一张长图 out/预览.png，交付时给用户看图文效果
- 普通行的行首缩进（≥2 个空格或全角空格）保留为 &nbsp;，emoji 项目符号的二级条目不会被吞缩进
- frontmatter（--- ... ---）跳过，只取 title / cover / subtitle；subtitle（可选）只在页顶预览里给出（no-paste，
  X 文章没有副标题栏，可以拿去当推文文案），不进复制内容
- HTML 注释（<!-- 写作提示 -->，可跨行）整段去掉，不进产物；代码块和行内代码里的原样保留

设计目标（对标 md2wechat 的公众号体验）：
- 文本+格式：页顶「一键复制全文」按钮 → 剪贴板富文本 → 粘贴进 X 文章编辑器。
  复制前自动剔除按钮/UI 与 .no-paste 块（标题、封面预览），配图换成 [图N] 占位段，
  只剩 X 可识别的语义标签：h2/h3/p/ul/ol/blockquote/a/hr
- 复制链路（按顺序降级）：① copy 事件 + execCommand('copy')，同步、在 file:// 和
  iframe 预览里也能用；② navigator.clipboard.write(ClipboardItem text/html+text/plain)，
  再退 writeText；③ 都不行就自动全选正文，提示按 Cmd/Ctrl+C。每步都有 toast
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
import shutil
import subprocess
import sys
import tempfile

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
.article p.src { font-size: 13px; line-height: 1.6; color: #536471; margin: -12px 0 18px; }
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
var toastTimer = null;
function toast(msg, ms){ var t=document.getElementById('toast'); t.textContent=msg;
  t.style.opacity=1; if(toastTimer){ clearTimeout(toastTimer); }
  toastTimer=setTimeout(function(){ t.style.opacity=0; }, ms||2200); }
/* 复制用的干净副本：去掉按钮/UI 与 .no-paste（标题、封面预览）；
   配图换成独占一段的 [图N] 占位——X 编辑器不认 data-URI 随文粘贴，
   带着几 MB base64 反而容易让写剪贴板/粘贴失败。图片用每张图下的「复制图片」单独粘。 */
function cleanClone(){
  var el=document.getElementById('article');
  var c=el.cloneNode(true);
  var figs=c.querySelectorAll('figure.ximg');
  for(var i=0;i<figs.length;i++){
    var cap=figs[i].querySelector('.cap');
    var p=document.createElement('p');
    p.textContent=cap ? cap.textContent : '[图]';
    figs[i].parentNode.replaceChild(p, figs[i]);
  }
  var kill=c.querySelectorAll('button, .no-paste, script, style');
  for(var j=0;j<kill.length;j++){ if(kill[j].parentNode){ kill[j].parentNode.removeChild(kill[j]); } }
  return c;
}
function plainText(node){
  /* innerText 依赖布局，离屏节点可能拿不到换行，按块级元素手动拼 */
  var out=[], blocks=node.querySelectorAll('h1,h2,h3,p,li,blockquote,hr');
  for(var i=0;i<blocks.length;i++){
    var b=blocks[i];
    if(b.tagName==='LI' && b.parentNode && b.parentNode.closest && b.parentNode.closest('li')){ continue; }
    if(b.tagName==='P' && b.closest('li,blockquote')){ continue; }
    if(b.tagName==='HR'){ out.push('---'); continue; }
    var t=(b.textContent||'').replace(/\\s+\\n/g,'\\n').trim();
    if(!t){ continue; }
    if(b.tagName==='LI'){ t=(b.parentNode.tagName==='OL' ? (Array.prototype.indexOf.call(b.parentNode.children,b)+1)+'. ' : '- ')+t; }
    out.push(t);
  }
  return out.join('\\n\\n');
}
/* 同步路径：copy 事件里直接塞 text/html + text/plain。
   file://、非安全上下文、没给 clipboard-write 的 iframe 预览里 navigator.clipboard 不可用，
   execCommand('copy') 仍能用；必须在点击的同步调用栈里执行（Safari 尤其严格），所以放第一步。 */
function copyViaEvent(html, text){
  var done=false;
  function onCopy(e){
    try{ e.clipboardData.setData('text/html', html); e.clipboardData.setData('text/plain', text);
         e.preventDefault(); done=true; }catch(err){}
  }
  var box=document.createElement('div');
  box.setAttribute('aria-hidden','true');
  box.style.cssText='position:fixed;left:-99999px;top:0;width:1px;height:1px;overflow:hidden;';
  box.textContent='.';
  document.body.appendChild(box);
  var sel=window.getSelection(), saved=[];
  for(var i=0;i<sel.rangeCount;i++){ saved.push(sel.getRangeAt(i)); }
  var r=document.createRange(); r.selectNodeContents(box); sel.removeAllRanges(); sel.addRange(r);
  document.addEventListener('copy', onCopy, true);
  var ok=false;
  try{ ok=document.execCommand('copy'); }catch(e){ ok=false; }
  document.removeEventListener('copy', onCopy, true);
  sel.removeAllRanges(); for(var k=0;k<saved.length;k++){ sel.addRange(saved[k]); }
  box.remove();
  return ok && done;
}
function selectArticle(){
  var el=document.getElementById('article');
  var sel=window.getSelection(); var r=document.createRange();
  r.selectNodeContents(el); sel.removeAllRanges(); sel.addRange(r);
  el.scrollIntoView({block:'start'});
}
function copyArticle(){
  var c=cleanClone();
  var html='<meta charset="utf-8">'+c.innerHTML;
  var text=plainText(c);
  if(copyViaEvent(html, text)){ window.__lastCopy='event'; toast('已复制全文（含格式）。到 X 正文粘贴，图片按 [图N] 逐张补'); return; }
  if(navigator.clipboard && window.ClipboardItem && window.isSecureContext){
    var item;
    try{ item=new ClipboardItem({'text/html': new Blob([html],{type:'text/html'}),
                                 'text/plain': new Blob([text],{type:'text/plain'})}); }catch(e){ item=null; }
    var p=item ? navigator.clipboard.write([item]) : Promise.reject(new Error('no ClipboardItem'));
    p.then(function(){ window.__lastCopy='async'; toast('已复制全文（含格式）。到 X 正文粘贴，图片按 [图N] 逐张补'); })
     .catch(function(){
       return navigator.clipboard.writeText(text).then(function(){
         window.__lastCopy='text'; toast('只复制到了纯文本（浏览器拒绝富文本）。建议改用 Chrome/Safari 直接打开本文件再点一次', 4000);
       });
     })
     .catch(function(){ window.__lastCopy='select'; selectArticle(); toast('浏览器不允许自动复制，已帮你全选正文：按 Cmd+C（Windows 用 Ctrl+C）', 6000); });
    return;
  }
  window.__lastCopy='select'; selectArticle();
  toast('浏览器不允许自动复制，已帮你全选正文：按 Cmd+C（Windows 用 Ctrl+C）', 6000);
}
function copyPrompt(btn){
  var code=btn.parentElement.querySelector('code').innerText;
  if(copyViaEvent(code.replace(/[&<>]/g,function(ch){return {'&':'&amp;','<':'&lt;','>':'&gt;'}[ch];}).replace(/\\n/g,'<br>'), code)){
    toast('提示词已复制，去 AI 生图工具粘贴'); return; }
  if(navigator.clipboard && window.isSecureContext){
    navigator.clipboard.writeText(code).then(function(){ toast('提示词已复制，去 AI 生图工具粘贴'); })
      .catch(function(){ toast('复制失败，请手动选中复制', 4000); });
  }else{ toast('复制失败，请手动选中复制', 4000); }
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
/* 图片转 PNG Blob：剪贴板只稳定支持 image/png，JPEG 先过 canvas 转一次。 */
function pngBlob(img){
  return new Promise(function(resolve, reject){
    var src=img.src;
    if(/^data:image\\/png;base64,/.test(src)){
      try{ var bin=atob(src.split(',')[1]), arr=new Uint8Array(bin.length);
           for(var i=0;i<bin.length;i++){ arr[i]=bin.charCodeAt(i); }
           resolve(new Blob([arr],{type:'image/png'})); }catch(e){ reject(e); }
      return;
    }
    var cv=document.createElement('canvas'); cv.width=img.naturalWidth; cv.height=img.naturalHeight;
    cv.getContext('2d').drawImage(img,0,0);
    cv.toBlob(function(b){ b ? resolve(b) : reject(new Error('toBlob')); }, 'image/png');
  });
}
/* 复制图片：image/png 写进剪贴板，到 X 编辑器对应 [图N] 处 Cmd/Ctrl+V。
   ClipboardItem 直接收 Promise，write() 在点击的同步栈里发起（Safari 要求），不要先 await 再 write。
   file:// 或 iframe 预览里异步剪贴板常被禁，失败时提示改用「下载图片」。 */
function copyImg(btn){
  var fig=btn.closest('figure');
  var img=fig ? fig.querySelector('img') : document.querySelector('#coverbox img');
  if(!img){ toast('找不到图片'); return; }
  var name=btn.getAttribute('data-fname') || (fig && fig.querySelector('.cap') ? fig.querySelector('.cap').textContent : '图片');
  if(!(navigator.clipboard && window.ClipboardItem && window.isSecureContext)){
    toast('当前打开方式不允许复制图片：点「下载图片」再上传，或用 Chrome/Safari 直接打开本文件', 5000); return; }
  var p;
  try{ p=navigator.clipboard.write([new ClipboardItem({'image/png': pngBlob(img)})]); }
  catch(e){ p=pngBlob(img).then(function(b){ return navigator.clipboard.write([new ClipboardItem({'image/png': b})]); }); }
  p.then(function(){ window.__lastImgCopy='ok'; toast(name+' 已复制，到 X 编辑器对应位置粘贴'); })
   .catch(function(){ window.__lastImgCopy='fail'; toast('复制图片失败：点「下载图片」再上传', 5000); });
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
  <span class="hint">全文复制只带文字和格式，配图位置留 [图N]；到 X 里在每个 [图N] 处点该图下的「复制图片」粘贴（或「下载图片」后上传），再删掉 [图N]。封面单独上传。若提示已全选，按 Cmd+C。</span>
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


TABLE_MODE = {"images": False, "chrome": None, "count": 0, "tmp": None}
TABLE_IMG_CSS = (
    "body{margin:0;padding:24px;background:#fff;font-family:-apple-system,'PingFang SC','Noto Sans CJK SC',"
    "'Microsoft YaHei',sans-serif;}table{border-collapse:collapse;font-size:18px;line-height:1.5;color:#0f1419;}"
    "th,td{border:1px solid #cfd9de;padding:10px 16px;text-align:left;vertical-align:top;}"
    "th{background:#f7f9fa;font-weight:700;}tr:nth-child(even) td{background:#fbfcfd;}"
)


def find_chrome():
    """无头浏览器：CHROME_PATH 环境变量，或 PATH 里的 google-chrome / chromium。找不到返回 None。"""
    env = os.environ.get("CHROME_PATH")
    if env and os.path.isfile(env):
        return env
    for c in ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/Applications/Chromium.app/Contents/MacOS/Chromium"):
        if os.path.isfile(c):
            return c
    for name in ("google-chrome", "chromium", "chromium-browser", "msedge"):
        found = shutil.which(name)
        if found:
            return found
    return None


def chrome_shot(chrome, html_path, png_path, width, height=4000):
    """无头 Chrome 截图，再按内容裁掉底部和右侧空白（有 Pillow 才裁）。成功返回 True。"""
    cmd = [chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--disable-gpu-sandbox",
           "--hide-scrollbars", "--force-device-scale-factor=2", "--window-size=%d,%d" % (width, height),
           "--screenshot=%s" % png_path, "file://" + os.path.abspath(html_path)]
    try:
        subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    except (OSError, subprocess.TimeoutExpired):
        return False
    if not os.path.isfile(png_path):
        return False
    try:
        from PIL import Image, ImageChops
        im = Image.open(png_path).convert("RGB")
        bg = Image.new("RGB", im.size, im.getpixel((im.size[0] - 2, im.size[1] - 2)))
        box = ImageChops.difference(im, bg).getbbox()
        if box:
            pad = 24
            im.crop((0, 0, min(im.size[0], box[2] + pad), min(im.size[1], box[3] + pad))).save(png_path)
    except Exception:
        pass
    return True


def table_to_image(rows):
    """把一张表渲染成 PNG，返回 data URI；失败返回 None（调用方退回列表）。"""
    chrome = TABLE_MODE["chrome"]
    if not chrome:
        return None
    TABLE_MODE["count"] += 1
    n = TABLE_MODE["count"]
    tmp = TABLE_MODE["tmp"]
    head, rest = rows[0], rows[1:]
    th = "".join("<th>%s</th>" % inline_md(c) for c in head)
    trs = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % inline_md(c) for c in r) for r in rest)
    page = ("<!doctype html><html><head><meta charset='utf-8'><style>%s</style></head>"
            "<body><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></body></html>") % (TABLE_IMG_CSS, th, trs)
    hp = os.path.join(tmp, "table-%02d.html" % n)
    pp = os.path.join(tmp, "table-%02d.png" % n)
    with open(hp, "w", encoding="utf-8") as f:
        f.write(page)
    if not chrome_shot(chrome, hp, pp, 1200, 2400):
        return None
    return data_uri(pp)


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


IMG_LINE_RE = re.compile(r"^\s*!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)\s*$")


def inline_images(md_text, base):
    """把独占一行的 ![说明](本地路径) 换成 [图N]，返回 (新文本, 图片绝对路径列表)。

    围栏代码块里的行不动；远程图片无法内嵌，换成一行「（远程图片：url）」并告警。"""
    out, images, fence = [], [], None
    for line in md_text.split("\n"):
        st = line.strip()
        fm = re.match(r"^(`{3,})", st)
        if fm:
            if fence is None:
                fence = fm.group(1)
            elif len(fm.group(1)) >= len(fence) and st.strip("`") == "":
                fence = None
            out.append(line)
            continue
        m = IMG_LINE_RE.match(line) if fence is None else None
        if not m:
            out.append(line)
            continue
        src = m.group(2)
        if re.match(r"https?://", src):
            print("警告：跳过远程图片（无法内嵌）：%s" % src, file=sys.stderr)
            out.append("（远程图片：%s）" % src)
            continue
        images.append(src if os.path.isabs(src) else os.path.normpath(os.path.join(base, src)))
        out.append("[图%d]" % len(images))
    return "\n".join(out), images


def frontmatter_value(md_text, key):
    lines = md_text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    for ln in lines[1:]:
        if ln.strip() == "---":
            break
        m = re.match(r"^%s:\s*(.+?)\s*$" % re.escape(key), ln)
        if m:
            return m.group(1).strip().strip("\"'")
    return None


_FENCE_OPEN_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")


def strip_html_comments(text):
    """去掉正文里的 HTML 注释（<!-- … -->，可跨行）：写作提示、骨架备注不进渲染产物。
    围栏代码块和行内代码里的 <!-- 原样保留；整行只有注释的行直接删掉。"""
    out, fence, in_c = [], None, False
    for line in text.split("\n"):
        if not in_c:
            m = _FENCE_OPEN_RE.match(line)
            if fence is None and m:
                fence = m.group(1)
                out.append(line)
                continue
            if fence is not None:
                if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) \
                        and not line.strip()[len(m.group(1)):].strip():
                    fence = None
                out.append(line)
                continue
        res, rest = "", line
        while rest:
            if in_c:
                j = rest.find("-->")
                if j < 0:
                    rest = ""
                    break
                rest, in_c = rest[j + 3:], False
                if res.endswith(" ") and rest.startswith(" "):
                    rest = rest.lstrip(" ")
            else:
                j = rest.find("<!--")
                if j < 0:
                    res += rest
                    break
                if (res + rest[:j]).count("`") % 2 == 1:  # 行内代码里的 <!-- 不算注释
                    res, rest = res + rest[:j + 4], rest[j + 4:]
                    continue
                res, rest, in_c = res + rest[:j], rest[j + 4:], True
        if res == line:
            out.append(line)
        elif res.strip():
            out.append(res.rstrip())
    return "\n".join(out)


def md_to_html(md_text, images, cover):
    lines = strip_html_comments(md_text).split("\n")
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
        uri = table_to_image(rows) if (rows and TABLE_MODE["images"]) else None
        if uri:
            out.append('<p><img src="%s" alt="表格"></p>' % uri)
        elif rows:
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
        # 图片后的「来源：」行 → 小号灰字图注（上一个输出块是图片时）
        if re.match(r"^来源[：:]", s) and out and out[-1].startswith('<figure class="ximg"'):
            out.append('<p class="src">%s</p>' % inline_md(s))
            i += 1
            continue
        # 保留行首缩进（X 稿里用 emoji 项目符号表示二级条目时需要缩进）：
        # 行首 ≥2 个空格 / 全角空格转成 &nbsp;，避免 HTML 把缩进吞掉
        lead = len(line) - len(line.lstrip(" \u3000"))
        pad = "&nbsp;" * lead if lead >= 2 else ""
        out.append("<p>%s%s</p>" % (pad, inline_md(s)))
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
    ap.add_argument("md", help="原稿 markdown 路径（文章文件夹结构下就是 <文章名>.md）")
    ap.add_argument("--out", default=None, help="输出 HTML 路径（缺省 <md 所在目录>/out/X长文.html）")
    ap.add_argument("--images", nargs="*", default=[], help="[图N] 对应的图片路径（按顺序）")
    ap.add_argument("--images-from", default=None, metavar="WECHAT_MD",
                    help="从指定的 markdown（如旧结构的公众号稿.md）中按文档顺序提取 ![]() 本地图片路径，"
                         "作为 [图N] 的图片来源。缺省：源稿自己有 ![]() 就直接读它；"
                         "禁止手工拼 --images 顺序（曾因此出现配图错位）")
    ap.add_argument("--cover", default=None,
                    help="封面图路径（1500×600，5:2）；缺省读 frontmatter 的 cover（相对 md 所在目录）")
    ap.add_argument("--tables-as-images", action="store_true",
                    help="表格渲染成图片内嵌（X Article 不渲染表格；需要无头 Chrome，找不到时退回列表）")
    ap.add_argument("--preview", action="store_true",
                    help="另存一张图文预览长图 out/预览.png（需要无头 Chrome），交付时给用户看效果")
    args = ap.parse_args()

    if not os.path.isfile(args.md):
        print("输入文件不存在：%s" % args.md, file=sys.stderr)
        sys.exit(1)
    with open(args.md, encoding="utf-8") as f:
        md_text = f.read()
    md_dir = os.path.dirname(os.path.abspath(args.md))
    if not args.out:
        args.out = os.path.join(md_dir, "out", "X长文.html")
    if not args.cover:
        fc = frontmatter_value(md_text, "cover")
        if fc:
            cp = fc if os.path.isabs(fc) else os.path.normpath(os.path.join(md_dir, fc))
            if os.path.isfile(cp):
                args.cover = cp
            else:
                print("警告：frontmatter 的 cover 文件不存在，跳过封面：%s" % fc, file=sys.stderr)

    has_markers = any(re.fullmatch(r"\[图\d+\]", ln.strip()) for ln in md_text.split("\n"))
    if not has_markers and not args.images and not args.images_from:
        # 新结构：源稿只有 ![]()，直接按文档顺序取图
        md_text, derived = inline_images(md_text, md_dir)
        if derived:
            print("从源稿直接取图：%d 张" % len(derived), file=sys.stderr)
        args.images = derived
    elif has_markers and not args.images and not args.images_from:
        print("源稿里有 [图N] 但没给图片来源：加 --images-from <带 ![]() 的稿子>，"
              "或把 [图N] 换回 ![说明](images/xx.png)", file=sys.stderr)
        sys.exit(1)

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

    n_tables = sum(1 for ln in md_text.split("\n") if re.match(r"^\s*\|?\s*:?-{3,}", ln.strip()) and "|" in ln)
    if args.tables_as_images and n_tables:
        TABLE_MODE["chrome"] = find_chrome()
        TABLE_MODE["images"] = True
        TABLE_MODE["tmp"] = tempfile.mkdtemp(prefix="md2x-tables-")
        if not TABLE_MODE["chrome"]:
            print("警告：找不到无头浏览器（设 CHROME_PATH），表格退回列表写法", file=sys.stderr)
    body = md_to_html(md_text, images, args.cover)
    if TABLE_MODE["tmp"]:
        shutil.rmtree(TABLE_MODE["tmp"], ignore_errors=True)
    if n_tables and not args.tables_as_images:
        body = ('<div class="cover-note no-paste">本文有 %d 个表格：X 长文不渲染表格，粘贴后会变成列表。'
                '要保留表格的样子，加 --tables-as-images 重新生成。</div>\n' % n_tables) + body
    subtitle = frontmatter_value(md_text, "subtitle")
    if subtitle:
        body = ('<div class="cover-note no-paste" id="subtitlebox">副标题（不进复制内容，可用作推文文案）：%s</div>\n'
                % html.escape(subtitle)) + body
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
    if args.preview:
        chrome = find_chrome()
        prev = os.path.join(out_dir, "预览.png")
        if chrome and chrome_shot(chrome, args.out, prev, 800, 16000):
            print("图文预览：%s" % prev)
        else:
            print("警告：没生成图文预览（找不到无头浏览器，设 CHROME_PATH）", file=sys.stderr)


if __name__ == "__main__":
    main()
