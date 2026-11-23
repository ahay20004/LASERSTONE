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
        self.assertIn('data-welcome-lang="ar"', result)
        self.assertIn('data-welcome-lang="en"', result)
        self.assertIn('class="topbar"', result)
        self.assertIn('class="mission-sidebar"', result)
        self.assertIn('welcome-language.js', result)
        self.assertIn('selector.addEventListener(\'change\', updateWelcome)', (build().parent / 'welcome-language.js').read_text(encoding='utf-8'))
        self.assertIn('id="laserstone-role-ar"', result)
        self.assertIn('id="laserstone-role-en"', result)
        self.assertIn('GAIN MEDIUM', result)
        self.assertIn('د. عبدالرحمن أ. حجر', result)
        self.assertNotIn('د. عبدالرحمن أ. هجر', result)
        self.assertIn('ls-hr-mirror', result)
        self.assertIn('ls-oc-mirror', result)
        self.assertIn('ls-output-arrow', result)
        script = (build().parent / 'welcome-language.js').read_text(encoding='utf-8')
        self.assertIn('Concave–concave resonator', script)
        self.assertIn('Plane–plane resonator', script)
        self.assertIn('Concave–plane resonator', script)
        self.assertIn('prefers-reduced-motion: reduce', script)
        self.assertIn('Violet', script)
        self.assertIn('prefers-reduced-motion', result)
        self.assertIn('class="topbar"', result)
        self.assertIn('SYNTHETIC DEMONSTRATION', result)
        self.assertIn('physics_consistency_engine', result)
        self.assertIn('connect-src \'none\'', result)
        self.assertEqual(original, (SOURCE / "index.html").read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
