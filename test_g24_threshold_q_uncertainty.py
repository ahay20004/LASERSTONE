import math
import unittest
from laser_physics_engine import audit_threshold_uncertainty, calculate_laser_physics, audit_gain_margin_uncertainty
from qfactor_engine import audit_q_uncertainty

class AccuracyTests(unittest.TestCase):
    def setUp(self):
        self.p = dict(lambda_em=632.8, refractive_index=1, cavity_length_m=.2,
                      mirror_r1=.999, mirror_r2=.95, internal_loss_m_inv=.1)
        self.u = dict(cavity_length_m=.001, mirror_r1=.0001, mirror_r2=.005,
                      internal_loss_m_inv=.01)

    def test_threshold_sensitivity(self):
        r = audit_threshold_uncertainty(self.p,self.u,True)
        self.assertEqual(r["status"],"DERIVED")
        for k,s in r["sensitivities"].items():
            h=1e-6
            p=dict(self.p); p[k]+=h
            m=dict(self.p); m[k]-=h
            fd=(calculate_laser_physics(p)["threshold_gain_m_inv"]-
                calculate_laser_physics(m)["threshold_gain_m_inv"])/(2*h)
            self.assertTrue(math.isclose(s,fd,rel_tol=1e-7))

    def test_threshold_independence(self):
        self.assertEqual(audit_threshold_uncertainty(self.p,self.u)["status"],"UNVERIFIED")

    def test_threshold_invalid(self):
        self.assertEqual(audit_threshold_uncertainty(self.p,dict(self.u,mirror_r1=-1),True)["status"],"INVALID")

    def test_q_reference(self):
        r=audit_q_uncertainty(5e14,5e9,5e12,5e7,0)
        self.assertEqual(r["status"],"DERIVED")
        self.assertTrue(math.isclose(r["standard_uncertainty"],math.sqrt(2)*1000))

    def test_q_correlated(self):
        self.assertAlmostEqual(audit_q_uncertainty(5e14,5e9,5e12,5e7,1)["standard_uncertainty"],0)

    def test_q_missing(self):
        self.assertEqual(audit_q_uncertainty(5e14,5e9,5e12,5e7)["status"],"UNVERIFIED")

    def test_q_invalid(self):
        self.assertEqual(audit_q_uncertainty(5e14,5e9,5e12,5e7,2)["status"],"INVALID")

    def test_gain_margin(self):
        p=dict(self.p,gain_m_inv=.3)
        r=audit_gain_margin_uncertainty(p,dict(self.u,gain_m_inv=.01),True)
        self.assertEqual(r["status"],"DERIVED")
        self.assertEqual(r["one_standard_uncertainty_sign"],"POSITIVE")
        self.assertTrue(math.isclose(r["standard_uncertainty_m_inv"],
            math.hypot(audit_threshold_uncertainty(self.p,self.u,True)["standard_uncertainty_m_inv"],.01)))

    def test_unresolved_margin(self):
        p=dict(self.p,gain_m_inv=calculate_laser_physics(self.p)["threshold_gain_m_inv"])
        r=audit_gain_margin_uncertainty(p,dict(self.u,gain_m_inv=.01),True)
        self.assertEqual(r["one_standard_uncertainty_sign"],"UNRESOLVED")

    def test_correlated_threshold(self):
        c={k:{j:float(k==j) for j in self.u} for k in self.u}
        c["mirror_r1"]["mirror_r2"]=c["mirror_r2"]["mirror_r1"]=.7
        r=audit_threshold_uncertainty(self.p,self.u,correlation=c)
        self.assertEqual(r["status"],"DERIVED")
        v={k:r["sensitivities"][k]*self.u[k] for k in self.u}
        expected=math.sqrt(sum(v[k]*c[k][j]*v[j] for k in v for j in v))
        self.assertAlmostEqual(r["standard_uncertainty_m_inv"],expected)
        c["mirror_r1"]["mirror_r2"]=2
        self.assertEqual(audit_threshold_uncertainty(self.p,self.u,correlation=c)["status"],"INVALID")

    def test_correlated_gain(self):
        p=dict(self.p,gain_m_inv=.3)
        u=dict(self.u,gain_m_inv=.01)
        c={k:{j:float(k==j) for j in u} for k in u}
        c["gain_m_inv"]["internal_loss_m_inv"]=c["internal_loss_m_inv"]["gain_m_inv"]=1
        r=audit_gain_margin_uncertainty(p,u,correlation=c)
        self.assertEqual(r["status"],"DERIVED")
        t=audit_threshold_uncertainty(p,self.u,True)
        expected=math.sqrt(sum((t["sensitivities"][k]*self.u[k])**2 for k in self.u if k!="internal_loss_m_inv"))
        self.assertAlmostEqual(r["standard_uncertainty_m_inv"],expected)
        self.assertEqual(audit_gain_margin_uncertainty(p,u,True,correlation=c)["status"],"INVALID")
