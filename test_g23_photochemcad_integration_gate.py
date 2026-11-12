"""Acceptance tests for PhotochemCAD -> legacy LASERSTONE integration gate."""

import copy
import unittest

from photochemcad_evidence_adapter import normalize_photochemcad_record
from photochemcad_integration_gate import (
    SIGMA_BLOCKER,
    assess_photochemcad_for_legacy,
)


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


class PhotochemCADIntegrationGateTests(unittest.TestCase):
    def test_asn_bx_maps_only_semantically_safe_fields(self):
        normalized = normalize_photochemcad_record(ASN_BX)
        result = assess_photochemcad_for_legacy(normalized)

        self.assertEqual(result["safe_legacy_map"]["phi"], 0.0074)
        self.assertEqual(result["safe_legacy_map"]["lambda_abs"], 476.0)
        self.assertNotIn("sigma_a", result["safe_legacy_map"])
        self.assertNotIn("lambda_em", result["safe_legacy_map"])

    def test_physical_sigma_is_separate_and_unit_bearing(self):
        normalized = normalize_photochemcad_record(ASN_BX)
        result = assess_photochemcad_for_legacy(normalized)

        self.assertIsNotNone(result["physical_evidence"]["sigma_a_cm2"])
        self.assertEqual(
            result["physical_evidence"]["unit"],
            "cm^2 molecule^-1",
        )
        self.assertIn(SIGMA_BLOCKER, result["blockers"])

    def test_quercetin_does_not_invent_phi(self):
        normalized = normalize_photochemcad_record(QUERCETIN)
        result = assess_photochemcad_for_legacy(normalized)

        self.assertEqual(result["safe_legacy_map"], {"lambda_abs": 256.0})
        self.assertIn("phi", result["unresolved_legacy_fields"])
        self.assertFalse(result["promotable_to_legacy_scientific_pipeline"])

    def test_lutein_does_not_invent_sigma(self):
        normalized = normalize_photochemcad_record(LUTEIN)
        result = assess_photochemcad_for_legacy(normalized)

        self.assertIsNone(result["physical_evidence"]["sigma_a_cm2"])
        self.assertNotIn("sigma_a", result["safe_legacy_map"])
        self.assertIn("sigma_a", result["unresolved_legacy_fields"])

    def test_missing_legacy_fields_block_execution(self):
        normalized = normalize_photochemcad_record(ASN_BX)
        result = assess_photochemcad_for_legacy(normalized)

        self.assertEqual(result["status"], "BLOCKED_FROM_LEGACY_EXECUTION")
        for field in ("tau", "sigma_a", "eta", "knr", "refractive_index", "lambda_em"):
            self.assertIn(field, result["unresolved_legacy_fields"])

    def test_gate_is_read_only(self):
        normalized = normalize_photochemcad_record(ASN_BX)
        before = copy.deepcopy(normalized)
        assess_photochemcad_for_legacy(normalized)
        self.assertEqual(normalized, before)

    def test_non_photochemcad_source_is_rejected(self):
        normalized = normalize_photochemcad_record(ASN_BX)
        normalized["source_database"] = "OtherDB"
        with self.assertRaises(ValueError):
            assess_photochemcad_for_legacy(normalized)

    def test_lambda_em_maps_only_when_reported(self):
        raw = dict(ASN_BX, lambda_em_nm=510)
        normalized = normalize_photochemcad_record(raw)
        result = assess_photochemcad_for_legacy(normalized)
        self.assertEqual(result["safe_legacy_map"]["lambda_em"], 510.0)


if __name__ == "__main__":
    unittest.main()
