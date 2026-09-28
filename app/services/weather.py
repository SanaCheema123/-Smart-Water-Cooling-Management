import httpx
from app.config import settings

async def current_weather():
    if not settings.weather_api_key:
        return {"source": "not_configured", "temperature_c": None, "humidity_pct": None}
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"lat": settings.weather_lat, "lon": settings.weather_lon,
              "appid": settings.weather_api_key, "units": "metric"}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        d = r.json()
    return {"source": "openweathermap",
            "temperature_c": d["main"]["temp"],
            "humidity_pct": d["main"]["humidity"]}
