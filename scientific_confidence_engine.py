from constants import (
    CONFIDENCE_WEIGHTS,
    THRESHOLDS
)


def calculate_scientific_confidence(plant):

    confidence = 50

    consistency = plant.get(
        "physics_consistency_score", 0
    )

    experimental = plant.get(
        "experimental_success_score", 0
    )

    novelty = plant.get(
        "research_novelty_score", 0
    )

    patent = plant.get(
        "patent_potential_score", 0
    )

    # Physics consistency
    confidence += (

        consistency *

        CONFIDENCE_WEIGHTS["consistency"]
    )

    # Experimental prediction
    confidence += (

        experimental *

        CONFIDENCE_WEIGHTS["experimental"]
    )

    # Research novelty
    confidence += (

        novelty *

        CONFIDENCE_WEIGHTS["novelty"]
    )

    # Patent potential
    confidence += (

        patent *

        CONFIDENCE_WEIGHTS["patent"]
    )

    confidence = min(confidence, 100)

    return round(confidence, 2)


def classify_confidence(score):

    if score >= THRESHOLDS["elite"]:

        return (
            "Extremely High Scientific "
            "Confidence"
        )

    elif score >= THRESHOLDS["advanced"]:

        return (
            "High Scientific Confidence"
        )

    elif score >= THRESHOLDS["promising"]:

        return (
            "Moderate Scientific Confidence"
        )

    else:

        return (
            "Preliminary Scientific Confidence"
        )