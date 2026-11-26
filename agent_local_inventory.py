"""Read-only local agent inventory. Never reads agent file contents or credentials."""
from __future__ import annotations
import json
import os
from pathlib import Path

CANDIDATES = (
    ("project", ".github/agents"),
    ("project", ".codex/agents"),
    ("project", ".claude/agents"),
    ("project", "agents"),
    ("project", "AGENTS.md"),
    ("project", ".github/copilot-instructions.md"),
    ("home", ".codex/agents"),
    ("home", ".config/Codex/agents"),
)
SUFFIXES = {".md", ".json", ".yaml", ".yml", ".toml"}

def inventory(root: Path, home: Path | None = None) -> dict:
    root = root.resolve()
    home = (home or Path.home()).resolve()
    entries = []
    for scope, relative in CANDIDATES:
        base = root if scope == "project" else home
        candidate = base / relative
        if not candidate.exists():
            continue
        # Never follow symlinks, recurse outside configured roots, or read contents.
        if candidate.is_symlink():
            entries.append({"scope": scope, "location": relative, "kind": "symlink_skipped"})
            continue
        if candidate.is_file():
            entries.append({"scope": scope, "location": relative, "kind": "configuration_file"})
        elif candidate.is_dir():
            names = sorted(p.name for p in candidate.iterdir()
                           if p.is_file() and not p.is_symlink() and p.suffix.lower() in SUFFIXES)
            entries.append({"scope": scope, "location": relative,
                            "kind": "configuration_directory", "file_names": names[:100],
                            "truncated": len(names) > 100})
    return {"schema": 1, "inventory": entries,
            "active_agents_verified": False, "agent_execution_attempted": False,
            "inspection_scope": "filenames_only", "machine": "local"}

def main() -> int:
    root = Path(__file__).resolve().parent
    result = inventory(root)
    destination = root / "agent_council_local_inventory.json"
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("LASERSTONE local agent inventory generated:", destination.name)
    print("Agent runtime and collaboration remain UNVERIFIED.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
