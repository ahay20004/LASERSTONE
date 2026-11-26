import unittest
from equation_domain_gate import assess_inputs

class DomainTests(unittest.TestCase):
    def test_valid(self):
        result = assess_inputs("vacuum_frequency", {"vacuum_wavelength": 532e-9})
        self.assertEqual(result["status"], "INPUT_DOMAIN_PASS")
        self.assertFalse(result["model_conditions_verified"])
        self.assertFalse(result["scientific_validation"])

    def test_invalid(self):
        for value in (0, -1, True, "NaN", "Infinity", None, "invalid"):
            with self.subTest(value=value):
                self.assertEqual(assess_inputs("vacuum_frequency",
                    {"vacuum_wavelength": value})["status"], "INPUT_DOMAIN_FAIL")
        for inputs in ({}, {"vacuum_wavelength": 1, "frequency": 1}):
            self.assertEqual(assess_inputs("vacuum_frequency", inputs)["status"],
                             "INPUT_DOMAIN_FAIL")

    def test_cavity(self):
        self.assertEqual(assess_inputs("linear_cavity_fsr",
            {"group_index": 1.5, "cavity_length": 0.1})["status"], "INPUT_DOMAIN_PASS")
        self.assertEqual(assess_inputs("linear_cavity_fsr",
            {"group_index": 0, "cavity_length": 0.1})["status"], "INPUT_DOMAIN_FAIL")
