from io import BytesIO
import pandas as pd

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.auth import get_current_user
from app.models.user_model import User
from app.models.prediction_log_model import PredictionLog

router = APIRouter(
    prefix="/api/export",
    tags=["Export"]
)

@router.get("/predictions/excel")
def export_predictions_excel(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    rows = (
        db.query(PredictionLog)
        .filter(
            PredictionLog.user_id ==
            current_user.id
        )
        .all()
    )

    data = []

    for item in rows:
        data.append({
            "Age": item.age,
            "Income": item.monthly_income,
            "Years": item.years_at_company,
            "Overtime": item.overtime,
            "Prediction": item.prediction,
            "Probability": item.probability,
            "Date": item.created_at
        })

    df = pd.DataFrame(data)

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:
        df.to_excel(
            writer,
            index=False
        )

    output.seek(0)

    return StreamingResponse(
        output,
        media_type=
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition":
            "attachment; filename=prediction_history.xlsx"
        }
    )