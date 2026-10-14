import time


def start_runtime_monitor():

    return time.time()


def stop_runtime_monitor(start_time):

    end_time = time.time()

    runtime = end_time - start_time

    return round(runtime, 2)


def generate_runtime_report(
    runtime,
    total_plants,
    total_engines
):

    return {

        "runtime_seconds": runtime,

        "plants_processed":
        total_plants,

        # This argument is a system-map layer count, not observed execution.
        "declared_layers": total_engines,
        "engines_active": None,
        "execution_status": "NOT_INSTRUMENTED",

        "system_status":
        classify_runtime(runtime)
    }


def classify_runtime(runtime):

    if runtime < 2:
        return "Excellent Runtime Performance"

    elif runtime < 5:
        return "Efficient Runtime Performance"

    elif runtime < 10:
        return "Moderate Runtime Performance"

    else:
        return "Heavy Computational Runtime"
