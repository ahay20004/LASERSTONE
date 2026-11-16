"""Generate reproducible CI artifacts from the read-only full engine audit."""
import json
from pathlib import Path
from cloud.full_engine_audit import audit, markdown_report


def main():
    result = audit()
    dest = Path("audit-artifacts")
    dest.mkdir(exist_ok=True)
    (dest / "engine_inventory.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (dest / "ENGINE_AUDIT_REPORT.md").write_text(
        markdown_report(result), encoding="utf-8"
    )
    print(json.dumps(result["summary"], indent=2))
    if result["parse_errors"]:
        raise SystemExit("Python parse errors found: see engine_inventory.json")


if __name__ == "__main__":
    main()
