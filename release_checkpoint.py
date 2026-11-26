"""Read-only checkpoint verification; never activates or updates a release."""
import re
import subprocess
from pathlib import Path

def inspect_checkpoint(root, expected_commit):
    if not isinstance(expected_commit,str) or not re.fullmatch(r"[0-9a-f]{40}",expected_commit):
        raise ValueError("Full commit SHA required")
    root = Path(root).resolve()
    def git(*args):
        return subprocess.check_output(["git","-C",str(root),*args],text=True).strip()
    actual = git("rev-parse","HEAD")
    clean = not git("status","--porcelain","--untracked-files=all")
    return {"expected_commit":expected_commit,"actual_commit":actual,
            "clean_worktree":clean,"checkpoint_match":actual==expected_commit and clean,
            "release_authorized":False}
