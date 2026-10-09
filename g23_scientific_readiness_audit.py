"""Read-only G23 scientific-readiness audit; does not validate laser physics."""
import ast
import json
from pathlib import Path

EXPECTED_DIRS = ("core", "data", "database", "docs", "ui", "reports")
CORE_FILES = ("project_registry.py", "registry_auto_builder.py", "gain_analysis.py", "data_validator.py")

def audit(root):
    root = Path(root).resolve()
    findings = []
    def flag(code, severity, path, detail):
        findings.append({"code": code, "severity": severity, "path": path, "detail": detail})
    for name in EXPECTED_DIRS:
        if (root / name).is_file():
            flag("DIRECTORY_NAME_IS_FILE", "warning", name, "Expected directory name is a file; compare with local authoritative project.")
    for name in CORE_FILES:
        if not (root / name).is_file():
            flag("MISSING_CORE_FILE", "warning", name, "Core audit target absent.")
    files = sorted(p for p in root.rglob("*.py") if not ({".git", "__pycache__", ".venv", "venv", "backup"} & set(p.relative_to(root).parts)))
    parsed = 0
    for path in files:
        rel = path.relative_to(root).as_posix()
        try:
            tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=rel)
        except (OSError, UnicodeError, SyntaxError) as exc:
            flag("SOURCE_PARSE_ERROR", "error", rel, str(exc))
            continue
        parsed += 1
        definitions = {}
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                definitions.setdefault(node.name, []).append(node.lineno)
        for symbol, lines in definitions.items():
            if len(lines) > 1:
                flag("DUPLICATE_TOP_LEVEL_DEFINITION", "warning", rel, f"{symbol}: lines {lines}")
    gain = root / "gain_analysis.py"
    if gain.is_file():
        source = gain.read_text(encoding="utf-8-sig", errors="replace")
        if "calculate_gain_potential" in source and "gain_score" in source:
            flag("GAIN_SCORE_NOT_PHYSICAL_GAIN", "critical", gain.name, "Heuristic gain_score is not physical optical gain in inverse length units.")
    validator = root / "data_validator.py"
    if validator.is_file():
        source = validator.read_text(encoding="utf-8-sig", errors="replace")
        if "REQUIRED_FIELDS" in source and "missing_fields" in source:
            flag("VALIDATOR_SCOPE_REVIEW", "warning", validator.name, "Check whether units, provenance, uncertainty and value origin are validated.")
    return {"schema": "laserstone.g23.audit.v1", "python_files": len(files),
            "parsed_python_files": parsed, "findings": findings,
            "verdict": "REQUIRES_SCIENTIFIC_REVIEW",
            "note": "Static screening only; not a publication or physical-validation clearance."}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root)
    if not root.is_dir():
        parser.error("--root must be an existing directory")
    print(json.dumps(audit(root), ensure_ascii=False, indent=2))
