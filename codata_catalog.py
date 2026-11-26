"""Read original NIST CODATA 2022 fixed-width ASCII, not flattened extracts."""
from dataclasses import dataclass
from decimal import Decimal
from hashlib import sha256
from types import MappingProxyType
import re

SOURCE = "https://physics.nist.gov/cuu/Constants/Table/allascii.txt"
VERSION = "CODATA-2022"

@dataclass(frozen=True)
class ReferenceConstant:
    name: str
    value: Decimal
    uncertainty: Decimal
    unit: str
    exact: bool
    truncated: bool
    original_value: str
    source: str = SOURCE
    version: str = VERSION

def parse_catalog(raw: bytes):
    """Return immutable records and SHA256 of the actual input bytes."""
    text = raw.decode("ascii")
    if "2022 CODATA adjustment" not in text:
        raise ValueError("Unexpected CODATA edition")
    lines = text.splitlines()
    start = next((i for i, line in enumerate(lines)
                  if re.fullmatch(r"-{100,}", line.strip())), None)
    if start is None:
        raise ValueError("Missing original table separator")
    records = {}
    for line in lines[start + 1:]:
        if not line.strip():
            continue
        if len(line) < 85:
            raise ValueError("Expected original fixed-width columns")
        name = line[:60].strip()
        value = line[60:85].strip()
        uncertainty = line[85:110].strip()
        unit = line[110:].strip()
        if not name or name in records or not value or not uncertainty:
            raise ValueError("Invalid or duplicate CODATA record")
        exact = uncertainty == "(exact)"
        truncated = "..." in value
        v = Decimal(value.replace(" ", "").replace("...", ""))
        u = Decimal(0) if exact else Decimal(uncertainty.replace(" ", ""))
        if not v.is_finite() or not u.is_finite() or u < 0:
            raise ValueError("Invalid numerical value or uncertainty")
        if truncated and not exact:
            raise ValueError("Unexpected truncated measured value")
        records[name] = ReferenceConstant(name, v, u, unit or "1", exact, truncated, value)
    if len(records) != 355:
        raise ValueError("Unexpected CODATA 2022 record count")
    return MappingProxyType(records), sha256(raw).hexdigest()
