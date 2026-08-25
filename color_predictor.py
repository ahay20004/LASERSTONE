def predict_laser_color(lambda_em):

    if 380 <= lambda_em < 450:
        return "Violet"

    elif 450 <= lambda_em < 495:
        return "Blue"

    elif 495 <= lambda_em < 570:
        return "Green"

    elif 570 <= lambda_em < 590:
        return "Yellow"

    elif 590 <= lambda_em < 620:
        return "Orange"

    elif 620 <= lambda_em <= 750:
        return "Red"

    else:
        return "Unknown"