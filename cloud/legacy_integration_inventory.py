"""Read-only inventory of LASERSTONE's existing engines and integration evidence.

No engine imports, GUI startup, simulator execution, network requests, or file writes.
This is a source-level inventory, NOT a runtime/physics validation certificate.
"""
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUFFIXES = ("_engine.py", "_hub.py", "_advisor.py", "_optimizer.py",
            "_validator.py", "_scanner.py")
SIMULATORS = ("python", "matlab", "scaps-1d", "comsol", "zemax", "lumerical")


def _parse(path):
    try:
        return ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    except (SyntaxError, UnicodeError, OSError) as exc:
        return {"parse_error": type(exc).__name__ + ": " + str(exc)}


def _registry_entries():
    path = ROOT / "project_registry.py"
    tree = _parse(path)
    if not isinstance(tree, ast.Module):
        return {}, {"registry": "unreadable"}
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "PROJECT_REGISTRY"
            for target in node.targets
        ):
            if not isinstance(node.value, ast.Dict):
                return {}, {"registry": "nonliteral dictionary"}
            entries, duplicate_keys = {}, []
            for key, value in zip(node.value.keys, node.value.values):
                if not isinstance(key, ast.Constant) or not isinstance(key.value, str):
                    continue
                if key.value in entries:
                    duplicate_keys.append(key.value)
                try:
                    entries[key.value] = ast.literal_eval(value)
                except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
                    entries[key.value] = {"parse_status": "NON_LITERAL"}
            return entries, {"duplicate_keys": sorted(set(duplicate_keys))}
    return {}, {"registry": "PROJECT_REGISTRY not found"}


def build_inventory(root=ROOT):
    root = Path(root)
    # Explicit root injection supports isolated regression tests.
    entries = {}
    registry_file = root / "project_registry.py"
    if registry_file.exists():
        tree = _parse(registry_file)
        if isinstance(tree, ast.Module):
            for node in tree.body:
                if isinstance(node, ast.Assign) and any(
                    isinstance(target, ast.Name) and target.id == "PROJECT_REGISTRY"
                    for target in node.targets
                ) and isinstance(node.value, ast.Dict):
                    for key, value in zip(node.value.keys, node.value.values):
                        if isinstance(key, ast.Constant) and isinstance(key.value, str):
                            try:
                                entries[key.value] = ast.literal_eval(value)
                            except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
                                entries[key.value] = {"parse_status": "NON_LITERAL"}
                    break
    files = sorted(path for path in root.glob("*.py")
                   if path.name.endswith(SUFFIXES))
    inventory = []
    for path in files:
        parsed = _parse(path)
        names = ([node.name for node in parsed.body
                  if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
                 if isinstance(parsed, ast.Module) else [])
        stem = path.stem
        registry = entries.get(stem)
        inventory.append({
            "module": stem,
            "file": path.name,
            "syntax": "AST_PARSED" if isinstance(parsed, ast.Module) else "PARSE_ERROR",
            "public_definitions": [name for name in names if not name.startswith("_")],
            "registry_declared": registry is not None,
            "registry_status_claim": registry.get("status") if isinstance(registry, dict) else None,
            "runtime_tested": "NOT_ESTABLISHED_BY_INVENTORY",
            "experimentally_validated": "NOT_ESTABLISHED_BY_INVENTORY",
            "cloud_connected": False,
        })
    modules = {item["module"] for item in inventory}
    registry_missing_files = sorted(name for name in entries
                                    if not (root / (name + ".py")).is_file())
    return {
        "scope": "SOURCE_INVENTORY_ONLY",
        "root_engine_like_files": len(files),
        "registry_entries": len(entries),
        "registry_missing_corresponding_root_py": registry_missing_files,
        "registry_engine_like_files": len(modules.intersection(entries)),
        "simulator_contract_identifiers": list(SIMULATORS),
        "simulator_execution_verified": False,
        "public_preview_live_engines": False,
        "university_view": "LOCAL_GUI_DOCUMENTED_NOT_CLOUD_DEPLOYED",
        "notes": [
            "Registry ACTIVE is a declaration, not an executed integration test.",
            "Root file suffixes include support utilities and are not a unique-engine count.",
            "Simulation envelope support does not establish installed software or working adapters.",
            "Windows GUI and external simulator availability require separate local checks.",
        ],
        "inventory": inventory,
    }


if __name__ == "__main__":
    print(json.dumps(build_inventory(), ensure_ascii=False, indent=2))
