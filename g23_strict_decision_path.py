"""Strict wrappers for legacy decision-path engines.

These wrappers preserve legacy formulas where possible but remove silent
missing->zero behavior. Outputs remain explicitly heuristic and are not
physical-validation claims.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from constants import LRI_WEIGHTS, MATERIAL_SCORE_WEIGHTS
from final_decision_engine import generate_final_decision
from g23_data_standardization_engine import standardize_quality_value_strict
from g23_scientific_missing_policy import (
    MissingScientificDataError,
    require_finite_number,
    require_score,
)
from physics_consistency_engine import evaluate_physics_consistency
from scientific_confidence_engine import calculate_scientific_confidence

LRI_FIELDS = (
    "thermal_score",
    "q_factor_score",
    "laser_efficiency_score",
    "beam_quality_score",
    "feasibility_score",
)

CONSISTENCY_FIELDS = (
    "gain_score",
    "laser_efficiency_score",
    "thermal_score",
    "q_factor_score",
    "material_score",
    "lri_score",
)

FINAL_DECISION_FIELDS = (
    "material_score",
    "lri_score",
    "physics_consistency_score",
)

CONFIDENCE_FIELDS = (
    "physics_consistency_score",
    "experimental_success_score",
    "research_novelty_score",
    "patent_potential_score",
)


def calculate_material_score_strict(
    record: Mapping[str, Any],
) -> dict[str, Any]:
    lsi = require_finite_number(record, "lsi", minimum=0.0)
    thermal = require_score(record, "thermal_score")
    q_factor = require_score(record, "q_factor_score")
    beam = require_score(record, "beam_quality_score")
    efficiency = require_score(record, "laser_efficiency_score")

    if "spectral_quality" not in record:
        raise MissingScientificDataError("spectral_quality is required and is missing")
    spectral_result = standardize_quality_value_strict(record.get("spectral_quality"))
    if spectral_result["value"] is None:
        raise MissingScientificDataError(
            "spectral_quality is unavailable or unrecognized"
        )
    spectral = spectral_result["value"]

    normalized_lsi = min(lsi * 10.0, 100.0)
    score = (
        normalized_lsi * MATERIAL_SCORE_WEIGHTS["lsi"]
        + thermal * MATERIAL_SCORE_WEIGHTS["thermal"]
        + q_factor * MATERIAL_SCORE_WEIGHTS["q_factor"]
        + beam * MATERIAL_SCORE_WEIGHTS["beam_quality"]
        + efficiency * MATERIAL_SCORE_WEIGHTS["efficiency"]
        + spectral * MATERIAL_SCORE_WEIGHTS["spectral"]
    )

    return {
        "score": round(score, 2),
        "status": "HEURISTIC_MATERIAL_SCORE_STRICT_INPUTS",
        "physical_validation": "NOT_ESTABLISHED",
        "spectral_standardization_status": spectral_result["status"],
    }


def calculate_lri_strict(record: Mapping[str, Any]) -> dict[str, Any]:
    values = {field: require_score(record, field) for field in LRI_FIELDS}
    score = (
        values["thermal_score"] * LRI_WEIGHTS["thermal"]
        + values["q_factor_score"] * LRI_WEIGHTS["q_factor"]
        + values["laser_efficiency_score"] * LRI_WEIGHTS["efficiency"]
        + values["beam_quality_score"] * LRI_WEIGHTS["beam_quality"]
        + values["feasibility_score"] * LRI_WEIGHTS["feasibility"]
    )
    return {
        "score": round(score, 2),
        "status": "HEURISTIC_SCORE_STRICT_INPUTS",
        "physical_validation": "NOT_ESTABLISHED",
    }


def evaluate_physics_consistency_strict(
    record: Mapping[str, Any],
) -> dict[str, Any]:
    checked = deepcopy(dict(record))
    for field in CONSISTENCY_FIELDS:
        checked[field] = require_score(record, field)
    return {
        "score": evaluate_physics_consistency(checked),
        "status": "HEURISTIC_CONSISTENCY_STRICT_INPUTS",
        "physical_validation": "NOT_ESTABLISHED",
    }


def generate_final_decision_strict(
    record: Mapping[str, Any],
) -> dict[str, Any]:
    checked = deepcopy(dict(record))
    for field in FINAL_DECISION_FIELDS:
        checked[field] = require_score(record, field)
    return {
        "decision": generate_final_decision(checked),
        "status": "HEURISTIC_RESEARCH_TRIAGE_ONLY",
        "prototype_authorization": False,
        "physical_validation": "NOT_ESTABLISHED",
    }


def calculate_scientific_confidence_strict(
    record: Mapping[str, Any],
) -> dict[str, Any]:
    checked = deepcopy(dict(record))
    for field in CONFIDENCE_FIELDS:
        checked[field] = require_score(record, field)
    return {
        "score": calculate_scientific_confidence(checked),
        "status": "HEURISTIC_CONFIDENCE_MODEL_STRICT_INPUTS",
        "physical_confidence_claim": False,
    }
