def prepare_visualization_data(
    ranked_plants
):

    visualization_data = []

    for plant in ranked_plants:

        plant_data = {

            "name":
            plant.get("name", "Unknown"),

            "material_score":
            plant.get(
                "material_score", 0
            ),

            "intelligence":
            plant[
                "intelligence_summary"
            ][
                "intelligence_score"
            ],

            "confidence":
            plant.get(
                "scientific_confidence_score",
                0
            ),

            "integrity":
            plant.get(
                "system_integrity_score",
                0
            ),

            "experimental":
            plant.get(
                "experimental_success_score",
                0
            ),

            "novelty":
            plant.get(
                "research_novelty_score",
                0
            ),

            "patent":
            plant.get(
                "patent_potential_score",
                0
            ),

            "rank":
            plant.get(
                "global_rank", 0
            )
        }

        visualization_data.append(
            plant_data
        )

    return visualization_data