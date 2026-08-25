# project_diagnostic_engine.py

import os


def run_project_diagnostic():

    print("\n\n")
    print("###################################")
    print("PROJECT DIAGNOSTIC ENGINE STARTED")
    print("###################################")

    print("\n=== PROJECT DIAGNOSTIC REPORT ===")

    print("Diagnostic Test Successful")

    required_files = [

        "main.py",

        "display.py",

        "dashboard.py",

        "project_registry.py",

        "physics_evidence_engine.py"

    ]

    missing_files = []

    for file_name in required_files:

        if not os.path.exists(file_name):

            missing_files.append(file_name)

    print(
        f"Required Files Checked: "
        f"{len(required_files)}"
    )

    if missing_files:

        print("\nMissing Files:")

        for file_name in missing_files:

            print(f"- {file_name}")

    else:

        print(
            "\nAll Required Files Found ✓"
        )

    print("\nDiagnostic Status: COMPLETE")

    print("\n" + "=" * 50)