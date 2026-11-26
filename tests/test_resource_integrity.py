import unittest
from tempfile import TemporaryDirectory
from pathlib import Path
from hashlib import sha256
from resource_integrity import inspect_resource

class ResourceTests(unittest.TestCase):
    def test_resource_states(self):
        with TemporaryDirectory() as root:
            digest = sha256(b"reference").hexdigest()
            def check(version="1"):
                return inspect_resource(root,"reference.txt",digest,version=version,required_version="1")
            self.assertEqual(check()["status"],"MISSING")
            p = Path(root)/"reference.txt"
            p.write_bytes(b"reference")
            self.assertEqual(check()["status"],"INTEGRITY_MATCH")
            self.assertFalse(check()["authenticity_verified"])
            self.assertEqual(check("2")["status"],"INCOMPATIBLE")
            p.write_bytes(b"changed")
            self.assertEqual(check()["status"],"CORRUPTED")
            with self.assertRaises(ValueError):
                inspect_resource(root,"../outside",digest,version="1",required_version="1")
