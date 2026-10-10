"""G23 simulation exchange contract; no external simulator is invoked.

Standard-library-only validation of a transport envelope. Passing this
contract does not validate the underlying physics or provenance claims.
"""
import math

SUPPORTED = frozenset({"python", "matlab", "scaps-1d", "comsol", "zemax", "lumerical"})
REQUIRED = ("simulator", "simulator_version", "model_id", "run_id",
            "inputs", "outputs", "conditions", "provenance")


def validate_simulation_envelope(envelope):
    errors = {}
    if not isinstance(envelope, dict):
        return {"valid": False, "errors": {"envelope": "Expected dictionary"},
                "status": "CONTRACT_ONLY"}
    for key in REQUIRED:
        if key not in envelope:
            errors[key] = "Missing required field"
    if errors:
        return {"valid": False, "errors": errors, "status": "CONTRACT_ONLY"}
    if envelope["simulator"] not in SUPPORTED:
        errors["simulator"] = "Unknown simulator identifier"
    for key in ("simulator_version", "model_id", "run_id"):
        if not isinstance(envelope[key], str) or not envelope[key].strip():
            errors[key] = "Required nonempty string"
    for key in ("inputs", "outputs"):
        items = envelope[key]
        if not isinstance(items, dict) or not items:
            errors[key] = "Expected nonempty mapping"
            continue
        for name, datum in items.items():
            if not isinstance(name, str) or not name.strip():
                errors[key] = "Variable names must be nonempty strings"
                continue
            if not isinstance(datum, dict):
                errors[f"{key}.{name}"] = "Expected value/unit record"
                continue
            value, unit = datum.get("value"), datum.get("unit")
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                errors[f"{key}.{name}.value"] = "Expected finite numeric scalar"
            else:
                try:
                    finite = math.isfinite(value)
                except (ValueError, TypeError, OverflowError):
                    finite = False
                if not finite:
                    errors[f"{key}.{name}.value"] = "Expected finite numeric scalar"
            if not isinstance(unit, str) or not unit.strip():
                errors[f"{key}.{name}.unit"] = "Explicit unit required (use '1' if dimensionless)"
    for key in ("conditions", "provenance"):
        if not isinstance(envelope[key], dict) or not envelope[key]:
            errors[key] = "Expected nonempty mapping"
    return {"valid": not errors, "errors": errors, "status": "CONTRACT_ONLY"}
