import os
import re


def ensure_reports_folder(reports_dir="reports"):
    os.makedirs(reports_dir, exist_ok=True)
    return reports_dir


def generate_scientific_report(plant):

    report = f"""
========================================
      LASERSTONE™ SCIENTIFIC REPORT
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
Q screening class     : {plant['q_factor_class']}
Physical Q            : {plant.get('evidence_decision', {}).get('physical_q', {}).get('q', 'UNVERIFIED')}
Evidence decision     : HOLD — independent validation required

----------------------------------------
BEAM & EFFICIENCY
----------------------------------------

Beam quality screening: {plant['beam_quality_class']}
Efficiency screening  : {plant['laser_efficiency_class']}

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

    reports_dir = ensure_reports_folder(reports_dir)

    safe_name = re.sub(r"[^\w-]+", "_", plant["name"].lower()).strip("_") or "unknown_plant"

    report = generate_scientific_report(plant)

    report_path = os.path.join(
        reports_dir,
        f"{safe_name}_report.txt"
    )

    # Exclusive creation preserves previous reports and avoids name collisions.
    index = 0
    while True:
        suffix = "" if index == 0 else f"_{index}"
        report_path = os.path.join(reports_dir, f"{safe_name}_report{suffix}.txt")
        try:
            with open(report_path, "x", encoding="utf-8") as file:
                file.write(report)
            return report_path
        except FileExistsError:
            index += 1


def save_all_reports(plants, reports_dir="reports"):

    saved_reports = []

    for plant in plants:

        report_path = save_single_report(plant, reports_dir)

        saved_reports.append(report_path)

    return saved_reports