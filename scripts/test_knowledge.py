#!/usr/bin/env python3
"""Knowledge CLI behavior: scoped retrieval, provenance, bounded reads and candidate writes."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
CLI = ROOT / 'shared/scripts/knowledge.py'


class KnowledgeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.pack = self.root / 'pack'
        (self.pack / 'cards').mkdir(parents=True)
        entries = []
        for id, skill, state in [('fonts', 'topmind-cover', 'active'), ('pending', 'topmind-cover', 'candidate'),
                                 ('old', 'topmind-cover', 'retired'), ('story', 'topmind-wechat-post', 'active')]:
            (self.pack / 'cards' / f'{id}.md').write_text('BODY_ONLY_VALUE\n' + ('示例正文。' * 120))
            entries.append(dict(id=id, title='字体与空间' if skill == 'topmind-cover' else '叙事与场景',
                summary='字体排版的具体方向', skills=[skill], tags=['字体', '排版'], kind='example',
                evidence='illustrative', status=state, scope='当前练习', limits='不证明效果',
                path=f'cards/{id}.md', sources=[{'kind':'original', 'ref':'Teaching example'}]))
        self.data = dict(schema_version=1, id='fixture', version='1.0.0', entries=entries)
        self.write_index()

    def write_index(self):
        (self.pack / 'index.json').write_text(json.dumps(self.data, ensure_ascii=False))

    def run_cli(self, command, *args, pack=None):
        return subprocess.run([sys.executable, str(CLI), command, '--pack', str(pack or self.pack), *args],
                              capture_output=True, text=True, timeout=15)

    def test_builtin_pack_valid_and_chinese_task_retrieves_relevant_cards(self):
        r = subprocess.run([sys.executable, str(CLI), 'validate'], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        r = subprocess.run([sys.executable, str(CLI), 'search', '优雅 字体 字号', '--skill', 'topmind-cover', '--json'], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        cards = json.loads(r.stdout)
        self.assertIn('cover-typography', [card['id'] for card in cards])
        self.assertTrue(all('topmind-cover' in card['skills'] or '*' in card['skills'] for card in cards))

    def test_scope_state_and_metadata_only_search(self):
        r = self.run_cli('search', '字体', '--skill', 'topmind-cover', '--json')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual([c['id'] for c in json.loads(r.stdout)], ['fonts'])
        self.assertNotIn('BODY_ONLY_VALUE', r.stdout)
        r = self.run_cli('search', '字体', '--skill', 'topmind-cover', '--include-candidates', '--json')
        self.assertEqual({c['id'] for c in json.loads(r.stdout)}, {'fonts', 'pending'})

    def test_explicit_show_labels_state_and_truncation(self):
        r = self.run_cli('show', 'pending', '--max-chars', '180')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('candidate', r.stdout)
        self.assertIn('illustrative', r.stdout)
        self.assertIn('Truncated', r.stdout)
        self.assertLess(len(r.stdout), 340)

    def test_unmatched_query_has_no_invented_suggestion(self):
        r = self.run_cli('search', 'zxq-unmatched', '--json')
        self.assertEqual(json.loads(r.stdout), [])

    def test_traversal_absolute_and_symlink_paths_rejected(self):
        outside = self.root / 'private.md'
        outside.write_text('DO_NOT_READ')
        for path in ['../private.md', str(outside), 'cards\\outside.md']:
            with self.subTest(path=path):
                self.data['entries'][0]['path'] = path
                self.write_index()
                r = self.run_cli('validate')
                self.assertEqual(r.returncode, 2)
                self.assertNotIn('DO_NOT_READ', r.stdout + r.stderr)
                self.assertNotIn('Traceback', r.stderr)
        alias = self.pack / 'cards/alias.md'
        alias.symlink_to(outside)
        self.data['entries'][0]['path'] = 'cards/alias.md'
        self.write_index()
        self.assertEqual(self.run_cli('validate').returncode, 2)

    def test_catalog_symlink_outside_pack_rejected(self):
        other = self.root / 'outside.json'
        other.write_text(json.dumps(self.data))
        (self.pack / 'index.json').unlink()
        (self.pack / 'index.json').symlink_to(other)
        self.assertEqual(self.run_cli('validate').returncode, 2)

    def add(self, pack, id='note', pack_id='private-notes'):
        body = self.root / 'body.md'
        body.write_text('场景、选择、结果、例外；仅为一次观察。')
        return self.run_cli('add', '--id', id, '--pack-id', pack_id, '--title', '字体反馈',
            '--summary', '一次局部选择', '--skills', 'topmind-cover', '--tags', '字体,反馈',
            '--body', str(body), '--scope', '当前技术随笔', '--limits', '没有效果测量', pack=pack)

    def test_capture_is_candidate_no_overwrite_and_search_opt_in(self):
        local = self.root / 'local'
        r = self.add(local)
        self.assertEqual(r.returncode, 0, r.stderr)
        data = json.loads((local / 'index.json').read_text())
        self.assertEqual(data['entries'][0]['status'], 'candidate')
        self.assertEqual(data['entries'][0]['evidence'], 'unverified')
        before = (local / 'cards/note.md').read_bytes()
        self.assertEqual(self.add(local).returncode, 2)
        self.assertEqual((local / 'cards/note.md').read_bytes(), before)
        r = self.run_cli('search', '字体', '--json', pack=local)
        self.assertEqual(json.loads(r.stdout), [])
        r = self.run_cli('search', '字体', '--json', '--include-candidates', pack=local)
        self.assertEqual(len(json.loads(r.stdout)), 1)

    def test_add_refuses_bundled_directory(self):
        local = self.root / 'topmind-cover/knowledge'
        local.parent.mkdir()
        (local.parent / 'SKILL.md').write_text('fixture')
        self.assertEqual(self.add(local).returncode, 2)
        self.assertFalse(local.exists())

    def test_invalid_capture_rolls_back_and_lock_prevents_concurrent_writes(self):
        local = self.root / 'rollback'
        self.assertEqual(self.add(local, pack_id='INVALID PACK').returncode, 2)
        self.assertFalse((local / 'cards/note.md').exists())
        self.assertFalse((local / 'index.json').exists())
        (local / '.write-lock').mkdir()
        self.assertEqual(self.add(local).returncode, 2)
        self.assertFalse((local / 'cards/note.md').exists())

    def test_duplicate_catalog_id_and_missing_body_fail_cleanly(self):
        self.data['entries'].append(copy.deepcopy(self.data['entries'][0]))
        self.write_index()
        r = self.run_cli('validate')
        self.assertEqual(r.returncode, 2)
        self.assertNotIn('Traceback', r.stderr)
        self.data['entries'].pop()
        self.data['entries'][0]['path'] = 'cards/missing.md'
        self.write_index()
        self.assertEqual(self.run_cli('validate').returncode, 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
