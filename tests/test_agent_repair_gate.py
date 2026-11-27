import unittest
from agent_repair_gate import assess_repair

class RepairGateTests(unittest.TestCase):
    def setUp(self):
        self.r = {"task_id": "AC-06", "change_ref": "commit-123",
                  "tests": [{"name": "unit", "result": "PASS", "evidence_ref": "ci-123"}],
                  "human_approval": False}

    def test_proposal_is_not_a_fix(self):
        self.r["change_ref"] = ""
        self.assertEqual(assess_repair(self.r)["status"], "PROPOSED_ONLY")

    def test_failed_test_blocks(self):
        self.r["tests"][0]["result"] = "FAIL"
        self.assertEqual(assess_repair(self.r)["status"], "TESTS_NOT_PASSED")

    def test_self_reported_pass_not_verified(self):
        self.assertEqual(assess_repair(self.r)["status"], "EVIDENCE_UNVERIFIED")

    def test_verified_evidence_still_needs_human_review(self):
        self.r["trusted_runner_verified"] = True
        result = assess_repair(self.r)
        self.assertTrue(result["ready_for_human_review"])
        self.assertFalse(result["execution_authorized"])

if __name__ == "__main__":
    unittest.main()
