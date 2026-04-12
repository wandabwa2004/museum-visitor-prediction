import os
from supabase import create_client, Client

_client: Client | None = None


def get_client() -> Client:
    global _client
    if _client is None:
        url = os.environ.get("SUPABASE_URL", "")
        key = os.environ.get("SUPABASE_KEY", "")
        if not url or not key:
            raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in environment")
        _client = create_client(url, key)
    return _client


def log_prediction(payload: dict) -> dict:
    """Insert a prediction into predictions_log and return the created row."""
    client = get_client()
    res = client.table("predictions_log").insert(payload).execute()
    return res.data[0] if res.data else {}


def fetch_historical(date_from: str | None = None,
                     date_to:   str | None = None,
                     limit: int = 365) -> list[dict]:
    """Fetch historical visitor records from Supabase."""
    client = get_client()
    query = (
        client.table("visitor_data")
        .select("date,visitors,day_name,month,is_public_holiday,"
                "is_school_holiday,special_exhibition,local_event,"
                "weather_type,temperature")
        .order("date", desc=False)
        .limit(limit)
    )
    if date_from:
        query = query.gte("date", date_from)
    if date_to:
        query = query.lte("date", date_to)
    res = query.execute()
    return res.data or []


def update_actual_visitors(predicted_for_date: str, actual_visitors: int) -> None:
    """Back-fill actual visitor count once known (for accuracy tracking)."""
    client = get_client()
    client.table("predictions_log").update(
        {"actual_visitors": actual_visitors}
    ).eq("predicted_for_date", predicted_for_date).execute()
