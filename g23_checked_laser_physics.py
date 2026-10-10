"""G23 opt-in safe facade; original laser physics and data validator untouched.

Requires complete plant record and applies the domain gate before calculation.
The underlying cavity result remains a special legacy assumption, NOT an
independently validated laser-cavity design.
"""
from g23_scientific_input_gate import validate_scientific_inputs
from laser_physics_engine import calculate_laser_physics


def calculate_checked_laser_physics(plant):
    check = validate_scientific_inputs(plant)
    if not check["valid"]:
        raise ValueError("Invalid scientific inputs: " + repr(check["errors"]))
    return calculate_laser_physics(plant)
