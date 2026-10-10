"""G23 opt-in guarded physics consistency assessment.

The legacy score is a heuristic comparison of six scores, NOT physical proof.
This adapter never alters the legacy engine or fabricates missing inputs.
"""
import math
from physics_consistency_engine import evaluate_physics_consistency

REQUIRED_SCORES = (
    "gain_score", "laser_efficiency_score", "thermal_score",
    "q_factor_score", "material_score", "lri_score",
)

def assess_physics_consistency(plant):
    if not isinstance(plant, dict):
        return {"status": "INVALID_INPUT", "score": None,
                "errors": {"plant": "Expected dictionary"}}
    errors = {}
    for key in REQUIRED_SCORES:
        value = plant.get(key)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            errors[key] = "Required numeric score"
        elif not math.isfinite(value):
            errors[key] = "Score must be finite"
        elif not 0 <= value <= 100:
            errors[key] = "Score outside [0, 100]"
    if errors:
        return {"status": "INSUFFICIENT_OR_INVALID_SCORES",
                "score": None, "errors": errors}
    return {"status": "HEURISTIC_SCORE_ONLY",
            "score": evaluate_physics_consistency(plant), "errors": {}}
