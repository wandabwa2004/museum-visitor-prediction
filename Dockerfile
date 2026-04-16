FROM python:3.11-slim

WORKDIR /app

# System deps for Prophet / pystan
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ libgomp1 && \
    rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code
COPY backend/app/ ./app/

# Model artifacts and data (paths relative to repo root build context)
COPY ml-pipeline/models/ ./ml-pipeline/models/
COPY data/processed/      ./data/processed/
COPY data/raw/            ./data/raw/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
