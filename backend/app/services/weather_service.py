from datetime import date, timedelta
from typing import Optional
import httpx

MELBOURNE_LAT = -37.8136
MELBOURNE_LON = 144.9631

# WMO weather interpretation codes → our four weather types
# https://open-meteo.com/en/docs#weathervariables
WMO_TO_TYPE: dict[int, str] = {
    0:  "Sunny",         # Clear sky
    1:  "Sunny",         # Mainly clear
    2:  "Partly Cloudy", # Partly cloudy
    3:  "Cloudy",        # Overcast
    45: "Cloudy",        # Fog
    48: "Cloudy",        # Depositing rime fog
    51: "Rainy",         # Light drizzle
    53: "Rainy",         # Moderate drizzle
    55: "Rainy",         # Dense drizzle
    56: "Rainy",         # Light freezing drizzle
    57: "Rainy",         # Heavy freezing drizzle
    61: "Rainy",         # Slight rain
    63: "Rainy",         # Moderate rain
    65: "Rainy",         # Heavy rain
    66: "Rainy",         # Light freezing rain
    67: "Rainy",         # Heavy freezing rain
    71: "Cloudy",        # Slight snowfall
    73: "Cloudy",        # Moderate snowfall
    75: "Cloudy",        # Heavy snowfall
    77: "Cloudy",        # Snow grains
    80: "Rainy",         # Slight rain showers
    81: "Rainy",         # Moderate rain showers
    82: "Rainy",         # Violent rain showers
    85: "Cloudy",        # Slight snow showers
    86: "Cloudy",        # Heavy snow showers
    95: "Rainy",         # Thunderstorm
    96: "Rainy",         # Thunderstorm with slight hail
    99: "Rainy",         # Thunderstorm with heavy hail
}


def get_weather(target_date: date) -> Optional[dict]:
    """
    Fetch Melbourne weather for a specific date from Open-Meteo (no API key required).

    Strategy:
      - More than 7 days in the past → archive API (actual observations)
      - Within 7 days past to 16 days future → forecast API
      - More than 16 days in the future → return None (use seasonal defaults)

    Returns dict with temperature, precipitation, weather_type, source
    or None on failure / out-of-range date.
    """
    today = date.today()
    delta = (target_date - today).days

    if delta > 16:
        return None  # too far ahead; caller falls back to seasonal defaults

    params = {
        "latitude":   MELBOURNE_LAT,
        "longitude":  MELBOURNE_LON,
        "daily":      "temperature_2m_mean,precipitation_sum,weathercode",
        "timezone":   "Australia/Melbourne",
        "start_date": str(target_date),
        "end_date":   str(target_date),
    }

    if delta < -7:
        url = "https://archive-api.open-meteo.com/v1/archive"
        source = "archive"
    else:
        url = "https://api.open-meteo.com/v1/forecast"
        source = "forecast"

    try:
        with httpx.Client(timeout=5.0) as client:
            resp = client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()

        daily  = data.get("daily", {})
        temps  = daily.get("temperature_2m_mean",  [None])
        precips = daily.get("precipitation_sum",   [0.0])
        codes  = daily.get("weathercode",          [2])

        temp   = temps[0]  if temps   else None
        precip = precips[0] if precips else 0.0
        code   = int(codes[0]) if codes else 2

        if temp is None:
            return None

        return {
            "temperature":  round(float(temp), 1),
            "precipitation": round(float(precip or 0.0), 1),
            "weather_type": WMO_TO_TYPE.get(code, "Partly Cloudy"),
            "source":       source,   # "archive" | "forecast"
        }
    except Exception:
        return None
