"""First-order standard uncertainty for explicitly independent inputs."""
from math import isfinite, hypot
from numbers import Real

def _finite(value):
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(value):
        raise ValueError("Expected finite real number")
    return float(value)

def propagate_independent(sensitivities, uncertainties, *, independent):
    if independent is not True:
        raise ValueError("Independence must be explicitly established")
    if not isinstance(sensitivities, dict) or not isinstance(uncertainties, dict):
        raise ValueError("Expected mappings")
    if not sensitivities or set(sensitivities) != set(uncertainties):
        raise ValueError("Every sensitivity requires a standard uncertainty")
    contributions = {}
    for key, sensitivity in sensitivities.items():
        s = _finite(sensitivity)
        u = _finite(uncertainties[key])
        if u < 0:
            raise ValueError("Standard uncertainty cannot be negative")
        contributions[key] = _finite(s * u)
    combined = _finite(hypot(*contributions.values()))
    return {"standard_uncertainty": combined,
            "signed_contributions": contributions,
            "method": "first_order_independent",
            "scientific_validation": False}
