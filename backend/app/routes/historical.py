from fastapi import APIRouter, Query, HTTPException
from datetime import date
from app.models import HistoricalResponse, HistoricalRecord
from app.services.model_service import ModelService

router = APIRouter()


@router.get("/historical", response_model=HistoricalResponse)
def get_historical(
    date_from: date = Query(None, description="Start date (YYYY-MM-DD)"),
    date_to:   date = Query(None, description="End date   (YYYY-MM-DD)"),
    limit:     int  = Query(365,  ge=1, le=1096, description="Max records to return"),
):
    """
    Return historical visitor records, optionally filtered by date range.
    """
    if not ModelService.is_loaded():
        raise HTTPException(status_code=503, detail="Model not loaded")

    df = ModelService.get_historical(date_from=date_from, date_to=date_to, limit=limit)

    if df.empty:
        raise HTTPException(status_code=404, detail="No historical data found for given range")

    keep_cols = [
        "date", "visitors", "day_name", "month",
        "is_public_holiday", "is_school_holiday",
        "special_exhibition", "local_event",
        "weather_type", "temperature",
    ]
    df = df[[c for c in keep_cols if c in df.columns]].copy()
    df["date"] = df["date"].dt.date

    records = [HistoricalRecord(**row) for row in df.to_dict(orient="records")]

    return HistoricalResponse(
        records=records,
        total_records=len(records),
        date_from=records[0].date,
        date_to=records[-1].date,
    )
