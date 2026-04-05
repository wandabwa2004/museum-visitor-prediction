# Museum Visitor Prediction — CLAUDE.md

## Project Overview

End-to-end predictive analytics system forecasting daily visitor numbers for the **Museum of Migration, Melbourne, Australia**. Built as a data science demonstration for non-technical stakeholders covering staffing, resource planning, and revenue forecasting.

- **Target**: 200–400 visitors/day typical; up to 1,200 during peak events
- **Location**: Melbourne (Southern Hemisphere seasons, Victorian public/school holidays)
- **Data**: 3 years synthetic data (2023–2025), 1,096 daily records

## Architecture

```
museum-visitor-prediction/
├── data/
│   ├── raw/museum_visitors_melbourne.csv      # Synthetic generated data
│   └── processed/museum_visitors_engineered.csv  # Feature-engineered data
├── notebooks/                                 # Jupyter analysis notebooks (01–05)
├── ml-pipeline/
│   ├── src/data/generate_data.py             # Data generation script
│   └── models/                               # Saved model artifacts
│       ├── xgboost.json
│       ├── random_forest.joblib
│       ├── prophet.pkl
│       ├── features.json                     # Feature list + best model name
│       └── model_results.csv                 # Model comparison metrics
├── backend/                                  # FastAPI application
│   └── app/
│       ├── main.py                           # App entry point + lifespan
│       ├── models.py                         # Pydantic request/response models
│       ├── routes/predict.py                 # POST /api/predict
│       ├── routes/historical.py              # GET /api/historical
│       ├── routes/insights.py                # GET /api/insights
│       └── services/
│           ├── model_service.py              # Model loading + inference + feature engineering
│           └── supabase_client.py            # Supabase logging (non-blocking)
├── frontend/                                 # React + Vite dashboard
│   └── src/
│       ├── App.jsx
│       ├── components/                       # PredictionForm, PredictionResult, HistoricalChart, InsightsPanel, StatCard
│       └── services/api.js
└── supabase/migrations/001_create_tables.sql # PostgreSQL schema
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| ML/Data | Python 3.10+, Pandas, NumPy, Scikit-learn, XGBoost, Prophet, SHAP |
| Backend | FastAPI, Pydantic v2, Uvicorn |
| Frontend | React 18, Vite, Tailwind CSS, Recharts, Axios |
| Database | Supabase (PostgreSQL) |
| Deployment | Frontend → Vercel, Backend → Railway, DB → Supabase Cloud |

## Development Commands

### ML Pipeline
```bash
cd ml-pipeline
source venv/bin/activate          # activate venv (Python 3.9 in venv)
pip install -r requirements.txt   # first-time setup
python src/data/generate_data.py  # generate raw data → data/raw/
jupyter notebook                  # explore notebooks/
```

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload     # runs on http://localhost:8000
# Docs: http://localhost:8000/docs
```

### Frontend
```bash
cd frontend
npm install
npm run dev                       # runs on http://localhost:5173
npm run build
```

## Key Design Decisions

### Model Service (`backend/app/services/model_service.py`)
- `ModelService` is a **class with only classmethods** — acts as a singleton loaded once at startup via FastAPI `lifespan`
- Supports XGBoost (log-transformed target, `np.expm1` on output) and Random Forest
- Best model determined by `ml-pipeline/models/features.json` (`best_model` key)
- Prediction intervals use residual std from training data (80% = ±1.28σ, 95% = ±1.96σ)
- Traffic tiers: Low (<250), Medium (250–450), High (>450)

### Feature Engineering
- Cyclical encoding for temporal features (sin/cos for day-of-week, month, day-of-year, week-of-year)
- Melbourne Southern Hemisphere seasons: Summer Dec–Feb, Autumn Mar–May, Winter Jun–Aug, Spring Sep–Nov
- Weather encoded as both ordinal (`weather_encoded`: Sunny=3…Rainy=0) and one-hot columns
- Lag features: 1, 2, 3, 7, 14, 21, 28, 60, 90 days; rolling stats (mean/std/max/min) at 3, 7, 14, 30, 60, 90 days
- Interaction features: `weekend_x_public_holiday`, `exhibition_x_weekend`, `sunny_weekend`, `marketing_x_exhibition`, `boost_count`

### Supabase Logging
- Prediction logging is **non-blocking** — wrapped in try/except, only runs if `SUPABASE_URL` env var is set
- Tables: `visitor_data` (historical), `predictions_log` (prediction audit trail with `actual_visitors` backfill)

### API Endpoints
- `POST /api/predict` — accepts `PredictionRequest`, returns `PredictionResponse` with point estimate + intervals + tier
- `GET /api/historical` — filtered/paginated historical records
- `GET /api/insights` — best model metrics, feature importances, model comparison

## Environment Variables

**Backend** (`backend/.env`):
```
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-or-service-role-key
APP_ENV=production
```

**Frontend** (`frontend/.env`):
```
VITE_API_URL=http://localhost:8000
```

## Notebook Workflow (in order)

1. `01_data_simulation.ipynb` — generate synthetic data
2. `02_eda.ipynb` — exploratory data analysis
3. `03_feature_engineering.ipynb` — create features → saves `museum_visitors_engineered.csv`
4. `04_modeling.ipynb` — train Random Forest, XGBoost, Prophet → saves model artifacts + `features.json`
5. `05_evaluation.ipynb` — model evaluation and SHAP interpretability

## ML Model Evaluation Targets
- MAPE < 15% on test set
- Metrics tracked: MAE, RMSE, R², MAPE, Bias

## Important Notes

- The venv in `ml-pipeline/venv/` uses Python 3.9 (not 3.10+)
- `features.json` in `ml-pipeline/models/` is the contract between notebooks and the backend — it contains the ordered feature list and best model name
- XGBoost model is trained on `log1p(visitors)` — predictions require `expm1` inverse transform
- Default temperature fallbacks by month are hardcoded in `model_service.py:_default_temp()` for Melbourne climate
- CORS is set to `allow_origins=["*"]` — restrict in production
