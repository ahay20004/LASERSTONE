from constants import (
    MATERIAL_SCORE_WEIGHTS,
    LRI_WEIGHTS,
    CONFIDENCE_WEIGHTS
)


def analyze_weight_distribution():

    suggestions = []

    # Material score analysis
    if MATERIAL_SCORE_WEIGHTS["efficiency"] < 0.25:

        suggestions.append(
            "Laser efficiency weight may "
            "benefit from slight increase."
        )

    if MATERIAL_SCORE_WEIGHTS["spectral"] < 0.10:

        suggestions.append(
            "Spectral contribution appears "
            "scientifically underweighted."
        )

    # LRI analysis
    if LRI_WEIGHTS["thermal"] < 0.20:

        suggestions.append(
            "Thermal readiness influence "
            "may require enhancement."
        )

    # Confidence analysis
    if (
        CONFIDENCE_WEIGHTS["consistency"]
        <
        0.20
    ):

        suggestions.append(
            "Physics consistency should "
            "remain highly influential."
        )

    if len(suggestions) == 0:

        suggestions.append(
            "Current configuration appears "
            "scientifically balanced."
        )

    return suggestions


def generate_self_optimization_report():

    report = {}

    report["optimization_suggestions"] = (
        analyze_weight_distribution()
    )

    report["optimization_status"] = (
        classify_optimization_state(
            len(
                report[
                    "optimization_suggestions"
                ]
            )
        )
    )

    return report


def classify_optimization_state(count):

    if count <= 1:
        return "Highly Optimized Configuration"

    elif count <= 3:
        return "Stable Scientific Configuration"

    else:
        return "Configuration Requires Review"