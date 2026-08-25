def normalize_parameter(value, minimum, maximum):
    """
    Normalize parameter between 0 and 1
    """

    if maximum == minimum:
        return 0

    return (value - minimum) / (maximum - minimum)


def calculate_normalized_lsi(plant):
    """
    Physics-aware normalized LSI model
    """

    phi_n = normalize_parameter(plant["phi"], 0, 1)

    tau_n = normalize_parameter(plant["tau"], 0, 10)

    sigma_n = normalize_parameter(
        plant["sigma_a"],
        0,
        2
    )

    knr_n = normalize_parameter(
        plant["knr"],
        0,
        2
    )

    eta_n = normalize_parameter(
        plant["eta"],
        0,
        2
    )

    n_n = normalize_parameter(
        plant["refractive_index"],
        1,
        2
    )

    # Physics-based weighted model
    normalized_lsi = (
        (phi_n * 0.30) +
        (tau_n * 0.25) +
        (sigma_n * 0.20) +
        (eta_n * 0.10)
    ) - (
        (knr_n * 0.10) +
        (n_n * 0.05)
    )

    return round(normalized_lsi * 100, 2)


def evaluate_gain_condition(plant):
    """
    Simplified optical gain condition
    """

    gain_factor = (
        plant["phi"] *
        plant["sigma_a"] *
        plant["tau"]
    )

    loss_factor = (
        plant["knr"] *
        plant["refractive_index"]
    )

    if gain_factor > loss_factor:
        return "Gain Dominant"

    return "Loss Dominant"


def estimate_laser_threshold(plant):
    """
    Simplified threshold estimation
    """

    threshold = (
        plant["knr"] *
        plant["refractive_index"]
    ) / (
        plant["phi"] *
        plant["tau"]
    )

    return round(threshold, 4)