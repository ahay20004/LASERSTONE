def evaluate_photobleaching_stability(
    plant,
    thermal_score,
    feasibility_score
):

    score = 0

    # Quantum yield contribution
    if plant["phi"] >= 0.7:
        score += 30

    elif plant["phi"] >= 0.5:
        score += 20

    else:
        score += 10

    # Thermal stability contribution
    if thermal_score >= 80:
        score += 30

    elif thermal_score >= 60:
        score += 20

    else:
        score += 10

    # Feasibility contribution
    if feasibility_score >= 80:
        score += 25

    elif feasibility_score >= 60:
        score += 15

    else:
        score += 5

    # Non-radiative decay resistance
    if plant["knr"] <= 0.35:
        score += 15

    elif plant["knr"] <= 0.5:
        score += 10

    else:
        score += 5

    return min(score, 100)


def classify_photobleaching(score):

    if score >= 80:
        return "Excellent Photostability"

    elif score >= 60:
        return "Good Photostability"

    elif score >= 40:
        return "Moderate Photostability"

    else:
        return "Poor Photostability"