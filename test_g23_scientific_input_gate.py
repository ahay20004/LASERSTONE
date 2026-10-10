"""Tests for opt-in G23 scientific input domain gate."""
import unittest
from g23_scientific_input_gate import validate_scientific_inputs


class ScientificInputGateTests(unittest.TestCase):
    def setUp(self):
        self.plant = dict(name="Synthetic test", scientific_name="Test species",
            origin="synthetic", phi=0.72, tau=4.1, sigma_a=1.05,
            eta=0.88, knr=0.34, refractive_index=1.33,
            lambda_abs=540.0, lambda_em=620.0)

    def test_valid_synthetic_case(self):
        self.assertTrue(validate_scientific_inputs(self.plant)["valid"])

    def test_reject_nonphysical_quantum_yield(self):
        self.assertFalse(validate_scientific_inputs(dict(self.plant, phi=1.5))["valid"])

    def test_reject_negative_wavelength(self):
        self.assertFalse(validate_scientific_inputs(dict(self.plant, lambda_em=-1))["valid"])

    def test_reject_zero_index(self):
        self.assertFalse(validate_scientific_inputs(dict(self.plant, refractive_index=0))["valid"])

    def test_reject_nan(self):
        self.assertFalse(validate_scientific_inputs(dict(self.plant, phi=float("nan")))["valid"])

    def test_reject_missing_field(self):
        plant = dict(self.plant)
        del plant["lambda_abs"]
        self.assertFalse(validate_scientific_inputs(plant)["valid"])

    def test_reject_boolean_as_numeric(self):
        self.assertFalse(validate_scientific_inputs(dict(self.plant, phi=True))["valid"])

    def test_reject_non_mapping(self):
        self.assertFalse(validate_scientific_inputs(None)["valid"])


if __name__ == "__main__":
    unittest.main()
