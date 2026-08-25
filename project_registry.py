PROJECT_REGISTRY = {

    "spectral_quality_engine": {
        "status": "ACTIVE",
        "category": "Scientific Analysis",
        "standardized": True,
        "dashboard_visible": True,
        "inputs": [
            "lambda_abs",
            "lambda_em"
        ],
        "outputs": [
            "spectral_quality",
            "spectral_quality_score",
            "spectral_quality_class"
        ]
    },

    "material_score_engine": {
        "status": "ACTIVE",
        "category": "Scientific Analysis",
        "standardized": True,
        "dashboard_visible": True,
        "inputs": [
            "plant_data"
        ],
        "outputs": [
            "material_score",
            "material_class"
        ]
    },

    "thermal_engine": {
        "status": "ACTIVE",
        "category": "Scientific Analysis",
        "standardized": True,
        "dashboard_visible": True,
        "inputs": [
            "plant_data"
        ],
        "outputs": [
            "thermal_score",
            "thermal_class"
        ]
    },

    "qfactor_engine": {
        "status": "ACTIVE",
        "category": "Scientific Analysis",
        "standardized": True,
        "dashboard_visible": True,
        "inputs": [
            "plant_data"
        ],
        "outputs": [
            "q_factor_score"
        ]
    },

    "feasibility_engine": {
    "status": "ACTIVE",
    "category": "Scientific Analysis",
    "standardized": True,
    "dashboard_visible": True,
    "inputs": [
        "plant_data"
    ],
    "outputs": [
        "feasibility_score",
        "feasibility_class"
    ]
},

"gain_ranking_engine": {
    "status": "ACTIVE",
    "category": "Ranking",
    "standardized": True,
    "dashboard_visible": True,
    "inputs": [
        "gain_score"
    ],
    "outputs": [
        "gain_rank"
    ]
},

"global_ranking_engine": {
    "status": "ACTIVE",
    "category": "Ranking",
    "standardized": True,
    "dashboard_visible": True,
    "inputs": [
        "material_score",
        "thermal_score",
        "q_factor_score"
    ],
    "outputs": [
        "global_rank"
    ]
},

"final_decision_engine": {
    "status": "ACTIVE",
    "category": "Decision Support",
    "standardized": True,
    "dashboard_visible": True,
    "inputs": [
        "global_rank",
        "feasibility_score",
        "strategic_advice"
    ],
    "outputs": [
        "final_decision"
    ]
},

"intelligence_hub": {
    "status": "ACTIVE",
    "category": "Artificial Intelligence",
    "standardized": True,
    "dashboard_visible": True,
    "inputs": [
        "global_rank",
        "feasibility_score",
        "thermal_score",
        "material_score"
    ],
    "outputs": [
        "intelligence_report"
    ]
},

"project_health_engine": {
    "status": "ACTIVE",
    "category": "System Health",
    "standardized": True,
    "dashboard_visible": True,
    "inputs": [
        "PROJECT_REGISTRY"
    ],
    "outputs": [
        "project_health_status"
    ]
},

"system_health_engine": {
    "status": "ACTIVE",
    "category": "System Health",
    "standardized": True,
    "dashboard_visible": True,
    "inputs": [
        "project_health_status"
    ],
    "outputs": [
        "system_health_status"
    ]
},

"system_integrity_engine": {
    "status": "ACTIVE",
    "category": "System Health",
    "standardized": True,
    "dashboard_visible": True,
    "inputs": [
        "PROJECT_REGISTRY",
        "system_health_status"
    ],
    "outputs": [
        "system_integrity_status"
    ]
},

"runtime_monitor_engine": {
    "status": "ACTIVE",
    "category": "Runtime Monitoring",
    "standardized": True,
    "dashboard_visible": True,
    "inputs": [
        "system_integrity_status"
    ],
    "outputs": [
        "runtime_status"
    ]
},

"network_intelligence_engine": {
    "status": "ACTIVE",
    "category": "Infrastructure Intelligence",
    "standardized": True,
    "dashboard_visible": True,
    "inputs": [
        "PROJECT_REGISTRY",
        "runtime_status"
    ],
    "outputs": [
        "network_intelligence_report"
    ]
},
"scientific_confidence_engine": {
    "status": "ACTIVE",
    "category": "Scientific Validation",
    "standardized": True,
    "dashboard_visible": True,
    "inputs": [
        "material_score",
        "thermal_score",
        "q_factor_score"
    ],
    "outputs": [
        "scientific_confidence"
    ]
},
"research_novelty_engine": {
    "status": "ACTIVE",
    "category": "Research Evaluation",
    "standardized": True,
    "dashboard_visible": True,
    "inputs": [
        "scientific_confidence"
    ],
    "outputs": [
        "research_novelty_score"
    ]
},
"physics_consistency_engine": {
    "status": "ACTIVE",
    "category": "Scientific Validation",
    "standardized": True,
    "dashboard_visible": True,
    "inputs": [
        "lambda_abs",
        "lambda_em"
    ],
    "outputs": [
        "physics_consistency_score"
    ]
},
"photobleaching_engine": {
    "status": "ACTIVE",
    "category": "Optical Stability",
    "standardized": True,
    "dashboard_visible": True,
    "inputs": [
        "plant_data"
    ],
    "outputs": [
        "photobleaching_score"
    ]
},
"patent_potential_engine": {
    "status": "ACTIVE",
    "category": "Innovation Assessment",
    "standardized": True,
    "dashboard_visible": True,
    "inputs": [
        "research_novelty_score",
        "scientific_confidence"
    ],
    "outputs": [
        "patent_potential_score"
    ]
},
"scientific_recommendation_engine": {
    "status": "ACTIVE",
    "category": "Scientific Decision",
    "standardized": True,
    "dashboard_visible": True,
    "inputs": [
        "scientific_confidence",
        "patent_potential_score"
    ],
    "outputs": [
        "scientific_recommendation"
    ]
},
"strategic_advisor_engine": {
    "status": "ACTIVE",
    "category": "Strategic Analysis",
    "standardized": True,
    "dashboard_visible": True,
    "inputs": [
        "scientific_recommendation",
        "global_rank"
    ],
    "outputs": [
        "strategic_advice"
    ]
},

"operation_mode_engine": {
    "status": "ACTIVE",
    "category": "System Control",
    "standardized": True,
    "dashboard_visible": True,
    "inputs": [
        "final_decision"
    ],
    "outputs": [
        "operation_mode"
    ]
},
"data_standardization_engine": {
    "status": "ACTIVE",
    "category": "Data Processing",
    "standardized": True,
    "dashboard_visible": True,
    "inputs": [
        "raw_classifications"
    ],
    "outputs": [
        "standardized_scores"
    ]
},

"spectral_analysis": {
    "status": "ACTIVE",
    "category": "Spectral Analysis",
    "standardized": True,
    "dashboard_visible": True,
    "inputs": [
        "lambda_abs",
        "lambda_em"
    ],
    "outputs": [
        "spectral_analysis_report"
    ]
},
"spectral_region": {
    "status": "ACTIVE",
    "category": "Spectral Classification",
    "standardized": True,
    "dashboard_visible": True,
    "inputs": [
        "lambda_em"
    ],
    "outputs": [
        "spectral_region"
    ]
},
"laser_sources": {
    "status": "ACTIVE",
    "category": "Laser Engineering",
    "standardized": True,
    "dashboard_visible": True,
    "inputs": [
        "spectral_region"
    ],
    "outputs": [
        "recommended_laser_source"
    ]
},

"beam_quality_engine": {
    "status": "ACTIVE",
    "category": "Laser Engineering",
    "standardized": True,
    "dashboard_visible": True,
    "inputs": [
        "lambda_em",
        "spectral_quality_score"
    ],
    "outputs": [
        "beam_quality_score"
    ]
},
"dependency_mapping_engine": {
    "status": "ACTIVE",
    "category": "Infrastructure Intelligence",
    "standardized": True,
    "dashboard_visible": True,
    "inputs": [
        "PROJECT_REGISTRY"
    ],
    "outputs": [
        "dependency_map"
    ]
},
"efficiency_engine": {
    "status": "ACTIVE",
    "category": "Performance Analysis",
    "standardized": True,
    "dashboard_visible": True,
    "inputs": [
        "material_score",
        "thermal_score"
    ],
    "outputs": [
        "efficiency_score"
    ]
},
"export_engine": {
    "status": "ACTIVE",
    "category": "Data Export",
    "standardized": True,
    "dashboard_visible": True,
    "inputs": [
        "plant_data"
    ],
    "outputs": [
        "export_package"
    ]
},
"final_snapshot_engine": {
    "status": "ACTIVE",
    "category": "System Monitoring",
    "standardized": True,
    "dashboard_visible": True,
    "inputs": [
        "global_rank",
        "final_decision"
    ],
    "outputs": [
        "system_snapshot"
    ]
},


    "recommendation_engine": {
        "status": "ACTIVE",
        "category": "Decision Support",
        "standardized": True,
        "dashboard_visible": True,
        "inputs": [
            "ranked_plants"
        ],
        "outputs": [
            "recommended_material",
            "best_overall_material",
            "best_patent_candidate",
            "system_assessment"
        ]
    }
}


