import math
import unittest
from physics_evidence_engine import audit_fluorescence_decay


class FluorescenceEvidenceTests(unittest.TestCase):
    def test_reference(self):
        r = audit_fluorescence_decay(.6, 4e-9)
        self.assertEqual(r["status"], "DERIVED")
        for key, expected in (("total_rate_s_inv", 2.5e8),
                              ("radiative_rate_s_inv", 1.5e8),
                              ("nonradiative_rate_s_inv", 1e8)):
            self.assertTrue(math.isclose(r[key], expected, rel_tol=1e-12))

    def test_conservation(self):
        for phi in (0, .01, .5, .99, 1):
            r = audit_fluorescence_decay(phi, 3e-9)
            self.assertTrue(math.isclose(r["total_rate_s_inv"],
                r["radiative_rate_s_inv"] + r["nonradiative_rate_s_inv"], rel_tol=1e-12))

    def test_limits(self):
        self.assertEqual(audit_fluorescence_decay(0, 1e-9)["radiative_rate_s_inv"], 0)
        self.assertEqual(audit_fluorescence_decay(1, 1e-9)["nonradiative_rate_s_inv"], 0)

    def test_missing(self):
        for phi, tau in ((None, 1e-9), (.5, None)):
            self.assertEqual(audit_fluorescence_decay(phi, tau)["status"], "UNVERIFIED")

    def test_invalid(self):
        for phi, tau in ((-1, 1), (1.1, 1), (.5, 0), (.5, -1),
                         (float("nan"), 1), (.5, float("inf")), (True, 1),
                         (.5, True), (.5, 5e-324)):
            with self.subTest(phi=phi, tau=tau):
                self.assertEqual(audit_fluorescence_decay(phi, tau)["status"], "INVALID")

    def test_no_gain_claim(self):
        r = audit_fluorescence_decay(1, 1e-9)
        self.assertIs(r["gain_verified"], False)
        self.assertIs(r["experimental_validation"], False)
