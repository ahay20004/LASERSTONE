"""G23 SRC-01 regression checks for the existing laser physics engine.

These tests verify arithmetic and document known model limitations.
They do NOT certify physical validity or authorize publication.
Run from the repository root:
    python -m unittest -v test_g23_laser_physics.py
"""
import math
import unittest

from laser_physics_engine import calculate_laser_physics


class LaserPhysicsSRC01Tests(unittest.TestCase):
    def test_photon_frequency_and_energy_reference_cases(self):
        # Values independently calculated from the constants in the legacy code.
        cases = [
            (532.0, 563.9097744360902e12, 2.332375883529047),
            (632.8, 474.0834386852086e12, 1.9608469817279601),
            (1064.0, 281.9548872180451e12, 1.1661879417645236),
        ]
        for wavelength_nm, expected_f, expected_e in cases:
            with self.subTest(wavelength_nm=wavelength_nm):
                result = calculate_laser_physics(
                    {"lambda_em": wavelength_nm, "refractive_index": 1.33}
                )
                self.assertTrue(math.isclose(
                    result["frequency_hz"], expected_f, rel_tol=1e-10
                ))
                self.assertTrue(math.isclose(
                    result["photon_energy_ev"], expected_e, rel_tol=2e-6
                ))

    def test_special_cavity_assumption_not_independent_design(self):
        # For L=lambda/(2*n), the returned FSR is algebraically c/lambda.
        # This is an explicit limitation, NOT a validation of cavity design.
        for n in (1.0, 1.33, 1.5):
            with self.subTest(refractive_index=n):
                result = calculate_laser_physics(
                    {"lambda_em": 632.8, "refractive_index": n}
                )
                self.assertTrue(math.isclose(
                    result["free_spectral_range_hz"],
                    result["frequency_hz"],
                    rel_tol=1e-12,
                ))

    def test_nonpositive_wavelength_returns_legacy_zero_sentinel(self):
        # Characterization only: a future validated API should reject invalid input.
        for wavelength_nm in (0, -1):
            with self.subTest(wavelength_nm=wavelength_nm):
                result = calculate_laser_physics({"lambda_em": wavelength_nm})
                self.assertEqual(result["frequency_hz"], 0)
                self.assertEqual(result["photon_energy_ev"], 0)

    @unittest.expectedFailure
    def test_invalid_refractive_index_should_be_rejected(self):
        # Expected failure tracks the existing input-validation defect.
        with self.assertRaises((ValueError, TypeError)):
            calculate_laser_physics(
                {"lambda_em": 632.8, "refractive_index": 0}
            )


if __name__ == "__main__":
    unittest.main()
