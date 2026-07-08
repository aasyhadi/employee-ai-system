from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.connection import get_db
from app.core.auth import get_current_user
from app.models.user_model import User
from app.models.prediction_log_model import PredictionLog
from app.models.model_version_model import ModelVersion

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
)


@router.get("/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    total_predictions = db.query(PredictionLog).count()

    high_risk = db.query(PredictionLog)\
        .filter(PredictionLog.prediction == "Yes")\
        .count()

    low_risk = db.query(PredictionLog)\
        .filter(PredictionLog.prediction == "No")\
        .count()

    average_probability = db.query(
        func.avg(PredictionLog.probability)
    ).scalar()

    health_score = 0
    if total_predictions > 0:
        health_score = (low_risk / total_predictions) * 100

    return {
        "total_predictions": total_predictions,
        "high_risk": high_risk,
        "low_risk": low_risk,
        "average_probability": round(float(average_probability or 0), 2),
        "health_score": round(health_score, 2)
    }

@router.get("/model-summary")
def model_summary(db: Session = Depends(get_db)):
    total_versions = db.query(ModelVersion).count()

    latest_model = (
        db.query(ModelVersion)
        .order_by(ModelVersion.created_at.desc())
        .first()
    )

    best_model = (
        db.query(ModelVersion)
        .order_by(ModelVersion.accuracy.desc())
        .first()
    )

    return {
        "total_versions": total_versions,
        "latest_accuracy": latest_model.accuracy if latest_model else 0,
        "best_accuracy": best_model.accuracy if best_model else 0,
        "latest_version": latest_model.version_name if latest_model else "-"
    }

@router.get("/prediction-trend")
def prediction_trend(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    rows = (
        db.query(
            func.date(PredictionLog.created_at).label("date"),
            func.count(PredictionLog.id).label("total")
        )
        .filter(PredictionLog.user_id == current_user.id)
        .group_by(func.date(PredictionLog.created_at))
        .order_by(func.date(PredictionLog.created_at))
        .all()
    )

    return [
        {
            "date": str(row.date),
            "total": row.total
        }
        for row in rows
    ]

@router.get("/recent-predictions")
def recent_predictions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    rows = (
        db.query(PredictionLog)
        .filter(PredictionLog.user_id == current_user.id)
        .order_by(PredictionLog.created_at.desc())
        .limit(5)
        .all()
    )

    return rows

@router.get("/top-risk")
def top_risk_employees(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    rows = (
        db.query(PredictionLog)
        .filter(
            PredictionLog.user_id == current_user.id
        )
        .order_by(
            PredictionLog.probability.desc()
        )
        .limit(10)
        .all()
    )

    return rows