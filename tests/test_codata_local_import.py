import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from hashlib import sha256
from codata_local_import import stage_candidate

class ImportTests(unittest.TestCase):
    def test_candidate(self):
        raw = ("2022 CODATA adjustment\n"+"-"*110+"\n"+
               "".join(f"{'fixture '+str(i):60}{'1.0':25}{'(exact)':25}m\n"
                       for i in range(355))).encode("ascii")
        with TemporaryDirectory() as root:
            source = Path(root)/"source.txt"
            source.write_bytes(raw)
            folder, receipt = stage_candidate(source,Path(root)/"staging")
            self.assertEqual((folder/"original.txt").read_bytes(),raw)
            self.assertEqual(receipt["sha256"],sha256(raw).hexdigest())
            self.assertFalse(receipt["activation_authorized"])
            self.assertFalse(receipt["authenticity_verified"])
            self.assertEqual(receipt["record_count"],355)
            source.write_bytes(b"invalid")
            with self.assertRaises(ValueError):
                stage_candidate(source,Path(root)/"staging")
