"""Synthetic regression checks for the gated optical solver."""
import importlib.util
from pathlib import Path
import math
import unittest

root = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("optical_solver_uncertainty", root / "optical_solver_uncertainty.py")
solver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(solver)

def regime():
    return {"thickness_m": 1e-3, "wavelength_m": 632.8e-9,
            "homogeneous": True, "scattering_negligible": True,
            "interface_reflections_accounted": True,
            "coherent_interference_negligible": True,
            "bulk_optical_constants_valid": True,
            "layer_stack_characterized": None, "complex_indices_available": None}

def inputs():
    return {"incident_power_W": 1.0, "incident_power_std_W": 0.01,
            "alpha_per_m": 100.0, "alpha_std_per_m": 2.0,
            "thickness_m": 1e-3, "thickness_std_m": 1e-5}

class OpticalSolverTests(unittest.TestCase):
    def test_expected_transmission_and_uncertainty(self):
        result = solver.solve(inputs(), regime())
        self.assertEqual(result["status"], "COMPUTED_MODEL_CONDITIONAL")
        self.assertAlmostEqual(result["result"]["transmittance"], math.exp(-0.1))
        expected = math.exp(-0.1) * math.sqrt(0.01**2 + (1e-3 * 2)**2 + (100 * 1e-5)**2)
        self.assertAlmostEqual(result["result"]["transmitted_power_standard_uncertainty_W"], expected)
        self.assertEqual(result["claims_authorized"], [])

    def test_interference_blocks_computation(self):
        r = regime()
        r["coherent_interference_negligible"] = False
        self.assertEqual(solver.solve(inputs(), r)["status"], "BLOCKED_MODEL_NOT_APPLICABLE")

    def test_missing_assumption_blocks_computation(self):
        r = regime()
        r["homogeneous"] = None
        self.assertEqual(solver.solve(inputs(), r)["status"], "BLOCKED_MODEL_NOT_APPLICABLE")

    def test_negative_alpha_rejected(self):
        data = inputs()
        data["alpha_per_m"] = -1
        with self.assertRaises(ValueError):
            solver.solve(data, regime())

    def test_thickness_mismatch_rejected(self):
        data = inputs()
        data["thickness_m"] = 2e-3
        with self.assertRaises(ValueError):
            solver.solve(data, regime())

    def test_nonfinite_uncertainty_rejected(self):
        data = inputs()
        data["alpha_std_per_m"] = float("nan")
        with self.assertRaises(ValueError):
            solver.solve(data, regime())

    def test_optical_depth_overflow_guard(self):
        data = inputs()
        data["alpha_per_m"] = 1e8
        with self.assertRaises(ValueError):
            solver.solve(data, regime())

if __name__ == "__main__":
    unittest.main()
