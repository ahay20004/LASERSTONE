"""Analytic local sensitivities for registered optical monomials."""
from decimal import Decimal, localcontext
from equation_registry import REGISTRY
from unified_scientific_engine import evaluate

def sensitivities(identifier, inputs):
    result = evaluate(identifier, inputs)
    powers = {}
    for kind, name, power in REGISTRY[identifier].factors:
        if kind == "quantity":
            powers[name] = powers.get(name, 0) + power
    with localcontext() as ctx:
        ctx.prec = 34
        y = Decimal(result["value_si"])
        derivatives = {name: str(Decimal(power)*y/Decimal(result["inputs_si"][name]))
                       for name, power in powers.items()}
    return {"calculation": result, "sensitivities_si": derivatives,
            "relative_sensitivities": powers, "method": "analytic_monomial",
            "scientific_validation": False}
