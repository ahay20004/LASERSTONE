def generate_hybrid_candidates(plants):

    hybrids = []

    total = len(plants)

    for i in range(total):

        for j in range(i + 1, total):

            plant1 = plants[i]
            plant2 = plants[j]

            score1 = plant1.get(
                "material_score", 0
            )

            score2 = plant2.get(
                "material_score", 0
            )

            lri1 = plant1.get(
                "lri_score", 0
            )

            lri2 = plant2.get(
                "lri_score", 0
            )

            hybrid_score = (
                score1 + score2 +
                lri1 + lri2
            ) / 4

            if hybrid_score >= 70:

                hybrid_name = (
                    f"{plant1['name']} + "
                    f"{plant2['name']}"
                )

                hybrids.append({

                    "hybrid": hybrid_name,

                    "score": round(
                        hybrid_score, 2
                    ),

                    "classification":
                    classify_hybrid(
                        hybrid_score
                    )
                })

    return hybrids


def classify_hybrid(score):

    if score >= 85:
        return "Advanced Hybrid Laser Material"

    elif score >= 70:
        return "Promising Hybrid Candidate"

    elif score >= 55:
        return "Experimental Hybrid System"

    else:
        return "Weak Hybrid Combination"