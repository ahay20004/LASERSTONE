"""G1 integrity tests with temporary synthetic files only."""
import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("gate_g1", Path(__file__).resolve().parents[1] / "gate_g1.py")
g1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g1)

class IntegrityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.file = self.root / "synthetic.txt"
        self.file.write_text("synthetic spectrum", encoding="utf-8")
        self.entry = {"path": "synthetic.txt", "source_id": "synthetic",
                      "rights_status": "authorized",
                      "sha256": hashlib.sha256(self.file.read_bytes()).hexdigest()}
    def test_matching_hash_passes(self):
        self.assertEqual(g1.verify({"files": [self.entry]}, self.root)["status"], "PASS")
    def test_modified_content_fails(self):
        self.file.write_text("modified", encoding="utf-8")
        self.assertEqual(g1.verify({"files": [self.entry]}, self.root)["status"], "FAIL")
    def test_traversal_fails(self):
        entry = dict(self.entry, path="../outside.txt")
        self.assertEqual(g1.verify({"files": [entry]}, self.root)["status"], "FAIL")
    def test_missing_source_fails(self):
        entry = dict(self.entry, source_id="")
        self.assertEqual(g1.verify({"files": [entry]}, self.root)["status"], "FAIL")
    def test_missing_file_fails(self):
        entry = dict(self.entry, path="missing.txt")
        self.assertEqual(g1.verify({"files": [entry]}, self.root)["status"], "FAIL")

if __name__ == "__main__":
    unittest.main()
