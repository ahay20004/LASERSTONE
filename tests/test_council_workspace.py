import json
import tempfile
from pathlib import Path
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

    def test_session_replay(self):
        w = CouncilWorkspace()
        w.convene({"id":"T1","summary":"Physics","specialties":["physics"]})
        w.submit_review({"reviewer":"physics","position":"approve","reason":"checked","evidence":["test"]})
        w.human_decision("approve","reviewed")
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "session.json"
            w.export(p)
            with self.assertRaises(FileExistsError):
                w.export(p)
            self.assertEqual(CouncilWorkspace().restore(p), w.snapshot())
            forged = json.loads(p.read_text(encoding="utf-8"))
            forged["execution_authorized"] = True
            p.write_text(json.dumps(forged), encoding="utf-8")
            empty = CouncilWorkspace()
            with self.assertRaises(ValueError):
                empty.restore(p)
            self.assertIsNone(empty.snapshot())
