import unittest
from scientific_trace_engine import generate_evidence_trace

class ScientificTraceTests(unittest.TestCase):
    def test_empty(self):
        r = generate_evidence_trace({})
        self.assertEqual(r["physical_audit"]["status"], "UNVERIFIED")
        self.assertEqual(r["prototype_decision"], "HOLD")

    def test_high_score(self):
        r = generate_evidence_trace({"lri_score": 100})
        self.assertEqual(r["legacy_screening_score"], 100)
        self.assertEqual(r["prototype_decision"], "HOLD")
        self.assertTrue(r["screening_only"])

    def test_model_agreement(self):
        p = dict(lambda_em=632.8, refractive_index=1, cavity_length_m=.2,
                 mirror_r1=.999, mirror_r2=.95, internal_loss_m_inv=.1,
                 gain_m_inv=.3, claims_above_threshold=True)
        r = generate_evidence_trace(p)
        self.assertEqual(r["physical_audit"]["status"], "CONSISTENT")
        self.assertEqual(r["prototype_decision"], "HOLD")
        self.assertIs(r["experimental_validation"], False)

    def test_invalid(self):
        r = generate_evidence_trace({"mirror_r1": 2, "lri_score": 100})
        self.assertEqual(r["physical_audit"]["status"], "INVALID")
        self.assertEqual(r["claims_authorized"], [])

    def test_self_declared_approval(self):
        r = generate_evidence_trace({"experimental_validation": True,
                                     "source_authentication": "VERIFIED",
                                     "prototype_decision": "GO"})
        self.assertEqual(r["source_authentication"], "NOT_VERIFIED")
        self.assertEqual(r["prototype_decision"], "HOLD")
        self.assertIs(r["experimental_validation"], False)
