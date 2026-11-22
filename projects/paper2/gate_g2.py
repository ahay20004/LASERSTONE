"""G2: validate spectral input arrays before physical interpretation.

Checks physical wavelength domain, finite values, monotonic sampling, overlap,
and interpolation resolution. These are necessary data-quality conditions,
not a substitute for calibration or measurement uncertainty.
"""
import argparse
import json
from pathlib import Path
import numpy as np

def validate(a, b, step_nm=1.0, min_points=5, min_overlap_points=6):
    errors = []
    if not np.isfinite(step_nm) or step_nm <= 0:
        errors.append("step_nm must be finite and positive")
    for label, arr in (("a", a), ("b", b)):
        arr = np.asarray(arr)
        if arr.ndim != 2 or arr.shape[1] != 2 or len(arr) < min_points:
            errors.append(f"{label}: expected at least {min_points} wavelength-signal pairs")
            continue
        if not np.all(np.isfinite(arr)):
            errors.append(f"{label}: non-finite values")
            continue
        if np.any(arr[:, 0] <= 0) or np.any(np.diff(arr[:, 0]) <= 0):
            errors.append(f"{label}: wavelength must be positive and strictly increasing")
        if np.ptp(arr[:, 1]) <= 0:
            errors.append(f"{label}: constant signal")
    if not errors:
        low = max(float(a[0, 0]), float(b[0, 0]))
        high = min(float(a[-1, 0]), float(b[-1, 0]))
        if high - low < (min_overlap_points - 1) * step_nm:
            errors.append("Insufficient shared spectral range for requested step")
        else:
            grid = np.arange(low, high + 1e-10, step_nm)
            if len(grid) < min_overlap_points:
                errors.append("Insufficient shared interpolation points")
            else:
                for label, arr in (("a", a), ("b", b)):
                    sampled = np.interp(grid, arr[:, 0], arr[:, 1])
                    if np.ptp(sampled) <= 0:
                        errors.append(f"{label}: constant signal on overlap")
    return {"gate": "G2", "version": "1.0",
            "status": "PASS" if not errors else "FAIL",
            "errors": errors,
            "caveats": [
                "Input checks do not establish measurement calibration or uncertainty.",
                "Signals may require scientifically justified baseline correction.",
                "Comparability of solvents, units and acquisition conditions must be independently assessed."
            ]}

def load_pairs(path):
    pairs = []
    for line in Path(path).read_text(encoding="utf-8-sig").splitlines():
        s = line.strip()
        if not s or s.startswith(("#", ";")):
            continue
        fields = s.replace(";", ",").split(",") if "," in s or ";" in s else s.split()
        if len(fields) < 2:
            continue
        try:
            pair = (float(fields[0]), float(fields[1]))
        except ValueError:
            continue
        pairs.append(pair)
    return np.asarray(pairs, dtype=float).reshape(-1, 2)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--a", required=True)
    p.add_argument("--b", required=True)
    p.add_argument("--step", type=float, default=1.0)
    p.add_argument("--out", default="output/g2_gate")
    args = p.parse_args()
    report = validate(load_pairs(args.a), load_pairs(args.b), args.step)
    dest = Path(args.out)
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "g2_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["status"] == "PASS" else 1)

if __name__ == "__main__":
    main()
