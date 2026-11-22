"""Stage 3.9: conservative scientific-claim and publication-readiness gate.

A gate cannot verify scientific novelty, journal compliance, or experimental
truth. It reports missing prerequisites and never auto-authorizes claims.
"""
import argparse
import hashlib
import json
from pathlib import Path

ALLOWED = {"THEORETICAL", "NUMERICAL", "EXPERIMENTAL", "COMPARATIVE"}
REQUIRED = {"claim_id", "claim_text", "claim_type", "evidence_ids",
            "equation_ids", "conditions_ids", "limitations", "novelty_reference_ids"}
REPORT_FIELDS = {"theory_id", "version", "proposal_sha256",
                 "evidence_input_sha256", "review_input_sha256", "reviews"}


def _nonblank(x):
    return isinstance(x, str) and bool(x.strip())


def _ids(x):
    return isinstance(x, list) and bool(x) and all(_nonblank(y) for y in x) and len(set(x)) == len(x)


def assess(evidence_review_report, claims):
    if not isinstance(evidence_review_report, dict) or not REPORT_FIELDS.issubset(evidence_review_report):
        raise ValueError("Stage 3.8 evidence review report required")
    for field in REPORT_FIELDS - {"reviews"}:
        if not _nonblank(evidence_review_report[field]):
            raise ValueError("Missing report binding: " + field)
    reviews = evidence_review_report["reviews"]
    if not isinstance(reviews, list) or not reviews:
        raise ValueError("At least one review record required")
    review_by_id = {}
    for r in reviews:
        if not isinstance(r, dict) or not _nonblank(r.get("evidence_id")) or r["evidence_id"] in review_by_id:
            raise ValueError("Review evidence IDs must be unique and nonempty")
        review_by_id[r["evidence_id"]] = r
    if not isinstance(claims, list) or not claims:
        raise ValueError("At least one scientific claim required")
    output = []
    seen = set()
    for claim in claims:
        if not isinstance(claim, dict) or set(claim) != REQUIRED:
            raise ValueError("Claim schema mismatch")
        if not _nonblank(claim["claim_id"]) or not _nonblank(claim["claim_text"]):
            raise ValueError("Claim ID and text required")
        if claim["claim_id"] in seen:
            raise ValueError("Duplicate claim ID")
        seen.add(claim["claim_id"])
        if claim["claim_type"] not in ALLOWED:
            raise ValueError("Unknown claim type")
        if not _ids(claim["evidence_ids"]) or not _ids(claim["equation_ids"]) or not _ids(claim["conditions_ids"]):
            raise ValueError("Evidence, equation, and condition references required")
        if not _nonblank(claim["limitations"]) or not _ids(claim["novelty_reference_ids"]):
            raise ValueError("Limitations and prior-art references required")
        unknown = sorted(set(claim["evidence_ids"]) - set(review_by_id))
        reported = [review_by_id[eid] for eid in claim["evidence_ids"] if eid in review_by_id]
        incomplete = sorted(r["evidence_id"] for r in reported if r.get("status") != "INDEPENDENT_REVIEW_REPORTED_UNAUTHENTICATED")
        blockers = []
        if unknown:
            blockers.append("UNKNOWN_EVIDENCE_IDS")
        if incomplete:
            blockers.append("INCOMPLETE_REVIEW_METADATA")
        # Even a reported independent review is not authenticated by Stage 3.8.
        blockers.extend(["INDEPENDENT_AUTHENTICATION_NOT_ESTABLISHED",
                         "NOVELTY_NOT_INDEPENDENTLY_ASSESSED",
                         "CLAIM_NOT_EXTERNALLY_VERIFIED"])
        output.append({
            "claim_id": claim["claim_id"], "claim_type": claim["claim_type"],
            "evidence_ids": claim["evidence_ids"],
            "unknown_evidence_ids": unknown,
            "incomplete_review_evidence_ids": incomplete,
            "status": "NOT_AUTHORIZED_FOR_PUBLICATION_CLAIM",
            "blockers": blockers,
            "claims_authorized": [],
        })
    digest = hashlib.sha256(json.dumps(claims, sort_keys=True, ensure_ascii=False,
                                       allow_nan=False).encode("utf-8")).hexdigest()
    return {
        "theory_id": evidence_review_report["theory_id"],
        "version": evidence_review_report["version"],
        "proposal_sha256": evidence_review_report["proposal_sha256"],
        "evidence_input_sha256": evidence_review_report["evidence_input_sha256"],
        "review_input_sha256": evidence_review_report["review_input_sha256"],
        "claims_input_sha256": digest, "claim_assessments": output,
        "publication_readiness": "NOT_ESTABLISHED",
        "novelty_assessment": "NOT_VERIFIED",
        "endorsement": "NONE", "claims_authorized": [],
        "caveat": "Automated metadata checks cannot establish originality, truth, or journal acceptance.",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--review-report", required=True)
    parser.add_argument("--claims", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    report = assess(json.loads(Path(args.review_report).read_text(encoding="utf-8")),
                    json.loads(Path(args.claims).read_text(encoding="utf-8")))
    dest = Path(args.out)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
