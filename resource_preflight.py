"""Read-only resource readiness report; never downloads or activates resources."""
from pathlib import Path
from resource_catalog import DEFAULT_CATALOG
import json

def report(root, catalog=DEFAULT_CATALOG):
    resources = []
    for identifier, record in sorted(catalog.records.items()):
        try:
            state = catalog.inspect(root, identifier, record.version)
        except (OSError, ValueError) as exc:
            state = {"status":"CHECK_FAILED","integrity_verified":False,
                     "error_type":type(exc).__name__}
        resources.append({"identifier":identifier,"version":record.version,
                          "status":state["status"],
                          "integrity_verified":state["integrity_verified"],
                          "recovery":record.recovery})
    return {"resources":resources,"all_integrity_matched":bool(resources) and
            all(r["integrity_verified"] for r in resources),
            "activation_authorized":False}

if __name__ == "__main__":
    print(json.dumps(report(Path(__file__).resolve().parent),ensure_ascii=True,indent=2))
