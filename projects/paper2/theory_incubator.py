"""LASERSTONE Theory Incubator: non-destructive hypothesis registry.

Registration is not scientific endorsement. Invalid or unverified ideas remain
traceable; only explicitly assessed evidence can change maturity state.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

STAGES = ("PROPOSED", "FORMAL_REVIEW", "NUMERICALLY_TESTED",
          "EXPERIMENTALLY_SUPPORTED", "RESTRICTED", "FALSIFIED")
REQUIRED = ("theory_id", "title", "original_equation", "proposed_equation",
            "modification_rationale", "assumptions", "domain_of_validity",
            "observables", "falsifiable_predictions", "source_references",
            "author", "version")

def register(proposal):
    if not isinstance(proposal, dict):
        raise ValueError("Proposal must be an object")
    missing = [key for key in REQUIRED if key not in proposal]
    if missing:
        raise ValueError("Missing fields: " + ", ".join(missing))
    for key in ("theory_id", "title", "original_equation", "proposed_equation",
                "modification_rationale", "author", "version"):
        if not isinstance(proposal[key], str) or not proposal[key].strip():
            raise ValueError(key + " must be a nonempty string")
    for key in ("assumptions", "domain_of_validity", "observables",
                "falsifiable_predictions", "source_references"):
        if not isinstance(proposal[key], list) or not proposal[key]:
            raise ValueError(key + " must be a nonempty list")
        if any(not isinstance(v, str) or not v.strip() for v in proposal[key]):
            raise ValueError(key + " entries must be nonempty strings")
    canonical = json.dumps(proposal, sort_keys=True, ensure_ascii=False, allow_nan=False)
    return {
        "theory_id": proposal["theory_id"],
        "version": proposal["version"],
        "proposal_sha256": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
        "stage": "PROPOSED",
        "endorsement": "NONE",
        "checks": {
            "dimensional_consistency": "NOT_RUN",
            "limiting_cases": "NOT_RUN",
            "mathematical_consistency": "NOT_RUN",
            "numerical_convergence": "NOT_RUN",
            "independent_experimental_comparison": "NOT_RUN",
            "literature_novelty_review": "NOT_RUN",
        },
        "development_bridges": [
            "Specify units and dimensions for all variables and parameters",
            "Derive limiting-case recovery of the reference model",
            "Define quantitative falsifiable observables and uncertainty budget",
            "Compare against independently sourced benchmark data",
            "Identify required experiments, instrumentation and validity boundaries",
            "Map claims to prior literature and potential application domains",
        ],
        "claims_authorized": [],
        "caveat": "Registration preserves a hypothesis; it does not validate or endorse it.",
    }

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--proposal", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()
    proposal = json.loads(Path(args.proposal).read_text(encoding="utf-8"))
    result = register(proposal)
    target = Path(args.out)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
