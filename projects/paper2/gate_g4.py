"""LASERSTONE Paper II: G4 numerical robustness gate.

Shape-only comparison. No optical gain or measurement uncertainty inferred.
Usage: python projects/paper2/gate_g4.py --a PATH --b PATH --out DIR
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import numpy as np

STEPS = (0.5, 1.0, 2.0)
THRESHOLDS = {
    "interpolation_nrmse_relative_range": 0.02,
    "interpolation_pearson_absolute_range": 0.0001,
    "normalization_nrmse_relative_change": 0.02,
}

def load(path):
    raw = Path(path).read_bytes()
    rows = []
    for line in raw.decode("utf-8-sig").splitlines():
        s = line.strip()
        if not s or s.startswith(("#", ";")):
            continue
        fields = s.replace(";", ",").split(",") if "," in s or ";" in s else s.split()
        if len(fields) < 2:
            continue
        try:
            x, y = float(fields[0]), float(fields[1])
        except ValueError:
            continue  # Header; input row auditing is separately required by G1/G2.
        if not (np.isfinite(x) and np.isfinite(y)):
            raise ValueError(f"Non-finite numeric value in {path}")
        rows.append((x, y))
    arr = np.asarray(rows, dtype=float).reshape(-1, 2)
    if len(arr) < 5:
        raise ValueError(f"Too few data pairs: {path}")
    arr = arr[np.argsort(arr[:, 0])]
    if np.any(np.diff(arr[:, 0]) <= 0) or np.any(arr[:, 0] <= 0):
        raise ValueError(f"Invalid wavelength coordinates: {path}")
    if np.ptp(arr[:, 1]) <= 0:
        raise ValueError(f"Constant signal: {path}")
    return arr, hashlib.sha256(raw).hexdigest()

def compute(a, b):
    lo = max(a[0, 0], b[0, 0])
    hi = min(a[-1, 0], b[-1, 0])
    if hi - lo < 10:
        raise ValueError("Insufficient spectral overlap")
    runs = []
    for step in STEPS:
        grid = np.arange(lo, hi + 1e-10, step)
        if len(grid) < 6:
            raise ValueError("Insufficient interpolation grid")
        va = np.interp(grid, a[:, 0], a[:, 1])
        vb = np.interp(grid, b[:, 0], b[:, 1])
        if np.ptp(va) <= 0 or np.ptp(vb) <= 0:
            raise ValueError("Constant spectrum on overlap")
        if va.max() <= 0 or vb.max() <= 0:
            raise ValueError("Peak normalization requires positive maxima")
        na = (va - va.min()) / np.ptp(va)
        nb = (vb - vb.min()) / np.ptp(vb)
        pa, pb = va / va.max(), vb / vb.max()
        runs.append({
            "step_nm": step,
            "nrmse_minmax": float(np.sqrt(np.mean((na - nb)**2))),
            "nrmse_peak": float(np.sqrt(np.mean((pa - pb)**2))),
            "pearson_r": float(np.corrcoef(na, nb)[0, 1]),
            "grid_peak_a_nm": float(grid[np.argmax(va)]),
            "grid_peak_b_nm": float(grid[np.argmax(vb)]),
        })
    ref = runs[1]
    vals = [r["nrmse_minmax"] for r in runs]
    correlations = [r["pearson_r"] for r in runs]
    if ref["nrmse_minmax"] == 0:
        nrmse_range = 0.0 if max(vals) == 0 else float("inf")
        norm_change = 0.0 if ref["nrmse_peak"] == 0 else float("inf")
    else:
        nrmse_range = (max(vals) - min(vals)) / ref["nrmse_minmax"]
        norm_change = abs(ref["nrmse_peak"] - ref["nrmse_minmax"]) / ref["nrmse_minmax"]
    observed = {
        "interpolation_nrmse_relative_range": float(nrmse_range),
        "interpolation_pearson_absolute_range": float(max(correlations) - min(correlations)),
        "normalization_nrmse_relative_change": float(norm_change),
    }
    checks = {name: bool(np.isfinite(value) and value <= THRESHOLDS[name])
              for name, value in observed.items()}
    peaks = {
        "a_nm": float(a[np.argmax(a[:, 1]), 0]),
        "b_nm": float(b[np.argmax(b[:, 1]), 0]),
    }
    return {
        "gate": "G4",
        "version": "1.0",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "reference_step_nm": 1.0,
        "overlap_nm": [float(lo), float(hi)],
        "thresholds": THRESHOLDS,
        "observed": observed,
        "checks": checks,
        "original_sampled_peaks": peaks,
        "runs": runs,
        "limitations": [
            "Project-defined provisional thresholds, not experimental uncertainties.",
            "Grid maxima are not fitted spectral peaks.",
            "Absorption shape comparison does not establish laser gain.",
            "Input audit, measurement conditions, and publication rights are separate gates.",
        ],
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--a", required=True)
    parser.add_argument("--b", required=True)
    parser.add_argument("--out", default="output/g4_gate")
    args = parser.parse_args()
    a, ha = load(args.a)
    b, hb = load(args.b)
    report = compute(a, b)
    report["input_sha256"] = {"a": ha, "b": hb}
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "g4_report.json").write_text(
        json.dumps(report, indent=2, allow_nan=False), encoding="utf-8")
    print(json.dumps(report, indent=2, allow_nan=False))
    raise SystemExit(0 if report["status"] == "PASS" else 1)

if __name__ == "__main__":
    main()
