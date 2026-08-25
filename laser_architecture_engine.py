def recommend_laser_architecture(plant):

    lri = plant.get("lri_score", 0)

    operation_mode = plant.get(
        "operation_mode",
        "Unknown"
    )

    gain_score = plant.get("gain_score", 0)

    thermal_score = plant.get("thermal_score", 0)

    if lri >= 85 and gain_score >= 80:

        architecture = (
            "High-Performance Tunable Laser"
        )

    elif operation_mode == "Continuous Wave":

        architecture = (
            "CW Solid-State Bio-Laser"
        )

    elif operation_mode == "Pulsed":

        architecture = (
            "Pulsed Organic Laser System"
        )

    elif thermal_score < 50:

        architecture = (
            "Low-Power Experimental Laser"
        )

    else:

        architecture = (
            "Research Prototype Laser"
        )

    return architecture

def generate_architecture_profile(plant):

    architecture = recommend_laser_architecture(
        plant
    )

    return {

        "architecture":
        architecture,

        "pump_source":
        "Optical Diode Pump",

        "cavity":
        "Fabry-Perot Resonator",

        "mirror_1":
        "High Reflector",

        "mirror_2":
        "Output Coupler",

        "cooling":
        "Passive Cooling",

        "validation":
        "Prototype Recommended"
    }