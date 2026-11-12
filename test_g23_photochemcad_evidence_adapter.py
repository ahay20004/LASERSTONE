"""Acceptance tests for the G23 PhotochemCAD evidence adapter.

Run:
    python -m unittest -v test_g23_photochemcad_evidence_adapter.py

These tests are deliberately read-only and use three manually verified
PhotochemCAD records. They do not perform network access.
"""

import copy
import unittest

from photochemcad_evidence_adapter import (
    DERIVED,
    MISSING,
    REPORTED,
    epsilon_to_sigma_cm2,
    normalize_photochemcad_record,
)


ASN_BX = {
    "photochemcad_id": "BX003",
    "name": "Asn-Bx",
    "compound_class": "Betaxanthin",
    "lambda_abs_nm": 476,
    "epsilon_M_cm": 56200,
    "phi_f": 0.0074,
    "solvent": "Water",
    "instrument": "Varian Cary 50 / Edimburgh FLS980",
    "reference": "Esteves et al., J. Nat. Prod. 2025",
    "source_url": "https://www.photochemcad.com/databases/betaxanthins/asn-bx",
}

QUERCETIN = {
    "photochemcad_id": "FL109",
    "name": "Quercetin",
    "compound_class": "Flavonol",
    "lambda_abs_nm": 256,
    "epsilon_M_cm": 18700,
    "solvent": "MeOH",
    "reference": "Taniguchi, 2022",
    "source_url": "https://www.photochemcad.com/databases/flavonoids/quercetin",
}

LUTEIN_HPLC = {
    "photochemcad_id": "CAR021a-6",
    "name": "Lutein [HPLC]",
    "compound_class": "Carotenoids",
    "lambda_abs_nm": 444.5,
    "solvent": "HPLC condition 8 [MeOH/MTBE (97:3)]",
    "source_url": "https://photochemcad.com/databases/carotenoids/lutein-hplc",
}


class PhotochemCADEvidenceAdapterAcceptanceTests(unittest.TestCase):
    def test_asn_bx_preserves_reported_values_and_derives_sigma(self):
        result = normalize_photochemcad_record(ASN_BX)
        self.assertEqual(result["lambda_abs_nm"], 476.0)
        self.assertEqual(result["epsilon_M_cm"], 56200.0)
        self.assertEqual(result["phi_f"], 0.0074)
        self.assertAlmostEqual(
            result["sigma_a_cm2"],
            2.1488252663537107e-16,
            delta=1e-28,
        )
        self.assertEqual(result["field_evidence"]["epsilon_M_cm"], REPORTED)
        self.assertEqual(result["field_evidence"]["sigma_a_cm2"], DERIVED)

    def test_quercetin_does_not_invent_missing_fluorescence(self):
        result = normalize_photochemcad_record(QUERCETIN)
        self.assertIsNone(result["phi_f"])
        self.assertIsNone(result["lambda_em_nm"])
        self.assertEqual(result["field_evidence"]["phi_f"], MISSING)
        self.assertEqual(result["field_evidence"]["lambda_em_nm"], MISSING)
        self.assertIsNotNone(result["sigma_a_cm2"])

    def test_lutein_does_not_invent_epsilon_or_sigma(self):
        result = normalize_photochemcad_record(LUTEIN_HPLC)
        self.assertEqual(result["lambda_abs_nm"], 444.5)
        self.assertIsNone(result["epsilon_M_cm"])
        self.assertIsNone(result["sigma_a_cm2"])
        self.assertEqual(result["field_evidence"]["epsilon_M_cm"], MISSING)
        self.assertEqual(result["field_evidence"]["sigma_a_cm2"], MISSING)
        self.assertIsNone(result["derivation_method"])

    def test_adapter_is_read_only(self):
        source = copy.deepcopy(ASN_BX)
        before = copy.deepcopy(source)
        normalize_photochemcad_record(source)
        self.assertEqual(source, before)

    def test_invalid_quantum_yield_is_rejected(self):
        bad = dict(ASN_BX, phi_f=1.2)
        with self.assertRaises(ValueError):
            normalize_photochemcad_record(bad)

    def test_nonphysical_wavelength_is_rejected(self):
        bad = dict(ASN_BX, lambda_abs_nm=0)
        with self.assertRaises(ValueError):
            normalize_photochemcad_record(bad)

    def test_conversion_formula_is_stable(self):
        self.assertAlmostEqual(
            epsilon_to_sigma_cm2(56200),
            2.1488252663537107e-16,
            delta=1e-28,
        )


if __name__ == "__main__":
    unittest.main()
