"""Offline integrity check for version-pinned local resources."""
from pathlib import Path
from hashlib import sha256
import re

def inspect_resource(root, relative_path, expected_sha256, *, version, required_version):
    if not isinstance(expected_sha256, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_sha256):
        raise ValueError("Expected SHA256 must be a lowercase hexadecimal digest")
    if not isinstance(version, str) or not version or not isinstance(required_version, str) or not required_version:
        raise ValueError("Explicit versions required")
    root = Path(root).resolve()
    relative = Path(relative_path)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("Resource path must stay within root")
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError("Resource path escapes root")
    result = {"version":version,"required_version":required_version,
              "status":"MISSING","integrity_verified":False,"authenticity_verified":False}
    if version != required_version:
        result["status"] = "INCOMPATIBLE"
        return result
    if not path.is_file():
        return result
    digest = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda:stream.read(65536),b""):
            digest.update(block)
    result["actual_sha256"] = digest.hexdigest()
    result["integrity_verified"] = result["actual_sha256"] == expected_sha256
    result["status"] = "INTEGRITY_MATCH" if result["integrity_verified"] else "CORRUPTED"
    return result
