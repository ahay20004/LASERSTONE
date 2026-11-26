import unittest
from decimal import Decimal
from hashlib import sha256
from codata_catalog import parse_catalog

def row(name, value, uncertainty, unit=""):
    return f"{name:60}{value:25}{uncertainty:25}{unit}"

def fixture():
    rows = [
        row("electron mass", "9.109 383 7139 e-31", "0.000 000 0028 e-31", "kg"),
        row("reduced Planck constant", "1.054 571 817... e-34", "(exact)", "J s"),
        row("ratio", "1.25", "0.01"),
    ]
    rows += [row(f"synthetic {i}", "1", "(exact)") for i in range(352)]
    return ("2022 CODATA adjustment\n" + "-"*125 + "\n" + "\n".join(rows)).encode("ascii")

class CodataTests(unittest.TestCase):
    def test_precision_and_provenance(self):
        raw = fixture()
        records, digest = parse_catalog(raw)
        self.assertEqual(len(records), 355)
        self.assertEqual(digest, sha256(raw).hexdigest())
        mass = records["electron mass"]
        self.assertEqual(mass.value, Decimal("9.1093837139e-31"))
        self.assertEqual(mass.uncertainty, Decimal("2.8e-40"))
        self.assertFalse(mass.exact)
        self.assertEqual(mass.unit, "kg")
        hbar = records["reduced Planck constant"]
        self.assertTrue(hbar.exact)
        self.assertTrue(hbar.truncated)
        self.assertEqual(hbar.uncertainty, Decimal(0))
        self.assertEqual(records["ratio"].unit, "1")
        with self.assertRaises(TypeError):
            records["new"] = None

    def test_reject_invalid_catalogs(self):
        raw = fixture()
        for bad in [
            raw.replace(b"2022 CODATA", b"2018 CODATA"),
            raw.replace(b"synthetic 1 ", b"synthetic 0 ", 1),
            raw.rsplit(b"\n", 1)[0],
            raw.replace(b"0.01", b"-0.1"),
            raw.replace(b"1.25", b"NaN "),
            b"2022 CODATA adjustment\n" + b"-"*125 + b"\nelectron mass 9.1e-31 0.1e-31 kg",
        ]:
            with self.subTest(sample=bad[:50]):
                with self.assertRaises(ValueError):
                    parse_catalog(bad)
