def predict_spectral_region(lambda_em):

    if lambda_em < 380:
        return "Ultraviolet (UV)"

    elif 380 <= lambda_em <= 750:
        return "Visible"

    elif lambda_em > 750:
        return "Near Infrared (NIR)"

    else:
        return "Unknown"