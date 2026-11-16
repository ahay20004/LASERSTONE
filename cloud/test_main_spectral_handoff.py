"""End-to-end canonical spectral handoff checks on original source records."""
import unittest
from plants_data import plants
from main import analyze_plant
from material_score_engine import calculate_material_score
from data_standardization_engine import standardize_quality_value


class MainSpectralHandoffTests(unittest.TestCase):
    def test_main_uses_numeric_spectral_handoff_without_losing_label(self):
        compared = 0
        for source in plants:
            with self.subTest(plant=source.get("name")):
                result = analyze_plant(source, canonical_spectral_handoff=True)
                if result.get("analysis_status") != "COMPLETE_HEURISTIC_ANALYSIS":
                    continue
                compared += 1
                label = result["spectral_quality"]
                self.assertIn(label, ("High", "Medium", "Low"))
                self.assertEqual(result["spectral_quality_score"],
                                 standardize_quality_value(label))
                canonical = dict(result, spectral_quality=result["spectral_quality_score"])
                self.assertEqual(result["material_score"], calculate_material_score(canonical))
                legacy = dict(result, spectral_quality=label)
                self.assertEqual(
                    round(result["material_score"] - calculate_material_score(legacy), 2),
                    {"High": 6.0, "Medium": 2.0, "Low": -1.0}[label],
                )
        self.assertGreater(compared, 0, "No source record completes the analysis")


if __name__ == "__main__":
    unittest.main()
