"""Read-only G23 integration audit for critical production call paths.

Reports source-level findings; does not execute main.py, mutate registries,
or certify scientific readiness. Static text matching is a screening aid.
"""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CHECKS = {
    "main.py": ("validate_plant_data", "evaluate_physics_consistency"),
    "dashboard.py": ("PROJECT_REGISTRY",),
    "laser_physics_engine.py": ("calculate_laser_physics",),
}


def audit_call_paths(root=ROOT):
    findings = {}
    for filename, symbols in CHECKS.items():
        path = Path(root) / filename
        if not path.is_file():
            findings[filename] = {"status": "MISSING", "symbols": {}}
            continue
        source = path.read_text(encoding="utf-8-sig")
        try:
            tree = ast.parse(source, filename=filename)
        except SyntaxError as exc:
            findings[filename] = {"status": "PARSE_ERROR", "error": str(exc)}
            continue
        references = {}
        for symbol in symbols:
            references[symbol] = sorted(set(
                node.lineno for node in ast.walk(tree)
                if isinstance(node, ast.Name) and node.id == symbol
            ))
        findings[filename] = {"status": "SCREENED", "symbols": references}
    return findings


if __name__ == "__main__":
    import json
    print(json.dumps(audit_call_paths(), indent=2, ensure_ascii=False))
