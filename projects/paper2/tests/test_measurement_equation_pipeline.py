"""Synthetic end-to-end measurement-to-equation integration checks."""
import importlib.util
from pathlib import Path
import math
import unittest

root = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("measurement_equation_pipeline", root / "measurement_equation_pipeline.py")
pipeline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline)

def measurement(role, quantity, value, unit, uncertainty):
    return {"measurement_id": "SYN-" + role, "quantity": quantity, "value": value,
            "unit": unit, "uncertainty": uncertainty, "uncertainty_type": "standard",
            "instrument_id": "synthetic-device", "calibration_reference": "synthetic-cal",
            "sample_id": "synthetic-sample", "conditions": {"temperature_K": 300},
            "source_id": "synthetic-source", "method": "synthetic",
            "equation_id": "beer-lambert"}

def records():
    return {
        "incident_power": measurement("power", "optical_power", 1000, "mW", 10),
        "absorption_coefficient": measurement("alpha", "absorption_coefficient", 1, "1/cm", 0.02),
        "thickness": measurement("thickness", "sample_thickness", 1, "mm", 0.01),
        "wavelength": measurement("wavelength", "wavelength", 632.8, "nm", 0.1),
    }

def regime():
    return {"thickness_m": 0.001, "wavelength_m": 632.8e-9,
            "homogeneous": True, "scattering_negligible": True,
            "interface_reflections_accounted": True,
            "coherent_interference_negligible": True,
            "bulk_optical_constants_valid": True,
            "layer_stack_characterized": None, "complex_indices_available": None}

class MeasurementEquationPipelineTests(unittest.TestCase):
    def test_mixed_units_normalize_and_predict(self):
        r = pipeline.evaluate(records(), regime())
        self.assertEqual(r["status"], "COMPUTED_MODEL_CONDITIONAL")
        self.assertAlmostEqual(r["result"]["transmitted_power_W"], math.exp(-0.1))
        self.assertEqual(r["traceability"]["thickness"]["measurement_id"], "SYN-thickness")
        self.assertEqual(r["claims_authorized"], [])

    def test_wrong_unit_blocks_intake(self):
        rs = records()
        rs["thickness"]["unit"] = "W"
        self.assertEqual(pipeline.evaluate(rs, regime())["status"], "BLOCKED_INTAKE")

    def test_wrong_sample_blocks(self):
        rs = records()
        rs["absorption_coefficient"]["sample_id"] = "another-sample"
        self.assertEqual(pipeline.evaluate(rs, regime())["status"], "BLOCKED_CONTEXT_MISMATCH")

    def test_different_conditions_block(self):
        rs = records()
        rs["incident_power"]["conditions"]["temperature_K"] = 310
        self.assertEqual(pipeline.evaluate(rs, regime())["status"], "BLOCKED_CONTEXT_MISMATCH")

    def test_expanded_uncertainty_not_silently_used(self):
        rs = records()
        rs["incident_power"]["uncertainty_type"] = "expanded"
        rs["incident_power"]["coverage_factor"] = 2
        with self.assertRaises(ValueError):
            pipeline.evaluate(rs, regime())

    def test_regime_wavelength_mismatch_rejected(self):
        r = regime()
        r["wavelength_m"] = 532e-9
        with self.assertRaises(ValueError):
            pipeline.evaluate(records(), r)

    def test_interference_blocks_calculation(self):
        r = regime()
        r["coherent_interference_negligible"] = False
        result = pipeline.evaluate(records(), r)
        self.assertEqual(result["status"], "BLOCKED_MODEL_NOT_APPLICABLE")
        self.assertIsNone(result["result"])

    def test_wrong_quantity_role_rejected(self):
        rs = records()
        rs["thickness"]["quantity"] = "wavelength"
        with self.assertRaises(ValueError):
            pipeline.evaluate(rs, regime())

if __name__ == "__main__":
    unittest.main()
