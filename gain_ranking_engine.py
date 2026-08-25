def calculate_gain_score(
    plant,
    lsi_value,
    feasibility_score,
    thermal_score,
    photobleaching_score
):

    score = 0

    # LSI contribution
    if lsi_value >= 5:
        score += 30

    elif lsi_value >= 2:
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

    # Thermal stability contribution
    if thermal_score >= 80:
        score += 20

    elif thermal_score >= 60:
        score += 12

    else:
        score += 5

    # Photobleaching resistance
    if photobleaching_score >= 80:
        score += 15

    elif photobleaching_score >= 60:
        score += 10

    else:
        score += 5

    # Quantum yield bonus
    if plant["phi"] >= 0.7:
        score += 10

    elif plant["phi"] >= 0.5:
        score += 5

    return min(score, 100)


def classify_gain_medium(score):

    if score >= 85:
        return "Excellent Gain Medium"

    elif score >= 70:
        return "Strong Gain Medium"

    elif score >= 50:
        return "Moderate Gain Medium"

    else:
        return "Weak Gain Medium"