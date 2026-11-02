import random

def get_traffic_delay(distance_km):
    """
    Simple real-world inspired congestion model
    """
    if distance_km < 50:
        return random.uniform(5, 15)
    elif distance_km < 300:
        return random.uniform(20, 60)
    else:
        return random.uniform(60, 180)
