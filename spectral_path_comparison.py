"""Diagnostic comparison between legacy and physical spectral paths.

The outputs are intentionally non-equivalent:
- legacy spectral quality is a heuristic category based on legacy fields;
- physical evidence completeness is a provenance-aware coverage metric.

This module never converts one into the other.
"""

from __future__ import annotations

from typing import Any, Mapping

from photochemcad_integration_gate import assess_photochemcad_for_legacy
from physical_spectral_evidence_engine import analyze_physical_spectral_evidence

LEGACY_SPECTRAL_REQUIRED_FIELDS = ("phi", "tau", "sigma_a", "knr")

NON_EQUIVALENT = "NON_EQUIVALENT_OUTPUTS_DO_NOT_RANK_AGAINST_EACH_OTHER"


def compare_spectral_paths(
    normalized: Mapping[str, Any],
) -> dict[str, Any]:
    """Compare path readiness for one normalized PhotochemCAD record."""
    physical = analyze_physical_spectral_evidence(normalized)
    legacy_gate = assess_photochemcad_for_legacy(normalized)

    safe_map = legacy_gate["safe_legacy_map"]
    missing_for_legacy_spectral = [
        field
        for field in LEGACY_SPECTRAL_REQUIRED_FIELDS
        if field not in safe_map
    ]

    if missing_for_legacy_spectral:
        legacy_status = "LEGACY_SPECTRAL_ENGINE_BLOCKED_MISSING_OR_UNSAFE_FIELDS"
        legacy_quality = None
    else:
        # This branch is deliberately unreachable for current PhotochemCAD
        # integration because legacy sigma_a is not unit-safe. Keeping the
        # result blocked avoids accidental use if mappings change elsewhere.
        legacy_status = "LEGACY_SPECTRAL_ENGINE_REQUIRES_EXPLICIT_REVIEW"
        legacy_quality = None

    return {
        "photochemcad_id": physical["photochemcad_id"],
        "compound_name": physical["compound_name"],
        "physical_path_status": "AVAILABLE",
        "physical_evidence_completeness_score": physical[
            "evidence_completeness_score"
        ],
        "physical_evidence_status": physical["evidence_status"],
        "legacy_path_status": legacy_status,
        "legacy_spectral_quality": legacy_quality,
        "legacy_safe_fields_available": sorted(safe_map.keys()),
        "legacy_spectral_required_fields": list(LEGACY_SPECTRAL_REQUIRED_FIELDS),
        "legacy_spectral_missing_or_unsafe_fields": missing_for_legacy_spectral,
        "comparison_status": NON_EQUIVALENT,
        "comparison_note": (
            "Physical evidence completeness measures documented data coverage; "
            "legacy spectral quality is a heuristic material category. "
            "They are not the same quantity and must not be numerically ranked."
        ),
        "laser_claim_status": physical["laser_gain_status"],
        "source_url": physical["source_url"],
    }
