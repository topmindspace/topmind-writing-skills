#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""技能分发包打包器（发布前完整性校验 + 发布清单）。

用法:
    python scripts/package_skill.py            # 校验 → 打包 → 写发布清单
    python scripts/package_skill.py --check    # 只校验不打包（CI / 提交前自检）

产物:
    dist/<skill>.zip            分发包（解压目录名 = 技能名）
    dist/<skill>.manifest.json  发布清单（版本 / 条目 / 大小 / SHA-256）

校验（任一不过 → 退出码 1）:
    · SKILL.md frontmatter 含 name / description；name 与目录名一致；
      description ≤ 1024 字符（平台截断阈值）
    · README.md / package.json 存在；package.json name 与技能名一致
    · scripts/*.py 全部可编译；references/*.md 非空
    · SKILL.md 引用的 references/<file> 全部存在
    · 无 scripts/_* / __pycache__ / .env 等不应进包的文件
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
NAME = ROOT.name
OUT = ROOT / "dist" / f"{NAME}.zip"
MANIFEST = ROOT / "dist" / f"{NAME}.manifest.json"
DESC_LIMIT = 1024

INCLUDE = ["SKILL.md", "README.md", "package.json", "assets/", "references/", "scripts/", "evals/", "agents/"]
EXCLUDE_RES = [
    re.compile(r"(^|/)scripts/_"),
    re.compile(r"(^|/)\.env($|\.)"),
    re.compile(r"(^|/)node_modules(/|$)"),
    re.compile(r"(^|/)dist(/|$)"),
]

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)
    print(f"  ✗ {msg}")


def ok(msg: str) -> None:
    print(f"  ✓ {msg}")


def read_frontmatter() -> dict:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"^---\r?\n([\s\S]*?)\r?\n---", text)
    if not m:
        fail("SKILL.md 缺 frontmatter")
        return {}
    fm = m.group(1)
    name = re.search(r"^name:\s*(\S+)\s*$", fm, re.M)
    desc = ""
    dm = re.search(r'^description:\s*"([^"]*)"\s*$', fm, re.M)
    if dm:
        desc = dm.group(1).strip()
    else:
        dm = re.search(r"^description:\s*>\-\s*\n((?:[ \t]+.*\n?)+)", fm, re.M)
        if dm:
            desc = " ".join(line.strip() for line in dm.group(1).splitlines() if line.strip())
    return {"name": name.group(1) if name else "", "description": desc}


def check() -> bool:
    print(f"[check] {NAME}")
    fm = read_frontmatter()
    if fm.get("name") != NAME:
        fail(f"frontmatter name={fm.get('name')!r} 与目录名 {NAME!r} 不一致")
    else:
        ok("name 与目录名一致")
    desc = fm.get("description", "")
    if not desc:
        fail("description 为空")
    elif len(desc) > DESC_LIMIT:
        fail(f"description {len(desc)} 字符，超过 {DESC_LIMIT}")
    else:
        ok(f"description {len(desc)} 字符")

    for f in ("README.md", "package.json"):
        if not (ROOT / f).is_file():
            fail(f"缺 {f}")
        else:
            ok(f"有 {f}")
    try:
        pkg = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        if pkg.get("name") != NAME:
            fail(f"package.json name={pkg.get('name')!r} 与技能名不一致")
        if not re.match(r"^\d+\.\d+\.\d+", str(pkg.get("version", ""))):
            fail("package.json version 非 semver")
    except (OSError, json.JSONDecodeError) as e:
        fail(f"package.json 解析失败: {e}")

    for p in ROOT.rglob("*"):
        if not p.is_file() or ".git" in p.parts:
            continue
        rel = p.relative_to(ROOT).as_posix()
        for rx in EXCLUDE_RES:
            if rx.search(rel):
                fail(f"不应进包的文件: {rel}")
                break
    ok("无禁用文件")

    for py in sorted((ROOT / "scripts").glob("*.py")):
        try:
            compile(py.read_text(encoding="utf-8"), str(py), "exec")
        except SyntaxError as e:
            fail(f"{py.name} 编译失败: {e}")
    ok("scripts/*.py 编译通过")

    refdir = ROOT / "references"
    if refdir.is_dir():
        for md in sorted(refdir.glob("*.md")):
            if md.stat().st_size == 0:
                fail(f"references/{md.name} 为空")
        skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        for ref in sorted(set(re.findall(r"references/([\w\-.]+\.md)", skill_text))):
            if not (refdir / ref).is_file():
                fail(f"SKILL.md 引用的 references/{ref} 不存在")
        ok("references 完整性通过")

    if errors:
        print(f"\n[check] {NAME}: {len(errors)} 项失败")
        return False
    print(f"\n[check] {NAME}: 全部通过")
    return True


def package() -> None:
    if not check():
        sys.exit(1)
    (ROOT / "dist").mkdir(exist_ok=True)
    entries: list[str] = []
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(ROOT.rglob("*")):
            if not p.is_file() or ".git" in p.parts:
                continue
            rel = p.relative_to(ROOT)
            rel_posix = rel.as_posix()
            if any(rx.search(rel_posix) for rx in EXCLUDE_RES):
                continue
            if not any(
                rel_posix == inc.rstrip("/") or rel_posix.startswith(inc)
                for inc in INCLUDE
                if inc.endswith("/")
            ) and rel_posix not in INCLUDE:
                continue
            z.write(p, arcname=f"{NAME}/{rel_posix}")
            entries.append(rel_posix)
    sha = hashlib.sha256(OUT.read_bytes()).hexdigest()
    pkg = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    manifest = {
        "name": NAME,
        "version": pkg.get("version"),
        "built_at": datetime.now(timezone.utc).isoformat(),
        "files": len(entries),
        "sha256": sha,
        "entries": entries,
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[package] {OUT} ({len(entries)} 文件, sha256={sha[:12]}…)")


def main() -> None:
    if "--check" in sys.argv[1:]:
        sys.exit(0 if check() else 1)
    package()


if __name__ == "__main__":
    main()
