"""Evidence-to-engine compatibility audit for LASERSTONE G23.

The audit answers whether a normalized PhotochemCAD record can safely feed a
reviewed engine without fabricating missing values or crossing unresolved unit
contracts.
"""

from __future__ import annotations

from typing import Any, Mapping

from photochemcad_integration_gate import assess_photochemcad_for_legacy
from physical_spectral_evidence_engine import analyze_physical_spectral_evidence

ENGINE_REQUIREMENTS = {
    "physical_spectral_evidence_engine": {
        "legacy_fields": (),
        "external_dependencies": (),
        "claim_level": "EVIDENCE_ANALYSIS",
    },
    "spectral_analysis": {
        "legacy_fields": ("lambda_abs", "lambda_em"),
        "external_dependencies": (),
        "claim_level": "SPECTRAL_DERIVATION",
    },
    "spectral_region": {
        "legacy_fields": ("lambda_em",),
        "external_dependencies": (),
        "claim_level": "SPECTRAL_CLASSIFICATION",
    },
    "color_predictor": {
        "legacy_fields": ("lambda_em",),
        "external_dependencies": (),
        "claim_level": "DISPLAY_CLASSIFICATION",
    },
    "pump_predictor": {
        "legacy_fields": ("lambda_abs", "phi", "eta", "tau"),
        "external_dependencies": ("stability_score", "laser_sources"),
        "claim_level": "HEURISTIC_PUMP_SELECTION",
    },
    "laser_physics_engine": {
        "legacy_fields": ("lambda_em", "refractive_index"),
        "external_dependencies": (),
        "claim_level": "DERIVED_PHYSICS",
    },
    "spectral_quality_engine": {
        "legacy_fields": ("phi", "tau", "sigma_a", "knr"),
        "external_dependencies": (),
        "claim_level": "HEURISTIC_SCORE",
    },
    "lsi_engine": {
        "legacy_fields": (
            "phi", "tau", "sigma_a", "eta", "knr", "refractive_index"
        ),
        "external_dependencies": (),
        "claim_level": "HEURISTIC_SCORE",
    },
    "gain_analysis": {
        "legacy_fields": ("phi", "tau", "eta", "knr"),
        "external_dependencies": ("stability_score",),
        "claim_level": "HEURISTIC_SCORE",
    },
    "feasibility_engine": {
        "legacy_fields": ("phi", "tau", "knr"),
        "external_dependencies": ("lsi_value", "pump_source"),
        "claim_level": "HEURISTIC_SCORE",
    },
    "thermal_engine": {
        "legacy_fields": ("phi", "tau", "knr", "refractive_index"),
        "external_dependencies": (),
        "claim_level": "HEURISTIC_SCORE",
    },
    "photobleaching_engine": {
        "legacy_fields": ("phi", "knr"),
        "external_dependencies": ("thermal_score", "feasibility_score"),
        "claim_level": "HEURISTIC_SCORE",
    },
    "operation_mode_engine": {
        "legacy_fields": ("knr",),
        "external_dependencies": ("thermal_score", "feasibility_score"),
        "claim_level": "HEURISTIC_MODE",
    },
    "qfactor_engine": {
        "legacy_fields": ("refractive_index",),
        "external_dependencies": (
            "gain_score", "thermal_score", "photobleaching_score"
        ),
        "claim_level": "HEURISTIC_SCORE",
    },
    "gain_ranking_engine": {
        "legacy_fields": ("phi",),
        "external_dependencies": (
            "lsi_value", "feasibility_score", "thermal_score",
            "photobleaching_score"
        ),
        "claim_level": "HEURISTIC_SCORE",
    },
    "efficiency_engine": {
        "legacy_fields": ("phi",),
        "external_dependencies": (
            "gain_score", "q_factor_score", "beam_quality_score",
            "thermal_score"
        ),
        "claim_level": "HEURISTIC_SCORE",
    },
    "material_score_engine": {
        "legacy_fields": (),
        "external_dependencies": (
            "lsi", "thermal_score", "q_factor_score", "beam_quality_score",
            "laser_efficiency_score", "spectral_quality"
        ),
        "claim_level": "HEURISTIC_SCORE",
    },
    "lri_engine": {
        "legacy_fields": (),
        "external_dependencies": (
            "thermal_score", "q_factor_score", "laser_efficiency_score",
            "beam_quality_score", "feasibility_score"
        ),
        "claim_level": "HEURISTIC_SCORE",
    },
    "final_decision_engine": {
        "legacy_fields": (),
        "external_dependencies": (
            "material_score", "lri_score", "physics_consistency_score"
        ),
        "claim_level": "DECISION_SUPPORT",
    },
    "laserstone_governor": {
        "legacy_fields": (),
        "external_dependencies": (
            "intelligence_score", "system_integrity_score",
            "scientific_confidence_score", "research_novelty_score",
            "patent_potential_score"
        ),
        "claim_level": "ADVANCED_DECISION_SUPPORT",
    },
}


def audit_engine_compatibility(
    normalized: Mapping[str, Any],
    available_external: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Audit reviewed engine compatibility for one normalized evidence record."""
    physical = analyze_physical_spectral_evidence(normalized)
    legacy = assess_photochemcad_for_legacy(normalized)
    available_external = dict(available_external or {})

    safe_map = legacy["safe_legacy_map"]
    results = {}

    for engine, spec in ENGINE_REQUIREMENTS.items():
        missing_legacy = [
            field for field in spec["legacy_fields"] if field not in safe_map
        ]
        missing_external = [
            field
            for field in spec["external_dependencies"]
            if field not in available_external
            or available_external.get(field) is None
        ]

        if engine == "physical_spectral_evidence_engine":
            status = "READY"
            reason = "NORMALIZED_EVIDENCE_SUPPORTED"
        elif missing_legacy or missing_external:
            status = "BLOCKED"
            reason = "MISSING_OR_UNSAFE_REQUIRED_INPUTS"
        else:
            status = "READY_WITHIN_DECLARED_SCOPE"
            reason = "ALL_REVIEWED_INPUTS_AVAILABLE"

        results[engine] = {
            "status": status,
            "reason": reason,
            "claim_level": spec["claim_level"],
            "missing_or_unsafe_legacy_fields": missing_legacy,
            "missing_external_dependencies": missing_external,
        }

    ready = sorted(
        engine for engine, result in results.items()
        if result["status"].startswith("READY")
    )
    blocked = sorted(
        engine for engine, result in results.items()
        if result["status"] == "BLOCKED"
    )

    return {
        "photochemcad_id": physical["photochemcad_id"],
        "compound_name": physical["compound_name"],
        "physical_evidence_status": physical["evidence_status"],
        "physical_evidence_completeness_score": physical[
            "evidence_completeness_score"
        ],
        "ready_engines": ready,
        "blocked_engines": blocked,
        "engine_results": results,
        "policy": "NO_FABRICATED_INPUTS",
    }
