import requests
from config.api_keys import OPENWEATHER_API_KEY


class WeatherService:
    def get_weather_context(self, lat, lon):
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        }

        response = requests.get(url, params=params)
        data = response.json()

        weather_main = data["weather"][0]["main"].lower()

        return {
            "condition": weather_main,
            "temperature": data["main"]["temp"],
            "wind_speed": data["wind"]["speed"],
            "visibility": data.get("visibility", 10000),
            "rain_mm": data.get("rain", {}).get("1h", 0)
        }

    def get_weather_multiplier(self, weather):
        if weather["condition"] in ["rain", "storm", "snow"]:
            return 1.2
        if weather["condition"] in ["fog", "mist"]:
            return 1.15
        return 1.0
