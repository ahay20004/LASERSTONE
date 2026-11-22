"""Stage 3.5: conservative numerical convergence and local sensitivity audit.

Inputs are independently generated, researcher-declared values. This module
does not execute a solver, establish grid independence or validate physics.
"""
import argparse
import json
import math
from pathlib import Path


def _number(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def convergence(spec):
    if not isinstance(spec, dict) or set(spec) != {"samples", "absolute_tolerance", "relative_tolerance"}:
        raise ValueError("Convergence needs samples, absolute_tolerance, relative_tolerance")
    atol, rtol = spec["absolute_tolerance"], spec["relative_tolerance"]
    if not all(_number(x) and x >= 0 for x in (atol, rtol)):
        raise ValueError("Tolerances must be finite and nonnegative")
    samples = spec["samples"]
    if not isinstance(samples, list) or len(samples) < 3:
        raise ValueError("At least three resolution samples required")
    scales, values = [], []
    for item in samples:
        if not isinstance(item, dict) or set(item) != {"resolution_scale", "value"}:
            raise ValueError("Each sample needs resolution_scale and value")
        scale, value = item["resolution_scale"], item["value"]
        if not _number(scale) or scale <= 0 or not _number(value):
            raise ValueError("Invalid resolution scale or output")
        scales.append(scale)
        values.append(value)
    if any(scales[i+1] >= scales[i] for i in range(len(scales)-1)):
        raise ValueError("Resolution scales must strictly decrease (smaller is finer)")
    changes = [abs(values[i+1] - values[i]) for i in range(len(values)-1)]
    decreasing = all(changes[i+1] <= changes[i] for i in range(len(changes)-1))
    threshold = atol + rtol * abs(values[-1])
    compatible = decreasing and changes[-1] <= threshold
    return {
        "status": "REFINEMENT_COMPATIBLE" if compatible else "REFINEMENT_REQUIRES_INVESTIGATION",
        "successive_absolute_changes": changes,
        "last_change_tolerance": threshold,
        "changes_nonincreasing": decreasing,
        "claims_authorized": [],
        "caveat": "Finite refinement samples and user-declared tolerances cannot establish solver correctness or asymptotic convergence.",
    }


def sensitivity(spec):
    if not isinstance(spec, dict) or set(spec) != {"parameter", "baseline_parameter", "baseline_output", "lower", "upper"}:
        raise ValueError("Sensitivity requires parameter, baseline_parameter, baseline_output, lower, upper")
    if not isinstance(spec["parameter"], str) or not spec["parameter"].strip():
        raise ValueError("Parameter must be named")
    x0, y0 = spec["baseline_parameter"], spec["baseline_output"]
    lower, upper = spec["lower"], spec["upper"]
    if not _number(x0) or not _number(y0):
        raise ValueError("Baseline must be finite")
    for row in (lower, upper):
        if not isinstance(row, dict) or set(row) != {"parameter_value", "output_value"}:
            raise ValueError("Perturbations require parameter_value and output_value")
        if not all(_number(v) for v in row.values()):
            raise ValueError("Perturbation values must be finite")
    xl, yl = lower["parameter_value"], lower["output_value"]
    xu, yu = upper["parameter_value"], upper["output_value"]
    if not xl < x0 < xu:
        raise ValueError("Perturbations must bracket baseline strictly")
    derivative = (yu - yl) / (xu - xl)
    if not math.isfinite(derivative):
        raise ValueError("Derivative overflow")
    normalized = None if x0 == 0 or y0 == 0 else derivative * x0 / y0
    if normalized is not None and not math.isfinite(normalized):
        raise ValueError("Normalized sensitivity overflow")
    return {
        "status": "LOCAL_FINITE_DIFFERENCE_RECORDED",
        "central_secant_slope": derivative,
        "normalized_sensitivity": normalized,
        "normalization_available": normalized is not None,
        "claims_authorized": [],
        "caveat": "A two-sided secant is a local numerical diagnostic; nonlinear behavior, uncertainty and causality are not established.",
    }


def audit(convergence_spec=None, sensitivity_spec=None):
    if convergence_spec is None and sensitivity_spec is None:
        raise ValueError("At least one numerical audit is required")
    results = {}
    if convergence_spec is not None:
        results["numerical_convergence"] = convergence(convergence_spec)
    if sensitivity_spec is not None:
        results["parameter_sensitivity"] = sensitivity(sensitivity_spec)
    return {"results": results, "claims_authorized": [], "endorsement": "NONE"}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--convergence")
    p.add_argument("--sensitivity")
    p.add_argument("--out", required=True)
    args = p.parse_args()
    def read(path):
        return json.loads(Path(path).read_text(encoding="utf-8")) if path else None
    result = audit(read(args.convergence), read(args.sensitivity))
    dest = Path(args.out)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(result, indent=2, allow_nan=False), encoding="utf-8")
    print(json.dumps(result, indent=2, allow_nan=False))
    raise SystemExit(0 if all(r["status"] != "REFINEMENT_REQUIRES_INVESTIGATION"
                              for r in result["results"].values()) else 1)


if __name__ == "__main__":
    main()
