"""Stage 3.4: bind executable audits to an immutable theory proposal identity.

Submitted specifications remain researcher-declared. Outputs are reproducible
records, not scientific endorsement or an automatic maturity transition.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

def _load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def _digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False,
                                     allow_nan=False).encode("utf-8")).hexdigest()

def run_audit(proposal, dimensional_spec=None, limit_case=None):
    registry = _load("theory_incubator").register(proposal)
    if dimensional_spec is None and limit_case is None:
        raise ValueError("At least one executable audit input is required")
    results = {}
    checks = dict(registry["checks"])
    if dimensional_spec is not None:
        result = _load("dimensional_validation").assess(dimensional_spec)
        results["dimensional_consistency"] = {
            "input_sha256": _digest(dimensional_spec), "result": result,
        }
        checks["dimensional_consistency"] = result["status"]
    if limit_case is not None:
        result = _load("limiting_case_validation").evaluate(limit_case)
        results["limiting_cases"] = {
            "input_sha256": _digest(limit_case), "result": result,
        }
        checks["limiting_cases"] = result["status"]
    return {
        "theory_id": registry["theory_id"],
        "version": registry["version"],
        "proposal_sha256": registry["proposal_sha256"],
        "audit_sha256": _digest(results),
        "stage": registry["stage"],
        "endorsement": registry["endorsement"],
        "checks": checks,
        "audit_results": results,
        "claims_authorized": [],
        "caveats": [
            "Audit inputs and parameter dimensions are researcher-declared and not independently authenticated.",
            "No mathematical proof, physical validation, novelty assessment or automatic theory promotion.",
            "Preserve all audit reports, including failures, with the associated proposal SHA-256.",
        ],
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--proposal", required=True)
    p.add_argument("--dimensions")
    p.add_argument("--limit-case")
    p.add_argument("--out", required=True)
    args = p.parse_args()
    def read(path):
        return json.loads(Path(path).read_text(encoding="utf-8")) if path else None
    report = run_audit(read(args.proposal), read(args.dimensions), read(args.limit_case))
    dest = Path(args.out)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    statuses = [item["result"]["status"] for item in report["audit_results"].values()]
    raise SystemExit(0 if all(x in ("DIMENSIONALLY_CONSISTENT", "NUMERICAL_LIMIT_COMPATIBLE")
                              for x in statuses) else 1)

if __name__ == "__main__":
    main()
