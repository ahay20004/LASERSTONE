"""Read-only whole-repository Python callable, registry and main.py audit.

AST only: never imports project modules or invokes engines, GUIs or simulators.
The output is structural evidence, not runtime or scientific certification.
"""
import ast
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", "__pycache__", ".venv", "venv", ".tox"}


def _files(root):
    return sorted(p for p in root.rglob("*.py")
                  if not any(part in EXCLUDED for part in p.relative_to(root).parts))


def _assigned_names(node):
    names = []
    for target in node.targets if isinstance(node, ast.Assign) else [node.target]:
        names.extend(n.id for n in ast.walk(target) if isinstance(n, ast.Name))
    return names


def _registry(root):
    tree = ast.parse((root / "project_registry.py").read_text(encoding="utf-8-sig"))
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)) and "PROJECT_REGISTRY" in _assigned_names(node):
            value = ast.literal_eval(node.value)
            if not isinstance(value, dict):
                raise ValueError("PROJECT_REGISTRY is not a literal dict")
            return value
    raise ValueError("PROJECT_REGISTRY literal not found")


def _signature(node):
    args = node.args
    pos = [a.arg for a in args.posonlyargs + args.args]
    kwonly = [a.arg for a in args.kwonlyargs]
    required = pos[:len(pos) - len(args.defaults)] + [
        a.arg for a, default in zip(args.kwonlyargs, args.kw_defaults) if default is None
    ]
    return {"positional": pos, "keyword_only": kwonly, "required": required,
            "vararg": args.vararg.arg if args.vararg else None,
            "kwarg": args.kwarg.arg if args.kwarg else None}


def audit(root=ROOT):
    root = Path(root)
    registry = _registry(root)
    files, parse_errors, module_functions, definitions = [], [], {}, []
    for path in _files(root):
        rel = path.relative_to(root).as_posix()
        try:
            tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=rel)
        except (SyntaxError, UnicodeError) as exc:
            parse_errors.append({"file": rel, "error": type(exc).__name__})
            continue
        files.append(rel)
        funcs = {}
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                funcs[node.name] = _signature(node)
                definitions.append({"file": rel, "qualname": node.name,
                                    "line": node.lineno, "signature": funcs[node.name]})
            elif isinstance(node, ast.ClassDef):
                for member in node.body:
                    if isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        definitions.append({"file": rel, "qualname": node.name + "." + member.name,
                                            "line": member.lineno, "signature": _signature(member)})
        module_functions[rel] = funcs
    main_tree = ast.parse((root / "main.py").read_text(encoding="utf-8-sig"))
    imports = defaultdict(set)
    module_aliases = {}
    for node in ast.walk(main_tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            for alias in node.names:
                imports[alias.asname or alias.name].add((node.module, alias.name))
        elif isinstance(node, ast.Import):
            for alias in node.names:
                module_aliases[alias.asname or alias.name.split(".")[0]] = alias.name
    calls = defaultdict(list)
    for node in ast.walk(main_tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                for module, symbol in imports.get(node.func.id, ()):
                    calls[module].append({"symbol": symbol, "line": node.lineno,
                                          "form": "imported_symbol"})
            elif isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                module = module_aliases.get(node.func.value.id)
                if module:
                    calls[module].append({"symbol": node.func.attr, "line": node.lineno,
                                          "form": "module_attribute"})
    providers = defaultdict(set)
    for name, entry in registry.items():
        for output in entry.get("outputs", []):
            providers[output].add(name)
    edges = sorted({(source, dest, field) for dest, entry in registry.items()
                    for field in entry.get("inputs", [])
                    for source in providers.get(field, ())
                    if source != dest})
    connected = {name for source, dest, _ in edges for name in (source, dest)}
    rows = []
    for name, entry in sorted(registry.items()):
        rel = name + ".py"
        actual = module_functions.get(rel, {})
        declared_inputs = list(entry.get("inputs", []))
        rows.append({
            "name": name, "declared_status": entry.get("status"),
            "file_exists": (root / rel).is_file(),
            "top_level_callables": sorted(actual),
            "main_static_call_sites": sorted(calls.get(name, []), key=lambda x: x["line"]),
            "declared_inputs": declared_inputs, "declared_outputs": entry.get("outputs", []),
            "declared_graph_connected": name in connected,
            "signature_contract_verified": False,
            "runtime_verified_by_this_audit": False,
            "physics_validated_by_this_audit": False,
        })
    return {
        "scope": "STATIC_AST_INVENTORY_ONLY",
        "summary": {
            "python_files_parsed": len(files), "python_parse_errors": len(parse_errors),
            "callable_definitions_including_methods": len(definitions),
            "registry_entries": len(registry),
            "registry_entries_with_root_file": sum(row["file_exists"] for row in rows),
            "registry_entries_with_main_static_calls": sum(bool(row["main_static_call_sites"]) for row in rows),
            "declared_edges": len(edges), "declared_connected_entries": len(connected),
            "declared_isolated_entries": len(registry) - len(connected),
        },
        "files": files, "parse_errors": parse_errors, "definitions": definitions,
        "registry_rows": rows,
        "declared_edges": [{"source": s, "target": t, "field": f} for s, t, f in edges],
        "main_imported_calls": {name: sorted(items, key=lambda x: x["line"])
                                for name, items in sorted(calls.items())},
        "notes": [
            "A static main.py call site does not establish reachability or successful execution.",
            "Registry inputs/outputs are declarations, not necessarily Python function arguments.",
            "Imports within nested scopes, dynamic dispatch and indirect calls may be missed.",
            "No experimental, numerical or simulator validation is established by this audit.",
            "All project Python files are parsed read-only, including university files.",
        ],
    }


def markdown_report(result):
    s = result["summary"]
    lines = ["# LASERSTONE core engine audit — static inventory",
             "", "Generated from repository source with AST only; no engine executed.",
             "", "## Summary", ""]
    lines += [f"- {k}: **{v}**" for k, v in s.items()]
    lines += ["", "## Registered modules", "",
              "| Module | File | Top-level functions | Main call sites | Registry graph |",
              "|---|---|---:|---:|---|"]
    for row in result["registry_rows"]:
        lines.append(f"| `{row['name']}` | {'yes' if row['file_exists'] else 'no'} | "
                     f"{len(row['top_level_callables'])} | {len(row['main_static_call_sites'])} | "
                     f"{'connected' if row['declared_graph_connected'] else 'isolated'} |")
    lines += ["", "## Important limitations", ""]
    lines += [f"- {note}" for note in result["notes"]]
    lines += ["", "Detailed definitions, signatures, declared edges and main call sites "
              "are in the accompanying JSON report.", ""]
    return "\n".join(lines)


if __name__ == "__main__":
    result = audit()
    print(markdown_report(result))
