"""Shared calculation contract for five scientific knowledge pathways."""
from dataclasses import asdict
from unified_scientific_engine import evaluate
from scientific_uncertainty_bridge import evaluate_with_uncertainty
from quantity_relationships import describe_equation

PATHWAYS = ("student", "educator", "researcher", "reviewer", "validation")

def build_pathways(identifier, inputs, *, uncertainties=None,
                   independent=False, correlation=None, output_unit=None):
    if uncertainties is None:
        if independent is not False or correlation is not None:
            raise ValueError("Uncertainty assumptions require uncertainties")
        result = evaluate(identifier, inputs, output_unit)
    else:
        result = evaluate_with_uncertainty(identifier, inputs, uncertainties,
            independent=independent, correlation=correlation, output_unit=output_unit)
    equation = describe_equation(identifier)
    equation["constants"] = [(name, power, asdict(record)) for name, power, record in equation["constants"]]
    result["uncertainty_analysis"] = result.get("uncertainty_analysis")
    return {
        "shared_result": result,
        "shared_equation": equation,
        "pathways": {
            "student": {"focus": ["expression", "inputs_si", "result"]},
            "educator": {"focus": ["expression", "constants", "conditions"]},
            "researcher": {"focus": ["inputs_si", "result", "uncertainty_analysis"]},
            "reviewer": {"focus": ["dimensional_assessment", "constants", "conditions"]},
            "validation": {"focus": ["model_conditions_verified", "scientific_validation"]},
        },
        "scientific_validation": False,
        "release_authorized": False,
    }
