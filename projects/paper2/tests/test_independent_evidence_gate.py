"""Synthetic tests for Stage 3.8 independent evidence review metadata gate."""
import importlib.util
from pathlib import Path
import unittest

p = Path(__file__).resolve().parents[1] / "independent_evidence_gate.py"
spec = importlib.util.spec_from_file_location("independent_evidence_gate", p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def record():
    return {
        "evidence_id": "synthetic-1", "source_id": None,
        "artifact_sha256": None, "submitter_id": "author-1",
        "reviewer_id": None, "review_artifact_sha256": None,
        "review_scope": None, "review_outcome": None,
        "reviewer_independence_attestation": False,
    }

def report():
    return {"theory_id": "theory-1", "version": "0.1",
            "proposal_sha256": "proposal-hash", "upstream_audit_sha256": "audit-hash",
            "evidence_input_sha256": "evidence-hash"}

class IndependentEvidenceTests(unittest.TestCase):
    def test_unverified_submission(self):
        r = mod.classify(record())
        self.assertEqual(r["status"], "SUBMITTED_UNVERIFIED")
        self.assertEqual(r["claims_authorized"], [])

    def test_documented_source_is_not_verified(self):
        d = record()
        d["source_id"] = "source-1"
        d["artifact_sha256"] = "a" * 64
        r = mod.classify(d)
        self.assertEqual(r["status"], "SOURCE_DOCUMENTED_REVIEW_NOT_VERIFIED")
        self.assertFalse(r["artifact_contents_verified"])

    def test_reported_review_not_authenticated(self):
        d = record()
        d.update(source_id="source-1", artifact_sha256="a" * 64,
                 reviewer_id="reviewer-2", review_artifact_sha256="b" * 64,
                 review_scope="synthetic only", review_outcome="SUPPORTS_WITHIN_SCOPE",
                 reviewer_independence_attestation=True)
        r = mod.classify(d)
        self.assertEqual(r["status"], "INDEPENDENT_REVIEW_REPORTED_UNAUTHENTICATED")
        self.assertFalse(r["independence_verified"])
        self.assertEqual(r["scientific_validation"], "NOT_ESTABLISHED")

    def test_self_review_rejected(self):
        d = record()
        d["reviewer_id"] = "author-1"
        with self.assertRaises(ValueError):
            mod.classify(d)

    def test_bad_sha_rejected(self):
        d = record()
        d["artifact_sha256"] = "not-a-hash"
        with self.assertRaises(ValueError):
            mod.classify(d)

    def test_unattached_review_rejected(self):
        d = record()
        d["review_outcome"] = "INCONCLUSIVE"
        with self.assertRaises(ValueError):
            mod.classify(d)

    def test_duplicate_ids_rejected(self):
        with self.assertRaises(ValueError):
            mod.bind_to_evidence_report(report(), [record(), record()])

    def test_report_binding_and_no_endorsement(self):
        r = mod.bind_to_evidence_report(report(), [record()])
        self.assertEqual(r["version"], "0.1")
        self.assertEqual(r["endorsement"], "NONE")
        self.assertEqual(r["claims_authorized"], [])

    def test_stable_review_hash(self):
        a = mod.bind_to_evidence_report(report(), [record()])
        b = mod.bind_to_evidence_report(report(), [record()])
        self.assertEqual(a["review_input_sha256"], b["review_input_sha256"])

if __name__ == "__main__":
    unittest.main()
