import asyncio
import aiohttp
from fetchers import fetch_traffic, fetch_weather, fetch_fuel_price
from publisher import EventPublisher

# Replace with real API URLs when USE_REAL_API = True
TRAFFIC_API = "https://your-real-traffic-api.com"
WEATHER_API = "https://your-real-weather-api.com"
FUEL_API = "https://your-real-fuel-api.com"

publisher = EventPublisher()

async def main_loop():
    async with aiohttp.ClientSession() as session:
        while True:
            traffic_event = await fetch_traffic(TRAFFIC_API, session)
            weather_event = await fetch_weather(WEATHER_API, session)
            fuel_event = await fetch_fuel_price(FUEL_API, session)

            publisher.publish_event(traffic_event)
            publisher.publish_event(weather_event)
            publisher.publish_event(fuel_event)

            print("Events published:", traffic_event, weather_event, fuel_event)
            await asyncio.sleep(5)  # Fetch every 5 seconds

if __name__ == "__main__":
    asyncio.run(main_loop())
