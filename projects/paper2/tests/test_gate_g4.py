"""Synthetic tests: no claim of experimental validation."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("gate_g4", ROOT / "gate_g4.py")
g4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g4)

class G4Tests(unittest.TestCase):
    def test_identical_spectra_pass(self):
        x = np.arange(350.0, 711.0, 2.0)
        y = 0.1 + np.exp(-((x - 430) / 25) ** 2)
        a = np.column_stack((x, y))
        report = g4.compute(a, a.copy())
        self.assertEqual(report["status"], "PASS")
        self.assertAlmostEqual(report["runs"][1]["nrmse_minmax"], 0.0)
        self.assertEqual(report["original_sampled_peaks"]["a_nm"],
                         report["original_sampled_peaks"]["b_nm"])

    def test_overlap_rejected(self):
        x = np.arange(350.0, 400.0, 2.0)
        a = np.column_stack((x, np.sin(x / 10)))
        b = np.column_stack((x + 100, np.sin(x / 10)))
        with self.assertRaises(ValueError):
            g4.compute(a, b)

    def test_metrics_finite(self):
        x = np.arange(350.0, 711.0, 2.0)
        a = np.column_stack((x, 0.1 + np.exp(-((x - 430) / 25) ** 2)))
        b = np.column_stack((x, 0.1 + np.exp(-((x - 432) / 25) ** 2)))
        report = g4.compute(a, b)
        for run in report["runs"]:
            self.assertTrue(np.isfinite(run["nrmse_minmax"]))
            self.assertTrue(np.isfinite(run["pearson_r"]))

if __name__ == "__main__":
    unittest.main()
