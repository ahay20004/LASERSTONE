"""Fail-closed adapter for the existing heuristic material score engine.

A score is a model-defined ranking, NOT a measured laser performance or
patentability estimate. All inputs require named provenance and evidence state.
"""
from dataclasses import dataclass
from math import isfinite
from material_score_engine import calculate_material_score, classify_material_score
from constants import MATERIAL_SCORE_WEIGHTS

FIELDS = ("lsi", "thermal_score", "q_factor_score", "beam_quality_score",
          "laser_efficiency_score", "spectral_quality")
EVIDENCE = frozenset(("MEASURED", "DERIVED", "SIMULATED", "PREDICTED"))


@dataclass(frozen=True)
class ScoreInput:
    value: float
    source: str
    evidence_state: str


def evaluate_material_score(inputs: dict[str, ScoreInput]):
    if not isinstance(inputs, dict) or set(inputs) != set(FIELDS):
        raise ValueError("all six score inputs required; no implicit defaults")
    payload = {}
    provenance = {}
    for field in FIELDS:
        item = inputs[field]
        if not isinstance(item, ScoreInput):
            raise ValueError(f"{field}: ScoreInput required")
        if (isinstance(item.value, bool) or not isinstance(item.value, (int, float))
                or not isfinite(item.value)):
            raise ValueError(f"{field}: finite numeric value required")
        maximum = 10 if field == "lsi" else 100
        if not 0 <= item.value <= maximum:
            raise ValueError(f"{field}: outside declared heuristic range 0–{maximum}")
        if not isinstance(item.source, str) or not item.source.strip():
            raise ValueError(f"{field}: named source required")
        if item.evidence_state not in EVIDENCE:
            raise ValueError(f"{field}: valid evidence state required")
        payload[field] = float(item.value)
        provenance[field] = {"source": item.source, "evidence_state": item.evidence_state}
    weights = [MATERIAL_SCORE_WEIGHTS[k] for k in
               ("lsi", "thermal", "q_factor", "beam_quality", "efficiency", "spectral")]
    if (any(isinstance(w, bool) or not isinstance(w, (int, float))
            or not isfinite(w) or w < 0 for w in weights)
            or abs(sum(weights) - 1) > 1e-9):
        raise ValueError("material score weights must be finite nonnegative and sum to 1")
    observed = calculate_material_score(payload)
    independent = round(sum(v * w for v, w in zip(
        (payload["lsi"] * 10, payload["thermal_score"], payload["q_factor_score"],
         payload["beam_quality_score"], payload["laser_efficiency_score"],
         payload["spectral_quality"]), weights)), 2)
    if observed != independent:
        raise ValueError("material score independent regression mismatch")
    return {
        "engine": "material_score_engine.calculate_material_score",
        "scope": "PROVENANCE_GATED_HEURISTIC_RANKING_ONLY",
        "score": observed,
        "legacy_classification": classify_material_score(observed),
        "independent_formula_agreement": True,
        "input_provenance": provenance,
        "scientific_validation": False,
        "experimental_validation": False,
        "patentability_assessment": False,
        "university_connected": False,
        "limitations": [
            "Scores and weights are legacy heuristics, not calibrated physical measurements",
            "Input provenance is caller supplied and is not independently authenticated",
            "No missing input is replaced with zero",
            "No evidence that score classes predict laser performance or patent eligibility",
        ],
    }
