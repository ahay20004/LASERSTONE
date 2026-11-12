"""Central evidence registry for LASERSTONE G23.

The registry stores normalized evidence records immutably by source identity,
tracks evidence completeness, and rejects conflicting duplicate records.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from physical_spectral_evidence_engine import analyze_physical_spectral_evidence


class EvidenceConflictError(ValueError):
    """Raised when the same evidence identity is re-used with different data."""


class EvidenceRegistry:
    """In-memory provenance registry for normalized evidence records."""

    def __init__(self) -> None:
        self._records: dict[str, dict[str, Any]] = {}

    @staticmethod
    def _key(record: Mapping[str, Any]) -> str:
        source = record.get("source_database")
        record_id = record.get("photochemcad_id")
        if source != "PhotochemCAD" or not isinstance(record_id, str) or not record_id:
            raise ValueError("normalized PhotochemCAD identity is required")
        return f"{source}:{record_id}"

    def add(self, record: Mapping[str, Any]) -> dict[str, Any]:
        """Add one normalized evidence record without mutating the source."""
        if not isinstance(record, Mapping):
            raise TypeError("record must be a mapping")

        candidate = deepcopy(dict(record))
        analysis = analyze_physical_spectral_evidence(candidate)
        key = self._key(candidate)

        envelope = {
            "evidence_key": key,
            "source_database": candidate["source_database"],
            "photochemcad_id": candidate["photochemcad_id"],
            "compound_name": candidate.get("compound_name"),
            "source_url": candidate.get("source_url"),
            "normalized_record": candidate,
            "physical_analysis": analysis,
        }

        if key in self._records:
            existing = self._records[key]
            if existing != envelope:
                raise EvidenceConflictError(
                    f"conflicting evidence already registered for {key}"
                )
            return deepcopy(existing)

        self._records[key] = envelope
        return deepcopy(envelope)

    def get(self, evidence_key: str) -> dict[str, Any] | None:
        record = self._records.get(evidence_key)
        return deepcopy(record) if record is not None else None

    def list_records(self) -> list[dict[str, Any]]:
        return [
            deepcopy(self._records[key])
            for key in sorted(self._records)
        ]

    def snapshot(self) -> dict[str, dict[str, Any]]:
        return deepcopy(self._records)

    def statistics(self) -> dict[str, Any]:
        records = list(self._records.values())
        if not records:
            return {
                "total_records": 0,
                "mean_evidence_completeness": None,
                "complete_core_records": 0,
                "partial_core_records": 0,
                "sparse_core_records": 0,
            }

        scores = [
            record["physical_analysis"]["evidence_completeness_score"]
            for record in records
        ]

        statuses = [
            record["physical_analysis"]["evidence_status"]
            for record in records
        ]

        return {
            "total_records": len(records),
            "mean_evidence_completeness": round(sum(scores) / len(scores), 2),
            "complete_core_records": statuses.count(
                "COMPLETE_CORE_SPECTRAL_EVIDENCE"
            ),
            "partial_core_records": statuses.count(
                "PARTIAL_CORE_SPECTRAL_EVIDENCE"
            ),
            "sparse_core_records": statuses.count(
                "SPARSE_CORE_SPECTRAL_EVIDENCE"
            ),
        }
