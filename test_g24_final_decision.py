import unittest
from final_decision_engine import generate_evidence_decision

class FinalEvidenceDecisionTests(unittest.TestCase):
    def setUp(self):
        self.p = dict(lambda_em=632.8, refractive_index=1, cavity_length_m=.2,
                      mirror_r1=.999, mirror_r2=.95, internal_loss_m_inv=.1,
                      gain_m_inv=.3, claims_above_threshold=True)

    def check(self, p, action):
        r = generate_evidence_decision(p)
        self.assertEqual(r["decision"], "HOLD")
        self.assertEqual(r["next_action"], action)
        self.assertIs(r["prototype_authorized"], False)
        self.assertIs(r["publication_authorized"], False)
        self.assertEqual(r["claims_authorized"], [])

    def test_missing(self):
        self.check({}, "COMPLETE_MODEL_EVIDENCE")

    def test_invalid(self):
        self.check(dict(self.p, mirror_r1=2), "CORRECT_INPUTS")

    def test_conflict(self):
        self.check(dict(self.p, gain_m_inv=.1), "RECONCILE_MODEL_AND_CLAIM")

    def test_consistent(self):
        self.check(self.p, "VERIFY_INDEPENDENT_EVIDENCE")

    def test_scores(self):
        self.check(dict(material_score=100, lri_score=100,
                        physics_consistency_score=100), "COMPLETE_MODEL_EVIDENCE")

    def test_self_authorization(self):
        self.check(dict(self.p, prototype_authorized=True,
                        publication_authorized=True, experimental_validation=True),
                   "VERIFY_INDEPENDENT_EVIDENCE")
