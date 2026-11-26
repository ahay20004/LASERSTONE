import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from hashlib import sha256
from resource_catalog import Catalog, Resource, DEFAULT_CATALOG

class CatalogTests(unittest.TestCase):
    def test_retrieval(self):
        with TemporaryDirectory() as root:
            record = Resource("fixture","1","fixture.txt","synthetic","test only",
                              "regenerate",sha256(b"test").hexdigest())
            catalog = Catalog([record])
            with self.assertRaises(ValueError):
                catalog.read_verified(root,"fixture","1")
            path = Path(root)/"fixture.txt"
            path.write_bytes(b"test")
            self.assertEqual(catalog.read_verified(root,"fixture","1"),b"test")
            with self.assertRaises(ValueError):
                catalog.read_verified(root,"fixture","2")
            path.write_bytes(b"changed")
            with self.assertRaises(ValueError):
                catalog.read_verified(root,"fixture","1")
            with self.assertRaises(ValueError):
                Catalog([record,record])
    def test_unpinned_codata(self):
        with TemporaryDirectory() as root:
            self.assertEqual(DEFAULT_CATALOG.inspect(root,"codata2022_original",
                "CODATA-2022")["status"],"UNPINNED")
            with self.assertRaises(ValueError):
                DEFAULT_CATALOG.read_verified(root,"codata2022_original","CODATA-2022")