def show_registered_engines():

    print("\n=== LASERSTONE ENGINE REGISTRY ===\n")

    for engine, info in PROJECT_REGISTRY.items():

        print(f"ENGINE: {engine}")
        print(f"STATUS: {info['status']}")
        print(f"CATEGORY: {info['category']}")
        print(f"STANDARDIZED: {info['standardized']}")
        print(f"DASHBOARD: {info['dashboard_visible']}")
        print("-" * 40)


def registry_statistics():

    total_engines = len(PROJECT_REGISTRY)

    standardized = sum(
        1
        for engine in PROJECT_REGISTRY.values()
        if engine["standardized"]
    )

    dashboard_engines = sum(
        1
        for engine in PROJECT_REGISTRY.values()
        if engine["dashboard_visible"]
    )

    print("\n=== REGISTRY STATISTICS ===\n")
    print(f"Total Engines: {total_engines}")
    print(f"Standardized Engines: {standardized}")
    print(f"Dashboard Engines: {dashboard_engines}")


def show_dependency_map():

    print("\n=== DEPENDENCY MAP ===\n")

    for engine_name, info in PROJECT_REGISTRY.items():

        print(f"ENGINE: {engine_name}")

        print("INPUTS:")
        for input_item in info.get("inputs", []):
            print(f"  <- {input_item}")

        print("OUTPUTS:")
        for output_item in info.get("outputs", []):
            print(f"  -> {output_item}")

        print("-" * 40)


