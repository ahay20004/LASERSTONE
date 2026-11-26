import unittest
from scientific_result_format import format_result

class ScientificFormatTests(unittest.TestCase):
    def test_photon(self):
        r = format_result("2.3305300457", "0.0043806956", "eV")
        self.assertEqual(r["display_value"], "2.3305")
        self.assertEqual(r["display_uncertainty"], "0.0044")
        self.assertEqual(r["raw_value"], "2.3305300457")
        self.assertFalse(r["scientific_validation"])

    def test_carry(self):
        r = format_result("1.23456", "0.00999", "J")
        self.assertEqual(r["display_uncertainty"], "0.010")
        self.assertEqual(r["display_value"], "1.235")

    def test_half_even(self):
        self.assertEqual(format_result("1.245", "0.12", "J")["display_value"], "1.24")
        self.assertEqual(format_result("-1.255", "0.12", "J")["display_value"], "-1.26")

    def test_unknown_and_zero(self):
        self.assertEqual(format_result("1.23", None, "J")["uncertainty_status"], "unknown")
        self.assertEqual(format_result("1.23", 0, "J")["uncertainty_status"], "reported_zero")

    def test_invalid(self):
        for v,u,unit in [(True,1,"J"),("NaN",1,"J"),(1,-1,"J"),(1,"Infinity","J"),(1,1,"")]:
            with self.subTest(v=v,u=u,unit=unit):
                with self.assertRaises(ValueError):
                    format_result(v,u,unit)
