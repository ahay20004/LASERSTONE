"""Master-manuscript contract for LASERSTONE research composition."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

MASTER_FILENAME = "LASERSTONE_PAPER1_MASTER.md"
REQUIRED_SECTION_HEADINGS = (
    "## Abstract",
    "## 1. Introduction",
    "## 2. Materials and Methods",
    "## 3. Results",
    "## 4. Discussion",
    "## 5. Conclusions",
    "## References",
    "## Master Manuscript Control",
)


def validate_master_manuscript(
    directive: Mapping[str, Any],
    manuscript_text: str,
) -> dict[str, Any]:
    if not isinstance(directive, Mapping):
        raise TypeError("directive must be a mapping")
    if not isinstance(manuscript_text, str):
        raise TypeError("manuscript_text must be text")

    errors: list[str] = []
    title = directive.get("title")

    if not isinstance(title, str) or not title.strip():
        errors.append("directive title is required")
    else:
        expected_heading = f"# {title.strip()}"
        first_line = manuscript_text.splitlines()[0].strip() if manuscript_text else ""
        if first_line != expected_heading:
            errors.append("master manuscript title does not match Research Directive")

    if directive.get("master_policy") != "ONE_RESEARCH_ONE_MASTER_ONE_EVIDENCE_TRAIL":
        errors.append("Research Directive does not enforce the one-master policy")

    for heading in REQUIRED_SECTION_HEADINGS:
        if heading not in manuscript_text:
            errors.append(f"required manuscript section missing: {heading}")

    if "This file is the single authoritative manuscript" not in manuscript_text:
        errors.append("authoritative-master declaration is missing")

    return {
        "valid": not errors,
        "errors": errors,
        "status": "MASTER_CONTRACT_PASSED" if not errors else "MASTER_CONTRACT_BLOCKED",
        "master_filename": MASTER_FILENAME,
        "title": title,
    }


def validate_master_file(
    directive: Mapping[str, Any],
    root: str | Path = ".",
) -> dict[str, Any]:
    path = Path(root) / MASTER_FILENAME
    if not path.is_file():
        return {
            "valid": False,
            "errors": [f"authoritative master not found: {MASTER_FILENAME}"],
            "status": "MASTER_CONTRACT_BLOCKED",
            "master_filename": MASTER_FILENAME,
            "title": directive.get("title"),
        }
    return validate_master_manuscript(
        directive,
        path.read_text(encoding="utf-8"),
    )
