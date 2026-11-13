"""G1: verify integrity of local evidence files against a controlled manifest.

No raw files are uploaded by this gate. Manifest format:
{"files":[{"path":"input/sample.txt","sha256":"<64 hex>",
           "source_id":"S1","rights_status":"authorized"}]}
Paths are resolved under --root; traversal and symlinks are rejected.
"""
import argparse
import hashlib
import json
from pathlib import Path

RIGHTS = {"authorized", "restricted", "unknown"}

def verify(manifest, root):
    root = Path(root).resolve()
    errors = []
    files = manifest.get("files") if isinstance(manifest, dict) else None
    if not isinstance(files, list) or not files:
        return {"gate": "G1", "status": "FAIL", "checked": 0, "errors": ["Nonempty files list required"]}
    seen = set()
    for i, item in enumerate(files):
        label = f"files[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{label}: invalid entry")
            continue
        rel = item.get("path")
        if not isinstance(rel, str) or not rel.strip():
            errors.append(f"{label}: missing path")
            continue
        path = Path(rel)
        if path.is_absolute() or ".." in path.parts:
            errors.append(f"{label}: unsafe path")
            continue
        target = (root / path).resolve()
        if not target.is_relative_to(root) or target == root:
            errors.append(f"{label}: path escapes root")
            continue
        if target in seen:
            errors.append(f"{label}: duplicate path")
        seen.add(target)
        if not item.get("source_id"):
            errors.append(f"{label}: missing source_id")
        if item.get("rights_status") not in RIGHTS:
            errors.append(f"{label}: invalid rights_status")
        if not target.is_file():
            errors.append(f"{label}: file missing")
            continue
        expected = item.get("sha256")
        if not isinstance(expected, str) or len(expected) != 64 or any(c not in "0123456789abcdef" for c in expected.lower()):
            errors.append(f"{label}: invalid expected SHA-256")
            continue
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        if digest != expected.lower():
            errors.append(f"{label}: SHA-256 mismatch")
    return {"gate": "G1", "version": "1.0", "status": "PASS" if not errors else "FAIL",
            "checked": len(files), "errors": errors,
            "caveat": "Integrity does not establish scientific accuracy or redistribution rights; restricted and unknown rights require separate review."}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", required=True)
    p.add_argument("--root", required=True)
    p.add_argument("--out", default="output/g1_gate")
    args = p.parse_args()
    report = verify(json.loads(Path(args.manifest).read_text(encoding="utf-8")), args.root)
    dest = Path(args.out)
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "g1_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["status"] == "PASS" else 1)

if __name__ == "__main__":
    main()
