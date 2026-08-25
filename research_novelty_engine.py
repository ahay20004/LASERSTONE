def convert_quality_to_score(value):

    quality_map = {

        "Excellent": 100,

        "Very Good": 85,

        "Good": 75,

        "Moderate": 60,

        "Low": 40,

        "Weak": 25
    }

    if isinstance(value, (int, float)):
        return value

    return quality_map.get(value, 40)


def evaluate_research_novelty(plant):

    novelty_score = 0

    material_score = plant.get(
        "material_score", 0
    )

    lri = plant.get(
        "lri_score", 0
    )

    spectral_quality = (
        convert_quality_to_score(
            plant.get(
                "spectral_quality", 0
            )
        )
    )

    q_factor = plant.get(
        "q_factor_score", 0
    )

    # High-performance rare combination
    if (
        material_score > 80
        and lri > 80
    ):

        novelty_score += 35

    # Strong spectral behavior
    if spectral_quality > 75:

        novelty_score += 25

    # High cavity quality
    if q_factor > 75:

        novelty_score += 25

    # Experimental promise
    if plant.get(
        "experimental_success_score",
        0
    ) > 80:

        novelty_score += 15

    novelty_score = min(
        novelty_score,
        100
    )

    return novelty_score


def classify_research_novelty(score):

    if score >= 85:

        return (
            "Potential Breakthrough Material"
        )

    elif score >= 70:

        return (
            "Highly Novel Research Candidate"
        )

    elif score >= 55:

        return (
            "Scientifically Interesting Material"
        )

    else:

        return (
            "Conventional Research Material"
        )