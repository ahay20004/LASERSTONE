def laserstone_governor_decision(plant):

    intelligence = plant[
        "intelligence_summary"
    ]["intelligence_score"]

    integrity = plant.get(
        "system_integrity_score", 0
    )

    confidence = plant.get(
        "scientific_confidence_score", 0
    )

    novelty = plant.get(
        "research_novelty_score", 0
    )

    patent = plant.get(
        "patent_potential_score", 0
    )

    # Elite scientific candidate
    if (
        intelligence >= 90
        and integrity >= 85
        and confidence >= 85
    ):

        return (
            "Elite Candidate for Advanced "
            "Bio-Laser Development"
        )

    # Patent-oriented material
    elif (
        novelty >= 80
        and patent >= 80
    ):

        return (
            "High-Priority Patent-Oriented "
            "Laser Material"
        )

    # Strong experimental system
    elif intelligence >= 75:

        return (
            "Recommended for Experimental "
            "Laser Prototyping"
        )

    # Research-only
    elif intelligence >= 60:

        return (
            "Suitable for Scientific "
            "Research and Optimization"
        )

    # Weak system
    else:

        return (
            "Currently Limited for "
            "Advanced Laser Deployment"
        )