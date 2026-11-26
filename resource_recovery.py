"""Restore pinned resources from verified independent local copies."""
from pathlib import Path
from hashlib import sha256
from tempfile import NamedTemporaryFile
import os

def copy_verified(catalog, identifier, version, source_root, destination_root):
    record = catalog.records[identifier]
    data = catalog.read_verified(source_root, identifier, version)
    source_root = Path(source_root).resolve()
    root = Path(destination_root).resolve()
    if root == source_root or root.is_relative_to(source_root) or source_root.is_relative_to(root):
        raise ValueError("Separate non-nested roots required")
    target = (root / record.relative_path).resolve()
    if not target.is_relative_to(root):
        raise ValueError("Destination escapes root")
    if target.exists():
        if catalog.inspect(root, identifier, version)["status"] == "INTEGRITY_MATCH":
            return {"status":"ALREADY_PRESENT","sha256":record.sha256}
        raise FileExistsError("Preserve existing destination; quarantine separately")
    target.parent.mkdir(parents=True, exist_ok=True)
    temp = None
    try:
        with NamedTemporaryFile(dir=target.parent,delete=False) as stream:
            temp = Path(stream.name)
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if sha256(temp.read_bytes()).hexdigest() != record.sha256:
            raise ValueError("Staged copy failed integrity check")
        # Hard link publishes atomically without overwriting an existing target.
        os.link(temp,target)
        if catalog.inspect(root,identifier,version)["status"] != "INTEGRITY_MATCH":
            raise ValueError("Destination verification failed")
        return {"status":"COPIED_VERIFIED","sha256":record.sha256}
    finally:
        if temp is not None:
            temp.unlink(missing_ok=True)
