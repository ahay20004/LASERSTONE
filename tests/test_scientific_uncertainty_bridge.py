import unittest
from scientific_uncertainty_bridge import evaluate_with_uncertainty

class BridgeTests(unittest.TestCase):
    def test_photon(self):
        r = evaluate_with_uncertainty("photon_energy_wavelength",
            {"vacuum_wavelength":{"value":532,"unit":"nm"}},
            {"vacuum_wavelength":{"value":1,"unit":"nm"}},
            independent=True, output_unit="eV")
        self.assertEqual(r["result"]["display_value"],"2.3305")
        self.assertEqual(r["result"]["display_uncertainty"],"0.0044")
        self.assertLess(float(r["sensitivities_si"]["vacuum_wavelength"]),0)
        self.assertFalse(r["scientific_validation"])

    def test_missing_assumption(self):
        with self.assertRaises(ValueError):
            evaluate_with_uncertainty("vacuum_frequency",
                {"vacuum_wavelength":{"value":532,"unit":"nm"}},
                {"vacuum_wavelength":{"value":1,"unit":"nm"}})
