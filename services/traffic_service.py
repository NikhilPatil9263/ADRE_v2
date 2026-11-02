import requests
from config.api_keys import TOMTOM_API_KEY

class TrafficService:
    def get_traffic_multiplier(self, lat, lon):
        """
        Returns traffic multiplier based on congestion
        """
        url = (
            "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
        )

        params = {
            "key": TOMTOM_API_KEY,
            "point": f"{lat},{lon}"
        }

        response = requests.get(url, params=params)
        data = response.json()

        if "flowSegmentData" not in data:
            return 1.0  # fallback

        free_flow = data["flowSegmentData"]["freeFlowSpeed"]
        current_speed = data["flowSegmentData"]["currentSpeed"]

        if current_speed <= 0:
            return 1.5

        congestion_ratio = free_flow / current_speed
        return round(min(congestion_ratio, 2.0), 2)
