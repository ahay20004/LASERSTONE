"""Compatibility gate between PhotochemCAD evidence and legacy LASERSTONE fields.

The gate is intentionally non-promoting: it exposes only mappings whose
semantics are documented, keeps physical absorption cross section in its own
unit-bearing field, and blocks legacy scientific execution while required
quantities or unit contracts remain unresolved.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from photochemcad_evidence_adapter import DERIVED, MISSING, REPORTED

LEGACY_SCIENTIFIC_FIELDS = (
    "phi",
    "tau",
    "sigma_a",
    "eta",
    "knr",
    "refractive_index",
    "lambda_abs",
    "lambda_em",
)

SAFE_FIELD_MAP = {
    "phi_f": "phi",
    "lambda_abs_nm": "lambda_abs",
    "lambda_em_nm": "lambda_em",
}

SIGMA_BLOCKER = (
    "Legacy LASERSTONE sigma_a unit/normalization is undocumented; "
    "PhotochemCAD sigma_a_cm2 must remain separate until a unit contract is defined."
)


def assess_photochemcad_for_legacy(
    normalized: Mapping[str, Any],
) -> dict[str, Any]:
    """Assess a normalized PhotochemCAD record for safe legacy field mapping.

    The function never mutates the source and never writes to production
    registries. A value is mapped only when its source field is explicitly
    marked LITERATURE_REPORTED. Derived sigma_a_cm2 is retained separately
    and is never copied into the legacy sigma_a field.
    """
    if not isinstance(normalized, Mapping):
        raise TypeError("normalized must be a mapping")

    source = deepcopy(dict(normalized))
    if source.get("source_database") != "PhotochemCAD":
        raise ValueError("source_database must be PhotochemCAD")

    evidence = source.get("field_evidence")
    if not isinstance(evidence, Mapping):
        raise ValueError("field_evidence mapping is required")

    safe_legacy_map: dict[str, float] = {}
    mapping_provenance: dict[str, dict[str, str]] = {}

    for source_field, legacy_field in SAFE_FIELD_MAP.items():
        value = source.get(source_field)
        state = evidence.get(source_field, MISSING)
        if value is not None and state == REPORTED:
            safe_legacy_map[legacy_field] = float(value)
            mapping_provenance[legacy_field] = {
                "source_field": source_field,
                "evidence_state": REPORTED,
                "source_database": "PhotochemCAD",
            }

    physical_sigma = source.get("sigma_a_cm2")
    sigma_state = evidence.get("sigma_a_cm2", MISSING)
    physical_evidence = {
        "sigma_a_cm2": (
            float(physical_sigma)
            if physical_sigma is not None and sigma_state == DERIVED
            else None
        ),
        "unit": "cm^2 molecule^-1",
        "evidence_state": sigma_state,
        "derivation_method": source.get("derivation_method"),
    }

    unresolved = [
        field for field in LEGACY_SCIENTIFIC_FIELDS
        if field not in safe_legacy_map
    ]

    blockers = []
    if physical_evidence["sigma_a_cm2"] is not None:
        blockers.append(SIGMA_BLOCKER)

    if unresolved:
        blockers.append(
            "Legacy scientific execution requires unresolved fields: "
            + ", ".join(unresolved)
        )

    status = "SAFE_PARTIAL_MAP_ONLY" if safe_legacy_map else "EVIDENCE_ONLY"
    promotable = not blockers and not unresolved
    if not promotable:
        status = "BLOCKED_FROM_LEGACY_EXECUTION"

    return {
        "status": status,
        "promotable_to_legacy_scientific_pipeline": promotable,
        "photochemcad_id": source.get("photochemcad_id"),
        "compound_name": source.get("compound_name"),
        "safe_legacy_map": safe_legacy_map,
        "mapping_provenance": mapping_provenance,
        "physical_evidence": physical_evidence,
        "unresolved_legacy_fields": unresolved,
        "blockers": blockers,
        "source_url": source.get("source_url"),
    }
