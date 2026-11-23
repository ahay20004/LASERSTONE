import unittest
from pathlib import Path
from local_unified_view import build, SOURCE

class UnifiedViewTests(unittest.TestCase):
    def test_original_ui_and_local_engine_evidence(self):
        original = (SOURCE / "index.html").read_text(encoding="utf-8")
        result = build().read_text(encoding="utf-8")
        self.assertIn('LASERSTONE | Scientific Research Platform', result)
        self.assertIn('local-scientific-evidence', result)
        self.assertIn('laserstone-welcome', result)
        self.assertIn('Dr. Abdelrahman A. Hagar', result)
        self.assertIn('Founder &amp; Scientific Director', result)
        self.assertIn('مرحبًا بكم', result)
        self.assertIn('SYNTHETIC DEMONSTRATION', result)
        self.assertIn('physics_consistency_engine', result)
        self.assertIn('connect-src \'none\'', result)
        self.assertEqual(original, (SOURCE / "index.html").read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
