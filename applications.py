def predict_application(lsi_value):

    if lsi_value >= 5:

        return [
            "Biomedical Imaging",
            "Dye Laser Systems",
            "Optical Sensors",
            "Medical Diagnostics"
        ]

    elif lsi_value >= 2:

        return [
            "Optical Filtering",
            "Low Power Laser Systems",
            "Bio-sensing"
        ]

    else:

        return [
            "Pigment Applications",
            "Optical Study Only"
        ]