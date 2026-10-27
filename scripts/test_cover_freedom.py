#!/usr/bin/env python3
"""Cover tool behavior: advisory style choices, explicit strict mode, valid render schema."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent / 'topmind-cover/scripts'


class CoverFreedomTests(unittest.TestCase):
    def check_spec(self, layers, *flags):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / 'spec.json'
            p.write_text(json.dumps({'layers': layers}, ensure_ascii=False))
            return subprocess.run([sys.executable, str(ROOT/'title-engine.py'), '--check', str(p), *flags], capture_output=True, text=True)

    def test_complex_author_layout_is_advisory_not_a_failure(self):
        layers=[{'type':'text', 'text':'可以不一样', 'size':0.12, 'role':'main', 'rotate':22, 'font':'hei', 'glow':{'color':'#FFF'}},
                {'type':'text', 'text':'精确的小字', 'size':0.035, 'role':'label', 'extrude':{'depth':0.1}}]
        layers += [{'type':'deco','kind':'star','x':0.2,'y':0.5}] * 5
        r=self.check_spec(layers)
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertIn('建议',r.stdout)
        self.assertEqual(self.check_spec(layers,'--strict').returncode,1)

    def test_structure_errors_fail_without_enabling_strict(self):
        cases=[[{'type':'unknown'}],[{'type':[]}],[{'text':''}],[{'text':'标题','size':0}],
               [{'text':'标题','size':'large'}],[{'text':'标题','size':float('nan')}],
               [{'text':'标题','role':[]}],[{'text':'标题','sizes':[]}],['not a layer']]
        for layers in cases:
            with self.subTest(layers=layers):
                r=self.check_spec(layers)
                self.assertEqual(r.returncode,1,r.stdout+r.stderr)
                self.assertNotIn('Traceback',r.stderr)

    def test_non_text_cover_is_a_valid_render_structure(self):
        r=self.check_spec([{'type':'deco','kind':'circle','x':0.5,'y':0.5}])
        self.assertEqual(r.returncode,0,r.stderr)

    def test_long_and_traditional_titles_remain_allowed(self):
        for title in ['重新理解我们与工具的关系，允许慢一点','鍵盤與生活','𠮷与未完成的故事']:
            r=subprocess.run([sys.executable,str(ROOT/'check-title.py'),title,'--json'],capture_output=True,text=True)
            self.assertEqual(r.returncode,0,r.stderr)
            payload=json.loads(r.stdout)
            self.assertTrue(payload['advisory'])
            self.assertIn(title,payload['items'])
        r=subprocess.run([sys.executable,str(ROOT/'check-title.py')],capture_output=True,text=True)
        self.assertNotEqual(r.returncode,0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
