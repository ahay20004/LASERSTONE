"""G23 read-only characterization tests: data integrity and registry contracts.

Run: python -m unittest -v test_g23_data_registry.py
Expected failures are known scientific-readiness gaps, not passed gates.
"""
import unittest

from data_validator import validate_plant_data
from project_registry import PROJECT_REGISTRY
from physics_consistency_engine import evaluate_physics_consistency


class G23DataRegistryTests(unittest.TestCase):
    def setUp(self):
        self.plant = dict(name="Test", scientific_name="Test species",
            origin="synthetic", phi=0.72, tau=4.1, sigma_a=1.05,
            eta=0.88, knr=0.34, refractive_index=1.33,
            lambda_abs=540.0, lambda_em=620.0)

    def test_missing_required_field_rejected(self):
        plant = dict(self.plant)
        del plant["lambda_em"]
        result = validate_plant_data(plant)
        self.assertFalse(result["valid"])
        self.assertIn("lambda_em", result["missing"])

    @unittest.expectedFailure
    def test_nonphysical_wavelength_rejected(self):
        plant = dict(self.plant, lambda_em=-620.0)
        self.assertFalse(validate_plant_data(plant)["valid"])

    @unittest.expectedFailure
    def test_nonphysical_quantum_yield_rejected(self):
        plant = dict(self.plant, phi=1.5)
        self.assertFalse(validate_plant_data(plant)["valid"])

    @unittest.expectedFailure
    def test_registry_contract_matches_consistency_engine_inputs(self):
        declared = set(PROJECT_REGISTRY["physics_consistency_engine"]["inputs"])
        consumed = {"gain_score", "laser_efficiency_score", "thermal_score",
                    "q_factor_score", "material_score", "lri_score"}
        self.assertEqual(declared, consumed)

    def test_consistency_score_is_heuristic_not_physics_proof(self):
        # Characterization: all missing scores default to zero and score 100.
        # A perfect score here must NOT be interpreted as physical validation.
        self.assertEqual(evaluate_physics_consistency({}), 100.0)


if __name__ == "__main__":
    unittest.main()
