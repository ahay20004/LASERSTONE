import unittest
from tempfile import TemporaryDirectory
from pathlib import Path
from resource_preflight import report

class PreflightTests(unittest.TestCase):
    def test_unpinned_resource(self):
        with TemporaryDirectory() as root:
            result = report(root)
            self.assertFalse(result["all_integrity_matched"])
            self.assertFalse(result["activation_authorized"])
            self.assertEqual(result["resources"][0]["status"],"UNPINNED")
            self.assertEqual(list(Path(root).iterdir()),[])
