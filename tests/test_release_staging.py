import unittest
import tempfile
import subprocess
from pathlib import Path
from release_staging import stage_release

class ReleaseStagingTests(unittest.TestCase):
    def test_isolation(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo=Path(tmp)/"source"
            repo.mkdir()
            def git(*args):
                return subprocess.check_output(["git","-C",str(repo),*args],text=True).strip()
            git("init")
            git("config","user.email","test@example.invalid")
            git("config","user.name","Test")
            p=repo/"tracked.txt"
            p.write_text("baseline")
            git("add","tracked.txt")
            git("commit","-m","baseline")
            sha=git("rev-parse","HEAD")
            p.write_text("private local change")
            root=Path(tmp)/"releases"
            receipt=stage_release(repo,root,sha)
            self.assertTrue(receipt["checkpoint_match"])
            self.assertFalse(receipt["activation_authorized"])
            self.assertEqual((root/sha/"tracked.txt").read_text(),"baseline")
            self.assertEqual(p.read_text(),"private local change")
            self.assertEqual(git("rev-parse","HEAD"),sha)
            with self.assertRaises(FileExistsError):
                stage_release(repo,root,sha)
            with self.assertRaises(ValueError):
                stage_release(repo,repo/"nested",sha)
            git("worktree","remove",str(root/sha))
