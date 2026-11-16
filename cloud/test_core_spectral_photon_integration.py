"""Real integration tests for two existing scientific modules."""
import unittest

from cloud.core_spectral_photon_integration import (
    SpectralPhotonRequest, evaluate_spectral_photon,
)


class SpectralPhotonIntegrationTests(unittest.TestCase):
    def test_independent_si_benchmark_and_legacy_labels(self):
        for wavelength, label in ((532.0, "Visible"),
                                  (632.8, "Visible"),
                                  (1064.0, "Near Infrared (NIR)")):
            with self.subTest(wavelength=wavelength):
                result = evaluate_spectral_photon(SpectralPhotonRequest(wavelength))
                self.assertEqual(result["spectral_label"], label)
                self.assertTrue(result["integration_passed"])
                self.assertFalse(result["experimental_validation"])
                self.assertFalse(result["cloud_service"])
                self.assertEqual(result["photon"]["wavelength_nm"], wavelength)
                self.assertTrue(all(v["within_tolerance"]
                                    for v in result["photon"]["comparisons"].values()))

    def test_legacy_visible_boundary_is_explicit(self):
        self.assertEqual(evaluate_spectral_photon(
            SpectralPhotonRequest(750))["spectral_label"], "Visible")
        self.assertEqual(evaluate_spectral_photon(
            SpectralPhotonRequest(750.01))["spectral_label"], "Near Infrared (NIR)")

    def test_refractive_index_is_not_photon_energy(self):
        a = evaluate_spectral_photon(SpectralPhotonRequest(532, 1))
        b = evaluate_spectral_photon(SpectralPhotonRequest(532, 1.5))
        self.assertEqual(a["photon"]["comparisons"]["photon_energy_ev"]["legacy_value"],
                         b["photon"]["comparisons"]["photon_energy_ev"]["legacy_value"])

    def test_out_of_scope_inputs_rejected(self):
        for wavelength in (0, -1, 379.99, 1100.01, float("nan"), float("inf"), True):
            with self.subTest(wavelength=wavelength):
                with self.assertRaises(ValueError):
                    evaluate_spectral_photon(SpectralPhotonRequest(wavelength))
        with self.assertRaises(ValueError):
            evaluate_spectral_photon(SpectralPhotonRequest(532, 0))
        with self.assertRaises(TypeError):
            evaluate_spectral_photon({"wavelength_nm": 532})


if __name__ == "__main__":
    unittest.main()
