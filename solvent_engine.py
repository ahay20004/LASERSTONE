def recommend_solvent_environment(plant):

    phi = plant["phi"]
    knr = plant["knr"]
    refractive_index = plant["refractive_index"]

    # High fluorescence efficiency
    if phi >= 0.7 and knr <= 0.35:

        if refractive_index <= 1.35:
            return {
                "solvent": "Ethanol",
                "reason": "High fluorescence stability in low-index organic solvent"
            }

        else:
            return {
                "solvent": "DMSO",
                "reason": "Enhanced molecular stabilization"
            }

    # Moderate fluorescence
    elif phi >= 0.5:

        return {
            "solvent": "Methanol",
            "reason": "Balanced optical behavior"
        }

    # Weak fluorescence systems
    else:

        return {
            "solvent": "Water",
            "reason": "Low-cost experimental medium"
        }