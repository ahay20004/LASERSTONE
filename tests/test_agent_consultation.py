import unittest
from agent_council import council, review, decide
from agent_consultation import open_consultation, respond

class ConsultationTests(unittest.TestCase):
    def setUp(self):
        self.c = council({"id": "AC-03", "summary": "Laser physics audit",
                          "specialties": ["physics", "evidence"], "guests": ["guest_dft"]})
        for who, pos in [("physics", "approve"), ("evidence", "revise"), ("guest_dft", "reject")]:
            review(self.c, {"reviewer": who, "position": pos,
                            "reason": "reviewed source", "evidence": ["reference"]})

    def test_no_premature_decision(self):
        open_consultation(self.c)
        with self.assertRaises(ValueError):
            decide(self.c, "approve", "premature")
        respond(self.c, {"reviewer": "physics", "position": "revise",
                         "analysis": "Address evidence objections", "addresses": ["evidence"]})
        self.assertEqual(self.c["review_status"], "CONSULTATION_IN_PROGRESS")

    def test_guest_and_disagreement_retained(self):
        open_consultation(self.c)
        for who, pos in [("physics", "revise"), ("evidence", "revise"), ("guest_dft", "reject")]:
            respond(self.c, {"reviewer": who, "position": pos,
                             "analysis": "Independent response", "addresses": ["physics"]})
        self.assertEqual(self.c["recommendation"], "DISAGREEMENT")
        self.assertEqual(len(self.c["consultation_disagreements"]), 3)
        decide(self.c, "revise", "Human review of unresolved objections")
        self.assertFalse(self.c["execution_authorized"])

    def test_no_duplicate_response(self):
        open_consultation(self.c)
        item = {"reviewer": "physics", "position": "revise", "analysis": "Check equations"}
        respond(self.c, item)
        with self.assertRaises(ValueError):
            respond(self.c, item)

if __name__ == "__main__":
    unittest.main()
