import copy
import unittest

class RealPipelineTest(unittest.TestCase):
    def test_original_analysis_preserves_evidence_hold(self):
        from main import analyze_plant
        from plants_data import plants
        self.assertTrue(plants)
        result = analyze_plant(copy.deepcopy(plants[0]))
        self.assertTrue(result["valid"])
        self.assertEqual(result["evidence_decision"]["decision"], "HOLD")
        self.assertTrue(result["final_decision"].startswith("HOLD"))
        self.assertIn("governor_decision", result)

    def test_all_registered_plant_records(self):
        from main import analyze_plant
        from plants_data import plants
        self.assertTrue(plants)
        for record in plants:
            with self.subTest(plant=record.get("name")):
                result = analyze_plant(copy.deepcopy(record))
                self.assertTrue(result["valid"])
                self.assertEqual(result["evidence_decision"]["decision"], "HOLD")
                self.assertTrue(result["final_decision"].startswith("HOLD"))
                self.assertIn("governor_decision", result)

    def test_real_launcher_preparation(self):
        from safe_dashboard_launcher import prepare_dashboard_plants
        from plants_data import plants
        original = copy.deepcopy(plants)
        ranked = prepare_dashboard_plants(plants)
        self.assertEqual(plants, original)
        self.assertEqual(len(ranked), len(plants))
        for result in ranked:
            self.assertTrue(result["valid"])
            self.assertEqual(result["evidence_decision"]["decision"], "HOLD")

if __name__ == "__main__":
    unittest.main()
