"""Acceptance tests for diagnostic comparison of spectral paths."""

import unittest

from photochemcad_evidence_adapter import normalize_photochemcad_record
from spectral_path_comparison import NON_EQUIVALENT, compare_spectral_paths


CASES = (
    (
        {
            "photochemcad_id": "BX003",
            "name": "Asn-Bx",
            "compound_class": "Betaxanthin",
            "lambda_abs_nm": 476,
            "epsilon_M_cm": 56200,
            "phi_f": 0.0074,
            "solvent": "Water",
            "source_url": "https://www.photochemcad.com/databases/betaxanthins/asn-bx",
        },
        75.0,
    ),
    (
        {
            "photochemcad_id": "FL109",
            "name": "Quercetin",
            "compound_class": "Flavonol",
            "lambda_abs_nm": 256,
            "epsilon_M_cm": 18700,
            "solvent": "MeOH",
            "source_url": "https://www.photochemcad.com/databases/flavonoids/quercetin",
        },
        50.0,
    ),
    (
        {
            "photochemcad_id": "CAR021a-6",
            "name": "Lutein [HPLC]",
            "compound_class": "Carotenoids",
            "lambda_abs_nm": 444.5,
            "solvent": "HPLC condition 8 [MeOH/MTBE (97:3)]",
            "source_url": "https://photochemcad.com/databases/carotenoids/lutein-hplc",
        },
        25.0,
    ),
)


class SpectralPathComparisonTests(unittest.TestCase):
    def test_three_cases_remain_physically_analyzable(self):
        for raw, expected in CASES:
            with self.subTest(raw["photochemcad_id"]):
                normalized = normalize_photochemcad_record(raw)
                result = compare_spectral_paths(normalized)
                self.assertEqual(
                    result["physical_evidence_completeness_score"],
                    expected,
                )
                self.assertEqual(result["physical_path_status"], "AVAILABLE")

    def test_legacy_path_is_blocked_for_all_three(self):
        for raw, _ in CASES:
            with self.subTest(raw["photochemcad_id"]):
                normalized = normalize_photochemcad_record(raw)
                result = compare_spectral_paths(normalized)
                self.assertEqual(
                    result["legacy_path_status"],
                    "LEGACY_SPECTRAL_ENGINE_BLOCKED_MISSING_OR_UNSAFE_FIELDS",
                )
                self.assertIsNone(result["legacy_spectral_quality"])
                self.assertIn(
                    "sigma_a",
                    result["legacy_spectral_missing_or_unsafe_fields"],
                )

    def test_outputs_are_explicitly_non_equivalent(self):
        normalized = normalize_photochemcad_record(CASES[0][0])
        result = compare_spectral_paths(normalized)
        self.assertEqual(result["comparison_status"], NON_EQUIVALENT)

    def test_asn_bx_only_safe_legacy_fields_are_phi_and_lambda_abs(self):
        normalized = normalize_photochemcad_record(CASES[0][0])
        result = compare_spectral_paths(normalized)
        self.assertEqual(
            result["legacy_safe_fields_available"],
            ["lambda_abs", "phi"],
        )

    def test_quercetin_does_not_gain_phi_from_legacy_defaults(self):
        normalized = normalize_photochemcad_record(CASES[1][0])
        result = compare_spectral_paths(normalized)
        self.assertEqual(
            result["legacy_safe_fields_available"],
            ["lambda_abs"],
        )
        self.assertIn(
            "phi",
            result["legacy_spectral_missing_or_unsafe_fields"],
        )

    def test_lutein_remains_sparse_without_epsilon_or_phi(self):
        normalized = normalize_photochemcad_record(CASES[2][0])
        result = compare_spectral_paths(normalized)
        self.assertEqual(
            result["legacy_safe_fields_available"],
            ["lambda_abs"],
        )
        self.assertEqual(
            result["physical_evidence_completeness_score"],
            25.0,
        )


if __name__ == "__main__":
    unittest.main()
