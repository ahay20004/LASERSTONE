import os
import sys
import traceback

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
CORE_DIR = os.path.join(ROOT_DIR, "core")
DATABASE_DIR = os.path.join(ROOT_DIR, "database")

for path in [ROOT_DIR, CORE_DIR, DATABASE_DIR]:
    if path not in sys.path:
        sys.path.insert(0, path)

from entry_gateway import open_entry_gateway
from executive_summary_engine import generate_executive_summary

def load_plants():
    try:
        from plants_data import plants
        return plants

    except Exception as error:
        print("PLANTS LOAD ERROR:")
        print(error)
        return []


def load_dashboard():
    try:
        from dashboard import launch_dashboard
        return launch_dashboard

    except Exception as error:
        print("DASHBOARD LOAD ERROR:")
        print(error)
        return None
def prepare_dashboard_plants(plants):

    try:
        from main import analyze_plant
        from global_ranking_engine import rank_plants

    except Exception as error:
        print("DASHBOARD PREPARATION IMPORT ERROR:")
        print(error)
        return plants

    analyzed_plants = []

    for plant in plants:

        try:
            analyzed_plant = analyze_plant(plant)

            if analyzed_plant.get("valid", True):
                analyzed_plants.append(analyzed_plant)

        except Exception as error:
            print("PLANT ANALYSIS ERROR:")
            print(plant.get("name", "Unknown"))
            print(error)

    if not analyzed_plants:
        return plants

    try:
        return rank_plants(analyzed_plants)

    except Exception as error:
        print("RANKING ERROR:")
        print(error)
        return analyzed_plants
def open_dashboard_after_approval():

    plants = load_plants()

    if not plants:
        print("No plants loaded.")
        return

    launch_dashboard = load_dashboard()

    if launch_dashboard is None:
        print("Dashboard could not be loaded.")
        return

    try:
        dashboard_plants = prepare_dashboard_plants(plants)
        launch_dashboard(dashboard_plants)

    except Exception:
        print("DASHBOARD RUNTIME ERROR:")
        traceback.print_exc()

def open_city_after_approval():

    try:
        plants = load_plants()

        if not plants:
            print("No plants loaded for Scientific City.")
            return

        from dashboard_city import launch_dashboard

        city_plants = prepare_dashboard_plants(plants)

        launch_dashboard(city_plants)

    except Exception:
        print("SCIENTIFIC CITY RUNTIME ERROR:")
        traceback.print_exc()
def main():

    print("\n===================================")
    print("LASERSTONE SAFE DASHBOARD LAUNCHER")
    print("===================================")

    open_entry_gateway(
        open_dashboard_after_approval,
        open_city_after_approval
   )


if __name__ == "__main__":
    main()