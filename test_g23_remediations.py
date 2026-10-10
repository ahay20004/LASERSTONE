"""G23 acceptance tests for four previously documented expected failures."""
import unittest
from g23_checked_laser_physics import calculate_checked_laser_physics
from g23_scientific_input_gate import validate_scientific_inputs
from g23_registry_contract_view import corrected_registry_view, CONSISTENCY_INPUTS
from project_registry import PROJECT_REGISTRY


class G23RemediationTests(unittest.TestCase):
    def setUp(self):
        self.plant = dict(name="Synthetic", scientific_name="Test species",
            origin="synthetic", phi=0.72, tau=4.1, sigma_a=1.05,
            eta=0.88, knr=0.34, refractive_index=1.33,
            lambda_abs=540.0, lambda_em=620.0)

    def test_zero_refractive_index_blocked_before_physics(self):
        with self.assertRaises(ValueError):
            calculate_checked_laser_physics(dict(self.plant, refractive_index=0))

    def test_negative_wavelength_rejected(self):
        self.assertFalse(validate_scientific_inputs(
            dict(self.plant, lambda_em=-620))["valid"])

    def test_phi_above_one_rejected(self):
        self.assertFalse(validate_scientific_inputs(
            dict(self.plant, phi=1.5))["valid"])

    def test_corrected_registry_contract(self):
        corrected = corrected_registry_view()
        self.assertEqual(
            set(corrected["physics_consistency_engine"]["inputs"]),
            set(CONSISTENCY_INPUTS))
        self.assertEqual(
            PROJECT_REGISTRY["physics_consistency_engine"]["inputs"],
            ["lambda_abs", "lambda_em"])

    def test_valid_checked_physics_preserves_legacy_numeric_output(self):
        from laser_physics_engine import calculate_laser_physics
        checked = calculate_checked_laser_physics(self.plant)
        self.assertEqual(checked, calculate_laser_physics(self.plant))


if __name__ == "__main__":
    unittest.main()
