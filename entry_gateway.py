import os
import sys
import tkinter as tk
from tkinter import messagebox


ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
CORE_DIR = os.path.join(ROOT_DIR, "core")
DATABASE_DIR = os.path.join(ROOT_DIR, "database")


for path in [ROOT_DIR, CORE_DIR, DATABASE_DIR]:
    if path not in sys.path:
        sys.path.insert(0, path)


def check_system_status():
    issues = []

    required_files = {
        "dashboard.py": os.path.join(ROOT_DIR, "dashboard.py"),
        "plants_data.py": os.path.join(ROOT_DIR, "plants_data.py"),
        "code_repair_advisor.py": os.path.join(ROOT_DIR, "code_repair_advisor.py"),
        "startup_diagnostic_engine.py": os.path.join(
            ROOT_DIR,
            "startup_diagnostic_engine.py"
        ),
        "system_integrity_engine.py": os.path.join(
            ROOT_DIR,
            "system_integrity_engine.py"
        ),
    }

    for file_name, file_path in required_files.items():
        if not os.path.exists(file_path):
            issues.append(f"Missing file: {file_name}")

    try:
        from plants_data import plants
        plants_count = len(plants)

    except Exception as error:
        plants_count = 0
        issues.append(f"Plants data error: {error}")

    try:
        from dashboard import launch_dashboard
        dashboard_ready = True

    except Exception as error:
        dashboard_ready = False
        issues.append(f"Dashboard import error: {error}")

    status = "READY" if not issues else "WARNING"

    return {
        "status": status,
        "issues": issues,
        "plants_count": plants_count,
        "dashboard_ready": dashboard_ready,
    }


def open_entry_gateway(on_approve, on_city=None):
    result = check_system_status()

    root = tk.Tk()
    root.title("LASERSTONE ENTRY GATEWAY")
    root.geometry("680x540")

    title = tk.Label(
        root,
        text="LASERSTONE™ ENTRY GATEWAY",
        font=("Arial", 16, "bold")
    )
    title.pack(pady=10)

    status_color = "lightgreen"

    if result["status"] != "READY":
        status_color = "khaki"

    status_label = tk.Label(
        root,
        text=f"SYSTEM STATUS: {result['status']}",
        font=("Arial", 13, "bold"),
        bg=status_color,
        width=42,
        height=2,
        relief="groove"
    )
    status_label.pack(pady=8)

    info_text = (
        f"Plants Loaded: {result['plants_count']}\n"
        f"Dashboard Ready: {result['dashboard_ready']}\n"
        f"Issues Found: {len(result['issues'])}"
    )

    info_label = tk.Label(
        root,
        text=info_text,
        font=("Arial", 11),
        justify="left"
    )
    info_label.pack(pady=8)

    text_box = tk.Text(
        root,
        height=14,
        wrap="word"
    )
    text_box.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=10
    )

    if result["issues"]:
        text_box.insert(
            "1.0",
            "ISSUES DETECTED:\n\n"
        )

        for issue in result["issues"]:
            text_box.insert(
                "end",
                f"- {issue}\n"
            )

        text_box.insert(
            "end",
            "\nDECISION OPTIONS:\n"
            "1) APPROVE & OPEN DASHBOARD:\n"
            "   Continue opening the dashboard despite warnings.\n\n"
            "2) STOP / REVIEW:\n"
            "   Stop here and review the listed issues manually.\n\n"
            "Safety Rule:\n"
            "No automatic repair is applied from this gateway."
        )

    else:
        text_box.insert(
            "1.0",
            "SYSTEM CHECK PASSED SUCCESSFULLY.\n\n"
            "The LASERSTONE dashboard is ready to open.\n\n"
            "Decision:\n"
            "Press APPROVE & OPEN DASHBOARD to continue."
        )

    text_box.config(state="disabled")

    def approve():
        root.destroy()
        on_approve()

    def open_city():
        root.withdraw()

        if on_city is not None:
            on_city()

    def stop():
        messagebox.showinfo(
            "LASERSTONE ENTRY GATEWAY",
            "Entry cancelled. No files were changed."
       )
        root.destroy()

    button_frame = tk.Frame(root)
    button_frame.pack(pady=12)

    approve_button = tk.Button(
        button_frame,
        text="APPROVE & OPEN DASHBOARD",
        font=("Arial", 11, "bold"),
        width=28,
        command=approve
    )
    approve_button.pack(
        side=tk.LEFT,
        padx=8
    )

    stop_button = tk.Button(
        button_frame,
        text="STOP / REVIEW",
        font=("Arial", 11, "bold"),
        width=18,
        command=stop
    )

    

    stop_button.pack(
        side=tk.LEFT,
        padx=8
    )

    city_button = tk.Button(
        button_frame,
        text="OPEN SCIENTIFIC CITY",
        font=("Arial", 11, "bold"),
        width=28,
        command=open_city)

    city_button.pack(
        side=tk.LEFT,
        padx=8 )

    root.mainloop()