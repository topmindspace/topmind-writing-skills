#!/usr/bin/env python3
"""封面导出的可观察行为：兼容性、构图范围、方向与原图保护。"""
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from PIL import Image

CROP = Path(__file__).with_name("crop-cover.py")


class CoverCropTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.src = self.root / "original.png"
        Image.new("RGB", (900, 1800), "green").save(self.src)

    def run_crop(self, *args, src=None, out=None):
        self.out = out or self.root / "out"
        return subprocess.run(
            [sys.executable, str(CROP), str(src or self.src), "--out-dir", str(self.out), *args],
            capture_output=True, text=True, timeout=30,
        )

    def test_all_presets_export_expected_names_and_sizes(self):
        expected = {
            "article": {"00-封面.png": (1500, 600), "00-封面-公众号.png": (900, 383)},
            "x-post": {"00-封面-X短文.png": (1200, 675)},
            "xiaohongshu": {"00-封面-小红书.png": (1080, 1440)},
            "douyin": {"00-封面-抖音图文.png": (1080, 1440)},
            "wechat": {"00-封面-公众号.png": (900, 383), "00-封面-公众号方图.png": (900, 900)},
        }
        for preset, targets in expected.items():
            with self.subTest(preset=preset):
                r = self.run_crop("--preset", preset, out=self.root / preset)
                self.assertEqual(r.returncode, 0, r.stderr)
                self.assertEqual({p.name for p in self.out.iterdir()}, set(targets))
                for name, size in targets.items():
                    with Image.open(self.out / name) as image:
                        self.assertEqual(image.size, size)
                        self.assertEqual(image.format, "PNG")

    def test_default_keeps_legacy_article_outputs(self):
        r = self.run_crop()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual({p.name for p in self.out.iterdir()}, {"00-封面.png", "00-封面-公众号.png"})

    def test_square_uses_original_not_a_wide_intermediate(self):
        image = Image.new("RGB", (900, 1800), "green")
        image.paste("red", (0, 0, 900, 600))
        image.paste("blue", (0, 1200, 900, 1800))
        image.save(self.src)
        r = self.run_crop("--preset", "wechat")
        self.assertEqual(r.returncode, 0, r.stderr)
        with Image.open(self.out / "00-封面-公众号方图.png") as square:
            self.assertEqual(square.getpixel((450, 10)), (255, 0, 0))
            self.assertEqual(square.getpixel((450, 890)), (0, 0, 255))

    def test_horizontal_anchors_retain_selected_subject(self):
        image = Image.new("RGB", (3000, 1500), "green")
        image.paste("red", (0, 0, 1000, 1500))
        image.paste("blue", (2000, 0, 3000, 1500))
        image.save(self.src)
        for anchor, color in [("left", (255, 0, 0)), ("center", (0, 128, 0)), ("right", (0, 0, 255))]:
            with self.subTest(anchor=anchor):
                r = self.run_crop("--preset", "xiaohongshu", "--anchor", anchor)
                self.assertEqual(r.returncode, 0, r.stderr)
                with Image.open(self.out / "00-封面-小红书.png") as result:
                    self.assertEqual(result.getpixel((540, 720)), color)

    def test_vertical_anchors_retain_selected_subject(self):
        image = Image.new("RGB", (600, 600), "green")
        image.paste("red", (0, 0, 600, 200))
        image.paste("blue", (0, 400, 600, 600))
        image.save(self.src)
        for anchor, color in [("top", (255, 0, 0)), ("bottom", (0, 0, 255))]:
            with self.subTest(anchor=anchor):
                r = self.run_crop("--preset", "x-post", "--anchor", anchor)
                self.assertEqual(r.returncode, 0, r.stderr)
                with Image.open(self.out / "00-封面-X短文.png") as result:
                    self.assertEqual(result.getpixel((600, 337)), color)

    def test_image_is_cropped_without_stretching(self):
        from PIL import ImageDraw
        image = Image.new("RGB", (600, 600), "white")
        ImageDraw.Draw(image).ellipse((200, 200, 400, 400), fill="black")
        image.save(self.src)
        r = self.run_crop("--preset", "x-post")
        self.assertEqual(r.returncode, 0, r.stderr)
        with Image.open(self.out / "00-封面-X短文.png") as result:
            bounds = result.convert("L").point(lambda p: 255 if p < 128 else 0).getbbox()
            self.assertIsNotNone(bounds)
            self.assertLessEqual(abs((bounds[2] - bounds[0]) - (bounds[3] - bounds[1])), 2)

    def test_exif_orientation_applied_before_crop(self):
        image = Image.new("RGB", (600, 800), "red")
        image.paste("blue", (300, 0, 600, 800))
        exif = image.getexif()
        exif[274] = 6  # 手机上竖向显示：顺时针旋转 90 度
        photo = self.root / "phone.jpg"
        image.save(photo, exif=exif)
        r = self.run_crop("--preset", "xiaohongshu", src=photo)
        self.assertEqual(r.returncode, 0, r.stderr)
        with Image.open(self.out / "00-封面-小红书.png") as result:
            top, bottom = result.getpixel((540, 100)), result.getpixel((540, 1340))
            self.assertGreater(top[0], 240)
            self.assertLess(top[2], 15)
            self.assertGreater(bottom[2], 240)
            self.assertLess(bottom[0], 15)

    def test_source_overwrite_rejected_without_changes(self):
        original = self.root / "00-封面.png"
        self.src.rename(original)
        before = hashlib.sha256(original.read_bytes()).digest()
        r = self.run_crop(src=original, out=self.root)
        self.assertNotEqual(r.returncode, 0)
        self.assertNotIn("Traceback", r.stderr)
        self.assertEqual(before, hashlib.sha256(original.read_bytes()).digest())
        self.assertFalse((self.root / "00-封面-公众号.png").exists())

    def test_invalid_input_does_not_create_output(self):
        for name in ["missing.png", "invalid.txt"]:
            with self.subTest(name=name):
                source = self.root / name
                if source.suffix == ".txt":
                    source.write_text("not an image")
                r = self.run_crop(src=source)
                self.assertNotEqual(r.returncode, 0)
                self.assertNotIn("Traceback", r.stderr)
                self.assertFalse(self.out.exists())

    def test_hardlink_to_source_is_not_overwritten(self):
        import os
        destination = self.root / "00-封面.png"
        os.link(self.src, destination)
        before = hashlib.sha256(self.src.read_bytes()).digest()
        r = self.run_crop(out=self.root)
        self.assertNotEqual(r.returncode, 0)
        self.assertNotIn("Traceback", r.stderr)
        self.assertEqual(before, hashlib.sha256(self.src.read_bytes()).digest())
        self.assertFalse((self.root / "00-封面-公众号.png").exists())

    def test_invalid_destination_or_options_fail_cleanly(self):
        blocked = self.root / "file"
        blocked.write_text("preserve me")
        r = self.run_crop(out=blocked)
        self.assertNotEqual(r.returncode, 0)
        self.assertNotIn("Traceback", r.stderr)
        self.assertEqual(blocked.read_text(), "preserve me")
        r = self.run_crop("--anchor", "unknown")
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse(self.out.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