def show_dependency_statistics():

    total_inputs = 0
    total_outputs = 0

    most_connected_engine = ""
    most_connections = 0

    for engine_name, info in PROJECT_REGISTRY.items():

        inputs_count = len(info.get("inputs", []))
        outputs_count = len(info.get("outputs", []))

        total_inputs += inputs_count
        total_outputs += outputs_count

        connections = inputs_count + outputs_count

        if connections > most_connections:
            most_connections = connections
            most_connected_engine = engine_name

    print("\n=== DEPENDENCY STATISTICS ===\n")
    print(f"Total Registered Engines: {len(PROJECT_REGISTRY)}")
    print(f"Total Inputs: {total_inputs}")
    print(f"Total Outputs: {total_outputs}")
    print(f"Most Connected Engine: {most_connected_engine}")
    print(f"Connections: {most_connections}")


def detect_unused_outputs():
    
    all_inputs = []
    all_outputs = []
    output_sources = {}

    for engine_name, info in PROJECT_REGISTRY.items():

        inputs = info.get("inputs", [])
        outputs = info.get("outputs", [])

        all_inputs.extend(inputs)
        all_outputs.extend(outputs)

        for output in outputs:
            output_sources[output] = engine_name

    unused_outputs = []

    for output in all_outputs:

        if output not in all_inputs:
            unused_outputs.append(output)

    print("\n=== UNUSED OUTPUTS DETECTOR ===\n")

    if not unused_outputs:
        print("All outputs are currently used by other engines.")
        return

    for output in unused_outputs:
        print(f"Unused Output: {output}")
        print(f"Produced By: {output_sources.get(output)}")
        print("Status: NOT USED")
        print("-" * 40)

