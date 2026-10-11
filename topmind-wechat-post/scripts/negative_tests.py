#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""topmind-wechat-post 异常输入测试：各脚本错误路径干净（任一失败 → 退出码 1）。"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
PY = sys.executable
fails: list[str] = []


def run(script: str, args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run([PY, str(SCRIPTS / script), *args], capture_output=True, text=True, timeout=60)


def check(name: str, cond: bool, detail: str = "") -> None:
    print(("  ✓ " if cond else "  ✗ ") + name + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        fails.append(name)


def main() -> None:
    print("[negative_tests] topmind-wechat-post")
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)

        # 1. lint 空文件不崩溃
        (td / "empty.md").write_text("", encoding="utf-8")
        r = run("lint-wechat.py", ["--input", str(td / "empty.md")])
        check("lint 空文件不崩溃", r.returncode == 0 and "Traceback" not in r.stderr, r.stderr[:100])

        # 2. md2wechat 缺失输入 → 非零干净报错
        r = run("md2wechat.py", ["--input", str(td / "nope.md"), "--out-dir", str(td), "--slug", "t"])
        check("md2wechat 缺失输入干净报错", r.returncode != 0 and "Traceback" not in r.stderr, r.stderr[:100])

        # 3. scan 空文件不崩溃
        r = run("scan_ai_flavor.py", [str(td / "empty.md")])
        check("scan 空文件不崩溃", r.returncode == 0 and "Traceback" not in r.stderr, r.stderr[:100])

        # 4. new-article --help 正常
        r = run("new-article.py", ["--help"])
        check("new-article --help 正常", r.returncode == 0, r.stderr[:100])

        # 5. sync-status 缺失包 → 非零干净报错
        r = run("sync-status.py", ["--set", "定稿", str(td / "nope-pkg")])
        check("sync-status 缺失包干净报错", r.returncode != 0 and "Traceback" not in r.stderr, r.stderr[:100])

        # 6. md2wechat 行内图片走图片管线（复制/embed/清单/计数）
        png = ("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk"
               "+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==")
        import base64 as _b64
        (td / "a.png").write_bytes(_b64.b64decode(png))
        (td / "inline.md").write_text(
            "# t\n\n段落 ![行内图](a.png) 后续文字。\n", encoding="utf-8")
        r = run("md2wechat.py", ["--input", str(td / "inline.md"),
                                 "--out-dir", str(td / "o6"), "--slug", "t6",
                                 "--embed-images"])
        html = (td / "o6" / "t6-公众号版.html").read_text(encoding="utf-8")
        manifest = (td / "o6" / "图片上传清单.md").read_text(encoding="utf-8")
        check("md2wechat 行内图片被内嵌", r.returncode == 0 and
              "data:image/png;base64," in html, r.stdout[:200])
        check("md2wechat 行内图片进清单", "a.png" in manifest)

        # 7. md2wechat 大写数字序号同样被剥离
        (td / "num.md").write_text(
            "# t\n\n## 第叁章 大写序号\n\n正文。\n", encoding="utf-8")
        r = run("md2wechat.py", ["--input", str(td / "num.md"),
                                 "--out-dir", str(td / "o7"), "--slug", "t7"])
        html = (td / "o7" / "t7-公众号版.html").read_text(encoding="utf-8")
        check("md2wechat 大写数字序号剥离",
              "第叁章" not in html and ">01</span>" in html)

        # 8. md2wechat 分隔线不触发自家合规 WARN（inline-block）
        (td / "hr.md").write_text("# t\n\n---\n\n正文。\n", encoding="utf-8")
        r = run("md2wechat.py", ["--input", str(td / "hr.md"),
                                 "--out-dir", str(td / "o8"), "--slug", "t8"])
        check("md2wechat 分隔线无 inline-block 告警",
              "inline-block" not in r.stdout, r.stdout[:200])

        # 9. 括号 URL 不被截断（链接与图片；历史 bug：`![a](img(1).png)` 被截成
        #    `img(1` 导致真实文件记成缺失；`[维基](…/猫_(动物))` 的 URL 被截断、
        #    正文多个悬挂 `)`；`[t](url "title")` 被原样保留）
        (td / "img(1).png").write_bytes(_b64.b64decode(png))
        (td / "paren.md").write_text(
            "# t\n\n![括号图](img(1).png)\n\n"
            "[维基](https://zh.wikipedia.org/wiki/猫_(动物)) 与 "
            "[带title](https://example.com/a \"标题文字\")。\n",
            encoding="utf-8")
        r = run("md2wechat.py", ["--input", str(td / "paren.md"),
                                 "--out-dir", str(td / "o9"), "--slug", "t9",
                                 "--no-toc", "--signature", "off"])
        html = (td / "o9" / "t9-公众号版.html").read_text(encoding="utf-8")
        check("md2wechat 括号图片不截断",
              'src="images/img(1).png"' in html and (td / "o9" / "images" / "img(1).png").exists(),
              r.stdout[:200])
        check("md2wechat 括号链接不截断",
              "猫_(动物)" in html and ")</sup>" not in html,
              r.stdout[:200])
        check("md2wechat title 链接被转换",
              "https://example.com/a" in html and '[带title](' not in html,
              r.stdout[:200])

        # 10. 脚注 URL 的 & 不双重转义（历史 bug：显示成 &amp;）
        (td / "amp.md").write_text(
            "# t\n\n[和号](https://x.com/?a=1&b=2)\n", encoding="utf-8")
        r = run("md2wechat.py", ["--input", str(td / "amp.md"),
                                 "--out-dir", str(td / "o10"), "--slug", "t10",
                                 "--no-toc", "--signature", "off"])
        html = (td / "o10" / "t10-公众号版.html").read_text(encoding="utf-8")
        check("md2wechat 脚注 URL 不双重转义",
              "a=1&amp;b=2" in html and "&amp;amp;" not in html)

        # 11. 坏主题 JSON 干净报错（历史 crash：json Traceback）
        (td / "bad-theme.json").write_text("{bad json", encoding="utf-8")
        (td / "t11.md").write_text("# t\n\n正文。\n", encoding="utf-8")
        r = run("md2wechat.py", ["--input", str(td / "t11.md"),
                                 "--out-dir", str(td / "o11"), "--slug", "t11",
                                 "--theme", str(td / "bad-theme.json")])
        check("md2wechat 坏主题 JSON 干净报错",
              r.returncode != 0 and "Traceback" not in r.stderr, r.stderr[:100])

        # 12. 目录当输入：文案明确（与 md2x 一致），非零干净退出
        r = run("md2wechat.py", ["--input", str(td),
                                 "--out-dir", str(td / "o12"), "--slug", "t12"])
        check("md2wechat 目录输入文案正确",
              r.returncode != 0 and "输入是目录不是文件" in r.stderr
              and "Traceback" not in r.stderr, r.stderr[:100])

        # 13. yaml/diff 代码块不高亮 crash（历史 crash：(?m) 拼进 alternation
        #     报 "global flags not at the start"，任何 ```yaml 块都 Traceback）
        (td / "hl.md").write_text(
            "# t\n\n```yaml\nkey: value\n```\n\n```diff\n+add\n-del\n```\n",
            encoding="utf-8")
        r = run("md2wechat.py", ["--input", str(td / "hl.md"),
                                 "--out-dir", str(td / "o13"), "--slug", "t13"])
        html = (td / "o13" / "t13-公众号版.html").read_text(encoding="utf-8")
        check("md2wechat yaml/diff 代码块不崩溃",
              r.returncode == 0 and "Traceback" not in r.stderr
              and "key" in html, r.stderr[:100])

        # 14. 嵌套围栏：```` 开栏不被内层 ``` 提前闭合
        (td / "nest.md").write_text(
            "# t\n\n````markdown\n外层\n```python\nprint(1)\n```\n结束\n````\n",
            encoding="utf-8")
        r = run("md2wechat.py", ["--input", str(td / "nest.md"),
                                 "--out-dir", str(td / "o14"), "--slug", "t14",
                                 "--no-toc", "--signature", "off"])
        html = (td / "o14" / "t14-公众号版.html").read_text(encoding="utf-8")
        body = html.split('<article id="wx-body"')[1]
        check("md2wechat 嵌套围栏不提前闭合",
              r.returncode == 0 and "````markdown" not in body
              and body.count("MARKDOWN</section>") == 1, r.stderr[:100])

        # 15. scan 转发器：找不到 canonical 时回落内置实现并提示缺姿态分
        import os as _os
        env = {k: v for k, v in _os.environ.items()
               if k not in ("QU_AIWEI_SCAN", "QU_AIWEI_SKILLS_DIRS")}
        env["HOME"] = str(td)  # 隔离用户级技能目录
        (td / "s.md").write_text("这是一段测试文字。\n", encoding="utf-8")
        r = subprocess.run([PY, str(SCRIPTS / "scan_ai_flavor.py"), str(td / "s.md")],
                           capture_output=True, text=True, timeout=60, env=env, cwd=str(td))
        check("scan 转发器回落内置实现且提示缺姿态分",
              r.returncode == 0 and "作者姿态分" in r.stderr and "Traceback" not in r.stderr,
              r.stderr[:200])
        r = subprocess.run([PY, str(SCRIPTS / "scan_ai_flavor.py"), "--require-canonical", str(td / "s.md")],
                           capture_output=True, text=True, timeout=60, env=env, cwd=str(td))
        check("scan --require-canonical 找不到 canonical 退出 3", r.returncode == 3, r.stderr[:200])

        # 16. scan 转发器：QU_AIWEI_SCAN 指向 canonical 时原样转发参数与退出码
        fake = td / "fake_scan.py"
        fake.write_text("import sys\nprint('FAKE', *sys.argv[1:])\nsys.exit(7)\n", encoding="utf-8")
        env2 = dict(env, QU_AIWEI_SCAN=str(fake))
        r = subprocess.run([PY, str(SCRIPTS / "scan_ai_flavor.py"), "--json", "x.md"],
                           capture_output=True, text=True, timeout=60, env=env2, cwd=str(td))
        check("scan 转发器透传参数与退出码", r.returncode == 7 and "FAKE --json x.md" in r.stdout,
              r.stdout[:200])

        # 17. 路径解析：无 --base / 环境变量时干净报错，不猜个人路径
        env3 = {k: v for k, v in env.items()
                if k not in ("TOPMIND_WORKSPACE", "TOPMIND_WECHAT_BASE", "TOPMIND_WECHAT_PACKAGE_ROOT")}
        r = subprocess.run([PY, str(SCRIPTS / "new-article.py"), "--slug", "测试", "--title", "T"],
                           capture_output=True, text=True, timeout=60, env=env3, cwd=str(td))
        check("new-article 无路径配置时干净报错",
              r.returncode != 0 and "--base" in (r.stderr + r.stdout) and "Traceback" not in r.stderr,
              r.stderr[:200])

        # 18. 路径解析：按类别名称发现（不写死编号），专题用当年
        import datetime as _dt
        ws = td / "ws"
        for d in ("00-收件箱", "20-长文", "88-输出"):
            (ws / d).mkdir(parents=True)
        env4 = dict(env3, TOPMIND_WORKSPACE=str(ws))
        r = subprocess.run([PY, str(SCRIPTS / "new-article.py"), "--slug", "测试", "--title", "T",
                            "--date", "2026-01-02"],
                           capture_output=True, text=True, timeout=60, env=env4, cwd=str(td))
        want = ws / "20-长文" / ("%d-公众号" % _dt.date.today().year) / "2026-01-02-测试" / "公众号稿.md"
        check("new-article 按名称发现长文类别 + 当年专题", r.returncode == 0 and want.is_file(),
              (r.stdout + r.stderr)[:200])
        if want.is_file():
            fmtxt = want.read_text(encoding="utf-8")
            check("骨架 frontmatter 的 category/topic 取实际目录名",
                  "category: 20-长文" in fmtxt and ("topic: %d-公众号" % _dt.date.today().year) in fmtxt)

        # 19. audit-provenance 参数错误干净退出（退出码 2）
        r = run("audit-provenance.py", ["--draft", str(td / "nope.md"), "--source", str(td / "nope2.md")])
        check("audit-provenance 缺文件退出 2 且无 Traceback",
              r.returncode == 2 and "Traceback" not in r.stderr, (r.stderr + r.stdout)[:200])

    if fails:
        print(f"\n[negative_tests] {len(fails)} 项失败")
        sys.exit(1)
    print("\n[negative_tests] 全部通过")


if __name__ == "__main__":
    main()
