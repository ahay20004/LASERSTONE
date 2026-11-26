"""LS-USE: registry-driven optical monomial calculations in SI."""
from decimal import Decimal, localcontext
from equation_registry import REGISTRY, check_equation
from equation_domain_gate import assess_inputs
from physical_constants import get_record
from physical_quantities import get_quantity
from unit_conversion import convert
from scientific_result_format import format_result

def evaluate(identifier, inputs, output_unit=None):
    eq = REGISTRY[identifier]
    required = {name for kind,name,power in eq.factors if kind == "quantity"}
    if not isinstance(inputs, dict) or set(inputs) != required:
        raise ValueError("Exact input identifiers required")
    with localcontext() as ctx:
        ctx.prec = 34
        si = {}
        for name, item in inputs.items():
            if not isinstance(item, dict) or set(item) != {"value","unit"}:
                raise ValueError("Explicit value and unit required")
            si[name] = convert(item["value"], name, item["unit"], get_quantity(name).unit)
        domain = assess_inputs(identifier, si)
        if domain["status"] != "INPUT_DOMAIN_PASS":
            raise ValueError(str(domain["errors"]))
        dimensions = check_equation(identifier)
        if dimensions["status"] != "DIMENSIONALLY_CONSISTENT":
            raise ValueError("Dimensional check failed")
        value = Decimal(eq.coefficient)
        constants = {}
        for kind,name,power in eq.factors:
            if kind == "constant":
                record = get_record(name)
                x = Decimal(str(record.value))
                constants[name] = {"value":str(x),"unit":record.unit,
                                   "source":record.source,"version":record.version}
            elif kind == "quantity":
                x = si[name]
            else:
                raise ValueError("Unknown factor kind")
            value *= x ** power
        if not value.is_finite() or value <= 0:
            raise ValueError("Invalid optical result")
        quantity = get_quantity(eq.output)
        unit = quantity.unit if output_unit is None else output_unit
        displayed = convert(value, eq.output, quantity.unit, unit)
        return {"equation_id":identifier,"expression":eq.expression,
                "coefficient":eq.coefficient,"conditions":eq.conditions,
                "inputs_si":{k:str(v) for k,v in si.items()},
                "constants":constants,"value_si":str(value),"unit_si":quantity.unit,
                "result":format_result(displayed,None,unit),
                "dimensional_assessment":dimensions,
                "model_conditions_verified":False,"scientific_validation":False}
