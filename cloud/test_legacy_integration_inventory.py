"""Regression checks for the read-only legacy inventory; synthetic fixtures only."""
import tempfile
import unittest
from pathlib import Path

from cloud.legacy_integration_inventory import build_inventory


class LegacyInventoryTests(unittest.TestCase):
    def test_inventory_does_not_execute_modules(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "laser_physics_engine.py").write_text(
                'raise RuntimeError("must not import")\ndef calculate(x): return x\n',
                encoding="utf-8")
            (root / "project_registry.py").write_text(
                'PROJECT_REGISTRY = {"laser_physics_engine": {"status": "ACTIVE"}, '
                '"missing_engine": {"status": "ACTIVE"}}\n', encoding="utf-8")
            result = build_inventory(root)
            self.assertEqual(result["root_engine_like_files"], 1)
            self.assertEqual(result["registry_entries"], 2)
            self.assertEqual(result["registry_missing_corresponding_root_py"], ["missing_engine"])
            self.assertEqual(result["inventory"][0]["runtime_tested"], "NOT_ESTABLISHED_BY_INVENTORY")
            self.assertFalse(result["inventory"][0]["cloud_connected"])

    def test_invalid_source_is_reported_without_running(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "broken_engine.py").write_text("def broken(:\n", encoding="utf-8")
            result = build_inventory(root)
            self.assertEqual(result["inventory"][0]["syntax"], "PARSE_ERROR")
            self.assertFalse(result["simulator_execution_verified"])

    def test_no_claim_of_experimental_validation(self):
        result = build_inventory()
        self.assertFalse(result["public_preview_live_engines"])
        self.assertFalse(result["simulator_execution_verified"])
        self.assertTrue(all(not row["experimentally_validated"] is True
                            for row in result["inventory"]))


if __name__ == "__main__":
    unittest.main()
