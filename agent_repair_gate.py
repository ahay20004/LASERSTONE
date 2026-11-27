"""AC-06 repair evidence gate: never confuse a proposal with a verified fix."""
from __future__ import annotations

def assess_repair(record: dict) -> dict:
    if not isinstance(record, dict):
        raise ValueError("Repair record must be an object")
    required = ("task_id", "change_ref", "tests", "human_approval")
    if any(k not in record for k in required):
        return {"status": "INCOMPLETE", "ready_for_human_review": False,
                "execution_authorized": False}
    if not isinstance(record["task_id"], str) or not record["task_id"].strip():
        raise ValueError("Invalid task ID")
    if not isinstance(record["change_ref"], str) or not record["change_ref"].strip():
        return {"status": "PROPOSED_ONLY", "ready_for_human_review": False,
                "execution_authorized": False}
    tests = record["tests"]
    if not isinstance(tests, list) or not tests:
        return {"status": "UNTESTED", "ready_for_human_review": False,
                "execution_authorized": False}
    for test in tests:
        if not isinstance(test, dict) or not all(
            isinstance(test.get(k), str) and test[k].strip()
            for k in ("name", "result", "evidence_ref")
        ):
            raise ValueError("Each test requires name, result and evidence_ref")
        if test["result"] not in ("PASS", "FAIL", "SKIPPED"):
            raise ValueError("Invalid test result")
    if any(t["result"] != "PASS" for t in tests):
        return {"status": "TESTS_NOT_PASSED", "ready_for_human_review": False,
                "execution_authorized": False}
    # Test evidence references are unverified pointers until a trusted runner
    # independently validates them; a self-reported PASS is not proof.
    if record.get("trusted_runner_verified") is not True:
        return {"status": "EVIDENCE_UNVERIFIED", "ready_for_human_review": False,
                "execution_authorized": False}
    return {"status": "READY_FOR_HUMAN_REVIEW", "ready_for_human_review": True,
            "human_approval_recorded": record["human_approval"] is True,
            "execution_authorized": False}
