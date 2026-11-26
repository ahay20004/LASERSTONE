import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from hashlib import sha256
from resource_catalog import Catalog, Resource
from resource_preflight import report
from resource_recovery import copy_verified
from codata_local_import import stage_candidate
from codata_catalog import parse_catalog

class LifecycleTests(unittest.TestCase):
    def test_synthetic_lifecycle(self):
        raw = ("2022 CODATA adjustment\n"+"-"*110+"\n"+
               "".join(f"{'fixture '+str(i):60}{'1.0':25}{'(exact)':25}m\n"
                       for i in range(355))).encode("ascii")
        with TemporaryDirectory() as folder:
            root = Path(folder)
            source = root/"fixture.txt"
            source.write_bytes(raw)
            staged, receipt = stage_candidate(source,root/"staging")
            self.assertFalse(receipt["activation_authorized"])
            # Explicit synthetic-only pin, never a production approval.
            catalog = Catalog([Resource("fixture","CODATA-2022","original.txt",
                "synthetic fixture","test only","restore",sha256(raw).hexdigest())])
            primary, backup = root/"primary", root/"backup"
            self.assertFalse(report(primary,catalog)["all_integrity_matched"])
            copy_verified(catalog,"fixture","CODATA-2022",staged,primary)
            copy_verified(catalog,"fixture","CODATA-2022",primary,backup)
            self.assertTrue(report(primary,catalog)["all_integrity_matched"])
            self.assertFalse(report(primary,catalog)["activation_authorized"])
            (primary/"original.txt").unlink()
            self.assertFalse(report(primary,catalog)["all_integrity_matched"])
            copy_verified(catalog,"fixture","CODATA-2022",backup,primary)
            recovered = catalog.read_verified(primary,"fixture","CODATA-2022")
            self.assertEqual(recovered,raw)
            self.assertEqual(len(parse_catalog(recovered)[0]),355)
            (primary/"original.txt").write_bytes(b"damaged")
            self.assertFalse(report(primary,catalog)["all_integrity_matched"])
            with self.assertRaises(FileExistsError):
                copy_verified(catalog,"fixture","CODATA-2022",backup,primary)
            self.assertEqual((primary/"original.txt").read_bytes(),b"damaged")
