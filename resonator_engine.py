def recommend_resonator(
    gain_score,
    thermal_score,
    operation_mode,
    photobleaching_score
):

    # High-performance materials
    if (
        gain_score >= 85 and
        thermal_score >= 80 and
        photobleaching_score >= 80
    ):

        if operation_mode == "CW Laser Compatible":
            return "Fabry-Perot Resonator"

        elif operation_mode == "Pulsed Laser Compatible":
            return "Q-Switched Resonator"

        else:
            return "Ring Resonator"

    # Medium-performance materials
    elif gain_score >= 70:

        if operation_mode == "CW Laser Compatible":
            return "Distributed Feedback (DFB)"

        else:
            return "Linear Optical Cavity"

    # Weak materials
    else:

        return "Low-Q Experimental Resonator"