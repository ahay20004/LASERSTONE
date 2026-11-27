import unittest
from scientific_confidence_engine import assess_evidence_confidence

class EvidenceConfidenceTests(unittest.TestCase):
    def test_empty(self):
        r = assess_evidence_confidence({})
        self.assertEqual(r["scientific_confidence"], "NOT_ESTABLISHED")
        self.assertIsNone(r["confidence_probability"])

    def test_scores_not_probability(self):
        r = assess_evidence_confidence(dict(lri_score=100, research_novelty_score=100,
                                            patent_potential_score=100))
        self.assertIsNone(r["confidence_probability"])
        self.assertEqual(r["prototype_decision"], "HOLD")

    def test_model_agreement(self):
        r = assess_evidence_confidence(dict(lambda_em=632.8, refractive_index=1,
            cavity_length_m=.2, mirror_r1=.999, mirror_r2=.95,
            internal_loss_m_inv=.1, gain_m_inv=.3, claims_above_threshold=True))
        self.assertEqual(r["model_consistency"], "CONSISTENT")
        self.assertEqual(r["scientific_confidence"], "NOT_ESTABLISHED")

    def test_invalid(self):
        r = assess_evidence_confidence({"mirror_r1": 2})
        self.assertEqual(r["model_consistency"], "INVALID")
        self.assertEqual(r["claims_authorized"], [])

    def test_self_declared(self):
        r = assess_evidence_confidence({"experimental_validation": True,
            "source_authentication": "VERIFIED", "confidence_probability": 1})
        self.assertIsNone(r["confidence_probability"])
        self.assertIs(r["experimental_validation"], False)
        self.assertEqual(r["source_authentication"], "NOT_VERIFIED")