def validate_registry_structure():

    required_keys = [
        "status",
        "category",
        "standardized",
        "dashboard_visible",
        "inputs",
        "outputs"
    ]

    print("\n=== REGISTRY STRUCTURE VALIDATION ===\n")

    errors_found = False

    for engine_name, info in PROJECT_REGISTRY.items():

        for key in required_keys:

            if key not in info:

                print(f"ERROR: {engine_name} missing key: {key}")
                errors_found = True

        if "inputs" in info and not isinstance(info["inputs"], list):

            print(f"ERROR: {engine_name} inputs must be a list")
            errors_found = True

        if "outputs" in info and not isinstance(info["outputs"], list):

            print(f"ERROR: {engine_name} outputs must be a list")
            errors_found = True

    if not errors_found:

        print("Registry structure is valid.")

def dependency_impact_report():

    print("\n=== DEPENDENCY IMPACT REPORT ===\n")

    impact_results = []

    for engine_name, info in PROJECT_REGISTRY.items():

        impact_count = 0
        impacted_engines = []

        for output_item in info.get("outputs", []):

            for other_engine, other_info in PROJECT_REGISTRY.items():

                if output_item in other_info.get("inputs", []):

                    impact_count += 1
                    impacted_engines.append(other_engine)

        impact_results.append(
            {
                "engine": engine_name,
                "impact_count": impact_count,
                "impacted_engines": impacted_engines
            }
        )

    impact_results = sorted(
        impact_results,
        key=lambda x: x["impact_count"],
        reverse=True
    )

    for result in impact_results:

        if result["impact_count"] > 0:

            print(
                f'{result["engine"]}: impacts {result["impact_count"]} engine(s)'
            )

            print(
                f'Affected: {", ".join(result["impacted_engines"])}'
            )

            print("-" * 40)

    zero_impact = sum(
        1
        for result in impact_results
        if result["impact_count"] == 0
    )

    print(
        f"\nZero Impact Engines: {zero_impact}"
    )

    
def connected_engines_report():

    print(
        "\n=== CONNECTED ENGINES REPORT ===\n"
    )

    connections_found = 0

    for engine_name, info in PROJECT_REGISTRY.items():

        outputs = info.get(
            "outputs",
            []
        )

        for output_item in outputs:

            for other_engine, other_info in PROJECT_REGISTRY.items():

                if engine_name == other_engine:
                    continue

                if output_item in other_info.get(
                    "inputs",
                    []
                ):

                    print(
                        f"{engine_name}"
                    )

                    print(
                        f"  ↓ {output_item}"
                    )

                    print(
                        f"{other_engine}"
                    )

                    print(
                        "-" * 40
                    )

                    connections_found += 1

    print(
        f"\nTotal Connections Found: {connections_found}"
    )
