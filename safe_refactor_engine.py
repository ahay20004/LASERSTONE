import os
import shutil


REPLACEMENTS = {
    '"High"': '"Excellent"',
    '"Medium"': '"Moderate"',
    '"Low"': '"Low"',
}


TARGET_EXTENSIONS = [".py"]


def create_backup(file_path):
    backup_path = file_path + ".bak"

    if not os.path.exists(backup_path):
        shutil.copy2(file_path, backup_path)

    return backup_path


def preview_changes(root_dir="."):
    print("\n=== PREVIEW CHANGES ===\n")

    for folder, _, files in os.walk(root_dir):

        if "__pycache__" in folder:
            continue

        for file in files:

            if not any(file.endswith(ext) for ext in TARGET_EXTENSIONS):
                continue

            file_path = os.path.join(folder, file)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                for old, new in REPLACEMENTS.items():

                    if old in content:
                        print(f"{file_path}")
                        print(f"  {old}  -->  {new}")

            except Exception as e:
                print(f"Could not read {file_path}: {e}")


def apply_changes(root_dir="."):
    print("\n=== APPLYING SAFE REFACTOR ===\n")

    for folder, _, files in os.walk(root_dir):

        if "__pycache__" in folder:
            continue

        for file in files:

            if not any(file.endswith(ext) for ext in TARGET_EXTENSIONS):
                continue

            file_path = os.path.join(folder, file)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                new_content = content

                for old, new in REPLACEMENTS.items():
                    new_content = new_content.replace(old, new)

                if new_content != content:
                    backup_path = create_backup(file_path)

                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)

                    print(f"Updated: {file_path}")
                    print(f"Backup : {backup_path}")

            except Exception as e:
                print(f"Could not update {file_path}: {e}")


if __name__ == "__main__":

    preview_changes()

    confirm = input("\nApply these changes? yes/no: ")

    if confirm.lower() == "yes":
        apply_changes()
        print("\nRefactor completed.")
    else:
        print("\nNo changes applied.")