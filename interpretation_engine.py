def generate_scientific_interpretation(plant):
    interpretation = []

    # LSI interpretation
    if plant["lsi"] >= 5:
        interpretation.append(
            "The material shows excellent laser suitability due to strong photophysical performance."
        )

    elif plant["lsi"] >= 3:
        interpretation.append(
            "The material demonstrates moderate-to-strong optical gain behavior."
        )

    else:
        interpretation.append(
            "The material shows limited laser amplification potential."
        )

    # Quantum yield
    if plant["phi"] >= 0.7:
        interpretation.append(
            "High quantum yield indicates efficient radiative emission."
        )

    # Lifetime
    if plant["tau"] >= 4:
        interpretation.append(
            "Long excited-state lifetime supports population inversion stability."
        )

    # Non-radiative loss
    if plant["knr"] <= 0.35:
        interpretation.append(
            "Low non-radiative decay enhances optical efficiency."
        )

    # Thermal behavior
    if plant["thermal_score"] >= 70:
        interpretation.append(
            "The material demonstrates good thermal stability for laser operation."
        )

    # Gain medium
    if plant["gain_score"] >= 70:
        interpretation.append(
            "Optical gain analysis suggests strong amplification capability."
        )

    return interpretation