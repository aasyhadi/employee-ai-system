from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.connection import Base, engine
from app.models.user_model import User
from app.models.prediction_log_model import PredictionLog
from app.models.model_version_model import ModelVersion

from app.routers.auth_router import router as auth_router
from app.routers.prediction_router import router as prediction_router
from app.routers.dashboard_router import router as dashboard_router
from app.routers.model_router import router as model_router
from app.routers.export_router import router as export_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Employee AI API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(prediction_router)
app.include_router(dashboard_router)
app.include_router(model_router)
app.include_router(export_router)

@app.get("/")
def root():
    return {
        "message": "Employee AI API Running"
    }