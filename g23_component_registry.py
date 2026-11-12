"""Non-invasive registry of G23 evidence-integration components.

This registry is separate from PROJECT_REGISTRY until production promotion is
approved. It prevents experimental evidence components from being counted as
production engines prematurely.
"""

from __future__ import annotations

from copy import deepcopy

G23_COMPONENT_REGISTRY = {
    "photochemcad_evidence_adapter": {
        "status": "EXPERIMENTAL_VERIFIED",
        "role": "External Evidence Normalization",
        "production_promoted": False,
        "inputs": ["verified_photochemcad_record"],
        "outputs": ["normalized_evidence_record"],
    },
    "photochemcad_integration_gate": {
        "status": "EXPERIMENTAL_VERIFIED",
        "role": "Legacy Compatibility Gate",
        "production_promoted": False,
        "inputs": ["normalized_evidence_record"],
        "outputs": ["safe_legacy_map", "integration_blockers"],
    },
    "physical_spectral_evidence_engine": {
        "status": "EXPERIMENTAL_VERIFIED",
        "role": "Physical Spectral Evidence Analysis",
        "production_promoted": False,
        "inputs": ["normalized_evidence_record"],
        "outputs": [
            "evidence_completeness_score",
            "physical_spectral_capabilities",
            "derived_stokes_shift",
        ],
    },
    "spectral_path_comparison": {
        "status": "EXPERIMENTAL_VERIFIED",
        "role": "Legacy/Physical Diagnostic Comparison",
        "production_promoted": False,
        "inputs": ["normalized_evidence_record"],
        "outputs": ["path_comparison_report"],
    },
    "g23_scientific_missing_policy": {
        "status": "EXPERIMENTAL_VERIFIED",
        "role": "Missing Data Safety Policy",
        "production_promoted": False,
        "inputs": ["scientific_record"],
        "outputs": ["strict_numeric_validation"],
    },
    "g23_unit_contracts": {
        "status": "EXPERIMENTAL_VERIFIED",
        "role": "Scientific Unit Contract Registry",
        "production_promoted": False,
        "inputs": ["field_name"],
        "outputs": ["unit_contract", "mapping_assessment"],
    },
    "g23_engine_compatibility_audit": {
        "status": "EXPERIMENTAL_VERIFIED",
        "role": "Evidence-to-Engine Compatibility",
        "production_promoted": False,
        "inputs": ["normalized_evidence_record", "available_external_inputs"],
        "outputs": ["engine_compatibility_report"],
    },
    "g23_evidence_registry": {
        "status": "EXPERIMENTAL_VERIFIED",
        "role": "Central Evidence Registry",
        "production_promoted": False,
        "inputs": ["normalized_evidence_record"],
        "outputs": ["evidence_snapshot", "evidence_statistics"],
    },
    "g23_evidence_decision_gate": {
        "status": "EXPERIMENTAL_VERIFIED",
        "role": "Fail-Closed Evidence Decision Gate",
        "production_promoted": False,
        "inputs": ["normalized_evidence_record", "engine_compatibility_report"],
        "outputs": ["allowed_actions", "blocked_claims"],
    },
    "g23_data_standardization_engine": {
        "status": "EXPERIMENTAL_VERIFIED",
        "role": "Strict Data Standardization",
        "production_promoted": False,
        "inputs": ["raw_quality_value"],
        "outputs": ["standardized_value", "standardization_status"],
    },
    "g23_strict_decision_path": {
        "status": "EXPERIMENTAL_VERIFIED",
        "role": "Strict Legacy Decision Wrappers",
        "production_promoted": False,
        "inputs": ["complete_heuristic_score_record"],
        "outputs": ["strict_heuristic_decision_outputs"],
    },
    "g23_evidence_interpretation_engine": {
        "status": "EXPERIMENTAL_VERIFIED",
        "role": "Evidence-Aware Interpretation",
        "production_promoted": False,
        "inputs": ["normalized_evidence_record"],
        "outputs": ["evidence_bounded_interpretation"],
    },
    "g23_evidence_trace_engine": {
        "status": "EXPERIMENTAL_VERIFIED",
        "role": "Evidence Traceability",
        "production_promoted": False,
        "inputs": ["normalized_evidence_record"],
        "outputs": ["provenance_trace"],
    },
    "g23_evidence_output_engine": {
        "status": "EXPERIMENTAL_VERIFIED",
        "role": "Evidence-Safe Output Representation",
        "production_promoted": False,
        "inputs": ["normalized_evidence_record"],
        "outputs": ["derived_spectral_output", "blocked_output_claims"],
    },
    "g23_legacy_provenance_audit": {
        "status": "EXPERIMENTAL_VERIFIED",
        "role": "Legacy Data Provenance Audit",
        "production_promoted": False,
        "inputs": ["legacy_plant_record", "legacy_reference_registry"],
        "outputs": ["provenance_gap_report", "reference_reconciliation_flags"],
    },
}


def component_registry_snapshot() -> dict:
    return deepcopy(G23_COMPONENT_REGISTRY)


def promotion_candidates() -> list[str]:
    """Return components technically staged but not production-promoted."""
    return sorted(
        name
        for name, info in G23_COMPONENT_REGISTRY.items()
        if info["status"] == "EXPERIMENTAL_VERIFIED"
        and info["production_promoted"] is False
    )
