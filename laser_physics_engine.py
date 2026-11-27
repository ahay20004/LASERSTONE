"""Linear homogeneous cavity model; SI units, vacuum wavelength."""
import math

C = 299792458.0
H = 6.62607015e-34
E = 1.602176634e-19


def _number(value, name, minimum=0, strict=False):
    if isinstance(value, bool):
        raise ValueError(name + " must be numeric")
    x = float(value)
    if not math.isfinite(x) or x < minimum or (strict and x == minimum):
        raise ValueError(name + " outside physical domain")
    return x


def calculate_laser_physics(plant):
    wavelength_nm = _number(plant.get("lambda_em", 0), "lambda_em")
    n = _number(plant.get("refractive_index", 1.0), "refractive_index", strict=True)
    ng = _number(plant.get("group_index", n), "group_index", strict=True)
    wavelength = wavelength_nm * 1e-9
    mode = _number(plant.get("longitudinal_mode", 1), "longitudinal_mode", 1)
    if not mode.is_integer():
        raise ValueError("longitudinal_mode must be an integer")
    explicit = plant.get("cavity_length_m") is not None
    length = (_number(plant["cavity_length_m"], "cavity_length_m", strict=True)
              if explicit else mode * wavelength / (2 * n))
    fsr = C / (2 * ng * length) if length else 0
    frequency = C / wavelength if wavelength else 0
    threshold = margin = None
    status = "UNVERIFIED"
    keys = ("mirror_r1", "mirror_r2", "internal_loss_m_inv")
    if all(plant.get(k) is not None for k in keys):
        r1, r2 = (_number(plant[k], k, strict=True) for k in keys[:2])
        if max(r1, r2) > 1:
            raise ValueError("mirror reflectivity must not exceed one")
        loss = _number(plant[keys[2]], keys[2])
        if explicit:
            threshold = loss - (math.log(r1) + math.log(r2)) / (2 * length)
            if plant.get("gain_m_inv") is not None:
                gain = _number(plant["gain_m_inv"], "gain_m_inv", -math.inf)
                margin = gain - threshold
                status = ("AT_THRESHOLD" if math.isclose(gain, threshold, rel_tol=1e-9, abs_tol=1e-12)
                          else "ABOVE_THRESHOLD" if margin > 0 else "BELOW_THRESHOLD")
    return {
        "frequency_hz": frequency,
        "photon_energy_ev": H * frequency / E,
        "cavity_length_m": length,
        "free_spectral_range_hz": fsr,
        "nearest_longitudinal_mode": round(2 * n * length / wavelength) if wavelength and length else None,
        "cavity_length_basis": "provided" if explicit else "ideal_resonance_assumption",
        "group_index_basis": "provided" if "group_index" in plant else "assumed_equal_to_phase_index",
        "threshold_gain_m_inv": threshold,
        "gain_margin_m_inv": margin,
        "threshold_status": status,
        "frequency_formula": "f = c / λ",
        "energy_formula": "E = hc / λ",
        "cavity_formula": "L = mλ / 2n",
        "fsr_formula": "FSR = c / 2ngL",
        "gain_condition": "Optical Gain > Total Loss",
        "basis_status": "Physics-Based Laser Design",
        "model_scope": "Linear homogeneous cavity; gain fills cavity; no experimental validation",
    }
