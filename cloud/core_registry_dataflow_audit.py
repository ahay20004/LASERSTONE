"""Read-only registry dependency reconciliation for LASERSTONE Core.

Registry declarations are not runtime connections. No imports or execution
of scientific engines, simulators, dashboards or university modules.
"""
import ast
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def audit_registry(root=ROOT):
    root = Path(root)
    source = (root / "project_registry.py").read_text(encoding="utf-8-sig")
    tree = ast.parse(source)
    registry = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "PROJECT_REGISTRY" for t in node.targets
        ):
            registry = ast.literal_eval(node.value)
            break
    if not isinstance(registry, dict):
        raise ValueError("Literal PROJECT_REGISTRY not found")
    providers = defaultdict(list)
    for name, item in registry.items():
        for output in item.get("outputs", []):
            if isinstance(output, str):
                providers[output].append(name)
    rows = []
    for name, item in registry.items():
        inputs = item.get("inputs", [])
        unresolved = [v for v in inputs if v not in providers and v != "PROJECT_REGISTRY"]
        internal = {v: providers[v] for v in inputs if v in providers}
        rows.append({
            "registry_key": name,
            "declared_status": item.get("status"),
            "root_module_exists": (root / (name + ".py")).is_file(),
            "internal_input_providers": internal,
            "unresolved_input_names": unresolved,
            "runtime_verified": False,
            "physics_validated": False,
        })
    return {
        "scope": "DECLARED_DATAFLOW_ONLY",
        "registered_entries": len(registry),
        "entries_without_same_name_root_module": sorted(
            row["registry_key"] for row in rows if not row["root_module_exists"]
        ),
        "outputs_with_multiple_declared_providers": {
            key: names for key, names in sorted(providers.items()) if len(names) > 1
        },
        "inputs_without_declared_provider": sorted({
            v for row in rows for v in row["unresolved_input_names"]
        }),
        "rows": rows,
        "notes": [
            "Unresolved input names may be valid external data, not necessarily errors.",
            "A matching module name is not proof of a callable interface.",
            "No runtime, scientific, or university integration is certified.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(audit_registry(), ensure_ascii=False, indent=2))
