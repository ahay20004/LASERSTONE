"""Research Hub: aggregate gate reports without fabricating a PASS.

Reads reports already produced by the gate CLIs. Missing or malformed reports
remain NOT_RUN. G7 READY_FOR_HUMAN_REVIEW is never treated as publication approval.
"""
import argparse
import json
from pathlib import Path

GATES = tuple(f"G{i}" for i in range(1, 8))
ACCEPTED = {"G1": {"PASS"}, "G2": {"PASS"}, "G3": {"PASS"},
            "G4": {"PASS"}, "G5": {"PASS"}, "G6": {"PASS"},
            "G7": {"READY_FOR_HUMAN_REVIEW"}}

def summarize(report_dir, project_id="paper2"):
    root = Path(report_dir)
    gates = {}
    for gate in GATES:
        file = root / gate.lower() / f"{gate.lower()}_report.json"
        entry = {"status": "NOT_RUN", "report": str(file)}
        if file.is_file():
            try:
                data = json.loads(file.read_text(encoding="utf-8"))
                if not isinstance(data, dict) or data.get("gate") != gate:
                    entry["status"] = "INVALID_REPORT"
                else:
                    status = data.get("status")
                    entry["status"] = status if status in ACCEPTED[gate] else (
                        "FAIL" if status in {"FAIL", "BLOCKED"} else "INVALID_REPORT")
            except (ValueError, OSError):
                entry["status"] = "INVALID_REPORT"
        gates[gate] = entry
    all_checks = all(gates[g]["status"] in ACCEPTED[g] for g in GATES)
    return {"project_id": project_id, "version": "1.0",
            "status": "REQUIRES_HUMAN_REVIEW" if all_checks else "INCOMPLETE",
            "gates": gates,
            "caveats": [
                "Summary reflects report contents, not independent authentication of reports.",
                "No PASS is inferred for missing reports.",
                "Human scientific and editorial approval remains mandatory."
            ]}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--reports", required=True)
    p.add_argument("--project-id", default="paper2")
    p.add_argument("--out", default="output/research_hub_status.json")
    args = p.parse_args()
    status = summarize(args.reports, args.project_id)
    dest = Path(args.out)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))

if __name__ == "__main__":
    main()
