"""G5 reproducibility: compare two independently generated JSON metric reports.

A PASS establishes agreement of selected computational metrics, not independent
experimental replication or physical accuracy.
"""
import argparse
import json
import math
from pathlib import Path

METRICS = ("normalized_rmse", "normalized_pearson_r",
           "peak_a_overlap_nm", "peak_b_overlap_nm", "delta_peak_overlap_nm")
IDENTITY = ("sha256_a", "sha256_b", "grid_step_nm", "overlap_nm")

def evaluate(first, second, abs_tol=1e-10):
    if not isinstance(first, dict) or not isinstance(second, dict):
        raise ValueError("Reports must be JSON objects")
    if not math.isfinite(abs_tol) or abs_tol < 0:
        raise ValueError("abs_tol must be finite and nonnegative")
    errors = []
    for field in IDENTITY:
        if field not in first or field not in second:
            errors.append(f"{field}: missing from one or both reports")
        elif first[field] != second[field]:
            errors.append(f"{field}: input or analysis identity differs")
    for field in METRICS:
        a, b = first.get(field), second.get(field)
        if isinstance(a, bool) or isinstance(b, bool) or not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            errors.append(f"{field}: missing or nonnumeric")
        elif not math.isfinite(a) or not math.isfinite(b) or not math.isclose(a, b, rel_tol=0, abs_tol=abs_tol):
            errors.append(f"{field}: metric differs beyond tolerance")
    return {
        "gate": "G5", "version": "1.0",
        "status": "PASS" if not errors else "FAIL",
        "absolute_tolerance": abs_tol,
        "checked_metrics": list(METRICS),
        "checked_identity": list(IDENTITY),
        "errors": errors,
        "caveat": "Computational reproducibility does not prove independent experimental replication or scientific validity."
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--first", required=True)
    parser.add_argument("--second", required=True)
    parser.add_argument("--abs-tol", type=float, default=1e-10)
    parser.add_argument("--out", default="output/g5_gate")
    args = parser.parse_args()
    first = json.loads(Path(args.first).read_text(encoding="utf-8"))
    second = json.loads(Path(args.second).read_text(encoding="utf-8"))
    result = evaluate(first, second, args.abs_tol)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "g5_report.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["status"] == "PASS" else 1)

if __name__ == "__main__":
    main()
