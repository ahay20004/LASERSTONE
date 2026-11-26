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


    def test_cavity_uncertainty(self):
        from math import sqrt
        inputs = {"group_index":{"value":1.5,"unit":"1"},
                  "cavity_length":{"value":10,"unit":"cm"}}
        uncertainties = {"group_index":{"value":0.01,"unit":"1"},
                         "cavity_length":{"value":0.1,"unit":"cm"}}
        expected = 299792458/(2*1.5*0.1)
        for rho in (-1,0,1):
            matrix = {i:{j:1 if i==j else rho for j in inputs} for i in inputs}
            r = evaluate_with_uncertainty("linear_cavity_fsr",inputs,uncertainties,
                                          correlation=matrix,output_unit="GHz")
            target = expected*sqrt((0.01/1.5)**2+0.01**2+2*rho*(0.01/1.5)*0.01)
            self.assertAlmostEqual(r["uncertainty_analysis"]["standard_uncertainty"]/expected,
                                   target/expected,places=12)
        r = evaluate_with_uncertainty("linear_cavity_fsr",inputs,uncertainties,independent=True)
        self.assertAlmostEqual(r["uncertainty_analysis"]["standard_uncertainty"]/expected,
                               sqrt((0.01/1.5)**2+0.01**2),places=12)
