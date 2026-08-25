def calculate_spectral_match(lambda_abs, laser_wavelength):

    difference = abs(lambda_abs - laser_wavelength)

    if difference <= 10:
        return 1.0

    elif difference <= 25:
        return 0.85

    elif difference <= 50:
        return 0.60

    else:
        return 0.30


def calculate_photonic_score(
    spectral_match,
    phi,
    eta,
    tau,
    stability_score
):

    score = (
        spectral_match * 0.35 +
        phi * 0.20 +
        eta * 0.20 +
        (tau / 5.0) * 0.15 +
        stability_score * 0.10
    )

    return round(score, 3)


def predict_best_pump(plant, laser_sources):

    best_laser = None
    best_score = -1

    for laser_name, laser_data in laser_sources.items():

        spectral_match = calculate_spectral_match(
            plant["lambda_abs"],
            laser_data["wavelength"]
        )

        photonic_score = calculate_photonic_score(
            spectral_match,
            plant["phi"],
            plant["eta"],
            plant["tau"],
            plant["stability_score"]
        )

        if photonic_score > best_score:

            best_score = photonic_score

            best_laser = {
                "laser_name": laser_name,
                "spectral_match": spectral_match,
                "photonic_score": photonic_score,
                "estimated_efficiency": round(
                    photonic_score * 100,
                    2
                )
            }

    return best_laser