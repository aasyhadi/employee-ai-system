from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.auth_schema import RegisterRequest, UserResponse
from app.services.auth_service import register_user

from app.schemas.auth_schema import LoginRequest, TokenResponse
from app.services.auth_service import login_user

from app.core.auth import get_current_user
from app.models.user_model import User

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post("/register", response_model=UserResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    user = register_user(db, request)

    if user is None:
        raise HTTPException(
            status_code=400,
            detail="Email sudah terdaftar"
        )

    return user

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    token = login_user(db, request)

    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Email atau password salah"
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role
    }