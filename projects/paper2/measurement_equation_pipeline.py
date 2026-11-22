"""Traceable record-to-equation pipeline for conditional Beer-Lambert predictions.

This module validates typed measurement records, verifies same sample and
conditions, assesses model applicability and propagates standard uncertainties.
No claims are promoted to experimental evidence by this pipeline.
"""
import argparse
import json
import math
from pathlib import Path

try:
    from measurement_intake import validate
    from optical_solver_uncertainty import solve
except ImportError:
    import importlib.util
    def _load(name):
        spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(name + ".py"))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    validate = _load("measurement_intake").validate
    solve = _load("optical_solver_uncertainty").solve

ROLE_QUANTITY = {
    "incident_power": "optical_power",
    "absorption_coefficient": "absorption_coefficient",
    "thickness": "sample_thickness",
    "wavelength": "wavelength",
}

def evaluate(records, regime):
    if not isinstance(records, dict) or set(records) != set(ROLE_QUANTITY):
        raise ValueError("Exactly incident_power, absorption_coefficient, thickness and wavelength records required")
    checks = {}
    for role, expected in ROLE_QUANTITY.items():
        record = records[role]
        result = validate(record)
        checks[role] = result
        if result["status"] != "RECORD_ACCEPTED_FOR_REVIEW":
            return {"status": "BLOCKED_INTAKE", "role": role, "checks": checks,
                    "result": None, "claims_authorized": []}
        if record["quantity"] != expected:
            raise ValueError(f"{role}: expected quantity {expected}")
        if record["uncertainty_type"] != "standard":
            raise ValueError("Solver only accepts standard uncertainty, not expanded uncertainty")
    sample_ids = {r["sample_id"] for r in records.values()}
    conditions = {json.dumps(r["conditions"], sort_keys=True, allow_nan=False) for r in records.values()}
    if len(sample_ids) != 1 or len(conditions) != 1:
        return {"status": "BLOCKED_CONTEXT_MISMATCH", "checks": checks,
                "result": None, "claims_authorized": []}
    values = {role: checks[role]["normalized"]["value_si"] for role in ROLE_QUANTITY}
    uncertainties = {role: checks[role]["normalized"]["uncertainty_si"] for role in ROLE_QUANTITY}
    if not isinstance(regime, dict):
        raise ValueError("Regime must be an object")
    if not math.isclose(regime.get("thickness_m", -1), values["thickness"], rel_tol=1e-12, abs_tol=0):
        raise ValueError("Regime thickness differs from measured thickness")
    if not math.isclose(regime.get("wavelength_m", -1), values["wavelength"], rel_tol=1e-12, abs_tol=0):
        raise ValueError("Regime wavelength differs from measured wavelength")
    result = solve({
        "incident_power_W": values["incident_power"],
        "incident_power_std_W": uncertainties["incident_power"],
        "alpha_per_m": values["absorption_coefficient"],
        "alpha_std_per_m": uncertainties["absorption_coefficient"],
        "thickness_m": values["thickness"],
        "thickness_std_m": uncertainties["thickness"],
    }, regime)
    return {
        "status": result["status"],
        "checks": checks,
        "traceability": {
            role: {"measurement_id": records[role]["measurement_id"],
                   "source_id": records[role]["source_id"],
                   "equation_id": records[role]["equation_id"],
                   "calibration_reference": records[role]["calibration_reference"]}
            for role in ROLE_QUANTITY
        },
        "result": result["result"], "selector": result["selector"],
        "claims_authorized": [],
        "caveats": [
            "Record declarations and matching contexts do not authenticate instruments or calibration.",
            "Coefficient and incident-power values must be independently established for the modeled conditions.",
            "Calculation is a model-conditional prediction, not an experimental validation.",
            "Input uncertainty independence is assumed; correlations and model discrepancy are not included.",
        ],
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--records", required=True)
    p.add_argument("--regime", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()
    result = evaluate(json.loads(Path(args.records).read_text(encoding="utf-8")),
                      json.loads(Path(args.regime).read_text(encoding="utf-8")))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, allow_nan=False), encoding="utf-8")
    print(json.dumps(result, indent=2, allow_nan=False))
    raise SystemExit(0 if result["status"] == "COMPUTED_MODEL_CONDITIONAL" else 1)

if __name__ == "__main__":
    main()
