"""Acceptance tests for the LASERSTONE research-composition entry gates."""

import json
import unittest
from pathlib import Path

from g23_research_directive import (
    EXPECTED_MASTER_POLICY,
    validate_research_directive,
)
from g23_research_novelty_gate import (
    AUTHORIZED,
    INSUFFICIENT,
    PROMISING,
    REVIEW_REQUIRED,
    assess_research_novelty_gate,
)


ROOT = Path(__file__).resolve().parent


def load_json(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


class ResearchDirectiveTests(unittest.TestCase):
    def test_paper1_directive_is_valid(self):
        directive = load_json("LASERSTONE_PAPER1_DIRECTIVE.json")
        result = validate_research_directive(directive)
        self.assertTrue(result["valid"])
        self.assertEqual(result["composition_status"], "DIRECTIVE_VALIDATED")
        self.assertEqual(result["master_policy"], EXPECTED_MASTER_POLICY)

    def test_missing_scientific_gap_blocks_directive(self):
        directive = load_json("LASERSTONE_PAPER1_DIRECTIVE.json")
        directive["scientific_gap"] = ""
        result = validate_research_directive(directive)
        self.assertFalse(result["valid"])
        self.assertEqual(result["composition_status"], "DIRECTIVE_BLOCKED")

    def test_multiple_master_policy_is_rejected(self):
        directive = load_json("LASERSTONE_PAPER1_DIRECTIVE.json")
        directive["master_policy"] = "MULTIPLE_DRAFTS"
        result = validate_research_directive(directive)
        self.assertFalse(result["valid"])


class ResearchNoveltyGateTests(unittest.TestCase):
    def test_prior_art_review_is_required(self):
        directive = load_json("LASERSTONE_PAPER1_DIRECTIVE.json")
        result = assess_research_novelty_gate(
            directive,
            {"review_status": "NOT_REVIEWED"},
        )
        self.assertEqual(result["status"], REVIEW_REQUIRED)
        self.assertFalse(result["authorized"])

    def test_direct_competitor_without_distinct_contribution_blocks_composition(self):
        directive = load_json("LASERSTONE_PAPER1_DIRECTIVE.json")
        prior = {
            "review_status": "REVIEWED",
            "search_scope_documented": True,
            "direct_competitor_found": True,
            "distinct_contribution_supported": False,
            "evidence_sufficient_for_current_claims": True,
        }
        result = assess_research_novelty_gate(directive, prior)
        self.assertEqual(result["status"], INSUFFICIENT)
        self.assertFalse(result["authorized"])

    def test_promising_but_evidence_incomplete_does_not_compose(self):
        directive = load_json("LASERSTONE_PAPER1_DIRECTIVE.json")
        prior = {
            "review_status": "REVIEWED",
            "search_scope_documented": True,
            "direct_competitor_found": False,
            "distinct_contribution_supported": True,
            "evidence_sufficient_for_current_claims": False,
        }
        result = assess_research_novelty_gate(directive, prior)
        self.assertEqual(result["status"], PROMISING)
        self.assertFalse(result["authorized"])

    def test_paper1_is_authorized_only_with_bounded_review_and_evidence(self):
        directive = load_json("LASERSTONE_PAPER1_DIRECTIVE.json")
        prior = load_json("LASERSTONE_PAPER1_PRIOR_ART.json")
        result = assess_research_novelty_gate(directive, prior)
        self.assertEqual(result["status"], AUTHORIZED)
        self.assertTrue(result["authorized"])
        self.assertEqual(
            result["novelty_basis"],
            "PRIOR_ART_COMPARISON_NOT_MATERIAL_PERFORMANCE",
        )


if __name__ == "__main__":
    unittest.main()
