"""Synthetic tests for theory-to-evidence review bridge."""
import importlib.util
from pathlib import Path
import unittest

p = Path(__file__).resolve().parents[1] / "theory_evidence_bridge.py"
spec = importlib.util.spec_from_file_location("theory_evidence_bridge", p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def proposal():
    return {
        "theory_id": "SYN-T1", "title": "Synthetic model", "original_equation": "y=x",
        "proposed_equation": "y=x+epsilon", "modification_rationale": "Software test",
        "assumptions": ["epsilon finite"], "domain_of_validity": ["synthetic"],
        "observables": ["y"], "falsifiable_predictions": ["epsilon tends to zero"],
        "source_references": ["synthetic"], "author": "test", "version": "0.1",
    }

class BridgeTests(unittest.TestCase):
    def test_no_evidence_creates_review_plan(self):
        r = mod.build_bridge(proposal())
        self.assertEqual(r["stage"], "PROPOSED")
        self.assertTrue(all(x["status"] == "NOT_SUBMITTED" for x in r["evidence_review"].values()))
        self.assertEqual(r["claims_authorized"], [])

    def test_submitted_evidence_not_verified(self):
        evidence = {"reference_limit": {"artifact_id": "SYN-A", "method": "synthetic limit",
                                        "outcome": "self-reported pass"}}
        r = mod.build_bridge(proposal(), evidence)
        self.assertEqual(r["evidence_review"]["reference_limit"]["status"], "SUBMITTED_FOR_INDEPENDENT_REVIEW")
        self.assertEqual(r["endorsement"], "NONE")

    def test_unknown_check_rejected(self):
        with self.assertRaises(ValueError):
            mod.build_bridge(proposal(), {"prove_lasing": {}})

    def test_incomplete_evidence_rejected(self):
        with self.assertRaises(ValueError):
            mod.build_bridge(proposal(), {"reference_limit": {"artifact_id": "A"}})

    def test_proposal_hash_stable(self):
        self.assertEqual(mod.build_bridge(proposal())["proposal_sha256"],
                         mod.build_bridge(proposal())["proposal_sha256"])

if __name__ == "__main__":
    unittest.main()
