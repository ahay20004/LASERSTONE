"""Fail-closed decision gate for external spectral evidence in LASERSTONE G23.

The gate separates actions supported by evidence from claims that require
additional experimental or validated model evidence.
"""

from __future__ import annotations

from typing import Any, Mapping

from g23_engine_compatibility_audit import audit_engine_compatibility
from g23_unit_contracts import unresolved_legacy_contracts
from physical_spectral_evidence_engine import analyze_physical_spectral_evidence


ADVANCED_CLAIMS = (
    "laser_gain_established",
    "lasing_feasibility_established",
    "prototype_readiness_established",
    "laser_efficiency_established",
    "q_factor_established",
)


def assess_evidence_decision_gate(
    normalized: Mapping[str, Any],
    available_external: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Return evidence-supported actions and blocked claim classes."""
    physical = analyze_physical_spectral_evidence(normalized)
    compatibility = audit_engine_compatibility(
        normalized,
        available_external=available_external,
    )

    capabilities = physical["capabilities"]
    actions = {
        "store_traceable_evidence": True,
        "analyze_absorption_peak": capabilities["absorption_peak_available"],
        "use_quantitative_absorption": capabilities[
            "quantitative_absorption_available"
        ],
        "analyze_fluorescence_peak": capabilities[
            "fluorescence_peak_available"
        ],
        "use_fluorescence_quantum_yield": capabilities[
            "fluorescence_quantum_yield_available"
        ],
        "derive_stokes_shift": capabilities["stokes_shift_available"],
        "classify_spectral_region": (
            compatibility["engine_results"]["spectral_region"]["status"]
            .startswith("READY")
        ),
        "classify_display_color": (
            compatibility["engine_results"]["color_predictor"]["status"]
            .startswith("READY")
        ),
    }

    advanced_claims = {claim: False for claim in ADVANCED_CLAIMS}

    legacy_decision_engines = (
        "spectral_quality_engine",
        "lsi_engine",
        "gain_analysis",
        "feasibility_engine",
        "thermal_engine",
        "photobleaching_engine",
        "qfactor_engine",
        "efficiency_engine",
        "material_score_engine",
        "lri_engine",
        "final_decision_engine",
        "laserstone_governor",
    )

    blocked_legacy = [
        engine
        for engine in legacy_decision_engines
        if compatibility["engine_results"][engine]["status"] == "BLOCKED"
    ]

    return {
        "photochemcad_id": physical["photochemcad_id"],
        "compound_name": physical["compound_name"],
        "status": "EVIDENCE_ANALYSIS_READY_LEGACY_DECISION_BLOCKED",
        "evidence_completeness_score": physical[
            "evidence_completeness_score"
        ],
        "evidence_status": physical["evidence_status"],
        "allowed_actions": actions,
        "advanced_claims": advanced_claims,
        "blocked_legacy_decision_engines": blocked_legacy,
        "unresolved_legacy_unit_contracts": unresolved_legacy_contracts(),
        "decision_basis": "TRACEABLE_EVIDENCE_ONLY",
        "policy": "NO_ADVANCED_CLAIM_FROM_SPECTRAL_EVIDENCE_ALONE",
    }
