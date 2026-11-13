"""Synthetic tests for the Research Hub lifecycle registry."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("registry", Path(__file__).resolve().parents[1] / "research_project_registry.py")
registry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(registry)

def item(project_id="paper2"):
    return {"project_id": project_id, "working_title": "Synthetic test project",
            "stage": "VALIDATION", "master_reference": "private-master",
            "owner_approval": True, "evidence_register_reference": "private-register",
            "gate_reports": {}}

class RegistryTests(unittest.TestCase):
    def test_valid_registry(self):
        self.assertEqual(registry.validate_registry({"projects": [item()]})["status"], "PASS")
    def test_duplicate_project_blocked(self):
        self.assertEqual(registry.validate_registry({"projects": [item(), item()]})["status"], "FAIL")
    def test_owner_approval_required(self):
        x = item()
        x["owner_approval"] = False
        self.assertEqual(registry.validate_registry({"projects": [x]})["status"], "FAIL")
    def test_unknown_stage_rejected(self):
        x = item()
        x["stage"] = "AUTOMATIC_PUBLICATION"
        self.assertEqual(registry.validate_registry({"projects": [x]})["status"], "FAIL")
    def test_empty_registry_rejected(self):
        self.assertEqual(registry.validate_registry({"projects": []})["status"], "FAIL")

if __name__ == "__main__":
    unittest.main()
