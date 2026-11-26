import unittest
from physics_consistency_engine import evaluate_physics_consistency, classify_consistency, REQUIRED_SCORES
from local_scientific_bridge import evaluate_synthetic_case

class LocalScientificBridgeTests(unittest.TestCase):
    def test_real_engine_called_with_synthetic_inputs(self):
        report = evaluate_synthetic_case()
        self.assertEqual(report["output"]["consistency_score"], 100)
        self.assertEqual(report["output"]["classification"], "Highly Consistent")
        self.assertEqual(report["input_kind"], "SYNTHETIC_DEMONSTRATION")
        self.assertFalse(report["independent_scientific_validation"])
        self.assertFalse(report["public_deployment_authorized"])

class ConsistencyInputTests(unittest.TestCase):
    def test_missing_scores(self):
        for key in REQUIRED_SCORES:
            values = dict.fromkeys(REQUIRED_SCORES, 70)
            del values[key]
            with self.assertRaises(ValueError):
                evaluate_physics_consistency(values)
        with self.assertRaises(ValueError):
            evaluate_physics_consistency({})

    def test_invalid_scores(self):
        for key in REQUIRED_SCORES:
            for invalid in (None, True, "70", -1, 101, float("nan"), float("inf"), -float("inf")):
                values = dict.fromkeys(REQUIRED_SCORES, 70)
                values[key] = invalid
                with self.subTest(key=key, invalid=invalid):
                    with self.assertRaises(ValueError):
                        evaluate_physics_consistency(values)

    def test_valid_boundaries_and_legacy_penalties(self):
        for value in (0, 100):
            self.assertEqual(evaluate_physics_consistency(dict.fromkeys(REQUIRED_SCORES, value)), 100)
        values = dict.fromkeys(REQUIRED_SCORES, 70)
        values.update(gain_score=10, laser_efficiency_score=90)
        self.assertEqual(evaluate_physics_consistency(values), 60)

    def test_invalid_classification(self):
        for value in (True, None, -1, 101, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                classify_consistency(value)

if __name__ == "__main__":
    unittest.main()
