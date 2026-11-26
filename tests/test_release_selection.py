import unittest
import tempfile
import subprocess
from pathlib import Path
from release_staging import stage_release
from release_selection import select_release, rollback

class SelectionTests(unittest.TestCase):
    def test_lifecycle(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo=Path(tmp)/"source"
            repo.mkdir()
            root=Path(tmp)/"releases"
            def git(*args):
                return subprocess.check_output(["git","-C",str(repo),*args],text=True).strip()
            git("init")
            git("config","user.email","test@example.invalid")
            git("config","user.name","Test")
            p=repo/"tracked.txt"
            commits=[]
            for value in ("first","second"):
                p.write_text(value)
                git("add","tracked.txt")
                git("commit","-m",value)
                commits.append(git("rev-parse","HEAD"))
            a,b=commits
            for sha in commits:
                stage_release(repo,root,sha)
            with self.assertRaises(PermissionError):
                select_release(root,a)
            self.assertEqual(select_release(root,a,approved=True)["active"],a)
            with self.assertRaises(ValueError):
                rollback(root,approved=True)
            self.assertEqual(select_release(root,b,approved=True)["previous"],a)
            with self.assertRaises(PermissionError):
                rollback(root)
            self.assertEqual(rollback(root,approved=True)["active"],a)
            self.assertEqual(p.read_text(),"second")
            self.assertEqual((root/b/"tracked.txt").read_text(),"second")
            (root/b/"tracked.txt").write_text("damaged")
            before=(root/"selection.json").read_bytes()
            with self.assertRaises(ValueError):
                rollback(root,approved=True)
            self.assertEqual((root/"selection.json").read_bytes(),before)
            for sha in commits:
                git("worktree","remove","--force",str(root/sha))
