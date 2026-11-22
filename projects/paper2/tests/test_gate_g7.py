"""G7 synthetic report-binding and publication-readiness tests."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("gate_g7", Path(__file__).resolve().parents[1] / "gate_g7.py")
g7 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g7)


def dossier(root):
    hashes = {}
    for gate in g7.GATES:
        path = root / gate.lower() / f"{gate.lower()}_report.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"gate": gate, "status": "PASS"}), encoding="utf-8")
        hashes[gate] = hashlib.sha256(path.read_bytes()).hexdigest()
    return {"gate_results": {k: "PASS" for k in g7.GATES},
            "gate_report_sha256": hashes,
            "editorial_checks": {k: True for k in g7.CHECKS},
            "manuscript_version": "synthetic-v1",
            "evidence_register_version": "synthetic-v1",
            "target_journal": "synthetic example journal"}


class ReadinessTests(unittest.TestCase):
    def test_complete_dossier_requires_human_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(g7.evaluate(dossier(root), root)["status"], "READY_FOR_HUMAN_REVIEW")

    def test_missing_gate_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            d = dossier(root)
            d["gate_results"]["G4"] = "NOT_RUN"
            self.assertEqual(g7.evaluate(d, root)["status"], "BLOCKED")

    def test_missing_authorship_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            d = dossier(root)
            d["editorial_checks"]["author_approval"] = False
            self.assertEqual(g7.evaluate(d, root)["status"], "BLOCKED")

    def test_missing_journal_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            d = dossier(root)
            d["target_journal"] = ""
            self.assertEqual(g7.evaluate(d, root)["status"], "BLOCKED")

    def test_empty_dossier_blocks(self):
        self.assertEqual(g7.evaluate({})["status"], "BLOCKED")

    def test_missing_report_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            d = dossier(root)
            (root / "g3" / "g3_report.json").unlink()
            self.assertEqual(g7.evaluate(d, root)["status"], "BLOCKED")

    def test_tampered_report_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            d = dossier(root)
            (root / "g4" / "g4_report.json").write_text('{"gate":"G4","status":"FAIL"}')
            self.assertEqual(g7.evaluate(d, root)["status"], "BLOCKED")

    def test_false_pass_with_matching_hash_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            d = dossier(root)
            path = root / "g4" / "g4_report.json"
            path.write_text('{"gate":"G4","status":"FAIL"}')
            d["gate_report_sha256"]["G4"] = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(g7.evaluate(d, root)["status"], "BLOCKED")

    def test_no_reports_dir_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(g7.evaluate(dossier(root))["status"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()
