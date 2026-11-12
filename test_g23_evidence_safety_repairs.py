"""Cross-cutting acceptance tests for G23 evidence safety repairs."""

import copy
import unittest

from g23_evidence_decision_gate import assess_evidence_decision_gate
from g23_evidence_registry import EvidenceConflictError, EvidenceRegistry
from g23_engine_compatibility_audit import audit_engine_compatibility
from g23_scientific_missing_policy import (
    MissingScientificDataError,
    assess_required_numeric,
    require_finite_number,
    strict_weighted_sum,
)
from g23_unit_contracts import (
    mapping_assessment,
    unresolved_legacy_contracts,
)
from photochemcad_evidence_adapter import normalize_photochemcad_record


ASN_BX = {
    "photochemcad_id": "BX003",
    "name": "Asn-Bx",
    "compound_class": "Betaxanthin",
    "lambda_abs_nm": 476,
    "epsilon_M_cm": 56200,
    "phi_f": 0.0074,
    "solvent": "Water",
    "source_url": "https://www.photochemcad.com/databases/betaxanthins/asn-bx",
}

QUERCETIN = {
    "photochemcad_id": "FL109",
    "name": "Quercetin",
    "compound_class": "Flavonol",
    "lambda_abs_nm": 256,
    "epsilon_M_cm": 18700,
    "solvent": "MeOH",
    "source_url": "https://www.photochemcad.com/databases/flavonoids/quercetin",
}

LUTEIN = {
    "photochemcad_id": "CAR021a-6",
    "name": "Lutein [HPLC]",
    "compound_class": "Carotenoids",
    "lambda_abs_nm": 444.5,
    "solvent": "HPLC condition 8 [MeOH/MTBE (97:3)]",
    "source_url": "https://photochemcad.com/databases/carotenoids/lutein-hplc",
}


class MissingDataPolicyTests(unittest.TestCase):
    def test_missing_is_not_zero(self):
        result = assess_required_numeric({"x": 0.0}, ("x", "y"))
        self.assertIn("y", result["missing"])
        self.assertNotIn("x", result["missing"])
        self.assertEqual(require_finite_number({"x": 0.0}, "x"), 0.0)

    def test_required_missing_raises(self):
        with self.assertRaises(MissingScientificDataError):
            require_finite_number({}, "phi")

    def test_weighted_sum_refuses_partial_record(self):
        with self.assertRaises(MissingScientificDataError):
            strict_weighted_sum({"a": 10.0}, {"a": 0.5, "b": 0.5})


class UnitContractTests(unittest.TestCase):
    def test_phi_mapping_is_explicitly_safe(self):
        result = mapping_assessment("phi_f", "phi")
        self.assertTrue(result["allowed"])

    def test_sigma_mapping_is_explicitly_blocked(self):
        result = mapping_assessment("sigma_a_cm2", "sigma_a")
        self.assertFalse(result["allowed"])
        self.assertIn("BLOCKED_UNIT_MISMATCH", result["reason"])

    def test_unresolved_legacy_contracts_are_visible(self):
        unresolved = unresolved_legacy_contracts()
        for field in ("tau", "sigma_a", "eta", "knr"):
            self.assertIn(field, unresolved)


class EngineCompatibilityTests(unittest.TestCase):
    def test_asn_bx_supports_physical_path_not_legacy_scores(self):
        normalized = normalize_photochemcad_record(ASN_BX)
        audit = audit_engine_compatibility(normalized)
        self.assertIn("physical_spectral_evidence_engine", audit["ready_engines"])
        self.assertIn("spectral_quality_engine", audit["blocked_engines"])
        self.assertIn("lsi_engine", audit["blocked_engines"])

    def test_emission_enables_only_emission_dependent_display_paths(self):
        normalized = normalize_photochemcad_record(dict(ASN_BX, lambda_em_nm=510))
        audit = audit_engine_compatibility(normalized)
        self.assertIn("spectral_analysis", audit["ready_engines"])
        self.assertIn("spectral_region", audit["ready_engines"])
        self.assertIn("color_predictor", audit["ready_engines"])
        self.assertIn("pump_predictor", audit["blocked_engines"])


class EvidenceRegistryTests(unittest.TestCase):
    def test_registry_accepts_three_records_and_reports_mean_completeness(self):
        registry = EvidenceRegistry()
        for raw in (ASN_BX, QUERCETIN, LUTEIN):
            registry.add(normalize_photochemcad_record(raw))
        stats = registry.statistics()
        self.assertEqual(stats["total_records"], 3)
        self.assertEqual(stats["mean_evidence_completeness"], 50.0)
        self.assertEqual(stats["partial_core_records"], 2)
        self.assertEqual(stats["sparse_core_records"], 1)

    def test_registry_is_idempotent_for_identical_record(self):
        registry = EvidenceRegistry()
        normalized = normalize_photochemcad_record(ASN_BX)
        first = registry.add(normalized)
        second = registry.add(normalized)
        self.assertEqual(first, second)
        self.assertEqual(registry.statistics()["total_records"], 1)

    def test_registry_rejects_conflicting_duplicate(self):
        registry = EvidenceRegistry()
        normalized = normalize_photochemcad_record(ASN_BX)
        registry.add(normalized)
        conflicting = copy.deepcopy(normalized)
        conflicting["phi_f"] = 0.02
        with self.assertRaises(EvidenceConflictError):
            registry.add(conflicting)

    def test_registry_returns_copies(self):
        registry = EvidenceRegistry()
        normalized = normalize_photochemcad_record(ASN_BX)
        registry.add(normalized)
        fetched = registry.get("PhotochemCAD:BX003")
        fetched["normalized_record"]["phi_f"] = 0.99
        fetched_again = registry.get("PhotochemCAD:BX003")
        self.assertEqual(fetched_again["normalized_record"]["phi_f"], 0.0074)


class EvidenceDecisionGateTests(unittest.TestCase):
    def test_advanced_claims_are_all_blocked_for_photochemcad_only(self):
        normalized = normalize_photochemcad_record(ASN_BX)
        gate = assess_evidence_decision_gate(normalized)
        self.assertTrue(gate["allowed_actions"]["store_traceable_evidence"])
        self.assertTrue(gate["allowed_actions"]["use_quantitative_absorption"])
        self.assertFalse(any(gate["advanced_claims"].values()))
        self.assertIn("final_decision_engine", gate["blocked_legacy_decision_engines"])

    def test_missing_emission_blocks_stokes_and_color(self):
        normalized = normalize_photochemcad_record(ASN_BX)
        gate = assess_evidence_decision_gate(normalized)
        self.assertFalse(gate["allowed_actions"]["derive_stokes_shift"])
        self.assertFalse(gate["allowed_actions"]["classify_display_color"])

    def test_reported_emission_enables_stokes_and_color_only_as_supported_actions(self):
        normalized = normalize_photochemcad_record(dict(ASN_BX, lambda_em_nm=510))
        gate = assess_evidence_decision_gate(normalized)
        self.assertTrue(gate["allowed_actions"]["derive_stokes_shift"])
        self.assertTrue(gate["allowed_actions"]["classify_display_color"])
        self.assertFalse(gate["advanced_claims"]["laser_gain_established"])


if __name__ == "__main__":
    unittest.main()
