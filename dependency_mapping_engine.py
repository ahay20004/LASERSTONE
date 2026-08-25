from project_registry import PROJECT_REGISTRY


def show_dependency_map():

    print("\n=== LASERSTONE DEPENDENCY MAP ===\n")

    for engine_name, info in PROJECT_REGISTRY.items():

        print(f"ENGINE: {engine_name}")

        print("Inputs:")
        for item in info.get("inputs", []):
            print(f"  <- {item}")

        print("Outputs:")
        for item in info.get("outputs", []):
            print(f"  -> {item}")

        print("-" * 40)


def show_dependency_statistics():

    total_inputs = 0
    total_outputs = 0

    most_connected_engine = "N/A"
    most_connections = 0

    for engine_name, info in PROJECT_REGISTRY.items():

        inputs_count = len(
            info.get("inputs", [])
        )

        outputs_count = len(
            info.get("outputs", [])
        )

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
    print("=" * 40)


if __name__ == "__main__":

    show_dependency_map()

    show_dependency_statistics()