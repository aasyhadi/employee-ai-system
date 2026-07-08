from pydantic import BaseModel
from datetime import datetime


class PredictionRequest(BaseModel):
    age: int
    monthly_income: int
    years_at_company: int
    job_satisfaction: int
    overtime: str


class PredictionResponse(BaseModel):
    prediction: str
    probability: float
    recommendation: str

class PredictionHistoryResponse(BaseModel):
    id: int
    age: int
    monthly_income: int
    years_at_company: int
    job_satisfaction: int
    overtime: str
    prediction: str
    probability: float
    recommendation: str
    created_at: datetime

    class Config:
        from_attributes = True