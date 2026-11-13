"""End-to-end synthetic smoke test for Paper II gate CLIs.

Uses only generated test spectra. It must NOT be interpreted as validation of
original experimental datasets or manuscript readiness.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

class EndToEndSmokeTests(unittest.TestCase):
    def test_synthetic_gate_pipeline_and_release_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            reports = root / "reports"
            x = np.arange(350., 711., 2.)
            y = 0.1 + np.exp(-((x - 430.) / 25.) ** 2)
            a = root / "a.txt"
            b = root / "b.txt"
            np.savetxt(a, np.column_stack((x, y)))
            np.savetxt(b, np.column_stack((x, y)))
            def run(script, *args, success=True):
                result = subprocess.run(
                    [sys.executable, str(ROOT / script), *map(str, args)],
                    capture_output=True, text=True, check=False)
                self.assertEqual(result.returncode, 0 if success else 1,
                                 f"{script}: {result.stdout}\n{result.stderr}")
            manifest = {"files": [
                {"path": name, "sha256": hashlib.sha256((root / name).read_bytes()).hexdigest(),
                 "source_id": f"synthetic-{name}", "rights_status": "authorized"}
                for name in ("a.txt", "b.txt")]}
            manifest_path = root / "manifest.json"
            manifest_path.write_text(json.dumps(manifest))
            run("gate_g1.py", "--manifest", manifest_path, "--root", root, "--out", reports / "g1")
            run("gate_g2.py", "--a", a, "--b", b, "--out", reports / "g2")
            run("gate_g3.py", "--evidence", "absorption", "--out", reports / "g3")
            run("gate_g4.py", "--a", a, "--b", b, "--out", reports / "g4")
            metric = {
                "sha256_a": manifest["files"][0]["sha256"],
                "sha256_b": manifest["files"][1]["sha256"],
                "grid_step_nm": 1.0, "overlap_nm": [350., 710.],
                "normalized_rmse": 0.0, "normalized_pearson_r": 1.0,
                "peak_a_overlap_nm": 430., "peak_b_overlap_nm": 430.,
                "delta_peak_overlap_nm": 0.0}
            metric_path = root / "metric.json"
            metric_path.write_text(json.dumps(metric))
            run("gate_g5.py", "--first", metric_path, "--second", metric_path,
                "--out", reports / "g5")
            register = [{
                "claim_id": "SYN-1", "claim_text": "Synthetic shapes compared",
                "evidence_type": "derived", "source_id": "synthetic-a.txt",
                "source_sha256": manifest["files"][0]["sha256"],
                "method": "minmax", "parameters": {"step_nm": 1.0},
                "conditions": {"synthetic": True},
                "result": {"nrmse": 0.0}, "limitations": "Not experimental evidence",
                "manuscript_location": "test-only"}]
            register_path = root / "register.json"
            register_path.write_text(json.dumps(register))
            run("gate_g6.py", "--register", register_path, "--out", reports / "g6")
            # The release gate must block when authorship/editorial confirmations
            # are absent, even if synthetic G1-G6 reports have passed.
            dossier = {"gate_results": {f"G{i}": "PASS" for i in range(1, 7)},
                       "editorial_checks": {}, "manuscript_version": "synthetic",
                       "evidence_register_version": "synthetic"}
            dossier_path = root / "dossier.json"
            dossier_path.write_text(json.dumps(dossier))
            run("gate_g7.py", "--dossier", dossier_path, "--out", reports / "g7",
                success=False)
            run("research_hub_status.py", "--reports", reports,
                "--out", root / "hub.json")
            hub = json.loads((root / "hub.json").read_text())
            self.assertEqual(hub["status"], "INCOMPLETE")
            self.assertEqual(hub["gates"]["G7"]["status"], "FAIL")
            for i in range(1, 7):
                self.assertEqual(hub["gates"][f"G{i}"]["status"], "PASS")

if __name__ == "__main__":
    unittest.main()
