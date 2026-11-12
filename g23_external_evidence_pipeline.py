"""Unified G23 external-evidence pipeline for LASERSTONE.

The pipeline coordinates evidence-safe components without invoking the legacy
laser-scoring or prototype-decision chain.
"""

from __future__ import annotations

from typing import Any, Iterable, Mapping

from g23_compound_evidence_linker import link_plant_to_compound_evidence
from g23_engine_compatibility_audit import audit_engine_compatibility
from g23_evidence_decision_gate import assess_evidence_decision_gate
from g23_evidence_interpretation_engine import generate_evidence_interpretation
from g23_evidence_output_engine import generate_evidence_output
from g23_evidence_registry import EvidenceRegistry
from g23_evidence_trace_engine import generate_evidence_trace
from photochemcad_evidence_adapter import normalize_photochemcad_record
from physical_spectral_evidence_engine import analyze_physical_spectral_evidence


def process_photochemcad_evidence(
    raw_record: Mapping[str, Any],
    *,
    registry: EvidenceRegistry | None = None,
    legacy_plants: Iterable[Mapping[str, Any]] | None = None,
    available_external: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Process one PhotochemCAD record through the complete evidence-safe path."""
    normalized = normalize_photochemcad_record(raw_record)
    registry = EvidenceRegistry() if registry is None else registry

    registry_entry = registry.add(normalized)
    physical = analyze_physical_spectral_evidence(normalized)
    compatibility = audit_engine_compatibility(
        normalized,
        available_external=available_external,
    )
    decision_gate = assess_evidence_decision_gate(
        normalized,
        available_external=available_external,
    )
    interpretation = generate_evidence_interpretation(normalized)
    trace = generate_evidence_trace(normalized)
    output = generate_evidence_output(normalized)

    plant_links = []
    if legacy_plants is not None:
        for plant in legacy_plants:
            link = link_plant_to_compound_evidence(plant, [normalized])
            if link.get("match_count", 0) > 0:
                plant_links.append(link)

    return {
        "pipeline_status": "EVIDENCE_SAFE_COMPLETE",
        "normalized_evidence": normalized,
        "registry_entry": registry_entry,
        "physical_analysis": physical,
        "engine_compatibility": compatibility,
        "decision_gate": decision_gate,
        "interpretation": interpretation,
        "trace": trace,
        "output": output,
        "legacy_plant_links": plant_links,
        "legacy_scoring_invoked": False,
        "production_registry_mutated": False,
        "advanced_claims_authorized": False,
    }


def process_photochemcad_batch(
    raw_records: Iterable[Mapping[str, Any]],
    *,
    legacy_plants: Iterable[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Process a batch through one shared evidence registry."""
    registry = EvidenceRegistry()
    packages = [
        process_photochemcad_evidence(
            raw,
            registry=registry,
            legacy_plants=legacy_plants,
        )
        for raw in raw_records
    ]

    return {
        "pipeline_status": "EVIDENCE_SAFE_BATCH_COMPLETE",
        "record_count": len(packages),
        "packages": packages,
        "registry_statistics": registry.statistics(),
        "registry_snapshot": registry.snapshot(),
        "legacy_scoring_invoked": False,
        "production_registry_mutated": False,
    }
