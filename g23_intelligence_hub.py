"""Strict G23 intelligence hub candidate.

This module repairs silent missing->zero behavior and the legacy connectivity
counting bug without replacing the production intelligence_hub.py.
"""

from __future__ import annotations

from typing import Any, Mapping

from constants import THRESHOLDS
from g23_scientific_missing_policy import require_score

INTELLIGENCE_WEIGHTS = {
    "material_score": 0.20,
    "lri_score": 0.15,
    "experimental_success_score": 0.15,
    "research_novelty_score": 0.15,
    "patent_potential_score": 0.10,
    "scientific_confidence_score": 0.15,
    "system_integrity_score": 0.10,
}


def classify_intelligence_strict(score: float) -> str:
    if score >= THRESHOLDS["elite"]:
        return "Elite Scientific Intelligence"
    if score >= THRESHOLDS["advanced"]:
        return "Advanced Scientific Intelligence"
    if score >= THRESHOLDS["promising"]:
        return "Promising Scientific Intelligence"
    return "Developing Scientific Intelligence"


def generate_intelligence_summary_strict(
    record: Mapping[str, Any],
) -> dict[str, Any]:
    values = {
        field: require_score(record, field)
        for field in INTELLIGENCE_WEIGHTS
    }

    score = sum(
        values[field] * weight
        for field, weight in INTELLIGENCE_WEIGHTS.items()
    )

    return {
        **values,
        "intelligence_score": round(score, 2),
        "classification": classify_intelligence_strict(score),
        "status": "HEURISTIC_INTELLIGENCE_STRICT_INPUTS",
        "physical_validation": "NOT_ESTABLISHED",
    }


def analyze_declared_registry_connectivity(
    registry: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    """Correctly count declared connected/isolated entries.

    This fixes the legacy for...else counting bug while keeping the metric
    explicitly structural rather than scientific.
    """
    if not isinstance(registry, Mapping):
        raise TypeError("registry must be a mapping")

    connected = 0
    isolated = 0
    most_connected_engine = None
    most_connections = -1

    for engine_name, info in registry.items():
        inputs = info.get("inputs", [])
        outputs = info.get("outputs", [])
        connections = len(inputs) + len(outputs)

        if connections > 0:
            connected += 1
        else:
            isolated += 1

        if connections > most_connections:
            most_connections = connections
            most_connected_engine = engine_name

    total = len(registry)
    coverage = round(100.0 * connected / total, 2) if total else 0.0

    return {
        "total_entries": total,
        "declared_connected": connected,
        "declared_isolated": isolated,
        "declared_connectivity_percent": coverage,
        "most_connected_engine": most_connected_engine,
        "most_connections": max(most_connections, 0),
        "status": "STRUCTURAL_CONNECTIVITY_ONLY",
        "scientific_validation": "NOT_ESTABLISHED",
    }
