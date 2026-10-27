#!/usr/bin/env python3
"""真实打包回归：重复执行、双语文档与产物排除，源目录禁用文件仍报错。"""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

SOURCE = Path(__file__).resolve().parent.parent / "shared" / "scripts" / "package_skill.py"


class SkillPackagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.skill = Path(self.temp.name) / "fixture"
        (self.skill / "scripts").mkdir(parents=True)
        shutil.copy2(SOURCE, self.skill / "scripts" / "package_skill.py")
        (self.skill / "SKILL.md").write_text('---\nname: fixture\ndescription: "A test skill"\n---\n\nTest.\n')
        (self.skill / "README.md").write_text("中文说明\n")
        (self.skill / "README.en.md").write_text("English instructions\n")
        (self.skill / "package.json").write_text(json.dumps({"name": "fixture", "version": "0.1.0"}))
        (self.skill / "knowledge/cards").mkdir(parents=True)
        (self.skill / "knowledge/index.json").write_text('{"entries":[]}')
        (self.skill / "knowledge/cards/note.md").write_text("有范围的经验")

    def run_pack(self, *args):
        return subprocess.run([sys.executable, str(self.skill / "scripts" / "package_skill.py"), *args],
                              capture_output=True, text=True, timeout=30)

    def test_repeated_pack_and_check_keep_outputs_outside_archive(self):
        for args in [(), ("--check",), ()]:
            r = self.run_pack(*args)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        with zipfile.ZipFile(self.skill / "dist" / "fixture.zip") as archive:
            names = archive.namelist()
            self.assertIn("fixture/README.en.md", names)
            self.assertIn("fixture/knowledge/index.json", names)
            self.assertIn("fixture/knowledge/cards/note.md", names)
            self.assertFalse(any("/dist/" in name for name in names))
            self.assertEqual(archive.read("fixture/README.md").decode(), "中文说明\n")

    def test_source_secrets_and_nested_dist_are_still_rejected(self):
        for rel in [".env", "scripts/_private.py", "assets/dist/bundle.js"]:
            with self.subTest(path=rel):
                p = self.skill / rel
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text("fixture only")
                r = self.run_pack("--check")
                self.assertNotEqual(r.returncode, 0)
                self.assertIn(rel, r.stdout)
                p.unlink()


if __name__ == "__main__":
    unittest.main(verbosity=2)
