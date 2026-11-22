"""Synthetic tests for measurement record intake; no instrument verification."""
import importlib.util
from pathlib import Path
import unittest

root = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("measurement_intake", root / "measurement_intake.py")
intake = importlib.util.module_from_spec(spec)
spec.loader.exec_module(intake)

def example():
    return {
        "measurement_id": "SYN-001", "quantity": "wavelength",
        "value": 632.8, "unit": "nm", "uncertainty": 0.1,
        "uncertainty_type": "standard", "instrument_id": "synthetic-spectrometer",
        "calibration_reference": "synthetic-calibration-only", "sample_id": "synthetic-sample",
        "conditions": {"temperature_K": 300}, "source_id": "synthetic-source",
        "method": "synthetic", "equation_id": "E=h*c/lambda",
    }

class MeasurementIntakeTests(unittest.TestCase):
    def test_valid_record_normalizes_si_but_does_not_prove_measurement(self):
        r = intake.validate(example())
        self.assertEqual(r["status"], "RECORD_ACCEPTED_FOR_REVIEW")
        self.assertAlmostEqual(r["normalized"]["value_si"], 632.8e-9)
        self.assertEqual(r["g3_evidence_types"], [])
        self.assertEqual(r["claims_authorized"], [])

    def test_wrong_dimension_unit_rejected(self):
        record = example()
        record["unit"] = "W"
        self.assertEqual(intake.validate(record)["status"], "REJECTED")

    def test_missing_calibration_rejected(self):
        record = example()
        record.pop("calibration_reference")
        self.assertEqual(intake.validate(record)["status"], "REJECTED")

    def test_nonfinite_rejected(self):
        record = example()
        record["value"] = float("nan")
        self.assertEqual(intake.validate(record)["status"], "REJECTED")

    def test_negative_uncertainty_rejected(self):
        record = example()
        record["uncertainty"] = -0.2
        self.assertEqual(intake.validate(record)["status"], "REJECTED")

    def test_unknown_quantity_rejected(self):
        record = example()
        record["quantity"] = "gain"
        self.assertEqual(intake.validate(record)["status"], "REJECTED")

    def test_expanded_uncertainty_requires_coverage_factor(self):
        record = example()
        record["uncertainty_type"] = "expanded"
        self.assertEqual(intake.validate(record)["status"], "REJECTED")
        record["coverage_factor"] = 2.0
        self.assertEqual(intake.validate(record)["status"], "RECORD_ACCEPTED_FOR_REVIEW")

    def test_boolean_value_rejected(self):
        record = example()
        record["value"] = True
        self.assertEqual(intake.validate(record)["status"], "REJECTED")

if __name__ == "__main__":
    unittest.main()
