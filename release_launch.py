"""Resolve an explicitly selected local release without updating it."""
import json
import re
from pathlib import Path
from release_checkpoint import inspect_checkpoint

def resolve_release(root):
    root=Path(root).resolve(strict=True)
    pointer=root/"selection.json"
    if pointer.is_symlink():
        raise ValueError("Symlink selection forbidden")
    record=json.loads(pointer.read_text(encoding="utf-8"))
    commit=record.get("active")
    if not isinstance(commit,str) or not re.fullmatch(r"[0-9a-f]{40}",commit):
        raise ValueError("Invalid selected commit")
    target=root/commit
    if target.is_symlink() or not target.is_dir():
        raise ValueError("Missing isolated release")
    if not inspect_checkpoint(target,commit)["checkpoint_match"]:
        raise ValueError("Selected release failed integrity check")
    launcher=target/"run_laserstone_unified_windows.bat"
    if not launcher.is_file() or launcher.is_symlink():
        raise ValueError("Missing release launcher")
    return launcher
