LASERSTONE_MILESTONES = {
    "DASHBOARD_READY": True,
    "LASER_OUTPUT_READY": True,
    "LASER_ARCHITECTURE_READY": True,
    "DIGITAL_TWIN_READY": True,
    "LRI_SYSTEM_COMPLETE": True,
    "LASER_PHYSICS_ENGINE_COMPLETE": True,
    "REFERENCE_VALIDATION_READY": False,
    "PROTOTYPE_READY": False,
    "PUBLICATION_READY": False,
}


LASERSTONE_ROADMAP = {
    "Scientific Evidence Chain": {
        "priority": "HIGH",
        "status": "WAITING",
        "trigger": "LASER_PHYSICS_ENGINE_COMPLETE",
        "scientific_value": 98,
        "patent_value": 85,
        "difficulty": 70,
        "description": (
            "Build a traceable scientific chain linking plant data, "
            "laser physics, architecture decisions, and prototype readiness."
        )
    },

    "Reference Validation Engine": {
        "priority": "HIGH",
        "status": "WAITING",
        "trigger": "LASER_PHYSICS_ENGINE_COMPLETE",
        "scientific_value": 100,
        "patent_value": 80,
        "difficulty": 75,
        "description": (
            "Validate plant optical data, wavelengths, scores, and formulas "
            "against trusted scientific references and DOI sources."
        )
    },

    "Prototype Roadmap": {
        "priority": "HIGH",
        "status": "WAITING",
        "trigger": "LRI_SYSTEM_COMPLETE",
        "scientific_value": 92,
        "patent_value": 88,
        "difficulty": 60,
        "description": (
            "Create a staged prototype path from material selection "
            "to experimental laser validation."
        )
    },

    "Solid-State Plant Dye Laser": {
        "priority": "FUTURE_RESEARCH",
        "status": "WAITING",
        "trigger": "PROTOTYPE_READY",
        "scientific_value": 99,
        "patent_value": 97,
        "difficulty": 90,
        "description": (
            "Study embedding plant-derived dyes into transparent solid hosts "
            "without changing their optical and laser-relevant properties."
        )
    },

    "Host Compatibility Engine": {
        "priority": "FUTURE_RESEARCH",
        "status": "WAITING",
        "trigger": "REFERENCE_VALIDATION_READY",
        "scientific_value": 95,
        "patent_value": 92,
        "difficulty": 85,
        "description": (
            "Evaluate compatibility between plant dyes and solid host materials "
            "for solid-state bio-laser development."
        )
    },

    "Publication Framework": {
        "priority": "MEDIUM",
        "status": "WAITING",
        "trigger": "REFERENCE_VALIDATION_READY",
        "scientific_value": 96,
        "patent_value": 70,
        "difficulty": 65,
        "description": (
            "Prepare LASERSTONE scientific methodology, results, references, "
            "and publication-ready structure."
        )
    }
}


def get_unlocked_roadmap_items():

    unlocked_items = []

    for item_name, item_data in LASERSTONE_ROADMAP.items():

        trigger = item_data.get("trigger")

        if LASERSTONE_MILESTONES.get(trigger, False):

            unlocked_items.append(
                {
                    "name": item_name,
                    **item_data
                }
            )

    return unlocked_items


def get_next_priority_item():

    unlocked_items = get_unlocked_roadmap_items()

    if not unlocked_items:
        return None

    unlocked_items = sorted(
        unlocked_items,
        key=lambda item: (
            item.get("scientific_value", 0)
            + item.get("patent_value", 0)
            - item.get("difficulty", 0)
        ),
        reverse=True
    )

    return unlocked_items[0]


def show_roadmap_alerts():

    print("\n=== LASERSTONE™ ROADMAP ALERTS ===\n")

    unlocked_items = get_unlocked_roadmap_items()

    if not unlocked_items:
        print("No roadmap items are ready yet.")
        return

    for item in unlocked_items:

        print(f"READY ITEM : {item['name']}")
        print(f"Priority   : {item['priority']}")
        print(f"Trigger    : {item['trigger']}")
        print(f"Scientific : {item['scientific_value']}")
        print(f"Patent     : {item['patent_value']}")
        print(f"Difficulty : {item['difficulty']}")
        print(f"Summary    : {item['description']}")
        print("-" * 45)


def show_next_priority():

    next_item = get_next_priority_item()

    print("\n=== NEXT LASERSTONE™ PRIORITY ===\n")

    if next_item is None:
        print("No active priority available.")
        return

    print(f"Next Step : {next_item['name']}")
    print(f"Priority  : {next_item['priority']}")
    print(f"Reason    : Trigger '{next_item['trigger']}' is complete.")
    print(f"Summary   : {next_item['description']}")


if __name__ == "__main__":

    show_roadmap_alerts()
    show_next_priority()