"""Synthetic tests: Stage 3.5 numerical diagnostics."""
import importlib.util
from pathlib import Path
import unittest

p = Path(__file__).resolve().parents[1] / "numerical_audit.py"
spec = importlib.util.spec_from_file_location("numerical_audit", p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def convergence():
    return {"absolute_tolerance": 0.002, "relative_tolerance": 0,
            "samples": [{"resolution_scale": 0.1, "value": 1.1},
                        {"resolution_scale": 0.05, "value": 1.02},
                        {"resolution_scale": 0.025, "value": 1.001}]}

def sensitivity():
    return {"parameter": "alpha", "baseline_parameter": 2,
            "baseline_output": 4,
            "lower": {"parameter_value": 1.9, "output_value": 3.8},
            "upper": {"parameter_value": 2.1, "output_value": 4.2}}

class NumericalAuditTests(unittest.TestCase):
    def test_refinement_passes_with_declared_tolerance(self):
        d = convergence()
        d["absolute_tolerance"] = 0.02
        self.assertEqual(mod.convergence(d)["status"], "REFINEMENT_COMPATIBLE")

    def test_refinement_flags_large_last_change(self):
        self.assertEqual(mod.convergence(convergence())["status"], "REFINEMENT_REQUIRES_INVESTIGATION")

    def test_nonmonotone_resolution_rejected(self):
        d = convergence()
        d["samples"][1]["resolution_scale"] = 0.2
        with self.assertRaises(ValueError):
            mod.convergence(d)

    def test_nonfinite_values_rejected(self):
        d = convergence()
        d["samples"][1]["value"] = float("inf")
        with self.assertRaises(ValueError):
            mod.convergence(d)

    def test_normalized_sensitivity(self):
        r = mod.sensitivity(sensitivity())
        self.assertAlmostEqual(r["central_secant_slope"], 2)
        self.assertAlmostEqual(r["normalized_sensitivity"], 1)

    def test_zero_baseline_disables_normalization(self):
        d = sensitivity()
        d["baseline_output"] = 0
        self.assertIsNone(mod.sensitivity(d)["normalized_sensitivity"])

    def test_unbracketed_perturbation_rejected(self):
        d = sensitivity()
        d["lower"]["parameter_value"] = 2.2
        with self.assertRaises(ValueError):
            mod.sensitivity(d)

    def test_no_auto_endorsement(self):
        r = mod.audit(convergence(), sensitivity())
        self.assertEqual(r["endorsement"], "NONE")
        self.assertEqual(r["claims_authorized"], [])

    def test_missing_inputs_rejected(self):
        with self.assertRaises(ValueError):
            mod.audit()

if __name__ == "__main__":
    unittest.main()
