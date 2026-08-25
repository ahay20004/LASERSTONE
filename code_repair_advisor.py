def explain_runtime_error(error_text):

    print("\n=== CODE REPAIR ADVISOR ===\n")

    error_text = str(error_text)

    if "tuple" in error_text and "has no attribute 'get'" in error_text:

        print("Detected Error:")
        print(error_text)

        print("\nExplanation:")
        print(
            "A tuple object was found where a dictionary "
            "was expected."
        )

        print("\nMost Likely Cause:")
        print(
            "An extra comma may have been added after "
            "a dictionary assignment."
        )

        print("\nExample:")

        print(
            'plant["reference_info"] = '
            'PLANT_REFERENCES.get(plant_key, {} ),'
        )

        print("\nSuggested Fix:")

        print(
            'plant["reference_info"] = '
            'PLANT_REFERENCES.get(plant_key, {})'
        )

        return

    if "IndentationError" in error_text:

        print("Detected Error:")
        print(error_text)

        print("\nExplanation:")
        print(
            "Python found inconsistent indentation."
        )

        print("\nSuggested Fix:")
        print(
            "Verify that all lines inside the same "
            "block use identical indentation."
        )

        return

    if "SyntaxError" in error_text:

        print("Detected Error:")
        print(error_text)

        print("\nExplanation:")
        print(
            "Python detected invalid syntax."
        )

        print("\nSuggested Fix:")
        print(
            "Check brackets, commas, and string "
            "termination near the reported line."
        )

        return

    print("Detected Error:")
    print(error_text)

    print("\nNo repair rule available yet.")

    print(
        "Add a new advisor rule for this error type."
    )