import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox


# ============================================================
# LASERSTONE INTERNATIONAL SCIENTIFIC UNIVERSITY
# UNIVERSITY GATEWAY V1
# ============================================================

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

LASERSTONE_LAUNCHER = os.path.join(
    ROOT_DIR,
    "safe_dashboard_launcher.py"
)


def open_laserstone_core():
    """
    Open the current stable LASERSTONE scientific platform.
    The existing LASERSTONE Core is not modified.
    """

    if not os.path.exists(LASERSTONE_LAUNCHER):

        messagebox.showerror(
            "LASERSTONE UNIVERSITY GATEWAY",
            "LASERSTONE Core launcher was not found.\n\n"
            "Expected file:\n"
            "safe_dashboard_launcher.py"
        )

        return

    answer = messagebox.askyesno(
        "LASERSTONE CORE",
        "LASERSTONE Scientific Core is ready.\n\n"
        "Open the current Grand Hall and Scientific Wings?"
    )

    if not answer:
        return

    try:

        subprocess.Popen(
            [
                sys.executable,
                LASERSTONE_LAUNCHER
            ],
            cwd=ROOT_DIR
        )

    except Exception as error:

        messagebox.showerror(
            "LASERSTONE CORE LAUNCH ERROR",
            str(error)
        )


def open_academic_city():
    """
    Academic City foundation window.
    Future colleges, centers, library and research facilities
    will be connected here.
    """

    city_window = tk.Toplevel(root)

    city_window.title(
        "LASERSTONE INTERNATIONAL SCIENTIFIC UNIVERSITY"
    )

    city_window.geometry(
        "850x600"
    )

    title = tk.Label(
        city_window,
        text="LASERSTONE™ INTERNATIONAL SCIENTIFIC UNIVERSITY",
        font=("Arial", 18, "bold")
    )

    title.pack(
        pady=20
    )

    subtitle = tk.Label(
        city_window,
        text="ACADEMIC CITY",
        font=("Arial", 16, "bold")
    )

    subtitle.pack(
        pady=10
    )

    status = tk.Label(
        city_window,
        text=(
            "UNIVERSITY FOUNDATION LAYER\n\n"
            "Academic City Status : FOUNDATION READY\n"
            "LASERSTONE Core      : AVAILABLE\n"
            "Grand Hall           : OPERATIONAL\n"
            "Scientific Wings     : OPERATIONAL\n\n"
            "Future Academic Structure\n\n"
            "• Colleges\n"
            "• Scientific Research Centers\n"
            "• International Scientific Library\n"
            "• Innovation and Discovery Centers\n"
            "• Graduate Research Programs\n"
            "• Scientific Training and Education\n"
            "• Technology and Prototype Development"
        ),
        font=("Arial", 12),
        justify="left",
        relief="groove",
        padx=30,
        pady=25
    )

    status.pack(
        fill="both",
        expand=True,
        padx=40,
        pady=20
    )

    close_button = tk.Button(
        city_window,
        text="RETURN TO UNIVERSITY GATEWAY",
        font=("Arial", 11, "bold"),
        width=32,
        command=city_window.destroy
    )

    close_button.pack(
        pady=20
    )


def show_university_status():

    messagebox.showinfo(
        "UNIVERSITY SYSTEM STATUS",
        (
            "LASERSTONE™ INTERNATIONAL SCIENTIFIC UNIVERSITY\n\n"
            "University Gateway : ACTIVE\n"
            "LASERSTONE Core    : READY\n"
            "Grand Hall         : OPERATIONAL\n"
            "Scientific Wings   : OPERATIONAL\n"
            "Academic City      : FOUNDATION STAGE\n\n"
            "Overall Status     : READY FOR EXPANSION"
        )
    )


# ============================================================
# MAIN UNIVERSITY GATEWAY
# ============================================================

root = tk.Tk()

root.title(
    "LASERSTONE UNIVERSITY GATEWAY"
)

root.geometry(
    "1000x650"
)


main_title = tk.Label(
    root,
    text="LASERSTONE™ INTERNATIONAL SCIENTIFIC UNIVERSITY",
    font=("Arial", 22, "bold")
)

main_title.pack(
    pady=(30, 8)
)


motto = tk.Label(
    root,
    text="Where Knowledge Becomes Discovery",
    font=("Arial", 13, "italic")
)

motto.pack(
    pady=(0, 25)
)


gateway_title = tk.Label(
    root,
    text="UNIVERSITY GATEWAY",
    font=("Arial", 17, "bold"),
    relief="groove",
    width=45,
    height=2
)

gateway_title.pack(
    pady=10
)


status_label = tk.Label(
    root,
    text=(
        "UNIVERSITY SYSTEM STATUS : READY\n"
        "LASERSTONE SCIENTIFIC CORE : OPERATIONAL"
    ),
    font=("Arial", 11, "bold")
)

status_label.pack(
    pady=15
)


navigation_frame = tk.Frame(
    root
)

navigation_frame.pack(
    pady=30
)


core_button = tk.Button(
    navigation_frame,
    text=(
        "LASERSTONE CORE\n\n"
        "Grand Hall • Scientific Wings\n"
        "Analysis • Intelligence • Discovery"
    ),
    font=("Arial", 12, "bold"),
    width=36,
    height=6,
    command=open_laserstone_core
)

core_button.grid(
    row=0,
    column=0,
    padx=25,
    pady=10
)


academic_button = tk.Button(
    navigation_frame,
    text=(
        "ACADEMIC CITY\n\n"
        "Colleges • Centers • Library\n"
        "Research • Education • Innovation"
    ),
    font=("Arial", 12, "bold"),
    width=36,
    height=6,
    command=open_academic_city
)

academic_button.grid(
    row=0,
    column=1,
    padx=25,
    pady=10
)


status_button = tk.Button(
    root,
    text="UNIVERSITY SYSTEM STATUS",
    font=("Arial", 11, "bold"),
    width=30,
    command=show_university_status
)

status_button.pack(
    pady=15
)


exit_button = tk.Button(
    root,
    text="EXIT UNIVERSITY GATEWAY",
    font=("Arial", 10, "bold"),
    width=28,
    command=root.destroy
)

exit_button.pack(
    pady=10
)


footer = tk.Label(
    root,
    text=(
        "LASERSTONE Scientific Core remains protected and independent.\n"
        "University Gateway V1"
    ),
    font=("Arial", 9)
)

footer.pack(
    side="bottom",
    pady=20
)


root.mainloop()