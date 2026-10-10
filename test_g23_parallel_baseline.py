"""G23 parallel-track regression tests; no production modules are modified.

These tests verify the existing opt-in guards and expose a known legacy
consistency limitation without treating it as a passing scientific result.
"""
import unittest
from g23_scientific_input_gate import validate_scientific_inputs
from g23_simulation_exchange_contract import validate_simulation_envelope
from physics_consistency_engine import evaluate_physics_consistency

class G23ParallelBaselineTests(unittest.TestCase):
    def test_b_input_gate_does_not_mutate_source(self):
        plant = {"name": "Synthetic", "scientific_name": "Test species",
                 "origin": "Synthetic", "phi": 0.5, "tau": 2.0,
                 "sigma_a": 0.2, "eta": 0.7, "knr": 0.1,
                 "refractive_index": 1.3, "lambda_abs": 500.0,
                 "lambda_em": 600.0}
        before = plant.copy()
        self.assertTrue(validate_scientific_inputs(plant)["valid"])
        self.assertEqual(plant, before)

    def test_a_zero_index_is_not_accepted_by_legacy_cavity_guard(self):
        plant = {"name": "Synthetic", "scientific_name": "Test species",
                 "origin": "Synthetic", "phi": 0.5, "tau": 2.0,
                 "sigma_a": 0.2, "eta": 0.7, "knr": 0.1,
                 "refractive_index": 0.0, "lambda_abs": 500.0,
                 "lambda_em": 600.0}
        self.assertFalse(validate_scientific_inputs(plant)["valid"])
        # This is a model guard, not evidence that the material is impossible.

    @unittest.expectedFailure
    def test_c_legacy_consistency_requires_complete_scores(self):
        # Legacy implementation currently awards 100 to an empty mapping.
        self.assertNotEqual(evaluate_physics_consistency({}), 100)

    def test_d_exchange_contract_does_not_claim_simulation(self):
        envelope = {
            "simulator": "scaps-1d", "simulator_version": "unverified",
            "model_id": "synthetic-test", "run_id": "test-only",
            "inputs": {"thickness": {"value": 1.0, "unit": "um"}},
            "outputs": {"current": {"value": 0.0, "unit": "A"}},
            "conditions": {"kind": "synthetic"},
            "provenance": {"source": "unit-test"}
        }
        result = validate_simulation_envelope(envelope)
        self.assertTrue(result["valid"])
        self.assertEqual(result["status"], "CONTRACT_ONLY")

if __name__ == "__main__":
    unittest.main()
