import requests

OSRM_URL = "http://router.project-osrm.org/route/v1/driving"

def get_route_distance(origin_coords, dest_coords):
    """
    origin_coords = (lat, lon)
    dest_coords   = (lat, lon)
    """
    url = f"{OSRM_URL}/{origin_coords[1]},{origin_coords[0]};{dest_coords[1]},{dest_coords[0]}"
    params = {
        "overview": "false",
        "annotations": "distance,duration"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    route = data["routes"][0]

    distance_km = route["distance"] / 1000
    duration_min = route["duration"] / 60

    return distance_km, duration_min
