"""Test canonical spectral material adapter, regression and failure isolation."""
import unittest
from cloud.canonical_spectral_material_adapter import (
    SpectralMaterialRequest, evaluate_spectral_material,
)
from cloud.core_material_score_gate import ScoreInput
from cloud.spectral_material_contract_diagnostic import LABEL_CASES


def request(sample):
    scores = {"lsi": 6, "thermal_score": 80, "q_factor_score": 75,
              "beam_quality_score": 70, "laser_efficiency_score": 65}
    return SpectralMaterialRequest(
        dict(sample),
        {key: ScoreInput(value, "synthetic-only", "SIMULATED")
         for key, value in scores.items()},
    )


class CanonicalSpectralMaterialTests(unittest.TestCase):
    def test_all_three_labels_corrected_and_historical_impact(self):
        for label, sample in LABEL_CASES:
            with self.subTest(label=label):
                result = evaluate_spectral_material(request(sample))
                self.assertEqual(result["label"], label)
                self.assertEqual(
                    result["canonical_spectral_score"],
                    {"High": 100, "Medium": 60, "Low": 30}[label],
                )
                self.assertEqual(
                    result["material_score_delta"],
                    {"High": 6.0, "Medium": 2.0, "Low": -1.0}[label],
                )
                self.assertTrue(result["material_score_result"]["independent_formula_agreement"])
                self.assertEqual(
                    result["material_score_result"]["input_provenance"]["spectral_quality"]["evidence_state"],
                    "DERIVED",
                )
                self.assertFalse(result["main_pipeline_corrected"])
                self.assertFalse(result["experimental_validation"])

    def test_fail_closed_invalid_inputs(self):
        for key, value in (("knr", 0), ("phi", 1.1), ("sigma_a", -1),
                           ("tau", float("nan")), ("phi", True)):
            req = request(LABEL_CASES[0][1])
            req.spectral_inputs[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                evaluate_spectral_material(req)
        req = request(LABEL_CASES[0][1])
        del req.other_scores["lsi"]
        with self.assertRaises(ValueError):
            evaluate_spectral_material(req)


if __name__ == "__main__":
    unittest.main()
