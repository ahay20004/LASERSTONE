"""Bounded real handoff: legacy thermal screening -> legacy material ranking.

No mutation of either legacy engine. Thermal score is a heuristic DERIVED
output, not measured temperature, thermal lifetime, or calibrated stability.
"""
from dataclasses import dataclass

from cloud.core_thermal_screen_gate import (
    FIELDS as THERMAL_FIELDS, ThermalInput, evaluate_thermal_screen,
)
from cloud.core_material_score_gate import (
    FIELDS as MATERIAL_FIELDS, ScoreInput, evaluate_material_score,
)


@dataclass(frozen=True)
class MaterialThermalRequest:
    thermal_inputs: dict[str, ThermalInput]
    material_inputs: dict[str, ScoreInput]


def evaluate_material_with_thermal(request: MaterialThermalRequest):
    if not isinstance(request, MaterialThermalRequest):
        raise TypeError("MaterialThermalRequest required")
    if not isinstance(request.thermal_inputs, dict) or set(request.thermal_inputs) != set(THERMAL_FIELDS):
        raise ValueError("complete thermal inputs required")
    if not isinstance(request.material_inputs, dict) or set(request.material_inputs) != set(MATERIAL_FIELDS) - {"thermal_score"}:
        raise ValueError("five nonthermal material inputs required; thermal_score must be derived")
    thermal = evaluate_thermal_screen(request.thermal_inputs)
    material_inputs = dict(request.material_inputs)
    material_inputs["thermal_score"] = ScoreInput(
        value=thermal["score"],
        source="DERIVED:thermal_engine.evaluate_thermal_stability; bounded heuristic adapter",
        evidence_state="DERIVED",
    )
    material = evaluate_material_score(material_inputs)
    if material["input_provenance"]["thermal_score"]["evidence_state"] != "DERIVED":
        raise ValueError("thermal handoff provenance lost")
    return {
        "scope": "LEGACY_THERMAL_TO_MATERIAL_HEURISTIC_HANDOFF",
        "thermal_screen": thermal,
        "material_ranking": material,
        "handoff_value": thermal["score"],
        "handoff_unit": "heuristic_score_0_100",
        "handoff_evidence_state": "DERIVED",
        "integration_passed": thermal["independent_formula_agreement"] and material["independent_formula_agreement"],
        "experimental_validation": False,
        "predictive_calibration": False,
        "university_connected": False,
        "limitations": [
            "The thermal heuristic score is not a thermodynamic measurement",
            "Both original model threshold and weight choices remain uncalibrated",
            "Caller supplied provenance is recorded but not independently authenticated",
            "The material score is a legacy ranking, not a validated laser material property",
        ],
    }
