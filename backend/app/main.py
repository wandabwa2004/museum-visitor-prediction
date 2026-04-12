from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routes import predict, historical, insights, date_info
from app.services.model_service import ModelService


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load models once at startup
    ModelService.load()
    yield


app = FastAPI(
    title="Museum Visitor Prediction API",
    description="Predict daily visitor numbers for the Melbourne Museum of Migration",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict.router,    prefix="/api", tags=["Predictions"])
app.include_router(historical.router, prefix="/api", tags=["Historical"])
app.include_router(insights.router,   prefix="/api", tags=["Insights"])
app.include_router(date_info.router,  prefix="/api", tags=["Date Info"])


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Museum Visitor Prediction API"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "model_loaded": ModelService.is_loaded()}
