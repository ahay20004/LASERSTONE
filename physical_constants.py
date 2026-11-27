"""LS-PCR v0.1: SI defining constants; not the complete CODATA catalog."""
from dataclasses import dataclass
from types import MappingProxyType

SOURCE = "https://www.bipm.org/en/measurement-units"
VERSION = "SI-2019"

@dataclass(frozen=True)
class Constant:
    symbol: str
    value: float
    unit: str
    dimensions: tuple
    name_ar: str
    uncertainty: float = 0.0
    exact: bool = True
    source: str = SOURCE
    version: str = VERSION

# Dimension order: M, L, T, I, Theta, N, J.
REGISTRY = MappingProxyType({
    "speed_of_light": Constant("c", 299792458, "m/s", (0,1,-1,0,0,0,0), "سرعة الضوء في الفراغ"),
    "planck_constant": Constant("h", 6.62607015e-34, "J s", (1,2,-1,0,0,0,0), "ثابت بلانك"),
    "elementary_charge": Constant("e", 1.602176634e-19, "C", (0,0,1,1,0,0,0), "الشحنة الأولية"),
    "boltzmann_constant": Constant("k_B", 1.380649e-23, "J/K", (1,2,-2,0,-1,0,0), "ثابت بولتزمان"),
    "avogadro_constant": Constant("N_A", 6.02214076e23, "mol^-1", (0,0,0,0,0,-1,0), "ثابت أفوجادرو"),
    "cesium_hyperfine_frequency": Constant("Delta nu_Cs", 9192631770, "Hz", (0,0,-1,0,0,0,0), "تردد الانتقال فائق الدقة للسيزيوم"),
    "luminous_efficacy": Constant("K_cd", 683, "lm/W", (-1,-2,3,0,0,0,1), "الفعالية الضوئية للإشعاع عند 540 تيراهرتز"),
})

def get_record(identifier: str) -> Constant:
    return REGISTRY[identifier]

def get_constant(identifier: str) -> float:
    return get_record(identifier).value

def get_records(*identifiers: str) -> dict:
    return {key: get_record(key) for key in identifiers}
