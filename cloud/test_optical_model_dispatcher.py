"""Tests of physics selection and refusal of unsupported regimes."""
import unittest

from cloud.material_registry_gate import OpticalRecord
from cloud.optical_model_dispatcher import (
    OpticalScenario, UnsupportedOpticalRegime, dispatch_optical_model,
)

RECORDS = (OpticalRecord(
    material_id="synthetic_sample",
    wavelength_nm=632.8,
    alpha_inv_cm=0.5,
    source="synthetic test fixture, not laboratory evidence",
    evidence_state="DERIVED",
    applicable_depth_cm=(0, 5),
),)


def scenario(**changes):
    values = dict(
        material_id="synthetic_sample",
        wavelength_nm=632.8,
        incident_mw_cm2=10,
        depth_cm=2,
        regime="bulk_absorption",
        homogeneous=True,
        constant_alpha=True,
        interface_effects_negligible=True,
    )
    values.update(changes)
    return OpticalScenario(**values)


class OpticalModelDispatcherTests(unittest.TestCase):
    def test_supported_model_uses_material_gate(self):
        result = dispatch_optical_model(scenario(), RECORDS)
        self.assertEqual(result.model_id, "beer_lambert_uniform_absorption_v1")
        self.assertEqual(result.evidence_state, "SIMULATED")
        self.assertFalse(result.validated_experimentally)

    def test_refuse_unimplemented_physics(self):
        for regime in (
            "interface_reflection", "thin_film_interference",
            "polarization_anisotropy", "multiple_scattering", "nonlinear_optics",
        ):
            with self.subTest(regime=regime):
                with self.assertRaises(UnsupportedOpticalRegime):
                    dispatch_optical_model(scenario(regime=regime), RECORDS)

    def test_refuse_unconfirmed_assumptions(self):
        for assumption in (
            "homogeneous", "constant_alpha", "interface_effects_negligible",
        ):
            with self.subTest(assumption=assumption):
                with self.assertRaises(UnsupportedOpticalRegime):
                    dispatch_optical_model(scenario(**{assumption: False}), RECORDS)

    def test_material_gate_remains_authoritative(self):
        with self.assertRaises(ValueError):
            dispatch_optical_model(scenario(wavelength_nm=532), RECORDS)
        with self.assertRaises(ValueError):
            dispatch_optical_model(scenario(depth_cm=6), RECORDS)


if __name__ == "__main__":
    unittest.main()
