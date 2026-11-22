"""Synthetic G2 tests; no unpublished or third-party spectra."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np

spec = importlib.util.spec_from_file_location("gate_g2", Path(__file__).resolve().parents[1] / "gate_g2.py")
g2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g2)

def spectrum(start=350, stop=710, step=2):
    x = np.arange(start, stop, step, dtype=float)
    return np.column_stack((x, np.exp(-((x-430)/30)**2)))

class SpectralInputTests(unittest.TestCase):
    def test_valid_overlap(self):
        self.assertEqual(g2.validate(spectrum(), spectrum())["status"], "PASS")
    def test_disjoint_spectra(self):
        self.assertEqual(g2.validate(spectrum(), spectrum(800, 1000))["status"], "FAIL")
    def test_duplicate_wavelength(self):
        a = spectrum()
        a[1, 0] = a[0, 0]
        self.assertEqual(g2.validate(a, spectrum())["status"], "FAIL")
    def test_nonfinite_signal(self):
        a = spectrum()
        a[3, 1] = np.nan
        self.assertEqual(g2.validate(a, spectrum())["status"], "FAIL")
    def test_nonpositive_step(self):
        self.assertEqual(g2.validate(spectrum(), spectrum(), 0)["status"], "FAIL")
    def test_constant_overlap(self):
        a = spectrum()
        a[:, 1] = 1.0
        self.assertEqual(g2.validate(a, spectrum())["status"], "FAIL")

if __name__ == "__main__":
    unittest.main()
