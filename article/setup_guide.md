# Setup Guide: Running the Museum Visitor Prediction App Locally

This guide walks you through getting the full application running on your own machine — backend API, frontend dashboard, and (optionally) prediction logging to a database. No prior experience with Python web servers or React is assumed, but you will need a terminal and a few tools installed.

---

## What You Are Setting Up

The application has three parts that talk to each other:

```
Your Browser
    ↕  (displays the dashboard)
Frontend (React app, port 5173)
    ↕  (sends API requests)
Backend  (FastAPI server, port 8000)
    ↕  (logs predictions — optional)
Supabase (cloud PostgreSQL database)
```

You will start the backend first, then the frontend. The browser talks to the frontend, which in turn talks to the backend. The backend loads the trained ML model and returns predictions.

---

## Prerequisites — Install These First

Before anything else, make sure the following are installed on your machine. Each item links to its official install page.

### 1. Python 3.10+

Check if you have it:
```bash
python3 --version
```
You need `3.10` or higher. If you see `command not found` or an older version, download Python from [python.org/downloads](https://www.python.org/downloads/) and run the installer.

> **Windows note**: During the Python installer, tick **"Add Python to PATH"** before clicking Install. If you miss this, Python commands won't work in your terminal.

### 2. Node.js 18+

Check if you have it:
```bash
node --version
```
You need `18` or higher. Download from [nodejs.org](https://nodejs.org/) — choose the **LTS** version. Node includes `npm` (the Node package manager), which you'll need for the frontend.

### 3. Git

Check if you have it:
```bash
git --version
```
If missing, download from [git-scm.com](https://git-scm.com/downloads).

### 4. A terminal

- **Mac**: Use the built-in Terminal app (search "Terminal" in Spotlight).
- **Windows**: Use **PowerShell** or install [Windows Terminal](https://aka.ms/terminal) from the Microsoft Store. Avoid the old Command Prompt — it handles paths differently.
- **Linux**: Any terminal emulator works.

---

## Step 1 — Get the Code

Open your terminal and run:

```bash
git clone <link_to_github_repo>
cd museum-visitor-prediction
```

This downloads the project into a folder called `museum-visitor-prediction` and moves you into it.

> **What is `git clone`?** It copies the entire project from GitHub to your machine. Think of it as downloading a zip file, except it also records the full change history.

After cloning, your folder structure looks like this:

```
museum-visitor-prediction/
├── ml-pipeline/      ← Python scripts that train the model
├── backend/          ← FastAPI server (the API)
├── frontend/         ← React dashboard (the UI)
├── data/             ← Raw and processed CSV data
└── supabase/         ← Database schema (optional)
```

---

## Step 2 — Generate the Trained Model

The backend needs a trained model file to make predictions. The model is not included in the repository (it's generated from data), so you need to run the training pipeline once.

### 2a — Move into the ML pipeline folder

```bash
cd ml-pipeline
```

### 2b — Create a virtual environment

A virtual environment is an isolated box for Python packages. It prevents the packages you install for this project from interfering with other Python projects on your machine.

```bash
python3 -m venv venv
```

This creates a folder called `venv/` inside `ml-pipeline/`.

### 2c — Activate the virtual environment

**Mac / Linux:**
```bash
source venv/bin/activate
```

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

You'll know it's active when your terminal prompt changes to show `(venv)` at the start of the line.

> **Why do we activate?** When the environment is active, `python` and `pip` commands use the isolated packages inside `venv/` instead of your system Python. To leave the environment later, type `deactivate`.

### 2d — Install the required Python packages

```bash
pip install -r requirements.txt
```

This reads `requirements.txt` (a list of libraries the project needs) and installs them all. This will take a couple of minutes the first time.

### 2e — Generate the raw data

```bash
python src/data/generate_data.py
```

This creates `data/raw/museum_visitors_melbourne.csv` — three years of synthetic daily visitor records.

### 2f — Run the training notebooks

The model is trained through a series of Jupyter notebooks. Start Jupyter:

```bash
jupyter notebook
```

Your browser will open automatically to the Jupyter interface. Run the notebooks **in order** by opening each one and clicking **Run → Run All Cells**:

1. `01_data_simulation.ipynb`
2. `02_eda.ipynb`
3. `03_feature_engineering.ipynb`
4. `04_modeling.ipynb`
5. `05_evaluation.ipynb`

> **What are Jupyter notebooks?** They are interactive documents that combine code, text, and charts. Each cell runs a piece of Python code. "Run All Cells" executes every cell from top to bottom.

After notebook 4 finishes, these files will exist in `ml-pipeline/models/`:
```
models/
├── xgboost.json          ← the trained XGBoost model
├── random_forest.joblib  ← the trained Random Forest model
├── features.json         ← ordered list of all 81 features + best model name
└── model_results.csv     ← performance metrics for each model
```

These files are the "contract" between the training pipeline and the backend — the backend reads them at startup.

When done, stop Jupyter with `Ctrl+C` in the terminal and go back to the project root:

```bash
cd ..
```

---

## Step 3 — Start the Backend

The backend is a FastAPI server that loads the trained model and exposes it as a REST API on port 8000.

### 3a — Move into the backend folder

```bash
cd backend
```

### 3b — Create and activate a virtual environment

The backend has its own dependencies separate from the ML pipeline, so it gets its own virtual environment:

```bash
python3 -m venv venv
```

**Mac / Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```powershell
.\venv\Scripts\Activate.ps1
```

### 3c — Install backend dependencies

```bash
pip install -r requirements.txt
```

### 3d — (Optional) Configure the database

If you want predictions to be logged to Supabase, create a file called `.env` inside the `backend/` folder with your Supabase credentials:

```
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-key
APP_ENV=development
```

> **How do I get these values?** Sign up at [supabase.com](https://supabase.com), create a new project, and find your project URL and anon key under **Project Settings → API**. Then run the SQL in `supabase/migrations/001_create_tables.sql` in the Supabase SQL editor to create the tables.

If you skip this step, the backend still works fine — predictions will not be logged but everything else functions normally.

### 3e — Start the server

```bash
uvicorn app.main:app --reload
```

Breaking this command down:
- `uvicorn` — the web server that runs FastAPI applications
- `app.main:app` — tells uvicorn where to find the FastAPI application: inside the `app/` folder, in `main.py`, the variable named `app`
- `--reload` — automatically restarts the server when you save a file (useful during development)

You should see output like:

```
INFO:     Loading model artifacts...
INFO:     Model loaded: XGBoost (MAPE=14.0%)
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

The server is now running. **Leave this terminal open** — the server stops if you close it.

### Verify the backend is working

Open a browser and go to: [http://localhost:8000/docs](http://localhost:8000/docs)

You should see the automatic API documentation page. This lists every endpoint, the fields each one accepts, and lets you try them directly from the browser. If you see this page, the backend is working correctly.

---

## Step 4 — Start the Frontend

Open a **new terminal window** (keep the backend terminal running). Go back to the project root and into the frontend folder:

```bash
cd museum-visitor-prediction/frontend
```

### 4a — Install Node dependencies

```bash
npm install
```

This reads `package.json` and downloads all the JavaScript libraries the frontend needs into a `node_modules/` folder. This takes a minute or two the first time.

### 4b — Configure the API URL

Create a file called `.env` inside the `frontend/` folder:

```
VITE_API_URL=http://localhost:8000
```

This tells the React app where to find the backend. The `VITE_` prefix is required by Vite — without it, the variable is invisible to the frontend code.

### 4c — Start the development server

```bash
npm run dev
```

You should see:

```
  VITE v5.x.x  ready in 300 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### Open the dashboard

Open your browser and go to: [http://localhost:5173](http://localhost:5173)

The museum visitor prediction dashboard should appear. If it does, both services are running correctly.

---

## Verifying Everything Works End-to-End

1. Go to the **Predict** tab
2. Click the date picker and select any future date (e.g., next Saturday)
3. Watch the weather and holiday fields auto-populate — this confirms the frontend is talking to the backend's `/api/date-info` endpoint
4. Click **Predict**
5. A result panel should appear with a visitor estimate, confidence intervals, and a traffic tier badge

If the result appears, the full stack is working: browser → frontend → backend → model → response → browser.

---

## Troubleshooting

### "Module not found" or "No module named X"
The virtual environment is not active, or `pip install -r requirements.txt` was not run. Make sure you see `(venv)` in your terminal prompt before running Python commands.

### "Connection refused" in the browser console
The backend is not running. Check the backend terminal — if it shows an error, read the message. Common causes: wrong working directory when running `uvicorn`, or the model files in `ml-pipeline/models/` don't exist yet (run the notebooks first).

### "CORS error" in the browser console
The frontend is pointed at the wrong backend URL. Check `frontend/.env` — the `VITE_API_URL` should be `http://localhost:8000` (no trailing slash).

### Port already in use
Another process is using port 8000 or 5173. Run the backend on a different port:
```bash
uvicorn app.main:app --reload --port 8001
```
Then update `frontend/.env` to `VITE_API_URL=http://localhost:8001`.

### Windows: "running scripts is disabled"
PowerShell has a security policy that blocks running scripts. Fix it:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then try activating the virtual environment again.

---

## Quick Reference — Commands Summary

| What | Command |
|------|---------|
| Clone the repo | `git clone <repo_url> && cd museum-visitor-prediction` |
| Generate data | `cd ml-pipeline && source venv/bin/activate && python src/data/generate_data.py` |
| Run notebooks | `jupyter notebook` (run 01 through 05 in order) |
| Start backend | `cd backend && source venv/bin/activate && uvicorn app.main:app --reload` |
| Start frontend | `cd frontend && npm run dev` |
| View API docs | [http://localhost:8000/docs](http://localhost:8000/docs) |
| View dashboard | [http://localhost:5173](http://localhost:5173) |

---

## What's Running Where

| Service | URL | What it does |
|---------|-----|--------------|
| Backend API | `http://localhost:8000` | Loads the model, serves predictions |
| API Docs | `http://localhost:8000/docs` | Interactive docs for every endpoint |
| Frontend | `http://localhost:5173` | The React dashboard you interact with |
