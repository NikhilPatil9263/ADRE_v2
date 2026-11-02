import asyncio
import random
from datetime import datetime
import aiohttp

USE_REAL_API = False  # True = real API, False = mock data

def convert_keys_to_str(d):
    """Convert tuple keys to strings for JSON serialization"""
    return {f"{k[0]}-{k[1]}": v for k, v in d.items()}

async def fetch_traffic(api_url=None, session=None):
    if USE_REAL_API:
        async with session.get(api_url) as response:
            data = await response.json()
            return {"type": "traffic", "timestamp": datetime.utcnow().isoformat(), "data": data}
    else:
        data = {
            ("A", "B"): round(random.uniform(1.0, 3.0), 2),
            ("B", "C"): round(random.uniform(1.0, 3.0), 2)
        }
        await asyncio.sleep(0.1)
        return {"type": "traffic", "timestamp": datetime.utcnow().isoformat(), "data": convert_keys_to_str(data)}


async def fetch_weather(api_url=None, session=None):
    if USE_REAL_API:
        async with session.get(api_url) as response:
            data = await response.json()
            return {"type": "weather", "timestamp": datetime.utcnow().isoformat(), "data": data}
    else:
        data = {
            ("A", "B"): round(random.uniform(0.8, 1.5), 2),
            ("B", "C"): round(random.uniform(0.8, 1.5), 2)
        }
        await asyncio.sleep(0.1)
        return {"type": "weather", "timestamp": datetime.utcnow().isoformat(), "data": convert_keys_to_str(data)}


async def fetch_fuel_price(api_url=None, session=None):
    if USE_REAL_API:
        async with session.get(api_url) as response:
            data = await response.json()
            return {"type": "fuel", "timestamp": datetime.utcnow().isoformat(), "data": data}
    else:
        data = {
            "diesel_price": round(random.uniform(100, 120), 2)  # price per liter
        }
        await asyncio.sleep(0.1)
        return {"type": "fuel", "timestamp": datetime.utcnow().isoformat(), "data": data}
