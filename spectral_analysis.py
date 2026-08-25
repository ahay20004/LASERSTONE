def calculate_stokes_shift(lambda_abs, lambda_em):

    return lambda_em - lambda_abs


def classify_stokes_shift(shift):

    if shift >= 120:
        return "Excellent"

    elif shift >= 80:
        return "Very Good"

    elif shift >= 50:
        return "Moderate"

    else:
        return "Low"


def analyze_spectrum(plant):

    shift = calculate_stokes_shift(
        plant["lambda_abs"],
        plant["lambda_em"]
    )

    quality = classify_stokes_shift(shift)

    return {
        "stokes_shift": shift,
        "spectral_quality": quality
    }