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

    def test_report_output_and_conflict(self):
        from pathlib import Path
        from tempfile import TemporaryDirectory
        from report_generator import save_single_report, ensure_reports_folder
        from safe_dashboard_launcher import prepare_dashboard_plants
        from plants_data import plants
        ranked = prepare_dashboard_plants(plants)
        self.assertTrue(ranked)
        with TemporaryDirectory() as directory:
            conflict = Path(directory) / "conflict"
            conflict.write_text("preserve", encoding="utf-8")
            with self.assertRaises(OSError):
                ensure_reports_folder(conflict)
            self.assertEqual(conflict.read_text(encoding="utf-8"), "preserve")
            report = Path(save_single_report(ranked[0], Path(directory) / "reports"))
            self.assertIn("HOLD", report.read_text(encoding="utf-8"))
            report.write_text("previous evidence", encoding="utf-8")
            next_report = Path(save_single_report(ranked[0], Path(directory) / "reports"))
            self.assertNotEqual(report, next_report)
            self.assertEqual(report.read_text(encoding="utf-8"), "previous evidence")
            self.assertIn("HOLD", next_report.read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
