def generate_scientific_basis(plant):

    c = 3.0e8
    h = 6.626e-34

    wavelength_nm = plant.get("lambda_em", 0)

    frequency_hz = 0
    photon_energy_j = 0
    photon_energy_ev = 0

    if wavelength_nm > 0:

        wavelength_m = wavelength_nm * 1e-9

        frequency_hz = c / wavelength_m

        photon_energy_j = (
            h * c / wavelength_m
        )

        photon_energy_ev = (
            photon_energy_j / 1.602e-19
        )

    return {
        "speed_of_light": c,
        "planck_constant": h,
        "wavelength_nm": wavelength_nm,
        "frequency_hz": frequency_hz,
        "photon_energy_j": photon_energy_j,
        "photon_energy_ev": photon_energy_ev,
        "frequency_formula": "f = c / λ",
        "energy_formula": "E = h c / λ",
        "basis_status": "Physics-Based Calculation"
    }