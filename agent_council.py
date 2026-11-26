"""LASERSTONE advisory council: deterministic, offline, human-gated review."""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import pathlib
import sys

ROLES = {
    "physics": ("physical consistency", "physics", "laser", "optics"),
    "evidence": ("provenance and traceability", "evidence", "dataset", "source"),
    "software": ("implementation and tests", "software", "code", "integration"),
    "numerical": ("numerical robustness", "numerical", "solver", "stability"),
    "security": ("permissions and release safety", "security", "secret", "release"),
    "research": ("novelty and scientific claims", "research", "novelty", "publication"),
}
SCHEMA = 1

def discover(root: pathlib.Path) -> dict:
    """Inventory repository evidence only; never claim a local/Codex agent is active."""
    candidates = [".github/agents", ".github/copilot-instructions.md",
                  "AGENTS.md", ".codex/agents", "agents", "agent_registry.json"]
    found = [p for p in candidates if (root / p).exists()]
    return {"repository_candidates": found, "local_runtime_verified": False,
            "codex_runtime_verified": False, "active_agents_verified": False,
            "declared_advisory_roles": sorted(ROLES)}

def council(task: dict) -> dict:
    if not isinstance(task, dict) or not isinstance(task.get("id"), str) or not task["id"].strip():
        raise ValueError("Task requires nonempty string id")
    if not isinstance(task.get("summary"), str) or not task["summary"].strip():
        raise ValueError("Task requires nonempty string summary")
    specialties = task.get("specialties", [])
    if not isinstance(specialties, list) or any(not isinstance(x, str) for x in specialties):
        raise ValueError("specialties must be a list of strings")
    unknown = set(specialties) - set(ROLES)
    if unknown:
        raise ValueError("Unknown specialties: " + ", ".join(sorted(unknown)))
    if not specialties:
        keywords = (task["summary"] + " " + task.get("context", "")).lower()
        specialties = [name for name, role in ROLES.items() if any(k in keywords for k in role[1:])]
    if not specialties:
        specialties = ["software", "evidence"]
    guests = task.get("guests", [])
    if not isinstance(guests, list) or any(not isinstance(x, str) or not x.strip() for x in guests):
        raise ValueError("guests must be nonempty strings")
    return {"schema": SCHEMA, "task_id": task["id"], "summary": task["summary"],
            "specialties": sorted(set(specialties)), "guest_advisers": sorted(set(guests)),
            "review_status": "AWAITING_INDEPENDENT_REVIEWS", "reviews": [],
            "recommendation": None, "human_decision": "PENDING",
            "execution_authorized": False}

def review(c: dict, r: dict) -> dict:
    if c["human_decision"] != "PENDING":
        raise ValueError("Cannot review a decided council")
    reviewer = r.get("reviewer")
    allowed = set(c["specialties"]) | set(c["guest_advisers"])
    if reviewer not in allowed:
        raise ValueError("Reviewer is not assigned to this council")
    if any(x["reviewer"] == reviewer for x in c["reviews"]):
        raise ValueError("Duplicate reviewer")
    if r.get("position") not in ("approve", "revise", "reject"):
        raise ValueError("Invalid position")
    if not isinstance(r.get("reason"), str) or not r["reason"].strip():
        raise ValueError("Evidence-based reason required")
    entry = {"reviewer": reviewer, "position": r["position"], "reason": r["reason"],
             "evidence": r.get("evidence", [])}
    if not isinstance(entry["evidence"], list):
        raise ValueError("evidence must be a list")
    if entry["position"] == "approve" and not any(isinstance(x, str) and x.strip() for x in entry["evidence"]):
        raise ValueError("Approval requires at least one nonempty evidence reference")
    c["reviews"].append(entry)
    expected = allowed
    actual = {x["reviewer"] for x in c["reviews"]}
    if actual == expected:
        positions = {x["position"] for x in c["reviews"]}
        c["review_status"] = "READY_FOR_HUMAN_DECISION"
        c["recommendation"] = positions.pop() if len(positions) == 1 else "DISAGREEMENT"
    return c

def decide(c: dict, decision: str, rationale: str) -> dict:
    if c["human_decision"] != "PENDING":
        raise ValueError("Human decision already recorded; convene a new council for reconsideration")
    if c["review_status"] != "READY_FOR_HUMAN_DECISION":
        raise ValueError("All assigned reviews required before decision")
    if decision not in ("approve", "revise", "reject") or not isinstance(rationale, str) or not rationale.strip():
        raise ValueError("Explicit human decision and rationale required")
    c["human_decision"] = decision.upper()
    c["human_rationale"] = rationale
    # Approval of advice never directly authorizes code execution or merging.
    c["execution_authorized"] = False
    return c

def save(path: pathlib.Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def main() -> int:
    parser = argparse.ArgumentParser(description="LASERSTONE offline advisory council")
    parser.add_argument("command", choices=["discover", "convene", "review", "decide"])
    parser.add_argument("--root", type=pathlib.Path, default=pathlib.Path(__file__).resolve().parent)
    parser.add_argument("--task", type=pathlib.Path)
    parser.add_argument("--input", type=pathlib.Path)
    parser.add_argument("--record", type=pathlib.Path)
    args = parser.parse_args()
    try:
        if args.command == "discover":
            result = discover(args.root)
        elif args.command == "convene":
            if not args.task or not args.record:
                raise ValueError("convene requires --task and --record")
            result = council(json.loads(args.task.read_text(encoding="utf-8")))
        else:
            if not args.input or not args.record or not args.record.is_file():
                raise ValueError("review/decide requires --input and existing --record")
            result = json.loads(args.record.read_text(encoding="utf-8"))
            data = json.loads(args.input.read_text(encoding="utf-8"))
            if args.command == "review":
                result = review(result, data)
            else:
                result = decide(result, data["decision"], data["rationale"])
        if args.record:
            save(args.record, result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as exc:
        print(f"COUNCIL ERROR: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
