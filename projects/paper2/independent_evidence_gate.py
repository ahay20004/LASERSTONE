"""Stage 3.8: conservative independent-evidence review gate.

All identifiers and attestations are self-declared until verified outside this
software. The gate never authenticates reviewer identity or awards scientific
endorsement solely on the basis of supplied metadata.
"""
import argparse
import hashlib
import json
from pathlib import Path


def _string(value):
    return isinstance(value, str) and bool(value.strip())


def classify(record):
    if not isinstance(record, dict):
        raise ValueError("Evidence must be an object")
    required = {"evidence_id", "source_id", "artifact_sha256", "submitter_id",
                "reviewer_id", "review_artifact_sha256", "review_scope",
                "review_outcome", "reviewer_independence_attestation"}
    if set(record) != required:
        raise ValueError("Evidence must contain exactly the declared fields")
    if not _string(record["evidence_id"]) or not _string(record["submitter_id"]):
        raise ValueError("Evidence and submitter identifiers are required")
    source = record["source_id"]
    artifact = record["artifact_sha256"]
    if source is not None and not _string(source):
        raise ValueError("source_id must be a string or null")
    if artifact is not None and (not isinstance(artifact, str) or
                                len(artifact) != 64 or
                                any(c not in "0123456789abcdef" for c in artifact)):
        raise ValueError("artifact_sha256 must be lowercase SHA-256 or null")
    reviewer = record["reviewer_id"]
    review_hash = record["review_artifact_sha256"]
    scope = record["review_scope"]
    outcome = record["review_outcome"]
    attested = record["reviewer_independence_attestation"]
    if reviewer is not None and not _string(reviewer):
        raise ValueError("reviewer_id must be string or null")
    if review_hash is not None and (not isinstance(review_hash, str) or
                                   len(review_hash) != 64 or
                                   any(c not in "0123456789abcdef" for c in review_hash)):
        raise ValueError("review_artifact_sha256 must be lowercase SHA-256 or null")
    if scope is not None and not _string(scope):
        raise ValueError("review_scope must be string or null")
    if outcome not in (None, "SUPPORTS_WITHIN_SCOPE", "DOES_NOT_SUPPORT", "INCONCLUSIVE"):
        raise ValueError("Unsupported review outcome")
    if not isinstance(attested, bool):
        raise ValueError("Independence attestation must be boolean")
    if reviewer is not None and reviewer == record["submitter_id"]:
        raise ValueError("Self-review cannot be labeled independent")
    if reviewer is None and (review_hash is not None or scope is not None or
                             outcome is not None or attested):
        raise ValueError("Reviewer identity required for any review metadata")
    documented = source is not None and artifact is not None
    review_complete = (documented and reviewer is not None and review_hash is not None
                       and scope is not None and outcome is not None and attested)
    if review_complete:
        status = "INDEPENDENT_REVIEW_REPORTED_UNAUTHENTICATED"
    elif documented:
        status = "SOURCE_DOCUMENTED_REVIEW_NOT_VERIFIED"
    else:
        status = "SUBMITTED_UNVERIFIED"
    return {
        "evidence_id": record["evidence_id"], "status": status,
        "source_documented": documented,
        "review_reported": review_complete,
        "review_outcome": outcome if review_complete else None,
        "reviewer_identity_authenticated": False,
        "artifact_contents_verified": False,
        "independence_verified": False,
        "scientific_validation": "NOT_ESTABLISHED",
        "claims_authorized": [],
        "next_action": ("Authenticate reviewer and artifact externally, inspect scope, "
                        "methods, provenance, uncertainty and conflicts of interest."
                        if review_complete else
                        "Complete evidence provenance and independent review documentation."),
    }


def bind_to_evidence_report(evidence_report, reviews):
    if not isinstance(evidence_report, dict):
        raise ValueError("Stage 3.7 report required")
    for field in ("theory_id", "version", "proposal_sha256",
                  "upstream_audit_sha256", "evidence_input_sha256"):
        if not _string(evidence_report.get(field)):
            raise ValueError("Missing Stage 3.7 binding: " + field)
    if not isinstance(reviews, list) or not reviews:
        raise ValueError("At least one evidence review required")
    ids = [r.get("evidence_id") if isinstance(r, dict) else None for r in reviews]
    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate evidence IDs")
    results = [classify(r) for r in reviews]
    digest = hashlib.sha256(json.dumps(reviews, sort_keys=True, ensure_ascii=False,
                                       allow_nan=False).encode("utf-8")).hexdigest()
    return {
        "theory_id": evidence_report["theory_id"],
        "version": evidence_report["version"],
        "proposal_sha256": evidence_report["proposal_sha256"],
        "upstream_audit_sha256": evidence_report["upstream_audit_sha256"],
        "evidence_input_sha256": evidence_report["evidence_input_sha256"],
        "review_input_sha256": digest, "reviews": results,
        "stage": "PROPOSED", "endorsement": "NONE",
        "claims_authorized": [],
        "caveat": "Self-declared independent reviews are not authenticated or scientific proof.",
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--evidence-report", required=True)
    p.add_argument("--reviews", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()
    report = bind_to_evidence_report(
        json.loads(Path(args.evidence_report).read_text(encoding="utf-8")),
        json.loads(Path(args.reviews).read_text(encoding="utf-8")))
    dest = Path(args.out)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
