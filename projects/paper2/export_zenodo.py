"""Fail-closed Paper II Zenodo export. Standard library + existing G4/numpy.
Usage: python projects/paper2/export_zenodo.py --manifest /absolute/path/manifest.json --out /absolute/path/output
Manifest: {"inputs":[{"id":"NCHL001","path":"...","sha256":"64 hex","source_url":"...","redistribution_allowed":true},{"id":"NCHL002",...}],"analysis_files":["/path/to/validated/script.py"],"evidence_register":"/path/to/evidence_register.csv","g4_report":"/path/to/g4_report.json","rights_reviewed":true}
No output ZIP unless all gates pass. Inputs are never fetched or substituted.
"""
import argparse
import csv
import hashlib
import json
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from gate_g4 import load, compute

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def fail(message):
    raise ValueError(message)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    manifest_path = Path(args.manifest).resolve()
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    report_path = out / "zenodo_export_status.json"
    # Never leave a previously generated ZIP looking valid after a blocked rerun.
    previous_zip = out / "PaperII_Zenodo_VERIFIED.zip"
    if previous_zip.exists():
        previous_zip.unlink()
    report = {"status": "BLOCKED", "package": None, "checks": {}}
    try:
        m = json.loads(manifest_path.read_text(encoding="utf-8"))
        if m.get("rights_reviewed") is not True:
            fail("Rights review not explicitly approved")
        inputs = m.get("inputs", [])
        if len(inputs) != 2 or {i.get("id") for i in inputs} != {"NCHL001", "NCHL002"}:
            fail("Exactly original NCHL001 and NCHL002 are required")
        source_files = {}
        for i in inputs:
            p = Path(i["path"]).resolve()
            if not p.is_file():
                fail("Missing original input: " + str(p))
            if not re.fullmatch(r"[a-fA-F0-9]{64}", str(i.get("sha256", ""))):
                fail("Missing valid expected SHA-256 for " + i["id"])
            if digest(p).lower() != i["sha256"].lower():
                fail("Source-byte SHA-256 mismatch: " + i["id"])
            if i.get("redistribution_allowed") is not True or not i.get("source_url"):
                fail("Source URL and explicit redistribution permission required: " + i["id"])
            source_files[i["id"]] = p
        report["checks"]["source_bytes_and_rights"] = "PASS"
        evidence = Path(m["evidence_register"]).resolve()
        if not evidence.is_file() or not evidence.read_text(encoding="utf-8").strip():
            fail("Evidence register missing or empty")
        with evidence.open(encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
        if not rows:
            fail("Evidence register has no records")
        evtext = evidence.read_text(encoding="utf-8-sig")
        for i in inputs:
            if i["sha256"].lower() not in evtext.lower() or i["id"] not in evtext:
                fail("Evidence register lacks source ID and hash: " + i["id"])
        report["checks"]["evidence_register"] = "PASS"
        code_files = [Path(p).resolve() for p in m.get("analysis_files", [])]
        if not code_files or not all(p.is_file() for p in code_files):
            fail("Runnable analysis source must be supplied")
        g4 = Path(m["g4_report"]).resolve()
        if not g4.is_file():
            fail("Original G4 report missing")
        previous = json.loads(g4.read_text(encoding="utf-8"))
        if previous.get("status") != "PASS":
            fail("Original G4 report is not PASS")
        expected = previous.get("input_sha256", {})
        if {expected.get("a"), expected.get("b")} != {digest(source_files["NCHL001"]), digest(source_files["NCHL002"])}:
            fail("G4 report is not tied to exact original source bytes")
        a, _ = load(source_files["NCHL001"])
        b, _ = load(source_files["NCHL002"])
        current = compute(a, b)
        if current["status"] != "PASS":
            fail("Recomputed G4 robustness check failed")
        for key in ("observed", "overlap_nm", "original_sampled_peaks"):
            if current[key] != previous.get(key):
                fail("Original G4 report differs from recomputation: " + key)
        report["checks"]["g4_recomputed"] = "PASS"
        # Manuscript-consistency gate: values must be transcribed from the
        # submitted master, not inferred from synthetic tests or fitted later.
        reference_name = m.get("manuscript_reference")
        if not reference_name:
            fail("Submitted-manuscript reference JSON is required")
        reference_path = Path(reference_name).resolve()
        if not reference_path.is_file():
            fail("Submitted-manuscript reference JSON not found")
        reference = json.loads(reference_path.read_text(encoding="utf-8"))
        if reference.get("manuscript_sha256") != "c0d23bb499b38b80accbe86e744d1c9204ecf2a8b795b5cb6632ab93355e3f08":
            fail("Manuscript reference is not tied to the user-confirmed submitted DOCX")
        if reference.get("source") != "submitted_methodsx_master":
            fail("Reference must explicitly identify submitted MethodsX master")
        if reference.get("input_sha256") != {k: digest(v) for k, v in source_files.items()}:
            fail("Manuscript reference not tied to exact source bytes")
        metrics = reference.get("metrics")
        if not isinstance(metrics, dict) or set(metrics) != {"nrmse_minmax", "pearson_r", "peak_a_nm", "peak_b_nm"}:
            fail("Manuscript reference must specify all four canonical metrics")
        ref_run = next(r for r in current["runs"] if r["step_nm"] == 1.0)
        actual = {
            "nrmse_minmax": ref_run["nrmse_minmax"],
            "pearson_r": ref_run["pearson_r"],
            "peak_a_nm": ref_run["grid_peak_a_nm"],
            "peak_b_nm": ref_run["grid_peak_b_nm"],
        }
        for name, observed in actual.items():
            entry = metrics[name]
            if not isinstance(entry, dict) or type(entry.get("decimals")) is not int or not (0 <= entry["decimals"] <= 12):
                fail("Invalid manuscript precision specification: " + name)
            try:
                published = float(entry["value"])
            except (ValueError, TypeError, KeyError):
                fail("Missing manuscript value: " + name)
            # Explicit rounding convention; no tolerance chosen after seeing results.
            from decimal import Decimal, ROUND_HALF_UP
            places = Decimal(1).scaleb(-entry["decimals"])
            rounded = float(Decimal(str(observed)).quantize(places, rounding=ROUND_HALF_UP))
            if rounded != published:
                fail("Submitted manuscript mismatch: " + name + " expected " + str(published) + " recomputed " + str(rounded))
        report["checks"]["submitted_manuscript_consistency"] = "PASS"
        # The publication gate also requires shift tests and an explicit external rights audit.
        shift = m.get("shift_test_report")
        if not shift:
            fail("Shift-test report required for +5/+10/+20/+40 nm under both boundary conventions")
        shift_path = Path(shift).resolve()
        if not shift_path.is_file():
            fail("Shift-test report not found")
        shifts = json.loads(shift_path.read_text(encoding="utf-8"))
        if shifts.get("status") != "PASS" or shifts.get("shifts_nm") != [5, 10, 20, 40] or set(shifts.get("boundary_conventions", [])) != {"constant-edge", "zero-padding"}:
            fail("Shift-test report does not attest required conventions and shifts")
        if shifts.get("input_sha256") != {k: digest(v) for k, v in source_files.items()}:
            fail("Shift tests not tied to exact original input bytes")
        report["checks"]["shift_report"] = "PASS"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "PaperII_Reproducibility"
            (root / "inputs").mkdir(parents=True)
            (root / "analysis").mkdir()
            (root / "reports").mkdir()
            for k, p in source_files.items():
                shutil.copy2(p, root / "inputs" / (k + p.suffix))
            shutil.copy2(evidence, root / "evidence_register.csv")
            for idx, p in enumerate(code_files, 1):
                shutil.copy2(p, root / "analysis" / (str(idx) + "_" + p.name))
            shutil.copy2(g4, root / "reports" / "g4_report.json")
            shutil.copy2(shift_path, root / "reports" / "shift_test_report.json")
            shutil.copy2(reference_path, root / "reports" / "submitted_manuscript_reference.json")
            (root / "manifest.json").write_text(json.dumps(m, indent=2), encoding="utf-8")
            (root / "README.txt").write_text("LASERSTONE Paper II source-verified export. Consult manifest and reports. Absorption agreement does not establish gain or lasing.\n", encoding="utf-8")
            package = out / "PaperII_Zenodo_VERIFIED.zip"
            with zipfile.ZipFile(package, "w", compression=zipfile.ZIP_DEFLATED) as z:
                for p in sorted(root.rglob("*")):
                    if p.is_file():
                        z.write(p, p.relative_to(root.parent))
        report["status"] = "PASS"
        report["package"] = str(package)
        report["package_sha256"] = digest(package)
    except Exception as exc:
        report["error"] = str(exc)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
