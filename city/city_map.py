# LASERSTONE International Scientific University
# Scientific City Map

CITY_BUILDINGS = {
    "university_plaza": {
        "name": "University Plaza",
        "role": "Central scientific entry point",
        "zone": "center",
        "symbol": "🏛️",
    },
    "college_of_physics": {
        "name": "College of Physics",
        "role": "Laser physics, optics, quantum and thermal evidence",
        "zone": "north",
        "symbol": "⚛️",
    },
    "college_of_materials": {
        "name": "College of Materials Science",
        "role": "Material ranking, spectroscopy and laser medium evaluation",
        "zone": "east",
        "symbol": "🌿",
    },
    "college_of_engineering": {
        "name": "College of Engineering",
        "role": "Prototype planning, cavity design and laser construction path",
        "zone": "south",
        "symbol": "⚙️",
    },
    "college_of_intelligence": {
        "name": "College of Scientific Intelligence",
        "role": "Scientific recommendations, confidence and decision support",
        "zone": "west",
        "symbol": "🧠",
    },
    "house_of_scientific_expertise": {
        "name": "House of Scientific Expertise",
        "role": "Final integrated scientific judgment",
        "zone": "core",
        "symbol": "🏛️",
    },
    "grand_scientific_library": {
        "name": "Grand Scientific Library",
        "role": "Scientific references, reports and knowledge archive",
        "zone": "east_wing",
        "symbol": "📚",
    },
    "research_laboratories": {
        "name": "Research Laboratories",
        "role": "Experimental validation and prototype testing",
        "zone": "south_wing",
        "symbol": "🔬",
    },
}


LASER_FRUIT_PATH = [
    "college_of_materials",
    "college_of_physics",
    "college_of_engineering",
    "house_of_scientific_expertise",
    "research_laboratories",
]


def get_building(building_id):
    return CITY_BUILDINGS.get(building_id, {})


def get_all_buildings():
    return CITY_BUILDINGS


def get_laser_fruit_path():
    return LASER_FRUIT_PATH


def get_laser_fruit_summary():
    return [
        CITY_BUILDINGS[building_id]["name"]
        for building_id in LASER_FRUIT_PATH
        if building_id in CITY_BUILDINGS
    ]