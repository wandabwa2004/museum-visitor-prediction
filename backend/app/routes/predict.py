from fastapi import APIRouter, HTTPException
from app.models import PredictionRequest, PredictionResponse
from app.services.model_service import ModelService

router = APIRouter()


@router.post("/predict", response_model=PredictionResponse)
def predict(req: PredictionRequest):
    """
    Predict visitor numbers for a given date and context.
    Returns point prediction, 80%/95% intervals, traffic tier, and confidence.
    """
    if not ModelService.is_loaded():
        raise HTTPException(status_code=503, detail="Model not loaded")

    historical_df = ModelService.get_historical()
    if historical_df.empty:
        raise HTTPException(status_code=503, detail="Historical data not available")

    try:
        feature_row = ModelService.build_feature_row(req, historical_df)
        result = ModelService.predict(feature_row)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    # Log prediction to Supabase (non-blocking — skip if not configured)
    try:
        import os
        if os.environ.get("SUPABASE_URL"):
            from app.services.supabase_client import log_prediction
            log_prediction({
                "predicted_for_date": str(req.date),
                "predicted_visitors":  result["predicted_visitors"],
                "lower_80":            result["lower_80"],
                "upper_80":            result["upper_80"],
                "lower_95":            result["lower_95"],
                "upper_95":            result["upper_95"],
                "traffic_tier":        result["traffic_tier"],
                "confidence":          result["confidence"],
                "model_used":          result["model_used"],
                "temperature":         req.temperature,
                "precipitation":       req.precipitation,
                "weather_type":        req.weather_type,
                "special_exhibition":  req.special_exhibition,
                "local_event":         req.local_event,
                "marketing_campaign":  req.marketing_campaign,
                "ticket_promotion":    req.ticket_promotion,
                "ticket_price":        req.ticket_price,
            })
    except Exception:
        pass  # Never fail a prediction because of logging

    return PredictionResponse(date=req.date, **result)
