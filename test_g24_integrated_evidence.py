import unittest
from data_validator import audit_parameter_record, PHYSICAL_PARAMETER_RULES
from final_decision_engine import generate_integrated_evidence_decision

def record(k, v):
    return dict(value=v, unit=PHYSICAL_PARAMETER_RULES[k][0],
                standard_uncertainty=0.01, source_id="synthetic",
                conditions_id="synthetic", basis="assumed")

class IntegratedEvidenceTests(unittest.TestCase):
    def test_units(self):
        r = record("lifetime_s", 4)
        r["unit"] = "ns"
        self.assertEqual(audit_parameter_record("lifetime_s", r)["status"], "INVALID")

    def test_zero(self):
        self.assertEqual(audit_parameter_record("quantum_yield",
            record("quantum_yield", 0))["status"], "RECORDED")

    def test_missing(self):
        r = record("lambda_em", 632.8)
        del r["standard_uncertainty"]
        self.assertEqual(audit_parameter_record("lambda_em", r)["status"], "UNVERIFIED")

    def test_domain(self):
        for k,v in (("mirror_r1", 1.1), ("lifetime_s", 0), ("quantum_yield", -1)):
            self.assertEqual(audit_parameter_record(k, record(k,v))["status"], "INVALID")

    def test_integrated(self):
        values = dict(lambda_em=632.8, refractive_index=1, cavity_length_m=.2,
                      mirror_r1=.999, mirror_r2=.95, internal_loss_m_inv=.1,
                      gain_m_inv=.3, quantum_yield=.6, lifetime_s=4e-9, linewidth_hz=5e9)
        r = generate_integrated_evidence_decision({k:record(k,v) for k,v in values.items()}, True)
        self.assertEqual(r["confidence"]["model_consistency"], "CONSISTENT")
        self.assertEqual(r["fluorescence"]["status"], "DERIVED")
        self.assertEqual(r["physical_q"]["status"], "DERIVED")
        self.assertEqual(r["decision"], "HOLD")
        self.assertFalse(r["uncertainty_propagated"])

    def test_invalid_optional(self):
        r = generate_integrated_evidence_decision({"quantum_yield":record("quantum_yield",2)})
        self.assertEqual(r["next_action"], "CORRECT_INPUTS")

    def test_empty(self):
        r = generate_integrated_evidence_decision({})
        self.assertEqual(r["physical_q"]["status"], "UNVERIFIED")
        self.assertEqual(r["decision"], "HOLD")
