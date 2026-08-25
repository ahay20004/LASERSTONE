def calculate_lsi(phi, tau, sigma_a, eta, knr, refractive_index):
    """
    LASERSTONE Index Calculation

    Parameters:
    phi               -> Quantum Yield
    tau               -> Fluorescence Lifetime
    sigma_a           -> Absorption Cross Section
    eta               -> Optical Efficiency
    knr               -> Non-radiative Decay Rate
    refractive_index  -> Refractive Index

    Returns:
    LSI Value
    """

    lsi = (phi * tau * sigma_a * eta) / (knr * refractive_index)

    return round(lsi, 3)