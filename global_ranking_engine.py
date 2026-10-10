"""Rank detached analysis records by unchanged material-score ordering."""
import copy
import math


def rank_plants(plants):
    records = copy.deepcopy(list(plants))
    for record in records:
        score = record.get("material_score")
        if (record.get("valid") is False or record.get("analysis_status") == "BLOCKED"
                or isinstance(score, bool) or not isinstance(score, (int, float))
                or not math.isfinite(score) or not 0 <= score <= 100):
            raise ValueError("Ranking requires an unblocked finite material score in [0, 100]")
    ranked = sorted(records, key=lambda item: item["material_score"], reverse=True)
    for rank, record in enumerate(ranked, 1):
        record["global_rank"] = rank
    return ranked
