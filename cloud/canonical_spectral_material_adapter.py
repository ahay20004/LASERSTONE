"""Explicit spectral label contract and material ranking impact assessment.

Canonical policy follows data_standardization_engine for High/Medium/Low.
Original legacy engines and main.py remain unchanged; no global patching.
"""
from dataclasses import dataclass
from math import isfinite

from spectral_quality_engine import calculate_spectral_quality
from data_standardization_engine import standardize_quality_value
from material_score_engine import calculate_material_score
from cloud.core_material_score_gate import ScoreInput, evaluate_material_score

CANONICAL = {"High": 100, "Medium": 60, "Low": 30}
OTHER_FIELDS = ("lsi", "thermal_score", "q_factor_score",
                "beam_quality_score", "laser_efficiency_score")


@dataclass(frozen=True)
class SpectralMaterialRequest:
    spectral_inputs: dict
    other_scores: dict[str, ScoreInput]


def evaluate_spectral_material(request: SpectralMaterialRequest):
    if not isinstance(request, SpectralMaterialRequest):
        raise ValueError("SpectralMaterialRequest required")
    if not isinstance(request.spectral_inputs, dict) or set(request.spectral_inputs) != {
        "phi", "tau", "sigma_a", "knr"
    }:
        raise ValueError("exactly four spectral inputs required")
    for name, value in request.spectral_inputs.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
            raise ValueError(f"{name}: finite numeric input required")
        if (name == "phi" and not 0 <= value <= 1) or (
            name in ("tau", "knr") and value <= 0
        ) or (name == "sigma_a" and value < 0):
            raise ValueError(f"{name}: outside bounded legacy domain")
    if not isinstance(request.other_scores, dict) or set(request.other_scores) != set(OTHER_FIELDS):
        raise ValueError("exactly five non-spectral ScoreInput values required")
    label = calculate_spectral_quality(request.spectral_inputs)
    if label not in CANONICAL:
        raise ValueError("unrecognized spectral label")
    numeric = CANONICAL[label]
    if standardize_quality_value(label) != numeric:
        raise ValueError("standardization contract drift")
    gated = dict(request.other_scores)
    gated["spectral_quality"] = ScoreInput(
        numeric, "DERIVED:spectral_quality_engine; canonical data_standardization_engine mapping",
        "DERIVED",
    )
    result = evaluate_material_score(gated)
    # Actual historical main.py passes a *string* to material_score_engine,
    # not spectral_quality_score. Compare without changing that behavior.
    legacy = {name: item.value for name, item in request.other_scores.items()
              if isinstance(item, ScoreInput)}
    legacy["spectral_quality"] = label
    historical = calculate_material_score(legacy)
    return {
        "scope": "EXPLICIT_CANONICAL_SPECTRAL_TO_MATERIAL_ADAPTER",
        "label": label, "canonical_spectral_score": numeric,
        "legacy_main_style_material_score": historical,
        "corrected_material_score": result["score"],
        "material_score_delta": round(result["score"] - historical, 2),
        "material_score_result": result,
        "policy": "High=100, Medium=60, Low=30; derived from existing data_standardization_engine",
        "original_engines_modified": False,
        "main_pipeline_modified": False,
        "main_pipeline_corrected": False,
        "experimental_validation": False,
        "limitations": [
            "Impact is calculated for synthetic/explicit caller data only",
            "Original main.py still sends a label to material scoring",
            "Spectral quality formula and score weights are legacy heuristics",
            "No source-level physical calibration is established",
        ],
    }
