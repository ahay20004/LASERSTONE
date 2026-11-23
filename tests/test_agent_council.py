import pathlib
import tempfile
import unittest

from agent_council import council, decide, discover, review

class CouncilTests(unittest.TestCase):
    def task(self):
        return {"id": "AC-01", "summary": "Physics and numerical stability audit",
                "specialties": ["physics", "numerical"], "guests": ["wien2k_guest"]}

    def test_discovery_does_not_claim_runtime(self):
        with tempfile.TemporaryDirectory() as d:
            result = discover(pathlib.Path(d))
            self.assertFalse(result["active_agents_verified"])

    def test_requires_all_specialists_and_guest(self):
        c = council(self.task())
        review(c, {"reviewer": "physics", "position": "approve", "reason": "equations reviewed"})
        review(c, {"reviewer": "numerical", "position": "revise", "reason": "convergence missing"})
        self.assertEqual(c["review_status"], "AWAITING_INDEPENDENT_REVIEWS")
        with self.assertRaises(ValueError):
            decide(c, "approve", "human review")
        review(c, {"reviewer": "wien2k_guest", "position": "reject", "reason": "DFT not audited"})
        self.assertEqual(c["recommendation"], "DISAGREEMENT")
        decide(c, "revise", "request reproducible DFT evidence")
        self.assertFalse(c["execution_authorized"])

    def test_duplicate_and_unassigned_rejected(self):
        c = council(self.task())
        r = {"reviewer": "physics", "position": "approve", "reason": "verified"}
        review(c, r)
        with self.assertRaises(ValueError):
            review(c, r)
        with self.assertRaises(ValueError):
            review(c, {"reviewer": "other", "position": "approve", "reason": "ok"})

    def test_unknown_role_rejected(self):
        with self.assertRaises(ValueError):
            council({"id": "x", "summary": "x", "specialties": ["fictional"]})

if __name__ == "__main__":
    unittest.main()
