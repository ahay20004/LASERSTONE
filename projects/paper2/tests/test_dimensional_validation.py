"""Synthetic tests for explicit dimensional validation."""
import importlib.util
from pathlib import Path
import unittest

p = Path(__file__).resolve().parents[1] / "dimensional_validation.py"
spec = importlib.util.spec_from_file_location("dimensional_validation", p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def spec():
    return {"symbols": {
        "E": {"M": 1, "L": 2, "T": -2},
        "h": {"M": 1, "L": 2, "T": -1},
        "c": {"L": 1, "T": -1},
        "lambda": {"L": 1},
    }, "lhs_terms": [{"E": 1}], "rhs_terms": [{"h": 1, "c": 1, "lambda": -1}]}

class DimensionTests(unittest.TestCase):
    def test_photon_energy_dimensions_match(self):
        r = mod.assess(spec())
        self.assertEqual(r["status"], "DIMENSIONALLY_CONSISTENT")
        self.assertEqual(r["claims_authorized"], [])

    def test_wrong_wavelength_exponent_detected(self):
        d = spec()
        d["rhs_terms"] = [{"h": 1, "c": 1, "lambda": 1}]
        self.assertEqual(mod.assess(d)["status"], "DIMENSIONAL_MISMATCH")

    def test_inconsistent_addition_detected(self):
        d = spec()
        d["rhs_terms"].append({"c": 1})
        self.assertEqual(mod.assess(d)["status"], "DIMENSIONAL_MISMATCH")

    def test_unknown_symbol_fails(self):
        d = spec()
        d["rhs_terms"] = [{"unknown": 1}]
        with self.assertRaises(ValueError):
            mod.assess(d)

    def test_noninteger_power_fails(self):
        d = spec()
        d["rhs_terms"] = [{"lambda": 0.5}]
        with self.assertRaises(ValueError):
            mod.assess(d)

    def test_invalid_dimension_label_fails(self):
        d = spec()
        d["symbols"]["c"] = {"length": 1}
        with self.assertRaises(ValueError):
            mod.assess(d)

if __name__ == "__main__":
    unittest.main()
