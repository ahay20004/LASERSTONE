from pathlib import Path
import csv

from plants_data import plants

QUANTITATIVE_FIELDS = [
    "lambda_abs", "lambda_em", "phi", "tau",
    "sigma_a", "eta", "knr", "refractive_index",
]
REQUIRED_EVIDENCE_METADATA = [
    "source", "doi", "units", "uncertainty",
    "experimental_condition", "value_origin",
]

rows = []
for record in plants:
    for field in QUANTITATIVE_FIELDS:
        numeric_present = field in record and record[field] is not None
        evidence_complete = numeric_present and all(
            record.get(meta) not in (None, "", [], {})
            for meta in REQUIRED_EVIDENCE_METADATA
        )
        rows.append({
            "material": record.get("name", "UNKNOWN"),
            "field": field,
            "numeric_present": int(numeric_present),
            "evidence_complete_under_strict_schema": int(evidence_complete),
        })

out = Path("paper1_outputs")
out.mkdir(exist_ok=True)
path = out / "legacy_registry_audit.csv"
with path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

numeric = sum(r["numeric_present"] for r in rows)
evidence = sum(r["evidence_complete_under_strict_schema"] for r in rows)
print(f"records={len(plants)}")
print(f"quantitative_entries={len(rows)}")
print(f"numeric_present={numeric}")
print(f"evidence_complete_under_strict_schema={evidence}")
print(path)
