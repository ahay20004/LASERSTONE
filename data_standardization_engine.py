def standardize_quality_value(value):
    """
    Convert text-based quality values into numeric scores.
    """

    if value is None:
        return 0

    if isinstance(value, (int, float)):
        return value

    value = str(value).strip().lower()

    quality_map = {
    "high": 100,
    "medium": 60,
    "low": 30,

    "excellent": 100,
    "very good": 85,
    "good": 75,
    "moderate": 60,
    "fair": 50,
    "poor": 20,

    "unknown": 0,
    "n/a": 0
}

    return quality_map.get(value, 0)


def classify_numeric_score(score):
    """
    Convert numeric score into a standard class.
    """

    if score >= 85:
        return "Excellent"

    if score >= 70:
        return "Very Good"

    if score >= 55:
        return "Moderate"

    if score >= 35:
        return "Low"

    return "Very Low"


def standardize_field(plant, source_key, target_score_key, target_class_key):
    """
    Read a plant field, convert it to numeric score,
    then store score and class inside the same plant.
    """

    raw_value = plant.get(source_key, "unknown")

    numeric_score = standardize_quality_value(raw_value)

    numeric_class = classify_numeric_score(numeric_score)

    plant[target_score_key] = numeric_score
    plant[target_class_key] = numeric_class

    return plant