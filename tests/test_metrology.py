import unittest
from decimal import Decimal
from physical_quantities import REGISTRY, get_quantity, same_dimensions
from unit_conversion import convert

class MetrologyTests(unittest.TestCase):
    def test_registry(self):
        self.assertEqual(len(REGISTRY), 30)
        for q in REGISTRY.values():
            self.assertEqual(len(q.dimensions), 7)
            self.assertTrue(all(type(x) is int for x in q.dimensions))
        self.assertTrue(same_dimensions("frequency", "angular_frequency"))
        self.assertNotEqual(get_quantity("frequency"), get_quantity("angular_frequency"))
        self.assertTrue(same_dimensions("photon_energy", "torque"))
        self.assertEqual(get_quantity("electrical_conductivity").dimensions, (-1,-3,3,2,0,0,0))

    def test_conversion(self):
        for value, kind, source, target, expected in [
            (532,"vacuum_wavelength","nm","m","5.32e-7"),
            (1,"photon_energy","eV","J","1.602176634e-19"),
            (1,"irradiance","mW/cm^2","W/m^2","10"),
            (1,"number_density","cm^-3","m^-3","1e6"),
            (50,"efficiency","%","1","0.5"),
        ]:
            with self.subTest(kind=kind):
                self.assertEqual(convert(value,kind,source,target), Decimal(expected))
                self.assertEqual(convert(expected,kind,target,source), Decimal(value))

    def test_rejection(self):
        with self.assertRaises(KeyError):
            convert(1,"frequency","Hz","rad/s")
        with self.assertRaises(KeyError):
            convert(1,"temperature","degC","K")
        with self.assertRaises(ValueError):
            convert("NaN","power","W","mW")
        with self.assertRaises(ValueError):
            convert(True,"power","W","mW")
