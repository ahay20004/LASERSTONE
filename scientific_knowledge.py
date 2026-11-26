"""Initial bilingual optical knowledge library; explanatory content, not validation."""
from equation_registry import REGISTRY
from quantity_relationships import describe_equation
from dataclasses import asdict

_CARDS = {
    "vacuum_frequency": {
        "ar": {"title":"التردد والطول الموجي في الفراغ","concept":"التردد عدد الدورات في الثانية. في الفراغ تنتشر الموجة الكهرومغناطيسية بسرعة الضوء.","derivation":["c = lambda_0 * nu","nu = c / lambda_0"],"application":"تحويل الطول الموجي الفراغي إلى تردد."},
        "en": {"title":"Vacuum wavelength and frequency","concept":"Frequency counts cycles per second. In vacuum electromagnetic waves propagate at the speed of light.","derivation":["c = lambda_0 * nu","nu = c / lambda_0"],"application":"Convert vacuum wavelength to frequency."}},
    "photon_energy": {
        "ar":{"title":"طاقة الفوتون","concept":"طاقة الفوتون تتناسب طرديا مع تردده وفق علاقة بلانك.","derivation":["E = h * nu"],"application":"حساب طاقة فوتون من تردده."},
        "en":{"title":"Photon energy","concept":"Photon energy is proportional to frequency through the Planck relation.","derivation":["E = h * nu"],"application":"Calculate photon energy from frequency."}},
    "photon_energy_wavelength": {
        "ar":{"title":"طاقة الفوتون والطول الموجي","concept":"تزداد طاقة الفوتون مع تناقص طوله الموجي الفراغي.","derivation":["E = h * nu","nu = c / lambda_0","E = h * c / lambda_0"],"application":"مقارنة طاقات فوتونات الليزر."},
        "en":{"title":"Photon energy and wavelength","concept":"Photon energy increases as vacuum wavelength decreases.","derivation":["E = h * nu","nu = c / lambda_0","E = h * c / lambda_0"],"application":"Compare laser photon energies."}},
    "linear_cavity_fsr": {
        "ar":{"title":"المدى الطيفي الحر للرنان","concept":"الفاصل الترددي المحلي بين الأنماط الطولية المتجاورة في رنان خطي متجانس، مع إهمال تأخير المجموعة عند المرايا.","derivation":["tau_g approximately 2 * n_g * L / c","FSR approximately 1 / tau_g","FSR approximately c / (2 * n_g * L)"],"application":"تقدير الفاصل الترددي المحلي بين الأنماط."},
        "en":{"title":"Linear cavity free spectral range","concept":"Local spacing between adjacent longitudinal modes of a homogeneous linear cavity, neglecting mirror group delay.","derivation":["tau_g approximately 2 * n_g * L / c","FSR approximately 1 / tau_g","FSR approximately c / (2 * n_g * L)"],"application":"Estimate local longitudinal mode spacing."}}
}

def knowledge_card(identifier, language):
    if language not in ("ar", "en"):
        raise ValueError("Unsupported language")
    eq = REGISTRY[identifier]
    description = describe_equation(identifier)
    description["constants"] = [(name,power,asdict(record)) for name,power,record in description["constants"]]
    card = _CARDS[identifier][language]
    return {"language":language,"title":card["title"],"concept":card["concept"],
            "derivation":list(card["derivation"]),"application":card["application"],
            "equation":description,"coefficient":eq.coefficient,
            "equation_source_status":"bibliographic_reference_pending",
            "scientific_validation":False}
