import joblib
import pandas as pd
import shap

from sqlalchemy.orm import Session
from app.models.prediction_log_model import PredictionLog

MODEL_PATH = "trained_models/employee_attrition.pkl"

model_package = joblib.load(MODEL_PATH)

model = model_package["model"]
features = model_package["features"]
encoder_overtime = model_package["encoder_overtime"]
encoder_target = model_package["encoder_attrition"]


def get_recommendation(prediction_label, probability):
    if prediction_label == "Yes":
        if probability >= 0.8:
            return "High attrition risk. Immediate HR intervention is recommended."
        return "Potential attrition risk. Monitor employee condition closely."

    return "Low attrition risk. Maintain current engagement strategy."


def get_top_reasons(input_df):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(input_df)

    if isinstance(shap_values, list):
        values = shap_values[1][0]
    else:
        values = shap_values[0]

    reasons = []

    for feature, value in zip(features, values):
        reasons.append({
            "feature": feature,
            "impact": round(float(value), 4)
        })

    reasons = sorted(
        reasons,
        key=lambda x: abs(x["impact"]),
        reverse=True
    )

    return reasons[:3]


def predict_attrition(request, db: Session, user_id: int):
    overtime_encoded = encoder_overtime.transform([request.overtime])[0]

    input_df = pd.DataFrame([{
        "Age": request.age,
        "MonthlyIncome": request.monthly_income,
        "YearsAtCompany": request.years_at_company,
        "JobSatisfaction": request.job_satisfaction,
        "OverTime": overtime_encoded
    }])

    input_df = input_df[features]

    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]

    prediction_label = encoder_target.inverse_transform([prediction])[0]
    probability = float(probabilities[prediction])

    try:
        top_reasons = get_top_reasons(input_df)
    except Exception as e:
        print("SHAP ERROR:", e)
        top_reasons = []

    recommendation = get_recommendation(
        prediction_label,
        probability
    )

    log = PredictionLog(
        user_id=user_id,
        age=request.age,
        monthly_income=request.monthly_income,
        years_at_company=request.years_at_company,
        job_satisfaction=request.job_satisfaction,
        overtime=request.overtime,
        prediction=prediction_label,
        probability=round(probability, 4),
        recommendation=recommendation,
        top_reasons=top_reasons
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return {
        "prediction": prediction_label,
        "probability": round(probability, 4),
        "recommendation": recommendation,
        "top_reasons": top_reasons
    }