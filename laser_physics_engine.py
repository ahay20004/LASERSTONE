def calculate_laser_physics(plant):

    c = 3.0e8
    h = 6.626e-34
    e = 1.602e-19

    wavelength_nm = plant.get("lambda_em", 0)
    refractive_index = plant.get("refractive_index", 1.0)

    frequency_hz = 0
    photon_energy_ev = 0
    cavity_length_m = 0
    free_spectral_range_hz = 0

    if wavelength_nm > 0:

        wavelength_m = wavelength_nm * 1e-9

        frequency_hz = c / wavelength_m

        photon_energy_j = h * c / wavelength_m

        photon_energy_ev = photon_energy_j / e

        cavity_length_m = wavelength_m / (
            2 * refractive_index
        )

        free_spectral_range_hz = c / (
            2 * refractive_index * cavity_length_m
        )

    return {
        "frequency_hz": frequency_hz,
        "photon_energy_ev": photon_energy_ev,
        "cavity_length_m": cavity_length_m,
        "free_spectral_range_hz": free_spectral_range_hz,
        "frequency_formula": "f = c / λ",
        "energy_formula": "E = hc / λ",
        "cavity_formula": "L = λ / 2n",
        "fsr_formula": "FSR = c / 2nL",
        "gain_condition": "Optical Gain > Total Loss",
        "basis_status": "Physics-Based Laser Design"
    }