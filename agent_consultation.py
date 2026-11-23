"""AC-03: evidence-preserving specialist consultation; no autonomous agent claims."""
from __future__ import annotations

def open_consultation(council: dict) -> dict:
    if council.get("review_status") != "READY_FOR_HUMAN_DECISION":
        raise ValueError("Independent specialist reviews must finish first")
    if council.get("human_decision") != "PENDING":
        raise ValueError("Council already decided")
    if council.get("consultation"):
        raise ValueError("Consultation already opened")
    reviews = council["reviews"]
    if not reviews:
        raise ValueError("No independent reviews")
    council["consultation"] = {
        "status": "AWAITING_SPECIALIST_RESPONSES",
        "issues": [{"raised_by": r["reviewer"], "position": r["position"],
                    "reason": r["reason"], "evidence": r["evidence"]} for r in reviews],
        "responses": [],
    }
    council["review_status"] = "CONSULTATION_IN_PROGRESS"
    return council

def respond(council: dict, response: dict) -> dict:
    session = council.get("consultation")
    if not session or session["status"] != "AWAITING_SPECIALIST_RESPONSES":
        raise ValueError("No open consultation")
    allowed = {r["reviewer"] for r in council["reviews"]}
    reviewer = response.get("reviewer")
    if reviewer not in allowed:
        raise ValueError("Only participating specialists may respond")
    if any(r["reviewer"] == reviewer for r in session["responses"]):
        raise ValueError("Specialist already responded")
    if not isinstance(response.get("analysis"), str) or not response["analysis"].strip():
        raise ValueError("Substantive analysis required")
    if response.get("position") not in ("approve", "revise", "reject"):
        raise ValueError("Invalid consultation position")
    addressed = response.get("addresses", [])
    if not isinstance(addressed, list) or any(x not in allowed for x in addressed):
        raise ValueError("Addresses must reference participating specialists")
    evidence = response.get("evidence", [])
    if not isinstance(evidence, list):
        raise ValueError("Evidence must be a list")
    session["responses"].append({"reviewer": reviewer, "analysis": response["analysis"],
                                 "position": response["position"], "addresses": addressed,
                                 "evidence": evidence})
    if {r["reviewer"] for r in session["responses"]} == allowed:
        positions = {r["position"] for r in session["responses"]}
        session["status"] = "COMPLETE"
        council["review_status"] = "READY_FOR_HUMAN_DECISION"
        council["recommendation"] = next(iter(positions)) if len(positions) == 1 else "DISAGREEMENT"
        council["consultation_disagreements"] = [
            r for r in session["responses"] if r["position"] != council["recommendation"]
        ] if council["recommendation"] != "DISAGREEMENT" else session["responses"][:]
    return council
