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

if __name__ == "__main__":
    unittest.main()
