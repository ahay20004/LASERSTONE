"""Use the same checked runtime preparation as the console and scientific city."""
import os
import sys
import traceback

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
CORE_DIR = os.path.join(ROOT_DIR, "core")
DATABASE_DIR = os.path.join(ROOT_DIR, "database")
for path in (ROOT_DIR, CORE_DIR, DATABASE_DIR):
    if path in sys.path:
        sys.path.remove(path)
    sys.path.insert(0, path)

from entry_gateway import open_entry_gateway


def load_plants():
    import copy
    from plants_data import plants
    if not isinstance(plants, (list, tuple)) or not plants:
        raise RuntimeError("Plant database is empty or malformed")
    return copy.deepcopy(plants)


def load_dashboard():
    from dashboard import launch_dashboard
    return launch_dashboard


def prepare_dashboard_plants(plants):
    """Compatibility entry point; all scientific preparation lives in main."""
    try:
        from main import prepare_runtime
        return prepare_runtime(plants)["ranked_plants"]
    except Exception as error:
        print("DASHBOARD PREPARATION ERROR:", error)
        return []


def _open_view(city=False, runtime_state=None):
    if runtime_state is None:
        # Standalone callbacks also use the shared scientific pipeline.
        ranked = prepare_dashboard_plants(load_plants())
    else:
        if runtime_state.get("status") != "ANALYSIS_READY":
            raise RuntimeError("Runtime is not ready")
        ranked = runtime_state["ranked_plants"]
    if not ranked:
        print("View stopped: no validated, ranked records.")
        return False
    if city:
        from dashboard_city import launch_dashboard
    else:
        launch_dashboard = load_dashboard()
    launch_dashboard(ranked, runtime_state=runtime_state)
    return True


def open_dashboard_after_approval(runtime_state=None):
    return _open_view(runtime_state=runtime_state)


def open_city_after_approval(runtime_state=None):
    return _open_view(city=True, runtime_state=runtime_state)


def main(check_only=False):
    from main import prepare_runtime
    # Prepare once; the gateway and selected view consume this same session.
    state = prepare_runtime(load_plants())
    if check_only:
        print("Runtime status:", state["status"])
        print("Ranked materials:", len(state["ranked_plants"]))
        print("Physical validation:", state["physical_validation"])
        print("SCAPS execution:", state["simulators"]["simulators"]["scaps-1d"]["simulation_execution"])
        return state
    open_entry_gateway(
        lambda: open_dashboard_after_approval(state),
        lambda: open_city_after_approval(state),
        runtime_state=state,
    )
    return state


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Checked LASERSTONE launcher")
    parser.add_argument("--check", action="store_true",
                        help="Prepare and verify without GUI, report export or simulator launch")
    args = parser.parse_args()
    try:
        main(check_only=args.check)
    except Exception:
        traceback.print_exc()
        sys.exit(1)
