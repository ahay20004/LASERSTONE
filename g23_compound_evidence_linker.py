"""Safe linker between legacy plant records and isolated-compound evidence.

A compound match is supporting evidence only. It never authorizes replacing
plant-extract measurements with isolated-compound values.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Iterable, Mapping


def _canonical_compound_name(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    text = " ".join(value.strip().lower().split())
    return text or None


def link_plant_to_compound_evidence(
    plant: Mapping[str, Any],
    evidence_records: Iterable[Mapping[str, Any]],
) -> dict[str, Any]:
    if not isinstance(plant, Mapping):
        raise TypeError("plant must be a mapping")

    active_compound = _canonical_compound_name(plant.get("active_compound"))
    if active_compound is None:
        return {
            "plant_name": plant.get("name"),
            "active_compound": plant.get("active_compound"),
            "status": "NO_ACTIVE_COMPOUND_IDENTITY",
            "matches": [],
            "substitution_allowed": False,
        }

    matches = []
    for record in evidence_records:
        if not isinstance(record, Mapping):
            continue
        compound_name = _canonical_compound_name(record.get("compound_name"))
        if compound_name == active_compound:
            matches.append(deepcopy(dict(record)))

    if not matches:
        status = "NO_EXACT_COMPOUND_EVIDENCE_MATCH"
    elif len(matches) == 1:
        status = "SUPPORTING_COMPOUND_EVIDENCE_ONLY"
    else:
        status = "MULTIPLE_COMPOUND_RECORDS_REVIEW_REQUIRED"

    return {
        "plant_name": plant.get("name"),
        "scientific_name": plant.get("scientific_name"),
        "active_compound": plant.get("active_compound"),
        "status": status,
        "matches": matches,
        "match_count": len(matches),
        "substitution_allowed": False,
        "allowed_use": [
            "compound-level spectral reference",
            "hypothesis generation",
            "comparison target for future extract measurements",
        ],
        "prohibited_use": [
            "replace plant-extract lambda_abs",
            "replace plant-extract lambda_em",
            "replace plant-extract quantum yield",
            "replace plant-extract lifetime",
            "claim plant-extract laser gain from isolated compound evidence",
        ],
        "scientific_boundary": (
            "Isolated-compound evidence and plant-extract evidence are "
            "different evidence objects and must remain distinct."
        ),
    }
