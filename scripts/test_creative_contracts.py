#!/usr/bin/env python3
"""Exercise observable author-intent and fidelity behavior through the shipped CLIs."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / 'shared' / 'scripts'


class CreativeContracts(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)

    def run_cli(self, script, text, *args):
        src = self.base / 'input.txt'
        src.write_text(text, encoding='utf-8')
        return subprocess.run([sys.executable, str(SCRIPTS / script), str(src), *args],
                              capture_output=True, text=True, timeout=15)

    def test_default_format_keeps_links_attribution_and_certainty(self):
        text = '厂商称耗时约 0.3 秒，仅限内部样本。\n来源：https://example.com/test?q=1&v=2\n'
        for mode in ('short', 'duanzi'):
            with self.subTest(mode=mode):
                result = self.run_cli('format_text.py', text, '--mode', mode)
                self.assertEqual(result.returncode, 0, result.stderr)
                for part in ('厂商称', '约 0.3 秒', '仅限内部样本', 'https://example.com/test?q=1&v=2'):
                    self.assertIn(part, result.stdout)

    def test_duanzi_keeps_opposition_and_emoji_sequences(self):
        text = '✅保留原文件\n❌删除所有记录\n程序员👩🏽‍💻今天休息🙂\n'
        result = self.run_cli('format_text.py', text, '--mode', 'duanzi')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, '✅保留原文件\n\n❌删除所有记录\n\n程序员👩🏽‍💻今天休息🙂\n')

    def test_author_requested_decoration_works_in_duanzi(self):
        result = self.run_cli('format_text.py', '今天打卡\n明天继续\n', '--mode', 'duanzi',
                              '--open', '🐱', '--close', '🌱')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('今天打卡 🐱', result.stdout)
        self.assertIn('明天继续 🌱', result.stdout)

    def test_explicit_separation_preserves_extracted_material(self):
        links = self.base / 'links.txt'
        text = '厂商测试约 80%。\n来源：https://example.com/report\n[图1] 测试截图\n'
        result = self.run_cli('format_text.py', text, '--mode', 'short', '--separate-links',
                              '--links-out', str(links))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, '厂商测试约 80%。\n')
        self.assertIn('来源：https://example.com/report', links.read_text())
        self.assertIn('[图1] 测试截图', links.read_text())

    def test_explicit_strip_is_optional(self):
        result = self.run_cli('format_text.py', '今天有进展🙂\n', '--mode', 'duanzi', '--strip-emoji')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, '今天有进展\n')

    def test_literal_lists_and_useful_links_do_not_block(self):
        text = '安装说明\n\n- 下载文件\n1. 运行安装器\n来源：https://example.com/download\n'
        result = self.run_cli('lint_x_post.py', text)
        self.assertEqual(result.returncode, 0, result.stdout)
        for code in ('W27', 'W28', 'W29', 'W30'):
            self.assertIn('[' + code + ']', result.stdout)
        self.assertNotIn('[E', result.stdout)

    def test_link_contract_can_be_requested_explicitly(self):
        text = '来源：https://example.com/report\n'
        result = self.run_cli('lint_x_post.py', text, '--separate-links')
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn('[E10]', result.stdout)
        self.assertIn('[E11]', result.stdout)
        long_result = self.run_cli('lint_x_post.py', text, '--long', '--separate-links')
        self.assertEqual(long_result.returncode, 0, long_result.stdout)

    def test_duanzi_emoji_is_advisory_even_under_strict(self):
        result = self.run_cli('lint_x_post.py', '今天完成了🙂\n', '--duanzi', '--strict')
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn('[H22]', result.stdout)

    def test_actual_placeholder_and_broken_markers_still_report(self):
        result = self.run_cli('lint_x_post.py', '```text\n**草稿**\n[图1]\n```\n')
        self.assertEqual(result.returncode, 1, result.stdout)
        for code in ('E8', 'E4', 'E12'):
            self.assertIn('[' + code + ']', result.stdout)

    def test_missing_input_fails_cleanly(self):
        for script in ('format_text.py', 'lint_x_post.py'):
            args = ['--mode', 'short'] if script == 'format_text.py' else []
            result = subprocess.run([sys.executable, str(SCRIPTS / script),
                                     str(self.base / 'missing.txt'), *args],
                                    capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn('Traceback', result.stderr)

    def test_bad_metadata_still_fails_without_fixed_heading_requirements(self):
        target = self.base / 'skill'
        (target / 'scripts').mkdir(parents=True)
        (target / 'scripts' / 'audit_skill.py').write_bytes((SCRIPTS / 'audit_skill.py').read_bytes())
        for body, expected in [('no metadata\n', 1), ('''---
name: demo-skill
description: "Create short copy for a stated audience."
metadata:
  triggers: "copy"
---

# Copy

Use the supplied material to deliver the requested text.
''', 0)]:
            (target / 'SKILL.md').write_text(body)
            result = subprocess.run([sys.executable, str(target / 'scripts' / 'audit_skill.py')],
                                    capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, expected, result.stdout)
            self.assertNotIn('Traceback', result.stderr)


if __name__ == '__main__':
    unittest.main()
