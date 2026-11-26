"""Structural charter gate, not scientific or release authorization."""
PATHWAYS = ("student", "educator", "researcher", "reviewer", "validation")
REQUIRED = ("module_id", "quantity_ids", "equation_ids", "sources",
            "validity_domain", "uncertainty_status", "evidence_status",
            "test_references")

def assess(manifest):
    errors = []
    if not isinstance(manifest, dict):
        raise ValueError("Expected module manifest")
    for key in REQUIRED:
        value = manifest.get(key)
        if key in ("quantity_ids", "equation_ids", "sources", "test_references"):
            valid = isinstance(value, list) and bool(value) and all(
                isinstance(x, str) and x.strip() for x in value)
        else:
            valid = isinstance(value, str) and bool(value.strip())
        if not valid:
            errors.append("Missing or invalid: " + key)
    paths = manifest.get("pathways")
    if not isinstance(paths, dict) or set(paths) != set(PATHWAYS):
        errors.append("Exactly five pathway declarations required")
    else:
        for key in PATHWAYS:
            item = paths[key]
            if not isinstance(item, dict):
                errors.append("Invalid pathway: " + key)
                continue
            status = item.get("status")
            detail = item.get("detail")
            if status not in ("documented", "not_applicable") or not isinstance(detail, str) or not detail.strip():
                errors.append("Missing pathway description or justification: " + key)
    return {"status": "DOCUMENTATION_COMPLETE" if not errors else "INCOMPLETE",
            "errors": errors, "scientific_validation": False,
            "release_authorized": False}
