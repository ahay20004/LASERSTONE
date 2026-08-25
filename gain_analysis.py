def calculate_gain_potential(
    phi,
    tau,
    eta,
    stability_score,
    knr
):

    gain_score = (
        phi * 0.30 +
        (tau / 5.0) * 0.20 +
        eta * 0.25 +
        stability_score * 0.15 +
        (1 - knr) * 0.10
    )

    return round(gain_score * 100, 2)


def classify_gain_medium(gain_score):

    if gain_score >= 80:
        return "Excellent Gain Medium"

    elif gain_score >= 65:
        return "Strong Gain Candidate"

    elif gain_score >= 50:
        return "Moderate Gain Candidate"

    else:
        return "Weak Gain Candidate"


def analyze_gain_medium(plant):

    gain_score = calculate_gain_potential(
        plant["phi"],
        plant["tau"],
        plant["eta"],
        plant["stability_score"],
        plant["knr"]
    )

    classification = classify_gain_medium(
        gain_score
    )

    return {
        "gain_score": gain_score,
        "gain_classification": classification
    }