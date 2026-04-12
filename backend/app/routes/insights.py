from fastapi import APIRouter, HTTPException
from app.models import InsightsResponse, ModelMetrics
from app.services.model_service import ModelService

router = APIRouter()


@router.get("/insights", response_model=InsightsResponse)
def get_insights():
    """
    Return model performance metrics, top feature importances, and comparison across all models.
    """
    if not ModelService.is_loaded():
        raise HTTPException(status_code=503, detail="Model not loaded")

    best = ModelService._best_model_name
    results = ModelService._model_results

    best_metrics = results.get(best, {})
    metrics = ModelMetrics(
        mae=round(best_metrics.get("MAE", 0), 2),
        rmse=round(best_metrics.get("RMSE", 0), 2),
        r2=round(best_metrics.get("R2", 0), 4),
        mape=round(best_metrics.get("MAPE", 0), 2),
        bias=0.0,
    )

    historical_df = ModelService.get_historical()
    training_records = max(0, len(historical_df) - 90)

    return InsightsResponse(
        best_model=best,
        metrics=metrics,
        feature_count=len(ModelService._features),
        training_records=training_records,
        top_features=ModelService.get_feature_importances(top_n=10),
        all_model_results=results,
    )
