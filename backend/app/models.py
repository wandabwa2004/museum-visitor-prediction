from pydantic import BaseModel, Field
from typing import Optional
from datetime import date as Date


class PredictionRequest(BaseModel):
    date: Date = Field(..., description="Date to predict visitors for")
    temperature: Optional[float] = Field(None, description="Expected temperature in Celsius")
    precipitation: Optional[float] = Field(0.0, description="Expected precipitation in mm")
    weather_type: Optional[str] = Field("Partly Cloudy",
                                        description="Sunny | Partly Cloudy | Cloudy | Rainy")
    is_public_holiday: Optional[int] = Field(None,
                                             description="1 if public holiday; auto-detected if omitted")
    is_school_holiday: Optional[int] = Field(None,
                                             description="1 if school holiday; auto-detected if omitted")
    special_exhibition: Optional[int] = Field(0, description="1 if special exhibition active")
    local_event: Optional[int] = Field(0, description="1 if local event active")
    marketing_campaign: Optional[int] = Field(0, description="1 if marketing campaign active")
    ticket_promotion: Optional[int] = Field(0, description="1 if ticket promotion active")
    ticket_price: Optional[float] = Field(25.0, description="Ticket price in AUD")


class PredictionResponse(BaseModel):
    date: Date
    predicted_visitors: int
    lower_80: int
    upper_80: int
    lower_95: int
    upper_95: int
    traffic_tier: str          # Low | Medium | High
    confidence: float          # 0-1
    model_used: str


class HistoricalRecord(BaseModel):
    date: Date
    visitors: int
    day_name: str
    month: int
    is_public_holiday: int
    is_school_holiday: int
    special_exhibition: int
    local_event: int
    weather_type: str
    temperature: float


class HistoricalResponse(BaseModel):
    records: list[HistoricalRecord]
    total_records: int
    date_from: Date
    date_to: Date


class ModelMetrics(BaseModel):
    mae: float
    rmse: float
    r2: float
    mape: float
    bias: float


class InsightsResponse(BaseModel):
    best_model: str
    metrics: ModelMetrics
    feature_count: int
    training_records: int
    top_features: list[dict]
    all_model_results: dict
