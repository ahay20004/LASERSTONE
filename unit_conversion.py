"""LS-UCE: explicit multiplicative conversions; no implicit affine conversions."""
from decimal import Decimal
from types import MappingProxyType
from physical_quantities import get_quantity
from physical_constants import get_constant

_FACTORS = MappingProxyType({
    "vacuum_wavelength": {"nm":"1e-9","um":"1e-6","mm":"1e-3","cm":"1e-2"},
    "cavity_length": {"nm":"1e-9","um":"1e-6","mm":"1e-3","cm":"1e-2"},
    "frequency": {"kHz":"1e3","MHz":"1e6","GHz":"1e9","THz":"1e12"},
    "free_spectral_range": {"MHz":"1e6","GHz":"1e9","THz":"1e12"},
    "lifetime": {"fs":"1e-15","ps":"1e-12","ns":"1e-9","us":"1e-6","ms":"1e-3"},
    "photon_energy": {"eV":str(get_constant("elementary_charge"))},
    "power": {"mW":"1e-3","uW":"1e-6","kW":"1e3"},
    "irradiance": {"W/cm^2":"1e4","mW/cm^2":"10"},
    "radiant_exposure": {"J/cm^2":"1e4","mJ/cm^2":"10"},
    "absorption_cross_section": {"cm^2":"1e-4"},
    "emission_cross_section": {"cm^2":"1e-4"},
    "absorption_coefficient": {"cm^-1":"100"},
    "gain_coefficient": {"cm^-1":"100"},
    "number_density": {"cm^-3":"1e6"},
    "electrical_conductivity": {"S/cm":"100"},
    "efficiency": {"%":"0.01"},
    "quantum_yield": {"%":"0.01"},
})

def factor(identifier, unit):
    quantity = get_quantity(identifier)
    if unit == quantity.unit:
        return Decimal(1)
    return Decimal(_FACTORS[identifier][unit])

def convert(value, identifier, source_unit, target_unit):
    if isinstance(value, bool):
        raise ValueError("Boolean is not a physical value")
    number = Decimal(str(value))
    if not number.is_finite():
        raise ValueError("Nonfinite physical value")
    return number * factor(identifier, source_unit) / factor(identifier, target_unit)
