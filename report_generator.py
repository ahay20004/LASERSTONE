"""Report export with exclusive creation; existing files are never removed."""
from pathlib import Path
import re


def ensure_reports_folder(reports_dir="reports"):
    path = Path(reports_dir)
    if path.exists() and not path.is_dir():
        raise FileExistsError(f"Report destination is not a directory: {path}")
    path.mkdir(parents=True, exist_ok=True)
    return str(path)


def generate_scientific_report(plant):
    if plant.get("valid") is False or plant.get("analysis_status") == "BLOCKED":
        raise ValueError("Cannot export a blocked analysis")

    report = f"""
========================================
      LASERSTONE™ SCIENTIFIC REPORT

Analysis Basis        : {plant.get("score_basis", "UNSPECIFIED")}
Physical Validation   : {plant.get("physical_validation_status", "NOT ESTABLISHED")}
Decision Basis        : {plant.get("decision_basis", "UNSPECIFIED")}
LRI Score             : {plant.get("lri_score", "N/A")}
Heuristic Consistency : {plant.get("physics_consistency_score", "N/A")}
Decision              : {plant.get("final_decision", "N/A")}
========================================

Plant Name            : {plant['name']}
Scientific Name       : {plant['scientific_name']}
Origin                : {plant['origin']}

----------------------------------------
LSI ANALYSIS
----------------------------------------

LSI Value             : {plant['lsi']}
Classification        : {plant['classification']}

----------------------------------------
SPECTRAL ANALYSIS
----------------------------------------

Absorption λ          : {plant['lambda_abs']} nm
Emission λ            : {plant['lambda_em']} nm

Laser Color           : {plant['predicted_color']}
Spectral Region       : {plant['predicted_region']}

----------------------------------------
LASER SYSTEM ANALYSIS
----------------------------------------

Pump Source           : {plant['pump_source']}
Operation Mode        : {plant['operation_mode']}
Recommended Resonator : {plant['recommended_resonator']}

----------------------------------------
STABILITY ANALYSIS
----------------------------------------

Thermal Stability     : {plant['thermal_class']}
Photostability        : {plant['photobleaching_class']}

----------------------------------------
GAIN & RESONANCE
----------------------------------------

Gain Medium           : {plant['gain_class']}
Q-Factor              : {plant['q_factor_class']}

----------------------------------------
BEAM & EFFICIENCY
----------------------------------------

Beam Quality          : {plant['beam_quality_class']}
Laser Efficiency      : {plant['laser_efficiency_class']}

----------------------------------------
SOLVENT ENVIRONMENT
----------------------------------------

Recommended Solvent   : {plant['recommended_solvent']}
Reason                : {plant['solvent_reason']}

----------------------------------------
GLOBAL RANKING
----------------------------------------

Global Rank           : #{plant['global_rank']}

========================================
"""

    return report


def save_single_report(plant, reports_dir="reports"):
    report = generate_scientific_report(plant)
    folder = Path(ensure_reports_folder(reports_dir))
    safe_name = re.sub(r"[^A-Za-z0-9_-]+", "_", str(plant["name"])).strip("_").lower() or "plant"
    index = 0
    while True:
        suffix = "" if index == 0 else f"_{index:03d}"
        path = folder / f"{safe_name}_report{suffix}.txt"
        try:
            with path.open("x", encoding="utf-8") as stream:
                stream.write(report)
            return str(path)
        except FileExistsError:
            index += 1


def save_all_reports(plants, reports_dir="reports"):
    records = list(plants)
    # Render all records first so invalid input cannot cause a partial batch.
    for plant in records:
        generate_scientific_report(plant)
    return [save_single_report(plant, reports_dir) for plant in records]
