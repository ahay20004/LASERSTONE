"""Regression tests for opt-in G23 consistency assessment."""
import unittest
from g23_checked_physics_consistency import assess_physics_consistency
from physics_consistency_engine import evaluate_physics_consistency

class CheckedConsistencyTests(unittest.TestCase):
    def setUp(self):
        self.scores = {
            "gain_score": 65, "laser_efficiency_score": 60,
            "thermal_score": 72, "q_factor_score": 70,
            "material_score": 68, "lri_score": 64,
        }
    def test_empty_is_not_full_consistency(self):
        result = assess_physics_consistency({})
        self.assertIsNone(result["score"])
        self.assertEqual(result["status"], "INSUFFICIENT_OR_INVALID_SCORES")
    def test_missing_score_is_reported(self):
        scores = dict(self.scores)
        scores.pop("lri_score")
        result = assess_physics_consistency(scores)
        self.assertIn("lri_score", result["errors"])
    def test_nan_is_rejected(self):
        scores = dict(self.scores, thermal_score=float("nan"))
        self.assertIsNone(assess_physics_consistency(scores)["score"])
    def test_boolean_is_rejected(self):
        scores = dict(self.scores, gain_score=True)
        self.assertIsNone(assess_physics_consistency(scores)["score"])
    def test_out_of_range_is_rejected(self):
        scores = dict(self.scores, q_factor_score=120)
        self.assertIsNone(assess_physics_consistency(scores)["score"])
    def test_valid_scores_preserve_legacy_number(self):
        result = assess_physics_consistency(self.scores)
        self.assertEqual(result["status"], "HEURISTIC_SCORE_ONLY")
        self.assertEqual(result["score"], evaluate_physics_consistency(self.scores))
    def test_input_not_mutated(self):
        before = dict(self.scores)
        assess_physics_consistency(self.scores)
        self.assertEqual(self.scores, before)

if __name__ == "__main__":
    unittest.main()
