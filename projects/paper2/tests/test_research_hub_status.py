"""Research Hub status tests using temporary reports only."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("hub", Path(__file__).resolve().parents[1] / "research_hub_status.py")
hub = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hub)

class ResearchHubTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
    def write(self, gate, status):
        directory = self.root / gate.lower()
        directory.mkdir(exist_ok=True)
        (directory / f"{gate.lower()}_report.json").write_text(
            json.dumps({"gate": gate, "status": status}), encoding="utf-8")
    def test_missing_reports_are_not_run(self):
        r = hub.summarize(self.root)
        self.assertEqual(r["status"], "INCOMPLETE")
        self.assertTrue(all(v["status"] == "NOT_RUN" for v in r["gates"].values()))
    def test_partial_pass_is_incomplete(self):
        self.write("G3", "PASS")
        r = hub.summarize(self.root)
        self.assertEqual(r["gates"]["G3"]["status"], "PASS")
        self.assertEqual(r["status"], "INCOMPLETE")
    def test_wrong_gate_is_invalid(self):
        d = self.root / "g1"
        d.mkdir()
        (d / "g1_report.json").write_text('{"gate":"G2","status":"PASS"}')
        self.assertEqual(hub.summarize(self.root)["gates"]["G1"]["status"], "INVALID_REPORT")
    def test_all_reported_passes_still_require_review(self):
        for gate in hub.GATES:
            self.write(gate, "READY_FOR_HUMAN_REVIEW" if gate == "G7" else "PASS")
        self.assertEqual(hub.summarize(self.root)["status"], "REQUIRES_HUMAN_REVIEW")

if __name__ == "__main__":
    unittest.main()
