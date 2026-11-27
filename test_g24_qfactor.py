import math
import unittest
from qfactor_engine import calculate_physical_q

class PhysicalQTests(unittest.TestCase):
    def test_linewidth(self):
        self.assertEqual(calculate_physical_q(5e14, linewidth_hz=5e9)["q"], 1e5)

    def test_lifetime(self):
        r = calculate_physical_q(5e14, energy_lifetime_s=1/(2*math.pi*5e9))
        self.assertTrue(math.isclose(r["q"], 1e5, rel_tol=1e-12))

    def test_scaling(self):
        self.assertEqual(calculate_physical_q(5e14, linewidth_hz=1e10)["q"], 5e4)

    def test_missing(self):
        self.assertEqual(calculate_physical_q(5e14)["status"], "UNVERIFIED")

    def test_ambiguous(self):
        self.assertEqual(calculate_physical_q(5e14, 5e9, 1e-9)["status"], "INVALID")

    def test_invalid(self):
        for nu, width in ((0, 1), (1, 0), (1, -1), (True, 1),
                          (float("nan"), 1), (1, float("inf")), (1e308, 1e-308)):
            with self.subTest(nu=nu, width=width):
                self.assertEqual(calculate_physical_q(nu, linewidth_hz=width)["status"], "INVALID")

    def test_scope(self):
        r = calculate_physical_q(5e14, linewidth_hz=5e9)
        self.assertEqual(r["status"], "DERIVED")
        self.assertIs(r["experimental_validation"], False)
