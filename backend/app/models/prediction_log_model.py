from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy import JSON

from app.database.connection import Base


class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    age = Column(Integer, nullable=False)
    monthly_income = Column(Integer, nullable=False)
    years_at_company = Column(Integer, nullable=False)
    job_satisfaction = Column(Integer, nullable=False)
    overtime = Column(String(10), nullable=False)

    prediction = Column(String(20), nullable=False)
    probability = Column(Float, nullable=False)
    recommendation = Column(String(255), nullable=False)

    top_reasons = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    