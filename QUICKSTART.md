# Quick Start Guide

Get started with the Museum Visitor Prediction project in 3 simple steps!

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Node.js 18+ (for React frontend, later)
- Git

## Step 1: Set Up Python Environment

```bash
# Navigate to the ML pipeline directory
cd ml-pipeline

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

## Step 2: Generate Synthetic Data

You have two options:

### Option A: Using Jupyter Notebook (Recommended for exploration)

```bash
# Start Jupyter Notebook
jupyter notebook

# Open notebooks/01_data_simulation.ipynb
# Run all cells to generate data and visualizations
```

### Option B: Using Python Script (Quick generation)

```bash
# Run the data generation script
cd ml-pipeline
python src/data/generate_data.py
```

Both methods will create a CSV file at:
```
data/raw/museum_visitors_melbourne.csv
```

## Step 3: Verify Data Generation

```bash
# Check that the data file exists
ls -lh data/raw/museum_visitors_melbourne.csv

# Quick preview (first 10 rows)
head data/raw/museum_visitors_melbourne.csv
```

## What's Next?

After generating the data, you can:

1. **Explore the data** - Run the Jupyter notebooks in order:
   - `01_data_simulation.ipynb` ✓ (Done)
   - `02_eda.ipynb` (Coming next - exploratory data analysis)
   - `03_feature_engineering.ipynb` (Feature creation)
   - `04_modeling.ipynb` (Train ML models)
   - `05_evaluation.ipynb` (Model evaluation)

2. **Build the backend API** - Set up FastAPI to serve predictions

3. **Create the React frontend** - Build the user interface

4. **Deploy the application** - Make it accessible to users

## Dataset Overview

The generated dataset includes:

- **3 years of data** (2023-2025)
- **1,096 records** (daily observations)
- **Typical visitors**: 200-400 per day
- **Peak visitors**: Up to 1,200 during special events

### Features

- **Temporal**: Date, day of week, month, season
- **Holidays**: Public holidays, school holidays
- **Weather**: Temperature, precipitation, weather type
- **Events**: Special exhibitions, local events
- **Marketing**: Campaigns, promotions, ticket prices
- **Historical**: Lagged features (7-day, 14-day, 30-day averages)
- **Target**: Number of visitors

## Project Structure

```
museum-visitor-prediction/
├── data/
│   └── raw/
│       └── museum_visitors_melbourne.csv  # Generated data
├── notebooks/
│   └── 01_data_simulation.ipynb          # Data generation notebook
├── ml-pipeline/
│   ├── src/
│   │   └── data/
│   │       └── generate_data.py          # Data generation script
│   ├── requirements.txt                  # Python dependencies
│   └── venv/                             # Virtual environment
└── QUICKSTART.md                         # This file
```

## Troubleshooting

### Issue: ModuleNotFoundError

**Solution**: Make sure you've activated the virtual environment and installed requirements:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue: Jupyter Notebook not found

**Solution**: Install Jupyter in your virtual environment:
```bash
pip install jupyter notebook
```

### Issue: Data file not created

**Solution**: Check that you're running the script from the correct directory:
```bash
cd museum-visitor-prediction/ml-pipeline
python src/data/generate_data.py
```

## Need Help?

- Check the main [README.md](README.md) for detailed project information
- Review [REQUIREMENTS.md](REQUIREMENTS.md) for specifications
- Ensure all prerequisites are installed

---

**Ready to build predictive models!** 🚀
