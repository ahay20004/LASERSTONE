"""G6: check that manuscript claims have traceable evidence records.

This gate validates metadata completeness and consistency, not scientific truth.
"""
import argparse
import json
from pathlib import Path

REQUIRED = ("claim_id", "claim_text", "evidence_type", "source_id",
            "source_sha256", "method", "parameters", "conditions", "result",
            "limitations", "manuscript_location")
ALLOWED_TYPES = {"measured", "derived", "predicted", "hypothesis"}
HEX = set("0123456789abcdef")

def validate(records):
    if not isinstance(records, list) or not records:
        return {"status": "FAIL", "errors": ["Nonempty list of evidence records required"], "records_checked": 0}
    errors = []
    ids = set()
    for index, record in enumerate(records):
        prefix = f"record[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{prefix}: expected object")
            continue
        missing = [key for key in REQUIRED if key not in record or record[key] in (None, "", [], {})]
        if missing:
            errors.append(f"{prefix}: missing {', '.join(missing)}")
        cid = record.get("claim_id")
        if isinstance(cid, str) and cid:
            if cid in ids:
                errors.append(f"{prefix}: duplicate claim_id")
            ids.add(cid)
        kind = record.get("evidence_type")
        if kind not in ALLOWED_TYPES:
            errors.append(f"{prefix}: invalid evidence_type")
        sha = record.get("source_sha256")
        if not isinstance(sha, str) or len(sha) != 64 or not set(sha.lower()) <= HEX:
            errors.append(f"{prefix}: invalid SHA-256 format")
        if kind == "predicted" and not record.get("model_version"):
            errors.append(f"{prefix}: predicted claim requires model_version")
        if kind == "hypothesis" and record.get("result") == "experimentally_verified":
            errors.append(f"{prefix}: hypothesis cannot be marked experimentally_verified")
    return {"gate": "G6", "version": "1.0", "status": "PASS" if not errors else "FAIL",
            "records_checked": len(records), "errors": errors,
            "caveat": "Metadata completeness does not establish validity of scientific claims or source rights."}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--register", required=True)
    parser.add_argument("--out", default="output/g6_gate")
    args = parser.parse_args()
    records = json.loads(Path(args.register).read_text(encoding="utf-8"))
    report = validate(records)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "g6_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["status"] == "PASS" else 1)

if __name__ == "__main__":
    main()
