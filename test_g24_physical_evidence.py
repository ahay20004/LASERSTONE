import unittest
from physics_consistency_engine import audit_physical_evidence


class EvidenceAuditTests(unittest.TestCase):
    def setUp(self):
        self.p = dict(lambda_em=632.8, refractive_index=1.0,
                      cavity_length_m=.2, mirror_r1=.999, mirror_r2=.95,
                      internal_loss_m_inv=.1, gain_m_inv=.3,
                      claims_above_threshold=True)

    def check_status(self, p, status):
        result = audit_physical_evidence(p)
        self.assertEqual(result["status"], status)
        self.assertIs(result["experimental_validation"], False)

    def test_empty(self):
        self.check_status({}, "UNVERIFIED")

    def test_complete(self):
        self.check_status(self.p, "CONSISTENT")

    def test_conflict(self):
        self.check_status(dict(self.p, gain_m_inv=.1), "INCONSISTENT")

    def test_below(self):
        self.check_status(dict(self.p, gain_m_inv=.1, claims_above_threshold=False), "CONSISTENT")

    def test_missing_claim(self):
        self.check_status(dict(self.p, claims_above_threshold=None), "UNVERIFIED")

    def test_invalid_partial_claim(self):
        self.check_status({"claims_above_threshold": "yes"}, "INVALID")

    def test_invalid_partial_reflectivity(self):
        self.check_status({"mirror_r1": 2}, "INVALID")

    def test_zero_wavelength(self):
        self.check_status(dict(self.p, lambda_em=0), "INVALID")

    def test_missing_each_parameter(self):
        for key in self.p:
            with self.subTest(key=key):
                p = dict(self.p)
                del p[key]
                self.check_status(p, "UNVERIFIED")


if __name__ == "__main__":
    unittest.main()