def most_influential_engine_report():

    print(
        "\n=== MOST INFLUENTIAL ENGINE REPORT ===\n"
    )

    engine_scores = []

    for engine_name, info in PROJECT_REGISTRY.items():

        influence_score = 0

        for output_item in info.get(
            "outputs",
            []
        ):

            for other_engine, other_info in PROJECT_REGISTRY.items():

                if output_item in other_info.get(
                    "inputs",
                    []
                ):

                    influence_score += 1

        engine_scores.append(
            (
                engine_name,
                influence_score
            )
        )

    engine_scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    for rank, (engine, score) in enumerate(
        engine_scores,
        start=1
    ):

        print(
            f"{rank}. {engine} -> Influence Score: {score}"
        )

    print("\n----------------------------")

    print(
        f"Most Influential Engine: {engine_scores[0][0]}"
    )

    print(
        f"Influence Score: {engine_scores[0][1]}"
    )
def most_influential_engine_report():

    print(
        "\n=== MOST INFLUENTIAL ENGINE REPORT ===\n"
    )

    engine_scores = []

    for engine_name, info in PROJECT_REGISTRY.items():

        influence_score = 0
        influenced_engines = []

        for output_item in info.get("outputs", []):

            for other_engine, other_info in PROJECT_REGISTRY.items():

                if engine_name == other_engine:
                    continue

                if output_item in other_info.get("inputs", []):

                    influence_score += 1
                    influenced_engines.append(other_engine)

        engine_scores.append(
            {
                "engine": engine_name,
                "score": influence_score,
                "influenced": influenced_engines
            }
        )

    engine_scores = sorted(
        engine_scores,
        key=lambda x: x["score"],
        reverse=True
    )

    for rank, result in enumerate(engine_scores[:5], start=1):

        if result["score"] >= 3:
            criticality = "HIGH"
        elif result["score"] == 2:
            criticality = "MEDIUM"
        elif result["score"] == 1:
            criticality = "LOW"
        else:
            criticality = "NONE"

        print(
            f'{rank}. {result["engine"]}'
        )

        print(
            f'Influence Score: {result["score"]}'
        )

        print(
            f'Criticality: {criticality}'
        )

        if result["influenced"]:
            print(
                "Influences: "
                + ", ".join(result["influenced"])
            )

        print("-" * 40)

    print(
        f'\nMost Influential Engine: {engine_scores[0]["engine"]}'
    )

    print(
        f'Influence Score: {engine_scores[0]["score"]}'
    )
def most_dependent_engine_report():

    print(
        "\n=== MOST DEPENDENT ENGINE REPORT ===\n"
    )

    dependency_scores = []

    for engine_name, info in PROJECT_REGISTRY.items():

        dependency_score = len(
            info.get(
                "inputs",
                []
            )
        )

        dependency_scores.append(
            (
                engine_name,
                dependency_score
            )
        )

    dependency_scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    for rank, (engine, score) in enumerate(
        dependency_scores[:10],
        start=1
    ):

        print(
            f"{rank}. {engine}"
        )

        print(
            f"Dependency Score: {score}"
        )

        print("-" * 40)

    print(
        f"\nMost Dependent Engine: {dependency_scores[0][0]}"
    )

    print(
        f"Dependency Score: {dependency_scores[0][1]}"
    )

def critical_engine_report():

    print(
        "\n=== CRITICAL ENGINE REPORT ===\n"
    )

    engine_results = []

    for engine_name, info in PROJECT_REGISTRY.items():

        influence_score = 0

        for output_item in info.get(
            "outputs",
            []
        ):

            for other_engine, other_info in PROJECT_REGISTRY.items():

                if output_item in other_info.get(
                    "inputs",
                    []
                ):

                    influence_score += 1

        dependency_score = len(
            info.get(
                "inputs",
                []
            )
        )

        critical_score = (
            influence_score +
            dependency_score
        )

        engine_results.append(
            {
                "engine": engine_name,
                "influence": influence_score,
                "dependency": dependency_score,
                "critical": critical_score
            }
        )

    engine_results.sort(
        key=lambda x: x["critical"],
        reverse=True
    )

    for rank, result in enumerate(
        engine_results[:10],
        start=1
    ):

        print(
            f"{rank}. {result['engine']}"
        )

        print(
            f"Influence Score: {result['influence']}"
        )

        print(
            f"Dependency Score: {result['dependency']}"
        )

        print(
            f"Critical Score: {result['critical']}"
        )

        print(
            "-" * 40
        )

    print(
        f"\nMost Critical Engine: {engine_results[0]['engine']}"
    )

    print(
        f"Critical Score: {engine_results[0]['critical']}"
    )
