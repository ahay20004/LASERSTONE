def discover_high_potential_patterns(plants):

    discoveries = []

    for plant in plants:

        material_score = plant.get(
            "material_score", 0
        )

        lri = plant.get("lri_score", 0)

        novelty = plant.get(
            "research_novelty_score", 0
        )

        patent = plant.get(
            "patent_potential_score", 0
        )

        if (
            material_score >= 80
            and lri >= 75
            and novelty >= 70
        ):

            discoveries.append(
                f"{plant['name']} shows "
                f"high-potential bio-laser behavior."
            )

        if patent >= 80:

            discoveries.append(
                f"{plant['name']} may represent "
                f"a future patent-class laser material."
            )

    if len(discoveries) == 0:

        discoveries.append(
            "No major autonomous discoveries detected."
        )

    return discoveries