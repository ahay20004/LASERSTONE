"""Integration tests for thermal-to-material data handoff."""
import unittest
from cloud.core_thermal_screen_gate import ThermalInput
from cloud.core_material_score_gate import ScoreInput
from cloud.core_thermal_material_handoff import (
    MaterialThermalRequest, evaluate_material_with_thermal,
)


def fixture():
    thermal = {
        "phi": ThermalInput(.8, "1", "synthetic", "SIMULATED"),
        "tau": ThermalInput(4.5, "ns", "synthetic", "SIMULATED"),
        "knr": ThermalInput(.3, "ns^-1", "synthetic", "SIMULATED"),
        "refractive_index": ThermalInput(1.35, "1", "synthetic", "SIMULATED"),
    }
    material = {
        name: ScoreInput(value, "synthetic", "SIMULATED")
        for name, value in (
            ("lsi", 6), ("q_factor_score", 80), ("beam_quality_score", 65),
            ("laser_efficiency_score", 75), ("spectral_quality", 85)
        )
    }
    return MaterialThermalRequest(thermal, material)


class ThermalMaterialHandoffTests(unittest.TestCase):
    def test_real_two_engine_execution_and_derived_provenance(self):
        result = evaluate_material_with_thermal(fixture())
        self.assertEqual(result["handoff_value"], 100)
        self.assertEqual(result["material_ranking"]["score"], 75.25)
        self.assertTrue(result["integration_passed"])
        self.assertEqual(result["handoff_evidence_state"], "DERIVED")
        self.assertEqual(
            result["material_ranking"]["input_provenance"]["thermal_score"]["evidence_state"],
            "DERIVED",
        )
        self.assertFalse(result["experimental_validation"])
        self.assertFalse(result["predictive_calibration"])

    def test_reject_untrusted_supplied_thermal_score(self):
        req = fixture()
        req.material_inputs["thermal_score"] = ScoreInput(0, "fake", "MEASURED")
        with self.assertRaises(ValueError):
            evaluate_material_with_thermal(req)

    def test_thermal_input_error_propagates(self):
        req = fixture()
        req.thermal_inputs["tau"] = ThermalInput(-1, "ns", "synthetic", "SIMULATED")
        with self.assertRaises(ValueError):
            evaluate_material_with_thermal(req)

    def test_no_silent_default_on_missing_material_field(self):
        req = fixture()
        del req.material_inputs["q_factor_score"]
        with self.assertRaises(ValueError):
            evaluate_material_with_thermal(req)


if __name__ == "__main__":
    unittest.main()
