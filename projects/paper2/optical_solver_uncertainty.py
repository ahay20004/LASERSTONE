"""Fail-closed Beer-Lambert solver with first-order independent uncertainties.

The solver is only enabled when the dynamic equation selector returns
APPLICABLE, and its input uncertainties are standard (1-sigma) values.
It does not verify model assumptions, calibrations, or measurement provenance.
"""
import argparse
import json
import math
from pathlib import Path

try:
    from dynamic_equation_selector import select_optical_model
except ImportError:
    import importlib.util
    _spec = importlib.util.spec_from_file_location(
        "dynamic_equation_selector", Path(__file__).with_name("dynamic_equation_selector.py"))
    _module = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_module)
    select_optical_model = _module.select_optical_model

def _finite(v, *, nonnegative=False, positive=False):
    return (isinstance(v, (float, int)) and not isinstance(v, bool)
            and math.isfinite(v) and (v > 0 if positive else v >= 0 if nonnegative else True))

def solve(record, regime):
    if not isinstance(record, dict):
        raise ValueError("Solver input must be a mapping")
    model = select_optical_model(regime)
    if model["models"]["beer_lambert"]["status"] != "APPLICABLE":
        return {"status": "BLOCKED_MODEL_NOT_APPLICABLE", "selector": model,
                "claims_authorized": [], "result": None}
    required = ("incident_power_W", "incident_power_std_W", "alpha_per_m",
                "alpha_std_per_m", "thickness_m", "thickness_std_m")
    if any(k not in record for k in required):
        raise ValueError("Missing required solver input or standard uncertainty")
    p, up = record["incident_power_W"], record["incident_power_std_W"]
    alpha, ua = record["alpha_per_m"], record["alpha_std_per_m"]
    d, ud = record["thickness_m"], record["thickness_std_m"]
    if not (_finite(p, positive=True) and _finite(alpha, nonnegative=True)
            and _finite(d, positive=True)
            and all(_finite(u, nonnegative=True) for u in (up, ua, ud))):
        raise ValueError("Invalid finite values or standard uncertainties")
    if not math.isclose(d, regime["thickness_m"], rel_tol=1e-12, abs_tol=0):
        raise ValueError("Solver thickness differs from applicability assessment")
    # Guard against underflow or overflow and silently meaningless outputs.
    optical_depth = alpha * d
    if not math.isfinite(optical_depth) or optical_depth > 700:
        raise ValueError("Optical depth outside supported numerical range")
    t = math.exp(-optical_depth)
    transmitted = p * t
    if not math.isfinite(transmitted) or transmitted <= 0:
        raise ValueError("Transmitted power not numerically representable")
    # First-order propagation assuming mutually independent input errors:
    # u(Pout)^2=(T u(Pin))^2+(Pin*T*d*u(alpha))^2+(Pin*T*alpha*u(d))^2.
    u_out = math.hypot(t * up, transmitted * math.hypot(d * ua, alpha * ud))
    if not math.isfinite(u_out):
        raise ValueError("Nonfinite propagated uncertainty")
    return {
        "status": "COMPUTED_MODEL_CONDITIONAL", "selector": model,
        "equation": "Pout=Pin*exp(-alpha*d)",
        "result": {"transmittance": t, "optical_depth": optical_depth,
                   "transmitted_power_W": transmitted,
                   "transmitted_power_standard_uncertainty_W": u_out},
        "uncertainty_model": "First-order propagation; independent standard uncertainties; no covariance",
        "claims_authorized": [],
        "caveats": [
            "Numerical result is model-conditional, not a measured optical power.",
            "Assumptions, alpha calibration, uncertainty independence and traceability are unverified.",
            "High uncertainty/nonlinear propagation may require Monte Carlo or covariance modeling.",
            "No optical gain or laser threshold is established.",
        ],
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--inputs", required=True)
    p.add_argument("--regime", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()
    inputs = json.loads(Path(args.inputs).read_text(encoding="utf-8"))
    regime = json.loads(Path(args.regime).read_text(encoding="utf-8"))
    result = solve(inputs, regime)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, allow_nan=False), encoding="utf-8")
    print(json.dumps(result, indent=2, allow_nan=False))
    raise SystemExit(0 if result["status"] == "COMPUTED_MODEL_CONDITIONAL" else 1)

if __name__ == "__main__":
    main()
