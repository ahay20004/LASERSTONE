"""Acceptance tests for G23 strict decision wrappers and component registry."""

import unittest

from g23_intelligence_hub import (
    analyze_declared_registry_connectivity,
    generate_intelligence_summary_strict,
)
from g23_component_registry import (
    G23_COMPONENT_REGISTRY,
    component_registry_snapshot,
    promotion_candidates,
)
from g23_scientific_missing_policy import MissingScientificDataError
from g23_strict_decision_path import (
    calculate_lri_strict,
    calculate_material_score_strict,
    calculate_scientific_confidence_strict,
    evaluate_physics_consistency_strict,
    generate_final_decision_strict,
)


VALID = {
    "thermal_score": 70.0,
    "q_factor_score": 72.0,
    "laser_efficiency_score": 68.0,
    "beam_quality_score": 66.0,
    "feasibility_score": 64.0,
    "gain_score": 65.0,
    "material_score": 67.0,
    "lri_score": 68.0,
    "physics_consistency_score": 80.0,
    "experimental_success_score": 60.0,
    "research_novelty_score": 55.0,
    "patent_potential_score": 50.0,
    "scientific_confidence_score": 75.0,
    "system_integrity_score": 80.0,
}


class StrictDecisionPathTests(unittest.TestCase):
    def test_lri_strict_refuses_missing_score(self):
        record = dict(VALID)
        del record["thermal_score"]
        with self.assertRaises(MissingScientificDataError):
            calculate_lri_strict(record)

    def test_lri_strict_returns_heuristic_status(self):
        result = calculate_lri_strict(VALID)
        self.assertEqual(result["status"], "HEURISTIC_SCORE_STRICT_INPUTS")
        self.assertEqual(result["physical_validation"], "NOT_ESTABLISHED")
        self.assertTrue(0 <= result["score"] <= 100)

    def test_consistency_strict_refuses_partial_record(self):
        record = dict(VALID)
        del record["gain_score"]
        with self.assertRaises(MissingScientificDataError):
            evaluate_physics_consistency_strict(record)

    def test_final_decision_never_authorizes_prototype(self):
        result = generate_final_decision_strict(VALID)
        self.assertEqual(result["status"], "HEURISTIC_RESEARCH_TRIAGE_ONLY")
        self.assertFalse(result["prototype_authorization"])
        self.assertEqual(result["physical_validation"], "NOT_ESTABLISHED")

    def test_confidence_is_labeled_heuristic_not_physical(self):
        result = calculate_scientific_confidence_strict(VALID)
        self.assertEqual(
            result["status"],
            "HEURISTIC_CONFIDENCE_MODEL_STRICT_INPUTS",
        )
        self.assertFalse(result["physical_confidence_claim"])


    def test_material_score_strict_refuses_missing_spectral_quality(self):
        record = dict(VALID)
        record["lsi"] = 3.0
        with self.assertRaises(MissingScientificDataError):
            calculate_material_score_strict(record)

    def test_material_score_strict_accepts_recognized_quality(self):
        record = dict(VALID)
        record["lsi"] = 3.0
        record["spectral_quality"] = "Moderate"
        result = calculate_material_score_strict(record)
        self.assertEqual(
            result["status"],
            "HEURISTIC_MATERIAL_SCORE_STRICT_INPUTS",
        )
        self.assertEqual(result["physical_validation"], "NOT_ESTABLISHED")
        self.assertTrue(0 <= result["score"] <= 100)


class G23IntelligenceHubTests(unittest.TestCase):
    def test_intelligence_summary_refuses_missing_score(self):
        record = dict(VALID)
        del record["research_novelty_score"]
        with self.assertRaises(MissingScientificDataError):
            generate_intelligence_summary_strict(record)

    def test_intelligence_summary_is_explicitly_heuristic(self):
        record = dict(VALID)
        record["system_integrity_score"] = 80.0
        result = generate_intelligence_summary_strict(record)
        self.assertEqual(
            result["status"],
            "HEURISTIC_INTELLIGENCE_STRICT_INPUTS",
        )
        self.assertEqual(result["physical_validation"], "NOT_ESTABLISHED")

    def test_registry_connectivity_counts_isolated_entries_correctly(self):
        registry = {
            "a": {"inputs": ["x"], "outputs": []},
            "b": {"inputs": [], "outputs": []},
            "c": {"inputs": [], "outputs": ["y"]},
        }
        result = analyze_declared_registry_connectivity(registry)
        self.assertEqual(result["declared_connected"], 2)
        self.assertEqual(result["declared_isolated"], 1)
        self.assertEqual(result["declared_connectivity_percent"], 66.67)
        self.assertEqual(result["status"], "STRUCTURAL_CONNECTIVITY_ONLY")


class G23ComponentRegistryTests(unittest.TestCase):
    def test_registry_does_not_claim_production_promotion(self):
        self.assertTrue(G23_COMPONENT_REGISTRY)
        self.assertTrue(
            all(not info["production_promoted"]
                for info in G23_COMPONENT_REGISTRY.values())
        )

    def test_snapshot_is_detached(self):
        snapshot = component_registry_snapshot()
        snapshot["g23_unit_contracts"]["status"] = "MUTATED"
        self.assertEqual(
            G23_COMPONENT_REGISTRY["g23_unit_contracts"]["status"],
            "EXPERIMENTAL_VERIFIED",
        )

    def test_all_components_are_promotion_candidates(self):
        self.assertEqual(
            promotion_candidates(),
            sorted(G23_COMPONENT_REGISTRY),
        )


if __name__ == "__main__":
    unittest.main()
