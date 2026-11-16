"""Conservative change classification for LASERSTONE owner review."""
from __future__ import annotations
import json
from pathlib import Path
import subprocess

def classify(paths):
    paths = list(paths)
    high = []
    medium = []
    for p in paths:
        if p.startswith(".github/workflows/") or p.startswith("cloud/governance/"):
            high.append(p)
        elif p == "main.py" or p.startswith(("physics/", "database/", "engines/")) or (
            p.endswith(".py") and not p.startswith(("cloud/test_", "cloud/huggingface/"))
        ):
            high.append(p)
        elif p.startswith(("cloud/site/", "cloud/huggingface/")):
            medium.append(p)
        else:
            medium.append(p)
    level = "HIGH" if high else ("MEDIUM" if medium else "NONE")
    return {
        "risk_level": level,
        "high_risk_paths": high,
        "other_changed_paths": medium,
        "owner_decision_required": True,
        "recommended_decision": "REVIEW_REQUIRED",
        "auto_publish": False,
        "interpretation": "Path-based triage only; not a code security audit or scientific validation",
    }

def main():
    paths = subprocess.check_output(
        ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"],
        text=True, encoding="utf-8").splitlines()
    report = classify(paths)
    out = Path("audit-artifacts/governance")
    out.mkdir(parents=True, exist_ok=True)
    (out / "risk_assessment.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("LASERSTONE review risk:", report["risk_level"])
    print("Owner approval required for all public deployment")

if __name__ == "__main__":
    main()
