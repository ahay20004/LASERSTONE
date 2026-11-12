"""Legacy plant-data provenance audit for LASERSTONE G23.

This module does not alter legacy plant values. It identifies where field-level
sources, units, and reference reconciliation are still required before legacy
numbers can be promoted as physical evidence.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Iterable, Mapping

from database.plant_identity import resolve_plant_name
from database.plant_references import PLANT_REFERENCES
from g23_unit_contracts import UNIT_CONTRACTS, UNRESOLVED
from plants_data import plants as LEGACY_PLANTS

CRITICAL_LEGACY_FIELDS = (
    "phi",
    "tau",
    "sigma_a",
    "eta",
    "knr",
    "refractive_index",
    "lambda_abs",
    "lambda_em",
)


def build_reference_index() -> dict[str, list[dict[str, Any]]]:
    index: dict[str, list[dict[str, Any]]] = {}

    for source_key, reference in PLANT_REFERENCES.items():
        canonical = resolve_plant_name(source_key)
        item = deepcopy(reference)
        item["source_key"] = source_key
        item["canonical_name"] = canonical
        index.setdefault(canonical, []).append(item)

    return index


def _reference_has_doi(reference: Mapping[str, Any]) -> bool:
    text = " ".join(
        str(value)
        for value in reference.values()
        if value is not None
    ).lower()
    return "doi.org/" in text or "doi:" in text


def audit_legacy_plant(record: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(record, Mapping):
        raise TypeError("record must be a mapping")

    canonical = resolve_plant_name(str(record.get("name", "")).strip())
    reference_index = build_reference_index()
    references = reference_index.get(canonical, [])

    field_audit = {}
    for field in CRITICAL_LEGACY_FIELDS:
        contract = UNIT_CONTRACTS.get(field)
        value_present = field in record and record.get(field) is not None

        if not value_present:
            state = "MISSING"
        elif contract is None:
            state = "NO_UNIT_CONTRACT"
        elif contract["status"] == UNRESOLVED:
            state = "VALUE_PRESENT_UNIT_UNRESOLVED"
        else:
            state = "VALUE_PRESENT_UNIT_RESOLVED_SOURCE_NOT_FIELD_LINKED"

        field_audit[field] = {
            "state": state,
            "value_present": value_present,
            "unit_contract": deepcopy(contract),
            "field_level_reference": None,
        }

    if not references:
        reference_status = "NO_REFERENCE_RECORD"
    elif len(references) == 1:
        reference_status = "REFERENCE_RECORD_PRESENT_NOT_FIELD_LINKED"
    else:
        reference_status = "MULTIPLE_REFERENCE_RECORDS_REQUIRE_RECONCILIATION"

    unresolved_units = [
        field
        for field, info in field_audit.items()
        if info["state"] == "VALUE_PRESENT_UNIT_UNRESOLVED"
    ]

    return {
        "name": record.get("name"),
        "scientific_name": record.get("scientific_name"),
        "canonical_name": canonical,
        "reference_status": reference_status,
        "reference_count": len(references),
        "references": deepcopy(references),
        "any_reference_with_doi": any(
            _reference_has_doi(reference) for reference in references
        ),
        "field_audit": field_audit,
        "unresolved_unit_fields": unresolved_units,
        "field_level_provenance_complete": False,
        "promotion_status": "PROVENANCE_UPGRADE_REQUIRED",
    }


def audit_all_legacy_plants(
    records: Iterable[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    records = LEGACY_PLANTS if records is None else list(records)
    audits = [audit_legacy_plant(record) for record in records]

    return {
        "total_records": len(audits),
        "records_with_reference": sum(
            audit["reference_count"] > 0 for audit in audits
        ),
        "records_without_reference": sum(
            audit["reference_count"] == 0 for audit in audits
        ),
        "records_with_multiple_references": sum(
            audit["reference_count"] > 1 for audit in audits
        ),
        "records_with_any_doi": sum(
            audit["any_reference_with_doi"] for audit in audits
        ),
        "records_field_level_provenance_complete": sum(
            audit["field_level_provenance_complete"] for audit in audits
        ),
        "audits": audits,
        "status": "LEGACY_PROVENANCE_AUDIT_COMPLETE",
    }
