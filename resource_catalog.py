"""Versioned local resource catalog; no automatic network access."""
from dataclasses import dataclass
from types import MappingProxyType
from pathlib import Path
from resource_integrity import inspect_resource
import re

@dataclass(frozen=True)
class Resource:
    identifier: str
    version: str
    relative_path: str
    source: str
    access: str
    recovery: str
    sha256: str | None = None

class Catalog:
    def __init__(self, records):
        entries = {}
        for record in records:
            if not isinstance(record, Resource):
                raise ValueError("Resource record required")
            for value in (record.identifier, record.version, record.relative_path,
                          record.source, record.access, record.recovery):
                if not isinstance(value, str) or not value.strip():
                    raise ValueError("Resource metadata required")
            if record.identifier in entries:
                raise ValueError("Duplicate resource identifier")
            path = Path(record.relative_path)
            if path.is_absolute() or ".." in path.parts or path.drive:
                raise ValueError("Unsafe resource path")
            if record.sha256 is not None and not re.fullmatch(r"[0-9a-f]{64}", record.sha256):
                raise ValueError("Invalid digest")
            entries[record.identifier] = record
        self.records = MappingProxyType(entries)

    def inspect(self, root, identifier, required_version):
        record = self.records[identifier]
        if not isinstance(required_version, str) or not required_version:
            raise ValueError("Explicit required version")
        if record.version != required_version:
            return {"status":"INCOMPATIBLE","integrity_verified":False}
        if record.sha256 is None:
            return {"status":"UNPINNED","integrity_verified":False,
                    "recovery":record.recovery}
        return inspect_resource(root, record.relative_path, record.sha256,
                                version=record.version, required_version=required_version)

    def read_verified(self, root, identifier, required_version):
        record = self.records[identifier]
        result = self.inspect(root, identifier, required_version)
        if result["status"] != "INTEGRITY_MATCH":
            raise ValueError("Resource unavailable: " + result["status"])
        from hashlib import sha256
        root = Path(root).resolve()
        path = (root / record.relative_path).resolve()
        if not path.is_relative_to(root):
            raise ValueError("Resource escapes root")
        data = path.read_bytes()
        if sha256(data).hexdigest() != record.sha256:
            raise ValueError("Resource changed during retrieval")
        return data

DEFAULT_CATALOG = Catalog([
    Resource("codata2022_original","CODATA-2022",
             "reference_data/codata2022_original.txt",
             "https://physics.nist.gov/cuu/Constants/Table/allascii.txt",
             "Official public reference; verify redistribution terms",
             "Import official original bytes and review provenance before pinning")
])
