def generate_recommendations(ranked_plants):

    if not ranked_plants:

        return {
            "recommended_material": "N/A",
            "best_overall_material": "N/A",
            "best_patent_candidate": "N/A",
            "system_assessment": "NO DATA"
        }

    recommended_material = ranked_plants[0]

    best_patent_candidate = max(
        ranked_plants,
        key=lambda plant: plant.get(
            "patent_potential_score",
            0
        )
    )

    recommendations = {

        "recommended_material":
        recommended_material.get(
            "name",
            "N/A"
        ),

        "best_overall_material":
        recommended_material.get(
            "name",
            "N/A"
        ),

        "best_patent_candidate":
        best_patent_candidate.get(
            "name",
            "N/A"
        ),

        "system_assessment":
        "READY FOR EXPANSION"
    }

    return recommendations