"""Tests for the isolated equation contract; not a validation of physical reality."""
import math
import unittest

from cloud.equation_contract import AttenuationRequest, Quantity, calculate_attenuation


def q(value, unit, source="hypothetical teaching input", state="SIMULATED"):
    return Quantity(value=value, unit=unit, source=source, evidence_state=state)


def request(alpha=0.5, depth=2, intensity=10):
    return AttenuationRequest(
        wavelength_nm=q(632.8, "nm"),
        incident_mw_cm2=q(intensity, "mW/cm2"),
        depth_cm=q(depth, "cm"),
        alpha_inv_cm=q(alpha, "cm^-1"),
    )


class EquationContractTests(unittest.TestCase):
    def test_reference_value_and_status(self):
        result = calculate_attenuation(request())
        self.assertAlmostEqual(result.relative_transmission, math.exp(-1))
        self.assertAlmostEqual(result.transmitted_mw_cm2, 10 * math.exp(-1))
        self.assertEqual(result.evidence_state, "SIMULATED")
        self.assertFalse(result.validated_experimentally)
        self.assertEqual(len(result.input_provenance), 4)

    def test_zero_depth_and_zero_attenuation(self):
        self.assertEqual(calculate_attenuation(request(depth=0)).relative_transmission, 1)
        self.assertEqual(calculate_attenuation(request(alpha=0)).relative_transmission, 1)

    def test_reject_invalid_inputs(self):
        for bad in (
            request(alpha=-0.1),
            request(depth=-1),
            request(intensity=-1),
            request(alpha=float("nan")),
            request(alpha=float("inf")),
        ):
            with self.assertRaises(ValueError):
                calculate_attenuation(bad)

    def test_reject_missing_source_and_unit_mismatch(self):
        base = request()
        for bad_alpha in (q(0.5, "cm^-1", source=""), q(0.5, "mm^-1")):
            with self.assertRaises(ValueError):
                calculate_attenuation(AttenuationRequest(
                    base.wavelength_nm, base.incident_mw_cm2, base.depth_cm, bad_alpha
                ))


if __name__ == "__main__":
    unittest.main()
