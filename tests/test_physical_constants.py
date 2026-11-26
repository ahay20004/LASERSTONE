import unittest
from dataclasses import FrozenInstanceError
from physical_constants import REGISTRY, get_constant, get_record, get_records

class PhysicalConstantsTests(unittest.TestCase):
    def test_si_values(self):
        expected = {"speed_of_light": 299792458, "planck_constant": 6.62607015e-34,
                    "elementary_charge": 1.602176634e-19, "boltzmann_constant": 1.380649e-23,
                    "avogadro_constant": 6.02214076e23, "cesium_hyperfine_frequency": 9192631770,
                    "luminous_efficacy": 683}
        for key, value in expected.items():
            with self.subTest(key=key):
                self.assertEqual(get_constant(key), value)
                record = get_record(key)
                self.assertTrue(record.exact)
                self.assertEqual(record.uncertainty, 0)
                self.assertEqual(len(record.dimensions), 7)
                self.assertTrue(record.source)

    def test_dimensions(self):
        self.assertEqual(get_record("planck_constant").dimensions, (1,2,-1,0,0,0,0))
        self.assertEqual(get_record("elementary_charge").dimensions, (0,0,1,1,0,0,0))
        self.assertEqual(get_record("boltzmann_constant").dimensions, (1,2,-2,0,-1,0,0))

    def test_read_only_and_unknown(self):
        with self.assertRaises(TypeError):
            REGISTRY["new"] = None
        with self.assertRaises(FrozenInstanceError):
            get_record("speed_of_light").value = 1
        with self.assertRaises(KeyError):
            get_constant("unknown")
        self.assertEqual(set(get_records("speed_of_light", "planck_constant")),
                         {"speed_of_light", "planck_constant"})

if __name__ == "__main__":
    unittest.main()
