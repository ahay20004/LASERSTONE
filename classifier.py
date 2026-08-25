def classify_lsi(lsi_value):

    if lsi_value >= 0.8:
        return "Strong Laser Candidate"

    elif lsi_value >= 0.5:
        return "Moderate Laser Candidate"

    else:
        return "Weak Laser Candidate"