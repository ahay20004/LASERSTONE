"""Stage 3.3: evidence-bounded limiting-case numerical comparison.

Compares researcher-supplied reference and modified model evaluations at a
declared sequence approaching a limit. Does not execute arbitrary expressions
or prove a mathematical limit.
"""
import argparse
import json
import math
from pathlib import Path

def _finite(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)

def evaluate(case):
    if not isinstance(case, dict):
        raise ValueError("Case must be a mapping")
    if set(case) != {"parameter", "limit_value", "samples", "absolute_tolerance", "relative_tolerance"}:
        raise ValueError("Required: parameter, limit_value, samples, absolute_tolerance, relative_tolerance")
    if not isinstance(case["parameter"], str) or not case["parameter"].strip():
        raise ValueError("Parameter must be named")
    limit = case["limit_value"]
    atol, rtol = case["absolute_tolerance"], case["relative_tolerance"]
    if not _finite(limit) or not all(_finite(x) and x >= 0 for x in (atol, rtol)):
        raise ValueError("Invalid limit or tolerances")
    samples = case["samples"]
    if not isinstance(samples, list) or len(samples) < 3:
        raise ValueError("At least three independent limit-approach samples required")
    distances = []
    rows = []
    for row in samples:
        if not isinstance(row, dict) or set(row) != {"parameter_value", "reference_value", "modified_value"}:
            raise ValueError("Sample must include parameter_value, reference_value and modified_value")
        p, ref, modified = (row[k] for k in ("parameter_value", "reference_value", "modified_value"))
        if not all(_finite(x) for x in (p, ref, modified)):
            raise ValueError("Nonfinite sample")
        distance = abs(p - limit)
        if distance == 0:
            raise ValueError("Use nonzero approach distances; exact-limit evaluation is not convergence evidence")
        distances.append(distance)
        difference = abs(modified - ref)
        threshold = atol + rtol * abs(ref)
        rows.append({"distance_to_limit": distance, "absolute_difference": difference,
                     "tolerance": threshold, "within_tolerance": difference <= threshold})
    if any(distances[i+1] >= distances[i] for i in range(len(distances)-1)):
        raise ValueError("Samples must approach limit with strictly decreasing distances")
    differences = [r["absolute_difference"] for r in rows]
    improving = all(differences[i+1] <= differences[i] for i in range(len(differences)-1))
    # A small final residual is not a proof of convergence; a large residual
    # is not a global falsification of the proposed model.
    status = ("NUMERICAL_LIMIT_COMPATIBLE" if rows[-1]["within_tolerance"] and improving
              else "LIMIT_REQUIRES_INVESTIGATION")
    return {
        "status": status, "parameter": case["parameter"], "limit_value": limit,
        "samples": rows, "residual_nonincreasing": improving,
        "claims_authorized": [], "theory_endorsed": False,
        "caveats": [
            "Only supplied numerical values are compared; model implementations and provenance are not verified.",
            "Finite samples cannot prove an analytic limit or asymptotic convergence.",
            "Tolerances must be scientifically justified, not tuned to force acceptance.",
            "Correlations, numerical error and measurement uncertainty are not estimated.",
        ],
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--case", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()
    result = evaluate(json.loads(Path(args.case).read_text(encoding="utf-8")))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, allow_nan=False), encoding="utf-8")
    print(json.dumps(result, indent=2, allow_nan=False))
    raise SystemExit(0 if result["status"] == "NUMERICAL_LIMIT_COMPATIBLE" else 1)

if __name__ == "__main__":
    main()
