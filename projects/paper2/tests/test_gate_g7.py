"""G7 publication-readiness unit tests with synthetic dossiers."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("gate_g7", Path(__file__).resolve().parents[1] / "gate_g7.py")
g7 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g7)

def dossier():
    return {"gate_results": {k: "PASS" for k in g7.GATES},
            "editorial_checks": {k: True for k in g7.CHECKS},
            "manuscript_version": "v1", "evidence_register_version": "v1",
            "target_journal": "example journal"}

class ReadinessTests(unittest.TestCase):
    def test_complete_dossier_requires_human_review(self):
        self.assertEqual(g7.evaluate(dossier())["status"], "READY_FOR_HUMAN_REVIEW")
    def test_missing_gate_blocks(self):
        d = dossier()
        d["gate_results"]["G4"] = "NOT_RUN"
        self.assertEqual(g7.evaluate(d)["status"], "BLOCKED")
    def test_missing_authorship_blocks(self):
        d = dossier()
        d["editorial_checks"]["author_approval"] = False
        self.assertEqual(g7.evaluate(d)["status"], "BLOCKED")
    def test_missing_journal_blocks(self):
        d = dossier()
        d["target_journal"] = ""
        self.assertEqual(g7.evaluate(d)["status"], "BLOCKED")
    def test_empty_dossier_blocks(self):
        self.assertEqual(g7.evaluate({})["status"], "BLOCKED")

if __name__ == "__main__":
    unittest.main()
