from fastapi import APIRouter, UploadFile, File
import shutil
import os
import subprocess
import json

from sqlalchemy.orm import Session
from fastapi import Depends
from app.database.connection import get_db
from app.models.model_version_model import ModelVersion

router = APIRouter(
    prefix="/api/model",
    tags=["Model Training"]
)

UPLOAD_PATH = "dataset/employee_attrition.csv"


@router.post("/upload-dataset")
def upload_dataset(file: UploadFile = File(...)):
    os.makedirs("dataset", exist_ok=True)

    with open(UPLOAD_PATH, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "Dataset berhasil diupload",
        "filename": file.filename
    }


@router.post("/retrain")
def retrain_model():
    result = subprocess.run(
        ["python", "scripts/train_model.py"],
        capture_output=True,
        text=True
    )

    return {
        "message": "Training selesai",
        "stdout": result.stdout,
        "stderr": result.stderr
    }

@router.get("/versions")
def get_model_versions(db: Session = Depends(get_db)):
    versions = (
        db.query(ModelVersion)
        .order_by(ModelVersion.created_at.desc())
        .all()
    )

    return versions

@router.get("/feature-importance")
def get_feature_importance():
    file_path = "trained_models/feature_importance.json"

    if not os.path.exists(file_path):
        return {
            "message": "Feature importance belum tersedia. Jalankan retrain model terlebih dahulu.",
            "data": []
        }

    with open(file_path, "r") as f:
        data = json.load(f)

    result = [
        {
            "feature": key,
            "importance": round(value, 4)
        }
        for key, value in data.items()
    ]

    result = sorted(
        result,
        key=lambda x: x["importance"],
        reverse=True
    )

    return result