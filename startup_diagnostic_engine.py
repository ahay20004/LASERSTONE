
import os
from pathlib import Path

def run_startup_diagnostic():

    print("\n=== LASERSTONE STARTUP DIAGNOSTIC ===\n")

    current_folder = os.getcwd()
    active_root = Path(__file__).resolve().parent
    if Path(current_folder).resolve() != active_root:
        print(f"Startup Status: PATH ERROR; run from active root: {active_root}")
        return False

    print(f"Current Folder:")
    print(current_folder)

           
    required_files = [
    "main.py",
    "project_registry.py",
    "dashboard.py",
    os.path.join("database", "plant_references.py")
]

    missing_files = []

    for file_path in required_files:
        if not os.path.isfile(file_path):
            missing_files.append(file_path)

    if missing_files:
        print("\nProblem: Missing required files")

        for file_path in missing_files:
            print(f"- {file_path}")

        print("\nPossible Cause:")
        print("You may be running the program from the wrong folder.")

        print("\nSuggested Fix:")
        print('cd "project 1"')
        print("python main.py")

        print("\nStartup Status: PATH ERROR")
        return False

    print("\nRequired files found ✓")

    files_to_check = [
        "main.py",
        "database/plant_references.py"
    ]

    for file_path in files_to_check:
        try:
            compile(Path(file_path).read_text(encoding="utf-8-sig"), file_path, "exec")
            print(f"Syntax OK: {file_path}")

        except (SyntaxError, OSError, UnicodeError) as error:
            print(f"\nProblem: Syntax error in {file_path}")
            print(error)
            print("\nStartup Status: CODE ERROR")
            return False

    print("\nStartup Status: READY ✓")
    print("=" * 50)

    return True
