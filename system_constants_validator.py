from constants import (
    MATERIAL_SCORE_WEIGHTS,
    LRI_WEIGHTS,
    CONFIDENCE_WEIGHTS,
    THRESHOLDS
)


def validate_weight_sum(weights_dict):

    total = sum(weights_dict.values())

    return round(total, 2)


def validate_thresholds():

    elite = THRESHOLDS["elite"]

    advanced = THRESHOLDS["advanced"]

    promising = THRESHOLDS["promising"]

    moderate = THRESHOLDS["moderate"]

    if not (
        elite >
        advanced >
        promising >
        moderate
    ):

        return False

    return True


def run_configuration_validation():

    report = {}

    # Weight validation
    report["material_weights"] = (
        validate_weight_sum(
            MATERIAL_SCORE_WEIGHTS
        )
    )

    report["lri_weights"] = (
        validate_weight_sum(
            LRI_WEIGHTS
        )
    )

    report["confidence_weights"] = (
        validate_weight_sum(
            CONFIDENCE_WEIGHTS
        )
    )

    # Threshold validation
    report["thresholds_valid"] = (
        validate_thresholds()
    )

    # Final status
    report["system_valid"] = (

        report["material_weights"] == 1.0

        and

        report["lri_weights"] == 1.0

        and

        report["confidence_weights"] == 0.60

        and

        report["thresholds_valid"]
    )

    return report