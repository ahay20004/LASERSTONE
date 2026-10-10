"""G23 non-invasive registry contract correction candidate.

This view does not mutate PROJECT_REGISTRY or change existing engine behavior.
"""
from project_registry import PROJECT_REGISTRY

CONSISTENCY_INPUTS = (
    "gain_score", "laser_efficiency_score", "thermal_score",
    "q_factor_score", "material_score", "lri_score",
)


def corrected_registry_view():
    registry = {name: dict(info) for name, info in PROJECT_REGISTRY.items()}
    if "physics_consistency_engine" not in registry:
        raise KeyError("physics_consistency_engine missing from registry")
    registry["physics_consistency_engine"]["inputs"] = list(CONSISTENCY_INPUTS)
    return registry
