"""Fail-closed regression checks for the Zenodo exporter; no real spectra needed."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORTER = ROOT / "export_zenodo.py"

class ExportSafetyTests(unittest.TestCase):
    def run_export(self, manifest):
        with tempfile.TemporaryDirectory() as d:
            directory = Path(d)
            manifest_file = directory / "manifest.json"
            manifest_file.write_text(json.dumps(manifest), encoding="utf-8")
            out = directory / "out"
            result = subprocess.run(
                [sys.executable, str(EXPORTER), "--manifest", str(manifest_file), "--out", str(out)],
                capture_output=True, text=True, timeout=30
            )
            status = json.loads((out / "zenodo_export_status.json").read_text(encoding="utf-8"))
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(status["status"], "BLOCKED")
            self.assertIsNone(status["package"])
            self.assertFalse(list(out.glob("*.zip")))
            return status

    def test_missing_rights_review_blocks(self):
        status = self.run_export({"inputs": [], "rights_reviewed": False})
        self.assertIn("Rights review", status["error"])

    def test_missing_original_inputs_blocks(self):
        status = self.run_export({"inputs": [], "rights_reviewed": True})
        self.assertIn("NCHL001", status["error"])

    def test_missing_source_bytes_blocks(self):
        fake = "0" * 64
        status = self.run_export({
            "rights_reviewed": True,
            "inputs": [
                {"id": "NCHL001", "path": "/missing/NCHL001.csv", "sha256": fake,
                 "source_url": "https://example.org/a", "redistribution_allowed": True},
                {"id": "NCHL002", "path": "/missing/NCHL002.csv", "sha256": fake,
                 "source_url": "https://example.org/b", "redistribution_allowed": True},
            ],
        })
        self.assertIn("Missing original input", status["error"])

if __name__ == "__main__":
    unittest.main()
