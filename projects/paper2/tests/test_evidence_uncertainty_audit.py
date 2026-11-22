"""Synthetic checks for Stage 3.7 evidence uncertainty comparison."""
import importlib.util
import math
from pathlib import Path
import unittest

p = Path(__file__).resolve().parents[1] / "evidence_uncertainty_audit.py"
spec = importlib.util.spec_from_file_location("evidence_uncertainty_audit", p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def record():
    return {"observable": "synthetic power", "unit": "W",
            "prediction": 10.0, "prediction_standard_uncertainty": 0.3,
            "measurement": 9.5, "measurement_standard_uncertainty": 0.4,
            "source_id": "synthetic", "instrument_id": "synthetic-meter",
            "calibration_id": "synthetic-cal", "conditions_id": "synthetic-condition"}

def report():
    return {"theory_id": "synthetic-theory", "version": "0.1",
            "proposal_sha256": "synthetic-proposal-hash",
            "audit_sha256": "synthetic-audit-hash"}

class EvidenceTests(unittest.TestCase):
    def test_combined_uncertainty_and_residual(self):
        r = mod.compare(record())
        self.assertAlmostEqual(r["combined_standard_uncertainty"], 0.5)
        self.assertAlmostEqual(r["absolute_normalized_residual"], 1)
        self.assertEqual(r["evidence_authentication"], "NOT_VERIFIED")

    def test_negative_uncertainty_rejected(self):
        d = record()
        d["measurement_standard_uncertainty"] = -0.1
        with self.assertRaises(ValueError):
            mod.compare(d)

    def test_nonfinite_rejected(self):
        d = record()
        d["prediction"] = float("nan")
        with self.assertRaises(ValueError):
            mod.compare(d)

    def test_zero_uncertainty_not_accepted(self):
        d = record()
        d["prediction_standard_uncertainty"] = 0
        d["measurement_standard_uncertainty"] = 0
        r = mod.compare(d)
        self.assertEqual(r["status"], "UNCERTAINTY_NOT_RESOLVED")
        self.assertIsNone(r["absolute_normalized_residual"])

    def test_missing_provenance_rejected(self):
        d = record()
        d["source_id"] = ""
        with self.assertRaises(ValueError):
            mod.compare(d)

    def test_version_binding_and_nonendorsement(self):
        r = mod.bind_report(report(), [record()])
        self.assertEqual(r["version"], "0.1")
        self.assertEqual(r["endorsement"], "NONE")
        self.assertEqual(r["claims_authorized"], [])

    def test_deterministic_evidence_hash(self):
        a = mod.bind_report(report(), [record()])
        b = mod.bind_report(report(), [record()])
        self.assertEqual(a["evidence_input_sha256"], b["evidence_input_sha256"])

    def test_empty_evidence_rejected(self):
        with self.assertRaises(ValueError):
            mod.bind_report(report(), [])

if __name__ == "__main__":
    unittest.main()
