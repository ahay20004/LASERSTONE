"""Synthetic integration tests for unified Stage 3.6 reporting."""
import importlib.util
from pathlib import Path
import unittest

root = Path(__file__).resolve().parents[1]
def load(name):
    spec = importlib.util.spec_from_file_location(name, root / (name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

report = load("unified_theory_report")

def proposal():
    return {
        "theory_id": "synthetic-theory", "title": "Synthetic model",
        "original_equation": "E=h*c/lambda", "proposed_equation": "E=h*c/lambda",
        "modification_rationale": "Synthetic test",
        "assumptions": ["synthetic"], "domain_of_validity": ["synthetic"],
        "observables": ["energy"], "falsifiable_predictions": ["synthetic"],
        "source_references": ["synthetic reference"], "author": "Test", "version": "0.1",
    }

def dimensions():
    return {
        "symbols": {"E": {"M": 1, "L": 2, "T": -2},
                    "h": {"M": 1, "L": 2, "T": -1},
                    "c": {"L": 1, "T": -1}, "lambda": {"L": 1}},
        "lhs_terms": [{"E": 1}],
        "rhs_terms": [{"h": 1, "c": 1, "lambda": -1}],
    }

def limit():
    return {"parameter": "epsilon", "limit_value": 0,
            "absolute_tolerance": 0.001, "relative_tolerance": 0,
            "samples": [
                {"parameter_value": 0.1, "reference_value": 1, "modified_value": 1.1},
                {"parameter_value": 0.01, "reference_value": 1, "modified_value": 1.01},
                {"parameter_value": 0.0001, "reference_value": 1, "modified_value": 1.0001},
            ]}

def convergence():
    return {"absolute_tolerance": 0.02, "relative_tolerance": 0,
            "samples": [
                {"resolution_scale": 0.1, "value": 1.1},
                {"resolution_scale": 0.05, "value": 1.02},
                {"resolution_scale": 0.025, "value": 1.001},
            ]}

def sensitivity():
    return {"parameter": "alpha", "baseline_parameter": 2,
            "baseline_output": 4,
            "lower": {"parameter_value": 1.9, "output_value": 3.8},
            "upper": {"parameter_value": 2.1, "output_value": 4.2}}

class UnifiedTests(unittest.TestCase):
    def test_four_audits_bound(self):
        r = report.build_report(proposal(), dimensions(), limit(), convergence(), sensitivity())
        self.assertEqual(r["summary"]["executed"], 4)
        self.assertEqual(r["summary"]["requires_investigation"], 0)
        self.assertEqual(r["stage"], "PROPOSED")
        self.assertEqual(r["endorsement"], "NONE")
        self.assertEqual(r["claims_authorized"], [])

    def test_not_run_preserved(self):
        r = report.build_report(proposal(), dimensions=dimensions())
        self.assertEqual(r["checks"]["limiting_cases"], "NOT_RUN")
        self.assertEqual(r["checks"]["parameter_sensitivity"], "NOT_RUN")

    def test_failure_preserved(self):
        d = dimensions()
        d["rhs_terms"] = [{"h": 1, "c": 1, "lambda": 1}]
        r = report.build_report(proposal(), dimensions=d)
        self.assertEqual(r["summary"]["requires_investigation"], 1)
        self.assertEqual(r["checks"]["dimensional_consistency"], "DIMENSIONAL_MISMATCH")

    def test_hash_stability(self):
        a = report.build_report(proposal(), dimensions=dimensions())
        b = report.build_report(proposal(), dimensions=dimensions())
        self.assertEqual(a["audit_sha256"], b["audit_sha256"])

    def test_proposal_version_binding(self):
        p = proposal()
        a = report.build_report(p, dimensions=dimensions())
        p["version"] = "0.2"
        b = report.build_report(p, dimensions=dimensions())
        self.assertNotEqual(a["proposal_sha256"], b["proposal_sha256"])

    def test_empty_rejected(self):
        with self.assertRaises(ValueError):
            report.build_report(proposal())

if __name__ == "__main__":
    unittest.main()
