"""Stage 3.6: unified, version-bound theoretical audit report.

No scientific endorsement is inferred from passing synthetic or declared
numerical checks. Report preserves raw diagnostics and NOT_RUN states.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

def _module(name):
    spec = importlib.util.spec_from_file_location(name, HERE / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def _sha(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False,
                                     allow_nan=False).encode("utf-8")).hexdigest()

def build_report(proposal, dimensions=None, limit_case=None,
                 convergence=None, sensitivity=None):
    if all(x is None for x in (dimensions, limit_case, convergence, sensitivity)):
        raise ValueError("At least one executable audit specification is required")
    base = _module("theory_audit_pipeline")
    registry = _module("theory_incubator").register(proposal)
    report = {
        "theory_id": registry["theory_id"],
        "version": registry["version"],
        "proposal_sha256": registry["proposal_sha256"],
        "stage": "PROPOSED", "endorsement": "NONE",
        "checks": dict(registry["checks"]),
        "audit_results": {},
        "claims_authorized": [],
    }
    if dimensions is not None or limit_case is not None:
        mathematical = base.run_audit(proposal, dimensions, limit_case)
        report["checks"].update(mathematical["checks"])
        report["audit_results"].update(mathematical["audit_results"])
    numerical = _module("numerical_audit")
    for name, input_spec, operation in (
        ("numerical_convergence", convergence, numerical.convergence),
        ("parameter_sensitivity", sensitivity, numerical.sensitivity),
    ):
        if input_spec is not None:
            result = operation(input_spec)
            report["checks"][name] = result["status"]
            report["audit_results"][name] = {
                "input_sha256": _sha(input_spec), "result": result,
            }
    report["checks"].setdefault("parameter_sensitivity", "NOT_RUN")
    report["audit_sha256"] = _sha(report["audit_results"])
    report["summary"] = {
        "executed": len(report["audit_results"]),
        "not_run": sum(value == "NOT_RUN" for value in report["checks"].values()),
        "requires_investigation": sum(
            value in ("DIMENSIONAL_MISMATCH", "LIMIT_REQUIRES_INVESTIGATION",
                      "REFINEMENT_REQUIRES_INVESTIGATION")
            for value in report["checks"].values()),
    }
    report["caveats"] = [
        "Input specifications and computed samples are supplied by researchers, not independently authenticated.",
        "Numerical compatibility is not a proof of physical validity, novelty, reproducibility or experimental support.",
        "Reports do not automatically change theory maturity or authorize claims.",
    ]
    return report

def main():
    p = argparse.ArgumentParser()
    for arg in ("proposal", "dimensions", "limit-case", "convergence", "sensitivity", "out"):
        p.add_argument("--" + arg, required=arg in ("proposal", "out"))
    args = p.parse_args()
    def read(path):
        return json.loads(Path(path).read_text(encoding="utf-8")) if path else None
    result = build_report(read(args.proposal), read(args.dimensions),
                          read(args.limit_case), read(args.convergence),
                          read(args.sensitivity))
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    raise SystemExit(1 if result["summary"]["requires_investigation"] else 0)

if __name__ == "__main__":
    main()
