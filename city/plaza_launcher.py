"""University entry point using the same checked project runtime."""
import sys
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from main import prepare_runtime
    from dashboard_city import launch_dashboard
    state = prepare_runtime()
    launch_dashboard(state["ranked_plants"], runtime_state=state, open_university=True)


if __name__ == "__main__":
    main()
