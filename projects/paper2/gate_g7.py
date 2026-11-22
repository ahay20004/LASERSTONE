"""G7: fail-closed readiness based on actual G1-G6 report bytes.

Report SHA-256 checks byte consistency, not provenance or scientific truth.
"""
import argparse
import hashlib
import json
from pathlib import Path

GATES = tuple(f"G{i}" for i in range(1, 7))
CHECKS = ("author_approval", "master_manuscript_frozen",
          "figures_and_tables_verified", "references_verified",
          "claims_traceable", "data_rights_reviewed",
          "journal_scope_reviewed", "conflicts_and_funding_disclosed")


def evaluate(dossier, reports_dir=None):
    errors = []
    if not isinstance(dossier, dict):
        return {"gate": "G7", "status": "BLOCKED", "errors": ["Expected JSON object"]}
    gates = dossier.get("gate_results")
    checks = dossier.get("editorial_checks")
    hashes = dossier.get("gate_report_sha256")
    gates = gates if isinstance(gates, dict) else {}
    checks = checks if isinstance(checks, dict) else {}
    hashes = hashes if isinstance(hashes, dict) else {}
    root = Path(reports_dir).resolve() if reports_dir is not None else None
    verified = {}
    for gate in GATES:
        if gates.get(gate) != "PASS":
            errors.append(f"{gate}: declared PASS required")
        expected = hashes.get(gate)
        if not isinstance(expected, str) or len(expected) != 64 or any(c not in "0123456789abcdef" for c in expected.lower()):
            errors.append(f"{gate}: valid report SHA-256 required")
            continue
        if root is None:
            errors.append(f"{gate}: --reports-dir required")
            continue
        path = root / gate.lower() / f"{gate.lower()}_report.json"
        if not path.is_file() or path.is_symlink():
            errors.append(f"{gate}: report missing or symlink")
            continue
        try:
            raw = path.read_bytes()
            actual = hashlib.sha256(raw).hexdigest()
            if actual != expected.lower():
                errors.append(f"{gate}: report SHA-256 mismatch")
                continue
            report = json.loads(raw)
            if not isinstance(report, dict) or report.get("gate") != gate or report.get("status") != "PASS":
                errors.append(f"{gate}: report identity/status invalid")
                continue
            verified[gate] = {"sha256": actual, "status": "PASS"}
        except (OSError, ValueError, UnicodeError) as exc:
            errors.append(f"{gate}: unreadable or invalid JSON ({type(exc).__name__})")
    for check in CHECKS:
        if checks.get(check) is not True:
            errors.append(f"{check}: explicit confirmation required")
    for key in ("manuscript_version", "evidence_register_version", "target_journal"):
        if not isinstance(dossier.get(key), str) or not dossier[key].strip():
            errors.append(f"{key}: required nonempty string")
    return {"gate": "G7", "version": "2.1-proposal",
            "status": "READY_FOR_HUMAN_REVIEW" if not errors else "BLOCKED",
            "verified_reports": verified, "errors": errors,
            "caveats": [
                "Hashes bind dossier declarations to report bytes; they do not authenticate who generated reports.",
                "A G1-G6 PASS is not independent scientific validation of original spectra.",
                "READY_FOR_HUMAN_REVIEW is not publication approval; novelty, ethics and claims require human review."]}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dossier", required=True)
    p.add_argument("--reports-dir", required=True)
    p.add_argument("--out", default="output/g7_gate")
    args = p.parse_args()
    dossier = json.loads(Path(args.dossier).read_text(encoding="utf-8"))
    report = evaluate(dossier, args.reports_dir)
    dest = Path(args.out)
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "g7_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["status"] == "READY_FOR_HUMAN_REVIEW" else 1)


if __name__ == "__main__":
    main()
