# Museum of Migration - Visitor Prediction Project

## Project Overview
An end-to-end predictive analytics solution to forecast daily/weekly visitor numbers to the Museum of Migration. This project will demonstrate how data science helps non-technical stakeholders make informed decisions about staffing, resource allocation, and visitor experience optimization.

## Business Objectives
- **Primary Goal**: Predict visitor numbers to optimize museum operations
- **Target Audience**: Museum administrators, operations managers, and policy makers
- **Deliverable**: A functional web application where users can input parameters and get visitor predictions

## Use Cases
1. **Staffing Optimization**: Predict peak days to schedule adequate staff
2. **Resource Planning**: Forecast busy periods for catering, security, and maintenance
3. **Marketing Insights**: Understand what drives visitor traffic
4. **Budget Planning**: Anticipate revenue from admissions and gift shop sales

---

## Data Requirements

### Temporal Features
- **Date**: Specific date of visit
- **Day of Week**: Monday through Sunday (weekends typically busier)
- **Month/Season**: Seasonal patterns (summer tourism, school holidays)
- **Public Holidays**: National and local holidays
- **School Holidays**: Half-term breaks, summer holidays
- **Week of Month**: First, second, third, fourth week

### Weather Conditions
- **Temperature**: Daily average (°C)
- **Precipitation**: Rainfall amount (mm)
- **Weather Type**: Sunny, Cloudy, Rainy, Snowy
- **Weather Forecast Accuracy**: Real vs predicted weather

### External Events
- **Special Exhibitions**: Temporary exhibitions at the museum
- **Local Events**: Festivals, conferences, sports events in the city
- **Tourism Indicators**: Hotel occupancy rates, airport arrivals
- **Museum Events**: Workshops, guided tours, special programs

### Marketing & Promotion
- **Marketing Campaigns**: Active social media or advertising campaigns
- **Ticket Promotions**: Discounts or special offers
- **Media Coverage**: Recent news articles or features about the museum

### Historical Performance
- **Previous Week Visitors**: Lagged features (7-day, 14-day, 30-day averages)
- **Same Day Last Year**: Year-over-year comparison
- **Trend**: Overall upward or downward visitor trends

### Economic Indicators
- **Economic Sentiment**: Consumer confidence index
- **Exchange Rates**: For international tourism (GBP/EUR/USD)
- **Fuel Prices**: Impact on domestic tourism

### Operational Factors
- **Ticket Price**: Current admission price
- **Opening Hours**: Extended or reduced hours
- **Accessibility**: Any closures or maintenance affecting access

---

## Technical Requirements

### Technology Stack

#### Data Science & ML
- **Language**: Python 3.10+
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn, Plotly
- **ML Libraries**: Scikit-learn, XGBoost, Prophet
- **Model Serialization**: Joblib/Pickle

#### Frontend
- **Framework**: React 18+
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui or Ant Design
- **Charts**: Recharts or Chart.js
- **HTTP Client**: Axios
- **State Management**: React Context or Zustand

#### Backend
- **Framework**: FastAPI
- **Validation**: Pydantic
- **CORS**: FastAPI middleware
- **Environment**: Python 3.10+

#### Database
- **Platform**: Supabase (PostgreSQL)
- **Client**: Supabase JS SDK (frontend), Supabase Python SDK (backend)
- **Features**: Real-time subscriptions, Auth (optional)

#### DevOps & Deployment
- **Version Control**: Git/GitHub
- **Frontend Hosting**: Vercel or Netlify
- **Backend Hosting**: Railway, Render, or Fly.io
- **Database**: Supabase Cloud
- **CI/CD**: GitHub Actions (optional)

### Data Simulation
- Generate 2-3 years of historical data
- Incorporate realistic patterns:
  - Seasonal variations
  - Day-of-week effects
  - Holiday spikes
  - Weather correlations
  - Special event impacts
- Add appropriate noise and outliers

### Model Development
- **Algorithms to Consider**:
  - Time series models (ARIMA, SARIMA, Prophet)
  - Machine learning (Random Forest, XGBoost, LightGBM)
  - Deep learning (LSTM, if data is sufficient)
- **Evaluation Metrics**:
  - MAE (Mean Absolute Error)
  - RMSE (Root Mean Squared Error)
  - MAPE (Mean Absolute Percentage Error)
  - R² Score
- **Model Interpretability**: Feature importance, SHAP values

### Application Requirements

