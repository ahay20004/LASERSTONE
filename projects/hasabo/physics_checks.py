"""Pure numerical checks; no experimental or publication claims authorized."""
import math

C = 299792458.0
HC_EV_NM = 1239.8419843320026

def positive(x):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) or x <= 0:
        raise ValueError("Expected finite positive quantity")
    return x

def theta(two_theta_deg):
    x = positive(two_theta_deg)
    if x >= 180:
        raise ValueError("2theta must be below 180 degrees")
    return math.radians(x / 2)

def bragg_nm(wavelength_nm, two_theta_deg):
    return positive(wavelength_nm) / (2 * math.sin(theta(two_theta_deg)))

def scherrer_nm(wavelength_nm, two_theta_deg, corrected_fwhm_rad, shape_factor):
    beta = positive(corrected_fwhm_rad)
    if beta >= math.pi:
        raise ValueError("FWHM must be in radians and below pi")
    return positive(shape_factor) * positive(wavelength_nm) / (beta * math.cos(theta(two_theta_deg)))

def photon_energy_ev(wavelength_nm):
    return HC_EV_NM / positive(wavelength_nm)

def shift_ratio(wavelength_a_nm, wavelength_b_nm, excitation_hz):
    a, b = positive(wavelength_a_nm), positive(wavelength_b_nm)
    return abs(C * 1e9 / a - C * 1e9 / b) / positive(excitation_hz)
