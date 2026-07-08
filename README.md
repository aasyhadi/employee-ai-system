# Employee AI System

Sistem Employee Attrition Prediction berbasis Artificial Intelligence menggunakan FastAPI, React, PostgreSQL, Machine Learning, SHAP Explainability, MLflow Tracking, dan Docker.

---

# Features

## Authentication

- JWT Authentication
- Login
- Protected API
- Role Based Access (Ready)

## Employee Management

- CRUD Employee
- Search Employee
- Filter Employee
- Pagination

## AI Prediction

- Employee Attrition Prediction
- Random Forest Model
- Probability Score
- Risk Classification

## Explainable AI

- SHAP Feature Importance
- Top Prediction Reasons
- Explain Prediction Result

## Dashboard Analytics

- KPI Summary
- Prediction Trend
- Top Risk Employees
- Recent Predictions
- Feature Importance
- Employee Health Score

## MLOps

- MLflow Experiment Tracking
- Model Versioning
- Model Metrics Tracking
- Artifact Storage

## Reporting

- Export Excel
- Export PDF

## Infrastructure

- Docker Compose
- PostgreSQL 17
- Alembic Migration
- Nginx Reverse Proxy
- HTTPS SSL
- GitHub Actions CI/CD

---

# Architecture

```text
                    Internet
                        │
                        ▼
                   NGINX SSL
                        │
        ┌───────────────┼───────────────┐
        ▼                               ▼
    React Frontend                 FastAPI Backend
                                         │
                    ┌────────────────────┴────────────────────┐
                    ▼                                         ▼
              PostgreSQL 17                              MLflow
                    │
                    ▼
            Random Forest Model
                    │
                    ▼
              SHAP Explainability
```

---

# Tech Stack

## Backend

- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- JWT Authentication
- Pydantic

## Frontend

- React
- Vite
- Axios
- Recharts
- React Router

## Machine Learning

- Scikit-Learn
- Random Forest
- Pandas
- NumPy
- SHAP

## MLOps

- MLflow

## Infrastructure

- Docker
- Docker Compose
- Nginx
- GitHub Actions

---

# Project Structure

```text
employee-ai-system/
│
├── backend/
│   ├── alembic/
│   ├── app/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── services/
│   │   ├── schemas/
│   │   ├── database/
│   │   └── core/
│   │
│   ├── trained_models/
│   ├── scripts/
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── Dockerfile.mlflow
│   └── alembic.ini
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── Dockerfile.prod
│
├── nginx/
│   └── nginx.conf
│
├── docker-compose.yml
├── .env
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/aasyhadi/employee-ai-system.git

cd employee-ai-system
```

---

# Environment Variables

Create:

```bash
.env
```

```env
POSTGRES_DB=employee_ai

POSTGRES_USER=postgres

POSTGRES_PASSWORD=postgres123

DATABASE_URL=postgresql://postgres:postgres123@postgres:5432/employee_ai

SECRET_KEY=employee-ai-secret-key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

# Run With Docker

Build:

```bash
docker compose build
```

Start:

```bash
docker compose up -d
```

Check:

```bash
docker ps
```

---

# Access Application

## Frontend

```text
http://localhost
```

## Backend Swagger

```text
http://localhost/api/docs
```

## MLflow

```text
http://localhost:5000
```

---

# Database Migration

Initialize Alembic:

```bash
alembic init alembic
```

Create Migration:

```bash
alembic revision --autogenerate -m "initial migration"
```

Run Migration:

```bash
alembic upgrade head
```

Check Current Version:

```bash
alembic current
```

Rollback:

```bash
alembic downgrade -1
```

---

# Machine Learning Training

Run Training:

```bash
docker compose exec backend python scripts/train_model.py
```

Model Artifact:

```text
backend/trained_models/
```

---

# MLflow Tracking

Tracking URI:

```python
mlflow.set_tracking_uri(
    "sqlite:////app/mlflow.db"
)
```

Experiment:

```python
mlflow.set_experiment(
    "employee-attrition-randomforest"
)
```

Open:

```text
http://localhost:5000
```

---

# SHAP Explainability

Generate Explanation:

```python
get_top_reasons(input_df)
```

Example Output:

```json
{
  "prediction": "Yes",
  "probability": 0.87,
  "top_reasons": [
    "OverTime",
    "JobSatisfaction",
    "MonthlyIncome"
  ]
}
```

---

# API Endpoints

## Authentication

### Login

```http
POST /api/auth/login
```

### Register

```http
POST /api/auth/register
```

---

## Employee

### Get Employees

```http
GET /api/employees
```

### Get Employee

```http
GET /api/employees/{id}
```

### Create Employee

```http
POST /api/employees
```

### Update Employee

```http
PUT /api/employees/{id}
```

### Delete Employee

```http
DELETE /api/employees/{id}
```

---

## Prediction

### Predict Attrition

```http
POST /api/predictions/predict
```

### Prediction History

```http
GET /api/predictions
```

---

## Dashboard

### Summary

```http
GET /api/dashboard/summary
```

### Prediction Trend

```http
GET /api/dashboard/trend
```

### Top Risk Employees

```http
GET /api/dashboard/top-risk
```

### Feature Importance

```http
GET /api/model/feature-importance
```

---

# Production Deployment

## VPS

Recommended:

```text
Ubuntu 24.04
2 vCPU
4 GB RAM
50 GB SSD
```

---

## Nginx

Frontend:

```text
https://employee-ai.company.com
```

Backend:

```text
https://employee-ai.company.com/api/docs
```

---

## SSL

Install:

```bash
apt install certbot python3-certbot-nginx
```

Generate:

```bash
certbot --nginx \
-d employee-ai.company.com
```

---

# CI/CD

Workflow:

```text
Push GitHub
      ↓
GitHub Actions
      ↓
SSH VPS
      ↓
Git Pull
      ↓
Docker Build
      ↓
Docker Deploy
```

Workflow File:

```text
.github/workflows/deploy.yml
```

---

# Monitoring

## Application

```bash
docker compose logs -f backend
```

## MLflow

```bash
docker compose logs -f mlflow
```

## Nginx

```bash
docker compose logs -f nginx
```

---

# Backup Database

Manual Backup:

```bash
docker compose exec -T postgres \
pg_dump -U postgres employee_ai \
> backup.sql
```

Restore:

```bash
docker compose exec -T postgres \
psql -U postgres employee_ai \
< backup.sql
```

---

# Future Roadmap

- Model Registry
- Multi Model Comparison
- XGBoost Integration
- LightGBM Integration
- Employee Recommendation Engine
- Email Notification
- WhatsApp Notification
- Kubernetes Deployment
- Prometheus Monitoring
- Grafana Dashboard

---

# Learning Outcomes

This project covers:

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- React
- Docker
- Nginx
- Machine Learning
- Explainable AI
- MLflow
- MLOps
- CI/CD
- VPS Deployment

---

# License

MIT License

---

# Author

Employee AI System

Built with:

- FastAPI
- React
- PostgreSQL
- Docker
- MLflow
- SHAP