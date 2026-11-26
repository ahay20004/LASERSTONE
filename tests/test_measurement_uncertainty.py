import unittest
from measurement_uncertainty import propagate_independent

class UncertaintyTests(unittest.TestCase):
    def test_independent(self):
        r = propagate_independent({"a": 3, "b": -4}, {"a": 1, "b": 1}, independent=True)
        self.assertEqual(r["standard_uncertainty"], 5)
        self.assertFalse(r["scientific_validation"])

    def test_invalid(self):
        for s,u,ind in [({"a":1},{},True),({"a":1},{"a":-1},True),
                        ({"a":1},{"a":1},False),({"a":1},{"a":float("nan")},True),
                        ({"a":True},{"a":1},True)]:
            with self.subTest(s=s,u=u,ind=ind):
                with self.assertRaises(ValueError):
                    propagate_independent(s,u,independent=ind)

    def test_photon(self):
        h,c,w = 6.62607015e-34,299792458,532e-9
        r = propagate_independent({"wavelength":-h*c/w**2},
                                  {"wavelength":1e-9}, independent=True)
        self.assertAlmostEqual(r["standard_uncertainty"]/(h*c/w),1/532,places=14)
