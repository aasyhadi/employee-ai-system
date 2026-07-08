import os
import json
import joblib
import pandas as pd
import mlflow
import mlflow.sklearn

mlflow.set_tracking_uri("sqlite:////app/mlflow.db")

from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from app.database.connection import SessionLocal
from app.models.model_version_model import ModelVersion


DATASET_PATH = "dataset/employee_attrition.csv"
MODEL_DIR = "trained_models"

os.makedirs(MODEL_DIR, exist_ok=True)

df = pd.read_csv(DATASET_PATH)

df = df[[
    "Age",
    "MonthlyIncome",
    "YearsAtCompany",
    "JobSatisfaction",
    "OverTime",
    "Attrition"
]]

encoder_overtime = LabelEncoder()
encoder_attrition = LabelEncoder()

df["OverTime"] = encoder_overtime.fit_transform(df["OverTime"])
df["Attrition"] = encoder_attrition.fit_transform(df["Attrition"])

X = df[[
    "Age",
    "MonthlyIncome",
    "YearsAtCompany",
    "JobSatisfaction",
    "OverTime"
]]

y = df["Attrition"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42
)
model.fit(X_train, y_train)
import json
feature_importance = dict(
    zip(
        X.columns,
        model.feature_importances_
    )
)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

mlflow.set_experiment("employee-attrition-randomforest")

with mlflow.start_run():
    mlflow.log_param("model", "RandomForestClassifier")
    mlflow.log_param("n_estimators", 200)
    mlflow.log_param("max_depth", 10)

    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    mlflow.log_metric("f1_score", f1)

    mlflow.sklearn.log_model(
        model,
        "random_forest_model"
    )

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
version_name = f"employee_attrition_{timestamp}"
model_path = f"{MODEL_DIR}/{version_name}.pkl"

with open(
        "trained_models/feature_importance.json",
        "w"
    ) as f:
        json.dump(
            feature_importance,
            f,
            indent=4
        )
        
joblib.dump(
    {
        "model": model,
        "encoder_overtime": encoder_overtime,
        "encoder_attrition": encoder_attrition,
        "features": list(X.columns)
    },
    model_path
)

joblib.dump(
    {
        "model": model,
        "encoder_overtime": encoder_overtime,
        "encoder_attrition": encoder_attrition,
        "features": list(X.columns)
    },
    f"{MODEL_DIR}/employee_attrition.pkl"
)

db = SessionLocal()

new_version = ModelVersion(
    version_name=version_name,
    model_path=model_path,
    accuracy=float(accuracy)
)

db.add(new_version)
db.commit()
db.close()

print(f"Training selesai")
print(f"Version: {version_name}")
print(f"Accuracy: {accuracy}")
print(f"Model path: {model_path}")
print("Feature importance saved:")
print(feature_importance)