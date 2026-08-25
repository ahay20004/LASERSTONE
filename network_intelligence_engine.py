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


def calculate_similarity(
    plant_a,
    plant_b
):

    similarity = 0

    # Material score similarity
    similarity += 100 - abs(

        plant_a.get(
            "material_score", 0
        )

        -

        plant_b.get(
            "material_score", 0
        )
    )

    # Spectral similarity
    spectral_a = (
        convert_quality_to_score(

            plant_a.get(
                "spectral_quality", 0
            )
        )
    )

    spectral_b = (
        convert_quality_to_score(

            plant_b.get(
                "spectral_quality", 0
            )
        )
    )

    similarity += 100 - abs(
        spectral_a - spectral_b
    )

    # Q-factor similarity
    similarity += 100 - abs(

        plant_a.get(
            "q_factor_score", 0
        )

        -

        plant_b.get(
            "q_factor_score", 0
        )
    )

    return round(similarity / 3, 2)


def build_material_network(
    ranked_plants
):

    network = []

    for i in range(
        len(ranked_plants)
    ):

        for j in range(
            i + 1,
            len(ranked_plants)
        ):

            plant_a = ranked_plants[i]

            plant_b = ranked_plants[j]

            similarity_score = (
                calculate_similarity(
                    plant_a,
                    plant_b
                )
            )

            if similarity_score >= 70:

                network.append({

                    "material_a":
                    plant_a["name"],

                    "material_b":
                    plant_b["name"],

                    "similarity":
                    similarity_score
                })

    return network