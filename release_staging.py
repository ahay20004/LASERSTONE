"""Offline staging of a pinned Git commit; no activation or cleanup of user files."""
import re
import subprocess
from pathlib import Path
from release_checkpoint import inspect_checkpoint

def stage_release(repository, releases_root, commit):
    if not isinstance(commit,str) or not re.fullmatch(r"[0-9a-f]{40}",commit):
        raise ValueError("Full commit SHA required")
    repository = Path(repository).resolve(strict=True)
    root = Path(releases_root).resolve()
    if root == repository or repository in root.parents or root in repository.parents:
        raise ValueError("Release root must be separate from source")
    def git(*args):
        return subprocess.check_output(["git","-C",str(repository),*args],text=True).strip()
    if git("rev-parse","--verify",commit+"^{commit}") != commit:
        raise ValueError("Commit identity mismatch")
    root.mkdir(parents=True,exist_ok=True)
    target = root / commit
    if target.exists() or target.is_symlink():
        raise FileExistsError("Existing release directory will not be replaced")
    git("worktree","add","--detach",str(target),commit)
    receipt = inspect_checkpoint(target,commit)
    if not receipt["checkpoint_match"]:
        raise ValueError("Staged checkpoint verification failed")
    return {**receipt,"path":str(target),"status":"STAGED","activation_authorized":False}
