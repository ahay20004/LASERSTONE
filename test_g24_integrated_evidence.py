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
                      gain_m_inv=.3, quantum_yield=.6, lifetime_s=4e-9, resonance_frequency_hz=5e14, linewidth_hz=5e9)
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

    def test_conditions_mismatch(self):
        records = {"quantum_yield":record("quantum_yield",.6),
                   "lifetime_s":record("lifetime_s",4e-9)}
        records["lifetime_s"]["conditions_id"] = "different"
        r = generate_integrated_evidence_decision(records, fluorescence_correlation=0)
        self.assertEqual(r["next_action"], "RECONCILE_CONDITIONS")
        self.assertEqual(r["fluorescence"]["status"], "UNVERIFIED")
        self.assertEqual(r["fluorescence_uncertainty"]["status"], "UNVERIFIED")

    def test_integrated_uncertainty(self):
        records = {"quantum_yield":record("quantum_yield",.6),
                   "lifetime_s":record("lifetime_s",4e-9)}
        records["lifetime_s"]["standard_uncertainty"] = .2e-9
        r = generate_integrated_evidence_decision(records, fluorescence_correlation=0)
        self.assertEqual(r["fluorescence_uncertainty"]["status"], "DERIVED")
        self.assertEqual(r["decision"], "HOLD")

    def test_threshold_q_uncertainty(self):
        values = dict(lambda_em=632.8, refractive_index=1, cavity_length_m=.2,
                      mirror_r1=.999, mirror_r2=.95, internal_loss_m_inv=.1,
                      gain_m_inv=.3, resonance_frequency_hz=5e14, linewidth_hz=5e9)
        r = generate_integrated_evidence_decision({k:record(k,v) for k,v in values.items()},
            True, threshold_independent=True, q_correlation=0)
        self.assertEqual(r["threshold_uncertainty"]["status"], "DERIVED")
        self.assertEqual(r["q_uncertainty"]["status"], "DERIVED")
        self.assertEqual(r["decision"], "HOLD")

    def test_fluorescence_not_resonance(self):
        r = generate_integrated_evidence_decision({
            "lambda_em":record("lambda_em",632.8),
            "linewidth_hz":record("linewidth_hz",5e9)})
        self.assertEqual(r["physical_q"]["status"],"UNVERIFIED")

    def test_energy_decay_q(self):
        r = generate_integrated_evidence_decision({
            "resonance_frequency_hz":record("resonance_frequency_hz",5e14),
            "energy_lifetime_s":record("energy_lifetime_s",1e-10)})
        self.assertEqual(r["physical_q"]["status"],"DERIVED")
        self.assertAlmostEqual(r["physical_q"]["q"],314159.2653589793)

    def test_integrated_correlated_margin(self):
        values=dict(lambda_em=632.8,refractive_index=1,cavity_length_m=.2,
                    mirror_r1=.999,mirror_r2=.95,internal_loss_m_inv=.1,gain_m_inv=.3)
        records={k:record(k,v) for k,v in values.items()}
        keys=("internal_loss_m_inv","mirror_r1","mirror_r2","cavity_length_m")
        all_keys=keys+("gain_m_inv",)
        c={k:{j:float(k==j) for j in all_keys} for k in all_keys}
        c["gain_m_inv"]["internal_loss_m_inv"]=c["internal_loss_m_inv"]["gain_m_inv"]=1
        sub={k:{j:c[k][j] for j in keys} for k in keys}
        r=generate_integrated_evidence_decision(records,threshold_correlation=sub,gain_correlation=c)
        self.assertEqual(r["threshold_uncertainty"]["status"],"DERIVED")
        self.assertEqual(r["gain_margin_uncertainty"]["status"],"DERIVED")
        self.assertEqual(r["decision"],"HOLD")
        self.assertFalse(r["prototype_authorized"])
        self.assertEqual(r["source_authentication"],"NOT_VERIFIED")
        c["gain_m_inv"]["internal_loss_m_inv"]=2
        r=generate_integrated_evidence_decision(records,threshold_correlation=sub,gain_correlation=c)
        self.assertEqual(r["next_action"],"CORRECT_INPUTS")
