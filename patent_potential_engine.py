def evaluate_patent_potential(plant):

    patent_score = 0

    novelty = plant.get(
        "research_novelty_score", 0
    )

    lri = plant.get("lri_score", 0)

    architecture = plant.get(
        "laser_architecture", ""
    )

    consistency = plant.get(
        "physics_consistency_score", 0
    )

    # Strong novelty
    if novelty >= 80:
        patent_score += 40

    elif novelty >= 65:
        patent_score += 25

    # High readiness
    if lri >= 75:
        patent_score += 25

    # Stable physics
    if consistency >= 80:
        patent_score += 20

    # Advanced architecture
    if (
        "Tunable" in architecture
        or "Prototype" in architecture
    ):
        patent_score += 15

    patent_score = min(patent_score, 100)

    return patent_score


def classify_patent_potential(score):

    if score >= 85:
        return "Strong Patent Potential"

    elif score >= 70:
        return "Promising Intellectual Property"

    elif score >= 55:
        return "Possible Research Patent Candidate"

    else:
        return "Low Patent Potential"