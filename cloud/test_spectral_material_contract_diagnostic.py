"""Regression guard for the spectral-to-material semantic contract discrepancy."""
import unittest
from cloud.spectral_material_contract_diagnostic import diagnose_spectral_material_contract


class SpectralMaterialContractTests(unittest.TestCase):
    def test_detects_exact_current_legacy_discrepancy(self):
        result = diagnose_spectral_material_contract()
        self.assertEqual(result["mismatched_labels"], ["High", "Medium", "Low"])
        self.assertEqual(
            [(r["label"], r["standardization_score"],
              r["material_direct_conversion_score"]) for r in result["rows"]],
            [("High", 100, 40), ("Medium", 60, 40), ("Low", 30, 40)],
        )
        self.assertFalse(result["original_engines_modified"])
        self.assertFalse(result["physical_validation"])


if __name__ == "__main__":
    unittest.main()
