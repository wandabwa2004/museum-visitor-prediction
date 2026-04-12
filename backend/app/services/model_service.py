import json
import pickle
import numpy as np
import pandas as pd
import joblib
import xgboost as xgb
from pathlib import Path

BASE_DIR   = Path(__file__).resolve().parents[3]
MODELS_DIR = BASE_DIR / "ml-pipeline" / "models"
DATA_DIR   = BASE_DIR / "data"


class ModelService:
    _model = None
    _features: list[str] = []
    _best_model_name: str = ""
    _historical_df: pd.DataFrame = None
    _model_results: dict = {}
    _residual_std: float = 0.0
    _xgb_log_offset: float = 0.0   # XGBoost 2.x no longer adds base_score in predict()

    @classmethod
    def load(cls):
        with open(MODELS_DIR / "features.json") as f:
            meta = json.load(f)
        cls._features = meta["features"]
        cls._best_model_name = meta["best_model"]

        if cls._best_model_name == "XGBoost":
            cls._model = xgb.XGBRegressor()
            cls._model.load_model(str(MODELS_DIR / "xgboost.json"))
        else:
            cls._model = joblib.load(MODELS_DIR / "random_forest.joblib")

        # Load historical data
        engineered_path = DATA_DIR / "processed" / "museum_visitors_engineered.csv"
        if engineered_path.exists():
            cls._historical_df = pd.read_csv(engineered_path, parse_dates=["date"])

        # Load model comparison results
        results_path = MODELS_DIR / "model_results.csv"
        if results_path.exists():
            cls._model_results = pd.read_csv(results_path, index_col=0).to_dict(orient="index")

        # Calibrate XGBoost log-offset and estimate residual std from training data
        if cls._historical_df is not None:
            train = cls._historical_df.iloc[:-90]
            X_train = train[[c for c in cls._features if c in train.columns]]
            raw = cls._model.predict(X_train)

            if cls._best_model_name == "XGBoost":
                # XGBoost 2.x drops base_score from predict() output; compute the
                # offset needed so that expm1(raw + offset) ≈ actual visitors.
                log_actual = np.log1p(train["visitors"].values)
                cls._xgb_log_offset = float((log_actual - raw).mean())
                preds = np.expm1(raw + cls._xgb_log_offset)
            else:
                preds = raw

            cls._residual_std = float(np.std(train["visitors"].values - preds))

        print(f"[ModelService] Loaded: {cls._best_model_name} | "
              f"Features: {len(cls._features)} | "
              f"XGB log-offset: {cls._xgb_log_offset:.4f} | "
              f"Residual std: {cls._residual_std:.1f}")

    @classmethod
    def is_loaded(cls) -> bool:
        return cls._model is not None

    @classmethod
    def predict(cls, feature_row: pd.DataFrame) -> dict:
        raw = cls._model.predict(feature_row)
        point = float(np.expm1(raw[0] + cls._xgb_log_offset)) if cls._best_model_name == "XGBoost" else float(raw[0])
        point = max(0, point)

        std = cls._residual_std or 50.0
        lower_80 = max(0, int(point - 1.28 * std))
        upper_80 = int(point + 1.28 * std)
        lower_95 = max(0, int(point - 1.96 * std))
        upper_95 = int(point + 1.96 * std)

        if point < 250:
            tier = "Low"
        elif point < 450:
            tier = "Medium"
        else:
            tier = "High"

        r2 = cls._model_results.get(cls._best_model_name, {}).get("R2", 0.0)
        confidence = max(0.0, min(1.0, float(r2)))

        return {
            "predicted_visitors": int(round(point)),
            "lower_80": lower_80,
            "upper_80": upper_80,
            "lower_95": lower_95,
            "upper_95": upper_95,
            "traffic_tier": tier,
            "confidence": round(confidence, 3),
            "model_used": cls._best_model_name,
        }

    @classmethod
    def get_historical(cls, date_from=None, date_to=None, limit: int = 365):
        if cls._historical_df is None:
            return pd.DataFrame()
        df = cls._historical_df.copy()
        if date_from:
            df = df[df["date"] >= pd.Timestamp(date_from)]
        if date_to:
            df = df[df["date"] <= pd.Timestamp(date_to)]
        return df.tail(limit)

    @classmethod
    def get_feature_importances(cls, top_n: int = 10) -> list[dict]:
        if cls._model is None:
            return []
        importances = cls._model.feature_importances_
        available = [c for c in cls._features if c in (
            cls._historical_df.columns if cls._historical_df is not None else cls._features
        )]
        pairs = sorted(zip(available, importances[:len(available)]),
                       key=lambda x: x[1], reverse=True)
        return [{"feature": f, "importance": round(float(v), 4)} for f, v in pairs[:top_n]]

    @classmethod
    def build_feature_row(cls, req, historical_df: pd.DataFrame) -> pd.DataFrame:
        """Build a single-row feature DataFrame from a PredictionRequest."""
        import math

        target_date = pd.Timestamp(req.date)

        # Temporal
        dow      = target_date.dayofweek
        month    = target_date.month
        doy      = target_date.dayofyear
        woy      = target_date.isocalendar()[1]
        row = {
            "day_of_week":   dow,
            "month":         month,
            "quarter":       (month - 1) // 3 + 1,
            "week_of_year":  woy,
            "doy":           doy,
            "days_since_start": (target_date - historical_df["date"].min()).days,
            "dow_sin":  math.sin(2 * math.pi * dow / 7),
            "dow_cos":  math.cos(2 * math.pi * dow / 7),
            "month_sin": math.sin(2 * math.pi * (month - 1) / 12),
            "month_cos": math.cos(2 * math.pi * (month - 1) / 12),
            "doy_sin":  math.sin(2 * math.pi * doy / 365),
            "doy_cos":  math.cos(2 * math.pi * doy / 365),
            "woy_sin":  math.sin(2 * math.pi * woy / 52),
            "woy_cos":  math.cos(2 * math.pi * woy / 52),
            "is_weekend": int(dow >= 5),
        }

        # Calendar — use explicit values from request, or auto-detect for Victoria
        if req.is_public_holiday is not None and req.is_school_holiday is not None:
            row["is_public_holiday"] = req.is_public_holiday
            row["is_school_holiday"] = req.is_school_holiday
        else:
            from app.services.calendar_service import get_holiday_info
            cal = get_holiday_info(target_date.date())
            row["is_public_holiday"] = req.is_public_holiday if req.is_public_holiday is not None else cal["is_public_holiday"]
            row["is_school_holiday"] = req.is_school_holiday if req.is_school_holiday is not None else cal["is_school_holiday"]

        # Weather
        temp = req.temperature if req.temperature is not None else _default_temp(month)
        row["temperature"]    = temp
        row["precipitation"]  = req.precipitation or 0.0
        row["weather_type"]   = req.weather_type or "Partly Cloudy"
        row["weather_encoded"] = {"Sunny": 3, "Partly Cloudy": 2, "Cloudy": 1, "Rainy": 0}.get(
            row["weather_type"], 2)
        for wt in ["Sunny", "Partly Cloudy", "Cloudy", "Rainy"]:
            row[f"weather_{wt}"] = int(row["weather_type"] == wt)

        # Season
        def _season(m):
            if m in [12, 1, 2]: return "Summer"
            elif m in [3, 4, 5]: return "Autumn"
            elif m in [6, 7, 8]: return "Winter"
            return "Spring"
        season = _season(month)
        for s in ["Autumn", "Spring", "Summer", "Winter"]:
            row[f"season_{s}"] = int(season == s)

        # Events / marketing
        row["special_exhibition"] = req.special_exhibition or 0
        row["local_event"]        = req.local_event or 0
        row["marketing_campaign"] = req.marketing_campaign or 0
        row["ticket_promotion"]   = req.ticket_promotion or 0
        row["ticket_price"]       = req.ticket_price or 25.0

        # Interactions
        row["weekend_x_public_holiday"] = row["is_weekend"] * row["is_public_holiday"]
        row["weekend_x_school_holiday"] = row["is_weekend"] * row["is_school_holiday"]
        row["exhibition_x_weekend"]     = row["special_exhibition"] * row["is_weekend"]
        row["sunny_weekend"]            = int(row["weather_type"] == "Sunny" and row["is_weekend"])
        row["marketing_x_exhibition"]   = row["marketing_campaign"] * row["special_exhibition"]
        row["any_boost"] = int(any([
            row["is_public_holiday"], row["is_school_holiday"],
            row["special_exhibition"], row["local_event"], row["marketing_campaign"]
        ]))
        row["boost_count"] = (row["is_public_holiday"] + row["is_school_holiday"] +
                              row["special_exhibition"] + row["local_event"] +
                              row["marketing_campaign"] + row["ticket_promotion"])

        # Lag & rolling features from historical data
        past = historical_df[historical_df["date"] < target_date].sort_values("date")
        visitors_series = past["visitors"] if "visitors" in past.columns else pd.Series(dtype=float)

        def lag_val(n):
            return float(visitors_series.iloc[-n]) if len(visitors_series) >= n else float(visitors_series.mean() or 300)

        def roll_val(n, stat="mean"):
            s = visitors_series.iloc[-n:] if len(visitors_series) >= n else visitors_series
            if stat == "mean":  return float(s.mean() or 300)
            if stat == "std":   return float(s.std() or 50)
            if stat == "max":   return float(s.max() or 300)
            if stat == "min":   return float(s.min() or 200)
            return 300.0

        for l in [1, 2, 3, 7, 14, 21, 28, 60, 90]:
            row[f"visitors_lag_{l}"] = lag_val(l)

        row["visitors_last_week"]          = lag_val(7)
        row["visitors_last_2weeks"]        = lag_val(14)
        row["visitors_last_month"]         = lag_val(30)
        row["visitors_same_day_last_year"] = lag_val(365)

        same_dow = past[past["day_of_week"] == dow]["visitors"] if "visitors" in past.columns else pd.Series()
        row["mean_last_4_same_dow"] = float(same_dow.tail(4).mean()) if len(same_dow) >= 1 else 300.0

        for w in [3, 7, 14, 30, 60, 90]:
            row[f"rolling_mean_{w}d"] = roll_val(w, "mean")
            row[f"rolling_std_{w}d"]  = roll_val(w, "std")
            row[f"rolling_max_{w}d"]  = roll_val(w, "max")
            row[f"rolling_min_{w}d"]  = roll_val(w, "min")

        row["ewma_7d"]  = roll_val(7,  "mean")
        row["ewma_14d"] = roll_val(14, "mean")
        row["ewma_30d"] = roll_val(30, "mean")

        # Align to expected feature order
        feature_row = {f: row.get(f, 0.0) for f in cls._features}
        return pd.DataFrame([feature_row])


def _default_temp(month: int) -> float:
    defaults = {1:20.5,2:20.5,3:18.5,4:15.5,5:12.0,6:10.0,
                7:9.5,8:11.0,9:12.5,10:15.0,11:17.0,12:19.5}
    return defaults.get(month, 16.0)
