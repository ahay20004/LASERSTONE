def generate_strategic_advice(
    ranked_plants
):

    advice = []

    if len(ranked_plants) == 0:

        advice.append(
            "No materials available for "
            "strategic evaluation."
        )

        return advice

    top_material = ranked_plants[0]

    top_score = top_material.get(
        "material_score", 0
    )

    top_patent = top_material.get(
        "patent_potential_score", 0
    )

    top_confidence = top_material.get(
        "scientific_confidence_score", 0
    )

    # Material quality
    if top_score >= 85:

        advice.append(
            "Platform contains elite "
            "laser material candidates."
        )

    # Patent potential
    if top_patent >= 80:

        advice.append(
            "Patent-oriented development "
            "is strongly recommended."
        )

    # Scientific confidence
    if top_confidence >= 85:

        advice.append(
            "Scientific stability supports "
            "future publication readiness."
        )

    # Dataset size
    if len(ranked_plants) < 10:

        advice.append(
            "Expanding the botanical dataset "
            "is recommended."
        )

    if len(advice) == 0:

        advice.append(
            "Platform remains in exploratory "
            "scientific mode."
        )

    return advice