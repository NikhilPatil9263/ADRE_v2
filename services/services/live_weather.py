import requests

API_KEY = "375408694ff02834ccf5ceb8f7d10f20"

def get_weather_delay(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"
    }

    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()

    data = r.json()
    condition = data["weather"][0]["main"].lower()

    delay_map = {
        "rain": 15,
        "thunderstorm": 30,
        "fog": 20,
        "snow": 40
    }

    return delay_map.get(condition, 0), condition
