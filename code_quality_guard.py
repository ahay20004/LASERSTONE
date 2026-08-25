import py_compile


def run_code_quality_guard():

    print("\n=== CODE QUALITY GUARD ===\n")

    files_to_check = [
        "main.py",
        "display.py",
        "startup_diagnostic_engine.py",
        "database/plant_references.py",
        "database/plant_knowledge.py",
        "database/plant_identity.py"
    ]

    for file_path in files_to_check:

        try:
            py_compile.compile(
                file_path,
                doraise=True
            )

            print(f"Syntax OK: {file_path}")

        except py_compile.PyCompileError as error:

            print(f"\nSyntax Error Found: {file_path}")
            print(error)
            print("\nStatus: FIX REQUIRED")
            return False

    print("\nCode Quality Status: PASS ✓")
    return True