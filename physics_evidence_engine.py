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



def audit_fluorescence_uncertainty(phi, tau, u_phi, u_tau, correlation=None):
    """First-order propagation; correlation must be explicitly supplied."""
    import math
    base = audit_fluorescence_decay(phi, tau)
    if base["status"] != "DERIVED":
        return {"status": base["status"]}
    if any(x is None for x in (u_phi, u_tau, correlation)):
        return {"status": "UNVERIFIED"}
    try:
        if any(isinstance(x, bool) for x in (u_phi, u_tau, correlation)):
            raise ValueError("Boolean uncertainty")
        a, b, rho = map(float, (u_phi, u_tau, correlation))
        if not all(map(math.isfinite, (a, b, rho))) or min(a,b) < 0 or abs(rho) > 1:
            raise ValueError("Invalid uncertainty or correlation")
        phi, tau = float(phi), float(tau)
        total = base["total_rate_s_inv"]
        x, y = a * total, (b / tau) * total
        def propagate(p, q):
            return math.hypot(p + rho*q, math.sqrt(max(0, 1-rho*rho))*q)
        ur = propagate(x, -phi*y)
        un = propagate(-x, -(1-phi)*y)
        if not all(map(math.isfinite, (y, ur, un))):
            raise ValueError("Numerical overflow")
    except (ValueError, TypeError, OverflowError, ZeroDivisionError):
        return {"status": "INVALID"}
    return {"status": "DERIVED", "total_standard_uncertainty_s_inv": y,
            "radiative_standard_uncertainty_s_inv": ur,
            "nonradiative_standard_uncertainty_s_inv": un,
            "correlation": rho, "method": "first_order_linearization",
            "experimental_validation": False}
