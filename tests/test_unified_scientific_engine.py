import unittest
from unified_scientific_engine import evaluate

class UnifiedEngineTests(unittest.TestCase):
    def test_reference_cases(self):
        cases = [
            ("vacuum_frequency", {"vacuum_wavelength":{"value":532,"unit":"nm"}}, "THz", 563.5196578947368),
            ("photon_energy", {"frequency":{"value":500,"unit":"THz"}}, "eV", 2.067833848461929),
            ("photon_energy_wavelength", {"vacuum_wavelength":{"value":532,"unit":"nm"}}, "eV", 2.330530045736847),
            ("linear_cavity_fsr", {"group_index":{"value":1.5,"unit":"1"},"cavity_length":{"value":10,"unit":"cm"}}, "GHz", 0.9993081933333333),
        ]
        for identifier, inputs, unit, expected in cases:
            with self.subTest(identifier=identifier):
                r = evaluate(identifier,inputs,unit)
                self.assertAlmostEqual(float(r["result"]["raw_value"]),expected,places=8)
                self.assertEqual(r["result"]["uncertainty_status"],"unknown")
                self.assertFalse(r["scientific_validation"])
                self.assertFalse(r["model_conditions_verified"])

    def test_rejection(self):
        for value,unit in [(0,"nm"),(-1,"nm"),(True,"nm"),(532,"kg")]:
            with self.subTest(value=value,unit=unit):
                with self.assertRaises((ValueError,KeyError)):
                    evaluate("vacuum_frequency",{"vacuum_wavelength":{"value":value,"unit":unit}})
        with self.assertRaises(ValueError):
            evaluate("vacuum_frequency",{})
