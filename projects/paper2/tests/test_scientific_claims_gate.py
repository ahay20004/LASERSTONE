"""Synthetic regression tests for Stage 3.9 claims gate."""
import importlib.util
from pathlib import Path
import unittest

p = Path(__file__).resolve().parents[1] / "scientific_claims_gate.py"
spec = importlib.util.spec_from_file_location("scientific_claims_gate", p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def report(status="SUBMITTED_UNVERIFIED"):
    return {"theory_id": "synthetic-theory", "version": "0.1",
            "proposal_sha256": "proposal-hash", "evidence_input_sha256": "evidence-hash",
            "review_input_sha256": "review-hash",
            "reviews": [{"evidence_id": "ev-1", "status": status}]}


def claim():
    return {"claim_id": "claim-1", "claim_text": "Synthetic hypothesis",
            "claim_type": "THEORETICAL", "evidence_ids": ["ev-1"],
            "equation_ids": ["eq-1"], "conditions_ids": ["cond-1"],
            "limitations": "Synthetic only", "novelty_reference_ids": ["ref-1"]}


class ClaimsTests(unittest.TestCase):
    def test_no_auto_publication(self):
        result = mod.assess(report(), [claim()])
        self.assertEqual(result["publication_readiness"], "NOT_ESTABLISHED")
        self.assertEqual(result["claims_authorized"], [])

    def test_incomplete_review_blocked(self):
        r = mod.assess(report(), [claim()])["claim_assessments"][0]
        self.assertIn("INCOMPLETE_REVIEW_METADATA", r["blockers"])

    def test_reported_review_still_unverified(self):
        r = mod.assess(report("INDEPENDENT_REVIEW_REPORTED_UNAUTHENTICATED"),
                       [claim()])["claim_assessments"][0]
        self.assertIn("INDEPENDENT_AUTHENTICATION_NOT_ESTABLISHED", r["blockers"])
        self.assertEqual(r["claims_authorized"], [])

    def test_unknown_evidence_blocked(self):
        c = claim()
        c["evidence_ids"] = ["ev-missing"]
        r = mod.assess(report(), [c])["claim_assessments"][0]
        self.assertEqual(r["unknown_evidence_ids"], ["ev-missing"])

    def test_duplicate_claim_rejected(self):
        with self.assertRaises(ValueError):
            mod.assess(report(), [claim(), claim()])

    def test_missing_limitations_rejected(self):
        c = claim()
        c["limitations"] = ""
        with self.assertRaises(ValueError):
            mod.assess(report(), [c])

    def test_missing_prior_art_rejected(self):
        c = claim()
        c["novelty_reference_ids"] = []
        with self.assertRaises(ValueError):
            mod.assess(report(), [c])

    def test_deterministic_hash(self):
        self.assertEqual(mod.assess(report(), [claim()])["claims_input_sha256"],
                         mod.assess(report(), [claim()])["claims_input_sha256"])

    def test_missing_report_binding_rejected(self):
        r = report()
        del r["proposal_sha256"]
        with self.assertRaises(ValueError):
            mod.assess(r, [claim()])

if __name__ == "__main__":
    unittest.main()
