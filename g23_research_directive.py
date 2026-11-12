"""Research Directive validation for LASERSTONE manuscript composition.

This module validates whether a research directive contains the minimum
scientific information required before novelty assessment or manuscript
composition may proceed.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

REQUIRED_TEXT_FIELDS = (
    "research_id",
    "master_policy",
    "title",
    "article_type",
    "domain",
    "research_question",
    "scientific_gap",
    "claim_boundary",
    "manuscript_structure",
    "status",
)

REQUIRED_LIST_FIELDS = (
    "proposed_contribution",
    "evidence_scope",
    "excluded_claims",
    "application_relevance",
    "future_research_path",
)

EXPECTED_MASTER_POLICY = "ONE_RESEARCH_ONE_MASTER_ONE_EVIDENCE_TRAIL"


def validate_research_directive(
    directive: Mapping[str, Any],
) -> dict[str, Any]:
    if not isinstance(directive, Mapping):
        raise TypeError("directive must be a mapping")

    source = deepcopy(dict(directive))
    errors: list[str] = []

    for field in REQUIRED_TEXT_FIELDS:
        value = source.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{field}: nonempty text required")

    for field in REQUIRED_LIST_FIELDS:
        value = source.get(field)
        if (
            not isinstance(value, list)
            or not value
            or any(not isinstance(item, str) or not item.strip() for item in value)
        ):
            errors.append(f"{field}: nonempty list of text items required")

    if source.get("master_policy") != EXPECTED_MASTER_POLICY:
        errors.append(
            "master_policy must enforce ONE_RESEARCH_ONE_MASTER_ONE_EVIDENCE_TRAIL"
        )

    if source.get("manuscript_structure") != "IMRAD":
        errors.append("manuscript_structure must be IMRAD for Paper 1")

    benchmark_results = source.get("benchmark_results")
    if not isinstance(benchmark_results, Mapping) or not benchmark_results:
        errors.append("benchmark_results: nonempty mapping required")

    return {
        "valid": not errors,
        "errors": errors,
        "research_id": source.get("research_id"),
        "title": source.get("title"),
        "composition_status": (
            "DIRECTIVE_VALIDATED"
            if not errors
            else "DIRECTIVE_BLOCKED"
        ),
        "master_policy": source.get("master_policy"),
    }
