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


def generate_scientific_recommendations(plant):

    recommendations = []

    thermal = plant.get("thermal_score", 0)

    efficiency = plant.get(
        "laser_efficiency_score", 0
    )

    q_factor = plant.get(
        "q_factor_score", 0
    )

    spectral = convert_quality_to_score(
        plant.get("spectral_quality", 0)
    )

    if thermal < 60:
        recommendations.append(
            "Improve thermal stabilization "
            "through cooling optimization."
        )

    if efficiency < 70:
        recommendations.append(
            "Enhance optical pumping efficiency."
        )

    if q_factor < 65:
        recommendations.append(
            "Optimize resonator cavity design."
        )

    if spectral < 60:
        recommendations.append(
            "Improve spectral purity and "
            "reduce emission broadening."
        )

    if len(recommendations) == 0:
        recommendations.append(
            "Material shows strong laser potential "
            "with balanced scientific indicators."
        )

    return recommendations