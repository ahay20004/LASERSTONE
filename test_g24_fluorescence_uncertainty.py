import unittest
import math
from physics_evidence_engine import audit_fluorescence_uncertainty as audit

class FluorescenceUncertaintyTests(unittest.TestCase):
    def test_independent(self):
        r = audit(.6, 4e-9, .03, .2e-9, 0)
        self.assertEqual(r["status"], "DERIVED")
        self.assertTrue(math.isclose(r["radiative_standard_uncertainty_s_inv"], math.hypot(7.5e6,7.5e6)))
        self.assertTrue(math.isclose(r["nonradiative_standard_uncertainty_s_inv"], math.hypot(7.5e6,5e6)))

    def test_positive_correlation(self):
        r = audit(.6,4e-9,.03,.2e-9,1)
        self.assertLess(r["radiative_standard_uncertainty_s_inv"],1e-7)
        self.assertTrue(math.isclose(r["nonradiative_standard_uncertainty_s_inv"],12.5e6))

    def test_negative_correlation(self):
        r = audit(.6,4e-9,.03,.2e-9,-1)
        self.assertTrue(math.isclose(r["radiative_standard_uncertainty_s_inv"],15e6))
        self.assertTrue(math.isclose(r["nonradiative_standard_uncertainty_s_inv"],2.5e6))

    def test_missing_correlation(self):
        self.assertEqual(audit(.6,4e-9,.03,.2e-9)["status"],"UNVERIFIED")

    def test_invalid(self):
        for u,v,rho in [(-1,0,0),(0,-1,0),(0,0,1.1),(0,0,float("nan")),(True,0,0)]:
            self.assertEqual(audit(.6,4e-9,u,v,rho)["status"],"INVALID")

    def test_zero_uncertainty(self):
        r = audit(.6,4e-9,0,0,0)
        self.assertEqual(r["radiative_standard_uncertainty_s_inv"],0)
        self.assertEqual(r["nonradiative_standard_uncertainty_s_inv"],0)
