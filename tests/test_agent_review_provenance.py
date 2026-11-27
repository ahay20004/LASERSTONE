import unittest
from agent_review_provenance import assess_submission, canonical_digest

class ProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.submission = {"reviewer": "physics", "task_id": "AC-04", "position": "revise",
                           "reason": "Needs independent measurements", "evidence": ["E-01"],
                           "run_id": "local-run-01"}
        self.payload = {k: v for k, v in self.submission.items() if k != "run_id"}

    def test_self_report_is_not_trusted(self):
        self.assertEqual(assess_submission(self.submission)["status"], "UNVERIFIED")

    def test_receipt_linked_not_identity_verified(self):
        trusted = {"local-run-01": {"reviewer": "physics", "task_id": "AC-04",
                                    "payload_sha256": canonical_digest(self.payload)}}
        result = assess_submission(self.submission, trusted)
        self.assertEqual(result["status"], "RUN_LINKED")
        self.assertFalse(result["agent_identity_independently_verified"])
        self.assertFalse(result["scientific_validity_verified"])

    def test_tampered_review_fails(self):
        trusted = {"local-run-01": {"reviewer": "physics", "task_id": "AC-04",
                                    "payload_sha256": canonical_digest(self.payload)}}
        self.submission["reason"] = "Changed"
        self.assertEqual(assess_submission(self.submission, trusted)["status"], "UNVERIFIED")

if __name__ == "__main__":
    unittest.main()
