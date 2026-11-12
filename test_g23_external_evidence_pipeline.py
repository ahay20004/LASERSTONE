"""Acceptance tests for the unified G23 external evidence pipeline."""

import unittest

from g23_evidence_registry import EvidenceRegistry
from g23_external_evidence_pipeline import (
    process_photochemcad_batch,
    process_photochemcad_evidence,
)
from plants_data import plants


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


class ExternalEvidencePipelineTests(unittest.TestCase):
    def test_single_record_runs_full_evidence_safe_path(self):
        registry = EvidenceRegistry()
        result = process_photochemcad_evidence(
            ASN_BX,
            registry=registry,
            legacy_plants=plants,
        )
        self.assertEqual(result["pipeline_status"], "EVIDENCE_SAFE_COMPLETE")
        self.assertFalse(result["legacy_scoring_invoked"])
        self.assertFalse(result["production_registry_mutated"])
        self.assertFalse(result["advanced_claims_authorized"])
        self.assertEqual(registry.statistics()["total_records"], 1)

    def test_quercetin_links_to_moringa_without_substitution(self):
        result = process_photochemcad_evidence(
            QUERCETIN,
            legacy_plants=plants,
        )
        self.assertEqual(len(result["legacy_plant_links"]), 1)
        link = result["legacy_plant_links"][0]
        self.assertEqual(link["plant_name"], "Moringa")
        self.assertFalse(link["substitution_allowed"])

    def test_batch_uses_shared_registry_and_preserves_completeness(self):
        result = process_photochemcad_batch(
            [ASN_BX, QUERCETIN, LUTEIN],
            legacy_plants=plants,
        )
        self.assertEqual(result["record_count"], 3)
        self.assertEqual(result["registry_statistics"]["total_records"], 3)
        self.assertEqual(
            result["registry_statistics"]["mean_evidence_completeness"],
            50.0,
        )
        self.assertFalse(result["legacy_scoring_invoked"])
        self.assertFalse(result["production_registry_mutated"])

    def test_pipeline_never_authorizes_advanced_claims(self):
        result = process_photochemcad_evidence(
            dict(ASN_BX, lambda_em_nm=510),
            legacy_plants=plants,
        )
        self.assertTrue(result["decision_gate"]["allowed_actions"]["derive_stokes_shift"])
        self.assertFalse(any(result["decision_gate"]["advanced_claims"].values()))
        self.assertIsNone(result["output"]["estimated_laser_power"])


if __name__ == "__main__":
    unittest.main()
