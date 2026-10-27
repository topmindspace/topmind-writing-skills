#!/usr/bin/env python3
"""Release validation rejects omissions, source drift and undocumented archive files."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

spec = importlib.util.spec_from_file_location('release_check', Path(__file__).with_name('check_release_artifacts.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ReleaseArtifactTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skill = self.root / 'fixture'
        (self.skill / 'dist').mkdir(parents=True)
        self.contents = {'SKILL.md': '# fixture', 'README.md': '说明', 'README.en.md': 'Instructions',
                         'package.json': json.dumps({'name':'fixture','version':'0.1.0'}),
                         'scripts/knowledge.py': '# reader',
                         'knowledge/index.json': json.dumps({'entries':[{'id':'one','path':'cards/one.md'}]}),
                         'knowledge/cards/one.md': '范围与例外'}
        for name, content in self.contents.items():
            p = self.skill / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content)

    def archive(self, contents=None):
        contents = self.contents if contents is None else contents
        path = self.skill / 'dist/fixture.zip'
        with zipfile.ZipFile(path, 'w') as archive:
            for name, content in contents.items():
                archive.writestr('fixture/' + name, content)
        data = dict(name='fixture', version='0.1.0', files=len(contents), entries=list(contents),
                    sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        (self.skill / 'dist/fixture.manifest.json').write_text(json.dumps(data))

    def test_valid_payload_matches_source(self):
        self.archive()
        self.assertEqual(module.check_skill(self.root, 'fixture'), len(self.contents))

    def test_missing_bilingual_document_or_card_fails_even_with_a_valid_checksum(self):
        for name in ['README.en.md', 'knowledge/cards/one.md']:
            with self.subTest(name=name):
                self.archive({k:v for k,v in self.contents.items() if k != name})
                with self.assertRaises(ValueError):module.check_skill(self.root, 'fixture')

    def test_changed_payload_cannot_be_hidden_by_recomputing_checksum(self):
        self.archive({**self.contents, 'README.md':'changed'})
        with self.assertRaisesRegex(ValueError, 'payload differs'):module.check_skill(self.root, 'fixture')

    def test_generated_archive_content_is_rejected(self):
        self.archive({**self.contents, '__pycache__/cache.pyc':'garbage'})
        with self.assertRaisesRegex(ValueError, 'generated/private'):module.check_skill(self.root, 'fixture')


if __name__ == '__main__':
    unittest.main(verbosity=2)
