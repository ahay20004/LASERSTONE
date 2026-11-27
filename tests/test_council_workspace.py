import unittest
from council_workspace import CouncilWorkspace

class WorkspaceTests(unittest.TestCase):
    def test_lifecycle(self):
        w = CouncilWorkspace()
        s = w.convene({"id":"T1","summary":"Physics review","specialties":["physics"]})
        s["execution_authorized"] = True
        self.assertFalse(w.snapshot()["execution_authorized"])
        with self.assertRaises(ValueError):
            w.human_decision("approve","premature")
        w.submit_review({"reviewer":"physics","position":"approve","reason":"checked","evidence":["test"]})
        s = w.human_decision("approve","review recorded")
        self.assertEqual(s["human_decision"],"APPROVE")
        self.assertFalse(s["execution_authorized"])
        with self.assertRaises(ValueError):
            w.convene({"id":"T2","summary":"new"})

    def test_no_task(self):
        w = CouncilWorkspace()
        with self.assertRaises(ValueError):
            w.submit_review({})
        with self.assertRaises(ValueError):
            w.human_decision("approve","none")
