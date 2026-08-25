import tkinter as tk

from city.university_plaza import open_university_plaza


def not_ready():
    print("Building under construction...")


callbacks = {
    "college_of_materials": not_ready,
    "college_of_physics": not_ready,
    "college_of_engineering": not_ready,
    "college_of_intelligence": not_ready,
    "house_of_scientific_expertise": not_ready,
    "grand_scientific_library": not_ready,
    "research_laboratories": not_ready,
}

root = tk.Tk()
root.withdraw()

open_university_plaza(
    root,
    [],
    callbacks
)

root.mainloop()