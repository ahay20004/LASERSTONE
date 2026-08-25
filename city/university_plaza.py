# LASERSTONE International Scientific University
# University Plaza Interface v2.0

import tkinter as tk

from city.city_theme import (
    UNIVERSITY_NAME,
    UNIVERSITY_MOTTO,
    DEFAULT_LANGUAGE,
    BUILDING_COLORS,
)

from city.city_map import (
    get_all_buildings,
    get_laser_fruit_summary,
)


BACKGROUND_COLOR = "#F7F5EF"
TEXT_COLOR = "#1E1E1E"
TREE_COLOR = "#2E7D5B"


def open_university_plaza(
    parent,
    ranked_plants,
    callbacks,
    language=DEFAULT_LANGUAGE
):
    plaza = tk.Toplevel(parent)
    plaza.title("LASERSTONE International Scientific University - Grand Plaza")
    plaza.geometry("1120x780")
    plaza.configure(bg=BACKGROUND_COLOR)

    university_name = UNIVERSITY_NAME.get(language, UNIVERSITY_NAME["en"])
    motto = UNIVERSITY_MOTTO.get(language, UNIVERSITY_MOTTO["en"])

    header = tk.Label(
        plaza,
        text=f"{university_name}\n{motto}",
        font=("Segoe UI", 20, "bold"),
        bg=BACKGROUND_COLOR,
        fg=TEXT_COLOR,
        justify="center"
    )
    header.pack(pady=(18, 8))

    tree_label = tk.Label(
        plaza,
        text="🌳\nTREE OF KNOWLEDGE\nGrowing Through Discovery",
        font=("Segoe UI", 16, "bold"),
        bg=BACKGROUND_COLOR,
        fg=TREE_COLOR,
        justify="center"
    )
    tree_label.pack(pady=12)

    guide = tk.Label(
        plaza,
        text="Welcome Researcher — choose your scientific destination",
        font=("Segoe UI", 13, "bold"),
        bg=BACKGROUND_COLOR,
        fg=TEXT_COLOR
    )
    guide.pack(pady=6)

    path_frame = tk.LabelFrame(
        plaza,
        text="Laser Fruit Path",
        font=("Segoe UI", 12, "bold"),
        bg=BACKGROUND_COLOR,
        fg=TEXT_COLOR
    )
    path_frame.pack(fill="x", padx=28, pady=12)

    laser_path = "  →  ".join(get_laser_fruit_summary())

    tk.Label(
        path_frame,
        text=laser_path,
        font=("Segoe UI", 11, "bold"),
        bg=BACKGROUND_COLOR,
        fg=TEXT_COLOR,
        wraplength=1000,
        justify="center"
    ).pack(padx=10, pady=10)

    buildings_frame = tk.LabelFrame(
        plaza,
        text="University Buildings",
        font=("Segoe UI", 12, "bold"),
        bg=BACKGROUND_COLOR,
        fg=TEXT_COLOR
    )
    buildings_frame.pack(fill="both", expand=True, padx=28, pady=14)

    buildings = get_all_buildings()

    ordered_buildings = [
        "college_of_materials",
        "college_of_physics",
        "college_of_engineering",
        "college_of_intelligence",
        "house_of_scientific_expertise",
        "grand_scientific_library",
        "research_laboratories",
    ]

    for index, building_id in enumerate(ordered_buildings):
        building = buildings.get(building_id, {})

        name = building.get("name", building_id)
        role = building.get("role", "")
        symbol = building.get("symbol", "🏛️")
        command = callbacks.get(building_id)

        bg_color = BUILDING_COLORS.get(building_id, "#FFFFFF")

        card = tk.Button(
            buildings_frame,
            text=f"{symbol}\n{name}\n\n{role}\n\nENTER",
            font=("Segoe UI", 10, "bold"),
            width=28,
            height=8,
            bg=bg_color,
            fg=TEXT_COLOR,
            relief="raised",
            command=command
        )

        card.grid(
            row=index // 3,
            column=index % 3,
            padx=16,
            pady=14
        )

    footer = tk.Label(
        plaza,
        text="Every discovery begins with a question.",
        font=("Segoe UI", 10, "italic"),
        bg=BACKGROUND_COLOR,
        fg="#555555"
    )
    footer.pack(pady=10)