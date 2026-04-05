# Museum Visitor Prediction System

> An end-to-end data science project demonstrating predictive analytics for museum visitor forecasting

![Project Status](https://img.shields.io/badge/status-in%20development-yellow)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![React](https://img.shields.io/badge/react-18+-61dafb)
![FastAPI](https://img.shields.io/badge/fastapi-0.100+-green)

## Overview

This project predicts daily visitor numbers for the Museum of Migration using machine learning and time series analysis. It's designed to help non-technical stakeholders understand how data science can optimize museum operations, staffing, and resource allocation.

**Key Features:**
- Simulated realistic museum visitor data (2-3 years)
- Multiple ML models (Random Forest, XGBoost, Prophet)
- Interactive React dashboard for predictions
- RESTful API for model serving
- Historical trends and insights visualization

## Business Value

### Use Cases
1. **Staffing Optimization** - Schedule staff based on predicted visitor traffic
2. **Resource Planning** - Prepare for busy periods (catering, security, maintenance)
3. **Marketing ROI** - Understand impact of campaigns on visitor numbers
4. **Revenue Forecasting** - Anticipate ticket sales and gift shop revenue

### Target Audience
- Museum administrators
- Operations managers
- Marketing teams
- Policy makers

## Technology Stack

### Frontend
- React 18+ with Vite
- Tailwind CSS for styling
- Recharts for data visualization
- Axios for API calls

### Backend
- FastAPI for API endpoints
- Python ML models (Scikit-learn, XGBoost, Prophet)
- Pydantic for data validation

### Database
- Supabase (PostgreSQL) for data storage
- Historical visitor data
- Prediction logs

### ML Pipeline
- Pandas & NumPy for data processing
- Scikit-learn for preprocessing and modeling
- XGBoost for gradient boosting
- Prophet for time series forecasting
- SHAP for model interpretability

## Project Structure

```
museum-visitor-prediction/
├── data/                    # Raw and processed datasets
├── notebooks/               # Jupyter notebooks for analysis
├── ml-pipeline/            # ML training and evaluation
├── backend/                # FastAPI application
├── frontend/               # React application
├── supabase/               # Database migrations and seeds
├── README.md               # This file
└── REQUIREMENTS.md         # Detailed requirements
```

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- Supabase account (free tier)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd museum-visitor-prediction
   ```

2. **Set up the ML pipeline**
   ```bash
   cd ml-pipeline
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up the backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Set up the frontend**
   ```bash
   cd frontend
   npm install
   ```

5. **Configure Supabase**
   - Create a project at supabase.com
   - Copy `.env.example` to `.env` in frontend and backend
   - Add your Supabase URL and API keys

### Running the Application

1. **Start the backend**
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```
   API will be available at `http://localhost:8000`

2. **Start the frontend**
   ```bash
   cd frontend
   npm run dev
   ```
   App will be available at `http://localhost:5173`

## Development Workflow

1. **Data Simulation** - Generate synthetic visitor data
2. **EDA** - Explore patterns and relationships
3. **Feature Engineering** - Create predictive features
4. **Model Training** - Train and evaluate models
5. **Model Selection** - Choose best performing model
6. **API Development** - Build FastAPI endpoints
7. **Frontend Development** - Create React interface
8. **Testing** - Unit and integration tests
9. **Deployment** - Deploy to production

## Model Features

The prediction model considers:
- **Temporal**: Day of week, month, holidays, school breaks
- **Weather**: Temperature, precipitation, weather type
- **Events**: Special exhibitions, local events, museum programs
- **Marketing**: Campaigns, promotions, media coverage
- **Historical**: Previous visitor trends, year-over-year comparison
- **Economic**: Exchange rates, consumer sentiment

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Key Endpoints
- `POST /api/predict` - Get visitor prediction
- `GET /api/historical` - Fetch historical data
- `GET /api/insights` - Model performance metrics

## Deployment

### Frontend (Vercel)
```bash
cd frontend
vercel deploy
```

### Backend (Railway)
```bash
cd backend
railway up
```

### Database
Already hosted on Supabase Cloud

## Contributing

This is a demonstration project for educational purposes. Suggestions and improvements are welcome!

## License

MIT License - See LICENSE file for details

## Author

Created as part of a data science article series demonstrating end-to-end ML projects for non-technical audiences.

## Acknowledgments

- Inspired by real-world museum analytics challenges
- Built with modern web and ML technologies
- Designed for educational and demonstration purposes

---

For detailed requirements and specifications, see [REQUIREMENTS.md](./REQUIREMENTS.md)
