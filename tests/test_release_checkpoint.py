import unittest
import tempfile
import subprocess
from pathlib import Path
from release_checkpoint import inspect_checkpoint

class CheckpointTests(unittest.TestCase):
    def test_checkpoint(self):
        with tempfile.TemporaryDirectory() as tmp:
            def git(*args):
                return subprocess.check_output(["git","-C",tmp,*args],text=True).strip()
            git("init")
            git("config","user.email","test@example.invalid")
            git("config","user.name","Test")
            p=Path(tmp)/"tracked.txt"
            p.write_text("baseline")
            git("add","tracked.txt")
            git("commit","-m","baseline")
            sha=git("rev-parse","HEAD")
            result=inspect_checkpoint(tmp,sha)
            self.assertTrue(result["checkpoint_match"])
            self.assertFalse(result["release_authorized"])
            self.assertFalse(inspect_checkpoint(tmp,"0"*40)["checkpoint_match"])
            p.write_text("modified")
            self.assertFalse(inspect_checkpoint(tmp,sha)["checkpoint_match"])
            git("restore","tracked.txt")
            (Path(tmp)/"untracked.txt").write_text("new")
            self.assertFalse(inspect_checkpoint(tmp,sha)["checkpoint_match"])
            with self.assertRaises(ValueError):
                inspect_checkpoint(tmp,"main")
