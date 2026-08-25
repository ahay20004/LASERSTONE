REQUIRED_FIELDS = [

    "name",
    "scientific_name",
    "origin",

    "phi",
    "tau",
    "sigma_a",
    "eta",
    "knr",
    "refractive_index",

    "lambda_abs",
    "lambda_em"
]


def validate_plant_data(plant):

    missing_fields = []

    for field in REQUIRED_FIELDS:

        if field not in plant:

            missing_fields.append(field)

    if missing_fields:

        return {
            "valid": False,
            "missing": missing_fields
        }

    return {
        "valid": True,
        "missing": []
    }