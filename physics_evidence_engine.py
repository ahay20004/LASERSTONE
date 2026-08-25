# core/physics_evidence_engine.py

def generate_physics_evidence(plant):

    plant["emission_strength"] = round(
        plant["phi"] * plant["tau"],
        3
    )

    plant["absorption_strength"] = round(
        plant["sigma_a"],
        3
    )

    plant["optical_quality"] = round(
        plant["phi"] +
        plant["eta"] +
        (plant["refractive_index"] / 2),
        3
    )

    plant["loss_indicator"] = round(
        plant["knr"],
        3
    )

    return plant