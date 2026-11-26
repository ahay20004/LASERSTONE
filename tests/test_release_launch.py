import unittest
import tempfile
import subprocess
from pathlib import Path
from release_staging import stage_release
from release_selection import select_release, selection_lock
from release_launch import resolve_release

class LaunchTests(unittest.TestCase):
    def test_resolution(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo=Path(tmp)/"source"
            repo.mkdir()
            root=Path(tmp)/"releases"
            def git(*args):
                return subprocess.check_output(["git","-C",str(repo),*args],text=True).strip()
            git("init")
            git("config","user.email","test@example.invalid")
            git("config","user.name","Test")
            name="run_laserstone_unified_windows.bat"
            (repo/name).write_text("@echo off")
            git("add",name)
            git("commit","-m","baseline")
            sha=git("rev-parse","HEAD")
            stage_release(repo,root,sha)
            with selection_lock(root):
                with self.assertRaises(FileExistsError):
                    select_release(root,sha,approved=True)
            self.assertTrue((root/"selection.lock").exists())
            with selection_lock(root):
                pass
            select_release(root,sha,approved=True)
            self.assertEqual(resolve_release(root),root.resolve()/sha/name)
            (root/sha/name).write_text("modified")
            with self.assertRaises(ValueError):
                resolve_release(root)
            git("worktree","remove","--force",str(root/sha))

    def test_process_termination_releases_lock(self):
        import sys
        with tempfile.TemporaryDirectory() as tmp:
            child=subprocess.Popen([sys.executable,"-u","-c",
                "from release_selection import selection_lock; import sys,time\nwith selection_lock(sys.argv[1]):\n print('locked',flush=True); time.sleep(60)",tmp],
                stdout=subprocess.PIPE,text=True)
            try:
                self.assertEqual(child.stdout.readline().strip(),"locked")
                with self.assertRaises(FileExistsError):
                    with selection_lock(tmp):
                        pass
            finally:
                child.kill()
                child.wait(timeout=10)
                child.stdout.close()
            with selection_lock(tmp):
                pass
