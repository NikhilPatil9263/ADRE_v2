def compute_risk(route_data):
    """
    Compute risk score (0 to 1) for a route based on ETA, traffic, weather, etc.
    route_data: dict with keys like 'eta_min', 'traffic_factor', 'weather_factor'
    Returns: float risk score
    """
    # Example simple calculation (can be extended later)
    base_risk = 0.1
    traffic_risk = 0.5 * route_data.get('traffic_factor', 1)
    weather_risk = 0.4 * route_data.get('weather_factor', 1)
    return min(base_risk + traffic_risk + weather_risk, 1.0)
