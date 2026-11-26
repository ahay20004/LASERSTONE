import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from hashlib import sha256
from resource_catalog import Catalog, Resource
from resource_recovery import copy_verified

class RecoveryTests(unittest.TestCase):
    def test_backup_restore(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            primary, backup = root/"primary", root/"backup"
            primary.mkdir()
            path = primary/"reference.txt"
            path.write_bytes(b"reference")
            catalog = Catalog([Resource("r","1","reference.txt","synthetic",
                "test","restore",sha256(b"reference").hexdigest())])
            def copy(a,b):
                return copy_verified(catalog,"r","1",a,b)
            self.assertEqual(copy(primary,backup)["status"],"COPIED_VERIFIED")
            self.assertEqual(copy(primary,backup)["status"],"ALREADY_PRESENT")
            path.unlink()
            self.assertEqual(copy(backup,primary)["status"],"COPIED_VERIFIED")
            self.assertEqual(path.read_bytes(),b"reference")
            path.write_bytes(b"damaged")
            with self.assertRaises(FileExistsError):
                copy(backup,primary)
            self.assertEqual(path.read_bytes(),b"damaged")
            with self.assertRaises(ValueError):
                copy(primary,backup)
            with self.assertRaises(ValueError):
                copy(backup,backup/"nested")
