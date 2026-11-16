"""Independent bounded regression of the existing laser physics callable."""
import unittest
from cloud.legacy_laser_photon_adapter import LaserPhotonRequest, evaluate_legacy_laser_photon


class LegacyPhotonAdapterTests(unittest.TestCase):
    def test_reference_wavelengths(self):
        for wavelength in (532.0, 632.8, 1064.0):
            with self.subTest(wavelength=wavelength):
                result = evaluate_legacy_laser_photon(LaserPhotonRequest(wavelength))
                self.assertTrue(result["benchmark_passed"])
                self.assertFalse(result["validated_experimentally"])
                self.assertFalse(result["cloud_connected"])
                self.assertEqual(result["scope"], "PHOTON_FREQUENCY_ENERGY_ONLY")
                self.assertTrue(all(v["relative_error"] < 0.001
                                    for v in result["comparisons"].values()))

    def test_refractive_index_does_not_change_photon_energy(self):
        a = evaluate_legacy_laser_photon(LaserPhotonRequest(632.8, 1.0))
        b = evaluate_legacy_laser_photon(LaserPhotonRequest(632.8, 1.5))
        self.assertEqual(a["comparisons"]["photon_energy_ev"]["legacy_value"],
                         b["comparisons"]["photon_energy_ev"]["legacy_value"])

    def test_invalid_inputs_rejected(self):
        for wavelength in (0, -1, float("nan"), float("inf"), True, 99, 100001):
            with self.subTest(wavelength=wavelength):
                with self.assertRaises(ValueError):
                    evaluate_legacy_laser_photon(LaserPhotonRequest(wavelength))
        for index in (0, float("nan"), 0.9, 5.1):
            with self.subTest(index=index):
                with self.assertRaises(ValueError):
                    evaluate_legacy_laser_photon(LaserPhotonRequest(532, index))
        with self.assertRaises(TypeError):
            evaluate_legacy_laser_photon({"wavelength_nm": 532})


if __name__ == "__main__":
    unittest.main()
