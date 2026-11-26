"""LS-PER initial optical equations; dimensional checks are not physical validation."""
from dataclasses import dataclass
from types import MappingProxyType
from physical_constants import get_record
from physical_quantities import get_quantity
from projects.paper2.dimensional_validation import BASE, assess

@dataclass(frozen=True)
class Equation:
    expression: str
    output: str
    factors: tuple
    conditions: str
    coefficient: str = "1"
    source_url: str = ""

REGISTRY = MappingProxyType({
    "vacuum_frequency": Equation("nu = c/lambda_0", "frequency",
        (("constant", "speed_of_light", 1), ("quantity", "vacuum_wavelength", -1)),
        "Positive vacuum wavelength; vacuum dispersion relation.", source_url="https://openstax.org/books/university-physics-volume-2/pages/16-summary"),
    "photon_energy": Equation("E = h nu", "photon_energy",
        (("constant", "planck_constant", 1), ("quantity", "frequency", 1)),
        "Positive photon frequency.", source_url="https://openstax.org/books/university-physics-volume-3/pages/6-key-equations"),
    "photon_energy_wavelength": Equation("E = h c/lambda_0", "photon_energy",
        (("constant", "planck_constant", 1), ("constant", "speed_of_light", 1),
         ("quantity", "vacuum_wavelength", -1)),
        "Positive vacuum wavelength.", source_url="https://openstax.org/books/university-physics-volume-3/pages/6-key-equations"),
    "linear_cavity_fsr": Equation("FSR approximately c/(2 n_g L)", "free_spectral_range",
        (("constant", "speed_of_light", 1), ("quantity", "group_index", -1),
         ("quantity", "cavity_length", -1)),
        "Homogeneous linear cavity; positive group index and length; negligible mirror group delay; local mode spacing.", coefficient="0.5", source_url="https://www.rp-photonics.com/free_spectral_range.html"),
})

def check_equation(identifier):
    eq = REGISTRY[identifier]
    symbols = {"output": dict(zip(BASE, get_quantity(eq.output).dimensions))}
    rhs = {}
    for kind, key, power in eq.factors:
        record = get_record(key) if kind == "constant" else get_quantity(key)
        symbol = kind + ":" + key
        symbols[symbol] = dict(zip(BASE, record.dimensions))
        rhs[symbol] = power
    return assess({"symbols": symbols, "lhs_terms": [{"output": 1}], "rhs_terms": [rhs]})
