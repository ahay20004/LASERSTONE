"""LS-PQR v0.1. Dimensions ordered M,L,T,I,Theta,N,J."""
from dataclasses import dataclass
from types import MappingProxyType

@dataclass(frozen=True)
class Quantity:
    symbol: str
    unit: str
    dimensions: tuple

REGISTRY = MappingProxyType({
    "vacuum_wavelength": Quantity("lambda_0", "m", (0,1,0,0,0,0,0)),
    "frequency": Quantity("nu", "Hz", (0,0,-1,0,0,0,0)),
    "angular_frequency": Quantity("omega", "rad/s", (0,0,-1,0,0,0,0)),
    "wavenumber": Quantity("k", "rad/m", (0,-1,0,0,0,0,0)),
    "photon_energy": Quantity("E", "J", (1,2,-2,0,0,0,0)),
    "power": Quantity("P", "W", (1,2,-3,0,0,0,0)),
    "irradiance": Quantity("I", "W/m^2", (1,0,-3,0,0,0,0)),
    "radiant_exposure": Quantity("H", "J/m^2", (1,0,-2,0,0,0,0)),
    "lifetime": Quantity("tau", "s", (0,0,1,0,0,0,0)),
    "absorption_cross_section": Quantity("sigma_a", "m^2", (0,2,0,0,0,0,0)),
    "emission_cross_section": Quantity("sigma_e", "m^2", (0,2,0,0,0,0,0)),
    "absorption_coefficient": Quantity("alpha", "m^-1", (0,-1,0,0,0,0,0)),
    "gain_coefficient": Quantity("g", "m^-1", (0,-1,0,0,0,0,0)),
    "number_density": Quantity("N", "m^-3", (0,-3,0,0,0,0,0)),
    "radiative_rate": Quantity("k_r", "s^-1", (0,0,-1,0,0,0,0)),
    "nonradiative_rate": Quantity("k_nr", "s^-1", (0,0,-1,0,0,0,0)),
    "quantum_yield": Quantity("phi", "1", (0,0,0,0,0,0,0)),
    "refractive_index": Quantity("n", "1", (0,0,0,0,0,0,0)),
    "group_index": Quantity("n_g", "1", (0,0,0,0,0,0,0)),
    "quality_factor": Quantity("Q", "1", (0,0,0,0,0,0,0)),
    "efficiency": Quantity("eta", "1", (0,0,0,0,0,0,0)),
    "cavity_length": Quantity("L", "m", (0,1,0,0,0,0,0)),
    "mirror_radius": Quantity("R", "m", (0,1,0,0,0,0,0)),
    "free_spectral_range": Quantity("FSR", "Hz", (0,0,-1,0,0,0,0)),
    "electrical_conductivity": Quantity("sigma", "S/m", (-1,-3,3,2,0,0,0)),
    "thermal_conductivity": Quantity("kappa", "W/(m K)", (1,1,-3,0,-1,0,0)),
    "magnetic_flux_density": Quantity("B", "T", (1,0,-2,-1,0,0,0)),
    "electric_field": Quantity("E", "V/m", (1,1,-3,-1,0,0,0)),
    "temperature": Quantity("T", "K", (0,0,0,0,1,0,0)),
    "torque": Quantity("tau", "N m", (1,2,-2,0,0,0,0)),
})

def get_quantity(identifier: str) -> Quantity:
    return REGISTRY[identifier]

def same_dimensions(left: str, right: str) -> bool:
    return get_quantity(left).dimensions == get_quantity(right).dimensions
