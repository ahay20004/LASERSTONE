def evaluate_platform_evolution(
    ranked_plants
):

    if len(ranked_plants) == 0:

        return {
            "stage":
            "Initialization Phase",

            "description":
            "Platform contains insufficient "
            "scientific data."
        }

    avg_intelligence = sum(

        plant[
            "intelligence_summary"
        ][
            "intelligence_score"
        ]

        for plant in ranked_plants

    ) / len(ranked_plants)

    avg_confidence = sum(

        plant.get(
            "scientific_confidence_score",
            0
        )

        for plant in ranked_plants

    ) / len(ranked_plants)

    avg_integrity = sum(

        plant.get(
            "system_integrity_score",
            0
        )

        for plant in ranked_plants

    ) / len(ranked_plants)

    evolution_index = (

        avg_intelligence * 0.4 +

        avg_confidence * 0.3 +

        avg_integrity * 0.3
    )

    if evolution_index >= 90:

        stage = (
            "World-Class Scientific Platform"
        )

    elif evolution_index >= 80:

        stage = (
            "Advanced Autonomous "
            "Research Platform"
        )

    elif evolution_index >= 65:

        stage = (
            "Integrated Scientific "
            "Analysis Platform"
        )

    else:

        stage = (
            "Developing Research Platform"
        )

    return {

        "evolution_index":
        round(evolution_index, 2),

        "stage":
        stage
    }