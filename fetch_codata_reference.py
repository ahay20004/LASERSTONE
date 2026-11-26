"""Explicit acquisition of original CODATA bytes; never runs on import."""
from pathlib import Path
from urllib.request import urlopen
from codata_catalog import SOURCE, parse_catalog

def acquire(destination: Path):
    with urlopen(SOURCE, timeout=30) as response:
        raw = response.read(1024 * 1024 + 1)
    if len(raw) > 1024 * 1024:
        raise ValueError("Unexpected reference size")
    records, digest = parse_catalog(raw)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("xb") as stream:
        stream.write(raw)
    print(f"Validated {len(records)} records; SHA256={digest}")
    return digest

if __name__ == "__main__":
    acquire(Path(__file__).resolve().parent / "reference_data" / "codata2022_original.txt")
