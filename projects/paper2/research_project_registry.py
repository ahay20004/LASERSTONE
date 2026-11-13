"""LASERSTONE Research Hub project registry.

Projects remain separate scientific and authorship units. This module validates
metadata and progress state; it does not claim that any scientific gate passed.
"""
import argparse
import json
from pathlib import Path

STAGES = ("IDEA", "EVIDENCE_INTAKE", "ANALYSIS", "VALIDATION",
          "MANUSCRIPT", "JOURNAL_SELECTION", "SUBMITTED", "UNDER_REVIEW",
          "REVISION", "ACCEPTED", "PUBLISHED", "ON_HOLD")
REQUIRED = ("project_id", "working_title", "stage", "master_reference",
            "owner_approval", "evidence_register_reference")

def validate_registry(data):
    errors = []
    projects = data.get("projects") if isinstance(data, dict) else None
    if not isinstance(projects, list) or not projects:
        return {"status": "FAIL", "errors": ["projects must be a nonempty list"], "count": 0}
    ids = set()
    for index, project in enumerate(projects):
        prefix = f"projects[{index}]"
        if not isinstance(project, dict):
            errors.append(f"{prefix}: not an object")
            continue
        for field in REQUIRED:
            if field not in project or project[field] in (None, ""):
                errors.append(f"{prefix}: missing {field}")
        pid = project.get("project_id")
        if isinstance(pid, str) and pid:
            if pid in ids:
                errors.append(f"{prefix}: duplicate project_id")
            ids.add(pid)
        if project.get("stage") not in STAGES:
            errors.append(f"{prefix}: invalid stage")
        if project.get("owner_approval") is not True:
            errors.append(f"{prefix}: owner_approval must be explicitly true")
        if project.get("gate_reports") not in (None, {}) and not isinstance(project.get("gate_reports"), dict):
            errors.append(f"{prefix}: gate_reports must be an object")
    return {"status": "PASS" if not errors else "FAIL",
            "count": len(projects), "errors": errors,
            "caveat": "Registry validation confirms metadata only; gate PASS requires separately verified reports."}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--registry", required=True)
    p.add_argument("--out", default="output/research_registry_report.json")
    args = p.parse_args()
    result = validate_registry(json.loads(Path(args.registry).read_text(encoding="utf-8")))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["status"] == "PASS" else 1)

if __name__ == "__main__":
    main()
