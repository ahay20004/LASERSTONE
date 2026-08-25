def calculate_trace_lri(plant):

    lri_score = plant.get(
        "lri_score",
        None
    )

    if lri_score is not None:
        return lri_score

    material_score = plant.get(
        "material_score",
        0
    )

    thermal_score = plant.get(
        "thermal_score",
        0
    )

    feasibility_score = plant.get(
        "feasibility_score",
        0
    )

    q_factor_score = plant.get(
        "q_factor_score",
        0
    )

    return round(
        (
            material_score
            + thermal_score
            + feasibility_score
            + q_factor_score
        ) / 4,
        2
    )


def classify_trace_decision(lri_score):

    if lri_score >= 85:

        return (
            "READY FOR PROTOTYPE",
            "HIGH"
        )

    if lri_score >= 60:

        return (
            "RESEARCH STAGE",
            "MEDIUM"
        )

    return (
        "NEEDS OPTIMIZATION",
        "LOW"
    )


def generate_scientific_trace(plant):

    trace = []

    material_score = plant.get(
        "material_score",
        0
    )

    thermal_score = plant.get(
        "thermal_score",
        0
    )

    feasibility_score = plant.get(
        "feasibility_score",
        0
    )

    q_factor_score = plant.get(
        "q_factor_score",
        0
    )

    lri_score = calculate_trace_lri(
        plant
    )

    decision, confidence = classify_trace_decision(
        lri_score
    )

    trace.append(
        "Scientific Evaluation Summary"
    )

    trace.append(
        f"Material Score : {material_score}"
    )

    trace.append(
        f"Thermal Score : {thermal_score}"
    )

    trace.append(
        f"Feasibility Score : {feasibility_score}"
    )

    trace.append(
        f"Q Factor Score : {q_factor_score}"
    )

    trace.append(
        f"LRI Score : {lri_score}"
    )

    trace.append(
        f"Prototype Decision : {decision}"
    )

    trace.append(
        f"Prototype Confidence : {confidence}"
    )

    trace.append(
        f"Emission Wavelength : {plant.get('lambda_em', 'N/A')} nm"
    )

    trace.append(
        f"Laser Color : {plant.get('laser_color', 'N/A')}"
    )

    trace.append(
        f"Governor Decision : {plant.get('governor_decision', 'N/A')}"
    )

    return trace


def generate_scientific_reasoning(plant):

    trace = []

    material_score = plant.get(
        "material_score",
        0
    )

    thermal_score = plant.get(
        "thermal_score",
        0
    )

    feasibility_score = plant.get(
        "feasibility_score",
        0
    )

    q_factor_score = plant.get(
        "q_factor_score",
        0
    )

    lri_score = calculate_trace_lri(
        plant
    )

    trace.append(
        "Scientific Evaluation Summary"
    )

    if material_score >= 70:

        trace.append(
            "→ Material performance supports laser generation."
        )

    else:

        trace.append(
            "→ Material performance needs further optimization."
        )

    if thermal_score >= 80:

        trace.append(
            "→ Thermal stability is excellent."
        )

    else:

        trace.append(
            "→ Thermal stability requires improvement."
        )

    if feasibility_score >= 80:

        trace.append(
            "→ Laser feasibility is high."
        )

    else:

        trace.append(
            "→ Laser feasibility remains under investigation."
        )

    if q_factor_score >= 80:

        trace.append(
            "→ Resonator quality potential is strong."
        )

    else:

        trace.append(
            "→ Resonator quality potential needs improvement."
        )

    trace.append(
        f"Combined LRI Score = {lri_score}"
    )

    decision, confidence = classify_trace_decision(
        lri_score
    )

    trace.append(
        f"→ FINAL DECISION: {decision}"
    )

    trace.append(
        f"→ PROTOTYPE CONFIDENCE: {confidence}"
    )

    return trace


def show_scientific_trace(plant):

    print(
        "\n=== SCIENTIFIC TRACE REPORT ===\n"
    )

    trace = generate_scientific_trace(
        plant
    )

    for item in trace:

        print(item)


def get_trace_summary(plant):

    lri = calculate_trace_lri(
        plant
    )

    recommendation, confidence = classify_trace_decision(
        lri
    )

    return {

        "plant":
        plant.get("name"),

        "lri":
        lri,

        "wavelength":
        plant.get("lambda_em"),

        "laser_color":
        plant.get("laser_color"),

        "recommendation":
        recommendation,

        "confidence":
        confidence
    }