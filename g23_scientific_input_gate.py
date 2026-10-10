"""G23 candidate scientific input gate (opt-in; production validator unchanged).

Checks only defensible numeric domains. It does not establish units, provenance,
uncertainty, experimental validity, or publication readiness.
"""
import math

REQUIRED_NUMERIC = ("phi", "tau", "sigma_a", "eta", "knr",
                    "refractive_index", "lambda_abs", "lambda_em")
REQUIRED_TEXT = ("name", "scientific_name", "origin")


def validate_scientific_inputs(plant):
    errors = {}
    if not isinstance(plant, dict):
        return {"valid": False, "errors": {"plant": "Expected a dictionary"}}

    for field in REQUIRED_TEXT:
        if not isinstance(plant.get(field), str) or not plant[field].strip():
            errors[field] = "Required nonempty text"

    for field in REQUIRED_NUMERIC:
        value = plant.get(field)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            errors[field] = "Required finite numeric value"
            continue
        try:
            finite = math.isfinite(value)
        except (TypeError, ValueError, OverflowError):
            finite = False
        if not finite:
            errors[field] = "Required finite numeric value"
            continue
        if field == "phi" and not 0 <= value <= 1:
            errors[field] = "Quantum yield must be in [0, 1]"
        elif field in ("lambda_abs", "lambda_em", "tau", "refractive_index") and value <= 0:
            errors[field] = "Must be positive"
        elif field in ("sigma_a", "knr") and value < 0:
            errors[field] = "Must be nonnegative"
        # eta is not range-limited until its physical definition is documented.
    return {"valid": not errors, "errors": errors,
            "status": "DOMAIN_SCREEN_ONLY"}
