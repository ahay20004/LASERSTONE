"""Read-only synthetic and real-tree regression tests for whole-engine AST audit."""
import tempfile
import unittest
from pathlib import Path
from cloud.full_engine_audit import audit, markdown_report


class FullEngineAuditTests(unittest.TestCase):
    def test_synthetic_registry_main_signatures_and_graph(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "project_registry.py").write_text(
                'PROJECT_REGISTRY = {"a": {"status":"ACTIVE","inputs":["external"],'
                '"outputs":["score"]}, "b": {"status":"ACTIVE","inputs":["score"],'
                '"outputs":["result"]}}', encoding="utf-8")
            (root / "a.py").write_text(
                "def calculate(x, y=1):\n    return x+y\n", encoding="utf-8")
            (root / "b.py").write_text(
                "class B:\n    def method(self, z):\n        return z\n", encoding="utf-8")
            (root / "main.py").write_text(
                "from a import calculate\n\ndef run():\n    return calculate(1)\n",
                encoding="utf-8")
            before = {p.name: p.read_bytes() for p in root.iterdir()}
            result = audit(root)
            self.assertEqual(result["summary"]["registry_entries"], 2)
            self.assertEqual(result["summary"]["declared_edges"], 1)
            self.assertEqual(result["summary"]["declared_connected_entries"], 2)
            self.assertEqual(result["summary"]["registry_entries_with_main_static_calls"], 1)
            self.assertEqual(result["summary"]["callable_definitions_including_methods"], 3)
            self.assertEqual(before, {p.name: p.read_bytes() for p in root.iterdir()})
            self.assertIn("a", markdown_report(result))
            self.assertFalse(any(row["runtime_verified_by_this_audit"]
                                 for row in result["registry_rows"]))

    def test_repository_is_read_only_and_reports_all_registry_entries(self):
        result = audit()
        self.assertEqual(result["summary"]["registry_entries"], 32)
        self.assertGreaterEqual(result["summary"]["python_files_parsed"], 100)
        self.assertEqual(result["summary"]["declared_edges"], 31)
        self.assertEqual(result["summary"]["declared_connected_entries"], 24)
        self.assertEqual(result["summary"]["declared_isolated_entries"], 8)
        self.assertTrue(all(not row["physics_validated_by_this_audit"]
                            for row in result["registry_rows"]))


if __name__ == "__main__":
    unittest.main()
