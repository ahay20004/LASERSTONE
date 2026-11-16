"""Fail-closed and independent-formula regression of material score adapter."""
import unittest
from cloud.core_material_score_gate import ScoreInput, FIELDS, evaluate_material_score


def sample():
    values = (6, 70, 80, 65, 75, 85)
    return {name: ScoreInput(value, "synthetic-test-only", "SIMULATED")
            for name, value in zip(FIELDS, values)}


class MaterialScoreGateTests(unittest.TestCase):
    def test_bounded_existing_engine_execution(self):
        result = evaluate_material_score(sample())
        self.assertTrue(result["independent_formula_agreement"])
        self.assertGreaterEqual(result["score"], 0)
        self.assertLessEqual(result["score"], 100)
        self.assertFalse(result["scientific_validation"])
        self.assertFalse(result["experimental_validation"])
        self.assertFalse(result["patentability_assessment"])
        self.assertEqual(set(result["input_provenance"]), set(FIELDS))

    def test_missing_inputs_do_not_silently_become_zero(self):
        data = sample()
        del data["thermal_score"]
        with self.assertRaises(ValueError):
            evaluate_material_score(data)

    def test_invalid_provenance_and_values_rejected(self):
        for field in FIELDS:
            for replacement in (ScoreInput(float("nan"), "source", "MEASURED"),
                                ScoreInput(True, "source", "MEASURED"),
                                ScoreInput(50, "", "MEASURED"),
                                ScoreInput(50, "source", "UNVERIFIED"),
                                ScoreInput(-1, "source", "MEASURED"),
                                ScoreInput(101, "source", "MEASURED")):
                with self.subTest(field=field, replacement=replacement):
                    data = sample()
                    data[field] = replacement
                    with self.assertRaises(ValueError):
                        evaluate_material_score(data)

    def test_zero_scores_are_explicit_not_missing(self):
        result = evaluate_material_score({
            name: ScoreInput(0, "synthetic-zero", "SIMULATED") for name in FIELDS
        })
        self.assertEqual(result["score"], 0)


if __name__ == "__main__":
    unittest.main()
