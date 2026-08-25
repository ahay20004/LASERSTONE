def predict_laser_output(plant):

    wavelength_nm = plant.get("lambda_em", 0)

    frequency_hz = 0

    if wavelength_nm > 0:
        frequency_hz = 3e8 / (wavelength_nm * 1e-9)

    material_score = plant.get("material_score", 0)
    thermal_score = plant.get("thermal_score", 0)
    feasibility_score = plant.get("feasibility_score", 0)

    if material_score >= 80 and thermal_score >= 70:
        estimated_power = "Medium Prototype Output"
        laser_class = "Class 3R / Research Prototype"

    elif material_score >= 60:
        estimated_power = "Low Prototype Output"
        laser_class = "Class 2 / Low-Power Visible Prototype"

    else:
        estimated_power = "Weak / Needs Optimization"
        laser_class = "Experimental Candidate"

    return {
        "active_medium": plant.get("name", "Unknown"),
        "emission_wavelength_nm": wavelength_nm,
        "frequency_hz": frequency_hz,
        "laser_color": plant.get("laser_color", "Unknown"),
        "spectral_region": plant.get("fluorescence_region", "Unknown"),
        "estimated_power": estimated_power,
        "proposed_laser_class": laser_class,
        "validation_status": "Theoretical Prediction - Requires Prototype Validation"
    }