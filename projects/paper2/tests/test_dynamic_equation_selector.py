"""Synthetic applicability tests for the optical model selector."""
import importlib.util
from pathlib import Path
import unittest

root = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("dynamic_equation_selector", root / "dynamic_equation_selector.py")
selector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(selector)

def regime(d=1e-3):
    return {"thickness_m": d, "wavelength_m": 632.8e-9,
            "homogeneous": True, "scattering_negligible": True,
            "interface_reflections_accounted": True,
            "coherent_interference_negligible": True,
            "bulk_optical_constants_valid": True,
            "layer_stack_characterized": None, "complex_indices_available": None}

class EquationSelectorTests(unittest.TestCase):
    def test_bulk_regime_declared_applicable(self):
        result = selector.select_optical_model(regime())
        self.assertEqual(result["models"]["beer_lambert"]["status"], "APPLICABLE")
        self.assertEqual(result["claims_authorized"], [])

    def test_nanometric_thickness_not_automatic_switch(self):
        result = selector.select_optical_model(regime(0.5e-9))
        self.assertEqual(result["models"]["beer_lambert"]["status"], "APPLICABLE")
        self.assertEqual(result["selected_for_computation"], ["beer_lambert"])

    def test_interference_blocks_single_pass(self):
        data = regime(20e-9)
        data["coherent_interference_negligible"] = False
        result = selector.select_optical_model(data)
        self.assertEqual(result["models"]["beer_lambert"]["status"], "NOT_APPLICABLE")
        self.assertEqual(result["selected_for_computation"], [])

    def test_unknown_condition_requires_review(self):
        data = regime()
        data["homogeneous"] = None
        self.assertEqual(selector.select_optical_model(data)["models"]["beer_lambert"]["status"], "CONDITIONAL")

    def test_thin_film_candidate_not_solver_approval(self):
        data = regime(5e-9)
        data["coherent_interference_negligible"] = False
        data["layer_stack_characterized"] = True
        data["complex_indices_available"] = True
        result = selector.select_optical_model(data)
        self.assertEqual(result["models"]["thin_film_transfer_matrix"]["status"], "CONDITIONAL")
        self.assertEqual(result["selected_for_computation"], [])

    def test_invalid_thickness_rejected(self):
        with self.assertRaises(ValueError):
            selector.select_optical_model(regime(0))

    def test_nonfinite_wavelength_rejected(self):
        data = regime()
        data["wavelength_m"] = float("nan")
        with self.assertRaises(ValueError):
            selector.select_optical_model(data)

if __name__ == "__main__":
    unittest.main()
