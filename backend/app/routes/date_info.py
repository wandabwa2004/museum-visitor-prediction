from fastapi import APIRouter
from datetime import date as Date
import pandas as pd

from app.services.calendar_service import get_holiday_info
from app.services.weather_service import get_weather

router = APIRouter()


def _season(month: int) -> str:
    if month in [12, 1, 2]:  return "Summer"
    if month in [3, 4, 5]:   return "Autumn"
    if month in [6, 7, 8]:   return "Winter"
    return "Spring"


@router.get("/date-info")
def date_info(date: Date):
    """
    Return automatic context for a given date:
    - Victorian public holiday detection (national + VIC-specific)
    - Victorian school holiday detection
    - Day name, season, weekend flag
    - Weather from Open-Meteo (historical archive or forecast; None if unavailable)
    """
    ts = pd.Timestamp(date)

    cal     = get_holiday_info(date)
    weather = get_weather(date)

    return {
        "date":       str(date),
        "day_name":   ts.day_name(),
        "is_weekend": int(ts.dayofweek >= 5),
        "season":     _season(date.month),
        **cal,
        "weather":    weather,  # None when beyond forecast horizon or fetch fails
    }
