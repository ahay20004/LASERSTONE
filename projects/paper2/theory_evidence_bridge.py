"""Theory-to-Evidence Bridge: conservative, auditable test-plan generator.

No symbolic equivalence, experimental authenticity, or novelty is asserted.
"""
import json
from pathlib import Path

try:
    from theory_incubator import register
except ImportError:
    import importlib.util
    spec = importlib.util.spec_from_file_location("theory_incubator", Path(__file__).with_name("theory_incubator.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    register = mod.register

CHECKS = {
    "dimensional_consistency": "Document dimensions of each term and each new parameter; compare LHS and RHS.",
    "reference_limit": "Specify a limiting operation that recovers the original equation and test it quantitatively.",
    "numerical_stability": "Test convergence, conditioning, parameter sensitivity and reproducibility.",
    "independent_benchmark": "Compare predictions against independently sourced measured or reference data with uncertainty.",
    "literature_positioning": "Identify closest prior work, distinctions, and claims supported by the citations.",
}

def build_bridge(proposal, evidence=None):
    registry = register(proposal)
    if evidence is None:
        evidence = {}
    if not isinstance(evidence, dict):
        raise ValueError("Evidence must be an object")
    unexpected = sorted(set(evidence) - set(CHECKS))
    if unexpected:
        raise ValueError("Unknown evidence checks: " + ", ".join(unexpected))
    checks = {}
    for name, instruction in CHECKS.items():
        item = evidence.get(name)
        if item is None:
            checks[name] = {"status": "NOT_SUBMITTED", "next_action": instruction}
            continue
        if not isinstance(item, dict) or set(item) != {"artifact_id", "method", "outcome"}:
            raise ValueError(name + " requires artifact_id, method, outcome")
        if any(not isinstance(item[k], str) or not item[k].strip() for k in item):
            raise ValueError(name + " evidence fields must be nonempty strings")
        checks[name] = {
            "status": "SUBMITTED_FOR_INDEPENDENT_REVIEW",
            "artifact_id": item["artifact_id"], "method": item["method"],
            "reported_outcome": item["outcome"],
            "next_action": "Independently inspect artifact, assumptions and source provenance",
        }
    return {
        "theory_id": registry["theory_id"],
        "version": registry["version"],
        "proposal_sha256": registry["proposal_sha256"],
        "stage": "PROPOSED",
        "evidence_review": checks,
        "falsifiable_predictions": proposal["falsifiable_predictions"],
        "observables": proposal["observables"],
        "claims_authorized": [],
        "endorsement": "NONE",
        "caveats": [
            "Submitted evidence is self-declared, not verified.",
            "No automatic scientific promotion, symbolic proof or literature novelty determination.",
            "Failures must be preserved and investigated, not silently discarded.",
        ],
    }

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--proposal", required=True)
    p.add_argument("--evidence")
    p.add_argument("--out", required=True)
    args = p.parse_args()
    proposal = json.loads(Path(args.proposal).read_text(encoding="utf-8"))
    evidence = json.loads(Path(args.evidence).read_text(encoding="utf-8")) if args.evidence else None
    result = build_bridge(proposal, evidence)
    target = Path(args.out)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
