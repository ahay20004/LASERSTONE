"""Synthetic regression checks for non-executing Core registry audit."""
import tempfile
import unittest
from pathlib import Path
from cloud.core_registry_dataflow_audit import audit_registry


class CoreRegistryDataflowTests(unittest.TestCase):
    def test_provider_graph_and_missing_inputs(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "project_registry.py").write_text(
                'PROJECT_REGISTRY = {'
                '"a": {"status":"ACTIVE","outputs":["signal"]},'
                '"b": {"inputs":["signal","external"],"outputs":["result"]},'
                '"c": {"outputs":["signal"]}}\n'
                'raise RuntimeError("must not execute")\n', encoding="utf-8")
            result = audit_registry(root)
            self.assertEqual(result["registered_entries"], 3)
            self.assertEqual(result["outputs_with_multiple_declared_providers"]["signal"], ["a", "c"])
            self.assertEqual(result["inputs_without_declared_provider"], ["external"])
            self.assertEqual(result["rows"][1]["internal_input_providers"]["signal"], ["a", "c"])
            self.assertTrue(all(not row["runtime_verified"] for row in result["rows"]))

    def test_no_university_or_scientific_execution(self):
        result = audit_registry()
        self.assertGreater(result["registered_entries"], 0)
        self.assertEqual(result["scope"], "DECLARED_DATAFLOW_ONLY")
        self.assertTrue(all(not row["physics_validated"] for row in result["rows"]))


if __name__ == "__main__":
    unittest.main()
