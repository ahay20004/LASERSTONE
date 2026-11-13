"""Synthetic G6 metadata tests; no real manuscript evidence is asserted."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("gate_g6", Path(__file__).resolve().parents[1] / "gate_g6.py")
g6 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g6)

def record(**changes):
    r = {
        "claim_id": "C1", "claim_text": "Two normalized spectra were compared",
        "evidence_type": "derived", "source_id": "S1",
        "source_sha256": "a" * 64, "method": "min-max",
        "parameters": {"step_nm": 1.0}, "conditions": {"solvent": "specified"},
        "result": {"nrmse": 0.02}, "limitations": "Shape only",
        "manuscript_location": "Results"
    }
    r.update(changes)
    return r

class TraceabilityTests(unittest.TestCase):
    def test_valid_metadata(self):
        self.assertEqual(g6.validate([record()])["status"], "PASS")
    def test_missing_source_rejected(self):
        self.assertEqual(g6.validate([record(source_id="")])["status"], "FAIL")
    def test_duplicate_claim_rejected(self):
        self.assertEqual(g6.validate([record(), record()])["status"], "FAIL")
    def test_prediction_requires_model_version(self):
        self.assertEqual(g6.validate([record(evidence_type="predicted")])["status"], "FAIL")
    def test_hypothesis_not_experiment(self):
        self.assertEqual(g6.validate([record(evidence_type="hypothesis", result="experimentally_verified")])["status"], "FAIL")

if __name__ == "__main__":
    unittest.main()
