"""Acceptance tests for the G23 physical spectral evidence engine."""

import copy
import unittest

from photochemcad_evidence_adapter import normalize_photochemcad_record
from physical_spectral_evidence_engine import (
    LASER_CLAIM_STATUS,
    analyze_physical_spectral_evidence,
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


class PhysicalSpectralEvidenceEngineTests(unittest.TestCase):
    def test_asn_bx_completeness_is_three_of_four_independent_fields(self):
        normalized = normalize_photochemcad_record(ASN_BX)
        result = analyze_physical_spectral_evidence(normalized)

        self.assertEqual(result["independent_reported_count"], 3)
        self.assertEqual(result["evidence_completeness_score"], 75.0)
        self.assertEqual(
            result["evidence_status"],
            "PARTIAL_CORE_SPECTRAL_EVIDENCE",
        )
        self.assertTrue(
            result["capabilities"]["quantitative_absorption_available"]
        )
        self.assertFalse(
            result["capabilities"]["fluorescence_peak_available"]
        )

    def test_quercetin_completeness_is_two_of_four(self):
        normalized = normalize_photochemcad_record(QUERCETIN)
        result = analyze_physical_spectral_evidence(normalized)

        self.assertEqual(result["independent_reported_count"], 2)
        self.assertEqual(result["evidence_completeness_score"], 50.0)
        self.assertIsNotNone(result["sigma_a_cm2"])
        self.assertIsNone(result["phi_f"])

    def test_lutein_is_sparse_not_artificially_completed(self):
        normalized = normalize_photochemcad_record(LUTEIN)
        result = analyze_physical_spectral_evidence(normalized)

        self.assertEqual(result["independent_reported_count"], 1)
        self.assertEqual(result["evidence_completeness_score"], 25.0)
        self.assertEqual(
            result["evidence_status"],
            "SPARSE_CORE_SPECTRAL_EVIDENCE",
        )
        self.assertIsNone(result["epsilon_M_cm"])
        self.assertIsNone(result["sigma_a_cm2"])

    def test_derived_sigma_is_not_double_counted(self):
        normalized = normalize_photochemcad_record(ASN_BX)
        result = analyze_physical_spectral_evidence(normalized)

        self.assertIsNotNone(result["sigma_a_cm2"])
        self.assertNotIn("sigma_a_cm2", result["reported_core_fields"])
        self.assertEqual(result["independent_reported_count"], 3)

    def test_stokes_shift_is_derived_only_when_both_peaks_exist(self):
        raw = dict(ASN_BX, lambda_em_nm=510)
        normalized = normalize_photochemcad_record(raw)
        result = analyze_physical_spectral_evidence(normalized)

        self.assertEqual(result["stokes_shift_nm"], 34.0)
        self.assertEqual(result["stokes_shift_flag"], "POSITIVE_STOKES_SHIFT")
        self.assertAlmostEqual(
            result["stokes_shift_cm_inv"],
            1.0e7 * ((1.0 / 476.0) - (1.0 / 510.0)),
            places=9,
        )

    def test_no_performance_or_lasing_claim_is_generated(self):
        normalized = normalize_photochemcad_record(ASN_BX)
        result = analyze_physical_spectral_evidence(normalized)

        self.assertIsNone(result["performance_score"])
        self.assertEqual(result["laser_gain_status"], LASER_CLAIM_STATUS)
        self.assertEqual(result["lasing_feasibility_status"], LASER_CLAIM_STATUS)

    def test_engine_is_read_only(self):
        normalized = normalize_photochemcad_record(ASN_BX)
        before = copy.deepcopy(normalized)
        analyze_physical_spectral_evidence(normalized)
        self.assertEqual(normalized, before)

    def test_non_photochemcad_source_is_rejected(self):
        normalized = normalize_photochemcad_record(ASN_BX)
        normalized["source_database"] = "OtherDB"
        with self.assertRaises(ValueError):
            analyze_physical_spectral_evidence(normalized)


if __name__ == "__main__":
    unittest.main()
