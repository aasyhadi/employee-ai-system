from io import BytesIO
import pandas as pd

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.auth import get_current_user
from app.models.user_model import User
from app.models.prediction_log_model import PredictionLog

from sqlalchemy import func
from app.models.model_version_model import ModelVersion

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

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
        .filter(PredictionLog.user_id == current_user.id)
        .order_by(PredictionLog.created_at.desc())
        .all()
    )

    data = []

    for item in rows:
        data.append({
            "Age": item.age,
            "Monthly Income": item.monthly_income,
            "Years At Company": item.years_at_company,
            "Overtime": item.overtime,
            "Prediction": item.prediction,
            "Probability": item.probability,
            "Created At": item.created_at,
        })

    df = pd.DataFrame(data)

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(
            writer,
            index=False,
            sheet_name="Prediction History"
        )

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=prediction_history.xlsx"
        }
    )
    
@router.get("/predictions/pdf")
def export_pdf(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    output = BytesIO()

    doc = SimpleDocTemplate(output)

    styles = getSampleStyleSheet()

    elements = []

    # =====================================
    # TITLE
    # =====================================

    elements.append(
        Paragraph(
            "Employee AI Executive Report",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 20))

    # =====================================
    # SUMMARY DATA
    # =====================================

    total = (
        db.query(PredictionLog)
        .filter(
            PredictionLog.user_id == current_user.id
        )
        .count()
    )

    high_risk = (
        db.query(PredictionLog)
        .filter(
            PredictionLog.user_id == current_user.id,
            PredictionLog.prediction == "High Risk"
        )
        .count()
    )

    low_risk = total - high_risk

    avg_probability = (
        db.query(
            func.avg(
                PredictionLog.probability
            )
        )
        .filter(
            PredictionLog.user_id == current_user.id
        )
        .scalar()
    )

    if avg_probability is None:
        avg_probability = 0

    elements.append(
        Paragraph(
            "Summary Statistics",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            f"Total Predictions : {total}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"High Risk Employees : {high_risk}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Low Risk Employees : {low_risk}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Average Probability : {avg_probability:.2%}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 20))

    # =====================================
    # MODEL INFORMATION
    # =====================================

    latest_model = (
        db.query(ModelVersion)
        .order_by(
            ModelVersion.created_at.desc()
        )
        .first()
    )

    elements.append(
        Paragraph(
            "Model Information",
            styles["Heading2"]
        )
    )

    if latest_model:
        elements.append(
            Paragraph(
                f"Version : {latest_model.version_name}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"Accuracy : {latest_model.accuracy:.2%}",
                styles["Normal"]
            )
        )

    else:
        elements.append(
            Paragraph(
                "No trained model available",
                styles["Normal"]
            )
        )

    elements.append(Spacer(1, 20))

    # =====================================
    # RECENT PREDICTIONS
    # =====================================

    elements.append(
        Paragraph(
            "Recent Predictions",
            styles["Heading2"]
        )
    )

    rows = (
        db.query(PredictionLog)
        .filter(
            PredictionLog.user_id == current_user.id
        )
        .order_by(
            PredictionLog.created_at.desc()
        )
        .limit(10)
        .all()
    )

    table_data = [
        [
            "Age",
            "Income",
            "Years",
            "Prediction"
        ]
    ]

    for item in rows:
        table_data.append([
            item.age,
            item.monthly_income,
            item.years_at_company,
            item.prediction
        ])

    table = Table(table_data)

    table.setStyle(
        TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ])
    )

    elements.append(table)

    # =====================================
    # BUILD PDF
    # =====================================

    doc.build(elements)

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
            "attachment; filename=employee_ai_report.pdf"
        }
    )