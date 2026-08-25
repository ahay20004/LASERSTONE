PROJECT_CAPABILITIES = {
    "laser physics": {
        "file": "laser_physics_engine.py",
        "action": "EXTEND EXISTING",
        "location": "After calculate_laser_physics()",
        "reason": "Laser physics calculations already belong here."
    },

    "laser output": {
        "file": "laser_output_engine.py",
        "action": "EXTEND EXISTING",
        "location": "Inside predict_laser_output() or after it",
        "reason": "Laser wavelength, frequency, color, and class are handled here."
    },

    "laser architecture": {
        "file": "laser_architecture_engine.py",
        "action": "EXTEND EXISTING",
        "location": "After generate_architecture_profile()",
        "reason": "Pump, resonator, mirrors, and cooling recommendations belong here."
    },

    "dashboard": {
        "file": "ui/dashboard.py",
        "action": "EXTEND EXISTING",
        "location": "Inside launch_dashboard() or show_plant_details()",
        "reason": "Visual output and user interaction belong in the dashboard."
    },

    "roadmap": {
        "file": "laserstone_master_roadmap.py",
        "action": "EXTEND EXISTING",
        "location": "Inside LASERSTONE_ROADMAP",
        "reason": "Deferred ideas and future triggers belong in the master roadmap."
    },

    "reference validation": {
        "file": "reference_validation_engine.py",
        "action": "CREATE IF MISSING",
        "location": "New engine under project root",
        "reason": "Scientific references and DOI validation need a dedicated engine."
    },

    "scientific trace": {
        "file": "scientific_trace_engine.py",
        "action": "CREATE IF MISSING",
        "location": "New engine under project root",
        "reason": "Decision explanation and evidence chains need a dedicated engine."
    },
}


def scan_project_capability(proposed_feature):

    feature = proposed_feature.lower()

    best_match = None

    for keyword, data in PROJECT_CAPABILITIES.items():

        if keyword in feature:

            best_match = {
                "keyword": keyword,
                **data
            }

            break

    if best_match is None:

        return {
            "status": "UNKNOWN",
            "action": "REVIEW MANUALLY",
            "file": "Not determined",
            "location": "Not determined",
            "reason": "No matching capability was found."
        }

    return {
        "status": "MATCH FOUND",
        **best_match
    }


def show_capability_advice(proposed_feature):

    result = scan_project_capability(
        proposed_feature
    )

    print("\n=== LASERSTONE™ CAPABILITY SCANNER ===\n")
    print(f"Proposed Feature : {proposed_feature}")
    print(f"Status           : {result.get('status')}")
    print(f"Suggested Action : {result.get('action')}")
    print(f"Suggested File   : {result.get('file')}")
    print(f"Location         : {result.get('location')}")
    print(f"Reason           : {result.get('reason')}")


if __name__ == "__main__":

    show_capability_advice(
        "add photon energy to laser physics"
    )