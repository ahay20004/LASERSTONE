# LASERSTONE International Scientific University
# Navigation System
# Defines official routes between university buildings

from city.city_theme import DEFAULT_LANGUAGE


UNIVERSITY_ROUTES = {
    "university_gate": {
        "en": "University Gate",
        "ar": "بوابة الجامعة",
        "next": ["university_plaza"],
    },

    "university_plaza": {
        "en": "University Plaza",
        "ar": "ساحة الجامعة",
        "next": [
            "college_of_physics",
            "college_of_materials",
            "college_of_intelligence",
            "college_of_engineering",
            "grand_scientific_library",
            "house_of_scientific_expertise",
            "research_laboratories",
        ],
    },

    "college_of_physics": {
        "en": "College of Physics",
        "ar": "كلية الفيزياء",
        "next": ["research_laboratories", "house_of_scientific_expertise"],
    },

    "college_of_materials": {
        "en": "College of Materials Science",
        "ar": "كلية علوم المواد",
        "next": ["college_of_engineering", "house_of_scientific_expertise"],
    },

    "college_of_intelligence": {
        "en": "College of Scientific Intelligence",
        "ar": "كلية الذكاء العلمي",
        "next": ["house_of_scientific_expertise", "grand_scientific_library"],
    },

    "college_of_engineering": {
        "en": "College of Engineering",
        "ar": "كلية الهندسة",
        "next": ["research_laboratories", "house_of_scientific_expertise"],
    },

    "grand_scientific_library": {
        "en": "Grand Scientific Library",
        "ar": "المكتبة العلمية الكبرى",
        "next": ["university_plaza"],
    },

    "house_of_scientific_expertise": {
        "en": "House of Scientific Expertise",
        "ar": "بيت الخبرة العلمية",
        "next": ["university_plaza"],
    },

    "research_laboratories": {
        "en": "Research Laboratories",
        "ar": "مختبرات البحث العلمي",
        "next": ["university_plaza"],
    },
}


def get_building_name(building_id, language=DEFAULT_LANGUAGE):
    building = UNIVERSITY_ROUTES.get(building_id)

    if building is None:
        return "Unknown Building"

    return building.get(language, building.get("en", "Unknown Building"))


def get_available_destinations(building_id):
    building = UNIVERSITY_ROUTES.get(building_id)

    if building is None:
        return []

    return building.get("next", [])


def can_navigate(from_building, to_building):
    destinations = get_available_destinations(from_building)

    return to_building in destinations


def get_route_summary(language=DEFAULT_LANGUAGE):
    summary = []

    for building_id, building_data in UNIVERSITY_ROUTES.items():
        building_name = get_building_name(building_id, language)
        destinations = building_data.get("next", [])

        destination_names = [
            get_building_name(destination, language)
            for destination in destinations
        ]

        summary.append(
            {
                "building_id": building_id,
                "building_name": building_name,
                "destinations": destination_names,
            }
        )

    return summary