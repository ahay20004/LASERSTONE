def evaluate_thermal_stability(plant):

    score = 0

    # Quantum yield stability
    if plant["phi"] >= 0.7:
        score += 30
    elif plant["phi"] >= 0.5:
        score += 20
    else:
        score += 10

    # Fluorescence lifetime contribution
    if plant["tau"] >= 4:
        score += 25
    elif plant["tau"] >= 2:
        score += 15
    else:
        score += 5

    # Non-radiative decay losses
    if plant["knr"] <= 0.35:
        score += 25
    elif plant["knr"] <= 0.5:
        score += 15
    else:
        score += 5

    # Refractive index effect
    if plant["refractive_index"] <= 1.4:
        score += 20
    else:
        score += 10

    return min(score, 100)


def classify_thermal_stability(score):

    if score >= 80:
        return "Excellent Thermal Stability"

    elif score >= 60:
        return "Good Thermal Stability"

    elif score >= 40:
        return "Moderate Thermal Stability"

    else:
        return "Poor Thermal Stability"