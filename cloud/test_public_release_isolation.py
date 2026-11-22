"""Regression checks for the isolated public release payload.

Run: python -m unittest -v cloud.test_public_release_isolation
This is a release-boundary check, not proof that a public Git repository is private.
"""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
STAGER = ROOT / "cloud" / "huggingface" / "prepare_space.py"
SOURCE = ROOT / "cloud" / "site"


class PublicReleaseIsolationTests(unittest.TestCase):
    def test_university_preserved_in_source_but_absent_from_release(self):
        original = (SOURCE / "index.html").read_text(encoding="utf-8")
        self.assertIn('id="university-campus"', original)
        self.assertEqual(original.split('id="university-campus"', 1)[1].split('id="agent-council"', 1)[0].count('class="campus-building"'), 7)

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "public"
            subprocess.run([sys.executable, str(STAGER), "--output", str(output)],
                           check=True, capture_output=True, text=True)
            self.assertEqual({p.name for p in output.iterdir()}, {
                "README.md", "index.html", "style.css", "i18n.js",
                "icon.svg", "manifest.webmanifest",
            })
            html = (output / "index.html").read_text(encoding="utf-8")
            js = (output / "i18n.js").read_text(encoding="utf-8")
            css = (output / "style.css").read_text(encoding="utf-8")
            for marker in ("university-campus", "navCampus", "missionCampus",
                           "campusB1", "campusD7", 'class="campus-building"'):
                self.assertNotIn(marker, html)
            for marker in ('"navCampus"', '"missionCampus"', '"campusB1"',
                           '"campusD7"', '"campusTitle"'):
                self.assertNotIn(marker, js)
            for marker in (".campus-section", ".campus-building", ".campus-sky"):
                self.assertNotIn(marker, css)
            for required in ('id="cockpit"', 'id="scientific-explorer"',
                             'id="research"', 'id="access"', 'id="agent-council"'):
                self.assertIn(required, html)
            self.assertIn('class="agent-role-card"', html)


if __name__ == "__main__":
    unittest.main()
