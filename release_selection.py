"""Local release selection metadata; does not launch or modify worktrees."""
import json
import os
import re
import tempfile
from pathlib import Path
from release_checkpoint import inspect_checkpoint

def _select_release(root, commit, *, approved=False):
    if approved is not True:
        raise PermissionError("Explicit approval required")
    if not isinstance(commit,str) or not re.fullmatch(r"[0-9a-f]{40}",commit):
        raise ValueError("Full commit SHA required")
    root=Path(root).resolve(strict=True)
    target=root/commit
    if target.is_symlink() or not target.is_dir():
        raise ValueError("Expected isolated release directory")
    if not inspect_checkpoint(target,commit)["checkpoint_match"]:
        raise ValueError("Release checkpoint mismatch")
    pointer=root/"selection.json"
    if pointer.is_symlink():
        raise ValueError("Symlink pointer forbidden")
    old=json.loads(pointer.read_text(encoding="utf-8")) if pointer.exists() else {}
    previous=old.get("active")
    if previous is not None and (not isinstance(previous,str) or not re.fullmatch(r"[0-9a-f]{40}",previous)):
        raise ValueError("Invalid existing selection")
    if previous==commit:
        return old
    record={"active":commit,"previous":previous,"operational_acceptance":False}
    temp=None
    try:
        with tempfile.NamedTemporaryFile(mode="w",encoding="utf-8",dir=root,delete=False) as stream:
            temp=Path(stream.name)
            json.dump(record,stream)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp,pointer)
    finally:
        if temp is not None and temp.exists():
            temp.unlink()
    return record

def _rollback(root, *, approved=False):
    if approved is not True:
        raise PermissionError("Explicit approval required")
    pointer=Path(root).resolve(strict=True)/"selection.json"
    if pointer.is_symlink():
        raise ValueError("Symlink pointer forbidden")
    previous=json.loads(pointer.read_text(encoding="utf-8")).get("previous")
    if previous is None:
        raise ValueError("No previous release")
    return _select_release(root,previous,approved=True)

from contextlib import contextmanager

@contextmanager
def selection_lock(root):
    root=Path(root).resolve(strict=True)
    lock=root/"selection.lock"
    if lock.is_symlink():
        raise ValueError("Symlink lock forbidden")
    with open(lock,"a+b") as stream:
        stream.seek(0)
        if os.name=="nt":
            import msvcrt
            try:
                msvcrt.locking(stream.fileno(),msvcrt.LK_NBLCK,1)
            except OSError as exc:
                raise FileExistsError("Selection busy") from exc
        else:
            import fcntl
            try:
                fcntl.flock(stream.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
            except BlockingIOError as exc:
                raise FileExistsError("Selection busy") from exc
        yield

def select_release(root, commit, *, approved=False):
    if approved is not True:
        raise PermissionError("Explicit approval required")
    with selection_lock(root):
        return _select_release(root,commit,approved=True)

def rollback(root, *, approved=False):
    if approved is not True:
        raise PermissionError("Explicit approval required")
    with selection_lock(root):
        return _rollback(root,approved=True)
