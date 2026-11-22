"""Cross-stage synthetic integration regression for Stages 3.7–4.1."""
import importlib.util
from pathlib import Path
import sys
import unittest

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))

import evidence_uncertainty_audit as uncertainty
import independent_evidence_gate as independent
import scientific_claims_gate as claims
import integrated_validation_dashboard as dashboard
import scientific_dashboard_ui as ui


class ClosureIntegrationTests(unittest.TestCase):
    def make_chain(self):
        proposal = {"theory_id": "synthetic-closure", "version": "1",
                    "proposal_sha256": "synthetic-proposal"}
        unified = {**proposal, "audit_sha256": "synthetic-audit",
                   "checks": {"dimensional_consistency": "NOT_RUN"}}
        observation = {
            "observable": "synthetic power", "unit": "W",
            "prediction": 1.0, "prediction_standard_uncertainty": 0.1,
            "measurement": 0.9, "measurement_standard_uncertainty": 0.1,
            "source_id": "synthetic-source", "instrument_id": "synthetic-instrument",
            "calibration_id": "synthetic-calibration",
            "conditions_id": "synthetic-condition",
        }
        compared = uncertainty.bind_report(unified, [observation])
        review = {
            "evidence_id": "synthetic-evidence", "source_id": "synthetic-source",
            "artifact_sha256": "a" * 64, "submitter_id": "synthetic-author",
            "reviewer_id": None, "review_artifact_sha256": None,
            "review_scope": None, "review_outcome": None,
            "reviewer_independence_attestation": False,
        }
        reviewed = independent.bind_to_evidence_report(compared, [review])
        claim = {
            "claim_id": "synthetic-claim", "claim_text": "Synthetic hypothesis",
            "claim_type": "THEORETICAL", "evidence_ids": ["synthetic-evidence"],
            "equation_ids": ["synthetic-eq"], "conditions_ids": ["synthetic-condition"],
            "limitations": "No experimental validation",
            "novelty_reference_ids": ["synthetic-reference"],
        }
        assessed = claims.assess(reviewed, [claim])
        return {"unified": unified, "uncertainty": compared,
                "independent_review": reviewed, "claims": assessed}

    def test_full_chain_to_html_preserves_nonendorsement(self):
        result = dashboard.build(self.make_chain())
        html = ui.render(result)
        self.assertIn("synthetic-closure", html)
        self.assertIn("NOT ESTABLISHED", html)
        self.assertEqual(result["claims_authorized"], [])
        self.assertIn("unified:INCOMPLETE_OR_NONPASS_CHECKS", result["gaps"])
        self.assertIn("independent_review:INCOMPLETE_REVIEW_METADATA", result["gaps"])

    def test_broken_evidence_hash_rejected(self):
        chain = self.make_chain()
        chain["independent_review"]["evidence_input_sha256"] = "altered"
        with self.assertRaises(ValueError):
            dashboard.build(chain)

    def test_broken_review_hash_rejected(self):
        chain = self.make_chain()
        chain["claims"]["review_input_sha256"] = "altered"
        with self.assertRaises(ValueError):
            dashboard.build(chain)

    def test_mismatched_theory_rejected(self):
        chain = self.make_chain()
        chain["claims"]["version"] = "other"
        with self.assertRaises(ValueError):
            dashboard.build(chain)

    def test_reviewer_attestation_does_not_authorize_claim(self):
        chain = self.make_chain()
        self.assertEqual(chain["claims"]["publication_readiness"], "NOT_ESTABLISHED")
        self.assertEqual(chain["claims"]["claim_assessments"][0]["claims_authorized"], [])


if __name__ == "__main__":
    unittest.main()
