def optimize_laser_cavity(
    gain_score,
    q_factor_score,
    operation_mode,
    thermal_score
):

    cavity = {}

    # High-performance systems
    if gain_score >= 85 and q_factor_score >= 85:

        cavity["mirror_reflectivity"] = "99%"
        cavity["output_coupler"] = "5%"
        cavity["geometry"] = "Compact Fabry-Perot"

    elif gain_score >= 70:

        cavity["mirror_reflectivity"] = "95%"
        cavity["output_coupler"] = "10%"
        cavity["geometry"] = "Linear Resonator"

    else:

        cavity["mirror_reflectivity"] = "90%"
        cavity["output_coupler"] = "20%"
        cavity["geometry"] = "Experimental Cavity"

    # Operation mode optimization
    if operation_mode == "CW Laser Compatible":

        cavity["recommended_length"] = "Short Cavity"

    elif operation_mode == "Pulsed Laser Compatible":

        cavity["recommended_length"] = "Long Cavity"

    else:

        cavity["recommended_length"] = "Medium Cavity"

    # Thermal behavior
    if thermal_score >= 80:

        cavity["cooling"] = "Passive Cooling"

    else:

        cavity["cooling"] = "Active Cooling"

    return cavity