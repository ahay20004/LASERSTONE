"""Synthetic tests for Stage 4.0 integrated scientific validation dashboard."""
import importlib.util
from pathlib import Path
import unittest

p = Path(__file__).resolve().parents[1] / "integrated_validation_dashboard.py"
spec = importlib.util.spec_from_file_location("integrated_validation_dashboard", p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def reports():
    base = {"theory_id": "synthetic", "version": "0.1", "proposal_sha256": "proposal"}
    return {
        "unified": {**base, "audit_sha256": "audit", "checks": {"dimension": "PASS"}},
        "uncertainty": {**base, "upstream_audit_sha256": "audit",
                        "evidence_input_sha256": "evidence",
                        "comparisons": [{"status": "COMPARISON_RECORDED"}]},
        "independent_review": {**base, "evidence_input_sha256": "evidence",
                               "review_input_sha256": "review",
                               "reviews": [{"status": "INDEPENDENT_REVIEW_REPORTED_UNAUTHENTICATED"}]},
        "claims": {**base, "evidence_input_sha256": "evidence",
                   "review_input_sha256": "review", "claims_input_sha256": "claims",
                   "claim_assessments": [{"claim_id": "synthetic-claim"}],
                   "publication_readiness": "NOT_ESTABLISHED", "claims_authorized": []},
    }

class DashboardTests(unittest.TestCase):
    def test_all_stages_no_auto_endorsement(self):
        r = mod.build(reports())
        self.assertEqual(r["scientific_validity"], "NOT_ESTABLISHED")
        self.assertEqual(r["claims_authorized"], [])
        self.assertEqual(r["gaps"], [])

    def test_missing_stages_are_not_run(self):
        r = mod.build({"unified": reports()["unified"]})
        self.assertEqual(r["stages"]["claims"], "NOT_RUN")
        self.assertIn("claims:NOT_RUN", r["gaps"])

    def test_nonpass_check_flagged(self):
        x = reports()
        x["unified"]["checks"]["dimension"] = "NOT_RUN"
        self.assertIn("unified:INCOMPLETE_OR_NONPASS_CHECKS", mod.build(x)["gaps"])

    def test_cross_theory_rejected(self):
        x = reports()
        x["claims"]["theory_id"] = "other"
        with self.assertRaises(ValueError):
            mod.build(x)

    def test_broken_audit_chain_rejected(self):
        x = reports()
        x["uncertainty"]["upstream_audit_sha256"] = "wrong"
        with self.assertRaises(ValueError):
            mod.build(x)

    def test_broken_review_chain_rejected(self):
        x = reports()
        x["claims"]["review_input_sha256"] = "wrong"
        with self.assertRaises(ValueError):
            mod.build(x)

    def test_publication_promotion_rejected(self):
        x = reports()
        x["claims"]["publication_readiness"] = "READY"
        with self.assertRaises(ValueError):
            mod.build(x)

    def test_deterministic_input_hash(self):
        self.assertEqual(mod.build(reports())["input_reports_sha256"],
                         mod.build(reports())["input_reports_sha256"])

    def test_empty_rejected(self):
        with self.assertRaises(ValueError):
            mod.build({})

if __name__ == "__main__":
    unittest.main()
