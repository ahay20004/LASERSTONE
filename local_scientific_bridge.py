"""Read-only local scientific engine bridge. No server, network or private datasets."""
from __future__ import annotations
import json
from physics_consistency_engine import evaluate_physics_consistency, classify_consistency

FIELDS = ("gain_score", "laser_efficiency_score", "thermal_score", "q_factor_score",
          "material_score", "lri_score")

def evaluate_synthetic_case() -> dict:
    # Deliberately synthetic; never present as measured scientific evidence.
    values = {"gain_score": 70, "laser_efficiency_score": 68, "thermal_score": 75,
              "q_factor_score": 72, "material_score": 70, "lri_score": 71}
    score = evaluate_physics_consistency(values)
    return {
        "schema": 1,
        "source_engine": "physics_consistency_engine.evaluate_physics_consistency",
        "input_kind": "SYNTHETIC_DEMONSTRATION",
        "inputs": values,
        "output": {"consistency_score": score, "classification": classify_consistency(score)},
        "independent_scientific_validation": False,
        "private_data_accessed": False,
        "public_deployment_authorized": False,
    }

def evaluate_registered_records() -> dict:
    """Read-only local screening summary; no experimental or release authorization."""
    from safe_dashboard_launcher import load_plants, prepare_dashboard_plants
    records = load_plants()
    ranked = prepare_dashboard_plants(records)
    return {
        "input_kind": "REGISTERED_LOCAL_RECORDS",
        "registered_count": len(records),
        "analyzed_count": len(ranked),
        "status": "HOLD",
        "complete": bool(records) and len(records) == len(ranked),
        "independent_scientific_validation": False,
        "public_deployment_authorized": False,
    }

if __name__ == "__main__":
    print(json.dumps(evaluate_synthetic_case(), ensure_ascii=False, indent=2))
