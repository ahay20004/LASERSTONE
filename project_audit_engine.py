import os


KEYWORDS = [
    "score",
    "class",
    "quality",
    'return "High"',
    'return "Medium"',
    'return "Low"',
    'return "Excellent"',
    'return "Moderate"',
    'return "Poor"',
]


def audit_project_files(root_dir="."):

    print("\n=== LASERSTONE PROJECT AUDIT ===\n")

    for folder, _, files in os.walk(root_dir):

        if "__pycache__" in folder:
            continue

        for file in files:

            if not file.endswith(".py"):
                continue

            file_path = os.path.join(folder, file)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                for line_number, line in enumerate(lines, start=1):

                    for keyword in KEYWORDS:

                        if keyword in line:

                            print(
                                f"{file_path} | Line {line_number} | {line.strip()}"
                            )

            except Exception as e:
                print(f"Could not read {file_path}: {e}")


if __name__ == "__main__":
    audit_project_files()