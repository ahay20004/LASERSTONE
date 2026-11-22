"""Synthetic theory-incubator registration tests."""
import importlib.util
from pathlib import Path
import unittest

p = Path(__file__).resolve().parents[1] / "theory_incubator.py"
spec = importlib.util.spec_from_file_location("theory_incubator", p)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def proposal():
    return {
        "theory_id": "SYN-HYP-01", "title": "Synthetic attenuation correction",
        "original_equation": "I=I0 exp(-alpha d)",
        "proposed_equation": "I=I0 exp(-alpha d)*(1+epsilon*d)",
        "modification_rationale": "Synthetic hypothesis for software tests",
        "assumptions": ["epsilon*d small"],
        "domain_of_validity": ["hypothetical uniform medium"],
        "observables": ["transmitted intensity"],
        "falsifiable_predictions": ["difference from reference model at known thickness"],
        "source_references": ["synthetic-only"],
        "author": "test-fixture", "version": "0.1",
    }

class TheoryIncubatorTests(unittest.TestCase):
    def test_proposal_preserved_without_endorsement(self):
        r = module.register(proposal())
        self.assertEqual(r["stage"], "PROPOSED")
        self.assertEqual(r["endorsement"], "NONE")
        self.assertEqual(r["claims_authorized"], [])
        self.assertTrue(all(v == "NOT_RUN" for v in r["checks"].values()))

    def test_stable_hash(self):
        self.assertEqual(module.register(proposal())["proposal_sha256"],
                         module.register(proposal())["proposal_sha256"])

    def test_missing_prediction_rejected(self):
        d = proposal()
        d["falsifiable_predictions"] = []
        with self.assertRaises(ValueError):
            module.register(d)

    def test_empty_reference_equation_rejected(self):
        d = proposal()
        d["original_equation"] = ""
        with self.assertRaises(ValueError):
            module.register(d)

    def test_non_object_rejected(self):
        with self.assertRaises(ValueError):
            module.register("theory")

if __name__ == "__main__":
    unittest.main()
