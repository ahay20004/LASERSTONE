import unittest
from equation_registry import REGISTRY, check_equation
from quantity_relationships import describe_quantity, describe_equation

class EquationTests(unittest.TestCase):
    def test_dimensions(self):
        for identifier in REGISTRY:
            with self.subTest(identifier=identifier):
                result = check_equation(identifier)
                self.assertEqual(result["status"], "DIMENSIONALLY_CONSISTENT")
                self.assertEqual(result["claims_authorized"], [])

    def test_relationships(self):
        q = describe_quantity("frequency")
        self.assertIn("vacuum_frequency", q["produced_by"])
        self.assertIn("photon_energy", q["used_by"])
        e = describe_equation("photon_energy_wavelength")
        self.assertEqual(e["output"]["identifier"], "photon_energy")
        self.assertEqual({x[0] for x in e["constants"]},
                         {"planck_constant", "speed_of_light"})
        self.assertFalse(e["scientific_validation"])
        self.assertTrue(e["conditions"])
        with self.assertRaises(KeyError):
            describe_quantity("unknown")
