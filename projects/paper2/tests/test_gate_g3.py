"""G3 physical evidence tests: controls eligibility, not scientific proof."""
import importlib.util
from pathlib import Path
import unittest

root = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("gate_g3", root / "gate_g3.py")
g3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g3)

class PhysicalEvidenceGateTests(unittest.TestCase):
    def test_absorption_only_blocks_laser_claims(self):
        r = g3.evaluate(["absorption"])
        self.assertEqual(r["claims"]["absorption_peak"]["status"], "ELIGIBLE_FOR_REVIEW")
        for claim in ("optical_gain", "laser_threshold", "stimulated_emission",
                      "stokes_shift", "emission_peak"):
            self.assertEqual(r["claims"][claim]["status"], "NOT_SUPPORTED")
        self.assertTrue(all(r["physical_boundary_checks"].values()))

    def test_emission_and_absorption_stokes_eligible(self):
        r = g3.evaluate(["absorption", "emission"])
        self.assertEqual(r["claims"]["stokes_shift"]["status"], "ELIGIBLE_FOR_REVIEW")
        self.assertEqual(r["claims"]["optical_gain"]["status"], "NOT_SUPPORTED")
        self.assertEqual(r["claims"]["laser_threshold"]["status"], "NOT_SUPPORTED")

    def test_gain_needs_gain_specific_evidence(self):
        r = g3.evaluate(["absorption", "emission", "stimulated_emission",
                         "gain_calibration", "pump_geometry"])
        self.assertEqual(r["claims"]["optical_gain"]["status"], "ELIGIBLE_FOR_REVIEW")
        self.assertEqual(r["claims"]["laser_threshold"]["status"], "NOT_SUPPORTED")

    def test_threshold_needs_pump_threshold_data(self):
        r = g3.evaluate(["stimulated_emission", "pump_geometry", "pump_threshold"])
        self.assertEqual(r["claims"]["laser_threshold"]["status"], "ELIGIBLE_FOR_REVIEW")
        self.assertEqual(r["claims"]["optical_gain"]["status"], "NOT_SUPPORTED")

    def test_reject_unknown_evidence(self):
        with self.assertRaises(ValueError):
            g3.evaluate(["absorption", "magic"])

if __name__ == "__main__":
    unittest.main()
