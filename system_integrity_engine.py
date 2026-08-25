def evaluate_system_integrity(plant):

    integrity_score = 100

    warnings = []

    material = plant.get(
        "material_score", 0
    )

    lri = plant.get(
        "lri_score", 0
    )

    confidence = plant.get(
        "scientific_confidence_score", 0
    )

    consistency = plant.get(
        "physics_consistency_score", 0
    )

    experimental = plant.get(
        "experimental_success_score", 0
    )

    # Material vs LRI mismatch
    if abs(material - lri) > 35:

        integrity_score -= 15

        warnings.append(
            "Material score and LRI "
            "show significant mismatch."
        )

    # Low consistency
    if consistency < 60:

        integrity_score -= 20

        warnings.append(
            "Physical consistency is weak."
        )

    # Experimental contradiction
    if experimental > 80 and confidence < 60:

        integrity_score -= 20

        warnings.append(
            "Experimental prediction exceeds "
            "scientific confidence."
        )

    # Weak confidence
    if confidence < 50:

        integrity_score -= 15

        warnings.append(
            "Scientific confidence is limited."
        )

    integrity_score = max(
        integrity_score,
        0
    )

    if len(warnings) == 0:

        warnings.append(
            "System integrity is stable."
        )

    return {
        "score": round(integrity_score, 2),
        "warnings": warnings
    }


def classify_integrity(score):

    if score >= 90:
        return "Highly Stable Scientific System"

    elif score >= 75:
        return "Stable Analytical System"

    elif score >= 60:
        return "Moderately Stable System"

    else:
        return "System Requires Scientific Review"