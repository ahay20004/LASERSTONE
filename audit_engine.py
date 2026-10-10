import math

def audit_plant(plant):

    fields = ("material_score", "scientific_confidence_score", "system_integrity_score", "experimental_success_score")
    invalid = []
    for field in fields:
        value = plant.get(field)
        if (isinstance(value, bool) or not isinstance(value, (int, float))
                or not math.isfinite(value) or not 0 <= value <= 100):
            invalid.append(field)
    if plant.get("valid") is False or plant.get("analysis_status") == "BLOCKED" or invalid:
        return {"status": "BLOCKED", "issues": ["Incomplete or blocked analysis: " + ", ".join(invalid)],
                "basis": "HEURISTIC_SCREEN_ONLY"}
    issues = []

    material = plant.get(
        "material_score", 0
    )

    confidence = plant.get(
        "scientific_confidence_score", 0
    )

    integrity = plant.get(
        "system_integrity_score", 0
    )

    experimental = plant.get(
        "experimental_success_score", 0
    )

    # Material quality
    if material < 50:

        issues.append(
            "Weak material performance."
        )

    # Confidence check
    if confidence < 60:

        issues.append(
            "Scientific confidence is limited."
        )

    # Integrity check
    if integrity < 70:

        issues.append(
            "System integrity requires review."
        )

    # Experimental prediction
    if experimental < 55:

        issues.append(
            "Experimental success probability "
            "is relatively low."
        )

    # Final audit status
    if len(issues) == 0:

        status = "PASS"

        issues.append(
            "Heuristic score screening completed "
            "successfully."
        )

    elif len(issues) <= 2:

        status = "WARNING"

    else:

        status = "REVIEW REQUIRED"

    return {

        "basis": "HEURISTIC_SCREEN_ONLY",
        "status": status,

        "issues": issues
    }
