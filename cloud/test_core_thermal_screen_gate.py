"""Synthetic tests for bounded legacy thermal screening execution."""
import unittest
from cloud.core_thermal_screen_gate import (
    FIELDS, UNITS, ThermalInput, evaluate_thermal_screen,
)


def sample():
    values = {"phi": .8, "tau": 4.5, "knr": .3, "refractive_index": 1.35}
    return {name: ThermalInput(values[name], UNITS[name], "synthetic-only", "SIMULATED")
            for name in FIELDS}


class ThermalScreenTests(unittest.TestCase):
    def test_legacy_execution_and_independent_threshold_formula(self):
        result = evaluate_thermal_screen(sample())
        self.assertEqual(result["score"], 100)
        self.assertTrue(result["independent_formula_agreement"])
        self.assertFalse(result["physical_thermal_stability_validated"])
        self.assertFalse(result["experimentally_validated"])

    def test_missing_and_extra_fields_rejected(self):
        values = sample()
        del values["tau"]
        with self.assertRaises(ValueError):
            evaluate_thermal_screen(values)
        values = sample()
        values["temperature"] = ThermalInput(300, "K", "test", "MEASURED")
        with self.assertRaises(ValueError):
            evaluate_thermal_screen(values)

    def test_fail_closed_on_invalid_inputs(self):
        for name in FIELDS:
            for replacement in (
                ThermalInput(float("nan"), UNITS[name], "test", "MEASURED"),
                ThermalInput(True, UNITS[name], "test", "MEASURED"),
                ThermalInput(.5, "wrong", "test", "MEASURED"),
                ThermalInput(.5, UNITS[name], "", "MEASURED"),
                ThermalInput(.5, UNITS[name], "test", "UNKNOWN"),
                ThermalInput(-1, UNITS[name], "test", "MEASURED"),
            ):
                with self.subTest(name=name, replacement=replacement):
                    values = sample()
                    values[name] = replacement
                    with self.assertRaises(ValueError):
                        evaluate_thermal_screen(values)
        values = sample()
        values["phi"] = ThermalInput(1.1, "1", "test", "MEASURED")
        with self.assertRaises(ValueError):
            evaluate_thermal_screen(values)

    def test_threshold_boundary(self):
        values = sample()
        values["phi"] = ThermalInput(.5, "1", "test", "SIMULATED")
        result = evaluate_thermal_screen(values)
        self.assertEqual(result["score"], 90)


if __name__ == "__main__":
    unittest.main()
