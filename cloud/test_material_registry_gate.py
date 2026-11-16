"""Contract tests for optical material-property gate; synthetic fixtures only."""
import math
import unittest

from cloud.material_registry_gate import OpticalRecord, resolve_attenuation


def record(**overrides):
    values = dict(
        material_id="synthetic_sample",
        wavelength_nm=632.8,
        alpha_inv_cm=0.5,
        source="synthetic regression fixture; not experimental data",
        evidence_state="MEASURED",
        applicable_depth_cm=(0.0, 5.0),
    )
    values.update(overrides)
    return OpticalRecord(**values)


class MaterialRegistryGateTests(unittest.TestCase):
    def test_exact_record_calculation_remains_simulated(self):
        result = resolve_attenuation("synthetic_sample", 632.8, 10, 2, (record(),))
        self.assertAlmostEqual(result.relative_transmission, math.exp(-1))
        self.assertEqual(result.evidence_state, "SIMULATED")
        self.assertFalse(result.validated_experimentally)
        self.assertIn("synthetic regression", result.input_provenance["alpha_inv_cm"])

    def test_missing_and_ambiguous_wavelength_rejected(self):
        for records, wavelength in (
            ((), 632.8),
            ((record(),), 532.0),
            ((record(), record()), 632.8),
        ):
            with self.assertRaises(ValueError):
                resolve_attenuation("synthetic_sample", wavelength, 10, 2, records)

    def test_reject_invalid_evidence_or_source(self):
        for item in (
            record(source=""),
            record(evidence_state="PREDICTED"),
            record(evidence_state="SIMULATED"),
            record(alpha_inv_cm=-1),
            record(model="unknown"),
        ):
            with self.assertRaises(ValueError):
                resolve_attenuation("synthetic_sample", 632.8, 10, 2, (item,))

    def test_reject_out_of_range_and_invalid_ranges(self):
        for item, depth in (
            (record(), 6),
            (record(applicable_depth_cm=(3, 1)), 2),
            (record(applicable_depth_cm=(-1, 5)), 2),
        ):
            with self.assertRaises(ValueError):
                resolve_attenuation("synthetic_sample", 632.8, 10, depth, (item,))


if __name__ == "__main__":
    unittest.main()