def isolated_engines_report():

    print(
        "\n=== ISOLATED ENGINES REPORT ===\n"
    )

    isolated_count = 0

    for engine_name, info in PROJECT_REGISTRY.items():

        influence_score = 0

        for output_item in info.get(
            "outputs",
            []
        ):

            for other_engine, other_info in PROJECT_REGISTRY.items():

                if output_item in other_info.get(
                    "inputs",
                    []
                ):

                    influence_score += 1

        dependency_score = len(
            info.get(
                "inputs",
                []
            )
        )

        if (
            influence_score == 0
            and
            dependency_score <= 1
        ):

            print(
                engine_name
            )

            isolated_count += 1

    print(
        f"\nTotal Isolated Engines: {isolated_count}"
    )

def duplicate_engine_detector():

    print("\n=== DUPLICATE ENGINE DETECTOR ===\n")

    import re

    with open(__file__, "r", encoding="utf-8") as file:
        content = file.read()

    engine_names = re.findall(
        r'"([a-zA-Z0-9_]+)"\s*:\s*{',
        content
    )

    counts = {}

    for name in engine_names:
        counts[name] = counts.get(name, 0) + 1

    duplicates = {
        name: count
        for name, count in counts.items()
        if count > 1
    }

    if not duplicates:
        print("No duplicate engines found.")
        print("Registry Status: CLEAN")
        return

    print(f"Duplicate Engines Found: {len(duplicates)}\n")

    for name, count in duplicates.items():
        print(f"Duplicate Engine: {name}")
        print(f"Occurrences: {count}")
        print("Status: NEEDS CLEANUP")
        print("-" * 40)

    print("Registry Status: WARNING")



def smart_duplicate_resolver():

    print("\n=== SMART DUPLICATE RESOLVER ===\n")

    import re

    with open(__file__, "r", encoding="utf-8") as file:
        content = file.read()

    pattern = r'"([a-zA-Z0-9_]+)"\s*:\s*{'

    matches = list(
        re.finditer(pattern, content)
    )

    engine_locations = {}

    for match in matches:

        engine_name = match.group(1)
        start_index = match.start()

        engine_locations.setdefault(
            engine_name,
            []
        ).append(start_index)

    duplicates = {
        name: locations
        for name, locations in engine_locations.items()
        if len(locations) > 1
    }

    if not duplicates:

        print("No duplicate engines found.")
        print("Smart Resolver Status: CLEAN")
        return

    for engine_name, locations in duplicates.items():

        print(f"Duplicate Engine: {engine_name}")
        print(f"Copies Found: {len(locations)}")

        print("Recommendation:")
        print("- Compare copies before deleting.")
        print("- If identical: delete one copy.")
        print("- If different: merge inputs/outputs, then delete extra copy.")

        print("Status: REVIEW REQUIRED")
        print("-" * 50)

    print("Smart Resolver Status: REVIEW NEEDED")

if __name__ == "__main__":

    show_registered_engines()
    registry_statistics()
    show_dependency_map()
    show_dependency_statistics()
    detect_unused_outputs()
    validate_registry_structure()
    dependency_impact_report()
    connected_engines_report()
    most_influential_engine_report()
    most_dependent_engine_report()
    critical_engine_report()
    isolated_engines_report()
    duplicate_engine_detector()
    smart_duplicate_resolver()