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


def audit_fluorescence_decay(quantum_yield, lifetime_s):
    """Single-exponential decay model; yield is a fraction, lifetime in seconds.
    Derived rates are not independent measurements or proof of optical gain.
    """
    import math
    if quantum_yield is None or lifetime_s is None:
        return {"status": "UNVERIFIED"}
    try:
        if isinstance(quantum_yield, bool) or isinstance(lifetime_s, bool):
            raise ValueError("Boolean inputs are not physical quantities")
        phi, tau = float(quantum_yield), float(lifetime_s)
        if not math.isfinite(phi) or not 0 <= phi <= 1:
            raise ValueError("Quantum yield must be a finite fraction in [0, 1]")
        if not math.isfinite(tau) or tau <= 0:
            raise ValueError("Lifetime must be finite and positive in seconds")
        total = 1 / tau
        if not math.isfinite(total):
            raise ValueError("Decay rate outside numerical range")
    except (ValueError, TypeError, OverflowError) as exc:
        return {"status": "INVALID", "reason": str(exc)}
    return {"status": "DERIVED", "total_rate_s_inv": total,
            "radiative_rate_s_inv": phi * total,
            "nonradiative_rate_s_inv": (1 - phi) * total,
            "model": "single_exponential_decay",
            "experimental_validation": False,
            "gain_verified": False}
