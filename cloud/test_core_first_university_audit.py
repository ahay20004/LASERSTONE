"""Core-first university audit tests: no campus execution or mutation."""
import tempfile
import unittest
from pathlib import Path
from cloud.core_first_university_audit import assess_university_assets


class CoreFirstAuditTests(unittest.TestCase):
    def test_static_audit_does_not_import_or_execute(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            city = root / "city"
            city.mkdir()
            sample = city / "physics_wing.py"
            original = 'raise RuntimeError("must not run")\ndef laser_physics(): return 42\n'
            sample.write_text(original, encoding="utf-8")
            result = assess_university_assets(root)
            self.assertEqual(result["review_candidates"], 1)
            self.assertEqual(result["approved_transfers"], 0)
            self.assertEqual(result["university_changes"], 0)
            self.assertEqual(sample.read_text(encoding="utf-8"), original)
            self.assertFalse(result["assets"][0]["core_integration_verified"])

    def test_empty_and_broken_assets_do_not_gain_certification(self):
        with tempfile.TemporaryDirectory() as tmp:
            city = Path(tmp) / "city"
            city.mkdir()
            (city / "scientific_library.py").write_text("", encoding="utf-8")
            (city / "physics_wing.py").write_text("def bad(:", encoding="utf-8")
            result = assess_university_assets(tmp)
            self.assertEqual(result["review_candidates"], 0)
            self.assertTrue(all(not a["scientific_validation_verified"] for a in result["assets"]))
            self.assertTrue(any(a["syntax"].startswith("PARSE_ERROR") for a in result["assets"]))

    def test_current_repository_is_preserved(self):
        result = assess_university_assets()
        self.assertEqual(result["policy"], "CORE_FIRST_UNIVERSITY_PRESERVED")
        self.assertEqual(result["approved_transfers"], 0)
        self.assertTrue(all(not a["university_original_modified"] for a in result["assets"]))


if __name__ == "__main__":
    unittest.main()
