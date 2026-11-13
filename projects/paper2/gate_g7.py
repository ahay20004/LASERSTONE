"""G7 publication readiness: conservative, auditable decision gate.

Input is a JSON readiness dossier. This gate does not assess novelty, scientific
truth, journal ranking, or guarantee acceptance. It prevents a release verdict
when evidence gates or editorial checks are missing.
"""
import argparse
import json
from pathlib import Path

GATES = tuple(f"G{i}" for i in range(1, 7))
CHECKS = ("author_approval", "master_manuscript_frozen",
          "figures_and_tables_verified", "references_verified",
          "claims_traceable", "data_rights_reviewed",
          "journal_scope_reviewed", "conflicts_and_funding_disclosed")

def evaluate(dossier):
    errors = []
    if not isinstance(dossier, dict):
        return {"gate": "G7", "status": "BLOCKED", "errors": ["Expected JSON object"]}
    gates = dossier.get("gate_results")
    checks = dossier.get("editorial_checks")
    if not isinstance(gates, dict):
        gates = {}
    if not isinstance(checks, dict):
        checks = {}
    for gate in GATES:
        if gates.get(gate) != "PASS":
            errors.append(f"{gate}: independently verified PASS required")
    for check in CHECKS:
        if checks.get(check) is not True:
            errors.append(f"{check}: explicit confirmation required")
    if not dossier.get("manuscript_version"):
        errors.append("manuscript_version: required")
    if not dossier.get("evidence_register_version"):
        errors.append("evidence_register_version: required")
    if not dossier.get("target_journal"):
        errors.append("target_journal: required")
    return {
        "gate": "G7", "version": "1.0",
        "status": "READY_FOR_HUMAN_REVIEW" if not errors else "BLOCKED",
        "errors": errors,
        "caveats": [
            "G7 requires verified gate reports; self-reported PASS values are not independently authenticated.",
            "READY_FOR_HUMAN_REVIEW is not acceptance, publication clearance or a scientific quality guarantee.",
            "Human authors must confirm novelty, ethics, authorship, journal policies and final submission."
        ]
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dossier", required=True)
    p.add_argument("--out", default="output/g7_gate")
    args = p.parse_args()
    dossier = json.loads(Path(args.dossier).read_text(encoding="utf-8"))
    report = evaluate(dossier)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "g7_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["status"] == "READY_FOR_HUMAN_REVIEW" else 1)

if __name__ == "__main__":
    main()