#### Frontend (React + Vite)
- **Framework**: React 18+ with Vite for fast development
- **UI Library**: Tailwind CSS or shadcn/ui for modern, responsive design
- **Charts**: Recharts or Chart.js for data visualization
- **Features**:
  - Date picker for prediction date
  - Input forms for weather, events, promotions
  - Real-time prediction results with confidence intervals
  - Interactive historical trends dashboard
  - Responsive design for mobile and desktop
  - Loading states and error handling

#### Backend
- **API**: FastAPI or Flask for Python-based ML model serving
- **Endpoints**:
  - `POST /api/predict` - Get visitor predictions
  - `GET /api/historical` - Fetch historical data
  - `GET /api/insights` - Model performance metrics
- **Model Serving**: Pickle/Joblib serialized models

#### Database (Supabase)
- **Historical Data Storage**: Store simulated visitor data
- **User Analytics**: Track app usage (optional)
- **Predictions Log**: Store predictions for comparison with actuals
- **Real-time Updates**: Supabase realtime for live dashboards (if needed)

#### Deployment
- **Frontend**: Vercel or Netlify
- **Backend**: Railway, Render, or Fly.io
- **Database**: Supabase cloud
- **Documentation**: User guide for non-technical users

---

## Project Structure
```
museum-visitor-prediction/
├── data/
│   ├── raw/                  # Simulated raw data
│   ├── processed/            # Cleaned and feature-engineered data
│   └── external/             # External data sources (if any)
├── notebooks/
│   ├── 01_data_simulation.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_modeling.ipynb
│   └── 05_evaluation.ipynb
├── ml-pipeline/
│   ├── src/
│   │   ├── data/             # Data processing scripts
│   │   ├── features/         # Feature engineering
│   │   ├── models/           # Model training and prediction
│   │   └── visualization/    # Plotting utilities
│   ├── models/               # Saved model artifacts
│   ├── tests/                # Unit tests
│   └── requirements.txt      # Python dependencies
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI application
│   │   ├── models.py         # Pydantic models
│   │   ├── routes/           # API endpoints
│   │   │   ├── predict.py
│   │   │   └── historical.py
│   │   └── services/
│   │       ├── ml_service.py # Model loading and prediction
│   │       └── supabase_client.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── PredictionForm.jsx
│   │   │   ├── ResultsDisplay.jsx
│   │   │   ├── HistoricalChart.jsx
│   │   │   └── Dashboard.jsx
│   │   ├── services/         # API calls
│   │   │   └── api.js
│   │   ├── utils/            # Helper functions
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── supabase/
│   ├── migrations/           # Database migrations
│   └── seed.sql              # Initial data seeding
├── README.md                 # Project documentation
└── REQUIREMENTS.md           # This file

```

---

## Success Criteria
- Model achieves MAPE < 15% on test data
- Application is user-friendly for non-technical users
- Clear visualizations explain predictions
- Documented insights for museum operations
- Deployable and shareable demo

---

## Next Steps
1. **Review and Refine Requirements**: Discuss and finalize data features
2. **Data Simulation**: Create realistic synthetic dataset
3. **Exploratory Data Analysis**: Understand patterns and relationships
4. **Feature Engineering**: Create derived features
5. **Model Development**: Train and compare multiple models
6. **Model Evaluation**: Select best performing model
7. **Application Development**: Build interactive web app
8. **Testing & Documentation**: Ensure quality and usability
9. **Deployment**: Make it accessible to end users
10. **Article Writing**: Document the journey for Medium

---

## Project Specifications (Finalized)

### Prediction Details
- **Granularity**: Daily visitor predictions
- **Typical Range**: 200-400 visitors/day
- **Peak Range**: Up to 1000+ visitors during favorable conditions
- **Location**: Melbourne, Australia
- **Output Type**: Exact numbers (regression model) for planning purposes
- **Prediction Horizons**:
  - 1 day ahead (short-term staffing)
  - 7 days ahead (weekly planning)
  - 14 days ahead (fortnightly resource allocation)

### Melbourne-Specific Considerations
- **Seasons**: Southern Hemisphere (Summer: Dec-Feb, Winter: Jun-Aug)
- **Public Holidays**: Australian national and Victorian state holidays
- **School Holidays**: Victorian school term breaks
- **Weather**: Temperate oceanic climate (four seasons, variable weather)
- **Tourism**: Major tourist destination, international and domestic visitors
- **Time Zone**: AEST (UTC+10) / AEDT (UTC+11 during daylight saving)

