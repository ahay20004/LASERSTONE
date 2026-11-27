def evaluate_q_factor(
    plant,
    gain_score,
    thermal_score,
    photobleaching_score
):

    q_score = 0

    # Gain contribution
    if gain_score >= 85:
        q_score += 35

    elif gain_score >= 70:
        q_score += 25

    else:
        q_score += 10

    # Thermal stability contribution
    if thermal_score >= 80:
        q_score += 25

    elif thermal_score >= 60:
        q_score += 15

    else:
        q_score += 5

    # Photobleaching resistance
    if photobleaching_score >= 80:
        q_score += 20

    elif photobleaching_score >= 60:
        q_score += 12

    else:
        q_score += 5

    # Refractive index influence
    if 1.3 <= plant["refractive_index"] <= 1.5:
        q_score += 20

    else:
        q_score += 10

    return min(q_score, 100)


def classify_q_factor(score):

    if score >= 85:
        return "Ultra High-Q Resonance"

    elif score >= 70:
        return "High-Q Resonance"

    elif score >= 50:
        return "Moderate-Q Resonance"

    else:
        return "Low-Q Resonance"


def calculate_physical_q(frequency_hz, linewidth_hz=None, energy_lifetime_s=None):
    """Isolated passive resonance; linewidth is power FWHM, lifetime is energy decay.
    Supply exactly one loss observable. Q is dimensionless.
    """
    import math
    if linewidth_hz is not None and energy_lifetime_s is not None:
        return {"status": "INVALID", "reason": "Supply one loss observable"}
    if frequency_hz is None or (linewidth_hz is None and energy_lifetime_s is None):
        return {"status": "UNVERIFIED", "q": None}
    try:
        def positive(value):
            if isinstance(value, bool):
                raise ValueError("Boolean is not a physical quantity")
            x = float(value)
            if not math.isfinite(x) or x <= 0:
                raise ValueError("Expected finite positive SI quantity")
            return x
        nu = positive(frequency_hz)
        if linewidth_hz is not None:
            q = nu / positive(linewidth_hz)
            basis = "power_fwhm"
        else:
            q = 2 * math.pi * (nu * positive(energy_lifetime_s))
            basis = "energy_decay_lifetime"
        if not math.isfinite(q) or q <= 0:
            raise ValueError("Q outside numerical range")
    except (ValueError, TypeError, OverflowError) as exc:
        return {"status": "INVALID", "reason": str(exc), "q": None}
    return {"status": "DERIVED", "q": q, "basis": basis,
            "model": "isolated_passive_resonance", "experimental_validation": False}



def audit_q_uncertainty(frequency_hz, linewidth_hz, u_frequency, u_linewidth, correlation=None):
    """First-order propagation for Q = frequency / power FWHM."""
    import math
    base = calculate_physical_q(frequency_hz, linewidth_hz)
    if base["status"] != "DERIVED":
        return {"status": base["status"]}
    if any(x is None for x in (u_frequency, u_linewidth, correlation)):
        return {"status": "UNVERIFIED"}
    try:
        if any(isinstance(x, bool) for x in (u_frequency, u_linewidth, correlation)):
            raise ValueError("Boolean uncertainty")
        a,b,rho = map(float,(u_frequency,u_linewidth,correlation))
        if not all(map(math.isfinite,(a,b,rho))) or min(a,b)<0 or abs(rho)>1:
            raise ValueError("Invalid uncertainty")
        x = a / float(linewidth_hz)
        y = -base["q"] * (b / float(linewidth_hz))
        u = math.hypot(x+rho*y, math.sqrt(max(0,1-rho*rho))*y)
        if not math.isfinite(u):
            raise ValueError("Nonfinite uncertainty")
    except (ValueError, TypeError, OverflowError, ZeroDivisionError):
        return {"status":"INVALID"}
    return {"status":"DERIVED", "q":base["q"], "standard_uncertainty":u,
            "correlation":rho, "method":"first_order_linearization",
            "experimental_validation":False}
