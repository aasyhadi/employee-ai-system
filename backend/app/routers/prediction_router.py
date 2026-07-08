from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.auth import get_current_user
from app.models.user_model import User
from app.models.prediction_log_model import PredictionLog
from app.schemas.prediction_schema import (
    PredictionRequest,
    PredictionResponse,
    PredictionHistoryResponse
)
from app.services.prediction_service import predict_attrition

router = APIRouter(
    prefix="/api/predictions",
    tags=["Predictions"]
)


@router.post("/", response_model=PredictionResponse)
def predict(
    request: PredictionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return predict_attrition(
        request=request,
        db=db,
        user_id=current_user.id
    )


@router.get("/history", response_model=List[PredictionHistoryResponse])
def history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logs = db.query(PredictionLog)\
        .filter(PredictionLog.user_id == current_user.id)\
        .order_by(PredictionLog.created_at.desc())\
        .all()

    return logs