"""Synthetic tests for Stage 3.4 audit registry binding."""
import importlib.util
from pathlib import Path
import unittest

path = Path(__file__).resolve().parents[1] / "theory_audit_pipeline.py"
spec = importlib.util.spec_from_file_location("theory_audit_pipeline", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def proposal():
    return {
        "theory_id": "synthetic-1", "title": "Synthetic equation",
        "original_equation": "E=h*c/lambda",
        "proposed_equation": "E=h*c/lambda",
        "modification_rationale": "Testing only",
        "assumptions": ["vacuum"], "domain_of_validity": ["synthetic"],
        "observables": ["energy"], "falsifiable_predictions": ["synthetic"],
        "source_references": ["synthetic test reference"], "author": "Test",
        "version": "0.1",
    }

def dimensions():
    return {
        "symbols": {"E": {"M": 1, "L": 2, "T": -2},
                    "h": {"M": 1, "L": 2, "T": -1},
                    "c": {"L": 1, "T": -1},
                    "lambda": {"L": 1}},
        "lhs_terms": [{"E": 1}],
        "rhs_terms": [{"h": 1, "c": 1, "lambda": -1}],
    }

def limit():
    return {
        "parameter": "epsilon", "limit_value": 0,
        "absolute_tolerance": 0.001, "relative_tolerance": 0,
        "samples": [
            {"parameter_value": 0.1, "reference_value": 1, "modified_value": 1.1},
            {"parameter_value": 0.01, "reference_value": 1, "modified_value": 1.01},
            {"parameter_value": 0.0001, "reference_value": 1, "modified_value": 1.0001},
        ],
    }

class PipelineTests(unittest.TestCase):
    def test_both_checks_bound_to_proposal(self):
        r = mod.run_audit(proposal(), dimensions(), limit())
        self.assertEqual(r["checks"]["dimensional_consistency"], "DIMENSIONALLY_CONSISTENT")
        self.assertEqual(r["checks"]["limiting_cases"], "NUMERICAL_LIMIT_COMPATIBLE")
        self.assertEqual(r["stage"], "PROPOSED")
        self.assertEqual(r["endorsement"], "NONE")
        self.assertEqual(r["claims_authorized"], [])

    def test_deterministic_hashes(self):
        self.assertEqual(mod.run_audit(proposal(), dimensions(), limit())["audit_sha256"],
                         mod.run_audit(proposal(), dimensions(), limit())["audit_sha256"])

    def test_proposal_change_changes_identity(self):
        p = proposal()
        a = mod.run_audit(p, dimensions())["proposal_sha256"]
        p["version"] = "0.2"
        b = mod.run_audit(p, dimensions())["proposal_sha256"]
        self.assertNotEqual(a, b)

    def test_failure_preserved_without_promotion(self):
        d = dimensions()
        d["rhs_terms"] = [{"h": 1, "c": 1, "lambda": 1}]
        r = mod.run_audit(proposal(), d)
        self.assertEqual(r["checks"]["dimensional_consistency"], "DIMENSIONAL_MISMATCH")
        self.assertEqual(r["stage"], "PROPOSED")

    def test_no_inputs_rejected(self):
        with self.assertRaises(ValueError):
            mod.run_audit(proposal())

    def test_unrun_checks_preserved(self):
        r = mod.run_audit(proposal(), dimensions())
        self.assertEqual(r["checks"]["limiting_cases"], "NOT_RUN")

if __name__ == "__main__":
    unittest.main()
