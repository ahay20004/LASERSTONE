def audit_plant(plant):

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
            "Scientific audit completed "
            "successfully."
        )

    elif len(issues) <= 2:

        status = "WARNING"

    else:

        status = "REVIEW REQUIRED"

    return {

        "status": status,

        "issues": issues
    }