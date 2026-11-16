"""Generate an immutable-run dated audit packet from Git history; no code writes or deployment."""
from __future__ import annotations
import datetime as dt
import json
import os
from pathlib import Path
import subprocess
from risk_gate import classify, changed_since_base

def git(*args):
    return subprocess.check_output(["git", *args], text=True, encoding="utf-8", errors="replace").strip()

def main():
    output = Path("audit-artifacts/governance")
    output.mkdir(parents=True, exist_ok=True)
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    sha = git("rev-parse", "HEAD")
    history = git("log", "-n", "30", "--date=iso-strict",
                  "--pretty=format:%H%x09%aI%x09%s").splitlines()
    entries = []
    for line in history:
        fields = line.split("\t", 2)
        if len(fields) == 3:
            entries.append(dict(commit=fields[0], timestamp=fields[1], summary=fields[2]))
    changed, comparison = changed_since_base()
    risk = classify(changed)
    packet = {
        "generated_utc": now,
        "repository": os.environ.get("GITHUB_REPOSITORY", "ahay20004/LASERSTONE"),
        "commit_sha": sha,
        "run_id": os.environ.get("GITHUB_RUN_ID", "local"),
        "branch": os.environ.get("GITHUB_REF_NAME", "unknown"),
        "review_scope": comparison,
        "changed_paths_since_base": changed,
        "risk_assessment": risk,
        "history": entries,
        "tests": "See workflow run results; packet generation does not imply PASS",
        "publication_status": "NOT_APPROVED",
        "allowed_decisions": ["approve", "approve_with_changes", "reject"],
        "safety": "No unattended code modification or public deployment",
    }
    (output / "review_packet.json").write_text(
        json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# LASERSTONE dated development ledger",
        "",
        f"Generated (UTC): {now}",
        f"Reviewed candidate SHA: `{sha}`",
        "Decision: PENDING OWNER REVIEW",
        "CI outcome must be checked independently before approval.",
        "",
        f"Comparison: {comparison}",
        f"Risk: {risk["risk_level"]} — owner review required",
        "Risk is path-based; scientific and security validation are separate.",
        "",
        "## Changed files in review scope",
        *[f"- `{p}`" for p in changed],
        "",
        "## Last 30 recorded commits",
        *[f"- {e['timestamp']} | `{e['commit'][:12]}` | {e['summary']}" for e in entries],
        "",
        "## Owner decision",
        "Approve: dispatch huggingface-preview.yml with decision=approve and exact candidate SHA.",
        "Approve with changes: do not deploy; request changes, re-test, then approve a new SHA.",
        "Reject: do not deploy; preserve the audit record.",
        "",
    ]
    (output / "development_ledger.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated dated audit packet for {sha}; awaiting owner decision")

if __name__ == "__main__":
    main()
