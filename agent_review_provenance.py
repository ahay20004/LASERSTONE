"""AC-04 review provenance gate: conservative, no unverifiable agent claims."""
from __future__ import annotations
import hashlib
import json

def canonical_digest(payload: dict) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False,
                                      separators=(",", ":")).encode("utf-8")).hexdigest()

def assess_submission(submission: dict, trusted_runs: dict | None = None) -> dict:
    """Check a supplied execution receipt against explicitly trusted local run records.

    trusted_runs is injected by an authorized runner, never self-reported by the reviewer.
    A matching receipt verifies only linkage to that runner's record, not scientific truth.
    """
    trusted_runs = trusted_runs or {}
    required = ("reviewer", "task_id", "position", "reason", "evidence", "run_id")
    if any(key not in submission for key in required):
        return {"status": "UNVERIFIED", "reason": "missing required fields"}
    run_id = submission["run_id"]
    if not isinstance(run_id, str) or not run_id:
        return {"status": "UNVERIFIED", "reason": "invalid run identifier"}
    record = trusted_runs.get(run_id)
    if not isinstance(record, dict):
        return {"status": "UNVERIFIED", "reason": "no trusted execution receipt"}
    if record.get("reviewer") != submission["reviewer"] or record.get("task_id") != submission["task_id"]:
        return {"status": "UNVERIFIED", "reason": "receipt identity mismatch"}
    payload = {k: submission[k] for k in required if k != "run_id"}
    if record.get("payload_sha256") != canonical_digest(payload):
        return {"status": "UNVERIFIED", "reason": "receipt payload mismatch"}
    return {"status": "RUN_LINKED", "reason": "matches externally supplied trusted run receipt",
            "scientific_validity_verified": False, "agent_identity_independently_verified": False}
