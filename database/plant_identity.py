PLANT_NAME_ALIASES = {
    "Gum Arabic": "Gum Arabic",
    "Acacia senegal": "Gum Arabic",

    "Senna": "Senna",
    "Senna alexandrina": "Senna",

    "Acacia Nilotica": "Acacia Nilotica",
    "Acacia nilotica": "Acacia Nilotica",

    "Moringa": "Moringa",
    "Moringa oleifera": "Moringa",

    "Turmeric": "Turmeric",
    "Curcuma longa": "Turmeric",

    "Henna": "Henna",
    "Lawsonia inermis": "Henna",

    "Hibiscus": "Hibiscus",
    "Hibiscus sabdariffa": "Hibiscus",
}


def resolve_plant_name(name):

    if not name:
        return "Unknown"

    normalized_name = name.strip()

    return PLANT_NAME_ALIASES.get(
        normalized_name,
        normalized_name
    )