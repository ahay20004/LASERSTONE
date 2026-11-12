"""Provenance-first scientific trace for LASERSTONE G23 evidence records."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from g23_evidence_decision_gate import assess_evidence_decision_gate
from physical_spectral_evidence_engine import analyze_physical_spectral_evidence


def generate_evidence_trace(normalized: Mapping[str, Any]) -> dict[str, Any]:
    analysis = analyze_physical_spectral_evidence(normalized)
    gate = assess_evidence_decision_gate(normalized)

    trace = {
        "identity": {
            "photochemcad_id": analysis["photochemcad_id"],
            "compound_name": analysis["compound_name"],
            "source_database": analysis["source_database"],
            "source_url": analysis["source_url"],
        },
        "evidence": {
            "reported_core_fields": list(analysis["reported_core_fields"]),
            "missing_core_fields": list(analysis["missing_core_fields"]),
            "completeness_score": analysis["evidence_completeness_score"],
            "evidence_status": analysis["evidence_status"],
        },
        "derived": {
            "sigma_a_cm2": analysis["sigma_a_cm2"],
            "sigma_a_unit": analysis["sigma_a_unit"],
            "stokes_shift_nm": analysis["stokes_shift_nm"],
            "stokes_shift_cm_inv": analysis["stokes_shift_cm_inv"],
        },
        "decision_gate": {
            "status": gate["status"],
            "allowed_actions": deepcopy(gate["allowed_actions"]),
            "advanced_claims": deepcopy(gate["advanced_claims"]),
            "blocked_legacy_decision_engines": list(
                gate["blocked_legacy_decision_engines"]
            ),
        },
        "trace_status": "TRACEABLE_EVIDENCE_RECORD",
        "prototype_decision": "NOT_AUTHORIZED_FROM_THIS_EVIDENCE",
    }

    return trace
