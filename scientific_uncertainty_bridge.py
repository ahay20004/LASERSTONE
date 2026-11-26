"""First-order uncertainty integration for registered optical equations."""
from decimal import Decimal
from math import isfinite
from equation_sensitivity import sensitivities
from physical_quantities import get_quantity
from physical_constants import get_record
from equation_registry import REGISTRY
from unit_conversion import convert
from measurement_uncertainty import propagate_independent, propagate_correlated
from scientific_result_format import format_result

def checked_float(value):
    original = Decimal(str(value))
    converted = float(original)
    if not isfinite(converted) or (original != 0 and converted == 0):
        raise ValueError("Value outside supported floating-point range")
    return converted

def evaluate_with_uncertainty(identifier, inputs, uncertainties, *,
                              independent=False, correlation=None, output_unit=None):
    analysis = sensitivities(identifier, inputs)
    result = analysis["calculation"]
    derivatives = analysis["sensitivities_si"]
    if not isinstance(uncertainties, dict) or set(uncertainties) != set(derivatives):
        raise ValueError("Explicit uncertainty required for each input")
    for kind, name, power in REGISTRY[identifier].factors:
        if kind == "constant" and not get_record(name).exact:
            raise ValueError("Uncertain constants not supported by this bridge")
    u_si = {}
    for name, item in uncertainties.items():
        if not isinstance(item, dict) or set(item) != {"value", "unit"}:
            raise ValueError("Explicit uncertainty value and unit required")
        u = convert(item["value"], name, item["unit"], get_quantity(name).unit)
        if u < 0:
            raise ValueError("Negative uncertainty")
        u_si[name] = checked_float(u)
    s = {name: checked_float(value) for name, value in derivatives.items()}
    if correlation is None:
        propagated = propagate_independent(s, u_si, independent=independent)
    else:
        if independent is not False:
            raise ValueError("Conflicting independence and correlation declarations")
        propagated = propagate_correlated(s, u_si, correlation)
    quantity = REGISTRY[identifier].output
    unit = result["unit_si"] if output_unit is None else output_unit
    value = convert(result["value_si"], quantity, result["unit_si"], unit)
    uncertainty = convert(propagated["standard_uncertainty"], quantity, result["unit_si"], unit)
    result["result"] = format_result(value, uncertainty, unit)
    result["uncertainty_analysis"] = propagated
    result["sensitivities_si"] = derivatives
    result["input_uncertainties_si"] = u_si
    result["correlation"] = correlation
    result["linear_approximation_verified"] = False
    return result
