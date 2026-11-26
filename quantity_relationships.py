"""Read-only relationship discovery from registered equations; no inferred causality."""
from physical_quantities import get_quantity
from physical_constants import get_record
from equation_registry import REGISTRY, check_equation

def describe_quantity(identifier):
    quantity = get_quantity(identifier)
    produced_by = []
    used_by = []
    for key, eq in REGISTRY.items():
        if eq.output == identifier:
            produced_by.append(key)
        if any(kind == "quantity" and name == identifier
               for kind, name, power in eq.factors):
            used_by.append(key)
    return {"identifier": identifier, "symbol": quantity.symbol,
            "unit": quantity.unit, "dimensions": quantity.dimensions,
            "produced_by": tuple(produced_by), "used_by": tuple(used_by)}

def describe_equation(identifier):
    eq = REGISTRY[identifier]
    return {"identifier": identifier, "expression": eq.expression,
            "output": describe_quantity(eq.output),
            "inputs": tuple((name, power, describe_quantity(name))
                            for kind, name, power in eq.factors if kind == "quantity"),
            "constants": tuple((name, power, get_record(name))
                               for kind, name, power in eq.factors if kind == "constant"),
            "conditions": eq.conditions,
            "dimensional_assessment": check_equation(identifier),
            "scientific_validation": False}
