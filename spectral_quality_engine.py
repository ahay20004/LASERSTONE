from data_standardization_engine import (
    standardize_quality_value,
    classify_numeric_score
)



def calculate_spectral_quality(plant):
    score = (
        plant["phi"] * 0.35 +
        plant["tau"] / 5 * 0.25 +
        plant["sigma_a"] * 0.25 +
        (1 / plant["knr"]) * 0.15
    )

    if score >= 1.5:
        return "High"
    elif score >= 1.0:
        return "Medium"
    else:
        return "Low"