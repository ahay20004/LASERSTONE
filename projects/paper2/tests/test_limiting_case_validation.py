"""Synthetic limiting-case checks, no physical model verification."""
import importlib.util
from pathlib import Path
import unittest

p = Path(__file__).resolve().parents[1] / "limiting_case_validation.py"
spec = importlib.util.spec_from_file_location("limiting_case_validation", p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def case():
    return {
        "parameter": "epsilon", "limit_value": 0,
        "absolute_tolerance": 1e-3, "relative_tolerance": 0,
        "samples": [
            {"parameter_value": 0.1, "reference_value": 1, "modified_value": 1.1},
            {"parameter_value": 0.01, "reference_value": 1, "modified_value": 1.01},
            {"parameter_value": 0.0001, "reference_value": 1, "modified_value": 1.0001},
        ],
    }

class LimitTests(unittest.TestCase):
    def test_approaching_reference(self):
        r = mod.evaluate(case())
        self.assertEqual(r["status"], "NUMERICAL_LIMIT_COMPATIBLE")
        self.assertFalse(r["theory_endorsed"])
        self.assertEqual(r["claims_authorized"], [])

    def test_persistent_difference_requires_investigation(self):
        d = case()
        for row in d["samples"]:
            row["modified_value"] = 1.5
        self.assertEqual(mod.evaluate(d)["status"], "LIMIT_REQUIRES_INVESTIGATION")

    def test_nonmonotone_approach_rejected(self):
        d = case()
        d["samples"][1]["parameter_value"] = 0.2
        with self.assertRaises(ValueError):
            mod.evaluate(d)

    def test_nan_rejected(self):
        d = case()
        d["samples"][0]["reference_value"] = float("nan")
        with self.assertRaises(ValueError):
            mod.evaluate(d)

    def test_invalid_tolerance_rejected(self):
        d = case()
        d["absolute_tolerance"] = -1
        with self.assertRaises(ValueError):
            mod.evaluate(d)

    def test_exact_limit_sample_not_convergence(self):
        d = case()
        d["samples"][-1]["parameter_value"] = 0
        with self.assertRaises(ValueError):
            mod.evaluate(d)

    def test_increasing_residual_not_compatible(self):
        d = case()
        d["samples"][0]["modified_value"] = 1.00001
        self.assertEqual(mod.evaluate(d)["status"], "LIMIT_REQUIRES_INVESTIGATION")

if __name__ == "__main__":
    unittest.main()
