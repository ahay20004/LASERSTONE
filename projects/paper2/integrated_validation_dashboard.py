"""Stage 4.0: read-only integrated scientific validation dashboard.

Summarizes upstream reports without manufacturing missing results or upgrading
scientific claims. Output is a portable JSON dashboard, not a certification.
"""
import argparse
import hashlib
import json
from pathlib import Path

STAGES = (
    ("unified", ("theory_id", "version", "proposal_sha256", "audit_sha256")),
    ("uncertainty", ("theory_id", "version", "proposal_sha256",
                     "upstream_audit_sha256", "evidence_input_sha256")),
    ("independent_review", ("theory_id", "version", "proposal_sha256",
                            "evidence_input_sha256", "review_input_sha256")),
    ("claims", ("theory_id", "version", "proposal_sha256",
                "evidence_input_sha256", "review_input_sha256", "claims_input_sha256")),
)


def _valid_text(v):
    return isinstance(v, str) and bool(v.strip())


def build(reports):
    if not isinstance(reports, dict) or not reports:
        raise ValueError("At least one stage report required")
    allowed = {name for name, _ in STAGES}
    if set(reports) - allowed:
        raise ValueError("Unknown stage report")
    reference = None
    stage_status = {}
    blockers = []
    for name, fields in STAGES:
        data = reports.get(name)
        if data is None:
            stage_status[name] = "NOT_RUN"
            blockers.append(name + ":NOT_RUN")
            continue
        if not isinstance(data, dict) or not all(_valid_text(data.get(f)) for f in fields):
            raise ValueError("Invalid " + name + " report")
        identity = tuple(data[k] for k in ("theory_id", "version", "proposal_sha256"))
        if reference is None:
            reference = identity
        elif identity != reference:
            raise ValueError("Cross-stage theory identity mismatch")
        if name == "unified":
            status = "REPORTED_WITHOUT_SCIENTIFIC_ENDORSEMENT"
            checks = data.get("checks", {})
            if not isinstance(checks, dict):
                raise ValueError("Invalid checks")
            if any(v != "PASS" for v in checks.values()):
                blockers.append("unified:INCOMPLETE_OR_NONPASS_CHECKS")
        elif name == "uncertainty":
            status = "DECLARED_COMPARISONS_UNAUTHENTICATED"
            if not isinstance(data.get("comparisons"), list) or not data["comparisons"]:
                raise ValueError("Missing uncertainty comparisons")
            if any(x.get("status") != "COMPARISON_RECORDED" for x in data["comparisons"]):
                blockers.append("uncertainty:UNRESOLVED_COMPARISON")
        elif name == "independent_review":
            status = "REVIEW_METADATA_UNAUTHENTICATED"
            if not isinstance(data.get("reviews"), list) or not data["reviews"]:
                raise ValueError("Missing review records")
            if any(x.get("status") != "INDEPENDENT_REVIEW_REPORTED_UNAUTHENTICATED"
                   for x in data["reviews"]):
                blockers.append("independent_review:INCOMPLETE_REVIEW_METADATA")
        else:
            status = "CLAIMS_NOT_AUTHORIZED"
            if data.get("publication_readiness") != "NOT_ESTABLISHED" or data.get("claims_authorized") != []:
                raise ValueError("Unexpected publication/claim authorization")
            if not isinstance(data.get("claim_assessments"), list) or not data["claim_assessments"]:
                raise ValueError("Missing claim assessments")
        stage_status[name] = status
    if reference is None:
        raise ValueError("No report provided")
    # Hash chain is checked where both adjacent stages are available.
    if reports.get("unified") and reports.get("uncertainty"):
        if reports["unified"]["audit_sha256"] != reports["uncertainty"]["upstream_audit_sha256"]:
            raise ValueError("Unified-to-uncertainty audit hash mismatch")
    if reports.get("uncertainty") and reports.get("independent_review"):
        if reports["uncertainty"]["evidence_input_sha256"] != reports["independent_review"]["evidence_input_sha256"]:
            raise ValueError("Uncertainty-to-review evidence hash mismatch")
    if reports.get("independent_review") and reports.get("claims"):
        for key in ("evidence_input_sha256", "review_input_sha256"):
            if reports["independent_review"][key] != reports["claims"][key]:
                raise ValueError("Review-to-claims hash mismatch: " + key)
    digest = hashlib.sha256(json.dumps(reports, sort_keys=True, ensure_ascii=False,
                                       allow_nan=False).encode("utf-8")).hexdigest()
    return {
        "theory_id": reference[0], "version": reference[1],
        "proposal_sha256": reference[2], "input_reports_sha256": digest,
        "stages": stage_status, "gaps": blockers,
        "technical_integration": "REPORTS_LINKED_NOT_INDEPENDENTLY_VERIFIED",
        "scientific_validity": "NOT_ESTABLISHED",
        "publication_readiness": "NOT_ESTABLISHED",
        "endorsement": "NONE", "claims_authorized": [],
    }


def main():
    p = argparse.ArgumentParser()
    for name, _ in STAGES:
        p.add_argument("--" + name.replace("_", "-"))
    p.add_argument("--out", required=True)
    args = p.parse_args()
    reports = {}
    for name, _ in STAGES:
        path = getattr(args, name)
        if path:
            reports[name] = json.loads(Path(path).read_text(encoding="utf-8"))
    result = build(reports)
    dest = Path(args.out)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
