import math
import unittest
from physics_checks import bragg_nm, scherrer_nm, photon_energy_ev, shift_ratio

class SyntheticChecks(unittest.TestCase):
    def test_bragg(self):
        self.assertAlmostEqual(bragg_nm(0.2, 60), 0.2)
    def test_scherrer(self):
        self.assertAlmostEqual(scherrer_nm(0.2, 60, 0.01, 0.9), 18 / math.cos(math.pi / 6))
    def test_energy(self):
        self.assertAlmostEqual(photon_energy_ev(500), 2.479683968664005)
    def test_shift(self):
        self.assertEqual(shift_ratio(500, 500, 1e9), 0)
        self.assertAlmostEqual(shift_ratio(500, 600, 1e14), 0.9993081933333333)
    def test_invalid(self):
        for x in (0, -1, float("nan"), float("inf"), True):
            with self.assertRaises(ValueError):
                photon_energy_ev(x)
        with self.assertRaises(ValueError):
            bragg_nm(0.2, 180)
        with self.assertRaises(ValueError):
            scherrer_nm(0.2, 60, 4, 0.9)
