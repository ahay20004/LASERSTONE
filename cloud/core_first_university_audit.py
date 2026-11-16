"""Read-only university asset assessment for CORE FIRST development.

Uses source text and AST only: no university imports, GUI startup or copying.
Candidates are NOT certified integrations; the campus remains unchanged.
"""
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIGNALS = {
    "scientific": ("physics", "simulation", "evidence", "research", "material", "laser"),
    "infrastructure": ("navigation", "library", "registry", "session", "validation"),
}


def assess_university_assets(root=ROOT):
    root = Path(root)
    city = root / "city"
    assets = []
    if city.is_dir():
        for path in sorted(city.glob("*.py")):
            try:
                source = path.read_text(encoding="utf-8-sig")
                tree = ast.parse(source, filename=str(path))
                defs = [node.name for node in tree.body
                        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
                        and not node.name.startswith("_")]
                imports = []
                for node in ast.walk(tree):
                    if isinstance(node, ast.ImportFrom) and node.module:
                        imports.append(node.module)
                    elif isinstance(node, ast.Import):
                        imports.extend(alias.name for alias in node.names)
                syntax = "AST_PARSED"
            except (OSError, UnicodeError, SyntaxError) as exc:
                source, defs, imports = "", [], []
                syntax = "PARSE_ERROR:" + type(exc).__name__
            tokens = (path.stem + " " + " ".join(defs)).lower()
            signals = sorted(key for key, words in SIGNALS.items()
                             if any(word in tokens for word in words))
            assets.append({
                "source": path.relative_to(root).as_posix(),
                "syntax": syntax,
                "public_definitions": defs,
                "imports": sorted(set(imports)),
                "candidate_signals": signals,
                "core_reuse_status": "REVIEW_ONLY" if signals and defs else "PRESERVE_ONLY",
                "university_original_modified": False,
                "core_integration_verified": False,
                "scientific_validation_verified": False,
            })
    return {
        "policy": "CORE_FIRST_UNIVERSITY_PRESERVED",
        "scope": "READ_ONLY_STATIC_ASSESSMENT",
        "university_files_assessed": len(assets),
        "review_candidates": sum(a["core_reuse_status"] == "REVIEW_ONLY" for a in assets),
        "approved_transfers": 0,
        "university_changes": 0,
        "assets": assets,
        "notes": [
            "Names and definitions indicate review candidates, not proven scientific utility.",
            "Do not copy university datasets, state, or engines without owner approval.",
            "Any future transfer requires source revision, rights review, contract and tests.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(assess_university_assets(), ensure_ascii=False, indent=2))
