def predict_eta(distance_km, weather_factor=1.0):
    """
    Predict ETA in minutes.
    Assumes base speed = 60 km/h (1 km = 1 min),
    adjusted by weather factor.
    """
    base_eta = distance_km  # 1 km = 1 minute
    return base_eta * weather_factor
