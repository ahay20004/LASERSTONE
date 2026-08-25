def rank_plants(plants):

    ranked = sorted(
        plants,
        key=lambda x: x["material_score"],
        reverse=True
    )

    rank = 1

    for plant in ranked:

        plant["global_rank"] = rank

        rank += 1

    return ranked