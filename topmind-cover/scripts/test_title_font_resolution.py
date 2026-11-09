import os
from pathlib import Path
import runpy
import unittest
from unittest.mock import patch


TITLE = Path(__file__).with_name("title-engine.py")


class TitleFontTests(unittest.TestCase):
    def setUp(self):
        self.engine = runpy.run_path(str(TITLE))
        self.resolve = self.engine["resolve_alias"]
        self.fallback, self.index = self.engine["MAC_FONT_FALLBACKS"]["hei"]

    def test_local_noto_takes_priority_over_system_font(self):
        candidate = self.engine["FONTS"]["hei"][0][0]
        with patch("os.path.isfile", side_effect={candidate, self.fallback}.__contains__):
            self.assertEqual(self.resolve("hei"), (candidate, 0, "Bold"))

    def test_system_fallback_selects_the_actual_bold_face(self):
        with patch("os.path.isfile", side_effect={self.fallback}.__contains__):
            self.assertEqual(self.resolve("hei"), (self.fallback, 2, None))

    @unittest.skipUnless(os.path.isfile("/System/Library/Fonts/Hiragino Sans GB.ttc"), "macOS CJK face")
    def test_fallback_renders_hiragino_w6(self):
        actual = os.path.isfile
        with patch("os.path.isfile", side_effect=lambda p: p == self.fallback and actual(p)):
            font = self.engine["font"]("hei", 52)
        self.assertEqual(font.getname(), ("Hiragino Sans GB", "W6"))
        self.assertIsNotNone(font.getmask("擎").getbbox())


if __name__ == "__main__":
    unittest.main()
