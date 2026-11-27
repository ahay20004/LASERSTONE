"""Input-domain checks for initial optical equations, not model validation."""
from decimal import Decimal, InvalidOperation
from equation_registry import REGISTRY

def assess_inputs(identifier, inputs):
    eq = REGISTRY[identifier]
    required = {name for kind, name, power in eq.factors if kind == "quantity"}
    if not isinstance(inputs, dict):
        raise ValueError("Expected SI input mapping")
    errors = []
    if set(inputs) != required:
        errors.append("Input identifiers must exactly match equation requirements")
    for name in sorted(required & set(inputs)):
        value = inputs[name]
        try:
            if isinstance(value, bool):
                raise ValueError("Boolean input")
            number = Decimal(str(value))
            if not number.is_finite() or number <= 0:
                raise ValueError("Expected positive finite value")
        except (InvalidOperation, ValueError, TypeError):
            errors.append("Invalid positive finite SI input: " + name)
    return {"status": "INPUT_DOMAIN_PASS" if not errors else "INPUT_DOMAIN_FAIL",
            "errors": errors, "model_conditions": eq.conditions,
            "model_conditions_verified": False, "scientific_validation": False}
