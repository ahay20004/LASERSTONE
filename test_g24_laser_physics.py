import unittest
import math
from laser_physics_engine import calculate_laser_physics


class LaserPhysicsG24Tests(unittest.TestCase):
    def test_photon(self):
        r = calculate_laser_physics({"lambda_em": 632.8})
        self.assertAlmostEqual(r["frequency_hz"]/1e12, 473.7554646, places=5)
        self.assertAlmostEqual(r["photon_energy_ev"], 1.959295, places=5)

    def test_independent_cavity(self):
        r = calculate_laser_physics({"lambda_em": 632.8, "cavity_length_m": .2})
        self.assertAlmostEqual(r["free_spectral_range_hz"], 749481145.0)
        self.assertEqual(r["nearest_longitudinal_mode"], 632111)

    def test_group_index(self):
        r = calculate_laser_physics({"cavity_length_m": .2, "group_index": 1.5})
        self.assertTrue(math.isclose(r["free_spectral_range_hz"], 499654096.6666667,
                                     rel_tol=1e-12, abs_tol=0.0))

    def test_threshold(self):
        p = dict(cavity_length_m=.2, mirror_r1=.999, mirror_r2=.95,
                 internal_loss_m_inv=.1, gain_m_inv=.3)
        r = calculate_laser_physics(p)
        self.assertAlmostEqual(r["threshold_gain_m_inv"], .2307344868025, places=5)
        self.assertEqual(r["threshold_status"], "ABOVE_THRESHOLD")
        p["gain_m_inv"] = .1
        self.assertEqual(calculate_laser_physics(p)["threshold_status"], "BELOW_THRESHOLD")
        p["gain_m_inv"] = r["threshold_gain_m_inv"]
        self.assertEqual(calculate_laser_physics(p)["threshold_status"], "AT_THRESHOLD")

    def test_missing_evidence(self):
        self.assertEqual(calculate_laser_physics({})["threshold_status"], "UNVERIFIED")

    def test_invalid(self):
        for p in ({"lambda_em": -1}, {"refractive_index": 0},
                  {"cavity_length_m": float("nan")}, {"longitudinal_mode": 1.5}):
            with self.subTest(p=p), self.assertRaises(ValueError):
                calculate_laser_physics(p)

    def test_partial_invalid_evidence(self):
        for p in ({"mirror_r1": 2}, {"mirror_r2": 0}, {"internal_loss_m_inv": -1}, {"gain_m_inv": float("inf")}):
            with self.subTest(p=p), self.assertRaises(ValueError):
                calculate_laser_physics(p)

    def test_mode_scaling(self):
        p = {"lambda_em": 500, "longitudinal_mode": 10}
        r = calculate_laser_physics(p)
        self.assertAlmostEqual(r["cavity_length_m"], 2.5e-6)
        self.assertAlmostEqual(r["free_spectral_range_hz"], r["frequency_hz"]/10)


if __name__ == "__main__":
    unittest.main()
