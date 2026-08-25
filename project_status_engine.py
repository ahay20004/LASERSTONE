PROJECT_STATUS = {

    "phase": "PLANT-BASED LASER DESIGN PLATFORM",

    "core_platform": {
        "plant_database_ready": True,
        "material_score_ready": True,
        "thermal_analysis_ready": True,
        "feasibility_analysis_ready": True,
        "q_factor_ready": True,
        "ranking_ready": True,
    },

    "laser_design": {
        "laser_output_ready": True,
        "laser_architecture_ready": True,
        "digital_twin_ready": True,
        "laser_physics_ready": True,
        "laser_readiness_ready": True,
    },

    "governance": {
        "project_registry_ready": True,
        "system_health_ready": True,
        "roadmap_ready": True,
        "capability_scanner_ready": True,
        "project_governor_ready": False,
    },

    "scientific_validation": {
        "scientific_trace_ready": False,
        "reference_validation_ready": False,
        "experimental_validation_ready": False,
        "publication_ready": False,
    },

    "prototype_path": {
        "prototype_roadmap_ready": False,
        "solid_state_dye_laser_ready": False,
        "host_compatibility_ready": False,
        "prototype_ready": False,
    }
}


def calculate_section_progress(section):

    values = PROJECT_STATUS.get(
        section,
        {}
    )

    if not values:
        return 0

    total = len(values)

    completed = sum(
        1 for value in values.values()
        if value is True
    )

    return round(
        (completed / total) * 100,
        2
    )


def calculate_overall_progress():

    total_items = 0
    completed_items = 0

    for section, values in PROJECT_STATUS.items():

        if isinstance(values, dict):

            total_items += len(values)

            completed_items += sum(
                1 for value in values.values()
                if value is True
            )

    if total_items == 0:
        return 0

    return round(
        (completed_items / total_items) * 100,
        2
    )


def get_project_stage():

    progress = calculate_overall_progress()

    if progress >= 90:
        return "ADVANCED SCIENTIFIC PLATFORM"

    elif progress >= 70:
        return "INTEGRATED LASER DESIGN PLATFORM"

    elif progress >= 50:
        return "ACTIVE DEVELOPMENT PLATFORM"

    else:
        return "EARLY DEVELOPMENT PLATFORM"


def get_blocked_items():

    blocked = []

    for section, values in PROJECT_STATUS.items():

        if isinstance(values, dict):

            for item, value in values.items():

                if value is False:

                    blocked.append(
                        {
                            "section": section,
                            "item": item
                        }
                    )

    return blocked


def show_project_status():

    print("\n=== LASERSTONE™ PROJECT STATUS ===\n")

    print(
        f"Current Phase : {PROJECT_STATUS['phase']}"
    )

    print(
        f"Overall Progress : {calculate_overall_progress()}%"
    )

    print(
        f"Project Stage : {get_project_stage()}"
    )

    print("\n--- SECTION PROGRESS ---\n")

    for section in PROJECT_STATUS:

        if isinstance(PROJECT_STATUS[section], dict):

            print(
                f"{section} : "
                f"{calculate_section_progress(section)}%"
            )

    print("\n--- PENDING ITEMS ---\n")

    blocked_items = get_blocked_items()

    if not blocked_items:
        print("All project items are complete.")
        return

    for item in blocked_items:

        print(
            f"{item['section']} -> {item['item']}"
        )


def get_project_status_summary():

    return {
        "phase": PROJECT_STATUS["phase"],
        "overall_progress": calculate_overall_progress(),
        "project_stage": get_project_stage(),
        "core_platform": calculate_section_progress("core_platform"),
        "laser_design": calculate_section_progress("laser_design"),
        "governance": calculate_section_progress("governance"),
        "scientific_validation": calculate_section_progress(
            "scientific_validation"
        ),
        "prototype_path": calculate_section_progress(
            "prototype_path"
        ),
        "pending_items": get_blocked_items()
    }

def get_next_strategic_target():

    targets = {

        "scientific_trace_ready":
        "Build Scientific Evidence Chain",

        "reference_validation_ready":
        "Build Reference Validation Engine",

        "experimental_validation_ready":
        "Prepare Experimental Validation Layer",

        "prototype_roadmap_ready":
        "Build Prototype Roadmap",

        "solid_state_dye_laser_ready":
        "Research Solid-State Plant Dye Laser",

        "host_compatibility_ready":
        "Research Host Compatibility",

        "prototype_ready":
        "Prepare First Prototype",

        "publication_ready":
        "Prepare Publication Framework"
    }

    blocked = get_blocked_items()

    for key in targets:

        for item in blocked:

            if item["item"] == key:

                return targets[key]

    return "PROJECT COMPLETE"


    print(f"Project Stage : {get_project_stage()}")
    print("\n--- NEXT STRATEGIC TARGET ---\n")
    print(get_next_strategic_target())
    print("\n--- SECTION PROGRESS ---\n")

if __name__ == "__main__":

    show_project_status()