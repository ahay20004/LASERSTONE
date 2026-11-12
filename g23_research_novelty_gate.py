"""Evidence-aware novelty gate for LASERSTONE research composition.

The gate does not infer novelty from material-performance scores. Novelty is
assessed from a structured prior-art review plus a clearly stated scientific
gap and distinct contribution.
"""

from __future__ import annotations

from typing import Any, Mapping

from g23_research_directive import validate_research_directive

REVIEWED = "REVIEWED"

AUTHORIZED = "RESEARCH_COMPOSITION_AUTHORIZED"
PROMISING = "SCIENTIFICALLY_PROMISING_EVIDENCE_REQUIRED"
INSUFFICIENT = "NOVELTY_INSUFFICIENT_DO_NOT_COMPOSE"
REVIEW_REQUIRED = "PRIOR_ART_REVIEW_REQUIRED"


def assess_research_novelty_gate(
    directive: Mapping[str, Any],
    prior_art_assessment: Mapping[str, Any],
) -> dict[str, Any]:
    directive_check = validate_research_directive(directive)
    if not directive_check["valid"]:
        return {
            "status": "DIRECTIVE_BLOCKED",
            "authorized": False,
            "reasons": directive_check["errors"],
        }

    if not isinstance(prior_art_assessment, Mapping):
        raise TypeError("prior_art_assessment must be a mapping")

    if prior_art_assessment.get("review_status") != REVIEWED:
        return {
            "status": REVIEW_REQUIRED,
            "authorized": False,
            "reasons": ["Structured prior-art review has not been completed."],
        }

    direct_competitor_found = bool(
        prior_art_assessment.get("direct_competitor_found", False)
    )
    distinct_contribution = bool(
        prior_art_assessment.get("distinct_contribution_supported", False)
    )
    evidence_sufficient = bool(
        prior_art_assessment.get("evidence_sufficient_for_current_claims", False)
    )
    search_scope_documented = bool(
        prior_art_assessment.get("search_scope_documented", False)
    )

    reasons: list[str] = []

    if not search_scope_documented:
        return {
            "status": REVIEW_REQUIRED,
            "authorized": False,
            "reasons": ["Prior-art search scope is not documented."],
        }

    if direct_competitor_found and not distinct_contribution:
        return {
            "status": INSUFFICIENT,
            "authorized": False,
            "reasons": [
                "A direct competitor was identified and the directive does not "
                "yet demonstrate a distinct scientific contribution."
            ],
        }

    if not distinct_contribution:
        reasons.append(
            "Distinct contribution relative to reviewed prior art is not yet supported."
        )

    if not evidence_sufficient:
        reasons.append(
            "Current evidence is insufficient for all claims in the directive."
        )

    if reasons:
        return {
            "status": PROMISING,
            "authorized": False,
            "reasons": reasons,
        }

    return {
        "status": AUTHORIZED,
        "authorized": True,
        "reasons": [
            "Directive is complete.",
            "Prior-art scope is documented.",
            "Distinct contribution is supported relative to reviewed prior art.",
            "Evidence is sufficient for the current bounded claims.",
        ],
        "novelty_basis": "PRIOR_ART_COMPARISON_NOT_MATERIAL_PERFORMANCE",
        "claim_boundary": directive.get("claim_boundary"),
    }
