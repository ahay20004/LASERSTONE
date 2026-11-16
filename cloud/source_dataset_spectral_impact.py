"""Read-only real-record spectral correction impact, using original main analysis.

No mutation of source records or original modules. Failed records remain blocked.
"""
import copy
import json
from pathlib import Path

from plants_data import plants
from main import analyze_plant
from global_ranking_engine import rank_plants
from cloud.canonical_spectral_material_adapter import CANONICAL
from data_standardization_engine import standardize_quality_value
from material_score_engine import calculate_material_score


def assess_dataset():
    rows = []
    for original in plants:
        name = original.get("name", "Unnamed")
        analyzed = analyze_plant(copy.deepcopy(original))
        if analyzed.get("analysis_status") != "COMPLETE_HEURISTIC_ANALYSIS":
            rows.append({
                "name": name, "status": "BLOCKED",
                "analysis_stage": analyzed.get("analysis_stage"),
                "validation_status": analyzed.get("validation_status"),
                "errors": analyzed.get("validation_errors", {}),
            })
            continue
        label = analyzed.get("spectral_quality")
        if label not in CANONICAL or standardize_quality_value(label) != CANONICAL[label]:
            rows.append({"name": name, "status": "BLOCKED_SPECTRAL_CONTRACT",
                         "label": label})
            continue
        historical_inputs = copy.deepcopy(analyzed)
        historical_inputs["spectral_quality"] = label
        historical = calculate_material_score(historical_inputs)
        corrected = analyzed["material_score"]
        proposed = copy.deepcopy(analyzed)
        proposed["spectral_quality"] = CANONICAL[label]
        if calculate_material_score(proposed) != corrected:
            raise AssertionError("main pipeline does not match canonical spectral score")
        rows.append({
            "name": name, "status": "COMPARED",
            "spectral_label": label, "canonical_spectral_score": CANONICAL[label],
            "legacy_material_score": historical, "corrected_material_score": corrected,
            "delta": round(corrected - historical, 2),
            "scientific_validation": False,
        })
    compared = [row for row in rows if row["status"] == "COMPARED"]
    old_rank = rank_plants([{"name": r["name"], "material_score": r["legacy_material_score"]}
                           for r in compared]) if compared else []
    new_rank = rank_plants([{"name": r["name"], "material_score": r["corrected_material_score"]}
                           for r in compared]) if compared else []
    old_positions = {r["name"]: r["global_rank"] for r in old_rank}
    new_positions = {r["name"]: r["global_rank"] for r in new_rank}
    for row in compared:
        row["old_rank_among_compared"] = old_positions[row["name"]]
        row["new_rank_among_compared"] = new_positions[row["name"]]
    return {
        "scope": "READ_ONLY_SOURCE_DATASET_IMPACT_ASSESSMENT",
        "source": "plants_data.py (repository records; measurements not independently authenticated)",
        "total_records": len(plants),
        "compared": len(compared),
        "blocked": len(rows) - len(compared),
        "rows": rows,
        "original_main_modified": True,
        "original_data_modified": False,
        "physical_validation": False,
        "limitations": [
            "Only successfully analyzed records are ranked; blocked records never receive inferred scores",
            "Rank positions are within compared subset only",
            "Main analysis and source data may contain heuristic assumptions",
            "Production main.py now passes the existing numeric spectral_quality_score to material scoring",
        ],
    }


def main():
    result = assess_dataset()
    dest = Path("audit-artifacts")
    dest.mkdir(exist_ok=True)
    (dest / "source_dataset_spectral_impact.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False, default=str) + "\n",
        encoding="utf-8")
    lines = [
        "# Source dataset — spectral material correction impact",
        "", f"Source records: {result['total_records']}; compared: {result['compared']}; "
        f"blocked: {result['blocked']}.", "",
        "| Material | Status | Spectral | Old score | Corrected score | Delta | Old rank | New rank |",
        "|---|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in result["rows"]:
        if row["status"] != "COMPARED":
            lines.append(f"| {row['name']} | {row['status']} | — | — | — | — | — | — |")
        else:
            lines.append(f"| {row['name']} | COMPARED | {row['spectral_label']} | "
                         f"{row['legacy_material_score']:.2f} | "
                         f"{row['corrected_material_score']:.2f} | "
                         f"{row['delta']:+.2f} | {row['old_rank_among_compared']} | "
                         f"{row['new_rank_among_compared']} |")
    lines += ["", "This is an impact assessment of existing heuristic records, not experimental validation.",
              "The original dataset and scientific engines are unchanged; main.py spectral handoff is corrected.", ""]
    (dest / "SOURCE_DATASET_SPECTRAL_IMPACT.md").write_text(
        "\n".join(lines), encoding="utf-8")
    print(json.dumps({"total_records": result["total_records"], "compared": result["compared"],
                      "blocked": result["blocked"]}, indent=2))


if __name__ == "__main__":
    main()
