import pathlib
import tempfile
import unittest
from agent_local_inventory import inventory

class InventoryTests(unittest.TestCase):
    def test_empty(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d)
            r = inventory(p, p)
            self.assertEqual(r["inventory"], [])
            self.assertFalse(r["active_agents_verified"])

    def test_file_names_only(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d)
            a = p / ".github" / "agents"
            a.mkdir(parents=True)
            (a / "physics.md").write_text("SECRET_TEST_STRING", encoding="utf-8")
            r = inventory(p, p)
            self.assertIn("physics.md", str(r))
            self.assertNotIn("SECRET_TEST_STRING", str(r))
            self.assertFalse(r["agent_execution_attempted"])

if __name__ == "__main__":
    unittest.main()
