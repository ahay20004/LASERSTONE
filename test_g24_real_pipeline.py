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


    def test_explicit_correlations_reach_real_pipeline(self):
        from main import analyze_plant
        from plants_data import plants
        from data_validator import PHYSICAL_PARAMETER_RULES
        plant = copy.deepcopy(plants[0])
        values = dict(lambda_em=632.8, refractive_index=1, cavity_length_m=.2,
                      mirror_r1=.999, mirror_r2=.95, internal_loss_m_inv=.1, gain_m_inv=.3)
        plant["physical_parameter_records"] = {
            k: dict(value=v, unit=PHYSICAL_PARAMETER_RULES[k][0],
                    standard_uncertainty=.01, source_id="synthetic",
                    conditions_id="synthetic", basis="assumed") for k,v in values.items()}
        keys=("internal_loss_m_inv","mirror_r1","mirror_r2","cavity_length_m")
        all_keys=keys+("gain_m_inv",)
        matrix={k:{j:float(k==j) for j in all_keys} for k in all_keys}
        matrix["gain_m_inv"]["internal_loss_m_inv"]=matrix["internal_loss_m_inv"]["gain_m_inv"]=1
        plant["threshold_correlation"]={k:{j:matrix[k][j] for j in keys} for k in keys}
        plant["gain_correlation"]=matrix
        result=analyze_plant(plant)["evidence_decision"]
        self.assertEqual(result["threshold_uncertainty"]["status"],"DERIVED")
        self.assertEqual(result["gain_margin_uncertainty"]["status"],"DERIVED")
        self.assertEqual(result["decision"],"HOLD")
        self.assertFalse(result["prototype_authorized"])

if __name__ == "__main__":
    unittest.main()
