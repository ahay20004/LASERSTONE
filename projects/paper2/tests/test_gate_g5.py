"""Synthetic G5 report-comparison tests."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("gate_g5", Path(__file__).resolve().parents[1] / "gate_g5.py")
g5 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g5)

def report():
    return {"sha256_a": "a"*64, "sha256_b": "b"*64,
            "grid_step_nm": 1.0, "overlap_nm": [350.0, 700.0],
            "normalized_rmse": 0.02, "normalized_pearson_r": 0.99,
            "peak_a_overlap_nm": 430.0, "peak_b_overlap_nm": 431.0,
            "delta_peak_overlap_nm": -1.0}

class ReproducibilityTests(unittest.TestCase):
    def test_identical_reports_pass(self):
        self.assertEqual(g5.evaluate(report(), report())["status"], "PASS")
    def test_legacy_agreement_does_not_establish_run_separation(self):
        result = g5.evaluate(report(), report())
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["run_separation"], "NOT_ESTABLISHED")
    def test_strict_rejects_missing_execution_ids(self):
        self.assertEqual(g5.evaluate(report(), report(), require_distinct_runs=True)["status"], "FAIL")
    def test_strict_accepts_distinct_declared_execution_ids(self):
        a, b = report(), report()
        a["execution_id"], b["execution_id"] = "synthetic-run-1", "synthetic-run-2"
        result = g5.evaluate(a, b, require_distinct_runs=True)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["run_separation"], "DISTINCT_DECLARED")
    def test_strict_rejects_same_declared_execution_id(self):
        a, b = report(), report()
        a["execution_id"] = b["execution_id"] = "same"
        self.assertEqual(g5.evaluate(a, b, require_distinct_runs=True)["status"], "FAIL")
    def test_changed_input_hash_fails(self):
        altered = report()
        altered["sha256_a"] = "c"*64
        self.assertEqual(g5.evaluate(report(), altered)["status"], "FAIL")
    def test_changed_metric_fails(self):
        altered = report()
        altered["normalized_rmse"] += 0.01
        self.assertEqual(g5.evaluate(report(), altered)["status"], "FAIL")
    def test_missing_metric_fails(self):
        altered = report()
        del altered["normalized_pearson_r"]
        self.assertEqual(g5.evaluate(report(), altered)["status"], "FAIL")
    def test_nonfinite_tolerance_rejected(self):
        with self.assertRaises(ValueError):
            g5.evaluate(report(), report(), float("nan"))

if __name__ == "__main__":
    unittest.main()
