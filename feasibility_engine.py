def calculate_feasibility_score(plant, lsi_value, pump_source):
    """
    Laser Feasibility Score Engine

    Evaluates how feasible a natural material is for laser applications.
    """

    score = 0

    # 1. LSI contribution
    if lsi_value >= 5:
        score += 35
    elif lsi_value >= 2:
        score += 25
    else:
        score += 10

    # 2. Quantum yield contribution
    if plant["phi"] >= 0.7:
        score += 20
    elif plant["phi"] >= 0.5:
        score += 12
    else:
        score += 5

    # 3. Lifetime contribution
    if plant["tau"] >= 4:
        score += 15
    elif plant["tau"] >= 2:
        score += 10
    else:
        score += 5

    # 4. Non-radiative losses
    if plant["knr"] <= 0.35:
        score += 15
    elif plant["knr"] <= 0.5:
        score += 10
    else:
        score += 3

    # 5. Pump compatibility
    if pump_source in [
        "Nd:YAG Laser Pump",
        "Diode Laser Pump",
        "Xenon Flash Lamp",
        "UV Pump Source"
    ]:
        score += 15
    else:
        score += 5

    return min(score, 100)


def classify_feasibility(score):

    if score >= 80:
        return "High Laser Feasibility"

    elif score >= 60:
        return "Moderate Laser Feasibility"

    elif score >= 40:
        return "Low Laser Feasibility"

    else:
        return "Research Only"