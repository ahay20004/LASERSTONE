"""Stage a local CODATA candidate without granting source approval."""
from pathlib import Path
from tempfile import mkdtemp
import json
from codata_catalog import parse_catalog, SOURCE, VERSION

def stage_candidate(source_file, staging_root):
    with Path(source_file).open("rb") as stream:
        raw = stream.read(1048577)
    if len(raw) > 1048576:
        raise ValueError("Reference exceeds size limit")
    records, digest = parse_catalog(raw)
    root = Path(staging_root)
    root.mkdir(parents=True, exist_ok=True)
    folder = Path(mkdtemp(prefix="codata-", dir=root))
    receipt = {"version":VERSION,"claimed_source":SOURCE,"sha256":digest,
               "record_count":len(records),"status":"CANDIDATE",
               "authenticity_verified":False,"activation_authorized":False}
    (folder / "original.txt").write_bytes(raw)
    (folder / "receipt.json").write_text(json.dumps(receipt,indent=2),encoding="utf-8")
    return folder, receipt

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_file")
    parser.add_argument("staging_root")
    args = parser.parse_args()
    folder, receipt = stage_candidate(args.source_file,args.staging_root)
    print(json.dumps({"folder":str(folder),**receipt},indent=2))
