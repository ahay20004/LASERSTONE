"""Source-record impact report invariants."""
import unittest
from cloud.source_dataset_spectral_impact import assess_dataset
from plants_data import plants


class DatasetImpactTests(unittest.TestCase):
    def test_all_source_records_accounted_and_no_silent_scores(self):
        result = assess_dataset()
        self.assertEqual(result["total_records"], len(plants))
        self.assertEqual(result["compared"] + result["blocked"], len(plants))
        self.assertFalse(result["original_main_modified"])
        self.assertFalse(result["original_data_modified"])
        for row in result["rows"]:
            if row["status"] == "COMPARED":
                self.assertAlmostEqual(
                    row["corrected_material_score"] - row["legacy_material_score"],
                    row["delta"], places=2,
                )
                self.assertIn(row["spectral_label"], ("High", "Medium", "Low"))
            else:
                self.assertNotIn("corrected_material_score", row)


if __name__ == "__main__":
    unittest.main()
