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


    def test_correlated(self):
        from measurement_uncertainty import propagate_correlated
        for rho, expected in [(0, 2**0.5), (1, 2), (-1, 0)]:
            matrix = {"a":{"a":1,"b":rho},"b":{"a":rho,"b":1}}
            result = propagate_correlated({"a":1,"b":1},{"a":1,"b":1},matrix)
            self.assertAlmostEqual(result["standard_uncertainty"],expected)
        matrix = {"a":{"a":1,"b":1},"b":{"a":1,"b":1}}
        self.assertAlmostEqual(propagate_correlated({"a":1,"b":-1},{"a":1,"b":1},matrix)["standard_uncertainty"],0)

    def test_invalid_correlation(self):
        from measurement_uncertainty import propagate_correlated
        s = {"a":1,"b":1,"c":1}
        matrix = {i:{j:1 if i==j else -0.9 for j in s} for i in s}
        with self.assertRaises(ValueError):
            propagate_correlated(s,s,matrix)
        with self.assertRaises(ValueError):
            propagate_correlated(s,s,{})

    def test_numeric_limits(self):
        from scientific_uncertainty_bridge import checked_float
        for value in ("1e-400", "-1e-400", "1e400"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    checked_float(value)
        self.assertEqual(checked_float("0"),0)
        self.assertEqual(checked_float("1e-30"),1e-30)
        for s,u in [(1e-200,1e-200),(1e200,1e200)]:
            with self.assertRaises(ValueError):
                propagate_independent({"a":s},{"a":u},independent=True)
        self.assertEqual(propagate_independent({"a":1},{"a":0},independent=True)["standard_uncertainty"],0)
